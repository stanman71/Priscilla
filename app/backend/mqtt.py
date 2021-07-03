from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import *
from app.backend.shared_resources import *
from app.backend.email            import SEND_EMAIL

from ping3       import ping
from ruamel.yaml import YAML
from pathlib     import Path

import paho.mqtt.client as mqtt
import heapq
import threading
import json
import datetime
import time
import os


""" ################################## """
"""  block battery low messages timer  """
""" ################################## """

list_battery_low_devices_blocked = []

def START_TIMER_BLOCK_BATTERY_LOW_DEVICES_THREAD(device):
	try:
		Thread = threading.Thread(target=TIMER_BLOCK_BATTERY_LOW_DEVICES_THREAD, args=(device, ))
		Thread.start()  

	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Timer Block 'Battery Low' Devices | " + str(e)) 


def TIMER_BLOCK_BATTERY_LOW_DEVICES_THREAD(device): 
    time.sleep(86400)  # 24h
    list_battery_low_devices_blocked.remove(device)


""" ########################## """
""" ########################## """
"""     messenger functions    """
""" ########################## """
""" ########################## """


""" ###################### """
"""  mqtt receive message  """
""" ###################### """
    
def START_MQTT_RECEIVE_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_RECEIVE_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Receive | " + str(e))  
  

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
            SEND_EMAIL("SYSTEM", "Network | MQTT | connected")
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

        if ("bridge" not in channel and
            "devices" not in channel and
            "test" not in channel and
            "log" not in channel and
            "get" not in channel and
            "set" not in channel and
            "config" not in channel and
            "update" not in channel and
            "command" not in channel):

            device_identity = channel.split("/")[2]

            for device in GET_ALL_DEVICES(""):

                # mqtt device                       
                if device.ieeeAddr == device_identity:
                    ieeeAddr    = device.ieeeAddr   
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

        if device_type != "":

            new_message = True
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(3):              
                
                # search for other messages from the same device
                if existing_message[1] == channel and existing_message[2] == msg:
                    new_message = False  
                    break


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
        

        # ##################
        # zigbee add devices
        # ##################

        if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "True":

            # new device connected
            if data["type"] == "pairing" and data["message"] == "interview_started":
                SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device found | " + data["meta"]["friendly_name"])   

            # device successful added
            if data["type"] == "pairing" and data["message"] == "interview_successful":

                try:

                    ieeeAddr = data["meta"]["friendly_name"]      
                    model    = data["meta"]["model"]               

                    # add new device
            
                    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):

                        new_device    = GET_ZIGBEE_DEVICE_INFORMATIONS(model)
                            
                        device_type   = new_device[0]
                        version       = ""                                            
                        description   = new_device[1]
                        input_values  = new_device[2]
                        input_trigger = new_device[3]  
                        commands      = new_device[4]                                
                        commands_json = new_device[5] 

                        ADD_DEVICE(ieeeAddr, "zigbee2mqtt", ieeeAddr, model, device_type, version, description, input_values, input_trigger, commands, commands_json)

                        SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device added | " + data["meta"]["friendly_name"]) 
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + data["meta"]["friendly_name"] + " | added")    
                        SET_ZIGBEE2MQTT_PAIRING_STATUS("Device added")  

                        # add device config for IKEA SYMFONISK sound controller and IKEA TRADFRI wireless dimmer
                        if model == "E1744" or model == "ICTC-G-1":
           
                            try:

                                yaml = YAML()
                                path = Path('/opt/zigbee2mqtt/data/configuration.yaml')

                                data   = yaml.load(path)
                                device = data['devices'][ieeeAddr]

                                device['debounce']        = 1
                                device['debounce_ignore'] = ['action']
                                yaml.dump(data, path)

                                os.system("sudo systemctl restart zigbee2mqtt")    

                            except Exception as e:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + data["meta"]["friendly_name"] + " | " + str(e))

                        time.sleep(10) 


                except Exception as e:
                    if "UNIQUE constraint failed" not in str(e):
                        WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + data["meta"]["friendly_name"] + " | " + str(e))
                        SET_ZIGBEE2MQTT_PAIRING_STATUS("Error: " + str(e))  
                    else:
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + data["meta"]["friendly_name"] + " | Device was already in database")  
                        SET_ZIGBEE2MQTT_PAIRING_STATUS("Device was already in database")  

                    time.sleep(10)


                SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 

            # device connection failed
            if data["type"] == "pairing" and data["message"] == "interview_failed":
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + data["meta"]["friendly_name"] + " | adding failed")
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Device adding failed | " + data["meta"]["friendly_name"])   
                time.sleep(10)
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 
      

        # #####################
        # zigbee remove devices
        # #####################

        if data["type"] == "device_removed":
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + data["meta"]["friendly_name"] + " | deleted")

        if data["type"] == "device_force_removed":
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + data["message"] + " | deleted (force)")


        # ##################
        # zigbee OTA updates
        # ##################

        if data["type"] == "ota_update":
            SET_ZIGBEE_DEVICE_UPDATE_STATUS(data["message"])
            
            # update found

            if data["meta"]["status"] == "available":
                SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "True")
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

            # update started

            if data["meta"]["status"] == "update_in_progress":
                WRITE_LOGFILE_SYSTEM("EVENT", "Network | Device | " + data["meta"]["device"] + " | Device Update | started")

            # update success

            if data["meta"]["status"] == "update_succeeded":
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + data["meta"]["device"] + " | Device Update | successful")
                time.sleep(10)
          
                SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "")

                # update update status
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("No Device Update available")

                for device in GET_ALL_DEVICES(""):
                    if device.update_available == "True":
                        SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

            # update failed
            
            if data["meta"]["status"] == "update_failed":
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + data["meta"]["device"] + " | Device Update | " + str(data["message"]))
                time.sleep(10)                

                # update update status
                SET_ZIGBEE_DEVICE_UPDATE_STATUS("No Device Update available")

                for device in GET_ALL_DEVICES(""):
                    if device.update_available == "True":
                        SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")

                # reset update variable
                if "No new image available" in str(data["message"]):
                    SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "False")
                else:
                    SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(GET_DEVICE_BY_NAME(data["meta"]["device"]).ieeeAddr, "True")


    # ########################
    # zigbee create networkmap
    # ########################

    if channel == "smarthome/zigbee2mqtt/bridge/networkmap/graphviz":

        try:

            # generate graphviz diagram
            from graphviz import Source, render

            src = Source(msg)
            src.render(filename = GET_PATH() + '/app/static/temp/zigbee_topology', format='png', cleanup=True)
            return

        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | Zigbee Topology | " + str)         


    # ###################
    # mqtt device updates
    # ###################

    if channel == "smarthome/mqtt/update":

        try:
            data = json.loads(msg)

            if data["message"] == "success":
                device = GET_DEVICE_BY_IEEEADDR(data["device_ieeeAddr"])

                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + device.name + " | updated || Version || " + device.version + " >>> " + str(data["version"]))
                UPDATE_MQTT_DEVICE_VERSION(device.ieeeAddr, data["version"])

            else:
                device = GET_DEVICE_BY_IEEEADDR(data["device_ieeeAddr"])

                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + device.name + " || " + str(data["message"]))                

        except:
            pass


    # ###########################
    # check battery + linkquality
    # ###########################

    if ieeeAddr != "":
        
        # save last values and last contact 
        SAVE_DEVICE_LAST_VALUES(ieeeAddr, msg)
        
        # check battery
        try:

            device_blocked = False

            # block existing device ?
            for device in list_battery_low_devices_blocked:   
                if device == ieeeAddr:
                    device_blocked = True
                    continue
                    
            if device_blocked == False:
                data = json.loads(msg)
            
                # special case eurotronic heater_thermostat
                if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "SPZB0001":
                    if int(data["battery"]) < 5:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device | " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")    

                        # add device to block list
                        list_battery_low_devices_blocked.append(ieeeAddr)
                        START_TIMER_BLOCK_BATTERY_LOW_DEVICES_THREAD(ieeeAddr)

                # default case for all other devices
                else:
                    if int(data["battery"]) < 20:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device | " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")           

                        # add device to block list
                        list_battery_low_devices_blocked.append(ieeeAddr)
                        START_TIMER_BLOCK_BATTERY_LOW_DEVICES_THREAD(ieeeAddr)

        except:
            pass               


        # check signal strength (mqtt)
        try:
            data = json.loads(msg)

            if device_type == "client_music" and int(data["signal_strength"]) < -65:

                # add ieeeAddr to the bad connection list
                bad_connection_list.append((str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ieeeAddr)) 

            if device_type != "client_music" and int(data["signal_strength"]) < -75:

                # add ieeeAddr to the bad connection list
                bad_connection_list.append((str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ieeeAddr))                 

        except:
            pass   


        if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

            # check linkquality (zigbee2mqtt)
            try:
                data = json.loads(msg)
                
                if int(data["linkquality"]) < 10:

                    # add ieeeAddr to the bad connection list
                    bad_connection_list.append((str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ieeeAddr)) 

            except:
                pass   


    # ##########
    # sensordata
    # ##########

    # save sensordata 
    for job in GET_ALL_SENSORDATA_JOBS():
        if job.device_ieeeAddr == ieeeAddr and job.always_active == "True":

            try:
                sensor_key = job.sensor_key.strip()
                data       = json.loads(msg)
                filename   = job.filename

                WRITE_SENSORDATA_FILE(filename, ieeeAddr, sensor_key, data[sensor_key])
                
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Sensordata | Job | " + job.name + " | " + str(e))


    # #########
    # schedular
    # #########

    # start schedular job 
    for task in GET_ALL_SCHEDULER_JOBS():
        if task.trigger_sensors == "True" and task.option_pause != "True":
            heapq.heappush(process_management_queue, (10, ("scheduler", task.id, ieeeAddr)))


    # ##########
    # controller
    # ##########

    # start controller job  
    if device_type == "controller":       
        heapq.heappush(process_management_queue, (1, ("controller", ieeeAddr, msg)))
        WRITE_LOGFILE_SYSTEM("WARNING", "TEST | Controller | " + str(msg))      
           
           
