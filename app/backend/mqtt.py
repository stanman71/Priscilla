import paho.mqtt.client as mqtt
import heapq
import threading
import json
import datetime
import time

from app import app
from app.database.models import *
from app.backend.file_management import *
from app.backend.shared_resources import *
from app.backend.email import SEND_EMAIL

from ping3 import ping


""" ###################### """
"""  mqtt receive message  """
""" ###################### """
    
def START_MQTT_RECEIVE_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_RECEIVE_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Receive | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Receive | " + str(e))    

    
def MQTT_RECEIVE_THREAD():

    def on_connect(client, userdata, flags, rc):   
        if rc != 0:
            print("ERROR: Network | MQTT | Returned Code = " + str(rc)) 
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Returned Code = " + str(rc))         
        
            SET_DEVICE_CONNECTION_MQTT(False)   
        
        else:
            client.subscribe("smarthome/#")
  
            print("Network | MQTT | Connected") 
            WRITE_LOGFILE_SYSTEM("NETWORK", "Network | MQTT | Connected")
            SET_DEVICE_CONNECTION_MQTT(True)


    def on_message(client, userdata, message):     
        global mqtt_incoming_messages_list

        new_message = True
        ieeeAddr    = ""
        device_type = ""  

        channel     = message.topic                 
        msg         = str(message.payload.decode("utf-8"))       


        # get ieeeAddr and device_type
        device_identity = channel.split("/")[2]
        
        if device_identity not in ["bridge", "devices", "test", "log", "get", "set", "config"]:
        
            list_devices = GET_ALL_DEVICES("")
        
            # zigbee2mqtt device
            for device in list_devices:
                if device.name == device_identity:             
                    ieeeAddr = device.ieeeAddr
                    break
            
            # mqtt device or no zigbee2mqtt friendly_name exist
            if ieeeAddr == "": 
                ieeeAddr = device_identity
                
            try:
                for device in list_devices:
                    if device.name == device_identity:             
                        device_type = device.device_type            
            except:
                device_type = ""    
                
            
        # message block ?
        if (device_type == "led_rgb" or 
            device_type == "led_simple" or 
            device_type == "power_switch" or 
            device_type == "heater_thermostat" or    
            device_type == "blind" or      
            device_type == "sensor_passiv"):
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(3):              
                
                # search for other messages from the same device
                if existing_message[1] == channel:
                    
                    try:
                        # device sends new data ?
                        existing_data = json.loads(existing_message[2])
                        new_data      = json.loads(msg)

                        if existing_data["state"] != new_data["state"]:
                            new_message = True
                            break
                            
                        else:
                            new_message = False
                            
                    except:
                        new_message = False                 


        # message block ?
        if (device_type == "controller"):
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(1):              
                
                # search for other messages from the same device
                if existing_message[1] == channel:
                    
                    try:
                        # device sends new data ?
                        existing_data = json.loads(existing_message[2])
                        new_data      = json.loads(msg)

                        if existing_data["state"] != new_data["state"]:
                            new_message = True
                            break
                            
                        else:
                            new_message = False
                            
                    except:
                        new_message = False  


        # message passing
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
                    WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Message | " + str(e)) 
                    SEND_EMAIL("ERROR", "Thread | MQTT Message | " + str(e))                    
                    print(e)


    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("localhost", 1883, 60)
        client.loop_forever()

    except Exception as e:
        print("ERROR: MQTT | " + str(e)) 
        WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e))        
        SET_DEVICE_CONNECTION_MQTT(False)    


""" ############## """
"""  mqtt message  """
""" ############## """

