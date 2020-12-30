
"""

https://github.com/drshrey/spotify-flask-auth-example

https://github.com/plamere/spotipy/issues/194
https://spotipy.readthedocs.io/en/latest/

https://developer.spotify.com/dashboard/
https://developer.spotify.com/documentation/general/guides/scopes/
https://developer.spotify.com/documentation/web-api/reference/search/search/
https://developer.spotify.com/documentation/web-api/reference/player/start-a-users-playback/


"""

from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import *
from app.backend.email            import SEND_EMAIL
from app.backend.shared_resources import mqtt_message_queue
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS

import requests
import json
import spotipy
import socket 
import time
import base64
import threading
import heapq

from urllib.parse import quote

from lms import find_server


""" ########################## """
"""  spotify authentification  """
""" ########################## """

#  Client Keys
CLIENT_ID             = GET_SPOTIFY_SETTINGS().client_id
CLIENT_SECRET         = GET_SPOTIFY_SETTINGS().client_secret

# Spotify URLS
SPOTIFY_AUTH_URL      = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL     = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL  = "https://api.spotify.com"
API_VERSION           = "v1"
SPOTIFY_API_URL       = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

SCOPE                 = "playlist-read-private user-read-recently-played user-read-currently-playing user-read-playback-state streaming"
STATE                 = ""
SHOW_DIALOG_bool      = True
SHOW_DIALOG_str       = str(SHOW_DIALOG_bool).lower()

#  Client Tokens
SPOTIFY_TOKEN         = ""
SPOTIFY_REFRESH_TOKEN = GET_SPOTIFY_REFRESH_TOKEN()


def GET_SPOTIFY_AUTHORIZATION():

    if GET_SYSTEM_SETTINGS().ip_address == "":
        REDIRECT_URI = "http://127.0.0.1:80/music/spotify/token"
    else:
        REDIRECT_URI = "http://" + str(GET_SYSTEM_SETTINGS().ip_address) + ":80/music/spotify/token"

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "client_id": CLIENT_ID      
    }    
    
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    
    return auth_url


def GENERATE_SPOTIFY_TOKEN(auth_token):
    global SPOTIFY_TOKEN    
    global SPOTIFY_REFRESH_TOKEN       

    if GET_SYSTEM_SETTINGS().ip_address == "":
        REDIRECT_URI = "http://127.0.0.1:80/music/spotify/token"
    else:
        REDIRECT_URI = "http://" + str(GET_SYSTEM_SETTINGS().ip_address) + ":80/music/spotify/token"   
 
    body = {
        "grant_type": 'authorization_code',
        "code" : str(auth_token),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=body)
    answer       = json.loads(post_request.text)

    try:
        SPOTIFY_TOKEN = answer["access_token"]
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Login | successful")
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Token | received")
        
    except:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Login | failed")
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Token | not received | " + str(answer))
        SEND_EMAIL("ERROR", "Music | Spotify | Token | not received | " + str(answer))

    try:
        SET_SPOTIFY_REFRESH_TOKEN(answer["refresh_token"])
        SPOTIFY_REFRESH_TOKEN = answer["refresh_token"]        
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Refresh Token | received") 
        
    except:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Refresh Token | not received | " + str(answer))
        SEND_EMAIL("ERROR", "Music | Spotify | Refresh Token | not received | " + str(answer))           


def GET_SPOTIFY_TOKEN():
    global SPOTIFY_TOKEN

    return SPOTIFY_TOKEN


def DELETE_SPOTIFY_TOKEN():
    global SPOTIFY_TOKEN
    global SPOTIFY_REFRESH_TOKEN   

    SPOTIFY_TOKEN         = ""
    SPOTIFY_REFRESH_TOKEN = ""
    SET_SPOTIFY_REFRESH_TOKEN("")