""" ###################### """
"""  mqtt publish message  """
""" ###################### """

def START_MQTT_PUBLISH_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_PUBLISH_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | MQTT Publish | " + str(e))  


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
                    print("ERROR: Network | MQTT | " + str(e))
                    
            except:
                print("ERROR: Network | MQTT")
                    
        time.sleep(0.1)


""" ########################### """
""" ########################### """
"""     background functions    """
""" ########################### """
""" ########################### """


""" ########################### """
"""  check mqtt running thread  """
""" ########################### """

def START_CHECK_MQTT_RUNNING_THREAD():

    try:
        Thread = threading.Thread(target=CHECK_MQTT_RUNNING_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Check MQTT running | " + str(e))  


def CHECK_MQTT_RUNNING_THREAD():
    
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
                    data    = json.loads(message)
                   
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
                        input_trigger = data['input_trigger']
                        input_trigger = ','.join(input_trigger)
                        input_trigger = input_trigger.replace("'", '"')                                         
                    except:
                        input_trigger = ""
                        
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
                        ADD_DEVICE(name, gateway, ieeeAddr, model, device_type, version, description, input_values, input_trigger, commands, commands_json)
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + name + " | added")   
                      
                    # update existing device

                    else:
                        id   = GET_DEVICE_BY_IEEEADDR(ieeeAddr).id
                        name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
                                        
                        UPDATE_DEVICE(id, name, gateway, model, device_type, version, description, input_values, input_trigger, commands, commands_json)
                        SET_DEVICE_LAST_CONTACT(ieeeAddr)
                      
                    # update input values
    
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/mqtt/" + ieeeAddr + "/get", "")))
                    time.sleep(1)

            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | MQTT | Update")
            return True


        except Exception as e:
            if str(e) == "string index out of range":
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Update | " + str(e))            
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
                                        
                                        # add new devices from zigbee2mqtt database
                                
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
                                            input_trigger = new_device[3]  
                                            commands      = new_device[4]                                
                                            commands_json = new_device[5] 

                                            ADD_DEVICE(name, gateway, ieeeAddr, new_model, device_type, version, description, input_values, input_trigger, commands, commands_json)
                                            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + name + " | added")    

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
                                                input_trigger = existing_device[3]  
                                                commands      = existing_device[4]  
                                                commands_json = existing_device[5] 

                                            except Exception as e:
                                                device_type   = device_data.device_type
                                                version       = ""                                                
                                                description   = device_data.description                                             
                                                input_values  = device_data.input_values
                                                input_trigger = device_data.input_trigger
                                                commands      = device_data.commands 
                                                commands_json = device_data.commands_json 
                                        
                                                error = "Error | " + str(existing_model) + " not found | " + str(e)
                                                                        
                                            UPDATE_DEVICE(id, name, gateway, existing_model, device_type, version, description, input_values, input_trigger, commands, commands_json)

                                except:
                                    pass

        
                if error != "":
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Update | " + str(error))                
                    return ("Network | ZigBee2MQTT | Update | " + str(error)) 
                else:
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Update")

                    # update zigbee topology
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/networkmap", "graphviz")))
                    return True
     
     
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Update | " + str(e))       
                return ("Network | ZigBee2MQTT | Update " + str(e))

        else:
            return True


