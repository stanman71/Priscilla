import time
import threading
import json
import heapq

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.email            import SEND_EMAIL
from app.backend.shared_resources import mqtt_message_queue



def SET_LIGHT_RGB(light_ieeeAddr, red, green, blue, brightness):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)
    
    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'
    
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'    
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg)))  
    time.sleep(1)


def SET_LIGHT_SIMPLE(light_ieeeAddr, brightness):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
        
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)


def SET_LIGHT_BRIGHTNESS(light_ieeeAddr, brightness):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"    
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    

def SET_LIGHT_TURN_OFF(light_ieeeAddr):
    device = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg = '{"state": "OFF","brightness":0}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"     
        msg = '{"state": "OFF","brightness":0}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    
    
    
""" ############################ """
""" lighting group check setting """
""" ############################ """


def CHECK_LIGHTING_GROUP_SETTING_THREAD(group_id, scene_id, scene, brightness, delay, limit): 
 
    Thread = threading.Thread(target=CHECK_LIGHTING_GROUP_SETTING_PROCESS, args=(group_id, scene_id, scene, brightness, delay, limit, ))
    Thread.start()   

 
def CHECK_LIGHTING_GROUP_SETTING_PROCESS(group_id, scene_id, scene, brightness, delay, limit): 
               
    if scene == "OFF":
        setting = "OFF"
    else:
        setting = "ON"
                    
    # check setting 1 try
    time.sleep(delay)                             
    result = CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, setting, limit)
    
    # set current state
    if result == []:
        SET_LIGHTING_GROUP_CURRENT_SCENE(group_id, scene)
        SET_LIGHTING_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)   
        
    else:
        # check setting 2 try
        time.sleep(delay)                             
        result = CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, setting, limit)
        
        # set current state 
        if result == []:
            SET_LIGHTING_GROUP_CURRENT_SCENE(group_id, scene)
            SET_LIGHTING_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)  
        
        else:
            # check setting 3 try
            time.sleep(delay)                             
            result = CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, setting, limit) 
     
              
    # output
    SET_LIGHTING_GROUP_CURRENT_SCENE(group_id, scene)
    SET_LIGHTING_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)                
                
    group_name = GET_LIGHTING_GROUP_BY_ID(group_id).name
                
    if result == []:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Lighting | Group - " + group_name + " | Setting changed | " + str(scene) + " : "  + str(brightness) + " %") 
    else:
        WRITE_LOGFILE_SYSTEM("WARNING", "Lighting | Group - " + group_name + " | "  + str(scene) + " : "  + str(brightness) + " | " + str(result)) 
        SEND_EMAIL("WARNING", "Lighting | Group - " + group_name + " | "  + str(scene) + " : "  + str(brightness) + " | " + str(result)) 

    return result     
                                                             
    
def CHECK_LIGHTING_GROUP_SETTING(group_id, scene_id, setting_json, limit):
    
    error_list = []

    try:      
        group = GET_LIGHTING_GROUP_BY_ID(group_id)
        
        # group isn't offline
        if scene_id != 0:
            
            scene = GET_LIGHTING_SCENE_BY_ID(scene_id)

            # light 1
            light_1 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_1)

            if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_1, setting_json, 10) == False:
                error_list.append(light_1.name + " >>> Setting not confirmed")

            # light 2
            light_2 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_2)
            
            if group.active_light_2 == "True": 

                if scene.active_light_2 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_2, setting_json, 10) == False:
                        error_list.append(light_2.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_2, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_2.name + " >>> Setting not confirmed")

            # light 3
            light_3 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_3)
            
            if group.active_light_3 == "True": 

                if scene.active_light_3 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_3, setting_json, 10) == False:
                        error_list.append(light_3.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_3, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_3.name + " >>> Setting not confirmed")

            # light 4
            light_4 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_4)
            
            if group.active_light_4 == "True": 

                if scene.active_light_4 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_4, setting_json, 10) == False:
                        error_list.append(light_4.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_4, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_4.name + " >>> Setting not confirmed")

            # light 5
            light_5 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_5)
            
            if group.active_light_5 == "True": 

                if scene.active_light_5 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_5, setting_json, 10) == False:
                        error_list.append(light_5.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_5, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_5.name + " >>> Setting not confirmed")

            # light 6
            light_6 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_6)
            
            if group.active_light_6 == "True": 

                if scene.active_light_6 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_6, setting_json, 10) == False:
                        error_list.append(light_6.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_6, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_6.name + " >>> Setting not confirmed")

            # light 7
            light_7 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_7)
            
            if group.active_light_7 == "True": 

                if scene.active_light_7 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_7, setting_json, 10) == False:
                        error_list.append(light_7.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_7, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_7.name + " >>> Setting not confirmed")

            # light 8
            light_8 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_8)
            
            if group.active_light_8 == "True": 

                if scene.active_light_8 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_8, setting_json, 10) == False:
                        error_list.append(light_8.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_8, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_8.name + " >>> Setting not confirmed")

            # light 9
            light_9 = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_9)
            
            if group.active_light_9 == "True": 

                if scene.active_light_9 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_9, setting_json, 10) == False:
                        error_list.append(light_9.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.light_ieeeAddr_9, '{"state":"OFF"}', 10) == False:
                        error_list.append(light_9.name + " >>> Setting not confirmed")

        return error_list
            
    
    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Start Scene | " + str(e))
        SEND_EMAIL("ERROR", "Lighting | Start Scene | " + str(e))            
        return [str(e)]
    
        
    else:
        return ["MQTT ist nicht verfügbar"]
    


