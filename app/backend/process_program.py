import threading
import heapq
import time
import spotipy

from app                          import app
from app.database.models          import *
from app.backend.file_management  import *
from app.backend.shared_resources import *
from app.backend.mqtt             import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD, REQUEST_SENSORDATA
from app.backend.lighting         import *
from app.backend.spotify          import *


stop_program_thread_1 = False
stop_program_thread_2 = False
stop_program_thread_3 = False
stop_program_thread_4 = False
stop_program_thread_5 = False
stop_program_thread_6 = False


def START_PROGRAM_THREAD(program_id):

    try:

        if GET_PROGRAM_THREAD_STATUS_1()[0] == "None":
            thread_id    = 1
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_1 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_1.start()   
   
            SET_PROGRAM_THREAD_STATUS_1(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True
    
        elif GET_PROGRAM_THREAD_STATUS_2()[0] == "None":
            thread_id    = 2
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_2 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_2.start()   
   
            SET_PROGRAM_THREAD_STATUS_2(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_3()[0] == "None":
            thread_id    = 3
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_3 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_3.start()   
   
            SET_PROGRAM_THREAD_STATUS_3(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_4()[0] == "None":
            thread_id    = 4
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_4 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_4.start()   
   
            SET_PROGRAM_THREAD_STATUS_4(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_5()[0] == "None":
            thread_id    = 5
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_5 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_5.start()   
   
            SET_PROGRAM_THREAD_STATUS_5(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_6()[0] == "None":
            thread_id    = 6
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_6 = threading.Thread(target = PROGRAM_THREAD, args =(lambda : True,thread_id,program_id, )) 
            program_thread_6.start()   
   
            SET_PROGRAM_THREAD_STATUS_6(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        else:
            return ("No empty program tread founded")

    except Exception as e:
        return e



def STOP_PROGRAM_THREAD_BY_ID(thread_id):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5    
    global stop_program_thread_6   

    if thread_id == 1 :
        stop_program_thread_1 = True
        program_name = GET_PROGRAM_THREAD_STATUS_1()[0]
        SET_PROGRAM_THREAD_STATUS_1(program_name,0,0,"STOPPED")
        return True

    if thread_id == 2 :
        stop_program_thread_2 = True
        program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
        SET_PROGRAM_THREAD_STATUS_2(program_name,0,0,"STOPPED")
        return True

    if thread_id == 3 :
        stop_program_thread_3 = True
        program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
        SET_PROGRAM_THREAD_STATUS_3(program_name,0,0,"STOPPED")
        return True

    if thread_id == 4 :
        stop_program_thread_4 = True
        program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
        SET_PROGRAM_THREAD_STATUS_4(program_name,0,0,"STOPPED")
        return True

    if thread_id == 5 :
        stop_program_thread_5 = True
        program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
        SET_PROGRAM_THREAD_STATUS_5(program_name,0,0,"STOPPED")
        return True

    if thread_id == 6 :
        stop_program_thread_6 = True
        program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
        SET_PROGRAM_THREAD_STATUS_6(program_name,0,0,"STOPPED")
        return True


def STOP_PROGRAM_THREAD_BY_NAME(program_name):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5    
    global stop_program_thread_6  

    try:

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_1()[0].lower():
            stop_program_thread_1 = True
            program_name = GET_PROGRAM_THREAD_STATUS_1()[0]
            SET_PROGRAM_THREAD_STATUS_1(program_name,0,0,"STOPPED")            
            return True

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_2()[0].lower():
            stop_program_thread_2 = True
            program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
            SET_PROGRAM_THREAD_STATUS_2(program_name,0,0,"STOPPED")                   
            return True

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_3()[0].lower():
            stop_program_thread_3 = True
            program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
            SET_PROGRAM_THREAD_STATUS_3(program_name,0,0,"STOPPED")                   
            return True

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_4()[0].lower():
            stop_program_thread_4 = True
            program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
            SET_PROGRAM_THREAD_STATUS_4(program_name,0,0,"STOPPED")                   
            return True

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_5()[0].lower():
            stop_program_thread_5 = True
            program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
            SET_PROGRAM_THREAD_STATUS_5(program_name,0,0,"STOPPED")                   
            return True

        if program_name.lower() == GET_PROGRAM_THREAD_STATUS_6()[0].lower():
            stop_program_thread_6 = True
            program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
            SET_PROGRAM_THREAD_STATUS_6(program_name,0,0,"STOPPED")                   
            return True

    except:
        pass

   
def PROGRAM_THREAD(running, thread_id, program_id):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5
    global stop_program_thread_6


    try:

        list_lines = [[GET_PROGRAM_BY_ID(program_id).line_active_1,  GET_PROGRAM_BY_ID(program_id).line_content_1],
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
                      [GET_PROGRAM_BY_ID(program_id).line_active_20, GET_PROGRAM_BY_ID(program_id).line_content_20],                  
                      [GET_PROGRAM_BY_ID(program_id).line_active_21, GET_PROGRAM_BY_ID(program_id).line_content_21],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_22, GET_PROGRAM_BY_ID(program_id).line_content_22],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_23, GET_PROGRAM_BY_ID(program_id).line_content_23],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_24, GET_PROGRAM_BY_ID(program_id).line_content_24],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_25, GET_PROGRAM_BY_ID(program_id).line_content_25],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_26, GET_PROGRAM_BY_ID(program_id).line_content_26],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_27, GET_PROGRAM_BY_ID(program_id).line_content_27],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_28, GET_PROGRAM_BY_ID(program_id).line_content_28], 
                      [GET_PROGRAM_BY_ID(program_id).line_active_29, GET_PROGRAM_BY_ID(program_id).line_content_29],  
                      [GET_PROGRAM_BY_ID(program_id).line_active_30, GET_PROGRAM_BY_ID(program_id).line_content_30]] 


        program_name = GET_PROGRAM_BY_ID(program_id).name

        # get total lines
        lines_total = 0

        for line in list_lines:
            if line[0] == "True":
                lines_total = lines_total + 1


        line_number = 1

        for line in list_lines:
            
            # stop program
            if thread_id == 1 and stop_program_thread_1 == True:
                stop_program_thread_1 = False  
                
                SET_PROGRAM_THREAD_STATUS_1("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            if thread_id == 2 and stop_program_thread_2 == True:
                stop_program_thread_2 = False  
                
                SET_PROGRAM_THREAD_STATUS_2("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            if thread_id == 3 and stop_program_thread_3 == True:
                stop_program_thread_3 = False  
                
                SET_PROGRAM_THREAD_STATUS_3("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            if thread_id == 4 and stop_program_thread_4 == True:
                stop_program_thread_4 = False  
                
                SET_PROGRAM_THREAD_STATUS_4("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            if thread_id == 5 and stop_program_thread_5 == True:
                stop_program_thread_5 = False  
                
                SET_PROGRAM_THREAD_STATUS_5("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            if thread_id == 6 and stop_program_thread_6 == True:
                stop_program_thread_6 = False  
                
                SET_PROGRAM_THREAD_STATUS_6("None",0,0,"")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                break

            # program running
            else:

                # update program status
                if thread_id == 1:
                    SET_PROGRAM_THREAD_STATUS_1(program_name,line_number,lines_total,line[1])
                if thread_id == 2:
                    SET_PROGRAM_THREAD_STATUS_2(program_name,line_number,lines_total,line[1])
                if thread_id == 3:
                    SET_PROGRAM_THREAD_STATUS_3(program_name,line_number,lines_total,line[1])
                if thread_id == 4:
                    SET_PROGRAM_THREAD_STATUS_4(program_name,line_number,lines_total,line[1])
                if thread_id == 5:
                    SET_PROGRAM_THREAD_STATUS_5(program_name,line_number,lines_total,line[1])
                if thread_id == 6:
                    SET_PROGRAM_THREAD_STATUS_6(program_name,line_number,lines_total,line[1])

                # line active ?
                if line[0] == "True":


                    # #####
                    # break
                    # #####
                            
                    if "break" in line[1]:
                            
                        line_content = line[1].split(" # ")
                        time.sleep(int(line_content[1]))          

                    # #####
                    # light
                    # #####
                                
                    if "lighting" in line[1] and "scene" in line[1]:
                            
                        line_content = line[1].split(" # ")
                        
                        try:
                            # start lighting scene
                            if line_content[2].lower() != "turn_off":
                                group_name        = line_content[2] 
                                scene_name        = line_content[3]
                                global_brightness = line_content[4]
                                group             = GET_LIGHTING_GROUP_BY_NAME(group_name)
                                scene             = GET_LIGHTING_SCENE_BY_NAME(scene_name)

                                SET_LIGHTING_GROUP_SCENE(group.id, scene.id, int(global_brightness))
                                CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, global_brightness, 2, 10)

                            # turn off group
                            elif line_content[2].lower() == "turn_off" and line_content[3].lower() == "all":
                                group      = GET_LIGHTING_GROUP_BY_NAME(group_name)
                                scene_name = group.current_scene
                                scene      = GET_LIGHTING_SCENE_BY_NAME(scene_name)
                                                
                                SET_LIGHTING_GROUP_TURN_OFF(group.id)
                                CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 2, 10)   

                                            
                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))


                    # ######    
                    # device
                    # ######

                    if "device" in line[1]:
                            
                        line_content = line[1].split(" # ")

                        try:
                                    
                            # get input group names 
                            for device_name in line_content[1].split(","): 
                                device = GET_DEVICE_BY_NAME(device_name.strip())

                                # device founded ?
                                if device != None:
                                    program_setting = line_content[2]
                                    
                                    # check device exception
                                    check_result = CHECK_DEVICE_EXCEPTIONS(device.id, program_setting)
                                                
                                    if check_result == True:           
                                        
                                        if device.gateway == "mqtt":
                                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                                        if device.gateway == "zigbee2mqtt":   
                                                channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                                        command_position  = 0
                                        list_command_json = device.commands_json.split(",")

                                        # get the json command statement and start process
                                        for command in device.commands.split(","):     
                                                            
                                            if program_setting in command:
                                                heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                                                CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, program_setting, 20)      
                                                break

                                                command_position = command_position + 1

                                    else:
                                        WRITE_LOGFILE_SYSTEM("WARNING", "Program - " + program_name + " | " + check_result)

                                else:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Device - " + device_name.strip() + " - not founded")     

                            
                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))


                    # ##################
                    # request sensordata
                    # ##################

                    if "request_sensordata" in line[1]:

                        line_content = line[1].split(" # ")

                        try:
                            job_number = line_content[1]    
                            REQUEST_SENSORDATA(job_number)              

                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | " + str(e))


                    # ########
                    # programs
                    # ########

                    if "program" in line[1]:
                        
                        line_content = line[1].split(" # ")

                        program = GET_PROGRAM_BY_NAME(line_content[1])

                        if program != None:

                            if line_content[2].lower() == "start":
                                START_PROGRAM_THREAD(program.id)
                                
                            elif line_content[2].lower() == "stop":
                                STOP_PROGRAM_THREAD_BY_NAME(program.name)

                            else:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | Invalid command")

                        else:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Zeile - " + line[1] + " | Program - " + program + " - not founded")


                    # #######
                    # spotify
                    # #######

                    if "spotify" in line[1]:
                            
                        line_content = line[1].split(" # ")

                        if GET_SPOTIFY_TOKEN() == "" and GET_SPOTIFY_REFRESH_TOKEN() != "":
                            GENERATE_SPOTIFY_TOKEN()

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


        if thread_id == 1:
            SET_PROGRAM_THREAD_STATUS_1("None",0,0,"")  
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 2:
            SET_PROGRAM_THREAD_STATUS_2("None",0,0,"") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 3:
            SET_PROGRAM_THREAD_STATUS_3("None",0,0,"") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 4:
            SET_PROGRAM_THREAD_STATUS_4("None",0,0,"") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 5:
            SET_PROGRAM_THREAD_STATUS_5("None",0,0,"")  
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 6:
            SET_PROGRAM_THREAD_STATUS_6("None",0,0,"")  
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")


    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Programm - " + GET_PROGRAM_BY_ID(program_id).name + " | " + str(e))
        return str(e)