from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.spotify          import *
from app.backend.shared_resources import mqtt_message_queue, GET_MQTT_INCOMING_MESSAGES, GET_DEVICE_CONNECTION_MQTT
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.common                   import COMMON, STATUS
from app.assets                   import *


from lms import find_server

import requests
import json
import spotipy
import socket 
import heapq

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
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


list_search_track_results = ""
list_search_album_results = ""


@app.route('/music', methods=['GET', 'POST'])
@login_required
@permission_required
def music():    
    page_title = 'Smarthome | Music'
    page_description = 'The music configuration page.'

    global list_search_track_results
    global list_search_album_results

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
    
    spotify_token = GET_SPOTIFY_TOKEN()


    """ ################# """
    """  spotify control  """
    """ ################# """   

    if spotify_token != "":

        try:

            sp            = spotipy.Spotify(auth=spotify_token)
            sp.trace      = False     
            player_volume = request.form.get("set_spotify_player_volume") 

            if "set_spotify_play" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "play", player_volume)       

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", player_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", player_volume)                         


            if "set_spotify_previous" in request.form: 
                SPOTIFY_CONTROL(spotify_token, "previous", player_volume)   

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", player_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", player_volume)       

      
            if "set_spotify_next" in request.form:
                SPOTIFY_CONTROL(spotify_token, "next", player_volume)     

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", player_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", player_volume)       


            if "set_spotify_stop" in request.form:  
                SPOTIFY_CONTROL(spotify_token, "stop", player_volume)   

                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", player_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", player_volume)       


            if "set_spotify_volume" in request.form: 
                device_name = sp.current_playback(market=None)['device']['name']
                SPOTIFY_CONTROL(spotify_token, "volume", player_volume)                  
      
                if request.form.get("checkbox_shuffle") == "on":
                    SPOTIFY_CONTROL(spotify_token, "shuffle_true", player_volume)
                else:
                    SPOTIFY_CONTROL(spotify_token, "shuffle_false", player_volume)       


            # ##############
            # start playlist
            # ##############

            if "spotify_start_playlist" in request.form:    
                spotify_device_id = request.form.get("set_spotify_device_id")
                playlist_uri      = request.form.get("set_spotify_playlist")
                playlist_volume   = request.form.get("set_spotify_playlist_volume")
                
                SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)


            # ############
            # search track
            # ############
        
            if "spotify_search_track" in request.form:     
                collapse_search_track_open = "True"   

                track_name   = request.form.get("set_spotify_search_track").strip()  
                track_artist = request.form.get("set_spotify_search_track_artist").strip()  
                
                list_search_track_results = SPOTIFY_SEARCH_TRACK(spotify_token, track_name, track_artist, 10)
            
                # check results founded ?
                if isinstance(list_search_track_results, str):
                    error_message_search_track = list_search_track_results
                    list_search_track_results  = []  
                          
            if "spotify_track_play" in request.form:       
                collapse_search_track_open = "True"  
                
                track_uri         = request.form.get("spotify_track_play")
                spotify_device_id = request.form.get("set_spotify_track_device:" + track_uri)
                track_volume      = request.form.get("set_spotify_track_volume:" + track_uri)
                
                SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)


            # ############
            # search album
            # ############
        
            if "spotify_search_album" in request.form:     
                collapse_search_album_open = "True"  

                album_name   = request.form.get("set_spotify_search_album").strip()  
                album_artist = request.form.get("set_spotify_search_album_artist").strip()  

                list_search_album_results = SPOTIFY_SEARCH_ALBUM(spotify_token, album_name, album_artist, 5)  
    
                # check results founded ?
                if isinstance(list_search_album_results, str):
                    error_message_search_album = list_search_album_results 
                    list_search_album_results  = []  
                                   
            if "spotify_album_play" in request.form:   
                collapse_search_album_open = "True" 
                
                album_uri         = request.form.get("spotify_album_play")
                spotify_device_id = request.form.get("set_spotify_album_device:" + album_uri)
                album_volume      = request.form.get("set_spotify_album_volume:" + album_uri)
                
                SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)
    
 
            # ############
            # account data
            # ############
                     
            spotify_user           = sp.current_user()["display_name"]   
            list_spotify_devices   = sp.devices()["devices"]        
            list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]    


            # player show ?
            if GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token) != ('', '', '', '', '', [], '', '', ''):
                show_player = True                             

            # get volume
            volume = str(GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[3])

            # get shuffle            
            if GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)[8] == True:
                shuffle = "True"
            else:
                shuffle = "False"         


        # login failed
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | " + str(e)) 
            SEND_EMAIL("ERROR", "Spotify | " + str(e)) 
            
            spotify_user = ""
            list_spotify_playlists = ""
            list_spotify_devices = ""
            volume = 50         
            shuffle = "False"


    # not logged in
    else:     
        spotify_user           = ""
        list_spotify_playlists = ""
        list_spotify_devices   = ""
        volume                 = 50     
        shuffle                = "False"


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

        if SET_SPOTIFY_DEFAULT_SETTINGS(spotify_default_device_id, 
                                        spotify_default_device_name, 
                                        spotify_default_playlist_uri, 
                                        spotify_default_playlist_name, 
                                        spotify_default_volume):

            success_message_change_default_settings = True  


    """ #################### """
    """  table client_music  """
    """ #################### """   

    if GET_DEVICE_CONNECTION_MQTT() == True:

        if request.form.get("save_client_music_settings") != None:
            
            for i in range (1,26):

                if request.form.get("radio_client_music_interface_" + str(i)) != None:
        
                    client_music_interface = request.form.get("radio_client_music_interface_" + str(i))
                    client_music_volume    = request.form.get("set_client_music_volume_" + str(i))                
                    device                 = GET_DEVICE_BY_ID(i)

                    # devices without volume control support
                    if client_music_volume == None:
                        client_music_volume = 0 

                    # last values founded
                    try:
                        data = json.loads(device.last_values_json)
                        
                        if client_music_interface != data["interface"] or str(client_music_volume) != str(data["volume"]):

                            heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"' + client_music_interface + '","volume":' + str(client_music_volume) + '}')))     

                            result = CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, '{"interface":"' + client_music_interface + '","volume":' + str(client_music_volume) + '}', 20)
                            
                            if result != True:
                                error_message_change_settings_client_music.append(result)
                            else:
                                success_message_change_settings_client_music.append(device.name + " || Einstellungen gespeichert")
                                
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

                        result = CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, '{"interface":"' + client_music_interface + '","volume":' + str(client_music_volume) + '}', 20)
                        
                        if result != True:
                            error_message_change_settings_client_music.append(result)
                        else:
                            success_message_change_settings_client_music.append(device.name + " || Einstellungen gespeichert")
                            
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
        error_message_change_settings_client_music.append("Keine MQTT-Verbindung")

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
                                                    volume=volume, 
                                                    shuffle=shuffle,
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