import threading
import heapq
import time
import spotipy

from app                          import app
from app.database.models          import *
from app.backend.file_management  import *
from app.backend.shared_resources import mqtt_message_queue, SET_PROGRAM_STATUS, GET_PROGRAM_STATUS
from app.backend.mqtt             import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD
from app.backend.led              import SET_LED_GROUP_SCENE, SET_LED_GROUP_TURN_OFF, CHECK_LED_GROUP_SETTING_THREAD
from app.backend.spotify          import *

stop_program    = False
repeat_program  = False


def START_PROGRAM_THREAD(program_id):

    if GET_PROGRAM_STATUS() == "None":

        try:
            Thread = threading.Thread(target=PROGRAM_THREAD, args=(program_id, ))
            Thread.start()    
            
            program_name = GET_PROGRAM_BY_ID(program_id).name
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True
        
        except Exception as e:
            return e

    else:
        return("Other Program running")

    
def STOP_PROGRAM_THREAD():
    try:
        global stop_program, repeat_program
        stop_program   = True
        repeat_program = False
        return True

    except Exception as e:
        return e   
    
   
def SET_REPEAT_PROGRAM(setting):
    global repeat_program
    repeat_program = setting

    
def GET_REPEAT_PROGRAM():
    global repeat_program
    return repeat_program       