def MQTT_MESSAGE(channel, msg, ieeeAddr, device_type):
  
    # zigbee2mqtt log messages
    if channel == "smarthome/zigbee2mqtt/bridge/log":
        
        data = json.loads(msg)
        
        # new device conneted
        if data["type"] == "pairing" and data["message"] == "interview_started":
            SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device founded - " + data["meta"]["friendly_name"])   

        # device successful added
        if data["type"] == "pairing" and data["message"] == "interview_successful":
            time.sleep(5)
            UPDATE_DEVICES("zigbee2mqtt")
            WRITE_LOGFILE_SYSTEM("NETWORK", "Network | Device - " + data["meta"]["friendly_name"] + " | added")   
            SET_ZIGBEE2MQTT_PAIRING_STATUS("New Device added - " + data["meta"]["friendly_name"])   
            time.sleep(10)      
            SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 

        # device connection failed
        if data["type"] == "pairing" and data["message"] == "interview_failed":
            SET_ZIGBEE2MQTT_PAIRING_STATUS("Device adding failed - " + data["meta"]["friendly_name"])   
            time.sleep(10)
            SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 
      
        # remove devices
        if data["type"] == "device_removed":
            WRITE_LOGFILE_SYSTEM("NETWORK", "Network | Device - " + data["meta"]["friendly_name"] + " | deleted")

        if data["type"] == "device_force_removed":
            WRITE_LOGFILE_SYSTEM("NETWORK", "Network | Device - " + data["message"] + " | deleted (force)")


    # start function networkmap
    if channel == "smarthome/zigbee2mqtt/bridge/networkmap/graphviz":

        # generate graphviz diagram
        from graphviz import Source, render

        src = Source(msg)
        src.render(filename = GET_PATH() + '/app/static/temp/zigbee_topology', format='png', cleanup=True)
        return


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
            if task.option_sensors == "True" and task.option_pause != "True":
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
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Publish | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Publish | " + str(e))    


def MQTT_PUBLISH_THREAD():
    
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            print("ERROR: Network | MQTT | Returned Code = " + str(rc)) 
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | Returned Code = " + str(rc))         
            SET_DEVICE_CONNECTION_MQTT(False)   
        
        else:
            SET_DEVICE_CONNECTION_MQTT(True)

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("localhost", 1883, 60)
        client.loop_start()
    
    except Exception as e:
        print("ERROR: MQTT | " + str(e)) 
        WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e))    
        SET_DEVICE_CONNECTION_MQTT(False)        


    while True:
        try:  
            # check mqtt connection
            if GET_DEVICE_CONNECTION_MQTT() == True:              
                mqtt_message = heapq.heappop(mqtt_message_queue)[1]      
                client.publish(mqtt_message[0],mqtt_message[1])        

        except Exception as e:         
            try:   
                if "index out of range" not in str(e):
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT Publish | " + str(e))  
                    SEND_EMAIL("ERROR", "Network | MQTT Publish | " + str(e))               
                    print(str(e))
                    
            except:
                print("ERROR: MQTT")
                    
        time.sleep(0.5)


""" ##################### """
"""  mqtt control thread  """
""" ##################### """

def START_MQTT_CONTROL_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_CONTROL_THREAD)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Publish | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Publish | " + str(e))    