def CHECK_CLIENT_MUSIC_CONNECTION():

    try:
        sp                   = spotipy.Spotify(auth=SPOTIFY_TOKEN)
        sp.trace             = False     
        list_spotify_devices = sp.devices()["devices"]  

        for client_music in GET_ALL_DEVICES("client_music"):
            device_found = False

            # check device connected to spotify
            if "spotify" in client_music.last_values_string:
                for element in list_spotify_devices:
                    if client_music.name.lower() == element["name"].lower():
                        device_found = True

            # find multiroom group and check device connected lms
            if "multiroom" in client_music.last_values_string:
                for element in list_spotify_devices:
                    if "multiroom" in element["name"].lower() and client_music.name.lower() in element["name"].lower():
                        device_found = True                        

            # if no connection found, restart services
            if device_found == False:

                try:
                    heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + client_music.ieeeAddr + "/set", '{"interface":"restart"}')))  

                except Exception as e:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + client_music.name + " | " + str(e))      

    except:
        pass


""" ###################### """
"""  token refresh thread  """
""" ###################### """

def START_REFRESH_SPOTIFY_TOKEN_THREAD():
    
    try:
        Thread = threading.Thread(target=REFRESH_SPOTIFY_TOKEN_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Host | Thread | Refresh Spotify Token | " + str(e)) 
        SEND_EMAIL("ERROR", "Host | Thread | Refresh Spotify Token | " + str(e)) 


def REFRESH_SPOTIFY_TOKEN_THREAD():   
    global SPOTIFY_TOKEN        
    global SPOTIFY_REFRESH_TOKEN 

    counter = 3001

    while True:
               
        try:

            # check spotify login 
            if SPOTIFY_REFRESH_TOKEN != "":

                if counter > 3000:

                    # get a new token
                
                    body = {
                        "grant_type" : "refresh_token",
                        "refresh_token" : GET_SPOTIFY_REFRESH_TOKEN()
                    }

                    auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
                    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': 'Basic {}'.format(b64_auth_str)
                    }

                    post_refresh = requests.post(SPOTIFY_TOKEN_URL, data=body, headers=headers) 
                    answer       = json.loads(post_refresh.text)

                    try:
                        SPOTIFY_TOKEN = answer["access_token"]
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Token | updated") 
                        
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Token | update | " + str(e)) 
                        SEND_EMAIL("ERROR", "Music | Spotify | Token | update | " + str(e)) 

                    try:
                        SET_SPOTIFY_REFRESH_TOKEN(answer["refresh_token"])
                        SPOTIFY_REFRESH_TOKEN = answer["refresh_token"]        
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Music | Spotify | Refresh Token | updated")  
                        
                    except:
                        pass
                        
                    # restart counter
                    counter = 0


                # check device connections every 30 seconds
                elif (counter % 30 == 0):
                    CHECK_CLIENT_MUSIC_CONNECTION()
                    counter = counter + 1

                else:
                    counter = counter + 1

        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Host | Thread | Refresh Spotify Token | " + str(e)) 
                
        time.sleep(1)


""" ############## """
"""  music volume  """
""" ############## """

def SET_MUSIC_VOLUME(spotify_token, volume):

    if int(volume) == 0:
        volume = 33

    sp                  = spotipy.Spotify(auth=spotify_token)
    sp.trace            = False     
    spotify_device_id   = sp.current_playback(market=None)['device']['id']
    spotify_device_name = sp.current_playback(market=None)['device']['name']

    sp.volume(int(volume), device_id=spotify_device_id)  

    if "multiroom" in spotify_device_name:
        server = find_server()

        for player in server.players:
            player.set_volume(volume)     

    time.sleep(0.15)


""" ################################### """
"""  update multiroom default settings  """
""" ################################### """