""" ####################### """
"""  check device settings  """
""" ####################### """
 
def CHECK_DEVICE_SETTING_THREAD(ieeeAddr, command, setting, seconds = 100): 
    Thread  = threading.Thread(target=CHECK_DEVICE_SETTING_PROCESS, args=(ieeeAddr, command, setting, seconds, ))
    Thread.start()   

 
def CHECK_DEVICE_SETTING_PROCESS(ieeeAddr, command, setting, seconds, log_report = True):  
    repeats = seconds * 5                 
    device  = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
    counter = 1

    while counter < repeats:  
        
        if device.gateway == "mqtt":
            result = CHECK_MQTT_SETTING(device.ieeeAddr, command)
        if device.gateway == "zigbee2mqtt":
            result = CHECK_ZIGBEE2MQTT_SETTING(device.name, command)   

        # set previous setting
        if result == True:
            if log_report == True:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device | " + device.name + " | Setting changed | " + setting)  

            return True

        counter = counter + 1
        time.sleep(0.2)       

    # error message
    if log_report == True:
        WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device | " + device.name + " | Setting not confirmed | " + setting)           
              
    return ("Device | " + device.name + " | Setting not confirmed | " + setting) 
                         

def CHECK_MQTT_SETTING(ieeeAddr, command):     
    command = command[1:-1]

    for message in GET_MQTT_INCOMING_MESSAGES(20):

        # search for fitting message in incoming_messages_list
        if (message[1] == "smarthome/mqtt/" + ieeeAddr or 
            message[1] == "smarthome/mqtt/" + ieeeAddr + "/state" or 
            message[1] == "smarthome/mqtt/" + ieeeAddr + "/command_status"):

            return_message = str(message[2])
            return_message = return_message.replace("{","")
            return_message = return_message.replace("}","")

            # only one command value ( "," = separator inside command entities || ";" = separator between command entities )
            if not ";" in command:    
                if command in return_message:
                    return True
                                                    
            # more then one command values:
            else:
                
                list_commands = command.split(";")
                
                for command in list_commands:      
                    if not command in return_message:
                        return False    
                        
                return True
                
    return False
   