def MQTT_CONTROL_THREAD():
    
    def on_connect(client, userdata, flags, rc):
        if rc != 0:    
            SET_DEVICE_CONNECTION_MQTT(False)   
        
        else:
            SET_DEVICE_CONNECTION_MQTT(True)

    while True:

        try:
            check_client = mqtt.Client()
            check_client.on_connect = on_connect
            check_client.connect("localhost", 1883, 60)
            check_client.disconnect()
    
        except Exception as e:
            SET_DEVICE_CONNECTION_MQTT(False)        
                    
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
                        ADD_DEVICE(name, gateway, ieeeAddr, model, device_type, description, input_values, input_events, commands, commands_json)
                      
                    # update existing device

                    else:
                        id   = GET_DEVICE_BY_IEEEADDR(ieeeAddr).id
                        name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
                                        
                        UPDATE_DEVICE(id, name, gateway, model, device_type, description, input_values, input_events, commands, commands_json)
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


    if gateway == "zigbee2mqtt":

        if GET_SYSTEM_SERVICES().zigbee2mqtt_active == "True":
        
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
                                
                                # skip coordinator
                                if device['type'] != "Coordinator":
                                    
                                    # add new device
                            
                                    if not GET_DEVICE_BY_IEEEADDR(device['ieeeAddr']):

                                        name     = device['friendly_name']
                                        gateway  = "zigbee2mqtt"              
                                        ieeeAddr = device['ieeeAddr']

                                        try:
                                            new_model  = device['model']
                                            new_device = GET_DEVICE_INFORMATIONS(new_model)
                                        except:
                                            new_model  = ""
                                            new_device = ["", "", "", "", "", ""]
                                            
                                        device_type   = new_device[0]
                                        description   = new_device[1]
                                        input_values  = new_device[2]
                                        input_events  = new_device[3]  
                                        commands      = new_device[4]                                
                                        commands_json = new_device[5] 

                                        ADD_DEVICE(name, gateway, ieeeAddr, new_model, device_type, description, input_values, input_events, commands, commands_json)

                                    # update device informations
                                
                                    else:
                                
                                        device_data = GET_DEVICE_BY_IEEEADDR(device['ieeeAddr'])

                                        id             = device_data.id         
                                        name           = device['friendly_name']
                                        existing_model = device['model']  
                                        gateway        = "zigbee2mqtt"

                                        try:                           
                                            existing_device = GET_DEVICE_INFORMATIONS(existing_model)
                                            
                                            device_type   = existing_device[0]
                                            description   = existing_device[1]
                                            input_values  = existing_device[2]
                                            input_events  = existing_device[3]  
                                            commands      = existing_device[4]  
                                            commands_json = existing_device[5] 

                                        except Exception as e:
                                            device_type   = device_data.device_type
                                            description   = device_data.description 
                                            input_values  = device_data.input_values
                                            input_events  = device_data.input_events
                                            commands      = device_data.commands 
                                            commands_json = device_data.commands_json 
                                    
                                            error = "Error | " + str(existing_model) + " not founded | " + str(e)
                                                                    
                                        UPDATE_DEVICE(id, name, gateway, existing_model, device_type, description, input_values, input_events, commands, commands_json)

        
                if error != "":
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Update | " + str(error))
                    SEND_EMAIL("ERROR", "Network | ZigBee2MQTT | Update | " + str(error))                 
                    return ("Network | ZigBee2MQTT | Update | " + str(error)) 
                else:
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Update")
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
 
def CHECK_DEVICE_SETTING_THREAD(ieeeAddr, setting, repeats = 10): 
    Thread = threading.Thread(target=CHECK_DEVICE_SETTING_PROCESS, args=(ieeeAddr, setting, repeats, ))
    Thread.start()   

 
def CHECK_DEVICE_SETTING_PROCESS(ieeeAddr, setting, repeats):                
    device  = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
    counter = 1

    # special case IKEA Roller Blinds 
    if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "E1757" or GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "E1926":
        return True

    else:

        while counter != repeats:  
            
            if device.gateway == "mqtt":
                result = CHECK_MQTT_SETTING(device.ieeeAddr, setting)
            if device.gateway == "zigbee2mqtt":
                result = CHECK_ZIGBEE2MQTT_SETTING(device.name, setting)    
        
            # set previous setting
            if result == True:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + device.name + " | Setting changed | " + setting)  
                return True

            counter = counter + 1
            time.sleep(1)       

        # error message
        WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + device.name + " | Setting not confirmed | " + setting)  
        SEND_EMAIL("ERROR", "Network | Device - " + device.name + " | Setting not confirmed | " + setting)                
        return ("Device - " + device.name + " | Setting not confirmed - " + setting) 
                         

def CHECK_MQTT_SETTING(ieeeAddr, setting):        
    for message in GET_MQTT_INCOMING_MESSAGES(10):
        
        # search for fitting message in incoming_messages_list
        if message[1] == "smarthome/mqtt/" + ieeeAddr:  
                       
            # only one setting value
            if not "," in setting:    
                if setting.lower() in message[2].lower():
                    return True
                                                    
            # more then one setting value:
            else:
                
                list_settings = setting.split(",")
                
                for setting in list_settings:           
                    if not setting.lower() in message[2].lower():
                        return False    
                        
                return True
                
    return False
   

