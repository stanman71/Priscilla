import time
import threading
import json
import heapq

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import CHECK_DEVICE_SETTING_PROCESS
from app.backend.email            import SEND_EMAIL
from app.backend.shared_resources import mqtt_message_queue



def SET_LED_BULB_RGB(led_name, red, green, blue, global_brightness):

    brightness = int(global_brightness*2.55)

    channel = "miranda/zigbee2mqtt/" + led_name + "/set"
    msg     = '{"state":"ON","brightness":' + str(brightness) + ',"color": { "r":' + str(red) + ',"g":' + str(green)  + ',"b":' + str(blue) + '}}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    
    time.sleep(1)


def SET_LED_BULB_SIMPLE(led_name, global_brightness):

    brightness = int(global_brightness*2.55)

    channel = "miranda/zigbee2mqtt/" + led_name + "/set"
    msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    
    time.sleep(1)


def SET_LED_BULB_BRIGHTNESS(led_name, global_brightness):

    brightness = int(global_brightness*2.55)    
    
    channel = "miranda/zigbee2mqtt/" + led_name + "/set"
    msg     = '{"state": "ON","brightness":"' + str(brightness) + '"}'
    
    heapq.heappush(mqtt_message_queue, (5, (channel, msg))) 
    
    time.sleep(1)
    

