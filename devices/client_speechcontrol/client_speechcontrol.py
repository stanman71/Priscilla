import paho.mqtt.client as mqtt
import json
import os
import time
import netifaces

from speechcontrol.microphone_led_control import MICROPHONE_LED_CONTROL
from speechcontrol.snowboy.snowboy        import SNOWBOY_THREAD
from shared_resources                     import *


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


""" ############### """
"""  speechcontrol  """
""" ############### """

# deactivate pixel_ring
MICROPHONE_LED_CONTROL(GET_MODEL(), "off") 

try:
    print("###### Start SPEECHCONTROL ######")
    SNOWBOY_THREAD()       

except Exception as e:
    if "signal only works in main thread" not in str(e): 
        print("ERROR: SnowBoy | " + str(e))


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
        msg     = '{"ieeeAddr":"' + GET_IEEEADDR() + '","model":"' + GET_MODEL() + '","device_type":"client_speechcontrol","description":"MQTT Client Speechcontrol","input_values":[],"input_events":[],"commands":[]}'

        MQTT_PUBLISH(channel, msg)


    # ###
    # set
    # ###

    if channel == "miranda/mqtt/" + GET_IEEEADDR() + "/set":

        data = json.loads(msg)   

        # change snowboy pause
        try:           
            UPDATE_SNOWBOY_PAUSE(data["snowboy_pause"])
            MQTT_PUBLISH("miranda/mqtt/" + GET_IEEEADDR(), '{"snowboy_pause":"' + GET_SNOWBOY_PAUSE() + '"}')

        except Exception as e:
            print("Error | " + str(e))                   
            MQTT_PUBLISH("miranda/mqtt/" + GET_IEEEADDR(), str(e))


    # ###
    # get
    # ###

    if channel == "miranda/mqtt/" + GET_IEEEADDR() + "/get":   
        MQTT_PUBLISH("miranda/mqtt/" + GET_IEEEADDR(), '{"snowboy_pause":"' + GET_SNOWBOY_PAUSE() + '"}')


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