def CHECK_ZIGBEE2MQTT_SETTING(device_name, setting):

    if GET_SYSTEM_SERVICES().zigbee2mqtt_active == "True":

        for message in GET_MQTT_INCOMING_MESSAGES(10):

            # search for fitting message in incoming_messages_list
            if message[1] == "smarthome/zigbee2mqtt/" + device_name:   

                # only one setting value
                if not "," in setting:       
                    if setting.lower() in message[2].lower():
                        return True
                                    
                # more then one setting value:
                else:
                    
                    list_settings = setting.split(",")
                    
                    for setting in list_settings:        
                        if not setting.lower() in message[2].lower():
                            return False    
                            
                    return True                    
                
        return False

    else:
        return False


""" ################# """
"""  check functions  """
""" ################# """
 
def CHECK_ZIGBEE2MQTT_AT_STARTUP():    
    counter = 1

    while counter != 5:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):          
            if message[1] == "smarthome/zigbee2mqtt/bridge/state":
            
                try:
                    if message[2] == "online":
                        SET_DEVICE_CONNECTION_ZIGBEE2MQTT(True)
                        return True

                except:
                    pass

        counter = counter + 1
        time.sleep(1)

    SET_DEVICE_CONNECTION_ZIGBEE2MQTT(False)     
    return False


def CHECK_ZIGBEE2MQTT_NAME_CHANGED(old_name, new_name):   
    counter = 1

    while counter != 10:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):      
            if message[1] == "smarthome/zigbee2mqtt/bridge/log":
            
                try:
                    data = json.loads(message[2])
                    
                    if data["type"] == "device_renamed" and data["message"]["from"] == old_name and data["message"]["to"] == new_name:
                        return True

                except:
                    pass

        counter = counter + 1
        time.sleep(1)
                
    return False


def CHECK_ZIGBEE2MQTT_PAIRING(pairing_setting):    
    counter = 1

    while counter != 5:       
        for message in GET_MQTT_INCOMING_MESSAGES(10):
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
        time.sleep(1)
                    
    return False


def CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):        
    counter = 1

    while counter != 15:       
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
        time.sleep(1)
                    
    return False 


""" ######################### """
"""  check device exceptions  """
""" ######################### """


def CHECK_DEVICE_EXCEPTIONS(id, setting):
    device = GET_DEVICE_BY_ID(id)

    try:
                        
        # ####################
        # exception ip_address 
        # ####################
        
        exception_setting = device.exception_setting.replace(" ", "")

        if device.exception_option == "IP-Address" and exception_setting == setting:

            for x in range(3):
                if ping(device.exception_value_1, timeout=1) != None:    
                    return (device.name + " | Device running")
                    break
    
            else:
                return True


        # ################
        # exception sensor
        # ################
        
        if device.exception_sensor_ieeeAddr != "None" and exception_setting == setting:
            
            sensor_ieeeAddr = device.exception_sensor_ieeeAddr
            sensor_key      = device.exception_value_1   
            operator        = device.exception_value_2
            value           = device.exception_value_3

            try:
                value = str(value).lower()
            except:
                pass
                    
            
            # get sensordata 
            data         = json.loads(GET_DEVICE_BY_IEEEADDR(device.exception_sensor_ieeeAddr).last_values_json)
            sensor_value = data[sensor_key]
            
            try:
                sensor_value = str(sensor_value).lower()
            except:
                pass
            
                
            # compare conditions
            if operator == "=" and value.isdigit():
                if int(sensor_value) == int(value):
                    return (device.name + " | Sensor passing failed")   
                else:
                    return True
                    
            if operator == "=" and not value.isdigit():
                if str(sensor_value) == str(value):
                    return (device.name + " | Sensor passing failed")  
                else:
                    return True
                    
            if operator == "<" and value.isdigit():
                if int(sensor_value) < int(value):
                    return (device.name + " | Sensor passing failed")  
                else:
                    return True
                    
            if operator == ">" and value.isdigit():
                if int(sensor_value) > int(value):
                    return (device.name + " | Sensor passing failed")  
                else:
                    return True
                
        return True

    except:
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
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | Device - " + device_name + " | Sensordata | saved")  
                return True
                
            except:
                pass

    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Device - " + device_name + " | Sensordata | Data not founded") 
    SEND_EMAIL("ERROR", "Network | Device - " + device_name + " | Sensordata | Data not founded")       

   
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