def SET_LED_BULB_TURN_OFF(led_name):

    channel = "miranda/zigbee2mqtt/" + led_name + "/set"
    msg = '{"state": "OFF"}'
    
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
                                                             
    
def CHECK_LED_GROUP_SETTING(group_id, scene_id, setting, limit):
    
    error_list = []

    try:      
        group = GET_LED_GROUP_BY_ID(group_id)
        
        # group isn't offline
        if scene_id != 0:
            
            scene = GET_LED_SCENE_BY_ID(scene_id)

            # led 1
            led_1 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_1)

            if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_1, setting, 10) == False:
                error_list.append(led_1.name + " >>> Setting not confirmed")

            # led 2
            led_2 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_2)
            
            if group.active_led_2 == "True": 

                if scene.active_led_2 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_2, setting, 10) == False:
                        error_list.append(led_2.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_2, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_2.name + " >>> Setting not confirmed")

            # led 3
            led_3 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_3)
            
            if group.active_led_3 == "True": 

                if scene.active_led_3 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_3, setting, 10) == False:
                        error_list.append(led_3.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_3, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_3.name + " >>> Setting not confirmed")

            # led 4
            led_4 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_4)
            
            if group.active_led_4 == "True": 

                if scene.active_led_4 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_4, setting, 10) == False:
                        error_list.append(led_4.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_4, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_4.name + " >>> Setting not confirmed")

            # led 5
            led_5 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_5)
            
            if group.active_led_5 == "True": 

                if scene.active_led_5 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_5, setting, 10) == False:
                        error_list.append(led_5.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_5, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_5.name + " >>> Setting not confirmed")

            # led 6
            led_6 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_6)
            
            if group.active_led_6 == "True": 

                if scene.active_led_6 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_6, setting, 10) == False:
                        error_list.append(led_6.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_6, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_6.name + " >>> Setting not confirmed")

            # led 7
            led_7 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_7)
            
            if group.active_led_7 == "True": 

                if scene.active_led_7 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_7, setting, 10) == False:
                        error_list.append(led_7.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_7, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_7.name + " >>> Setting not confirmed")

            # led 8
            led_8 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_8)
            
            if group.active_led_8 == "True": 

                if scene.active_led_8 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_8, setting, 10) == False:
                        error_list.append(led_8.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_8, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_8.name + " >>> Setting not confirmed")

            # led 9
            led_9 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_9)
            
            if group.active_led_9 == "True": 

                if scene.active_led_9 == "True":
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_9, setting, 10) == False:
                        error_list.append(led_9.name + " >>> Setting not confirmed")
                                
                else:
                    if CHECK_DEVICE_SETTING_PROCESS(group.led_ieeeAddr_9, '{"state":"OFF"}', 10) == False:
                        error_list.append(led_9.name + " >>> Setting not confirmed")

        return error_list
            
    
    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Start Scene | " + setting + " | " + str(e))
        SEND_EMAIL("ERROR", "LED | Start Scene | " + setting + " | " + str(e))            
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

        if led_1.device_type == "led_rgb":
            SET_LED_BULB_RGB(led_1.name, scene.red_1, scene.green_1, scene.blue_1, int(brightness_global))                      
        if led_1.device_type == "led_simple":
            SET_LED_BULB_SIMPLE(led_1.name, int(brightness_global))   

        # led 2
        led_2 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_2)
        
        if group.active_led_2 == "True": 
            if scene.active_led_2 == "True":
            
                if led_2.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_2.name, scene.red_2, scene.green_2, scene.blue_2, int(brightness_global))                                                            
                if led_2.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_2.name, int(brightness_global))  
                    
            else:
                SET_LED_BULB_TURN_OFF(led_2.name)

        # led 3
        led_3 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_3)           
        
        if group.active_led_3 == "True": 
            if scene.active_led_3 == "True":

                if led_3.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_3.name, scene.red_3, scene.green_3, scene.blue_3, int(brightness_global))                                          
                if led_3.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_3.name, int(brightness_global))   

            else:
                SET_LED_BULB_TURN_OFF(led_3.name)
            
        # led 4
        led_4 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_4)            
        
        if group.active_led_4 == "True": 
            if scene.active_led_4 == "True":

                if led_4.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_4.name, scene.red_4, scene.green_4, scene.blue_4, int(brightness_global))                                        
                if led_4.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_4.name, int(brightness_global))  

            else:
                SET_LED_BULB_TURN_OFF(led_4.name)
            
        # led 5
        led_5 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_5)           
        
        if group.active_led_5 == "True": 
            if scene.active_led_5 == "True":

                if led_5.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_5.name, scene.red_5, scene.green_5, scene.blue_5, int(brightness_global))                                         
                if led_5.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_5.name, int(brightness_global))  
    
            else:
                SET_LED_BULB_TURN_OFF(led_5.name)
                                
        # led 6
        led_6 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_6)           
        
        if group.active_led_6 == "True": 
            if scene.active_led_6 == "True":

                if led_6.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_6.name, scene.red_6, scene.green_6, scene.blue_6, int(brightness_global))                                         
                if led_6.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_6.name, int(brightness_global))                       
    
            else:
                SET_LED_BULB_TURN_OFF(led_6.name)
                                
        # led 7
        led_7 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_7)            
        
        if group.active_led_7 == "True":       
            if scene.active_led_7 == "True":

                if led_7.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_7.name, scene.red_7, scene.green_7, scene.blue_7, int(brightness_global))                                          
                if led_7.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_7.name, int(brightness_global))    
        
            else:
                SET_LED_BULB_TURN_OFF(led_7.name)
                                
        # led 8
        led_8 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_8)           
        
        if group.active_led_8 == "True": 
            if scene.active_led_8 == "True":

                if led_8.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_8.name, scene.red_8, scene.green_8, scene.blue_8, int(brightness_global))                                        
                if led_8.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_8.name, int(brightness_global))   
    
            else:
                SET_LED_BULB_TURN_OFF(led_8.name)
                                
        # led 9
        led_9 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_9)           
        
        if group.active_led_9 == "True":   
            if scene.active_led_9 == "True":

                if led_9.device_type == "led_rgb":
                    SET_LED_BULB_RGB(led_9.name, scene.red_9, scene.green_9, scene.blue_9, int(brightness_global))                                          
                if led_9.device_type == "led_simple":
                    SET_LED_BULB_SIMPLE(led_9.name, int(brightness_global))                                           
    
            else:
                SET_LED_BULB_TURN_OFF(led_9.name)                       

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
        led_1        = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_1)
        
        SET_LED_BULB_BRIGHTNESS(led_1.name, int(brightness_global))
            
        # led 2
        if group.active_led_2 == "True":       
            led_2 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_2)   
            SET_LED_BULB_BRIGHTNESS(led_2.name, int(brightness_global))

        # led 3
        if group.active_led_3 == "True":      
            led_3 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_3)    
            SET_LED_BULB_BRIGHTNESS(led_3.name, int(brightness_global))

        # led 4
        if group.active_led_4 == "True":      
            led_4 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_4)
            SET_LED_BULB_BRIGHTNESS(led_4.name, int(brightness_global))

        # led 5
        if group.active_led_5 == "True":      
            led_5 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_5)
            SET_LED_BULB_BRIGHTNESS(led_5.name, int(brightness_global))

        # led 6
        if group.active_led_6 == "True":       
            led_6 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_6)
            SET_LED_BULB_BRIGHTNESS(led_6.name, int(brightness_global))

        # led 7
        if group.active_led_7 == "True":      
            led_7 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_7)
            SET_LED_BULB_BRIGHTNESS(led_7.name, int(brightness_global))

        # led 8
        if group.active_led_8 == "True":      
            led_8 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_8)
            SET_LED_BULB_BRIGHTNESS(led_8.name, int(brightness_global))

        # led 9
        if group.active_led_9 == "True":      
            led_9 = GET_DEVICE_BY_IEEEADDR(group.led_ieeeAddr_9)
            SET_LED_BULB_BRIGHTNESS(led_9.name, int(brightness_global))
            
        return True
    
    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Set Brightness | " + str(e))
        SEND_EMAIL("ERROR", "LED | Set Brightness | " + str(e))            
        return [str(e)]


def SET_LED_GROUP_TURN_OFF(group_id):

    try:
        group = GET_LED_GROUP_BY_ID(group_id)
        
        # led 1
        SET_LED_BULB_TURN_OFF(group.led_name_1)
            
        # led 2
        if group.active_led_2 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_2)
        # led 3
        if group.active_led_3 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_3)
        # led 4
        if group.active_led_4 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_4)
        # led 5
        if group.active_led_5 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_5)
        # led 6
        if group.active_led_6 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_6)
        # led 7
        if group.active_led_7 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_7)
        # led 8
        if group.active_led_8 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_8)
        # led 9
        if group.active_led_9 == "True": 
            SET_LED_BULB_TURN_OFF(group.led_name_9)
        
        return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | Turn_off | " + str(e))
        SEND_EMAIL("ERROR", "LED | Turn_off | " + str(e))            
        return [str(e)]
