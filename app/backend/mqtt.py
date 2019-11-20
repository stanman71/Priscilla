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
    
    
def MQTT_RECEIVE_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_RECEIVE)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Receive | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Receive | " + str(e))    

    
def MQTT_RECEIVE():

    def on_message(client, userdata, new_message): 
        
        global mqtt_incoming_messages_list
      
        channel = new_message.topic                 
        msg     = str(new_message.payload.decode("utf-8"))        
      
        new_message = True
        ieeeAddr    = ""
        device_type = ""


        # get ieeeAddr and device_type
        incoming_topic  = channel
        incoming_topic  = incoming_topic.split("/")
        device_identity = incoming_topic[2]
        
        if device_identity not in ["bridge", "devices", "test", "log", "get", "set", "config"]:
        
            list_devices = GET_ALL_DEVICES("")
         
            # zigbee2mqtt device
            for device in list_devices:
                if device.name == device_identity:             
                    ieeeAddr = device.ieeeAddr
                    break
            
            # mqtt device or no zigbee2mqtt name choosed
            if ieeeAddr == "": 
                ieeeAddr = device_identity
                
            try:
                for device in list_devices:
                    if device.name == device_identity:             
                        device_type = device.device_type            
            except:
                device_type = ""    
                
            
        # message block ?
        if (device_type == "led_rgb" or device_type == "led_simple" or device_type == "power_switch" or device_type == "heater"):
    
            for existing_message in GET_MQTT_INCOMING_MESSAGES(3):              
                
                if existing_message[1] == channel:
                    
                    try:
                        # devices changes state ?
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


    def on_connect(client, userdata, flags, rc):   
        if rc != 0:
            print("ERROR: MQTT | Broker - " + GET_MQTT_BROKER() + " | Bad Connection | Returned Code = " + str(rc)) 
            WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | Broker - " + GET_MQTT_BROKER() + " | Bad Connection | Returned Code = " + str(rc))         
        
        else:
            client.subscribe("miranda/#")
  
            print("MQTT | Broker - " + GET_MQTT_BROKER() + " | Connected") 
            WRITE_LOGFILE_SYSTEM("EVENT", "MQTT | Broker - " + GET_MQTT_BROKER() + " | Connected")
                
 
    client = mqtt.Client()
    client.username_pw_set(username=GET_MQTT_BROKER_USERNAME(),password=GET_MQTT_BROKER_PASSWORD())
    client.on_connect = on_connect
    client.on_message = on_message
     
    try:
        client.connect(GET_MQTT_BROKER())
        client.loop_forever()

    except Exception as e:
        print("ERROR: MQTT | Broker - " + GET_MQTT_BROKER() + " | " + str(e))
        
        WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | Broker - " + GET_MQTT_BROKER() + " | " + str(e))
        SEND_EMAIL("ERROR", "MQTT | Broker - " + GET_MQTT_BROKER() + " | " + str(e))


""" ############## """
"""  mqtt message  """
""" ############## """


def MQTT_MESSAGE(channel, msg, ieeeAddr, device_type):
  
    channel = channel.split("/")
  
    # filter incoming messages
    try:

        # zigbee2mqtt log messages
        if channel[3] == "log":
            
            data = json.loads(msg)
            
            # add devices
            if data["type"] == "device_connected":
                time.sleep(5)
                UPDATE_DEVICES("zigbee2mqtt")
                WRITE_LOGFILE_SYSTEM("EVENT", "Device | Added - " + data["message"])    
    
            # remove devices
            if data["type"] == "device_removed":
                WRITE_LOGFILE_SYSTEM("EVENT", "Device | Deleted - " + data["message"])


        # start function networkmap
        if channel[3] == "networkmap" and channel[4] == "graphviz":

            # generate graphviz diagram
            from graphviz import Source, render

            src = Source(msg)
            src.render(filename = GET_PATH() + '/app/static/temp/zigbee_topology', format='png', cleanup=True)
            return
        
    except:
        pass
         
         
    if ieeeAddr != "":
        
        # save last values and last contact 
        SAVE_DEVICE_LAST_VALUES(ieeeAddr, msg)
        
        # check battery
        if GET_DEVICE_BY_IEEEADDR(ieeeAddr).gateway == "zigbee2mqtt":
            
            try:
                data = json.loads(msg)
                
                if int(data["battery"]) < 25:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")
                    SEND_EMAIL("WARNING", "Device - " + GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " | Battery low")                         
            except Exception as e:
                print(e)                


    if device_type == "sensor_passiv" or device_type == "sensor_active" or device_type == "sensor_contact" or device_type == "watering_controller":
        
        # save sensor data of passive devices
        if FIND_SENSORDATA_JOB_INPUT(ieeeAddr) != "":
            list_jobs = FIND_SENSORDATA_JOB_INPUT(ieeeAddr)

            for job in list_jobs:   
                SAVE_SENSORDATA(job) 

        # start schedular job 
        for task in GET_ALL_SCHEDULER_TASKS():
            if task.option_sensors == "checked" and task.option_pause != "checked":
                heapq.heappush(process_management_queue, (10, ("scheduler", "sensor", task.id, ieeeAddr)))


    # start controller job  
    if device_type == "controller":       
        heapq.heappush(process_management_queue, (1, ("controller", ieeeAddr, msg)))
            