def UPDATE_MULTIROOM_DEFAULT_SETTINGS():

    try:

        # update multiroom settings
        if "multiroom" in GET_SPOTIFY_SETTINGS().default_device_name:

            sp                   = spotipy.Spotify(auth=SPOTIFY_TOKEN)
            sp.trace             = False     
            list_spotify_devices = sp.devices()["devices"]  

            for device in list_spotify_devices:    

                if "multiroom" in device['name']:
                    spotify_default_device_name = device['name']
                    spotify_default_device_id   = device['id']

                    SET_SPOTIFY_DEFAULT_SETTINGS(spotify_default_device_id, 
                                                    spotify_default_device_name, 
                                                    GET_SPOTIFY_SETTINGS().default_playlist_uri, 
                                                    GET_SPOTIFY_SETTINGS().default_playlist_name, 
                                                    GET_SPOTIFY_SETTINGS().default_volume,
                                                    GET_SPOTIFY_SETTINGS().default_shuffle)        


        # update single device settings
        else:

                sp                   = spotipy.Spotify(auth=SPOTIFY_TOKEN)
                sp.trace             = False     
                list_spotify_devices = sp.devices()["devices"]  

                default_device_name  = GET_SPOTIFY_SETTINGS().default_device_name

                for device in list_spotify_devices:    
                    
                    if default_device_name.lower() == device['name'].lower():
                        spotify_default_device_id = device['id']

                        SET_SPOTIFY_DEFAULT_SETTINGS(spotify_default_device_id, 
                                                    GET_SPOTIFY_SETTINGS().default_device_name, 
                                                    GET_SPOTIFY_SETTINGS().default_playlist_uri, 
                                                    GET_SPOTIFY_SETTINGS().default_playlist_name, 
                                                    GET_SPOTIFY_SETTINGS().default_volume,
                                                    GET_SPOTIFY_SETTINGS().default_shuffle)    

    except:
        pass


""" ################################# """
"""  check multiroom synchronization  """
""" ################################# """

def START_CHECK_MULTIROOM_SYNCHRONIZATION_THREAD():
	try:
		Thread = threading.Thread(target=CHECK_MULTIROOM_SYNCHRONIZATION_THREAD)
		Thread.start()  

	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Check Multiroom Synchronization | " + str(e)) 


def CHECK_MULTIROOM_SYNCHRONIZATION_THREAD(): 
    counter = 0

    try:

        while counter < 15:

            sp                       = spotipy.Spotify(auth=SPOTIFY_TOKEN)
            sp.trace                 = False     
            spotify_current_playback = sp.current_playback(market=None)
                    
            spotify_current_playback_state = spotify_current_playback['is_playing']
            spotify_current_device_id      = spotify_current_playback['device']['id']

            # restart playback
            if spotify_current_playback_state == False:
                sp.start_playback(device_id=spotify_current_device_id)
            else:
                break

            counter = counter + 1
            time.sleep(1)

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Host | Thread | Check Multiroom Synchronization | " + str(e))         

        
""" ################################## """
"""  multiroom synchronization thread  """
""" ################################## """

