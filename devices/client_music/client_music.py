#!/usr/bin/python3

import paho.mqtt.client as mqtt
import json
import os
import time
import yaml
import random
import netifaces


""" ###### """
"""  path  """
""" ###### """
                           
PATH = "/home/pi/python/"


""" ############ """
""" get wlan_ip  """
""" ############ """

time.sleep(10)
counter = 1

try:
    wlan_ip_address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]["addr"]
except:
    wlan_ip_address = ""

# repeat process
while wlan_ip_address == "" or counter != 5:
    time.sleep(5)
    counter = counter + 1

    try:
        wlan_ip_address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]["addr"]
        break
    except:
        wlan_ip_address = ""


""" ############# """
"""  config file  """
""" ############# """

try:
    # open config file
    with open(PATH + "/config.yaml", "r") as file_config:
        config = yaml.load(file_config, Loader=yaml.SafeLoader)
        file_config.close()

except Exception as e:
    print("##### ERROR: config file not founded #####")


# ###############
# device ieeeAddr
# ###############

if str(config['general']['ieeeAddr']) == "None":

    # generate new ieeeAddr
    try:
        with open(PATH + "/config.yaml") as file_config:
            upload_config = yaml.load(file_config, Loader=yaml.SafeLoader)
                        
        device_ieeeAddr = "0x" + str(random.randrange(1000000, 9999999))

        upload_config['general']['ieeeAddr'] = device_ieeeAddr

        with open(PATH + "/config.yaml", 'w') as file_config:
            yaml.dump(upload_config, file_config)
            
    except Exception as e:
        print("ERROR: " + str(e))

else:
    device_ieeeAddr = str(config['general']['ieeeAddr'])


# ###############
# current setting
# ###############

def GET_MODEL():
    try:
        return str(config['general']['model'])
    except:
        return ""   

def GET_SOUNDCARD_NUMBER():
    try:
        return str(config['general']['soundcard_number'])
    except:
        return ""   


current_interface = str(config['general']['current_interface'])
current_volume    = str(config['general']['current_volume'])

if current_interface == "spotify":
    try:
        os.system("sudo systemctl start raspotify")
        print("Raspotify | Started")
        time.sleep(2)

    except Exception as e:
        print("Raspotify | Error | " + str(e))        
        MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))

if current_interface == "multiroom":
    try:
        os.system("sudo systemctl start squeezelite")
        print("Squeezelite | Started")        
        time.sleep(2)

    except Exception as e:
        print("Squeezelite | Error | " + str(e))             
        MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))

if current_volume != "":
    try:
        os.system("amixer -c " + GET_SOUNDCARD_NUMBER() + " cset numid=1 " + current_volume)
        print("AlsaMixer | Volume adjusted")        
        time.sleep(2)

    except Exception as e:
        print("AlsaMixer | Error | " + str(e))             
        MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))


def UPDATE_CURRENT_INTERFACE(interface):
    global current_interface

    try:
        with open(PATH + "/config.yaml") as file_config:
            upload_config = yaml.load(file_config, Loader=yaml.SafeLoader)

        upload_config['general']['current_interface'] = interface  

        with open(PATH + "/config.yaml", 'w') as file_config:
            yaml.dump(upload_config, file_config)

        current_interface = interface
            
    except Exception as e:
        return ("ERROR: " + str(e))


def UPDATE_CURRENT_VOLUME(volume):
    global current_volume

    try:
        with open(PATH + "/config.yaml") as file_config:
            upload_config = yaml.load(file_config, Loader=yaml.SafeLoader)

        upload_config['general']['current_volume'] = volume  

        with open(PATH + "/config.yaml", 'w') as file_config:
            yaml.dump(upload_config, file_config)

        current_volume = volume
            
    except Exception as e:
        return ("ERROR: " + str(e))


# ###########
# mqtt broker
# ###########

def GET_MQTT_BROKER():
    try:
        return str(config['mqtt']['broker'])
    except:
        return "localhost"   


def GET_MQTT_BROKER_USERNAME():
    try:
        return str(config['mqtt']['username'])
    except:
        return ""   


def GET_MQTT_BROKER_PASSWORD():
    try:
        return str(config['mqtt']['password'])
    except:
        return ""   
        

""" ###################### """
"""  mqtt receive message  """
""" ###################### """
    
