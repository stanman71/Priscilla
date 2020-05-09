import paho.mqtt.client as mqtt
import heapq
import threading
import json
import datetime
import time

from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import *
from app.backend.shared_resources import *
from app.backend.email            import SEND_EMAIL

from ping3 import ping


""" ###################### """
"""  mqtt receive message  """
""" ###################### """
    
def START_MQTT_RECEIVE_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_RECEIVE_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Receive | " + str(e))  
        SEND_EMAIL("ERROR", "System | Thread | MQTT Receive | " + str(e))    

    
def MQTT_RECEIVE_THREAD():

    def on_connect(client, userdata, flags, rc):   
        if rc != 0:
            print("ERROR: Network | MQTT | Returned Code = " + str(rc)) 
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Returned Code = " + str(rc))         
        
            SET_MQTT_CONNECTION_STATUS(False)   
        
        else:
            client.subscribe("smarthome/#")
  
            print("Network | MQTT | connected") 
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | MQTT | connected")
            SET_MQTT_CONNECTION_STATUS(True)


    def on_message(client, userdata, message):     
        global mqtt_incoming_messages_list

        new_message = True
        ieeeAddr    = ""
        device_type = ""  

        channel     = message.topic                 
        msg         = str(message.payload.decode("utf-8"))       


        # ############################
        # get ieeeAddr and device_type
        # ############################

        device_identity = channel.split("/")[2]

        if device_identity not in ["bridge", "devices", "test", "log", "get", "set", "config", "update"]:
        
            list_devices = GET_ALL_DEVICES("")
        
            for device in list_devices:

                # mqtt device                       
                if device.ieeeAddr == device_identity:
                    ieeeAddr    = device_identity   
                    device_type = device.device_type            
                    break

                # zigbee2mqtt device
                if device.name == device_identity:                       
                    ieeeAddr    = device.ieeeAddr
                    device_type = device.device_type  
                    break


        # ################
        # message ignore ?
        # ################

        if (device_type == "led_rgb" or 
            device_type == "led_simple" or 
            device_type == "power_switch" or 
            device_type == "heater_thermostat" or    
            device_type == "blind" or      
            device_type == "sensor_passiv"):
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(3):              
                
                # search for other messages from the same device
                if existing_message[1] == channel:
                    
                    # device sends new data ?
                    
                    try:
                        existing_data = json.loads(existing_message[2])
                        new_data      = json.loads(msg)

                        # default case 
                        try:
                            if existing_data["state"] != new_data["state"]:
                                new_message = True
                                break
                                
                            else:
                                new_message = False

                        except:
                            pass

                        # special case IKEA blinds   
                        try:                     
                            if existing_data["position"] != new_data["position"]:
                                new_message = True
                                break
                                
                            else:
                                new_message = False

                        except:
                            pass
                                
                    except:
                        new_message = False     


        # ################
        # message ignore ?
        # ################

        if (device_type == "controller"):
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(2):              
                
                # search for other messages from the same device
                if existing_message[1] == channel:
                    
                    # controller sends new data ?

                    try:
                        existing_data = json.loads(existing_message[2])
                        new_data      = json.loads(msg)

                        # command "action"
                        try:
                            if existing_data["action"] != new_data["action"]:
                                new_message = True
                                break
                                
                            else:
                                new_message = False

                        except:
                            pass
                                
                        # command "click"
                        try:
                            if existing_data["click"] != new_data["click"]:
                                new_message = True
                                break
                                
                            else:
                                new_message = False       

                        except:
                            pass                 
                            
                    except:
                        new_message = False  


        # ###############
        # message passing
        # ###############
        
        if new_message:
            
            print("message topic: ", channel)       
            print("message received: ", msg)    
            
            WRITE_LOGFILE_DEVICES(channel, msg)
                
            # add message to the incoming message list
            mqtt_incoming_messages_list.append((str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), channel, msg))  
            

            # start message thread for additional processes
            if channel != "" and channel != None:   
                
                try:    
                    Thread = threading.Thread(target=MQTT_MESSAGE, args=(channel, msg, ieeeAddr, device_type,))
                    Thread.start()   
                except Exception as e:
                    WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Message | " + str(e)) 
                    SEND_EMAIL("ERROR", "System | Thread | MQTT Message | " + str(e))                    
                    print(e)


    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("localhost", 1883, 60)
        client.loop_forever()

    except Exception as e:
        print("ERROR: Network | MQTT | " + str(e)) 
        WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | " + str(e))        
        SET_MQTT_CONNECTION_STATUS(False)    