""" ######################### """
"""  lighting group functions """
""" ######################### """


def SET_LIGHTING_GROUP_SCENE(group_id, scene_id, brightness_global = 100):

    try:      
        group = GET_LIGHTING_GROUP_BY_ID(group_id)
        scene = GET_LIGHTING_SCENE_BY_ID(scene_id)
    
        # light 1
        light_1        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_1)        
        brightness_1 = scene.brightness_1*(brightness_global/100)

        if light_1.device_type == "led_rgb":
            SET_LIGHT_RGB(group.light_ieeeAddr_1, scene.red_1, scene.green_1, scene.blue_1, int(brightness_1))                      
        if light_1.device_type == "led_simple":
            SET_LIGHT_SIMPLE(group.light_ieeeAddr_1, int(brightness_global))   

        # light 2
        light_2        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_2)           
        brightness_2 = scene.brightness_2*(brightness_global/100)        
        
        if group.active_light_2 == "True": 
            if scene.active_light_2 == "True":
            
                if light_2.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_2, scene.red_2, scene.green_2, scene.blue_2, int(brightness_2))                                                            
                if light_2.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_2, int(brightness_global))  
                    
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_2)

        # light 3  
        light_3        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_3)           
        brightness_3 = scene.brightness_3*(brightness_global/100)                
        
        if group.active_light_3 == "True": 
            if scene.active_light_3 == "True":

                if light_3.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_3, scene.red_3, scene.green_3, scene.blue_3, int(brightness_3))                                          
                if light_3.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_3, int(brightness_global))   

            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_3)
            
        # light 4
        light_4        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_4)           
        brightness_4 = scene.brightness_4*(brightness_global/100)                
        
        if group.active_light_4 == "True": 
            if scene.active_light_4 == "True":

                if light_4.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_4, scene.red_4, scene.green_4, scene.blue_4, int(brightness_4))                                        
                if light_4.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_4, int(brightness_global))  

            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_4)
            
        # light 5 
        light_5        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_5)           
        brightness_5 = scene.brightness_5*(brightness_global/100)               
        
        if group.active_light_5 == "True": 
            if scene.active_light_5 == "True":

                if light_5.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_5, scene.red_5, scene.green_5, scene.blue_5, int(brightness_5))                                         
                if light_5.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_5, int(brightness_global))  
    
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_5)
                                
        # light 6    
        light_6        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_6)   
        brightness_6 = scene.brightness_6*(brightness_global/100)           
        
        if group.active_light_6 == "True": 
            if scene.active_light_6 == "True":

                if light_6.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_6, scene.red_6, scene.green_6, scene.blue_6, int(brightness_6))                                         
                if light_6.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_6, int(brightness_global))                       
    
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_6)
                                
        # light 7
        light_7        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_7)          
        brightness_7 = scene.brightness_7*(brightness_global/100)                 
        
        if group.active_light_7 == "True":       
            if scene.active_light_7 == "True":

                if light_7.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_7, scene.red_7, scene.green_7, scene.blue_7, int(brightness_7))                                          
                if light_7.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_7, int(brightness_global))    
        
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_7)
                                
        # light 8 
        light_8        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_8)           
        brightness_8 = scene.brightness_8*(brightness_global/100)                
        
        if group.active_light_8 == "True": 
            if scene.active_light_8 == "True":

                if light_8.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_8, scene.red_8, scene.green_8, scene.blue_8, int(brightness_8))                                        
                if light_8.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_8, int(brightness_global))   
    
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_8)
                                
        # light 9  
        light_9        = GET_DEVICE_BY_IEEEADDR(group.light_ieeeAddr_9)           
        brightness_9 = scene.brightness_9*(brightness_global/100)              
        
        if group.active_light_9 == "True":   
            if scene.active_light_9 == "True":

                if light_9.device_type == "led_rgb":
                    SET_LIGHT_RGB(group.light_ieeeAddr_9, scene.red_9, scene.green_9, scene.blue_9, int(brightness_9))                                          
                if light_9.device_type == "led_simple":
                    SET_LIGHT_SIMPLE(group.light_ieeeAddr_9, int(brightness_global))                                           
    
            else:
                SET_LIGHT_TURN_OFF(group.light_ieeeAddr_9)                       

        return True

    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Start Scene | " + str(e))            
        SEND_EMAIL("ERROR", "Lighting | Start Scene | " + str(e))
        return [str(e)]
    


