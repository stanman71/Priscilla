import sys
import signal
import heapq
import time
import yaml
import os

from speechcontrol.snowboy                      import snowboydetect
from speechcontrol.snowboy                      import snowboydecoder
from speechcontrol.microphone_led_control       import MICROPHONE_LED_CONTROL
from speechcontrol.speech_recognition_provider  import SPEECH_RECOGNITION_PROVIDER
from shared_resources                           import *


interrupted = False

def signal_handler(signal, frame):
   global interrupted
   interrupted = True

def interrupt_callback():
   global interrupted
   return interrupted


def GET_ALL_HOTWORD_FILES():
    file_list_temp = []
    file_list = []

    for files in os.walk(GET_PATH() + "/speechcontrol/snowboy/resources/"):  
        file_list_temp.append(files)

    if file_list_temp == []:
        return ""  
    else:
        file_list_temp = file_list_temp[0][2]
        for file in file_list_temp:        
            if file != "common.res":
                file_list.append(file)
                
        return file_list


""" ############# """
"""  snow thread  """
""" ############# """

def SNOWBOY_THREAD():

    signal.signal(signal.SIGINT, signal_handler)

    hotword_file = GET_SNOWBOY_HOTWORD()

    # check hotword files exist
    if hotword_file in GET_ALL_HOTWORD_FILES():
   
        # voice models here:
        models = GET_PATH() + '/speechcontrol/snowboy/resources/' +  GET_SNOWBOY_HOTWORD()
      
        sensitivity_value = int(GET_SNOWBOY_SENSITIVITY()) / 100

        # modify sensitivity for better detection / accuracy
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity_value)  
      
        def detect_callback():
            detector.terminate()
            MICROPHONE_LED_CONTROL(GET_MODEL(), "on")
     
            speech_recognition_answer = SPEECH_RECOGNITION_PROVIDER(GET_SNOWBOY_TIMEOUT())
     
            if speech_recognition_answer != None and speech_recognition_answer != "":
                
                if "could not" in speech_recognition_answer or "Could not" in speech_recognition_answer:     
                    pass
                    
                else:    
                    MQTT_PUBLISH("miranda/mqtt/" + GET_IEEEADDR(), '{"speech_recognition_answer":"' + speech_recognition_answer + '"}')


            MICROPHONE_LED_CONTROL(GET_MODEL(), "off")
            
            # pause snowboy
            set_led = True
            while GET_SNOWBOY_PAUSE() == "True":

                if set_led:
                    MICROPHONE_LED_CONTROL(GET_MODEL(), "pause")
                    set_led = False
                time.sleep(1)
                
            MICROPHONE_LED_CONTROL(GET_MODEL(), "off") 

            detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)


        print("Speechcontrol | Started") 

        # pause snowboy
        set_led = True
        while GET_SNOWBOY_PAUSE() == "True":

            if set_led:
                MICROPHONE_LED_CONTROL(GET_MODEL(), "pause")
                set_led = False
            time.sleep(1)
            
        MICROPHONE_LED_CONTROL(GET_MODEL(), "off") 

        # main loop
        detector.start(detected_callback=detect_callback,
                        interrupt_check=interrupt_callback,
                        sleep_time=0.03)

        detector.terminate()

    else:
        print("ERROR", "Speechcontrol | Snowboy Hotword - " + hotword_file + " | Not founded")