""" ############## """
"""  mqtt message  """
""" ############## """

def MQTT_MESSAGE(channel, msg, ieeeAddr, device_type):
  
    if channel == "smarthome/zigbee2mqtt/bridge/log":  
        data = json.loads(msg)
        

        # ################################
        # zigbee2mqtt pairing log messages
        # ################################

        if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "True":

            # new device connected
            if data["type"] == "pairing" and data["message"] == "interview_started":
                SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device found - " + data["meta"]["friendly_name"])   

            # device successful added
            if data["type"] == "pairing" and data["message"] == "interview_successful":
                time.sleep(5)
                UPDATE_DEVICES("zigbee2mqtt")
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + data["meta"]["friendly_name"] + " | added")   
                SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device added - " + data["meta"]["friendly_name"])   
                time.sleep(10)      
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 

            # device connection failed
            if data["type"] == "pairing" and data["message"] == "interview_failed":
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Device adding failed - " + data["meta"]["friendly_name"])   
                time.sleep(10)
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 
      

        # ##############
        # remove devices
        # ##############

        if data["type"] == "device_removed":
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + data["meta"]["friendly_name"] + " | deleted")

        if data["type"] == "device_force_removed":
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + data["message"] + " | deleted (force)")


        # #####################
        # zigbee device updates
        # #####################

        if data["type"] == "ota_update":
            SET_ZIGBEE_DEVICE_UPDATE_STATUS(data["message"])
            
            # update found

            if data["meta"]["status"] == "available":
                SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "True")
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

            # update started

            if data["meta"]["status"] == "update_in_progress":
                WRITE_LOGFILE_SYSTEM("EVENT", "Network | Device - " + data["meta"]["device"] + " | Device Update | started")

            # update success

            if data["meta"]["status"] == "update_succeeded":
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + data["meta"]["device"] + " | Device Update | " + str(data["message"]))
                time.sleep(10)
          
                SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "")

                # update update status
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("No Device Update available")

                for device in GET_ALL_DEVICES(""):
                    if device.update_available == "True":
                        SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

            # update failed
            
            if data["meta"]["status"] == "update_failed":
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + data["meta"]["device"] + " | Device Update | " + str(data["message"]))
                time.sleep(10)                

                # update update status
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("No Device Update available")

                for device in GET_ALL_DEVICES(""):
                    if device.update_available == "True":
                        SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

                # reset update variable
                SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "True")


    # #########################
    # start function networkmap
    # #########################

    if channel == "smarthome/zigbee2mqtt/bridge/networkmap/graphviz":

        # generate graphviz diagram
        from graphviz import Source, render

        src = Source(msg)
        src.render(filename = GET_PATH() + '/app/static/temp/zigbee_topology', format='png', cleanup=True)
        return


    # ############
    # mqtt updates
    # ############

    if channel == "smarthome/mqtt/update":

        try:
            data = json.loads(msg)

            if data["message"] == "success":
                device = GET_DEVICE_BY_IEEEADDR(data["device_ieeeAddr"])

                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + device.name + " | updated || Version || " + device.version + " >>> " + str(data["version"]))
                UPDATE_MQTT_DEVICE_VERSION(device.ieeeAddr, data["version"])

            else:
                device = GET_DEVICE_BY_IEEEADDR(data["device_ieeeAddr"])

                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + device.name + " || " + str(data["message"]))                

        except:
            pass


    # ################
    # device processes
    # ################

    if ieeeAddr != "":
        
        # save last values and last contact 
        SAVE_DEVICE_LAST_VALUES(ieeeAddr, msg)
        
        # check battery
        try:
            data = json.loads(msg)
            
            # special case eurotronic heater_thermostat
            if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "SPZB0001":
                if int(data["battery"]) < 5:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")
                    SEND_EMAIL("WARNING", "Network | Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")                    
                
            else:
                if int(data["battery"]) < 25:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")
                    SEND_EMAIL("WARNING", "Network | Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")             

        except:
            pass               


    if device_type == "sensor_passiv" or device_type == "sensor_active" or device_type == "heater_thermostat" or device_type == "watering_controller":
        
        # save sensor data of passive devices
        if FIND_SENSORDATA_JOB_INPUT(ieeeAddr) != "":
            list_jobs = FIND_SENSORDATA_JOB_INPUT(ieeeAddr)

            for job in list_jobs:   
                SAVE_SENSORDATA(job) 

        # start schedular job 
        for task in GET_ALL_SCHEDULER_TASKS():
            if task.trigger_sensors == "True" and task.option_pause != "True":
                heapq.heappush(process_management_queue, (10, ("scheduler", task.id, ieeeAddr)))


    # start controller job  
    if device_type == "controller":       
        heapq.heappush(process_management_queue, (1, ("controller", ieeeAddr, msg)))
            

