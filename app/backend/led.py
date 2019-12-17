import time
import threading
import json
import heapq

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.email            import SEND_EMAIL
from app.backend.shared_resources import mqtt_message_queue



def SET_LED_RGB(led_ieeeAddr, red, green, blue, brightness):
    device = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr)
    
    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'
    
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'    
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg)))  
    time.sleep(1)


def SET_LED_SIMPLE(led_ieeeAddr, brightness):
    device = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
        
    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)


def SET_LED_BRIGHTNESS(led_ieeeAddr, brightness):
    device = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"    
        msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    

def SET_LED_TURN_OFF(led_ieeeAddr):
    device = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr)

    if device.gateway == "mqtt":
        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"
        msg = '{"state": "OFF","brightness":0}'

    if device.gateway == "zigbee2mqtt":
        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"     
        msg = '{"state": "OFF","brightness":0}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    time.sleep(1)
    
    
    
""" ####################### """
""" led group check setting """
""" ####################### """


def CHECK_LED_GROUP_SETTING_THREAD(group_id, scene_id, scene, brightness, delay, limit): 
 
    Thread = threading.Thread(target=CHECK_LED_GROUP_SETTING_PROCESS, args=(group_id, scene_id, scene, brightness, delay, limit, ))
    Thread.start()   

 
def CHECK_LED_GROUP_SETTING_PROCESS(group_id, scene_id, scene, brightness, delay, limit): 
               
    if scene == "OFF":
        setting = '{"state":"OFF"}'
    else:
        setting = '{"state":"ON"}'
                    
    # check setting 1 try
    time.sleep(delay)                             
    result = CHECK_LED_GROUP_SETTING(group_id, scene_id, setting, limit)
    
    # set current state
    if result == []:
        SET_LED_GROUP_CURRENT_SETTING(group_id, scene)
        SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)   
        
    else:
        # check setting 2 try
        time.sleep(delay)                             
        result = CHECK_LED_GROUP_SETTING(group_id, scene_id, setting, limit)
        
        # set current state 
        if result == []:
            SET_LED_GROUP_CURRENT_SETTING(group_id, scene)
            SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)  
        
        else:
            # check setting 3 try
            time.sleep(delay)                             
            result = CHECK_LED_GROUP_SETTING(group_id, scene_id, setting, limit) 
     
              
    # output
    SET_LED_GROUP_CURRENT_SETTING(group_id, scene)
    SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness)                
                
    group_name = GET_LED_GROUP_BY_ID(group_id).name
                
    if result == []:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "LED | Group - " + group_name + " | Setting changed | " + str(scene) + " : "  + str(brightness) + " %") 
    else:
        WRITE_LOGFILE_SYSTEM("WARNING", "LED | Group - " + group_name + " | "  + str(scene) + " : "  + str(brightness) + " | " + str(result)) 
        SEND_EMAIL("WARNING", "LED | Group - " + group_name + " | "  + str(scene) + " : "  + str(brightness) + " | " + str(result)) 

    return result     
                                                             
    
def CHECK_LED_GROUP_SETTING(group_id, scene_id, setting_json, limit):
    
    error_list = []

    try:      
        group = GET_LED_GROUP_BY_ID(group_id)
        
        # group isn't offline
        if scene_id != 0:
            
            scene = GET_LED_SCENE_BY_ID(scene_id)

            # led 1
            led_1 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_1)

            if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_1, setting_json, 10) == False:
                error_list.append(led_1.name + " >>> Setting not confirmed")

            # led 2
            led_2 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_2)
            
            if group.active_led_2 == "True": 

                if scene.active_led_2 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_2, setting_json, 10) == False:
                        error_list.append(led_2.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_2, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_2.name + " >>> Setting not confirmed")

            # led 3
            led_3 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_3)
            
            if group.active_led_3 == "True": 

                if scene.active_led_3 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_3, setting_json, 10) == False:
                        error_list.append(led_3.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_3, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_3.name + " >>> Setting not confirmed")

            # led 4
            led_4 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_4)
            
            if group.active_led_4 == "True": 

                if scene.active_led_4 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_4, setting_json, 10) == False:
                        error_list.append(led_4.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_4, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_4.name + " >>> Setting not confirmed")

            # led 5
            led_5 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_5)
            
            if group.active_led_5 == "True": 

                if scene.active_led_5 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_5, setting_json, 10) == False:
                        error_list.append(led_5.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_5, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_5.name + " >>> Setting not confirmed")

            # led 6
            led_6 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_6)
            
            if group.active_led_6 == "True": 

                if scene.active_led_6 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_6, setting_json, 10) == False:
                        error_list.append(led_6.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_6, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_6.name + " >>> Setting not confirmed")

            # led 7
            led_7 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_7)
            
            if group.active_led_7 == "True": 

                if scene.active_led_7 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_7, setting_json, 10) == False:
                        error_list.append(led_7.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_7, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_7.name + " >>> Setting not confirmed")

            # led 8
            led_8 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_8)
            
            if group.active_led_8 == "True": 

                if scene.active_led_8 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_8, setting_json, 10) == False:
                        error_list.append(led_8.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_8, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_8.name + " >>> Setting not confirmed")

            # led 9
            led_9 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_9)
            
            if group.active_led_9 == "True": 

                if scene.active_led_9 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_9, setting_json, 10) == False:
                        error_list.append(led_9.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_9, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_9.name + " >>> Setting not confirmed")

        return error_list
            
    
    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Start Scene | " + str(e))
        SEND_EMAIL("ERROR", "LED | Start Scene | " + str(e))            
        return [str(e)]
    
        
    else:
        return ["Keine LED-Steuerung aktiviert"]
    


