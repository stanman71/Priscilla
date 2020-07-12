from app.backend.lighting         import *
from app.backend.mqtt             import *
from app.backend.spotify          import *
from app.backend.file_management  import BACKUP_DATABASE
from app.backend.shared_resources import *

import spotipy
import re
import json
import time


def START_TASK(task, source, error_informations, blocked_program_thread_id = 0):

    try:
    
        # ############################
        # group - start lighting scene
        # ############################

        if "lighting" in task and "start_scene" in task and "turn_off" not in task:
            task = task.split(" # ")
            
            group = GET_LIGHTING_GROUP_BY_NAME(task[2].strip())
            scene = GET_LIGHTING_SCENE_BY_NAME(task[3].strip())

            # group existing ?
            if group != None:

                # group not empty ?
                if group.light_ieeeAddr_1 != "None":

                    # scene existing ?
                    if scene != None:

                        try:
                            brightness = int(task[4].strip())
                        except:
                            brightness = 100
                            
                        SET_LIGHTING_GROUP_SCENE(group.id, scene.id, brightness)
                        CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

                    else:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Scene - " + task[3] + " | missing")

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | empty")             
                
            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | missing")


        # #######################################
        # group - start lighting scene / turn off
        # #######################################

        if "lighting" in task and "start_scene" in task and "turn_off" in task:
            task = task.split(" # ")
            
            group = GET_LIGHTING_GROUP_BY_NAME(task[2].strip())
            scene = GET_LIGHTING_SCENE_BY_NAME(task[3].strip())

            # group existing ?
            if group != None:

                # group not empty ?
                if group.light_ieeeAddr_1 != "None":

                    if group.current_scene != "OFF":

                        SET_LIGHTING_GROUP_TURN_OFF(group.id)
                        CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)                      

                    else:

                        # scene existing ?
                        if scene != None:          
                                
                            try:
                                brightness = int(task[4].strip())
                            except:
                                brightness = 100
                                
                            SET_LIGHTING_GROUP_SCENE(group.id, scene.id, brightness)
                            CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

                        else:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Scene - " + task[3] + " | missing")

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | empty")                        

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | missing")


        # #############################
        # group - rotate lighting scene
        # #############################

        if "lighting" in task and "rotate_scene" in task:
            task = task.split(" # ") 

            group = GET_LIGHTING_GROUP_BY_NAME(task[2].strip())

            # group existing ?
            if group != None:

                # group not empty ?
                if group.light_ieeeAddr_1 != "None":

                    # create list of scene names
                    list_scene_names = []

                    for scene in GET_ALL_LIGHTING_SCENES():
                        list_scene_names.append(scene.name)

                    # find position of current scene
                    scene_position = 0

                    for position, scene_name in enumerate(list_scene_names):
                        if scene_name == group.current_scene:
                            scene_position = position

                    # get next scene
                    try:
                        # current scene is not the last scene
                        next_scene = list_scene_names[scene_position + 1]
                    except:
                        # current scene is the last scene
                        next_scene = list_scene_names[0]


                    scene      = GET_LIGHTING_SCENE_BY_NAME(next_scene)    
                    brightness = group.current_brightness
                            
                    SET_LIGHTING_GROUP_SCENE(group.id, scene.id, brightness)
                    CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | empty")            

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | missing")


        # #########################
        # group - change brightness
        # #########################

        if "lighting" in task and "brightness" in task:
            task = task.split(" # ")
            
            group   = GET_LIGHTING_GROUP_BY_NAME(task[2].strip())
            command = task[3].strip()

            # group existing ?
            if group != None:

                # group not empty ?
                if group.light_ieeeAddr_1 != "None":

                    # command valid ?
                    if command.lower() == "turn_up" or command.lower() == "turn_down":
                        
                        scene_name = group.current_scene

                        # lighting_group off ?
                        if scene_name != "off":
                            
                            scene = GET_LIGHTING_SCENE_BY_NAME(scene_name)

                            # get new brightness_value
                            current_brightness = group.current_brightness

                            if (command.lower() == "turn_up") and current_brightness != 100:
                                target_brightness = int(current_brightness) + 20

                                if target_brightness > 100:
                                    target_brightness = 100

                                SET_LIGHTING_GROUP_BRIGHTNESS_DIMMER(group.id, "turn_up")
                                CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, target_brightness, 2, 10)

                            elif (command.lower() == "turn_down") and current_brightness != 0:

                                target_brightness = int(current_brightness) - 20

                                if target_brightness < 10:
                                    target_brightness = 10

                                SET_LIGHTING_GROUP_BRIGHTNESS_DIMMER(group.id, "turn_down")
                                CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, target_brightness, 2, 10)

                            else:
                                WRITE_LOGFILE_SYSTEM("STATUS", "Light | Group - " + group.name +
                                                    " | " + scene_name + " : " + str(current_brightness) + " %")

                        else:
                            WRITE_LOGFILE_SYSTEM("WARNING", "Light | Group - " + group.name + " | OFF : 0 %")

                    else:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Command - " + task[3] + " | invalid")

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | empty")            

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + task[2] + " | missing")


        # ###################
        # light - start light
        # ###################

        if "lighting" in task and "light" in task and "start_scene" not in task and "turn_off" not in task:
            task = task.split(" # ") 
                    
            device = GET_DEVICE_BY_NAME(task[2].strip())

            # device existing ?
            if device != None:

                try:
                    rgb_values = re.findall(r'\d+', task[3])
                except:
                    rgb_values = []                                        

                try:
                    brightness = int(task[4].strip())
                except:
                    brightness = 100     

                if rgb_values != []:    
                    SET_LIGHT_RGB_THREAD(device.ieeeAddr, rgb_values[0], rgb_values[1], rgb_values[2], brightness)
                    CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "ON", 10)

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Invalid settings")  

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Light - " + task[2] + " | missing")   


        # #########
        # light off
        # #########

        if "lighting" in task and "turn_off" in task:
            task = task.split(" # ")

            if task[2].lower() == "group":

                # get input group names and lower the letters
                try:
                    list_groups = task[3].split(",")
                except:
                    list_groups = [task[3]]

                for input_group_name in list_groups:
                    input_group_name = input_group_name.strip()

                    group_found = False

                # get exist group names
                for group in GET_ALL_LIGHTING_GROUPS():

                    if input_group_name.lower() == group.name.lower():
                        group_found = True

                        # group not empty ?
                        if group.light_ieeeAddr_1 != "None":               

                            SET_LIGHTING_GROUP_TURN_OFF(group.id)
                            CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   

                        else:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + input_group_name + " | empty")            

                # group not found
                if group_found == False:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + input_group_name + " | missing")


            elif task[2].lower() == "light":

                device = GET_DEVICE_BY_NAME(task[3].strip())

                # device existing ?
                if device != None:                            
                    SET_LIGHT_TURN_OFF_THREAD(device.ieeeAddr)
                    CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "OFF", 10)

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Light - " + task[3].strip() + " | missing")


            elif task[2].lower() == "all":

                for light in GET_ALL_DEVICES("light"):
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(light.ieeeAddr, ))
                    Thread.start()   

                for group in GET_ALL_LIGHTING_GROUPS():

                    # group not empty ?
                    if group.light_ieeeAddr_1 != "None":  

                        CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   

                    else:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Group - " + group.name + " | empty")      

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | No Target found")      


        # ######
        # device
        # ######

        if "device" in task:  
            task = task.split(" # ")
            
            # get input group names 
            for device_name in task[1].split(","): 
                device = GET_DEVICE_BY_NAME(device_name.strip())

                # device found ?
                if device != None:
                    controller_command = task[2].strip()
                    
                    # check device exception
                    check_result = CHECK_DEVICE_EXCEPTIONS(device.ieeeAddr, controller_command)
                                
                    if check_result == True:           

                        if device.gateway == "mqtt":

                            # special case roborock s50
                            if device.model == "roborock_s50": 
                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/command"  
                            else:
                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  

                        if device.gateway == "zigbee2mqtt":   
                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                        command_position  = 0

                        # special case roborock s50
                        if device.model == "roborock_s50":
                            list_command_json = device.commands_json.split(",")

                        else:
                            list_command_json = device.commands_json.replace("},{", "};{")                       
                            list_command_json = list_command_json.split(";")

                        # get the json command statement and start process
                        for command in device.commands.split(","):     
                                                    
                            if str(controller_command.lower()) == command.lower():

                                # special case roborock s50
                                if device.model == "roborock_s50" and controller_command.lower() == "return_to_base":
                                    heapq.heappush(mqtt_message_queue, (10, (channel, "stop")))            
                                    time.sleep(5)
                                    heapq.heappush(mqtt_message_queue, (10, (channel, "return_to_base")))                               
                                    CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, controller_command, 60)  
                                    continue    

                                else:
                                    heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                                    CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, controller_command, 60)      
                                    continue

                            command_position = command_position + 1
        
                    else:
                        WRITE_LOGFILE_SYSTEM("WARNING","Task | " + source + " | " + str(error_informations) + " | " + check_result)
                                        
                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Gerät - " + task[1] + " | missing")        
        

        # ##################
        # request sensordata
        # ##################

        if "request_sensordata" in task:
            task       = task.split(" # ")
            job_number = task[1].strip()    

            REQUEST_SENSORDATA(job_number)              


        # ###############
        # backup database
        # ###############

        if "backup_database" in task:
            BACKUP_DATABASE()


        # #############
        # backup zigbee
        # #############

        if "backup_zigbee" in task:
            BACKUP_ZIGBEE()


        # ##############
        # update devices
        # ##############

        if "update_devices" in task:
            UPDATE_DEVICES("mqtt")
            UPDATE_DEVICES("zigbee2mqtt")


        # ###############
        # reset log files
        # ###############

        if "reset_log_files" in task:

            # reset device log if size > 2,5 mb
            file_size = os.path.getsize(PATH + "/data/logs/log_devices.csv")
            file_size = round(file_size / 1024 / 1024, 2)

            if file_size > 2.5:
                RESET_LOGFILE("log_devices")

            # reset system log if size > 2.5 mb
            file_size = os.path.getsize(PATH + "/data/logs/log_system.csv")
            file_size = round(file_size / 1024 / 1024, 2)

            if file_size > 2.5:
                RESET_LOGFILE("log_system")

            # delete system2mqtt log if size > 5 mb
            file_size = os.path.getsize(PATH + "/data/logs/zigbee2mqtt.txt")
            file_size = round(file_size / 1024 / 1024, 2)

            if file_size > 5:
                os.remove(PATH + "/data/logs/zigbee2mqtt.txt")


        # ############
        # reset system
        # ############

        if "reset_system" in task:
            WRITE_LOGFILE_SYSTEM("EVENT", "System | Reboot")
            os.system("sudo reboot")


        # ###############
        # shutdown system
        # ###############

        if "shutdown_system" in task:
            WRITE_LOGFILE_SYSTEM("EVENT", "System | Shutdown")
            os.system("sudo shutdown")


        # ########
        # programs
        # ########

        if "program" in task:   
            task    = task.split(" # ") 
            program = GET_PROGRAM_BY_NAME(task[1].strip())

            if program != None:

                if task[2].strip() == "START":
                    heapq.heappush(process_management_queue, (10, ("program", "start", program.id)))  

                elif task[2].strip() == "STOP":
                    heapq.heappush(process_management_queue, (10, ("program", "stop", program.name, blocked_program_thread_id)))  
     
                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Invalid command")

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | Program - " + program + " | missing")


        # #####
        # music
        # #####

        if "music" in task:  
            spotify_token = GET_SPOTIFY_TOKEN()
            
            if spotify_token != "":
                    
                task = task.split(" # ")
                
                sp       = spotipy.Spotify(auth=spotify_token)
                sp.trace = False

                # basic control 

                if (task[1].strip() == "PLAY" or
                    task[1].strip() == "PLAY/STOP" or            
                    task[1].strip() == "PREVIOUS" or
                    task[1].strip() == "NEXT" or
                    task[1].strip() == "STOP" or
                    task[1].strip() == "VOLUME_UP" or
                    task[1].strip() == "VOLUME_DOWN" or                
                    task[1].strip() == "VOLUME"):
                
                    try: 
                        spotify_volume = sp.current_playback(market=None)['device']['volume_percent']
                    except:
                        spotify_volume = GET_SPOTIFY_SETTINGS().default_volume

                    if task[1].strip() == "PLAY":
                        SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       
        
                    if task[1].strip() == "PLAY/STOP":
                        SPOTIFY_CONTROL(spotify_token, "play/stop", spotify_volume)       

                    if task[1].strip() == "PREVIOUS":
                        SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                    if task[1].strip() == "NEXT":
                        SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                    if task[1].strip() == "STOP": 
                        SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                    if task[1].strip() == "VOLUME_UP":   
                        device_name = sp.current_playback(market=None)['device']['name']
                        SPOTIFY_CONTROL(spotify_token, "volume_up", spotify_volume)

                    if task[1].strip() == "VOLUME_DOWN":   
                        device_name = sp.current_playback(market=None)['device']['name']
                        SPOTIFY_CONTROL(spotify_token, "volume_down", spotify_volume)         

                    if task[1].strip() == "VOLUME":            
                        spotify_volume = int(task[2])
                        SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  

                # start playlist
                        
                if task[1].strip() == "playlist": 
                    
                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip()) 
                    playlist_uri      = GET_SPOTIFY_PLAYLIST(spotify_token, task[3].strip(), 20)
                    playlist_volume   = int(task[4]) 

                    SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
            
                # start track
                        
                if task[1].strip() == "track": 

                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip())                  
                    track_uri         = SPOTIFY_SEARCH_TRACK(spotify_token, task[3].strip(), task[4].strip(), 1) [0][2]
                    track_volume      = int(task[5].strip())
                    
                    SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)

                # start album
                        
                if task[1].strip() == "album": 
                                
                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip())                        
                    album_uri         = SPOTIFY_SEARCH_ALBUM(spotify_token, task[3].strip(), task[4].strip(), 1) [0][2]
                    album_volume      = int(task[5].strip())
                    
                    SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)

                # change interface
                        
                if task[1].strip() == "interface": 

                    device = GET_DEVICE_BY_NAME(task[2].strip())

                    # device found ?
                    if device != None:

                        interface = task[3].strip()
                        volume    = task[4].strip()

                        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                        message = '{"interface":"' + interface + '","volume":' + str(volume) + '}'

                        heapq.heappush(mqtt_message_queue, (10, (channel, message)))            
                        CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, interface + '; ' + str(volume), 60)      

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | No Spotify Token found")


    except Exception as e:
        if "'NoneType' object is not subscriptable" not in str(e):
            WRITE_LOGFILE_SYSTEM("ERROR", "Task | " + source + " | " + str(error_informations) + " | " + str(e))