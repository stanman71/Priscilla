import datetime
import time
import threading

from app                         import app
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.email           import SEND_EMAIL

process_management_queue = []


""" ################ """
"""  mqtt functions  """
""" ################ """

mqtt_message_queue          = []
mqtt_incoming_messages_list = []


def START_REFRESH_MQTT_INPUT_MESSAGES_THREAD():

	try:
		Thread = threading.Thread(target=REFRESH_MQTT_INPUT_MESSAGES_THREAD)
		Thread.start()  
		
	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "Host | Thread | Refresh MQTT Messages | " + str(e)) 
		SEND_EMAIL("ERROR", "Host | Thread | Refresh MQTT Messages | " + str(e)) 


def REFRESH_MQTT_INPUT_MESSAGES_THREAD():   
	
	while True:
	
		try:

			# get the time check value
			time_check = datetime.datetime.now() - datetime.timedelta(seconds=60)
			time_check = time_check.strftime("%Y-%m-%d %H:%M:%S")

			for message in mqtt_incoming_messages_list:

				time_message = datetime.datetime.strptime(message[0],"%Y-%m-%d %H:%M:%S")   
				time_limit   = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S")

				# remove saved message after 60 seconnds
				if time_message <= time_limit:
					mqtt_incoming_messages_list.remove(message)

		except Exception as e:
			print(e)
			
		time.sleep(1)


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


""" ################ """
"""  program status  """
""" ################ """

program_status = "None"

def SET_PROGRAM_STATUS(value):
	global program_status
	program_status = value

def GET_PROGRAM_STATUS():
    global program_status
    return program_status 


""" ############################ """
"""  zigbee2mqtt pairing status  """
""" ############################ """

zigbee2mqtt_pairing_status = "None"

def SET_ZIGBEE2MQTT_PAIRING_STATUS(value):
	global zigbee2mqtt_pairing_status
	zigbee2mqtt_pairing_status = value

def GET_ZIGBEE2MQTT_PAIRING_STATUS():
    global zigbee2mqtt_pairing_status
    return zigbee2mqtt_pairing_status 


""" ################# """
"""  system messages  """
""" ################# """

device_connetion_mqtt        = False
device_connetion_zigbee2mqtt = False

def SET_DEVICE_CONNECTION_MQTT(value):
	global device_connetion_mqtt
	device_connetion_mqtt = value

def GET_DEVICE_CONNECTION_MQTT():
    global device_connetion_mqtt
    return device_connetion_mqtt 

def SET_DEVICE_CONNECTION_ZIGBEE2MQTT(value):
	global device_connetion_zigbee2mqtt
	device_connetion_zigbee2mqtt = value	

def GET_DEVICE_CONNECTION_ZIGBEE2MQTT():
    global device_connetion_zigbee2mqtt
    return device_connetion_zigbee2mqtt	

