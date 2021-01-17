from flask                        import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                  import current_user, login_required
from werkzeug.exceptions          import HTTPException, NotFound, abort
from functools                    import wraps

from app                          import app
from app.backend.database_models  import *
from app.backend.spotify          import *
from app.backend.shared_resources import mqtt_message_queue, GET_MQTT_INCOMING_MESSAGES, GET_MQTT_CONNECTION_STATUS
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.user_id          import SET_CURRENT_USER_ID
from app.common                   import COMMON, STATUS
from app.assets                   import *

from lms import find_server

import requests
import json
import spotipy
import socket 
import heapq
import threading


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "user" or current_user.role == "administrator":
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


list_search_track_results = ""
list_search_album_results = ""



@app.route('/music', methods=['GET', 'POST'])
@login_required
@permission_required
def music():    
    page_title       = 'Bianca | Music'
    page_description = 'The music configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    global list_search_track_results
    global list_search_album_results
    global timeout_spotify

    spotify_token = GET_SPOTIFY_TOKEN()
    spotify_data  = GET_SPOTIFY_CONTROL_DATA(spotify_token)

    spotify_user           = spotify_data[0]
    list_spotify_devices   = spotify_data[1]
    list_spotify_playlists = spotify_data[2]
    spotify_volume         = spotify_data[3]
    spotify_shuffle        = spotify_data[4]

    UPDATE_MULTIROOM_DEFAULT_SETTINGS()

    error_message_search_track                   = ""
    error_message_search_album                   = ""
    error_message_spotify                        = ""
    success_message_change_settings_client_music = []
    error_message_change_settings_client_music   = [] 
    success_message_change_default_settings      = False

    track_name   = ""
    track_artist = ""
    album_name   = "" 
    album_artist = ""  

    show_player = False
    
    collapse_search_track_open = ""   
    collapse_search_album_open = ""        


    """ ################# """
    """  spotify control  """
    """ ################# """   

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

        if "set_spotify_volume" in request.form: 
            SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)        

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
            playlist_volume   = request.form.get("set_spotify_playlist_volume")

            if request.form.get("set_checkbox_shuffle_setting") != None:
                playlist_shuffle = True
            else:
                playlist_shuffle = False

            SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume, playlist_shuffle)

            spotify_volume = playlist_volume


        # ############
        # search track
        # ############
    
        if "spotify_search_track" in request.form:     
            collapse_search_track_open = "True"   

            track_name   = request.form.get("set_spotify_search_track").strip()  
            track_artist = request.form.get("set_spotify_search_track_artist").strip()  
            
            list_search_track_results = SPOTIFY_SEARCH_TRACK(spotify_token, track_name, track_artist, 10)
        
            # check results found ?
            if isinstance(list_search_track_results, str):
                error_message_search_track = list_search_track_results
                list_search_track_results  = []  

        if "spotify_track_play" in request.form:       
            collapse_search_track_open = "True"  
            
            track_uri         = request.form.get("spotify_track_play")
            spotify_device_id = request.form.get("set_spotify_track_device:" + track_uri)
            track_volume      = request.form.get("set_spotify_track_volume:" + track_uri)
            
            SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)

            spotify_volume = track_volume   


        # ############
        # search album
        # ############
    
        if "spotify_search_album" in request.form:     
            collapse_search_album_open = "True"  

            album_name   = request.form.get("set_spotify_search_album").strip()  
            album_artist = request.form.get("set_spotify_search_album_artist").strip()  

            list_search_album_results = SPOTIFY_SEARCH_ALBUM(spotify_token, album_name, album_artist, 5)  

            # check results found ?
            if isinstance(list_search_album_results, str):
                error_message_search_album = list_search_album_results 
                list_search_album_results  = []  
                                
        if "spotify_album_play" in request.form:   
            collapse_search_album_open = "True" 
            
            album_uri         = request.form.get("spotify_album_play")
            spotify_device_id = request.form.get("set_spotify_album_device:" + album_uri)
            album_volume      = request.form.get("set_spotify_album_volume:" + album_uri)
            
            SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)

            spotify_volume = album_volume  


    """ ############## """
    """  music volume  """
    """ ############## """   

    if request.method == 'POST':
        if (spotify_token != "" and 
            timeout_spotify == 0 and 
            request.form.get("set_spotify_player_volume") != None):

            timeout_spotify = 1
            START_TIMEOUT_SPOTIFY_THREAD()

            spotify_volume = request.form.get("set_spotify_player_volume") 
            SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume) 


    """ ################## """
    """  default settings  """
    """ ################## """   

    if request.form.get("save_default_settings") != None:

        spotify_default_device_id   = request.form.get("set_spotify_default_device_id") 
        spotify_default_device_name = ""

        for device in list_spotify_devices:    
            if device['id'] == spotify_default_device_id:
                spotify_default_device_name = device['name']

        spotify_default_playlist_uri  = request.form.get("set_spotify_default_playlist_uri") 
        spotify_default_playlist_name = ""

        for playlist in list_spotify_playlists:    
            if playlist['uri'] == spotify_default_playlist_uri:
                spotify_default_playlist_name = playlist['name']      

        spotify_default_volume = request.form.get("set_spotify_default_volume") 

        if request.form.get("set_checkbox_default_shuffle_setting") != None:
            spotify_default_shuffle = "True"
        else:
            spotify_default_shuffle = "False"
            

        if SET_SPOTIFY_DEFAULT_SETTINGS(spotify_default_device_id, 
                                        spotify_default_device_name, 
                                        spotify_default_playlist_uri, 
                                        spotify_default_playlist_name, 
                                        spotify_default_volume, 
                                        spotify_default_shuffle):

            success_message_change_default_settings = True  


    """ #################### """
    """  table client_music  """
    """ #################### """   

    if GET_MQTT_CONNECTION_STATUS() == True:

        if request.form.get("save_client_music_settings") != None:
            
            for i in range (1,26):

                if request.form.get("set_radio_client_music_interface_" + str(i)) != None:
        
                    client_music_interface = request.form.get("set_radio_client_music_interface_" + str(i))
                    client_music_volume    = request.form.get("set_client_music_volume_" + str(i))                
                    device                 = GET_DEVICE_BY_ID(i)

                    # devices without volume control support
                    if client_music_volume == None:
                        client_music_volume = 0 

                    # last values found
                    try:
                        data = json.loads(device.last_values_json)
                        
                        if client_music_interface != data["interface"] or str(client_music_volume) != str(data["volume"]):

                            heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"' + client_music_interface + '","volume":' + str(client_music_volume) + '}')))     

                            result = CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, client_music_interface + '; ' + str(client_music_volume), 45)
                            
                            if result != True:
                                error_message_change_settings_client_music.append(result)
                            else:
                                success_message_change_settings_client_music.append(device.name + " || Settings successfully saved")
                                
                                # update last values for GUI
                                try:
                                    for message in GET_MQTT_INCOMING_MESSAGES(5):              
                    
                                        if message[1] == "smarthome/mqtt/" + device.ieeeAddr:                
                                            SAVE_DEVICE_LAST_VALUES(device.ieeeAddr, message[2])
                                            break

                                except:
                                    pass
                                        
                    # no valid last values existing                        
                    except:

                        heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"' + client_music_interface + '","volume":' + str(client_music_volume) + '}')))     

                        result = CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, client_music_interface + '; ' + str(client_music_volume), 45)
                        
                        if result != True:
                            error_message_change_settings_client_music.append(result)
                        else:
                            success_message_change_settings_client_music.append(device.name + " || Settings successfully saved")
                            
                            # update last values for GUI
                            try:
                                for message in GET_MQTT_INCOMING_MESSAGES(5):              
                
                                    if message[1] == "smarthome/mqtt/" + device.ieeeAddr:                
                                        SAVE_DEVICE_LAST_VALUES(device.ieeeAddr, message[2])
                                        break

                            except:
                                pass


        if request.form.get("restart_client_music_services") != None:
            list_client_music = GET_ALL_DEVICES("client_music")

            for client_music in list_client_music:
                heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + client_music.ieeeAddr + "/set", '{"interface":"restart"}')))  

    else:
        error_message_change_settings_client_music.append("No MQTT connection")

    list_client_music = GET_ALL_DEVICES("client_music")
    default_settings  = GET_SPOTIFY_SETTINGS()

    data = {'navigation': 'music'}    

    return render_template('layouts/default.html',
                            data=data,
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/music.html',
                                                    error_message_search_track=error_message_search_track,
                                                    error_message_search_album=error_message_search_album,
                                                    error_message_spotify=error_message_spotify,
                                                    success_message_change_settings_client_music=success_message_change_settings_client_music,
                                                    error_message_change_settings_client_music=error_message_change_settings_client_music, 
                                                    success_message_change_default_settings=success_message_change_default_settings,
                                                    spotify_user=spotify_user,  
                                                    list_spotify_playlists=list_spotify_playlists,
                                                    list_spotify_devices=list_spotify_devices, 
                                                    list_search_track_results=list_search_track_results, 
                                                    list_search_album_results=list_search_album_results,     
                                                    show_player=show_player,
                                                    track_name=track_name,
                                                    track_artist=track_artist,     
                                                    album_name=album_name,
                                                    album_artist=album_artist,   
                                                    spotify_volume=spotify_volume, 
                                                    spotify_shuffle=spotify_shuffle,
                                                    default_settings=default_settings,
                                                    list_client_music=list_client_music,
                                                    collapse_search_track_open=collapse_search_track_open,   
                                                    collapse_search_album_open=collapse_search_album_open,     
                                                    ) 
                           )


@app.route("/music/spotify/login")
@login_required
@permission_required
def spotify_login():
    return redirect(GET_SPOTIFY_AUTHORIZATION()) 
 
 
@app.route("/music/spotify/token")
@login_required
@permission_required
def spotify_token():
    GENERATE_SPOTIFY_TOKEN(request.args['code'])
    return redirect(url_for('music'))
      

@app.route("/music/spotify/logout")
@login_required
@permission_required
def spotify_logout():
    DELETE_SPOTIFY_TOKEN()
    WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Logout") 
    return redirect(url_for('music'))      