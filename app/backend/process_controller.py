import spotipy
import re
import json
import time

from app                          import app
from app.database.models          import *
from app.backend.led              import *
from app.backend.mqtt             import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.process_program  import START_PROGRAM_THREAD, STOP_PROGRAM_THREAD
from app.backend.spotify          import *
from app.backend.shared_resources import mqtt_message_queue, GET_PROGRAM_STATUS

from difflib import SequenceMatcher


""" ################################ """
""" ################################ """
"""        process controller        """
""" ################################ """
""" ################################ """


def PROCESS_CONTROLLER(ieeeAddr, msg):

    for controller in GET_ALL_CONTROLLER():
        
        if controller.device_ieeeAddr == ieeeAddr:
            
            # #########
            # command_1
            # #########
            
            try:                                                                                    
                if str(controller.command_1)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_1, controller.device.name, controller.command_1)                      
                    return
                            
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_1[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_2
            # #########
            
            try:

                if str(controller.command_2)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_2, controller.device.name, controller.command_2)                
                    return
                          
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_3
            # #########

            try:

                if str(controller.command_3)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_3, controller.device.name, controller.command_3)               
                    return                      
           
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_3[1:-1].replace('"','') + " | " + str(e))    
                                           
            # #########
            # command_4
            # #########
            
            try:

                if str(controller.command_4)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_4, controller.device.name, controller.command_4)                 
                    return
                            
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_4[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_5
            # #########
            
            try:

                if str(controller.command_5)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_5, controller.device.name, controller.command_5)                    
                    return
                            
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_5[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_6
            # #########
            
            try:

                if str(controller.command_6)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_6, controller.device.name, controller.command_6)                    
                    return
                               
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_6[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_7
            # #########
            
            try:
           
                if str(controller.command_7)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_7, controller.device.name, controller.command_7)                   
                    return                      
           
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_7[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_8
            # #########
            
            try:                                            
                                                
                if str(controller.command_8)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_8, controller.device.name, controller.command_8)                   
                    return
                            
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_8[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_9
            # #########
            
            try:

                if str(controller.command_9)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_9, controller.device.name, controller.command_9)                    
                    return
           
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_9[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_10
            # ##########
            
            try:                                              
                                            
                if str(controller.command_10)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_10, controller.device.name, controller.command_10)                 
                    return
        
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_10[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_11
            # ##########
            
            try:
                                                                       
                if str(controller.command_11)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_11, controller.device.name, controller.command_11)               
                    return
           
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_11[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_12
            # ##########
            
            try:

                if str(controller.command_12)[1:-1] in str(msg):
                    START_CONTROLLER_TASK(controller.task_12, controller.device.name, controller.command_12)            
                    return
           
            except Exception as e:
                if "list index out of range" not in str(e) and "Expecting value: line 1 column 1 (char 0)" not in str(e):
                    print(e)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + 
                                         controller.command_12[1:-1].replace('"','') + " | " + str(e))    


""" ################################ """
""" ################################ """
"""         controller tasks         """
""" ################################ """
""" ################################ """