def CHECK_ZIGBEE2MQTT_SETTING(device_name, command):
    command = command[1:-1]

    if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

        for message in GET_MQTT_INCOMING_MESSAGES(20):

            # search for fitting message in incoming_messages_list
            if message[1] == "smarthome/zigbee2mqtt/" + device_name:   

                return_message = str(message[2])
                return_message = return_message.replace("{","")
                return_message = return_message.replace("}","")

                # only one setting value ( "," = separator between command entities || ";" = separator between command values )
                if not ";" in command:       
                    if command in return_message:
                        return True
                                    
                # more then one command value:
                else:
                    
                    list_commands = command.split(";")
                    
                    for command in list_commands:        
                        if not command in return_message:
                            return False    
                            
                    return True                    
                
        return False

    else:
        return False


""" ######################## """
"""  check functions zigbee  """
""" ######################## """
 
def CHECK_ZIGBEE2MQTT_STARTED():    
    counter = 1

    # 10 seconds
    while counter < 50:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):          
            if message[1] == "smarthome/zigbee2mqtt/bridge/state":
            
                try:
                    if message[2] == "online":
                        SET_ZIGBEE2MQTT_CONNECTION_STATUS(True)
                        return True

                except:
                    pass

        counter = counter + 1
        time.sleep(0.2)

    SET_ZIGBEE2MQTT_CONNECTION_STATUS(False)     
    return False