""" ###################### """
"""  mqtt publish message  """
""" ###################### """

def MQTT_PUBLISH_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_PUBLISH)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Publish | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Publish | " + str(e))    


def MQTT_PUBLISH():
    
    while True:
        
        try:  
            mqtt_message = heapq.heappop(mqtt_message_queue)[1]
            
            def on_publish(client, userdata, mid):
                print ('Message Published...')

            client = mqtt.Client()
            client.username_pw_set(username=GET_MQTT_BROKER_USERNAME(),password=GET_MQTT_BROKER_PASSWORD())          
            client.on_publish = on_publish
            client.connect(GET_MQTT_BROKER())      
            client.publish(mqtt_message[0],mqtt_message[1])        
            client.disconnect()

        except Exception as e:         
            try:   
                if "index out of range" not in str(e):
                    WRITE_LOGFILE_SYSTEM("ERROR", "MQTT Publish | " + str(e))  
                    SEND_EMAIL("ERROR", "MQTT Publish | " + str(e))               
                    print(str(e))
                    
            except:
                pass
                    
        time.sleep(0.5)


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
        
        heapq.heappush(mqtt_message_queue, (20, ("miranda/mqtt/devices", "")))
        time.sleep(10)

        try:
            for message in GET_MQTT_INCOMING_MESSAGES(15):
                
                if message[1] == "miranda/mqtt/log":

                    message = str(message[2])
                   
                    data = json.loads(message)
                   
                    name            = data['ieeeAddr']
                    gateway         = "mqtt"
                    ieeeAddr        = data['ieeeAddr']
                    model           = data['model']

                    try:
                        device_type = data['device_type']
                    except:
                        device_type = ""                 
                      
                    try:
                        description = data['description']
                    except:
                        description = ""

                    try:
                        input_values = data['input_values']
                        input_values = ','.join(input_values)   
                        input_values = input_values.replace("'", '"')
                    except:
                        input_values = ""
                      
                    try:
                        input_events = data['input_events']
                        input_events = ','.join(input_events)
                        input_events = input_events.replace("'", '"') 
                        input_events = input_events.replace("},{", '} {')                                           
                    except:
                        input_events = ""
                        
                    try:
                        commands     = data['commands'] 
                        commands     = ','.join(commands)
                        commands     = commands.replace("'", '"')
                        commands     = commands.replace("},{", '} {')                               
                    except:
                        commands     = ""


                    # add new device

                    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):
                        ADD_DEVICE(name, gateway, ieeeAddr, model, device_type, description, input_values, input_events, commands)
                      
                    # update existing device

                    else:
                        id   = GET_DEVICE_BY_IEEEADDR(ieeeAddr).id
                        name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
                                        
                        UPDATE_DEVICE(id, name, gateway, model, device_type, description, input_values, input_events, commands)
                        SET_DEVICE_LAST_CONTACT(ieeeAddr)
                      
                    # update input values
                    
                    heapq.heappush(mqtt_message_queue, (20, ("miranda/mqtt/" + ieeeAddr + "/get", "")))
                    time.sleep(1)

            WRITE_LOGFILE_SYSTEM("SUCCESS", "Devices | MQTT | Update")
            return True


        except Exception as e:
            if str(e) == "string index out of range":
                WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | No Connection") 
                SEND_EMAIL("ERROR", "MQTT | No Connection")                 
                return ("Devices | Update | " + str(error))     


    if gateway == "zigbee2mqtt":
        
        error = ""
    
        heapq.heappush(mqtt_message_queue, (20, ("miranda/zigbee2mqtt/bridge/config/devices", "")))        
        time.sleep(5)
      
        try:

            for message in GET_MQTT_INCOMING_MESSAGES(10):
                    
                if message[1] == "miranda/zigbee2mqtt/bridge/log":

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

                                    name         = device['friendly_name']
                                    gateway      = "zigbee2mqtt"              
                                    ieeeAddr     = device['ieeeAddr']

                                    try:
                                        new_model  = device['model']
                                        new_device = GET_DEVICE_INFORMATIONS(new_model)
                                    except:
                                        new_model  = ""
                                        new_device = ["", "", "", "", ""]
                                        
                                    device_type  = new_device[0]
                                    description  = new_device[1]
                                    input_values = new_device[2]
                                    input_events = new_device[3]  
                                    commands     = new_device[4]                                

                                    ADD_DEVICE(name, gateway, ieeeAddr, new_model, device_type, description, input_values, input_events, commands)

                                # update device informations
                            
                                else:
                               
                                    device_data = GET_DEVICE_BY_IEEEADDR(device['ieeeAddr'])

                                    id       = device_data.id         
                                    name     = device['friendly_name']
                                    gateway  = "zigbee2mqtt"

                                    try:          
                                        model = device['model'] 
                                                
                                        existing_device = GET_DEVICE_INFORMATIONS(model)
                                        
                                        device_type  = existing_device[0]
                                        description  = existing_device[1]
                                        input_values = existing_device[2]
                                        input_events = existing_device[3]  
                                        commands     = existing_device[4]  

                                    except Exception as e:
                                        device_type  = device_data.device_type
                                        description  = device_data.description 
                                        input_values = device_data.input_values
                                        input_events = device_data.input_events
                                        commands     = device_data.commands 
                                 
                                        error = "Error | " + str(model) + " not founded | " + str(e)
                                                                 
                                    UPDATE_DEVICE(id, name, gateway, model, device_type, description, input_values, input_events, commands)

     
            if error != "":
                WRITE_LOGFILE_SYSTEM("ERROR", "Devices | ZigBee2MQTT | Update | " + str(error))
                SEND_EMAIL("ERROR", "Devices | ZigBee2MQTT | Update | " + str(error))                 
                return ("Devices | ZigBee2MQTT | Update | " + str(error)) 
            else:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Devices | ZigBee2MQTT | Update")
                return True
                                
            
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "Devices | ZigBee2MQTT | Update | " + str(e))  
            SEND_EMAIL("ERROR", "Devices | ZigBee2MQTT | Update | " + str(e))             
            return ("Devices | ZigBee2MQTT | Update " + str(e))
     

