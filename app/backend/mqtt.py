import paho.mqtt.client as mqtt
import heapq
import threading
import json
import datetime
import time

from app import app
from app.database.models import *
from app.backend.file_management import *
from app.backend.shared_resources import process_management_queue, mqtt_incoming_messages_list
from app.backend.email import SEND_EMAIL

from ping3 import ping


""" ################################ """
""" ################################ """
"""              mqtt main           """
""" ################################ """
""" ################################ """

def GET_MQTT_INCOMING_MESSAGES(limit):

    # get the time check value
    time_check = datetime.datetime.now() - datetime.timedelta(seconds=limit)
    time_check = time_check.strftime("%Y-%m-%d %H:%M:%S")   
    
    message_list = []
    
    for message in mqtt_incoming_messages_list:
        
        time_message = datetime.datetime.strptime(message[0],"%Y-%m-%d %H:%M:%S")   
        time_limit   = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S")

        # select messages in search_time 
        if time_message > time_limit:
            message_list.append(message)
                
    return message_list

""" #################### """
""" mqtt receive message """
""" #################### """
    
    
def MQTT_RECEIVE_THREAD():

    try:
        Thread = threading.Thread(target=MQTT_RECEIVE)
        Thread.start()  
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Receive | " + str(e))  
        SEND_EMAIL("ERROR", "Thread | MQTT Receive | " + str(e))    

    
def MQTT_RECEIVE():

    global mqtt_incoming_messages_list

    def on_message(client, userdata, message): 
        
        channel = message.topic                 
        msg     = str(message.payload.decode("utf-8"))        
      
        ieeeAddr    = ""

        # get ieeeAddr and device_type
        incoming_topic   = channel
        incoming_topic   = incoming_topic.split("/")
        device_name      = incoming_topic[2]
     
        list_devices = GET_ALL_DEVICES("")
     
        try:
            for device in list_devices:
                if device.name == device_name:             
                    ieeeAddr = device.ieeeAddr
        except:
            pass        

        print("message topic: ", channel)       
        print("message received: ", msg)    
        
        # write data in logs
        WRITE_LOGFILE_DEVICES(channel, msg)
            
        # add message to the incoming message list
        mqtt_incoming_messages_list.append((str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), channel, msg))  

        # start message thread for additional processes
        if channel != "" and channel != None:   
            
            try:    
                Thread = threading.Thread(target=MQTT_MESSAGE, args=(channel, msg, ieeeAddr, ))
                Thread.start()   
            except Exception as e:
                    WRITE_LOGFILE_SYSTEM("ERROR", "Thread | MQTT Message | " + str(e)) 
                    SEND_EMAIL("ERROR", "Thread | MQTT Message | " + str(e))                    
                    print(e)


    def on_connect(client, userdata, flags, rc):   
        if rc != 0:
            print("ERROR: MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | Bad Connection | Returned Code = " + str(rc)) 
        
            WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | Bad Connection | Returned Code = " + str(rc))         
        
        else:
            client.subscribe("miranda/#")
  
            print("MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | Connected") 
            WRITE_LOGFILE_SYSTEM("EVENT", "MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | Connected")
                
 
    client = mqtt.Client()
    client.username_pw_set(username=GET_MQTT_BROKER_SETTINGS().user,password=GET_MQTT_BROKER_SETTINGS().password)
    client.on_connect = on_connect
    client.on_message = on_message
     
    try:
        client.connect(GET_MQTT_BROKER_SETTINGS().broker)
        client.loop_forever()

    except Exception as e:
        print("ERROR: MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | " + str(e))
        
        WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | " + str(e))
        SEND_EMAIL("ERROR", "MQTT | Broker - " + str(GET_MQTT_BROKER_SETTINGS().broker) + " | " + str(e))


""" ############# """
"""  mqtt message """
""" ############# """

def MQTT_MESSAGE(channel, msg, ieeeAddr):
    
    channel = channel.split("/")

    # filter incoming messages
    try:
        if channel[2] == "devices":
            return
        if channel[2] == "test":    
            return
        if channel[2] == "log": 
            return          
        if channel[3] == "set":
            return  

    except:    
        if ieeeAddr != "":
            
            # save last values and last contact 
            SET_DEVICE_LAST_VALUES(ieeeAddr, msg)


""" #################### """
""" mqtt publish message """
""" #################### """


