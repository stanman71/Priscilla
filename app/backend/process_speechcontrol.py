import spotipy
import re
import json

from app                          import app
from app.database.models          import *
from app.backend.led              import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.process_program  import START_PROGRAM_THREAD, STOP_PROGRAM_THREAD, GET_PROGRAM_RUNNING
from app.backend.spotify          import *
from app.backend.shared_resources import mqtt_message_queue

from difflib import SequenceMatcher


def SPEECHCONTROL_TASKS(message):

    data = json.loads(message)


    """

    # ###########
    # start scene 
    # ###########

    if CHECK_SPEECHCONTROL_ANSWER(answer, keywords) == True:

        try:
            groups = GET_ALL_LED_GROUPS()
            scenes = GET_ALL_LED_SCENES() 

            group_id   = None
            scene_id   = None
            brightness = 100

            # search group
            for group in groups:
                for word in answer_words:

                    if SequenceMatcher(None, group.name.lower(), word.lower()).ratio() > ratio_value:
                        group_id = group.id
                        continue

            # search scene
            for scene in scenes:
                for word in answer_words:
                    
                    if SequenceMatcher(None, scene.name.lower(), word.lower()).ratio() > ratio_value:
                        scene_id = scene.id
                        continue

            # search brightness value
            for element in answer.split():
                element = element.replace("%","")

                # check brightness as 'number' value
                if element.isdigit() and (1 <= int(element) <= 100):
                    brightness = int(element)
                    continue

                # check brightness as 'word' value
                try:
                    brightness = int(table_numbers[element])
                    continue
                except:
                    pass  


            # group founded ?
            if group_id != None: 

                # scene founded ?
                if scene_id != None:   
                    group = GET_LED_GROUP_BY_ID(group_id)
                    scene = GET_LED_SCENE_BY_ID(scene_id) 

                    # new led setting ?
                    if group.current_setting != scene.name or int(group.current_brightness) != brightness:
                        SET_LED_GROUP_SCENE(group.id, scene.id, brightness)
                        CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 3, 15)     
                        time.sleep(1)
                        return                               

                    else:
                        WRITE_LOGFILE_SYSTEM("STATUS", "LED | Group - " + group.name + " | " + scene.name + " : " + str(brightness) + " %")     
                        return

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | Scene not founded")
                    return

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | Group not founded")
                return


        except Exception as e:
            print(e)
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | " + str(e))  
            return


    # ##############
    # set brightness
    # ##############

    keywords = GET_SPEECHCONTROL_LED_TASK_BY_ID(2).keywords

    if CHECK_SPEECHCONTROL_ANSWER(answer, keywords) == True:
                
        try:        
            groups = GET_ALL_LED_GROUPS()

            group_id   = None
            brightness = None

            # search group
            for group in groups:
                for word in answer_words:

                    if SequenceMatcher(None, group.name.lower(), word.lower()).ratio() > ratio_value:
                        group_id = group.id
                        continue

            # search brightness value
            for element in answer.split():
                element = element.replace("%","")

                # check brightness as 'number' value
                if element.isdigit() and (1 <= int(element) <= 100):
                    brightness = int(element)
                    continue

                # check brightness as 'word' value
                try:
                    brightness = int(table_numbers[element])
                    continue
                except:
                    pass                    
            
            # group founded ?
            if group_id != None: 

                # brightness value founded ?
                if brightness != None:  
                    group = GET_LED_GROUP_BY_ID(group_id)

                    # led_group off ?
                    if group.current_setting != "OFF":
                        scene_name = group.current_setting
                        scene      = GET_LED_SCENE_BY_NAME(scene_name)                            

                        # new led brightness setting ?
                        if group.current_brightness != brightness:
                            
                            SET_LED_GROUP_BRIGHTNESS(group.id, brightness)
                            CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene_name, brightness, 3, 15)  
                            time.sleep(1)
                            return                                       

                        else:
                            WRITE_LOGFILE_SYSTEM("STATUS", "LED | Group - " + group.name + " | " + scene_name + " : " + str(brightness) + " %") 
                            return  

                    else:
                        WRITE_LOGFILE_SYSTEM("WARNING", "LED | Group - " + group.name + " | OFF : 0 %") 
                        return                                     

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | Brightness value not founded")
                    return
                    
            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | Group not founded")
                return

        except Exception as e:
            print(e)
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | " + str(e))    
            return


    # ##################
    # turn off led group
    # ##################

    keywords = GET_SPEECHCONTROL_LED_TASK_BY_ID(3).keywords

    if CHECK_SPEECHCONTROL_ANSWER(answer, keywords) == True:

        try:
            groups = GET_ALL_LED_GROUPS()
            
            founded_groups = []

            # search group
            for group in groups:
                for word in answer_words:

                    if SequenceMatcher(None, group.name.lower(), word.lower()).ratio() > ratio_value:
                        founded_groups.append(group)        


            # group founded
            if founded_groups != []:

                for group in founded_groups:
                    scene_name = group.current_setting
                    scene      = GET_LED_SCENE_BY_NAME(scene_name)

                    # new led setting ?
                    if group.current_setting != "OFF":
                        SET_LED_GROUP_TURN_OFF(group.id)
                        CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 3, 15)  
                        time.sleep(1)
                        return                                       

                    else:
                        WRITE_LOGFILE_SYSTEM("STATUS", "LED | Group - " + group.name + " | OFF : 0 %")  
                        return                       

            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | No Group founded")
                return                        


        except Exception as e:
            print(e)
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | " + str(e))    
            return


    # #################
    # turn off all leds
    # #################

    keywords = GET_SPEECHCONTROL_LED_TASK_BY_ID(4).keywords

    if CHECK_SPEECHCONTROL_ANSWER(answer, keywords) == True:
        
        try:
            # check all led groups
            for group in GET_ALL_LED_GROUPS():
                scene_name = group.current_setting
                scene      = GET_LED_SCENE_BY_NAME(scene_name)

                # new led setting ?
                if group.current_setting != "OFF":
                    SET_LED_GROUP_TURN_OFF(group.id)
                    CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 3, 15)   
                    time.sleep(1)
                    return                              

                else:
                    WRITE_LOGFILE_SYSTEM("STATUS", "LED | Group - " + group.name + " | OFF : 0 %") 
                    return

        except Exception as e:
            print(e)
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | LED Task | " + answer + " | " + str(e))    
            return



    # ######
    # device 
    # ######        

    for task in GET_ALL_SPEECHCONTROL_DEVICE_TASKS():

        if CHECK_SPEECHCONTROL_ANSWER(answer, task.keywords) == True:
        
            try:
                device = GET_DEVICE_BY_IEEEADDR(task.device_ieeeAddr)

                # device founded ?
                if device != None:
                    speechcontrol_setting_formated = task.setting
                    
                    # check device exception
                    check_result = CHECK_DEVICE_EXCEPTIONS(device.id, speechcontrol_setting_formated)
                    
                   
                    if check_result == True:    
                    
                        # convert string to json-format
                        speechcontrol_setting = speechcontrol_setting_formated.replace(' ', '')
                        speechcontrol_setting = speechcontrol_setting.replace(':', '":"')
                        speechcontrol_setting = speechcontrol_setting.replace(',', '","')
                        speechcontrol_setting = '{"' + str(speechcontrol_setting) + '"}'        

                        # new device setting ?  
                        new_setting = False
                        
                        if not "," in speechcontrol_setting:
                            if not speechcontrol_setting[1:-1] in device.last_values:
                                new_setting = True
                                                                        
                        # more then one setting value:
                        else:   
                            speechcontrol_setting_temp = speechcontrol_setting[1:-1]
                            list_speechcontrol_setting = speechcontrol_setting_temp.split(",")
                            
                            for setting in list_speechcontrol_setting:
                                
                                if not setting in device.last_values:
                                    new_setting = True  


                        if new_setting == True:

                            if device.gateway == "mqtt":
                                channel = "miranda/mqtt/" + device.ieeeAddr + "/set"  
                            if device.gateway == "zigbee2mqtt":   
                                channel = "miranda/zigbee2mqtt/" + device.name + "/set"          

                            msg = speechcontrol_setting

                            heapq.heappush(mqtt_message_queue, (10, (channel, msg)))            
                            CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, speechcontrol_setting, 20)  

                        else:
                            WRITE_LOGFILE_SYSTEM("STATUS", "Devices | Device - " + device.name + " | " + speechcontrol_setting_formated) 

                    else:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Speechcontrol | Device Task | " + answer + " | " + check_result)                     

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Device Task | " + answer + " | Device not founded")
                    return                             


            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Device Task | " + answer + " | " + str(e))      
                return                    



    # #######
    # program 
    # #######                

    for task in GET_ALL_SPEECHCONTROL_PROGRAM_TASKS():

        if CHECK_SPEECHCONTROL_ANSWER(answer, task.keywords) == True:
                    
            try:
                program = GET_PROGRAM_BY_ID(task.program_id)

                # program founded ?
                if program != None:
                    command = task.command.lower()
                    command = command.replace(" ", "")

                    program_running = GET_PROGRAM_RUNNING() 

                    if command == "start" and program_running == None:
                        START_PROGRAM_THREAD(program.id)
                        return
                        
                    elif command == "start" and program_running != None:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Speechcontrol | Program Task | " + answer + " | Other Program running")    
                        return  
                                    
                    elif command == "stop":
                        STOP_PROGRAM_THREAD() 
                        return
                        
                    else:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Program Task | " + answer + " | Command not valid")
                        return

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Program Task | " + answer + " | Program not founded")    
                    return       

            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Program Task | " + answer + " | " + str(e))   
                return 
  

    # ##############
    # start playlist 
    # ##############

    keywords = GET_SPEECHCONTROL_SPOTIFY_TASK_BY_ID(1).keywords

    if CHECK_SPEECHCONTROL_ANSWER(answer, keywords) == True:    
        spotify_token = GET_SPOTIFY_TOKEN()
                
        if spotify_token != "": 

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False              

            try:
                list_spotify_devices   = sp.devices()["devices"] 
                list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]

                spotify_device_id    = None
                spotify_playlist_uri = None
                playlist_volume      = 50

                # search spotify device
                for device in list_spotify_devices:
                    for word in answer_words:

                        if SequenceMatcher(None, device["name"].lower(), word.lower()).ratio() > ratio_value:
                            spotify_device_id = device["id"]
                            continue

                # search playlist
                for playlist in list_spotify_playlists:
                    for word in answer_words:
                        
                        if SequenceMatcher(None, playlist["name"].lower(), word.lower()).ratio() > ratio_value:
                            spotify_playlist_uri = playlist["uri"]
                            continue

                # search volume value
                for element in answer.split():
                    element = element.replace("%","")

                    # check brightness as 'number' value
                    if element.isdigit() and (1 <= int(element) <= 100):
                        volume = int(element)
                        continue

                    # check volume as 'word' value
                    try:
                        playlist_volume = int(table_numbers[element])
                        continue
                    except:
                        pass  
    

                # device founded ?
                if spotify_device_id != None: 

                    # playlist founded ?
                    if spotify_playlist_uri != None:   
                                                        
                        SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, spotify_playlist_uri, playlist_volume)
                        
                    else:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | " + answer + " | Playlist not founded")
                        return

                else:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | " + answer + " | Device not founded") 
                    return   
                        
                        
            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | " + answer + " | " + str(e))   
                return                       


        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | " + answer + " | No Spotify Token founded")   
            return   

    """


    # ####
    # play  
    # ####

    if "music_play" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "": 

            sp       = spotipy.Spotify(auth=spotify_token)
            sp.trace = False      
            
            try: 

                # start current playlist and device
                spotify_device_id = sp.current_playback(market=None)['device']['id']
                spotify_volume    = sp.current_playback(market=None)['device']['volume_percent']

                SPOTIFY_CONTROL(spotify_token, "play", spotify_volume) 
                sp.shuffle(True, device_id=spotify_device_id)

            except Exception as e:

                # start default playlist and device
                for device in sp.devices()["devices"]:  

                    if "multiroom" in device["name"]:
                        spotify_device_id = device["id"]
               
                        SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, "spotify:user:stanman71:playlist:4Qg6xrKdd3WJEEkvkEZrQd", "33")
                        sp.shuffle(True, device_id=spotify_device_id)   
                        break           

      
        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Play | No Spotify Token founded")   
            return   
                    
                    
    # ########
    # previous  
    # ########

    if "music_previous" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "": 

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False      
            spotify_volume = sp.current_playback(market=None)['device']['volume_percent']    

            try:
                SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)
                time.sleep(1)
                SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)       
                                                    
            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Previous | " + str(e))   
                return                       

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Previous | No Spotify Token founded")   
            return   
            
                    
    # ####
    # next  
    # ####

    if "music_next" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()  

        if spotify_token != "": 

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False      
            spotify_volume = sp.current_playback(market=None)['device']['volume_percent']       

            try:
                SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)
                                                                       
            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Next | " + str(e))   
                return                       

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Next | No Spotify Token founded")   
            return   
            
                    
    # ####
    # stop  
    # ####
   
    if "music_stop" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "": 

            sp             = spotipy.Spotify(auth=spotify_token)
            sp.trace       = False      
            spotify_volume = sp.current_playback(market=None)['device']['volume_percent']       

            try:
                SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)
                                                                          
            except Exception as e:
                print(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Stop | " + str(e))   
                return                       

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Stop | No Spotify Token founded")   
            return                                          

    # ######
    # volume  
    # ######

    if "music_volume_up" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "": 

            sp          = spotipy.Spotify(auth=spotify_token)
            sp.trace    = False      
            device_name = sp.current_playback(market=None)['device']['name']

            # spotify

            if "multiroom" not in device_name:
                spotify_volume = sp.current_playback(market=None)['device']['volume_percent']       

                if spotify_volume != 100:

                    volume = spotify_volume + 10

                    if volume > 100:
                        volume = 100

                    try:                 
                        SPOTIFY_CONTROL(spotify_token, "volume", volume)                        
                                                            
                    except Exception as e:
                        print(e)
                        WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Volume_Up | " + str(e))   
                        return       

            else:
                list_devices = device_name.split(", ")
                list_devices = list_devices.split(" & ")




        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Volume_Up | No Spotify Token founded")   
            return   


    if "music_volume_down" in data["intent"]["intentName"]:

        spotify_token = GET_SPOTIFY_TOKEN()
        
        if spotify_token != "": 

            sp          = spotipy.Spotify(auth=spotify_token)
            sp.trace    = False      
            device_name = sp.current_playback(market=None)['device']['name']

            if "multiroom" not in device_name:
                spotify_volume = sp.current_playback(market=None)['device']['volume_percent']       

                if spotify_volume != 0:

                    volume = spotify_volume - 10

                    if volume < 0:
                        volume = 0

                    try:                 
                        SPOTIFY_CONTROL(spotify_token, "volume", volume)
                                                                                    
                    except Exception as e:
                        print(e)
                        WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Volume_Down | " + str(e))   
                        return                       

        else:
            WRITE_LOGFILE_SYSTEM("ERROR", "Speechcontrol | Spotify Task | Volume_Down | No Spotify Token founded")   
            return   