def CHECK_ZIGBEE2MQTT_NAME_CHANGED(previous_name, new_name):   
    counter = 1

    # 10 seconds
    while counter < 50:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):      
            if message[1] == "smarthome/zigbee2mqtt/bridge/log":
            
                try:
                    data = json.loads(message[2])
                    
                    if data["type"] == "device_renamed" and data["message"]["from"] == previous_name and data["message"]["to"] == new_name:
                        return True

                except:
                    pass

        counter = counter + 1
        time.sleep(0.2)
                
    return False


def CHECK_ZIGBEE2MQTT_PAIRING(pairing_setting):    
    counter = 1

    # 10 seconds
    while counter < 50:       
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

        counter = counter + 1
        time.sleep(0.2)
                    
    return False


def CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):        
    counter = 1

    # 15 seconds
    while counter < 100:       
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

        counter = counter + 1
        time.sleep(0.2)
                    
    return False 


def START_CHECK_ZIGBEE2MQTT_RUNNING_THREAD():

    try:
        Thread = threading.Thread(target=CHECK_ZIGBEE2MQTT_RUNNING_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Check ZIGBEE running | " + str(e))  


def CHECK_ZIGBEE2MQTT_RUNNING_THREAD():   

    while True:

        try:

            if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

                counter = 1

                if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "True":
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "true")))   

                if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "False":
                    heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))   

                zigbee_active = False

                # 10 seconds
                while counter < 50:       
                    for message in GET_MQTT_INCOMING_MESSAGES(15):
                        if message[1] == "smarthome/zigbee2mqtt/bridge/config":   
                            zigbee_active = True
                            counter       = 50

                    counter = counter + 1
                    time.sleep(0.2)

                if zigbee_active == True:
                    SET_ZIGBEE2MQTT_CONNECTION_STATUS(True)      
                else:          
                    SET_ZIGBEE2MQTT_CONNECTION_STATUS(False)
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | No connection")  
                    SEND_EMAIL("SYSTEM", "Network | ZigBee2MQTT | No connection")    

                    fail_counter = 0

                    # fail process
                    while fail_counter < 3600 and zigbee_active == False:

                        if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "True":
                            heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "true")))   

                        if GET_ZIGBEE2MQTT_PAIRING_SETTING() == "False":
                            heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))                           

                        counter = 1                        

                        # 10 seconds
                        while counter < 50:       
                            for message in GET_MQTT_INCOMING_MESSAGES(15):
                                if message[1] == "smarthome/zigbee2mqtt/bridge/config":  
                                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | connected")  
                                    SEND_EMAIL("SYSTEM", "Network | ZigBee2MQTT | connected")    
                                    zigbee_active = True
                                    counter       = 50
                                    break

                            counter = counter + 1
                            time.sleep(0.2)

                        fail_counter = fail_counter + 10
                        time.sleep(10)

        except:
            pass

        time.sleep(600)   # every 10 minutes