def MQTT_PUBLISH(MQTT_TOPIC, MQTT_MSG):

    try:
        def on_publish(client, userdata, mid):
            print ('Message Published...')

        client = mqtt.Client()
        client.username_pw_set(username=GET_MQTT_BROKER_SETTINGS().user,password=GET_MQTT_BROKER_SETTINGS().password)          
        client.on_publish = on_publish
        client.connect(GET_MQTT_BROKER_SETTINGS().broker)      
        client.publish(MQTT_TOPIC,MQTT_MSG)
        
        client.disconnect()

        return 

    except Exception as e:
        print("ERROR: MQTT Publish | " + str(e))
        return ("Fehler MQTT >>> " + str(e))


""" ################################ """
""" ################################ """
"""           mqtt functions         """
""" ################################ """
""" ################################ """


""" ################### """
"""    update devices   """
""" ################### """


def UPDATE_DEVICES():
   
    message_founded = False

    MQTT_PUBLISH("miranda/mqtt/devices", "")  
    time.sleep(3)

    try:
        for message in GET_MQTT_INCOMING_MESSAGES(5):
            
            if message[1] == "miranda/mqtt/log":

                message_founded = True   

                message = str(message[2])
                
                data = json.loads(message)
                
                name        = data['ieeeAddr']
                ieeeAddr    = data['ieeeAddr']
                model       = data['model']
                device_type = data['device_type']

                try:
                    inputs  = data['inputs']
                    inputs  = ','.join(inputs)   
                    inputs  = inputs.replace("'", '"')
                except:
                    inputs  = ""

                # add new device
                if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):
                    ADD_DEVICE(name, ieeeAddr, model, device_type, inputs)
                    
                # update existing device
                else:
                    id   = GET_DEVICE_BY_IEEEADDR(ieeeAddr).id
                    name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
                                    
                    UPDATE_DEVICE(id, name, model, device_type, inputs)
                    SET_DEVICE_LAST_CONTACT(ieeeAddr)
                    
                # update sensor values 
                MQTT_PUBLISH("miranda/mqtt/" + ieeeAddr + "/get", "")  


        if message_founded == True:
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Update Devices")
            return "Success"
            
        else:    
            WRITE_LOGFILE_SYSTEM("WARNING", "Update Devices | No Message founded")
            SEND_EMAIL("WARNING", "Update Devices | No Message founded")             
            return "Update Devices | Kein Message gefunden"
        
    
    except Exception as e:
        if str(e) == "string index out of range":
            WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | No connection") 
            SEND_EMAIL("ERROR", "MQTT | No connection")                 
            return ("MQTT | No connection")     
         

""" #################### """
"""  mqtt check setting  """
""" #################### """
 
 
def CHECK_MQTT_SETTING_THREAD(ieeeAddr, setting, delay = 1, limit = 15): 
 
    Thread = threading.Thread(target=CHECK_MQTT_SETTING_PROCESS, args=(ieeeAddr, setting, delay, limit, ))
    Thread.start()   

 
def CHECK_MQTT_SETTING_PROCESS(ieeeAddr, setting, delay, limit): 
                      
    device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
                    
    # check setting 1 try
    time.sleep(delay)                             
    
    result = CHECK_MQTT_SETTING(ieeeAddr, setting, limit)
    
    # format for gui
    setting_formated = setting.replace('"', '')
    setting_formated = setting_formated.replace('{', '')
    setting_formated = setting_formated.replace('}', '')    
    setting_formated = setting_formated.replace(':', ': ')
    setting_formated = setting_formated.replace(',', ', ')      
    
    # set previous setting
    if result == True:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "MQTT | Device - " + device.name + " | Setting changed | " + setting_formated)  
    
    else:
        # check setting 2 try
        time.sleep(delay)                             
        result = CHECK_MQTT_SETTING(ieeeAddr, setting, limit)
        
        # set previous setting
        if result == True:
            WRITE_LOGFILE_SYSTEM("SUCCESS", "MQTT | Device - " + device.name + " | Setting changed | " + setting_formated)      
            
        else:
            # check setting 3 try
            time.sleep(delay)                             
            result = CHECK_MQTT_SETTING(ieeeAddr, setting, limit)
             
            # set previous setting
            if result == True:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "MQTT | Device - " + device.name + " | Setting changed | " + setting_formated)          
                
            # error message
            else:
                WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | Device - " + device.name + " | Setting not confirmed | " + setting_formated)  
                SEND_EMAIL("ERROR", "MQTT | Device - " + device.name + " | Setting not confirmed | " + setting_formated)                
                return ("MQTT | Device - " + device.name + " | Setting not confirmed - " + setting_formated) 
                
    return ""
                    

def CHECK_MQTT_SETTING(ieeeAddr, setting, limit):
            
    for message in GET_MQTT_INCOMING_MESSAGES(limit):
        
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