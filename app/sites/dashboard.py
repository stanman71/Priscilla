from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app, socketio
from app.database.models         import *
from app.backend.led             import *
from app.backend.spotify         import *
from app.backend.mqtt            import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD
from app.backend.process_program import *
from app.common                  import COMMON, STATUS
from app.assets                  import *

from lms import find_server

import os, shutil, re, cgi


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        #try:
        if current_user.role == "dashboard_only" or current_user.role == "user" or current_user.role == "administrator":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout'))
        #except Exception as e:
        #    print(e)
        #    return redirect(url_for('logout'))
        
    return wrap


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@permission_required
def dashboard():

    # custommize your page title / description here
    page_title       = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'


    """ ############### """
    """  led / devices  """
    """ ############### """   

    if "apply_changes_led_devices" != None: 

        for i in range (1,26):
            
            # led 

            try:

                group      = GET_LED_GROUP_BY_ID(i)
                scene      = GET_LED_SCENE_BY_ID(request.form.get("set_led_scene_" + str(i)))
                brightness = request.form.get("set_brightness_" + str(i))

                # new led setting ?
                if group.current_setting != scene.name or int(group.current_brightness) != brightness:
                    
                    SET_LED_GROUP_SCENE(group.id, scene.id, brightness)
                    CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

            except:
                pass
            
            # devices

            try:    

                device              = GET_DEVICE_BY_ID(i)
                device_setting_json = request.form.get("set_command_" + str(i))

                # convert json-format to string
                device_setting_string = device_setting_json.replace('"', '')
                device_setting_string = device_setting_string.replace('{', '')
                device_setting_string = device_setting_string.replace('}', '')
                
                check_result = CHECK_DEVICE_EXCEPTIONS(i, device_setting_string)    


                # check device exception
                check_result = CHECK_DEVICE_EXCEPTIONS(device.id, device_setting_string)
                    
                if check_result == True:               
            
                    new_setting = False
                    
                    # new device setting ?  
                    if device.last_values_json != None:
                        
                        # one setting value
                        if not "," in device_setting_json:
                            if not device_setting_json[1:-1] in device.last_values_json:
                                new_setting = True
                                                                
                        # more then one setting value
                        else:
                            device_setting_temp  = device_setting_json[1:-1]
                            list_device_settings = device_setting_temp.split(",")
                            
                            for setting in list_device_settings:
                                
                                if not setting in device.last_values_json:
                                    new_setting = True                      

                    else:
                        new_setting = True
                                
                                
                    if new_setting == True:    

                        if device.gateway == "mqtt":
                            channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                        if device.gateway == "zigbee2mqtt":   
                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                        heapq.heappush(mqtt_message_queue, (1, (channel, device_setting_json)))            
                        CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, device_setting_json, 20)            

            except:
                pass        


    """ ########## """
    """  programs  """
    """ ########## """   

    if request.form.get("start_program") != None:
        START_PROGRAM_THREAD(request.form.get("select_program"))

        if request.form.get("checkbox_program_repeat") == "on":
            SET_REPEAT_PROGRAM(True)
        else:
            SET_REPEAT_PROGRAM(False)

    if request.form.get("stop_program") != None:
        STOP_PROGRAM_THREAD()   
        SET_REPEAT_PROGRAM(False)


    """ ####### """
    """  music  """
    """ ####### """   

    spotify_token = GET_SPOTIFY_TOKEN()

    if spotify_token != "":

        try:

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False     
            spotify_volume = request.form.get("slider_spotify_volume") 

            if "set_spotify_play" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       

                device_name = sp.current_playback(market=None)['device']['name']

                if "multiroom" in device_name:
                    server = find_server()

                    for player in server.players:
                            player.set_volume(spotify_volume)       

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)                         


            if "set_spotify_previous" in request.form: 
                SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)       

      
            if "set_spotify_next" in request.form:
                SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)       


            if "set_spotify_stop" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)       


            if "set_spotify_volume" in request.form: 
                device_name = sp.current_playback(market=None)['device']['name']

                if "multiroom" not in device_name:
                    SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  

                else:
                    SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)  

                    server  = find_server()

                    for player in server.players:
                            player.set_volume(spotify_volume)
            
                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", spotify_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", spotify_volume)       


            # ##############
            # start playlist
            # ##############

            if "spotify_start_playlist" in request.form:    
                spotify_device_id = request.form.get("set_spotify_device_id")
                playlist_uri      = request.form.get("set_spotify_playlist")
                
                SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, spotify_volume)

                time.sleep(1)

                device_name = sp.current_playback(market=None)['device']['name']

                if "multiroom" in device_name:
                    server  = find_server()

                    for player in server.players:
                            player.set_volume(spotify_volume)          


            # ############
            # account data
            # ############

            spotify_devices   = sp.devices()["devices"]        
            spotify_playlists = sp.current_user_playlists(limit=20)["items"]                        

            # get volume
            spotify_volume = str(GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[3])

            # get shuffle            
            if GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[8] == True:
                spotify_shuffle = "True"
            else:
                spotify_shuffle = "False"         


        # login failed
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Spotify | " + str(e)) 
            SEND_EMAIL("ERROR", "Spotify | " + str(e)) 
            
            spotify_playlists = ""
            spotify_devices   = ""
            spotify_volume    = 50         
            spotify_shuffle   = "False"


    # not logged in
    else:     
        spotify_playlists = ""
        spotify_devices   = ""
        spotify_volume    = 50     
        spotify_shuffle   = "False"


    dropdown_list_led_scenes = GET_ALL_LED_SCENES()
    list_led_groups          = GET_ALL_LED_GROUPS()
    list_devices             = GET_ALL_DEVICES("devices")

    dropdown_list_programs   = GET_ALL_PROGRAMS()
    program_repeat           = str(GET_REPEAT_PROGRAM())

    data = {'navigation': 'dashboard'}

    return render_template('layouts/default.html',
                            async_mode=socketio.async_mode,
                            data=data,
                            content=render_template( 'pages/dashboard.html', 
                                                    list_led_groups=list_led_groups,
                                                    dropdown_list_led_scenes=dropdown_list_led_scenes,      
                                                    spotify_playlists=spotify_playlists,
                                                    spotify_devices=spotify_devices, 
                                                    spotify_volume=spotify_volume, 
                                                    spotify_shuffle=spotify_shuffle,
                                                    list_devices=list_devices,    
                                                    dropdown_list_programs=dropdown_list_programs,
                                                    program_repeat=program_repeat,                                                            
                                                    ) 
                           )      