""" ##################### """
"""  led group functions """
""" ##################### """


def SET_LED_GROUP_SCENE(group_id, scene_id, brightness_global = 100):

    try:      
        group = GET_LED_GROUP_BY_ID(group_id)
        scene = GET_LED_SCENE_BY_ID(scene_id)
    
        # led 1
        led_1        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_1)        
        brightness_1 = scene.brightness_1*(brightness_global/100)

        if led_1.device_type == "led_rgb":
            SET_LED_RGB(group.led_ieeeAddr_1, scene.red_1, scene.green_1, scene.blue_1, int(brightness_1))                      
        if led_1.device_type == "led_simple":
            SET_LED_SIMPLE(group.led_ieeeAddr_1, int(brightness_global))   

        # led 2
        led_2        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_2)           
        brightness_2 = scene.brightness_2*(brightness_global/100)        
        
        if group.active_led_2 == "True": 
            if scene.active_led_2 == "True":
            
                if led_2.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_2, scene.red_2, scene.green_2, scene.blue_2, int(brightness_2))                                                            
                if led_2.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_2, int(brightness_global))  
                    
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_2)

        # led 3  
        led_3        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_3)           
        brightness_3 = scene.brightness_3*(brightness_global/100)                
        
        if group.active_led_3 == "True": 
            if scene.active_led_3 == "True":

                if led_3.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_3, scene.red_3, scene.green_3, scene.blue_3, int(brightness_3))                                          
                if led_3.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_3, int(brightness_global))   

            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_3)
            
        # led 4
        led_4        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_4)           
        brightness_4 = scene.brightness_4*(brightness_global/100)                
        
        if group.active_led_4 == "True": 
            if scene.active_led_4 == "True":

                if led_4.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_4, scene.red_4, scene.green_4, scene.blue_4, int(brightness_4))                                        
                if led_4.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_4, int(brightness_global))  

            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_4)
            
        # led 5 
        led_5        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_5)           
        brightness_5 = scene.brightness_5*(brightness_global/100)               
        
        if group.active_led_5 == "True": 
            if scene.active_led_5 == "True":

                if led_5.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_5, scene.red_5, scene.green_5, scene.blue_5, int(brightness_5))                                         
                if led_5.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_5, int(brightness_global))  
    
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_5)
                                
        # led 6    
        led_6        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_6)   
        brightness_6 = scene.brightness_6*(brightness_global/100)           
        
        if group.active_led_6 == "True": 
            if scene.active_led_6 == "True":

                if led_6.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_6, scene.red_6, scene.green_6, scene.blue_6, int(brightness_6))                                         
                if led_6.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_6, int(brightness_global))                       
    
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_6)
                                
        # led 7
        led_7        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_7)          
        brightness_7 = scene.brightness_7*(brightness_global/100)                 
        
        if group.active_led_7 == "True":       
            if scene.active_led_7 == "True":

                if led_7.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_7, scene.red_7, scene.green_7, scene.blue_7, int(brightness_7))                                          
                if led_7.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_7, int(brightness_global))    
        
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_7)
                                
        # led 8 
        led_8        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_8)           
        brightness_8 = scene.brightness_8*(brightness_global/100)                
        
        if group.active_led_8 == "True": 
            if scene.active_led_8 == "True":

                if led_8.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_8, scene.red_8, scene.green_8, scene.blue_8, int(brightness_8))                                        
                if led_8.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_8, int(brightness_global))   
    
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_8)
                                
        # led 9  
        led_9        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_9)           
        brightness_9 = scene.brightness_9*(brightness_global/100)              
        
        if group.active_led_9 == "True":   
            if scene.active_led_9 == "True":

                if led_9.device_type == "led_rgb":
                    SET_LED_RGB(group.led_ieeeAddr_9, scene.red_9, scene.green_9, scene.blue_9, int(brightness_9))                                          
                if led_9.device_type == "led_simple":
                    SET_LED_SIMPLE(group.led_ieeeAddr_9, int(brightness_global))                                           
    
            else:
                SET_LED_TURN_OFF(group.led_ieeeAddr_9)                       

        return True

    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Start Scene | " + str(e))            
        SEND_EMAIL("ERROR", "LED | Start Scene | " + str(e))
        return [str(e)]
    


