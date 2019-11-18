import threading
import time
import json
import heapq

from app import app
from app.database.models          import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import mqtt_message_queue
from app.backend.mqtt             import CHECK_MQTT_SETTING, CHECK_DEVICE_SETTING_PROCESS
from app.backend.email            import SEND_EMAIL


""" ############ """
""" pump control """
""" ############ """

def START_PUMP(plant_id):
    
    time.sleep(5)
    
    plant    = GET_PLANT_BY_ID(plant_id)
    ieeeAddr = plant.mqtt_device.ieeeAddr 
    msg      = '{"pump":"ON","pump_duration":' + str(plant.pump_duration) + '}'
        
    heapq.heappush(mqtt_message_queue, (50, ("watering", ieeeAddr, msg)))
    
    time.sleep(5)

    if CHECK_DEVICE_SETTING_PROCESS(ieeeAddr, msg, 10) == True:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Pump started")  
        return True

    else:           
        WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Pump starting not confimed")   
        return False

        
""" ##################### """
""" start watering thread """
""" ##################### """

def START_WATERING_THREAD(group_number):

    try:
        Thread = threading.Thread(target=WATERING_THREAD, args=(group_number, ))
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | Start Watering | Group - " + group_number + " | " + str(e)) 
        SEND_EMAIL("ERROR", "Thread | Start Watering | Group - " + group_number + " | " + str(e)) 


""" ############### """
""" watering thread """
""" ############### """

def WATERING_THREAD(group_number):
    pump_running = 0
    seconds      = 0 
    warnings     = []       
  

    # ##############
    # starting pumps
    # ##############
    
    # search plant
    for plant in GET_ALL_PLANTS():
        
        # valid group ?
        valid_group = False
        
        if group_number.isdigit():
            if plant.group == int(group_number):       
                valid_group = True
        
        if group_number == "all" or group_number == "ALL":
            valid_group = True
               
        
        # valid group founded
        if valid_group == True:
            
            # check watertank sensor
            if plant.control_sensor_watertank == "checked":
                
                sensor_values      = plant.mqtt_device.last_values
                sensor_values_json = json.loads(sensor_values)              
                current_watertank  = sensor_values_json["sensor_watertank"] 
                
                if current_watertank == 0:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Watertank Low")                    
                    warnings.append("Watertank Low")    
         
            if plant.pump_duration != "" and plant.pump_duration != None and plant.pump_duration != "None":

                # start watering
                WRITE_LOGFILE_SYSTEM("EVENT", "Watering | Plant - " + plant.name + " | Starting") 
                
                if START_PUMP(plant.id) != True:  
                    warnings.append("Pump starting not confimed")
                        
                pump_running = pump_running + 1

            else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Watering | Plant - " + plant.name + " | No Pump_Duration_Value founded")  
                
 
    # ####################
    # check pumps stopping
    # ####################
                    
    # check watering process
    while pump_running != 0 or seconds == 180:
        
        time.sleep(10)
    
        # search plant
        for plant in GET_ALL_PLANTS():
            
            # valid group ?
            valid_group = False
            
            if group_number.isdigit():
                if plant.group == int(group_number):               
                    valid_group = True
            
            if group_number == "all" or group_number == "ALL":
                valid_group = True
                
            
            # valid group founded
            if valid_group == True:

                # check pump stopped ?
                if CHECK_MQTT_SETTING(plant.mqtt_device.ieeeAddr , '"pump":"OFF"', 15):  
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Pump stopped")                              
                    pump_running = pump_running - 1

        seconds = seconds + 10
                      
                             
    # pump stopping not confirmed
    if pump_running > 0:
        
        WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Pump stopping not confimed")         
        warnings.append("Pump stopping not confimed")


    if warnings != []:
        WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Finished with Warning | " + str(warnings))
        SEND_EMAIL("WARNING", "Watering | Plant - " + plant.name + " | Finished with Warning | " + str(warnings))                      
    else:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Finished")    