""" ###################### """
"""  check device setting  """
""" ###################### """
 
 
def CHECK_DEVICE_SETTING_THREAD(ieeeAddr, setting, repeats = 10): 
    Thread = threading.Thread(target=CHECK_DEVICE_SETTING_PROCESS, args=(ieeeAddr, setting, repeats, ))
    Thread.start()   

 
def CHECK_DEVICE_SETTING_PROCESS(ieeeAddr, setting, repeats):                
    device  = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
    counter = 1
                    
    # format for gui
    setting_formated = setting.replace('"', '')
    setting_formated = setting_formated.replace('{', '')
    setting_formated = setting_formated.replace('}', '')    
    setting_formated = setting_formated.replace(':', ': ')
    setting_formated = setting_formated.replace(',', ', ')      

    while counter != repeats:  
        
        if device.gateway == "mqtt":
            result = CHECK_MQTT_SETTING(device.ieeeAddr, setting)
        if device.gateway == "zigbee2mqtt":
            result = CHECK_ZIGBEE2MQTT_SETTING(device.name, setting)    
    
        # set previous setting
        if result == True:
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Device - " + device.name + " | Setting changed | " + setting_formated)  
            return True

        counter = counter + 1
        time.sleep(1)       

    # error message
    WRITE_LOGFILE_SYSTEM("ERROR", "Device - " + device.name + " | Setting not confirmed | " + setting_formated)  
    SEND_EMAIL("ERROR", "Device - " + device.name + " | Setting not confirmed | " + setting_formated)                
    return ("Device - " + device.name + " | Setting not confirmed - " + setting_formated) 
                         

def CHECK_MQTT_SETTING(ieeeAddr, setting):        
    for message in GET_MQTT_INCOMING_MESSAGES(10):
        
        # search for fitting message in incoming_messages_list
        if message[1] == "miranda/mqtt/" + ieeeAddr:  
            
            setting = setting[1:-1]
            
            # only one setting value
            if not "," in setting:    
                if setting in message[2]:
                    return True
                                                    
            # more then one setting value:
            else:
                
                list_settings = setting.split(",")
                
                for setting in list_settings:           
                    if not setting in message[2]:
                        return False    
                        
                return True
                
    return False
   