""" ###################### """
"""  mqtt publish message  """
""" ###################### """

def START_MQTT_PUBLISH_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_PUBLISH_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Publish | " + str(e))  
        SEND_EMAIL("ERROR", "System | Thread | MQTT Publish | " + str(e))    


def MQTT_PUBLISH_THREAD():
    
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            print("ERROR: Network | MQTT | Returned Code = " + str(rc)) 
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Returned Code = " + str(rc))         
            SET_MQTT_CONNECTION_STATUS(False)   
        
        else:
            SET_MQTT_CONNECTION_STATUS(True)

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("localhost", 1883, 60)
        client.loop_start()
    
    except Exception as e:
        print("ERROR: Network | MQTT | " + str(e)) 
        WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | " + str(e))    
        SET_MQTT_CONNECTION_STATUS(False)        


    while True:
        try:  
            # check mqtt connection
            if GET_MQTT_CONNECTION_STATUS() == True:              
                mqtt_message = heapq.heappop(mqtt_message_queue)[1]      
                client.publish(mqtt_message[0],mqtt_message[1])        

        except Exception as e:         
            try:   
                if "index out of range" not in str(e):
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT Publish | " + str(e))  
                    SEND_EMAIL("ERROR", "Network | MQTT Publish | " + str(e))               
                    print(str(e))
                    
            except:
                print("ERROR: Network | MQTT")
                    
        time.sleep(0.1)


""" ##################### """
"""  mqtt control thread  """
""" ##################### """

def START_MQTT_CONTROL_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_CONTROL_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Publish | " + str(e))  
        SEND_EMAIL("ERROR", "System | Thread | MQTT Publish | " + str(e))    


def MQTT_CONTROL_THREAD():
    
    def on_connect(client, userdata, flags, rc):
        if rc != 0:    
            SET_MQTT_CONNECTION_STATUS(False)   
        
        else:
            SET_MQTT_CONNECTION_STATUS(True)

    while True:

        try:
            check_client = mqtt.Client()
            check_client.on_connect = on_connect
            check_client.connect("localhost", 1883, 60)
            check_client.disconnect()
    
        except Exception as e:
            SET_MQTT_CONNECTION_STATUS(False)        
                    
        time.sleep(10)


""" ################################ """
""" ################################ """
"""           mqtt functions         """
""" ################################ """
""" ################################ """


""" ################ """
"""  update devices  """
""" ################ """

