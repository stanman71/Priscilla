import paho.mqtt.client as mqtt
import json
import os
import time
import yaml
import random


""" ###### """
"""  path  """
""" ###### """
                           
PATH = "/home/pi/python"

def GET_PATH():
    return PATH

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

def GET_IEEEADDR():
    return device_ieeeAddr   


def GET_MODEL():
    try:
        return str(config['general']['model'])
    except:
        return ""   


def GET_SNOWBOY_HOTWORD():
    try:
        return str(config['speechcontrol']['snowboy_hotword'])
    except:
        return ""   


def GET_SNOWBOY_SENSITIVITY():
    try:
        return str(config['speechcontrol']['snowboy_sensitivity'])
    except:
        return ""   


def GET_SNOWBOY_TIMEOUT():
    try:
        return str(config['speechcontrol']['snowboy_timeout'])
    except:
        return ""   


snowboy_pause = str(config['speechcontrol']['snowboy_pause'])

def GET_SNOWBOY_PAUSE():
    return snowboy_pause  


def GET_SPEECH_RECOGNITION_PROVIDER():
    try:
        return str(config['speechcontrol']['speech_recognition_provider'])
    except:
        return ""   


def GET_SPEECH_RECOGNITION_PROVIDER_USERNAME():
    try:
        return str(config['speechcontrol']['speech_recognition_provider_username'])
    except:
        return ""   


def GET_SPEECH_RECOGNITION_PROVIDER_KEY():
    try:
        return str(config['speechcontrol']['speech_recognition_provider_key'])
    except:
        return ""   


def UPDATE_SNOWBOY_PAUSE(command):
    global snowboy_pause

    try:
        with open(PATH + "/config.yaml") as file_config:
            upload_config = yaml.load(file_config, Loader=yaml.SafeLoader)

        upload_config['speechcontrol']['snowboy_pause'] = command  

        with open(PATH + "/config.yaml", 'w') as file_config:
            yaml.dump(upload_config, file_config)

        snowboy_pause = command
            
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