def on_message(client, userdata, message): 
    channel = message.topic                 
    msg     = str(message.payload.decode("utf-8"))     

    print("### " + channel)
    print("### " + msg) 


    # #######
    # devices
    # #######

    if channel == "miranda/mqtt/devices":
        channel = "miranda/mqtt/log"
        msg     = '{"ieeeAddr":"' + device_ieeeAddr + '","model":"' + GET_MODEL() + '","device_type":"client_music","description":"MQTT Client Music","input_values":[],"input_events":[],"commands":[]}'

        MQTT_PUBLISH(channel, msg)


    # ###
    # set
    # ###

    if channel == "miranda/mqtt/" + device_ieeeAddr + "/set":

        data = json.loads(msg)   

        # interface spotify

        if data["interface"] == "spotify" and current_interface != "spotify":

            try:
                os.system("sudo systemctl stop squeezelite")
                print("Squeezelite | Stopped")                   
                time.sleep(2)
                os.system("sudo systemctl start raspotify")
                print("Raspotify | Started")                    
                time.sleep(2)

                try:
                    # volume changed ?
                    if str(data["volume"]) != str(current_volume):
                        try:
                            os.system("amixer -c " + GET_SOUNDCARD_NUMBER() + " cset numid=1 " + str(data["volume"]))
                            print("AlsaMixer | Volume adjusted")                    
                            time.sleep(2)
                            UPDATE_CURRENT_VOLUME(str(data["volume"]))

                        except Exception as e:
                            print("AlsaMixer | Error | " + str(e))                     
                            MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))

                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"spotify","volume":' + str(data["volume"]) + ',"wlan_ip_address":"' + wlan_ip_address + '"}')

                except:
                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"spotify","wlan_ip_address":"' + wlan_ip_address + '"}')

                UPDATE_CURRENT_INTERFACE("spotify")

            except Exception as e:
                print("Raspotify | Error | " + str(e))                   
                MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))


        # interface multiroom

        if data["interface"] == "multiroom" and current_interface != "multiroom":
            
            try:
                os.system("sudo systemctl stop raspotify")
                print("Raspotify | Stopped")                    
                time.sleep(2)
                os.system("sudo systemctl start squeezelite")
                print("Squeezelite | Started")                    
                time.sleep(2)

                try:
                    # volume changed ?
                    if str(data["volume"]) != str(current_volume):
                        try:
                            os.system("amixer -c " + GET_SOUNDCARD_NUMBER() + " cset numid=1 " + str(data["volume"]))
                            print("AlsaMixer | Volume adjusted")                    
                            time.sleep(2)
                            UPDATE_CURRENT_VOLUME(str(data["volume"]))

                        except Exception as e:
                            print("AlsaMixer | Error | " + str(e))                     
                            MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))

                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"multiroom","volume":' + str(data["volume"]) + ',"wlan_ip_address":"' + wlan_ip_address + '"}')

                except:
                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"multiroom","wlan_ip_address":"' + wlan_ip_address + '"}')      
                    
                UPDATE_CURRENT_INTERFACE("multiroom")

            except Exception as e:
                print("Squeezelite | Error | " + str(e))                     
                MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))


        # reset interface

        try:
            if str(data["interface"]) == "restart":
                try:

                    if current_interface == "spotify":
                        os.system("sudo systemctl stop raspotify")
                        print("Raspotify | Stopped")                    
                        time.sleep(2)
                        os.system("sudo systemctl start raspotify")
                        print("Raspotify | Started")                    
                        time.sleep(2)

                    if current_interface == "multiroom":
                        os.system("sudo systemctl stop squeezelite")
                        print("Squeezelite | Stopped")                    
                        time.sleep(2)
                        os.system("sudo systemctl start squeezelite")
                        print("Squeezelite | Started")                    
                        time.sleep(2)

                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"' + current_interface + '","volume":' + current_volume + ',"wlan_ip_address":"' + wlan_ip_address + '"}')

                except Exception as e:
                    print("Reset | Error | " + str(e))                     
                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))
        
        except:
            pass     


        # volume

        try:
            if str(data["volume"]) != str(current_volume):
                try:
                    os.system("amixer -c " + GET_SOUNDCARD_NUMBER() + " cset numid=1 " + str(data["volume"]))
                    print("AlsaMixer | Volume adjusted")                    
                    time.sleep(2)
                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"' + data["interface"] + '","volume":' + str(data["volume"]) + ',"wlan_ip_address":"' + wlan_ip_address + '"}')
                    UPDATE_CURRENT_VOLUME(str(data["volume"]))

                except Exception as e:
                    print("AlsaMixer | Error | " + str(e))                     
                    MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, str(e))
        
        except:
            pass   


    # ###
    # get
    # ###

    if channel == "miranda/mqtt/" + device_ieeeAddr + "/get":   
        MQTT_PUBLISH("miranda/mqtt/" + device_ieeeAddr, '{"interface":"' + current_interface + '","volume":' + current_volume + ',"wlan_ip_address":"' + wlan_ip_address + '"}')


""" ###################### """
"""  mqtt publish message  """
""" ###################### """

def MQTT_PUBLISH(channel, msg):

    def on_publish(client, userdata, mid):
        print ('Message Published...')

    client = mqtt.Client()
    client.username_pw_set(username=GET_MQTT_BROKER_USERNAME(),password=GET_MQTT_BROKER_PASSWORD())          
    client.on_publish = on_publish
    client.connect(GET_MQTT_BROKER())      
    client.publish(channel,msg)        
    client.disconnect()


""" ################# """
"""  mqtt connection  """
""" ################# """

def on_connect(client, userdata, flags, rc):   
    if rc != 0:
        print("ERROR: MQTT | Broker - " + GET_MQTT_BROKER() + " | Bad Connection | Returned Code = " + str(rc)) 

    else:
        client.subscribe("miranda/#")
        print("MQTT | Broker - " + GET_MQTT_BROKER() + " | Connected") 


client = mqtt.Client()
client.username_pw_set(username=GET_MQTT_BROKER_USERNAME(),password=GET_MQTT_BROKER_PASSWORD())
client.on_connect = on_connect
client.on_message = on_message
    
try:
    client.connect(GET_MQTT_BROKER(), 1883, 60)
    client.loop_forever()
    
except Exception as e:
    print("ERROR: MQTT | Broker - " + GET_MQTT_BROKER() + " | " + str(e))