def UPDATE_DEVICES(gateway):
   
    # ####
    # mqtt
    # ####

    if gateway == "mqtt":
        
        heapq.heappush(mqtt_message_queue, (20, ("smarthome/mqtt/devices", "")))
        time.sleep(10)

        try:
            for message in GET_MQTT_INCOMING_MESSAGES(15):
                
                if message[1] == "smarthome/mqtt/log":

                    message = str(message[2])
                   
                    data = json.loads(message)
                   
                    name             = data['ieeeAddr']
                    gateway          = "mqtt"
                    ieeeAddr         = data['ieeeAddr']
                    model            = data['model']

                    try:
                        device_type  = data['device_type']
                    except:
                        device_type  = ""                 

                    try:
                        version      = data['version']
                    except:
                        version      = ""  

                    try:
                        description  = data['description']
                    except:
                        description  = ""

                    try:
                        input_values  = data['input_values']
                        input_values  = ','.join(input_values)   
                        input_values  = input_values.replace("'", '"')
                    except:
                        input_values  = ""
                      
                    try:
                        input_events  = data['input_events']
                        input_events  = ','.join(input_events)
                        input_events  = input_events.replace("'", '"')                                         
                    except:
                        input_events  = ""
                        
                    try:
                        commands      = data['commands'] 
                        commands      = ','.join(commands)
                        commands      = commands.replace("'", '"')                             
                    except:
                        commands      = ""

                    try:
                        commands_json = data['commands_json'] 
                        commands_json = ','.join(commands_json)
                        commands_json = commands_json.replace("'", '"')                          
                    except:
                        commands_json = ""


                    # add new device

                    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):
                        ADD_DEVICE(name, gateway, ieeeAddr, model, device_type, version, description, input_values, input_events, commands, commands_json)
                      
                    # update existing device

                    else:
                        id   = GET_DEVICE_BY_IEEEADDR(ieeeAddr).id
                        name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
                                        
                        UPDATE_DEVICE(id, name, gateway, model, device_type, version, description, input_values, input_events, commands, commands_json)
                        SET_DEVICE_LAST_CONTACT(ieeeAddr)
                      
                    # update input values
    
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/mqtt/" + ieeeAddr + "/get", "")))
                    time.sleep(1)

            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | MQTT | Update")
            return True


        except Exception as e:
            if str(e) == "string index out of range":
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Update") 
                SEND_EMAIL("ERROR", "Network | MQTT | Update")                 
                return ("Network | MQTT | Update | " + str(e))     


    # ###########
    # zigbee2mqtt
    # ###########

    if gateway == "zigbee2mqtt":

        if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":
        
            error = ""
        
            heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/devices", "")))        
            time.sleep(5)
        
            try:

                for message in GET_MQTT_INCOMING_MESSAGES(10):
                        
                    if message[1] == "smarthome/zigbee2mqtt/bridge/log":

                        message = str(message[2])
                        message = message.replace("'","")

                        data = json.loads(message)  
                    
                        if (data['type']) == "devices":                       
                            devices = (data['message'])
                        
                            for i in range(0, len(devices)):                        
                                device = devices[i]
                                
                                try:

                                    # skip coordinator
                                    if device['type'] != "Coordinator":
                                        
                                        # add new device
                                
                                        if not GET_DEVICE_BY_IEEEADDR(device['ieeeAddr']):

                                            name     = device['friendly_name']
                                            gateway  = "zigbee2mqtt"              
                                            ieeeAddr = device['ieeeAddr']

                                            try:
                                                new_model  = device['model']
                                                new_device = GET_ZIGBEE_DEVICE_INFORMATIONS(new_model)
                                            except:
                                                new_model  = ""
                                                new_device = ["", "", "", "", "", ""]
                                                
                                            device_type   = new_device[0]
                                            version       = ""                                            
                                            description   = new_device[1]
                                            input_values  = new_device[2]
                                            input_events  = new_device[3]  
                                            commands      = new_device[4]                                
                                            commands_json = new_device[5] 

                                            ADD_DEVICE(name, gateway, ieeeAddr, new_model, device_type, version, description, input_values, input_events, commands, commands_json)


                                        # update device informations
                                    
                                        else:
                                    
                                            device_data = GET_DEVICE_BY_IEEEADDR(device['ieeeAddr'])

                                            id             = device_data.id         
                                            name           = device['friendly_name']
                                            existing_model = device['model']  
                                            gateway        = "zigbee2mqtt"

                                            try:                           
                                                existing_device = GET_ZIGBEE_DEVICE_INFORMATIONS(existing_model)
                                                
                                                device_type   = existing_device[0]
                                                version       = ""                                                
                                                description   = existing_device[1]                                            
                                                input_values  = existing_device[2]
                                                input_events  = existing_device[3]  
                                                commands      = existing_device[4]  
                                                commands_json = existing_device[5] 

                                            except Exception as e:
                                                device_type   = device_data.device_type
                                                version       = ""                                                
                                                description   = device_data.description                                             
                                                input_values  = device_data.input_values
                                                input_events  = device_data.input_events
                                                commands      = device_data.commands 
                                                commands_json = device_data.commands_json 
                                        
                                                error = "Error | " + str(existing_model) + " not found | " + str(e)
                                                                        
                                            UPDATE_DEVICE(id, name, gateway, existing_model, device_type, version, description, input_values, input_events, commands, commands_json)

                                except:
                                    pass

        
                if error != "":
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Update | " + str(error))
                    SEND_EMAIL("ERROR", "Network | ZigBee2MQTT | Update | " + str(error))                 
                    return ("Network | ZigBee2MQTT | Update | " + str(error)) 
                else:
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Update")

                    # update zigbee topology
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/networkmap", "graphviz")))
                    return True
     
     
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Update | " + str(e))  
                SEND_EMAIL("ERROR", "Network | ZigBee2MQTT | Update | " + str(e))             
                return ("Network | ZigBee2MQTT | Update " + str(e))

        else:
            return True