def SET_LED_GROUP_BRIGHTNESS_DIMMER(group_id, command):
    
    group              = GET_LED_GROUP_BY_ID(group_id)
    current_brightness = group.current_brightness
    
    if command == "turn_up":
        target_brightness = int(current_brightness) + 20
        
        if target_brightness > 100:
            target_brightness = 100
    
    if command == "turn_down":
        target_brightness = int(current_brightness) - 20
        
        if target_brightness < 0:
            target_brightness = 0    
             
    SET_LED_GROUP_BRIGHTNESS(group.id, target_brightness)
    
    

def SET_LED_GROUP_BRIGHTNESS(group_id, brightness_global = 100):
    
    try:
        group      = GET_LED_GROUP_BY_ID(group_id)
        scene_name = GET_LED_GROUP_BY_ID(group_id).current_setting
        scene      = GET_LED_SCENE_BY_NAME(scene_name)
        
        # led 1
        brightness_1 = scene.brightness_1*(brightness_global/100)
        
        SET_LED_BRIGHTNESS(group.led_ieeeAddr_1, int(brightness_1))
            
        # led 2
        if group.active_led_2 == "True":         
            brightness_2 = scene.brightness_2*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_2, int(brightness_2))

        # led 3
        if group.active_led_3 == "True":       
            brightness_3 = scene.brightness_3*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_3, int(brightness_3))

        # led 4
        if group.active_led_4 == "True":      
            brightness_4 = scene.brightness_4*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_4, int(brightness_4))

        # led 5
        if group.active_led_5 == "True":      
            brightness_5 = scene.brightness_5*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_5, int(brightness_5))

        # led 6
        if group.active_led_6 == "True":       
            brightness_6 = scene.brightness_6*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_6, int(brightness_6))

        # led 7
        if group.active_led_7 == "True":      
            brightness_7 = scene.brightness_7*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_7, int(brightness_7))

        # led 8
        if group.active_led_8 == "True":      
            brightness_8 = scene.brightness_8*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_8, int(brightness_8))

        # led 9
        if group.active_led_9 == "True":      
            brightness_9 = scene.brightness_9*(brightness_global/100)

            SET_LED_BRIGHTNESS(group.led_ieeeAddr_9, int(brightness_9))
            
        return True
    
    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Set Brightness | " + str(e))
        SEND_EMAIL("ERROR", "LED | Set Brightness | " + str(e))            
        return [str(e)]


def SET_LED_GROUP_TURN_OFF(group_id):

    try:
        group = GET_LED_GROUP_BY_ID(group_id)
        
        # led 1
        SET_LED_TURN_OFF(group.led_ieeeAddr_1)
            
        # led 2
        if group.active_led_2 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_2)
        # led 3
        if group.active_led_3 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_3)
        # led 4
        if group.active_led_4 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_4)
        # led 5
        if group.active_led_5 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_5)
        # led 6
        if group.active_led_6 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_6)
        # led 7
        if group.active_led_7 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_7)
        # led 8
        if group.active_led_8 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_8)
        # led 9
        if group.active_led_9 == "True": 
            SET_LED_TURN_OFF(group.led_ieeeAddr_9)
        
        return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Turn_off | " + str(e))
        SEND_EMAIL("ERROR", "LED | Turn_off | " + str(e))            
        return [str(e)]