def PROGRAM_THREAD(program_id):
    global stop_program, repeat_program

    try:

        lines = [[GET_PROGRAM_BY_ID(program_id).line_active_1,  GET_PROGRAM_BY_ID(program_id).line_content_1],
                 [GET_PROGRAM_BY_ID(program_id).line_active_2,  GET_PROGRAM_BY_ID(program_id).line_content_2],
                 [GET_PROGRAM_BY_ID(program_id).line_active_3,  GET_PROGRAM_BY_ID(program_id).line_content_3],
                 [GET_PROGRAM_BY_ID(program_id).line_active_4,  GET_PROGRAM_BY_ID(program_id).line_content_4],
                 [GET_PROGRAM_BY_ID(program_id).line_active_5,  GET_PROGRAM_BY_ID(program_id).line_content_5],
                 [GET_PROGRAM_BY_ID(program_id).line_active_6,  GET_PROGRAM_BY_ID(program_id).line_content_6],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_7,  GET_PROGRAM_BY_ID(program_id).line_content_7],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_8,  GET_PROGRAM_BY_ID(program_id).line_content_8],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_9,  GET_PROGRAM_BY_ID(program_id).line_content_9],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_10, GET_PROGRAM_BY_ID(program_id).line_content_10],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_11, GET_PROGRAM_BY_ID(program_id).line_content_11],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_12, GET_PROGRAM_BY_ID(program_id).line_content_12],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_13, GET_PROGRAM_BY_ID(program_id).line_content_13],
                 [GET_PROGRAM_BY_ID(program_id).line_active_14, GET_PROGRAM_BY_ID(program_id).line_content_14],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_15, GET_PROGRAM_BY_ID(program_id).line_content_15],
                 [GET_PROGRAM_BY_ID(program_id).line_active_16, GET_PROGRAM_BY_ID(program_id).line_content_16],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_17, GET_PROGRAM_BY_ID(program_id).line_content_17],
                 [GET_PROGRAM_BY_ID(program_id).line_active_18, GET_PROGRAM_BY_ID(program_id).line_content_18],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_19, GET_PROGRAM_BY_ID(program_id).line_content_19],            
                 [GET_PROGRAM_BY_ID(program_id).line_active_20, GET_PROGRAM_BY_ID(program_id).line_content_20]]                  
            
        program_name = GET_PROGRAM_BY_ID(program_id).name
        repeat       = True

        while repeat == True:

            # get total lines
            lines_total = 0

            for line in lines:
                if line[0] == "True":
                    lines_total = lines_total + 1


            line_number = 1

            for line in lines:
                
                # stop program
                if stop_program == True:
                    stop_program = False  # reset variable
                    
                    SET_PROGRAM_STATUS("None")

                    WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                    break

                # program running
                else:
                    
                    # update program info
                    SET_PROGRAM_STATUS(program_name + " ( " + str(line_number) + " | " + str(lines_total) + " || " + str(line[1]) + " )")
                       
                    # line active ?
                    if line[0] == "True":


                        # #####
                        # break
                        # #####
                                
                        if "break" in line[1]:
                                
                            line_content = line[1].split(" # ")
                            time.sleep(int(line_content[1]))          


                        # ######    
                        # device
                        # ######

                        if "device" in line[1]:
                                
                            line_content = line[1].split(" # ")

                            try:
                                      
                                device_name = line_content[1]    
                                device      = ""
                                device      = GET_DEVICE_BY_NAME(device_name)
                                
                                program_setting_formated = line_content[2]
                                 
                                # check device exception
                                check_result = CHECK_DEVICE_EXCEPTIONS(device.id, program_setting_formated)
                                
                               
                                if check_result == True:      

                                    # convert string to json-format
                                    program_setting = program_setting_formated.replace(" ", "")
                                    program_setting = program_setting.replace(':', '":"')
                                    program_setting = program_setting.replace(',', '","')
                                    program_setting = '{"' + str(program_setting) + '"}'                        
                                                                 
                                    # new device setting ?  
                                    new_setting = False

                                    if not "," in program_setting:
                                        if not program_setting[1:-1] in device.last_values_json:
                                            new_setting = True

                                    # more then one setting value:
                                    else:   
                                        program_setting_temp = program_setting[1:-1]
                                        list_program_setting = program_setting_temp.split(",")

                                        for setting in list_program_setting:

                                            if not setting in device.last_values_json:
                                                new_setting = True  

                                    if new_setting == True: 

                                        if device.gateway == "mqtt":
                                            channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                                        if device.gateway == "zigbee2mqtt":   
                                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                                        msg = program_setting

                                        heapq.heappush(mqtt_message_queue, (10, (channel, msg)))    
                                        CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, program_setting, 20)     
                                                         
                                    else:
                                        WRITE_LOGFILE_SYSTEM("STATUS", "Devices | Device - " + device.name + " | " + program_setting)                                

                                else:
                                    WRITE_LOGFILE_SYSTEM("WARNING", "Program - " + program_name + " | " + check_result)
                                
                            except Exception as e:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))


                        # ###
                        # led 
                        # ###
                                 
                        if "scene" in line[1]:
                                
                            line_content = line[1].split(" # ")
                            
                            try:
                                group_name = line_content[1]    
                                
                                if line_content[2] != "off" and line_content[2] != "OFF":

                                    scene_name        = line_content[2]
                                    global_brightness = line_content[3]

                                    group = GET_LED_GROUP_BY_NAME(group_name)
                                    scene = GET_LED_SCENE_BY_NAME(scene_name)

                                    SET_LED_GROUP_SCENE(group.id, scene.id, int(global_brightness))
                                    CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, global_brightness, 2, 10)

                                if line_content[2] == "off" or line_content[2] == "OFF":

                                    group = GET_LED_GROUP_BY_NAME(group_name)
                                    scene = GET_LED_SCENE_BY_NAME(scene_name)
                                                   
                                    SET_LED_GROUP_TURN_OFF(group.id)
                                    CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 2, 10)                  

                            except Exception as e:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))


                        # #######
                        # spotify
                        # #######

                        if "spotify" in line[1]:
                                
                            line_content = line[1].split(" # ")

                            if GET_SPOTIFY_TOKEN() == "" and GET_SPOTIFY_REFRESH_TOKEN() != "":
                                REFRESH_SPOTIFY_TOKEN()

                            spotify_token = GET_SPOTIFY_TOKEN()

                            # check spotify login 
                            if spotify_token != "":
                                
                                try:
                                    
                                    sp       = spotipy.Spotify(auth=spotify_token)
                                    sp.trace = False


                                    # basic control
                                    
                                    try:
                                    
                                        spotify_device_id = sp.current_playback(market=None)['device']['id']
                                        spotify_volume    = sp.current_playback(market=None)['device']['volume_percent']

                                        if line_content[1].lower() == "play":
                                            SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       
                                
                                        if line_content[1].lower() == "previous":
                                            SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                                        if line_content[1].lower() == "next":
                                            SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                                        if line_content[1].lower() == "stop": 
                                            SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                                        if line_content[1].lower() == "volume":          
                                            spotify_volume = int(line_content[2])
                                            SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  

                                    except:
                                        pass
                                                                         
                                  
                                    # start playlist
                                            
                                    if line_content[1].lower() == "playlist": 

                                        # get spotify_device_id
                                        device_name          = line_content[2]                                    
                                        list_spotify_devices = sp.devices()["devices"]  
                                        
                                        for device in list_spotify_devices:
                                            if device['name'].lower() == device_name.lower():
                                                spotify_device_id = device['id']  
                                                continue                                
                                        
                                        # get playlist_uri
                                        playlist_name          = line_content[3]
                                        list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]
                                        
                                        for playlist in list_spotify_playlists:
                                            if playlist['name'].lower() == playlist_name.lower():
                                                playlist_uri = playlist['uri']
                                                continue
                                              
                                        # get volume
                                        playlist_volume = int(line_content[4])
                                        
                                        SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
                                
                         
                                    # start track
                                            
                                    if line_content[1].lower() == "track": 

                                        # get spotify_device_id
                                        device_name          = line_content[2]                                    
                                        list_spotify_devices = sp.devices()["devices"]  
                                        
                                        for device in list_spotify_devices:
                                            if device['name'].lower() == device_name.lower():
                                                spotify_device_id = device['id']  
                                                continue                                
                                        
                                        # get playlist_uri
                                        track_uri = SPOTIFY_SEARCH_TRACK(spotify_token, line_content[3], line_content[4], 1) [0][2]
                                              
                                        # get volume
                                        track_volume = int(line_content[5])
                                        
                                        SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)


                                    # start album
                                            
                                    if line_content[1].lower() == "album": 

                                        # get spotify_device_id
                                        device_name          = line_content[2]                                    
                                        list_spotify_devices = sp.devices()["devices"]  
                                        
                                        for device in list_spotify_devices:
                                            if device['name'].lower() == device_name.lower():
                                                spotify_device_id = device['id']  
                                                continue                                
                                        
                                        # get album_uri
                                        album_uri = SPOTIFY_SEARCH_ALBUM(spotify_token, line_content[3], line_content[4], 1) [0][2]
                                              
                                        # get volume
                                        album_volume = int(line_content[5])
                                        
                                        SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)


                                except Exception as e:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))
            
                                            
                            else:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Programm - " + GET_PROGRAM_BY_ID(program_id).name + " | No Spotify Token founded")   

                            
                        line_number = line_number + 1
                        time.sleep(1)
               
                    
            # ################     
            # repeat program ?
            # ################

            if repeat_program == True:        
                repeat = True
            else:
                repeat = False
                
        
        SET_PROGRAM_STATUS("None")    
        time.sleep(10)
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")
                

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Programm - " + GET_PROGRAM_BY_ID(program_id).name + " | " + str(e))
        return str(e)