def START_MULTIROOM_SYNCHRONIZATION_THREAD():
    
    try:
        Thread = threading.Thread(target=MULTIROOM_SYNCHRONIZATION_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Host | Thread | Multiroom Synchronization | " + str(e)) 


def MULTIROOM_SYNCHRONIZATION_THREAD():   
    last_lms_position  = 0
    lms_position_error = 0

    while True:
               
        if SPOTIFY_TOKEN != "":

            try:

                sp                       = spotipy.Spotify(auth=SPOTIFY_TOKEN)
                sp.trace                 = False     
                spotify_current_playback = sp.current_playback(market=None)

                spotify_current_device_id            = spotify_current_playback['device']['id']
                spotify_current_playback_device_name = spotify_current_playback['device']['name']                
                spotify_current_playback_state       = spotify_current_playback['is_playing']
                spotify_current_playback_progress    = spotify_current_playback['progress_ms'] 
        
                if spotify_current_playback_state == True and "multiroom" in spotify_current_playback_device_name.lower():

                    # get lms position
                    server = find_server()

                    for player in server.players:
                        lms_position = player.position
                        break    

                    # lms stopped playing ?
                    if lms_position != 0 and last_lms_position != 0 and lms_position <= last_lms_position:
                        lms_position_error = lms_position_error + 1
                    else:
                        lms_position_error = 0

                    if lms_position_error > 2:
                        sp.next_track(device_id=spotify_current_device_id)  

                        # restart playback, if necessary
                        START_CHECK_MULTIROOM_SYNCHRONIZATION_THREAD()
                             
                    last_lms_position = lms_position


                    # get spotify position
                    spotify_position = int(spotify_current_playback_progress / 1000)

                    # calculate position distance
                    if lms_position > 15 and spotify_position > 15:              
                        position_distance = abs((lms_position) - (spotify_position))

                        # start next track, if synchronization was lost
                        if position_distance > 30:  
                            
                            while True:

                                # lms stopped playing ?
                                if lms_position <= last_lms_position:
                                    lms_position_error = lms_position_error + 1

                                if lms_position_error > 2:
                                    lms_position_error = 0

                                    sp.next_track(device_id=spotify_current_device_id)  

                                    # restart playback, if necessary
                                    START_CHECK_MULTIROOM_SYNCHRONIZATION_THREAD()
                                    break
                                        
                                # lms start next track        
                                if lms_position < 2:
                                    lms_position_error = 0

                                    sp.next_track(device_id=spotify_current_device_id)  

                                    # restart playback, if necessary
                                    START_CHECK_MULTIROOM_SYNCHRONIZATION_THREAD()
                                    break

                                last_lms_position = lms_position
                                time.sleep(0.5)
            
            except:
                pass
                    
        time.sleep(1)


""" ################# """
"""  spotify control  """
""" ################# """

def SPOTIFY_CONTROL(spotify_token, command, spotify_volume):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False     

    try:

        if command == "play":    
            
            try:

                # start current playback
                spotify_current_playback = sp.current_playback(market=None)
                spotify_device_id        = sp.current_playback(market=None)['device']['id']

                sp.next_track(device_id=spotify_device_id) 
                SET_MUSIC_VOLUME(spotify_token, spotify_volume) 

            except:

                # start default settings
                UPDATE_MULTIROOM_DEFAULT_SETTINGS()

                # get spotity device id
                spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, GET_SPOTIFY_SETTINGS().default_device_name) 

                sp.start_playback(device_id=spotify_device_id, 
                                  context_uri=GET_SPOTIFY_SETTINGS().default_playlist_uri, 
                                  uris=None, 
                                  offset = None)    

                SET_MUSIC_VOLUME(spotify_token, GET_SPOTIFY_SETTINGS().default_volume)
                
                # set shuffle setting
                if GET_SPOTIFY_SETTINGS().default_shuffle == "True":
                    spotify_device_id = sp.current_playback(market=None)['device']['id'] 
                    sp.shuffle(True, device_id=spotify_device_id) 
                    sp.next_track(device_id=spotify_device_id)                    
                
                else:
                    sp.shuffle(False, device_id=spotify_device_id)         


        if command == "play/stop":    

            try:
                spotify_current_playback = sp.current_playback(market=None)

                # start current playback 
                if spotify_current_playback['is_playing'] == False:
                    spotify_device_id = sp.current_playback(market=None)['device']['id']
                    sp.next_track(device_id=spotify_device_id) 
                    SET_MUSIC_VOLUME(spotify_token, spotify_volume)

                # stop playing
                if spotify_current_playback['is_playing'] == True:
                    spotify_device_id = sp.current_playback(market=None)['device']['id']
                    sp.pause_playback(device_id=spotify_device_id)      

            except:                                
                # start default settings
                UPDATE_MULTIROOM_DEFAULT_SETTINGS()

                # get spotity device id
                spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, GET_SPOTIFY_SETTINGS().default_device_name) 

                sp.start_playback(device_id=spotify_device_id, 
                                  context_uri=GET_SPOTIFY_SETTINGS().default_playlist_uri, 
                                  uris=None, 
                                  offset = None)    

                SET_MUSIC_VOLUME(spotify_token, GET_SPOTIFY_SETTINGS().default_volume)

                # set shuffle setting
                if GET_SPOTIFY_SETTINGS().default_shuffle == "True":
                    spotify_device_id = sp.current_playback(market=None)['device']['id'] 
                    sp.shuffle(True, device_id=spotify_device_id) 
                    sp.next_track(device_id=spotify_device_id)    

                else:
                    spotify_device_id = sp.current_playback(market=None)['device']['id'] 
                    sp.shuffle(False, device_id=spotify_device_id)                      


        if command == "rotate_playlist":   
            
            # get playlist name
            spotify_current_playlist_uri = sp.current_playback(market=None)["context"]["uri"]

            # create list of playlist uris
            list_playlist_uris = []

            for playlist in sp.current_user_playlists(limit=20)["items"]:
                list_playlist_uris.append(playlist["uri"])

            # find position of current playlist
            playlist_position = 0

            for position, playlist_uri in enumerate(list_playlist_uris):
                if playlist_uri == spotify_current_playlist_uri:
                    playlist_position = position

            # get next playlist
            try:
                # current playlist is not the last playlist
                next_playlist = list_playlist_uris[playlist_position + 1]
            except:
                # current scene is the last scene
                next_playlist = list_playlist_uris[0]

            # start next playlist
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.start_playback(device_id=spotify_device_id, context_uri=next_playlist, uris=None, offset = None)         
            SET_MUSIC_VOLUME(spotify_token, spotify_volume) 

            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.shuffle(True, device_id=spotify_device_id)     
            sp.next_track(device_id=spotify_device_id) 

        if command == "previous":      
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.previous_track(device_id=spotify_device_id)     
            SET_MUSIC_VOLUME(spotify_token, spotify_volume)

        if command == "next":     
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.next_track(device_id=spotify_device_id) 
            SET_MUSIC_VOLUME(spotify_token, spotify_volume)
            
        if command == "stop":    
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.pause_playback(device_id=spotify_device_id)  

        if command == "shuffle_true":     
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.shuffle(True, device_id=spotify_device_id) 
            SET_MUSIC_VOLUME(spotify_token, spotify_volume) 

        if command == "shuffle_false":              
            spotify_device_id = sp.current_playback(market=None)['device']['id']
            sp.shuffle(False, device_id=spotify_device_id) 
            SET_MUSIC_VOLUME(spotify_token, spotify_volume) 

        if command == "volume":   
            spotify_device_id = sp.current_playback(market=None)['device']['id']  
            SET_MUSIC_VOLUME(spotify_token, spotify_volume)    

        if command == "volume_up":   
            
            try:

                spotify_device_name = sp.current_playback(market=None)['device']['name']

                # case multiroom
                if "multiroom" in spotify_device_name:
                    if spotify_volume < 97:
                        volume = spotify_volume + 3
                    else:
                        volume = 100      

                    SET_MUSIC_VOLUME(spotify_token, volume)

                # case hifiberry_AMP2
                if GET_DEVICE_BY_NAME(spotify_device_name).model == "hifiberry_AMP2":
                    if spotify_volume < 98:
                        volume = spotify_volume + 2
                    else:
                        volume = 100
                    
                    SET_MUSIC_VOLUME(spotify_token, volume)
                    
                # case hifiberry_miniAMP
                if GET_DEVICE_BY_NAME(spotify_device_name).model == "hifiberry_miniAMP":

                    if spotify_volume < 98:
                        volume = spotify_volume + 2
                    else:
                        volume = 100
                    
                    SET_MUSIC_VOLUME(spotify_token, volume)      

            except:

                # case spotity connect device
                if spotify_volume < 97:
                    volume = spotify_volume + 3
                else:
                    volume = 100
                
                SET_MUSIC_VOLUME(spotify_token, volume)     


        if command == "volume_down":   

            try:

                spotify_device_name = sp.current_playback(market=None)['device']['name']

                # case multiroom
                if "multiroom" in spotify_device_name:                 
                    if spotify_volume > 3:
                        volume = spotify_volume - 3       
                    else:
                        volume = 1              

                    SET_MUSIC_VOLUME(spotify_token, volume)   

                # case hifiberry_AMP2                
                if GET_DEVICE_BY_NAME(spotify_device_name).model == "hifiberry_AMP2":
            
                    if spotify_volume > 2:
                        volume = spotify_volume - 2       
                    else:
                        volume = 1

                    SET_MUSIC_VOLUME(spotify_token, volume) 

                # case hifiberry_miniAMP
                if GET_DEVICE_BY_NAME(spotify_device_name).model == "hifiberry_miniAMP":

                    if spotify_volume > 2:
                        volume = spotify_volume - 2       
                    else:
                        volume = 1

                    SET_MUSIC_VOLUME(spotify_token, volume) 

            except Exception as e:

                # case spotity connect device
                if spotify_volume > 3:
                    volume = spotify_volume - 3       
                else:
                    volume = 1

                SET_MUSIC_VOLUME(spotify_token, volume)    


    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Control | " + str(e)) 


def SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False    
    
    sp.start_playback(device_id=spotify_device_id, context_uri=playlist_uri, uris=None, offset = None)      
    sp.shuffle(True, device_id=spotify_device_id)
    sp.next_track(device_id=spotify_device_id) 
    SET_MUSIC_VOLUME(spotify_token, playlist_volume)
    

def SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False    

    sp.start_playback(device_id=spotify_device_id, context_uri=None, uris=[track_uri], offset={"position": 0})    
    SET_MUSIC_VOLUME(spotify_token, track_volume)


def SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False    

    sp.start_playback(device_id=spotify_device_id, context_uri=album_uri, uris=None, offset={"position": 0})      
    SET_MUSIC_VOLUME(spotify_token, album_volume)


""" ###################### """
"""  get current playback  """
""" ###################### """

def GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False        

    spotify_current_playback = sp.current_playback(market=None)

    try:
        # get device name
        spotify_current_playback_device_name = spotify_current_playback['device']['name']

    except:
        spotify_current_playback_device_name = ""
 
    try:
        # get device type
        spotify_current_playback_device_type = spotify_current_playback['device']['type']
        
    except:
        spotify_current_playback_device_type = ""     

    try:
        # get playback state
        spotify_current_playback_state = str(spotify_current_playback['is_playing']).upper()
        
    except:
        spotify_current_playback_state = ""
 
    try:
        # get playback volume
        spotify_current_playback_volume = spotify_current_playback['device']['volume_percent']
        
    except:
        spotify_current_playback_volume = ""      
 
    try:
        # get playback track
        spotify_current_playback_track = spotify_current_playback['item']['name']   
        
    except:
        spotify_current_playback_track = ""           
 
    try:
        # get playback track artists
        spotify_current_playback_artists = ""
        
        for i in range(len(spotify_current_playback["item"]["artists"])):
            spotify_current_playback_artists = spotify_current_playback_artists + ", " + spotify_current_playback["item"]["artists"][i]["name"]  

        spotify_current_playback_artists = spotify_current_playback_artists[1:]        
            
    except:
        spotify_current_playback_artists = []     

    try:
        # get progress in minutes:seconds
        spotify_current_playback_progress = spotify_current_playback['progress_ms'] / 1000
        
        def convertSeconds(seconds):
            h = seconds//(60*60)
            m = int((seconds-h*60*60)//60)
            s = int(seconds-(h*60*60)-(m*60))
            
            if len(str(s)) == 1:
                s = str(0) + str(s) 
            
            return [m, s]
            
        spotify_current_playback_progress = (str(convertSeconds(spotify_current_playback_progress)[0]) + ":" + 
                                             str(convertSeconds(spotify_current_playback_progress)[1]))
    
    except:
        spotify_current_playback_progress = ""
     
    try:
        # get playlist name
        spotify_current_playback_playlist_name = sp.user_playlist(sp.current_user()["display_name"], spotify_current_playback["context"]["uri"], fields=None)
        spotify_current_playback_playlist_name = spotify_current_playback_playlist_name['name']
        
    except:
        spotify_current_playback_playlist_name = ""
                 
    try:
        # get playback shuffle state
        spotify_current_playback_shuffle_state = spotify_current_playback['shuffle_state']
        
    except:
        spotify_current_playback_shuffle_state = ""  
        
    
    tupel_current_playback = (spotify_current_playback_device_name,
                              spotify_current_playback_device_type,
                              spotify_current_playback_state,
                              spotify_current_playback_volume,
                              spotify_current_playback_track,
                              spotify_current_playback_artists,
                              spotify_current_playback_progress,
                              spotify_current_playback_playlist_name,
                              spotify_current_playback_shuffle_state)
                
                            
    return tupel_current_playback


""" ################### """
"""  spotify device id  """
""" ################### """

def GET_SPOTIFY_DEVICE_ID(spotify_token, device_name):       

    sp                = spotipy.Spotify(auth=spotify_token)
    sp.trace          = False                                 
    spotify_device_id = 0
    counter           = 0

    try:

        # check current device interface
        if device_name.lower() != "multiroom":
            device = GET_DEVICE_BY_NAME(device_name)
            data   = json.loads(device.last_values_json)

            if str(data["interface"]).lower() == "multiroom":
                heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"spotify","volume":' + str(data["volume"]) + '}')))     

                CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "spotify" + '; ' + str(data["volume"]), 45)     
                
        # get device spotify id
        while spotify_device_id == 0 and counter < 30:

            for device in sp.devices()["devices"]:

                # spotify client
                if device['name'].lower() == device_name.lower():
                    spotify_device_id = device['id']  
                    continue      

                # select multiroom group
                if device_name.lower() == "multiroom":
                    if "multiroom" in device['name'].lower():
                        spotify_device_id = device['id'] 
                        continue    

            counter = counter + 1
            time.sleep(1)     

        return spotify_device_id

    except:
        pass  


