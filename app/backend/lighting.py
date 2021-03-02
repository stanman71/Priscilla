from app                          import app
from app.backend.database_models  import *
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.shared_resources import mqtt_message_queue, GET_MQTT_CONNECTION_STATUS
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM

import time
import threading
import json
import heapq


""" ################## """
"""  lighting threads  """
""" ################## """


def SET_LIGHT_RGB_THREAD(light_ieeeAddr, red, green, blue, brightness):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)
    
    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'
    
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'    
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg)))  
    time.sleep(1)


def SET_LIGHT_SIMPLE_THREAD(light_ieeeAddr, brightness):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
        
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)


def SET_LIGHT_BRIGHTNESS_THREAD(light_ieeeAddr, brightness, red, green, blue):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'    
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    

def SET_LIGHT_TURN_OFF_THREAD(light_ieeeAddr):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg = '{"state": "OFF","brightness":0}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"     
        msg = '{"state": "OFF","brightness":0}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    

""" ########################## """
"""  lighting group functions  """
""" ########################## """


def SET_LIGHTING_GROUP_SCENE(group_id, scene_id, brightness_global = 100):

    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:  

        try:     
            
            group = GET_LIGHTING_GROUP_BY_ID(group_id)
            scene = GET_LIGHTING_SCENE_BY_ID(scene_id)

            # light 1
            light_1      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_1)        
            brightness_1 = scene.brightness_1*(brightness_global/100)

            if light_1.device_type == "led_rgb":              
                Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_1, scene.red_1, scene.green_1, scene.blue_1, int(brightness_1), ))
                Thread.start()                      
            if light_1.device_type == "led_simple":
                Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_1, int(brightness_global), ))
                Thread.start()   

            # light 2   
            if group.active_light_2 == "True": 
                if scene.active_light_2 == "True":

                    light_2      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_2)           
                    brightness_2 = scene.brightness_2*(brightness_global/100)          

                    if light_2.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_2, scene.red_2, scene.green_2, scene.blue_2, int(brightness_2), ))
                        Thread.start()                      
                    if light_2.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_2, int(brightness_global), ))
                        Thread.start()   
                        
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_2, ))
                    Thread.start()      

            # light 3       
            if group.active_light_3 == "True": 
                if scene.active_light_3 == "True":

                    light_3      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_3)           
                    brightness_3 = scene.brightness_3*(brightness_global/100)      

                    if light_3.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_3, scene.red_3, scene.green_3, scene.blue_3, int(brightness_3), ))
                        Thread.start()                      
                    if light_3.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_3, int(brightness_global), ))
                        Thread.start()   

                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_3, ))
                    Thread.start()      
                
            # light 4
            if group.active_light_4 == "True": 
                if scene.active_light_4 == "True":

                    light_4      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_4)           
                    brightness_4 = scene.brightness_4*(brightness_global/100)      

                    if light_4.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_4, scene.red_4, scene.green_4, scene.blue_4, int(brightness_4), ))
                        Thread.start()                      
                    if light_4.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_4, int(brightness_global), ))
                        Thread.start()   

                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_4, ))
                    Thread.start()      
                
            # light 5 
            if group.active_light_5 == "True": 
                if scene.active_light_5 == "True":

                    light_5      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_5)           
                    brightness_5 = scene.brightness_5*(brightness_global/100)      

                    if light_5.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_5, scene.red_5, scene.green_5, scene.blue_5, int(brightness_5), ))
                        Thread.start()                      
                    if light_5.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_5, int(brightness_global), ))
                        Thread.start()   
        
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_5, ))
                    Thread.start()      
                                    
            # light 6    
            if group.active_light_6 == "True": 
                if scene.active_light_6 == "True":

                    light_6      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_6)           
                    brightness_6 = scene.brightness_6*(brightness_global/100)      

                    if light_6.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_6, scene.red_6, scene.green_6, scene.blue_6, int(brightness_6), ))
                        Thread.start()                      
                    if light_6.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_6, int(brightness_global), ))
                        Thread.start()                     
        
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_6, ))
                    Thread.start()      
                                    
            # light 7
            if group.active_light_7 == "True":       
                if scene.active_light_7 == "True":

                    light_7      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_7)           
                    brightness_7 = scene.brightness_7*(brightness_global/100)      

                    if light_7.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_7, scene.red_7, scene.green_7, scene.blue_7, int(brightness_7), ))
                        Thread.start()                      
                    if light_7.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_7, int(brightness_global), ))
                        Thread.start()    
            
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_7, ))
                    Thread.start()      
                                    
            # light 8 
            if group.active_light_8 == "True": 
                if scene.active_light_8 == "True":

                    light_8      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_8)           
                    brightness_8 = scene.brightness_8*(brightness_global/100)      

                    if light_8.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_8, scene.red_8, scene.green_8, scene.blue_8, int(brightness_8), ))
                        Thread.start()                      
                    if light_8.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_8, int(brightness_global), ))
                        Thread.start()   
        
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_8, ))
                    Thread.start()      
                                    
            # light 9  
            if group.active_light_9 == "True":   
                if scene.active_light_9 == "True":

                    light_9      = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_9)           
                    brightness_9 = scene.brightness_9*(brightness_global/100)      

                    if light_9.device_type == "led_rgb":
                        Thread = threading.Thread(target=SET_LIGHT_RGB_THREAD, args=(group.light_ieeeAddr_9, scene.red_9, scene.green_9, scene.blue_9, int(brightness_9), ))
                        Thread.start()                      
                    if light_9.device_type == "led_simple":
                        Thread = threading.Thread(target=SET_LIGHT_SIMPLE_THREAD, args=(group.light_ieeeAddr_9, int(brightness_global), ))
                        Thread.start()                                            
        
                else:
                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_9, ))
                    Thread.start()        
                
            return True
    
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Start scene | " + str(e))            
            return [str(e)]
    
    else:
        return ["MQTT is not avilable"]