def SET_LIGHTING_GROUP_BRIGHTNESS_DIMMER(group_id, command):
    
    group              = GET_LIGHTING_GROUP_BY_ID(group_id)
    current_brightness = group.current_brightness
    
    if command == "turn_up":
        target_brightness = int(current_brightness) + 20
        
        if target_brightness > 100:
            target_brightness = 100
    
    if command == "turn_down":
        target_brightness = int(current_brightness) - 20
        
        if target_brightness < 0:
            target_brightness = 0    
             
    SET_LIGHTING_GROUP_BRIGHTNESS(group.id, target_brightness)
    
    

def SET_LIGHTING_GROUP_BRIGHTNESS(group_id, brightness_global = 100):
    
    try:
        group      = GET_LIGHTING_GROUP_BY_ID(group_id)
        scene_name = GET_LIGHTING_GROUP_BY_ID(group_id).current_scene
        scene      = GET_LIGHTING_SCENE_BY_NAME(scene_name)
        
        # light 1
        brightness_1 = scene.brightness_1*(brightness_global/100)
        
        SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_1, int(brightness_1))
            
        # light 2
        if group.active_light_2 == "True":         
            brightness_2 = scene.brightness_2*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_2, int(brightness_2))

        # light 3
        if group.active_light_3 == "True":       
            brightness_3 = scene.brightness_3*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_3, int(brightness_3))

        # light 4
        if group.active_light_4 == "True":      
            brightness_4 = scene.brightness_4*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_4, int(brightness_4))

        # light 5
        if group.active_light_5 == "True":      
            brightness_5 = scene.brightness_5*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_5, int(brightness_5))

        # light 6
        if group.active_light_6 == "True":       
            brightness_6 = scene.brightness_6*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_6, int(brightness_6))

        # light 7
        if group.active_light_7 == "True":      
            brightness_7 = scene.brightness_7*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_7, int(brightness_7))

        # light 8
        if group.active_light_8 == "True":      
            brightness_8 = scene.brightness_8*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_8, int(brightness_8))

        # light 9
        if group.active_light_9 == "True":      
            brightness_9 = scene.brightness_9*(brightness_global/100)

            SET_LIGHT_BRIGHTNESS(group.light_ieeeAddr_9, int(brightness_9))
            
        return True
    
    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Set Brightness | " + str(e))
        SEND_EMAIL("ERROR", "Lighting | Set Brightness | " + str(e))            
        return [str(e)]


def SET_LIGHTING_GROUP_TURN_OFF(group_id):

    try:
        group = GET_LIGHTING_GROUP_BY_ID(group_id)
        
        # light 1
        SET_LIGHT_TURN_OFF(group.light_ieeeAddr_1)
            
        # light 2
        if group.active_light_2 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_2)
        # light 3
        if group.active_light_3 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_3)
        # light 4
        if group.active_light_4 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_4)
        # light 5
        if group.active_light_5 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_5)
        # light 6
        if group.active_light_6 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_6)
        # light 7
        if group.active_light_7 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_7)
        # light 8
        if group.active_light_8 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_8)
        # light 9
        if group.active_light_9 == "True": 
            SET_LIGHT_TURN_OFF(group.light_ieeeAddr_9)
        
        return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Lighting | Turn_off | " + str(e))
        SEND_EMAIL("ERROR", "Lighting | Turn_off | " + str(e))            
        return [str(e)]