""" ###################### """
"""  check device setting  """
""" ###################### """
 
def CHECK_DEVICE_SETTING_THREAD(ieeeAddr, setting, seconds = 10): 
    repeats = seconds * 5
    Thread  = threading.Thread(target=CHECK_DEVICE_SETTING_PROCESS, args=(ieeeAddr, setting, repeats, ))
    Thread.start()   

 
def CHECK_DEVICE_SETTING_PROCESS(ieeeAddr, setting, repeats, log_report = True):                
    device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
    timer  = 1

    # special case roborock s50
    if device.model == "roborock_s50":
        if setting.lower() == "start":
            setting = "cleaning"
        if setting.lower() == "stop":
            setting = "idle"        
        if setting.lower() == "pause":
            setting = "paused"
        if setting.lower() == "return_to_base":
            setting = "returning"
        if setting.lower() == "locate":
            return True

    while timer < repeats:  
        
        if device.gateway == "mqtt":
            result = CHECK_MQTT_SETTING(device.ieeeAddr, setting)
        if device.gateway == "zigbee2mqtt":
            result = CHECK_ZIGBEE2MQTT_SETTING(device.name, setting)   

        # set previous setting
        if result == True:
            if log_report == True:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + device.name + " | Setting changed | " + setting)  

            return True

        timer = timer + 1
        time.sleep(0.2)       

    # error message
    if log_report == True:
        WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + device.name + " | Setting not confirmed | " + setting)  
        SEND_EMAIL("ERROR", "Network | Device - " + device.name + " | Setting not confirmed | " + setting)          
              
    return ("Device - " + device.name + " | Setting not confirmed - " + setting) 
                         