def SET_LIGHTING_GROUP_BRIGHTNESS_DIMMER(group_id, command):

    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:    

        group              = GET_LIGHTING_GROUP_BY_ID(group_id)
        current_brightness = group.current_brightness
        
        if command == "turn_up":
            target_brightness = int(current_brightness) + 20
            
            if target_brightness > 100:
                target_brightness = 100
        
        if command == "turn_down":
            target_brightness = int(current_brightness) - 20
            
            if target_brightness < 10:
                target_brightness = 10    
                
        SET_LIGHTING_GROUP_BRIGHTNESS(group.id, target_brightness)

    else:
        return ["MQTT is not avilable"]    


def SET_LIGHTING_GROUP_BRIGHTNESS(group_id, brightness_global = 100):
    
    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:  

        try:
            group      = GET_LIGHTING_GROUP_BY_ID(group_id)
            scene_name = GET_LIGHTING_GROUP_BY_ID(group_id).current_scene
            scene      = GET_LIGHTING_SCENE_BY_NAME(scene_name)
            
            # light 1
            brightness_1 = scene.brightness_1*(brightness_global/100)

            Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_1, int(brightness_1), scene.red_1, scene.green_1, scene.blue_1, ))
            Thread.start()     
    
            # light 2
            if group.active_light_2 == "True":         
                brightness_2 = scene.brightness_2*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_2, int(brightness_2), scene.red_2, scene.green_2, scene.blue_2, ))
                Thread.start()     

            # light 3
            if group.active_light_3 == "True":       
                brightness_3 = scene.brightness_3*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_3, int(brightness_3), scene.red_3, scene.green_3, scene.blue_3, ))
                Thread.start()     

            # light 4
            if group.active_light_4 == "True":      
                brightness_4 = scene.brightness_4*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_4, int(brightness_4), scene.red_4, scene.green_4, scene.blue_4, ))
                Thread.start()     

            # light 5
            if group.active_light_5 == "True":      
                brightness_5 = scene.brightness_5*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_5, int(brightness_5), scene.red_5, scene.green_5, scene.blue_5, ))
                Thread.start()     

            # light 6
            if group.active_light_6 == "True":       
                brightness_6 = scene.brightness_6*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_6, int(brightness_6), scene.red_6, scene.green_6, scene.blue_6, ))
                Thread.start()     

            # light 7
            if group.active_light_7 == "True":      
                brightness_7 = scene.brightness_7*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_7, int(brightness_7), scene.red_7, scene.green_7, scene.blue_7, ))
                Thread.start()     

            # light 8
            if group.active_light_8 == "True":      
                brightness_8 = scene.brightness_8*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_8, int(brightness_8), scene.red_8, scene.green_8, scene.blue_8, ))
                Thread.start()     

            # light 9
            if group.active_light_9 == "True":      
                brightness_9 = scene.brightness_9*(brightness_global/100)

                Thread = threading.Thread(target=SET_LIGHT_BRIGHTNESS_THREAD, args=(group.light_ieeeAddr_9, int(brightness_9), scene.red_9, scene.green_9, scene.blue_9, ))
                Thread.start()     
                
            return True
        
        
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Set brightness | " + str(e))           
            return [str(e)]


    else:
        return ["MQTT is not avilable"]


