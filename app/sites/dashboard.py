from flask                        import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                  import current_user, login_required
from werkzeug.exceptions          import HTTPException, NotFound, abort
from functools                    import wraps

from app                          import app, socketio
from app.backend.database_models  import *
from app.backend.lighting         import *
from app.backend.music            import *
from app.backend.mqtt             import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.backend.user_id          import SET_CURRENT_USER_ID
from app.common                   import COMMON, STATUS
from app.assets                   import *

import threading

# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "dashboard_only" or current_user.role == "user" or current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################") 
            return redirect(url_for('logout'))
        
    return wrap


# timeout spotify
timeout_spotify = 0

def START_TIMEOUT_SPOTIFY_THREAD():
	try:
		Thread = threading.Thread(target=TIMEOUT_SPOTIFY_THREAD)
		Thread.start()  
		
	except:
		pass

def TIMEOUT_SPOTIFY_THREAD():   
    global timeout_spotify
    
    time.sleep(1)
    timeout_spotify = 0



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@permission_required
def dashboard():
    page_title       = 'Bianca | Dashboard'
    page_description = 'The main page and Dashboard'

    SET_CURRENT_USER_ID(current_user.id)    

    # prevent timeout errors
    global timeout_spotify

    spotify_token = GET_SPOTIFY_TOKEN()
    spotify_data  = GET_SPOTIFY_CONTROL_DATA(spotify_token)

    list_spotify_devices   = spotify_data[1]
    list_spotify_playlists = spotify_data[2]
    spotify_volume         = spotify_data[3]
    spotify_shuffle        = spotify_data[4]
    

    """ ############################ """
    """  lightings_groups / devices  """
    """ ############################ """   

    if request.form.get("apply_changes_lighting_groups_devices") != None: 

        for i in range (1,100):
            
            # ########
            # lighting 
            # ########

            try:
                group = GET_LIGHTING_GROUP_BY_ID(i)

                if group.light_ieeeAddr_1 != "None":

                    scene_name = str(request.form.get("set_lighting_group_scene_" + str(i)))
                    brightness = request.form.get("set_lighting_group_brightness_" + str(i))
                    scene      = GET_LIGHTING_SCENE_BY_NAME(scene_name)

                    if scene_name == "OFF":
                        if group.current_scene != "OFF":
                            SET_LIGHTING_GROUP_TURN_OFF(group.id)
                            CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 2, 10)

                    else:
                        if group.current_scene != scene_name or int(group.current_brightness) != int(brightness):
                            SET_LIGHTING_GROUP_SCENE(group.id, scene.id, int(brightness))
                            CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, int(brightness), 2, 10)

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Start_Scene | Group | " + str(group.name) + " | empty")

            except:
                pass

            # #######
            # devices
            # #######

            try:    

                device            = GET_DEVICE_BY_ID(i)
                dashboard_command = request.form.get("set_command_" + str(i))

                if dashboard_command != None and dashboard_command != "None":

                    # check device exception
                    
                    check_result = CHECK_DEVICE_EXCEPTIONS(device.ieeeAddr, dashboard_command)

                    if check_result == True:               

                        # generate mqtt channel

                        if device.gateway == "mqtt":
                            if device.model == "xiaomi_mi" or device.model == "roborock_s50":
                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/command"  
                            else:
                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  

                        if device.gateway == "zigbee2mqtt":   
                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                        # generate list of commands

                        if device.model == "xiaomi_mi" or device.model == "roborock_s50":
                            list_command_json = device.commands_json.split(",")

                        else:
                            list_command_json = device.commands_json.replace("},{", "};{")                       
                            list_command_json = list_command_json.split(";")

                        command_position  = 0                           

                        # get the json command statement and start process

                        for command in device.commands.split(","):     
                                            
                            if str(dashboard_command.lower()) == command.lower():

                                if (device.model == "xiaomi_mi" or device.model == "roborock_s50") and dashboard_command.lower() == "return_to_base":
                                    heapq.heappush(mqtt_message_queue, (10, (channel, "stop")))            
                                    time.sleep(5)
                                    heapq.heappush(mqtt_message_queue, (10, (channel, "return_to_base")))                               
                                    CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, dashboard_command.lower(), dashboard_command, 50)  

                                elif device.model == "xiaomi_mi" or device.model == "roborock_s50" and dashboard_command.lower() == "locate":
                                    heapq.heappush(mqtt_message_queue, (10, (channel, "locate")))  

                                else:
                                    heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                                    CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, list_command_json[command_position], dashboard_command, 50)      

                            command_position = command_position + 1

                    else:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Network | " + check_result)       

            except:
                pass        


    """ ########## """
    """  programs  """
    """ ########## """   

    if request.form.get("start_program") != None:
        program_id = request.form.get("select_program")
        heapq.heappush(process_management_queue, (10, ("program", "start", program_id))) 


    """ ####### """
    """  music  """
    """ ####### """   

    if ("set_spotify_play" in request.form or 
        "set_spotify_previous" in request.form or
        "set_spotify_next" in request.form or
        "set_spotify_stop" in request.form or
        "set_spotify_shuffle" in request.form or
        "spotify_start_playlist" in request.form):

        if spotify_token != "":

            # ##############
            # player control
            # ##############

            if "set_spotify_play" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "play")       

            if "set_spotify_previous" in request.form: 
                SPOTIFY_CONTROL(spotify_token, "previous")   
    
            if "set_spotify_next" in request.form:
                SPOTIFY_CONTROL(spotify_token, "next")     

            if "set_spotify_stop" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "stop")   

            if "set_spotify_shuffle" in request.form:  

                if spotify_shuffle == "True":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false")   
                    spotify_shuffle = "False" 
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true")   
                    spotify_shuffle = "True"                 

            # ##############
            # start playlist
            # ##############

            if "spotify_start_playlist" in request.form:    
                spotify_device_id = request.form.get("set_spotify_device_id")
                playlist_uri      = request.form.get("set_spotify_playlist")
                
                SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, spotify_volume)


    """ ############## """
    """  music volume  """
    """ ############## """   

    if request.method == 'POST':
        if (spotify_token != "" and 
            timeout_spotify == 0 and 
            request.form.get("set_spotify_volume") != None):

            timeout_spotify = 1
            START_TIMEOUT_SPOTIFY_THREAD()

            spotify_volume = request.form.get("set_spotify_volume") 
            SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume) 


    """ ###### """
    """  logs  """
    """ ###### """   

    if request.form.get("apply_changes_log_show_exceptions") != None:
        log_setting = request.form.get("set_radio_show_messages")
        SET_DASHBOARD_LOG_SHOW_EXCEPTIONS(current_user.id, log_setting)


    dropdown_list_lighting_scenes = GET_ALL_LIGHTING_SCENES()
    list_lighting_groups          = GET_ALL_LIGHTING_GROUPS()
    list_devices                  = GET_ALL_DEVICES("devices")

    dropdown_list_programs = GET_ALL_PROGRAMS()
    log_show_exceptions    = current_user.dashboard_log_show_exceptions      

    data = {'navigation': 'dashboard'}

    return render_template('layouts/default.html',
                            async_mode=socketio.async_mode,
                            data=data,
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/dashboard.html', 
                                                    list_lighting_groups=list_lighting_groups,
                                                    dropdown_list_lighting_scenes=dropdown_list_lighting_scenes,
                                                    spotify_token=spotify_token,      
                                                    list_spotify_playlists=list_spotify_playlists,
                                                    list_spotify_devices=list_spotify_devices, 
                                                    spotify_volume=spotify_volume, 
                                                    spotify_shuffle=spotify_shuffle,
                                                    list_devices=list_devices,    
                                                    dropdown_list_programs=dropdown_list_programs,    
                                                    log_show_exceptions=log_show_exceptions,                                              
                                                    ) 
                           )      