def CHECK_MQTT_SETTING(ieeeAddr, setting):     
    setting = setting.lower()
    
    for message in GET_MQTT_INCOMING_MESSAGES(5):

        # search for fitting message in incoming_messages_list
        if message[1] == "smarthome/mqtt/" + ieeeAddr or message[1] == "smarthome/mqtt/" + ieeeAddr + "/state":

            # only one setting value ("," = separator between commands || ";" = separator between command arguments)
            if not ";" in setting:    
                if str(setting.strip()) in str(message[2].lower()):
                    return True
                                                    
            # more then one setting value:
            else:
                
                list_settings = setting.split(";")
                
                for setting in list_settings:      
                    if not str(setting.strip()) in str(message[2].lower()):
                        return False    
                        
                return True
                
    return False
   

def CHECK_ZIGBEE2MQTT_SETTING(device_name, setting):
    setting = setting.lower()

    if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

        for message in GET_MQTT_INCOMING_MESSAGES(5):

            # search for fitting message in incoming_messages_list
            if message[1] == "smarthome/zigbee2mqtt/" + device_name:   

                # only one setting value ("," = separator between commands || ";" = separator between command arguments)
                if not ";" in setting:       
                    if str(setting.strip()) in str(message[2].lower()):
                        return True
                                    
                # more then one setting value:
                else:
                    
                    list_settings = setting.split(";")
                    
                    for setting in list_settings:        
                        if not str(setting.strip()) in str(message[2].lower()):
                            return False    
                            
                    return True                    
                
        return False

    else:
        return False


""" ################# """
"""  check functions  """
""" ################# """
 
def CHECK_ZIGBEE2MQTT_STARTED():    
    timer = 1

    # 10 seconds
    while timer < 50:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):          
            if message[1] == "smarthome/zigbee2mqtt/bridge/state":
            
                try:
                    if message[2] == "online":
                        SET_ZIGBEE2MQTT_CONNECTION_STATUS(True)
                        return True

                except:
                    pass

        timer = timer + 1
        time.sleep(0.2)

    SET_ZIGBEE2MQTT_CONNECTION_STATUS(False)     
    return False


def CHECK_ZIGBEE2MQTT_NAME_CHANGED(previous_name, new_name):   
    timer = 1

    # 10 seconds
    while timer < 50:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):      
            if message[1] == "smarthome/zigbee2mqtt/bridge/log":
            
                try:
                    data = json.loads(message[2])
                    
                    if data["type"] == "device_renamed" and data["message"]["from"] == previous_name and data["message"]["to"] == new_name:
                        return True

                except:
                    pass

        timer = timer + 1
        time.sleep(0.2)
                
    return False


def CHECK_ZIGBEE2MQTT_PAIRING(pairing_setting):    
    timer = 1

    # 10 seconds
    while timer < 50:       
        for message in GET_MQTT_INCOMING_MESSAGES(15):
            if message[1] == "smarthome/zigbee2mqtt/bridge/config":
            
                try:
                    data = json.loads(message[2])
                    
                    if pairing_setting == "True":
                        if data["permit_join"] == True:
                            return True

                    if pairing_setting == "False":
                        if data["permit_join"] == False:
                            return True

                except:
                    pass

        timer = timer + 1
        time.sleep(0.2)
                    
    return False


def CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):        
    timer = 1

    # 15 seconds
    while timer < 75:       
        for message in GET_MQTT_INCOMING_MESSAGES(15):
            if message[1] == "smarthome/zigbee2mqtt/bridge/log":
            
                try:
                    data = json.loads(message[2])
                    
                    if data["type"] == "device_removed" and data["message"] == device_name:
                        return True

                    if data["type"] == "device_force_removed" and data["message"] == device_name:
                        return True

                except:
                    pass

        timer = timer + 1
        time.sleep(0.2)
                    
    return False 


""" ######################### """
"""  check device exceptions  """
""" ######################### """