""" ################## """
"""  spotify playlist  """
""" ################## """

def GET_SPOTIFY_PLAYLIST(spotify_token, playlist_name, number_results):

    sp           = spotipy.Spotify(auth=spotify_token)
    sp.trace     = False         
    playlist_uri = ""

    try:

        list_spotify_playlists = sp.current_user_playlists(limit=number_results)["items"]
        
        for playlist in list_spotify_playlists:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_uri = playlist['uri']
                continue

        return playlist_uri

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Get Playlist URI | " + str(e)) 
        return ("ERROR: " + str(e))      


""" ############## """
"""  search track  """
""" ############## """

def SPOTIFY_SEARCH_TRACK(spotify_token, track_name, track_artist, number_results):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False        
    
    list_search_track_results = []

    try:
        
        if track_name != "":
                  
            if track_artist != '':

                results = sp.search(q='artist:' + track_artist + ' track:' + track_name, limit = number_results, type='track')

                if results['tracks']['items'] != []:

                    for i in range(len(results['tracks']['items'])):
                        list_search_track_results.append((results['tracks']['items'][i]['name'],
                                                          results['tracks']['items'][i]['artists'][0]['name'],
                                                          results['tracks']['items'][i]['uri']))
                                                          
                    return list_search_track_results
                    
            else:

                results = sp.search(q=' track:' + track_name, limit = number_results, type='track')

                if results['tracks']['items'] != []:

                    for i in range(len(results['tracks']['items'])):
                        list_search_track_results.append((results['tracks']['items'][i]['name'],
                                                          results['tracks']['items'][i]['artists'][0]['name'],
                                                          results['tracks']['items'][i]['uri']))
                                                          
                    return list_search_track_results             
                    
        else:
            return ("No track name given")
                              
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Search Track | " + str(e)) 
        return ("ERROR: " + str(e))  