def START_CONTROLLER_TASK(task, controller_name, controller_command):

    controller_command = controller_command[1:-1].replace('"','')


    # ###########
    # start scene
    # ###########

    if "scene" in task:

        task = task.lower()
        task = task.split(" # ")
        
        group = GET_LED_GROUP_BY_NAME(task[1])
        scene = GET_LED_SCENE_BY_NAME(task[2])

        # group existing ?
        if group != None:

            # scene existing ?
            if scene != None:

                try:
                    brightness = int(task[3])
                except:
                    brightness = 100
                    
                SET_LED_GROUP_SCENE(group.id, scene.id, brightness)
                CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " +
                                     controller_command + " | Scene - " + task[2] + " | not founded")

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " +
                                 controller_command + " | Group - " + task[1] + " | not founded")

    # #################
    # change brightness
    # #################

    if "brightness" in task:
        
        task = task.lower()
        task = task.split(" # ")
        
        group   = GET_LED_GROUP_BY_NAME(task[1])
        command = task[2]

        # group existing ?
        if group != None:

            # command valid ?
            if command == "turn_up" or command == "turn_down":
                
                scene_name = group.current_scene

                # led_group off ?
                if scene_name != "off":
                    
                    scene = GET_LED_SCENE_BY_NAME(scene_name)

                    # get new brightness_value
                    current_brightness = group.current_brightness

                    if (command == "turn_up") and current_brightness != 100:
                        target_brightness = int(current_brightness) + 20

                        if target_brightness > 100:
                            target_brightness = 100

                        SET_LED_GROUP_BRIGHTNESS_DIMMER(group.id, "turn_up")
                        CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, target_brightness, 2, 10)

                    elif (command == "turn_down") and current_brightness != 0:

                        target_brightness = int(current_brightness) - 20

                        if target_brightness < 0:
                            target_brightness = 0

                        SET_LED_GROUP_BRIGHTNESS_DIMMER(group.id, "turn_down")
                        CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, target_brightness, 2, 10)

                    else:
                        WRITE_LOGFILE_SYSTEM("STATUS", "Light | Group - " + group.name +
                                             " | " + scene_name + " : " + str(current_brightness) + " %")

                else:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Light | Group - " +
                                         group.name + " | OFF : 0 %")

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " +
                                     controller_command + " | Command - " + task[2] + " | not valid")

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " +
                                 controller_command + " | Group - " + task[1] + " | not founded")

    # #######
    # led off
    # #######

    if "led_off" in task:
        
        task = task.lower()
        task = task.split(" # ")

        if task[1] == "group":

            # get input group names and lower the letters
            try:
                list_groups = task[2].split(",")
            except:
                list_groups = [task[2]]

            for input_group_name in list_groups:
                input_group_name = input_group_name.replace(" ", "")

                group_founded = False

            # get exist group names
            for group in GET_ALL_LED_GROUPS():

                if input_group_name == group.name.lower():
                    group_founded = True
                    scene_name    = group.current_scene
                    scene         = GET_LED_SCENE_BY_NAME(scene_name)

                    SET_LED_GROUP_TURN_OFF(group.id)
                    CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 2, 10)

            # group not founded
            if group_founded == False:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " +
                                     controller_command + " | Group - " + input_group_name + " | not founded")

        if task[1] == "all":
            for group in GET_ALL_LED_GROUPS():
                scene_name = group.current_scene
                scene      = GET_LED_SCENE_BY_NAME(scene_name)

                SET_LED_GROUP_TURN_OFF(group.id)
                CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 2, 10)

    # ######
    # device
    # ######

    if "device" in task:
        task   = task.split(" # ")
        device = GET_DEVICE_BY_NAME(task[1].lower())
        
        # device founded ?
        if device != None:
            
            controller_setting = task[2]

            # check device exception
            check_result = CHECK_DEVICE_EXCEPTIONS(device.id, controller_setting)
                 
            if check_result == True:               

                if device.gateway == "mqtt":
                    channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                if device.gateway == "zigbee2mqtt":   
                    channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                command_position  = 0
                list_command_json = device.commands_json.split(",")

                # get the json command statement and start process
                for command in device.commands.split(","):     
                                    
                    if controller_setting in command:
                        heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                        CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, controller_setting, 20)      
                        break

                    command_position = command_position + 1
                           
            else:
                WRITE_LOGFILE_SYSTEM("WARNING", "Network | Controller - " + controller_name + " | " + check_result)
                                
        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " + controller_command + " | Gerät - " + task[1] + " | not founded")


    # ##################
    # request sensordata
    # ##################

    if "request_sensordata" in task:

        task = task.lower()
        task = task.split(" # ")

        job_number = task[1]    
        REQUEST_SENSORDATA(job_number)              


    # ########
    # programs
    # ########

    if "program" in task:
        
        task = task.lower()
        task = task.split(" # ")
        
        program = GET_PROGRAM_BY_NAME(task[1].lower())

        if program != None:

            if task[2] == "start" and GET_PROGRAM_STATUS() == None:
                START_PROGRAM_THREAD(program.id)
                
            elif task[2] == "start" and GET_PROGRAM_STATUS() != None:
                WRITE_LOGFILE_SYSTEM("WARNING", "Network | Controller - " + controller_name + " | Command - " + controller_command + " | Other Program running")
                                     
            elif task[2] == "stop":
                STOP_PROGRAM_THREAD()
                
            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " + controller_command + " | Command not valid")

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " + controller_command + " | Program not founded")


    # #######
    # spotify
    # #######

    if "spotify" in task:
        
        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "":
            
            task = task.lower()         
            task = task.split(" # ")
            
            sp       = spotipy.Spotify(auth=spotify_token)
            sp.trace = False
            
            try:
                spotify_volume = sp.current_playback(market=None)['device']['volume_percent']
            except:
                spotify_volume = 50
            
            if task[1] == "play":
                SPOTIFY_CONTROL(spotify_token, "play", spotify_volume) 

            if task[1] == "play/stop":
                SPOTIFY_CONTROL(spotify_token, "play/stop", spotify_volume) 

            if task[1] == "previous": 
                SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

            if task[1] == "next":
                SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

            if task[1] == "stop": 
                SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)      

            if task[1] == "volume_up":   
                device_name = sp.current_playback(market=None)['device']['name']
                SPOTIFY_CONTROL(spotify_token, "volume_up", spotify_volume)

            if task[1] == "volume_down":   
                device_name = sp.current_playback(market=None)['device']['name']
                SPOTIFY_CONTROL(spotify_token, "volume_down", spotify_volume)                 

            if task[1].lower() == "volume":            
                spotify_volume = int(task[2])
                SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  


            # start playlist
                    
            if task[1].lower() == "playlist": 
                
                # get spotify_device_id
                device_name          = task[2]                                    
                list_spotify_devices = sp.devices()["devices"]  
                spotify_device_id    = 0
                
                for device in list_spotify_devices:

                    # spotify client
                    if device['name'].lower() == device_name.lower():
                        spotify_device_id = device['id']  
                        continue      

                    # select multiroom group
                    if device_name.lower() == "multiroom":
                        if "multiroom" in device['name'].lower():
                            spotify_device_id = device['id'] 
                            continue    

                # if device not founded, reset raspotify on client music               
                if spotify_device_id == 0:
                    device = GET_DEVICE_BY_NAME(device_name)

                    heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                    time.sleep(5)

                    for device in list_spotify_devices:

                        # spotify client
                        if device['name'].lower() == device_name.lower():
                            spotify_device_id = device['id']  
                            continue      

                        # select multiroom group
                        if device_name.lower() == "multiroom":
                            if "multiroom" in device['name'].lower():
                                spotify_device_id = device['id'] 
                                continue                        
            
                # get playlist_uri
                playlist_name          = task[3]
                list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]
                
                for playlist in list_spotify_playlists:
                    if playlist['name'].lower() == playlist_name.lower():
                        playlist_uri = playlist['uri']
                        continue
         
                # get volume
                playlist_volume = int(task[4]) 
                SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
        
        
            # start track
                    
            if task[1].lower() == "track": 

                # get spotify_device_id
                device_name          = task[2]                                    
                list_spotify_devices = sp.devices()["devices"]  
                spotify_device_id    = 0
                
                for device in list_spotify_devices:

                    # spotify client
                    if device['name'].lower() == device_name.lower():
                        spotify_device_id = device['id']  
                        continue      

                    # select multiroom group
                    if device_name.lower() == "multiroom":
                        if "multiroom" in device['name'].lower():
                            spotify_device_id = device['id'] 
                            continue    

                # if device not founded, reset raspotify on client music               
                if spotify_device_id == 0:
                    device = GET_DEVICE_BY_NAME(device_name)

                    heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                    time.sleep(5)

                    for device in list_spotify_devices:

                        # spotify client
                        if device['name'].lower() == device_name.lower():
                            spotify_device_id = device['id']  
                            continue      

                        # select multiroom group
                        if device_name.lower() == "multiroom":
                            if "multiroom" in device['name'].lower():
                                spotify_device_id = device['id'] 
                                continue                            
           
                # get playlist_uri
                track_uri = SPOTIFY_SEARCH_TRACK(spotify_token, task[3], task[4], 1) [0][2]
                      
                # get volume
                track_volume = int(task[5])
                
                SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)


            # start album
                    
            if task[1].lower() == "album": 

                # get spotify_device_id
                device_name          = task[2]                                    
                list_spotify_devices = sp.devices()["devices"]  
                spotify_device_id    = 0
                
                for device in list_spotify_devices:

                    # spotify client
                    if device['name'].lower() == device_name.lower():
                        spotify_device_id = device['id']  
                        continue      

                    # select multiroom group
                    if device_name.lower() == "multiroom":
                        if "multiroom" in device['name'].lower():
                            spotify_device_id = device['id'] 
                            continue    

                # if device not founded, reset raspotify on client music               
                if spotify_device_id == 0:
                    device = GET_DEVICE_BY_NAME(device_name)

                    heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                    time.sleep(5)

                    for device in list_spotify_devices:

                        # spotify client
                        if device['name'].lower() == device_name.lower():
                            spotify_device_id = device['id']  
                            continue      

                        # select multiroom group
                        if device_name.lower() == "multiroom":
                            if "multiroom" in device['name'].lower():
                                spotify_device_id = device['id'] 
                                continue                                 
                
                # get album_uri
                album_uri = SPOTIFY_SEARCH_ALBUM(spotify_token, task[3], task[4], 1) [0][2]
                      
                # get volume
                album_volume = int(task[5])
                
                SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)
   
        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller_name + " | Command - " + controller_command + " | No Spotify Token founded")