def CHECK_ZIGBEE2MQTT_SETTING(device_name, setting):
    for message in GET_MQTT_INCOMING_MESSAGES(10):

        # search for fitting message in incoming_messages_list
        if message[1] == "miranda/zigbee2mqtt/" + device_name:   
    
            setting = setting[1:-1]

            # only one setting value
            if not "," in setting:       
                if setting in message[2]:
                    return True
                                
            # more then one setting value:
            else:
                
                list_settings = setting.split(",")
                
                for setting in list_settings:        
                    if not setting in message[2]:
                        return False    
                        
                return True                    
            
    return False
   

""" ################# """
"""  check functions  """
""" ################# """
 
def CHECK_MQTT():
    MQTT_TOPIC = "miranda/mqtt/test"
    MQTT_MSG   = ""

    try:
        def on_publish(client, userdata, mid):
            print ('Message Published...')

        client = mqtt.Client()
        client.username_pw_set(username=GET_MQTT_BROKER_USERNAME(),password=GET_MQTT_BROKER_PASSWORD())          
        client.on_publish = on_publish
        client.connect(GET_MQTT_BROKER())      
        client.publish(MQTT_TOPIC,MQTT_MSG)    
        client.disconnect()

        SET_DEVICE_CONNECTION_MQTT(True)
        return True

    except Exception as e:
        SET_DEVICE_CONNECTION_MQTT(False)
        return ("MQTT | " + str(e))    


def CHECK_ZIGBEE2MQTT_AT_STARTUP():     
    counter = 1

    while counter != 5:      
        for message in GET_MQTT_INCOMING_MESSAGES(10):          
            if message[1] == "miranda/zigbee2mqtt/bridge/state":
            
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
            if message[1] == "miranda/zigbee2mqtt/bridge/log":
            
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
            if message[1] == "miranda/zigbee2mqtt/bridge/config":
            
                try:
                    data = json.loads(message[2])
                    
                    if pairing_setting == "true":
                        if data["permit_join"] == True:
                            return True

                    if pairing_setting == "false":
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
            if message[1] == "miranda/zigbee2mqtt/bridge/log":
            
                try:
                    data = json.loads(message[2])
                    
                    if data["type"] == "device_removed" and data["message"] == device_name:
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
        
        setting           = setting.replace(" ", "")
        exception_setting = device.exception_setting.replace(" ", "")
        
        if device.exception_option == "IP-Address" and exception_setting == setting:

            if ping(device.exception_value_1, timeout=1) != None:    
                return (device.name + " | Device running")
            
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
            data         = json.loads(GET_DEVICE_BY_IEEEADDR(device.exception_sensor_ieeeAddr).last_values)
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
    device_ieeeAddr = sensordata_job.device.ieeeAddr  
    
    sensor_key = sensordata_job.sensor_key
    sensor_key = sensor_key.replace(" ", "")
 
    channel = "miranda/" + device_gateway + "/" + device_ieeeAddr + "/get"
 
    heapq.heappush(mqtt_message_queue, (20, (channel, "")))        
    time.sleep(2) 
  
    for message in GET_MQTT_INCOMING_MESSAGES(5):
        
        if message[1] == "miranda/" + device_gateway + "/" + device_ieeeAddr:
                
            try:

                data     = json.loads(message[2])
                filename = sensordata_job.filename
    
                WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Devices | Sensor Data saved")  
                return True
                
            except:
                pass

    WRITE_LOGFILE_SYSTEM("ERROR", "Devices | Request Sensordata | Message not founded") 
    SEND_EMAIL("ERROR", "Devices | Request Sensordata | Message not founded")       

   
def SAVE_SENSORDATA(job_id):
    sensordata_job  = GET_SENSORDATA_JOB_BY_ID(job_id)
    device_gateway  = sensordata_job.device.gateway
    device_ieeeAddr = sensordata_job.device.ieeeAddr 
     
    sensor_key = sensordata_job.sensor_key
    sensor_key = sensor_key.replace(" ", "")
    
    for message in GET_MQTT_INCOMING_MESSAGES(10):
        
        if (message[1] == "miranda/" + device_gateway + "/" + device_ieeeAddr):
                                
            try:
                data     = json.loads(message[2])
                filename = sensordata_job.filename
    
                WRITE_SENSORDATA_FILE(filename, device_ieeeAddr, sensor_key, data[sensor_key])
                return True

            except:
                pass