""" ########################## """
"""  check device connections  """
""" ########################## """

def START_CHECK_DEVICE_CONNECTION_THREAD():

    try:
        Thread = threading.Thread(target=CHECK_DEVICE_CONNECTION_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Check Device connection | " + str(e))  


def CHECK_DEVICE_CONNECTION_THREAD():   

    while True:

        try:

            # get the current time value
            time_check_mqtt = datetime.datetime.now() - datetime.timedelta(days=2) 
            time_check_mqtt = time_check_mqtt.strftime("%Y-%m-%d %H:%M:%S")

            for device in GET_ALL_DEVICES("mqtt"):

                time_last_contact = datetime.datetime.strptime(device.last_contact,"%Y-%m-%d %H:%M:%S")   
                time_limit        = datetime.datetime.strptime(time_check_mqtt, "%Y-%m-%d %H:%M:%S")                

                # error message if no connection in the last 48 hours
                if time_last_contact < time_limit:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device | " + device.name + " | No connection since: " + str(time_last_contact))


            if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

                # get the current time value
                time_check_zigbee2mqtt = datetime.datetime.now() - datetime.timedelta(days=2) 
                time_check_zigbee2mqtt = time_check_zigbee2mqtt.strftime("%Y-%m-%d %H:%M:%S")

                for device in GET_ALL_DEVICES("zigbee2mqtt"):

                    time_last_contact = datetime.datetime.strptime(device.last_contact,"%Y-%m-%d %H:%M:%S")   
                    time_limit        = datetime.datetime.strptime(time_check_zigbee2mqtt, "%Y-%m-%d %H:%M:%S")                

                    # error message if no connection in the last 48 hours
                    if time_last_contact < time_limit:
                        WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device | " + device.name + " | No connection since: " + str(time_last_contact))

        except:
            pass

        # check every 12h
        time.sleep(43200)


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

                if exception.exception_option == "IP-ADDRESS" and exception_command.lower() == command.lower():

                    for x in range(5):
                        if ping(exception.exception_value_1, timeout=1) != None:    
                            return (exception.device.name + " | Device running")
       

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
 
    if device_gateway == "mqtt":
        channel = "smarthome/" + device_gateway + "/" + device_ieeeAddr + "/get" 

    if device_gateway == "zigbee2mqtt":
        channel = "smarthome/" + device_gateway + "/" + device_name + "/get"
 
    heapq.heappush(mqtt_message_queue, (20, (channel, "")))        
    time.sleep(2) 
  
    for message in GET_MQTT_INCOMING_MESSAGES(5):
        
        # mqtt
        if device_gateway == "mqtt":

            if message[1] == "smarthome/" + device_gateway + "/" + device_ieeeAddr:
                    
                try:

                    data     = json.loads(message[2])
                    filename = sensordata_job.filename
        
                    WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Sensordata | Job | " + job_name + " | Data saved")  
                    return True
                    
                except:
                    pass

        # zigbee2mqtt                
        if device_gateway == "zigbee2mqtt":

            if message[1] == "smarthome/" + device_gateway + "/" + device_name:
                    
                try:

                    data     = json.loads(message[2])
                    filename = sensordata_job.filename
        
                    WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Sensordata | Job | " + job_name + " | Data saved")  
                    return True
                    
                except:
                    pass

    WRITE_LOGFILE_SYSTEM("ERROR", "Sensordata | Job | " + job_name + " | No Data found") 