def SET_LIGHTING_GROUP_TURN_OFF(group_id):

    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:  

        try:
            group = GET_LIGHTING_GROUP_BY_ID(group_id)
            
            # light 1
            Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_1, ))
            Thread.start()     
            
            # light 2
            if group.active_light_2 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_2, ))
                Thread.start()     
            # light 3
            if group.active_light_3 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_3, ))
                Thread.start()    
            # light 4
            if group.active_light_4 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_4, ))
                Thread.start()    
            # light 5
            if group.active_light_5 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_5, ))
                Thread.start()    
            # light 6
            if group.active_light_6 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_6, ))
                Thread.start()    
            # light 7
            if group.active_light_7 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_7, ))
                Thread.start()    
            # light 8
            if group.active_light_8 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_8, ))
                Thread.start()    
            # light 9
            if group.active_light_9 == "True": 
                Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(group.light_ieeeAddr_9, ))
                Thread.start()    
            
            return True

        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Turn_off | " + str(e))         
            return [str(e)]

    else:
        return ["MQTT is not avilable"]


""" ############################## """
"""  lighting group check setting  """
""" ############################## """


def CHECK_LIGHTING_GROUP_SETTING_THREAD(group_id, scene_id, scene, brightness, delay, limit): 
 
    Thread = threading.Thread(target=CHECK_LIGHTING_GROUP_SETTING_PROCESS, args=(group_id, scene_id, scene, brightness, delay, limit, ))
    Thread.start()   

 
def CHECK_LIGHTING_GROUP_SETTING_PROCESS(group_id, scene_id, scene_name, brightness, delay, limit): 

    # update program settings
    SET_LIGHTING_GROUP_CURRENT_SCENE(group_id, scene_name)
    SET_LIGHTING_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)      

    # check setting 
    time.sleep(delay)                             
    result = CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, limit)

    group_name = GET_LIGHTING_GROUP_BY_ID(group_id).name
                
    if result == []:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Lighting | Group | " + group_name + " | Setting changed | " + str(scene_name) + " : "  + str(brightness) + " %") 
    else:
        device_errors = ""

        for element in result:
            device_errors = device_errors + ", " + element

        WRITE_LOGFILE_SYSTEM("WARNING", "Lighting | Group | " + group_name + " | "  + str(scene_name) + " : "  + str(brightness) + " | Setting not confirmed | " + device_errors[2:])

    return result     
                                                             
    
def CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, limit):

    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:  

        error_list = []

        try:      
            group = GET_LIGHTING_GROUP_BY_ID(group_id)

            # light 1
            light_1 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_1)

            # get setting for LED 1
            if scene_id != 0:
                if GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_1 != 0:
                    setting = "ON"
                else:
                    setting = "OFF"
            else:
                setting = "OFF"

            if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_1, setting, 10, False) != True:
                error_list.append(light_1.name)

            # light 2
            light_2 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_2)
            
            if group.active_light_2 == "True": 

                # get setting for LED 2
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_2 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_2 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_2, setting, 10, False) != True:
                    error_list.append(light_2.name)
                                
            # light 3
            light_3 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_3)
            
            if group.active_light_3 == "True": 

                # get setting for LED 3
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_3 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_3 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_3, setting, 10, False) != True:
                    error_list.append(light_3.name)

            # light 4
            light_4 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_4)
            
            if group.active_light_4 == "True": 

                # get setting for LED 4
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_4 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_4 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_4, setting, 10, False) != True:
                    error_list.append(light_4.name)

            # light 5
            light_5 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_5)
            
            if group.active_light_5 == "True": 

                # get setting for LED 5
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_5 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_5 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_5, setting, 10, False) != True:
                    error_list.append(light_5.name)

            # light 6
            light_6 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_6)
            
            if group.active_light_6 == "True": 

                # get setting for LED 6
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_6 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_6 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_6, setting, 10, False) != True:
                    error_list.append(light_6.name)

            # light 7
            light_7 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_7)
            
            if group.active_light_7 == "True": 

                # get setting for LED 7
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_7 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_7 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_7, setting, 10, False) != True:
                    error_list.append(light_7.name)

            # light 8
            light_8 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_8)
            
            if group.active_light_8 == "True": 

                # get setting for LED 8
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_8 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_8 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_8, setting, 10, False) != True:
                    error_list.append(light_8.name)

            # light 9
            light_9 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_9)
            
            if group.active_light_9 == "True": 

                # get setting for LED 9
                if scene_id != 0:
                    if GET_LIGHTING_SCENE_BY_ID(scene_id).active_light_9 == "True" and GET_LIGHTING_SCENE_BY_ID(scene_id).brightness_9 != 0:
                        setting = "ON"
                    else:
                        setting = "OFF"
                else:
                    setting = "OFF"

                if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_9, setting, 10, False) != True:
                    error_list.append(light_9.name)

            return error_list
                
        
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Start scene | " + str(e))        
            return [str(e)]

    else:
        return ["MQTT is not avilable"]