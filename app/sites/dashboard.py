from flask                     import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login               import current_user, login_required
from werkzeug.exceptions       import HTTPException, NotFound, abort
from functools                 import wraps
from flask_mobility.decorators import mobile_template

from app                         import app, socketio
from app.backend.database_models import *
from app.backend.lighting        import *
from app.backend.spotify         import *
from app.backend.mqtt            import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD
from app.backend.process_program import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.common                  import COMMON, STATUS
from app.assets                  import *


import os, shutil, re, cgi


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
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@permission_required
def dashboard():
    page_title       = 'homatiX | Dashboard'
    page_description = 'The main page and Dashboard'


    """ ############################ """
    """  lightings_groups / devices  """
    """ ############################ """   

    if request.form.get("apply_changes_lighting_groups_devices") != None: 

        for i in range (1,101):
            
            # ########
            # lighting 
            # ########

            try:
                group      = GET_LIGHTING_GROUP_BY_ID(i)
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

            except:
                pass


            # #######
            # devices
            # #######

            try:    

                device         = GET_DEVICE_BY_ID(i)
                device_setting = request.form.get("set_command_" + str(i))

                if device_setting != None and device_setting != "None":

                    # check device exception
                    check_result = CHECK_DEVICE_EXCEPTIONS(device.id, device_setting)
                        
                    if check_result == True:               

                        if device.gateway == "mqtt":
                            channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                        if device.gateway == "zigbee2mqtt":   
                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                        command_position  = 0
                        list_command_json = device.commands_json.replace("},{", "};{")                       
                        list_command_json = list_command_json.split(";")

                        # get the json command statement and start process
                        for command in device.commands.split(","):     
                                            
                            if str(device_setting.lower()) == command.lower():    
                                heapq.heappush(mqtt_message_queue, (1, (channel, list_command_json[command_position])))            
                                CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, device_setting, 45)      
                                break

                            command_position = command_position + 1

                    else:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Network | " + check_result)       

            except:
                pass        

        time.sleep(5)


    """ ########## """
    """  programs  """
    """ ########## """   

    if request.form.get("start_program") != None:
        START_PROGRAM_THREAD(request.form.get("select_program"))


    """ ####### """
    """  music  """
    """ ####### """   

    spotify_token = GET_SPOTIFY_TOKEN()

    if spotify_token != "":

        try:

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False     
            
            # ############
            # account data
            # ############

            list_spotify_devices   = sp.devices()["devices"]        
            list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]                        

            # get volume
            spotify_volume = str(GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[3])

            # get shuffle            
            if GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[8] == True:
                spotify_shuffle = "True"
            else:
                spotify_shuffle = "False"     


            # ##############
            # player control
            # ##############

            if "set_spotify_play" in request.form:  
                spotify_volume = request.form.get("slider_spotify_volume") 
                SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       

            if "set_spotify_previous" in request.form: 
                spotify_volume = request.form.get("slider_spotify_volume") 
                SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   
      
            if "set_spotify_next" in request.form:
                spotify_volume = request.form.get("slider_spotify_volume") 
                SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

            if "set_spotify_stop" in request.form:  
                spotify_volume = request.form.get("slider_spotify_volume") 
                SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

            if "set_spotify_shuffle" in request.form:  
                spotify_volume = request.form.get("slider_spotify_volume") 

                if spotify_shuffle == "True":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)   
                    spotify_shuffle = "False" 
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)   
                    spotify_shuffle = "True"                 

            if "set_spotify_volume" in request.form: 
                spotify_volume = request.form.get("slider_spotify_volume") 
                SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  
            

            # ##############
            # start playlist
            # ##############

            if "spotify_start_playlist" in request.form:    
                spotify_device_id = request.form.get("set_spotify_device_id")
                playlist_uri      = request.form.get("set_spotify_playlist")
                spotify_volume    = request.form.get("slider_spotify_volume") 
                
                SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, spotify_volume)


        # login failed
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | " + str(e)) 
            SEND_EMAIL("ERROR", "Music | Spotify | " + str(e)) 
            
            list_spotify_playlists = ""
            list_spotify_devices   = ""
            spotify_volume         = 50         
            spotify_shuffle        = "False"


    # not logged in
    else:     
        list_spotify_playlists = ""
        list_spotify_devices   = ""
        spotify_volume         = 50     
        spotify_shuffle        = "False"


    dropdown_list_lighting_scenes = GET_ALL_LIGHTING_SCENES()
    list_lighting_groups          = GET_ALL_LIGHTING_GROUPS()
    list_devices                  = GET_ALL_DEVICES("devices")

    dropdown_list_programs   = GET_ALL_PROGRAMS()

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
                                                    ) 
                           )      