""" ############## """
"""  search album  """
""" ############## """

def SPOTIFY_SEARCH_ALBUM(spotify_token, album_name, album_artist, number_results):

    sp       = spotipy.Spotify(auth=spotify_token)
    sp.trace = False        
    
    list_search_album_results = []

    try:

        if album_name != "":

            if album_artist != '':

                results = sp.search(q='artist:' + album_artist + ' album:' + album_name, limit = number_results, type='album')

                if results['albums']['items'] != []:

                    for i in range(len(results['albums']['items'])):
                        list_search_album_results.append((results['albums']['items'][i]['name'],
                                                          results['albums']['items'][i]['artists'][0]['name'],
                                                          results['albums']['items'][i]['uri']))
                    
                    return list_search_album_results                                      
                
            else:

                results = sp.search(q=' album:' + album_name, limit = number_results, type='album')

                if results['albums']['items'] != []:

                    for i in range(len(results['albums']['items'])):
                        list_search_album_results.append((results['albums']['items'][i]['name'],
                                                          results['albums']['items'][i]['artists'][0]['name'],
                                                          results['albums']['items'][i]['uri']))
                                                          
                    return list_search_album_results
                                      
        else:
            return ("No album name given")
                      
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Music | Spotify | Search Album | " + str(e)) 
        return ("ERROR: " + str(e))  