def CHECK_DEVICE_EXCEPTIONS(ieeeAddr, command):

    for exception in GET_ALL_DEVICE_EXCEPTIONS():

        if exception.device_ieeeAddr == ieeeAddr:

            try:
                                
                # ####################
                # exception ip_address 
                # ####################
                
                exception_command = exception.exception_command.strip()

                if exception.exception_option == "IP-Address" and exception_command.lower() == command.lower():

                    for x in range(3):
                        if ping(exception.exception_value_1, timeout=1) != None:    
                            return (exception.device.name + " | Device running")
                            break
            

                # ################
                # exception sensor
                # ################
                
                if exception.exception_sensor_ieeeAddr != "None" and exception_command.lower() == command.lower():
                    
                    sensor_ieeeAddr = exception.exception_sensor_ieeeAddr
                    sensor_key      = exception.exception_value_1   
                    operator        = exception.exception_value_2
                    value           = exception.exception_value_3

                    try:
                        value = str(value).lower()
                    except:
                        pass
                            
                    
                    # get sensordata 
                    data         = json.loads(GET_DEVICE_BY_IEEEADDR(exception.exception_sensor_ieeeAddr).last_values_json)
                    sensor_value = data[sensor_key]
                    
                    try:
                        sensor_value = str(sensor_value).lower()
                    except:
                        pass
                    
                        
                    # compare conditions
                    if operator == "=" and value.isdigit():
                        if int(sensor_value) == int(value):
                            return (exception.device.name + " | Sensor passing failed")   
                          
                    if operator == "=" and not value.isdigit():
                        if str(sensor_value) == str(value):
                            return (exception.device.name + " | Sensor passing failed")  
                            
                    if operator == "<" and value.isdigit():
                        if int(sensor_value) < int(value):
                            return (exception.device.name + " | Sensor passing failed")  
                            
                    if operator == ">" and value.isdigit():
                        if int(sensor_value) > int(value):
                            return (exception.device.name + " | Sensor passing failed")  
                        
            except Exception as e:
                return (exception.device.name + " | Error Exception Check || " + str(e))  

    return True


""" ############ """
"""  sensordata  """
""" ############ """

def REQUEST_SENSORDATA(job_name):
    sensordata_job  = GET_SENSORDATA_JOB_BY_NAME(job_name)
    device_gateway  = sensordata_job.device.gateway
    device_name     = sensordata_job.device.name  
    device_ieeeAddr = sensordata_job.device.ieeeAddr
    
    sensor_key = sensordata_job.sensor_key
    sensor_key = sensor_key.replace(" ", "")
 
    channel = "smarthome/" + device_gateway + "/" + device_ieeeAddr + "/get"
 
    heapq.heappush(mqtt_message_queue, (20, (channel, "")))        
    time.sleep(2) 
  
    for message in GET_MQTT_INCOMING_MESSAGES(5):
        
        if message[1] == "smarthome/" + device_gateway + "/" + device_ieeeAddr:
                
            try:

                data     = json.loads(message[2])
                filename = sensordata_job.filename
    
                WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Sensordata | Job - " + job_name + " | Data saved")  
                return True
                
            except:
                pass

    WRITE_LOGFILE_SYSTEM("ERROR", "Sensordata | Job - " + job_name + " | No Data found") 
    SEND_EMAIL("ERROR", "Sensordata | Job - " + job_name + " | No Data found")       

   
def SAVE_SENSORDATA(job_id):
    sensordata_job  = GET_SENSORDATA_JOB_BY_ID(job_id)
    device_gateway  = sensordata_job.device.gateway
    device_ieeeAddr = sensordata_job.device.ieeeAddr 
     
    sensor_key = sensordata_job.sensor_key
    sensor_key = sensor_key.replace(" ", "")
    
    for message in GET_MQTT_INCOMING_MESSAGES(10):
        
        if (message[1] == "smarthome/" + device_gateway + "/" + device_ieeeAddr):
                                
            try:
                data     = json.loads(message[2])
                filename = sensordata_job.filename
    
                WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                return True

            except:
                pass