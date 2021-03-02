from app                         import app
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.database_models import GET_ALL_DEVICES
from app.backend.email           import SEND_EMAIL

import datetime
import time
import threading
import heapq
import json

process_management_queue    = []
mqtt_message_queue          = []


""" ################ """
"""  mqtt functions  """
""" ################ """

mqtt_incoming_messages_list = []

def START_REFRESH_MQTT_INPUT_MESSAGES_THREAD():
	try:
		Thread = threading.Thread(target=REFRESH_MQTT_INPUT_MESSAGES_THREAD)
		Thread.start()  
		
	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Refresh MQTT Messages | " + str(e)) 
		SEND_EMAIL("ERROR", "System | Thread | Refresh MQTT Messages | " + str(e)) 


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

		except:
			pass
			
		time.sleep(1)


def GET_MQTT_INCOMING_MESSAGES(limit):

    # get the time check value
    time_check = datetime.datetime.now() - datetime.timedelta(seconds=limit)
    time_check = time_check.strftime("%Y-%m-%d %H:%M:%S")   
    
    message_list = []
    
    for message in mqtt_incoming_messages_list:     
        time_message = datetime.datetime.strptime(message[0],"%Y-%m-%d %H:%M:%S")   
        time_limit   = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S")

        # select messages in search_time limit
        if time_message > time_limit:
            message_list.append(message)
                
    return message_list


""" ################ """
"""  program status  """
""" ################ """

program_thread_status_1 = ["None","","",""]
program_thread_status_2 = ["None","","",""]
program_thread_status_3 = ["None","","",""]
program_thread_status_4 = ["None","","",""]
program_thread_status_5 = ["None","","",""]
program_thread_status_6 = ["None","","",""]
program_thread_status_7 = ["None","","",""]
program_thread_status_8 = ["None","","",""]
program_thread_status_9 = ["None","","",""]

def GET_PROGRAM_THREAD_STATUS_1():
    global program_thread_status_1
    return program_thread_status_1 

def SET_PROGRAM_THREAD_STATUS_1(program_name, line, lines_total, command):
	global program_thread_status_1
	program_thread_status_1 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_2():
    global program_thread_status_2
    return program_thread_status_2 

def SET_PROGRAM_THREAD_STATUS_2(program_name, line, lines_total, command):
	global program_thread_status_2
	program_thread_status_2 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_3():
    global program_thread_status_3
    return program_thread_status_3 

def SET_PROGRAM_THREAD_STATUS_3(program_name, line, lines_total, command):
	global program_thread_status_3
	program_thread_status_3 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_4():
    global program_thread_status_4
    return program_thread_status_4 

def SET_PROGRAM_THREAD_STATUS_4(program_name, line, lines_total, command):
	global program_thread_status_4
	program_thread_status_4 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_5():
    global program_thread_status_5
    return program_thread_status_5 

def SET_PROGRAM_THREAD_STATUS_5(program_name, line, lines_total, command):
	global program_thread_status_5
	program_thread_status_5 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_6():
    global program_thread_status_6
    return program_thread_status_6 

def SET_PROGRAM_THREAD_STATUS_6(program_name, line, lines_total, command):
	global program_thread_status_6
	program_thread_status_6 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_7():
    global program_thread_status_7
    return program_thread_status_7 

def SET_PROGRAM_THREAD_STATUS_7(program_name, line, lines_total, command):
	global program_thread_status_7
	program_thread_status_7 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_8():
    global program_thread_status_8
    return program_thread_status_8 

def SET_PROGRAM_THREAD_STATUS_8(program_name, line, lines_total, command):
	global program_thread_status_8
	program_thread_status_8 = [program_name, line, lines_total, command]

def GET_PROGRAM_THREAD_STATUS_9():
    global program_thread_status_9
    return program_thread_status_9 

def SET_PROGRAM_THREAD_STATUS_9(program_name, line, lines_total, command):
	global program_thread_status_9
	program_thread_status_9 = [program_name, line, lines_total, command]


""" ################# """
"""  system messages  """
""" ################# """

mqtt_connetion_status        = False
zigbee2mqtt_connetion_status = False

def GET_MQTT_CONNECTION_STATUS():
    global mqtt_connetion_status
    return mqtt_connetion_status 

def SET_MQTT_CONNECTION_STATUS(value):
	global mqtt_connetion_status
	mqtt_connetion_status = value

def GET_ZIGBEE2MQTT_CONNECTION_STATUS():
    global zigbee2mqtt_connetion_status
    return zigbee2mqtt_connetion_status	

def SET_ZIGBEE2MQTT_CONNECTION_STATUS(value):
	global zigbee2mqtt_connetion_status
	zigbee2mqtt_connetion_status = value	


""" ###################### """
"""  zigbee device update  """
""" ###################### """

zigbee_device_update_status = "No Device Update available"

def GET_ZIGBEE_DEVICE_UPDATE_STATUS():
    global zigbee_device_update_status
    return zigbee_device_update_status 

def SET_ZIGBEE_DEVICE_UPDATE_STATUS(status):
	global zigbee_device_update_status
	zigbee_device_update_status = status


""" ##################### """
"""  zigbee2mqtt pairing  """
""" ##################### """

zigbee2mqtt_pairing_setting  = "None"
zigbee2mqtt_pairing_status   = "None"
timer_disable_zigbee_pairing = "None"

def GET_ZIGBEE2MQTT_PAIRING_SETTING():
    global zigbee2mqtt_pairing_setting
    return zigbee2mqtt_pairing_setting 

def SET_ZIGBEE2MQTT_PAIRING_SETTING(setting):
	global zigbee2mqtt_pairing_setting
	zigbee2mqtt_pairing_setting = setting

def GET_ZIGBEE2MQTT_PAIRING_STATUS():
    global zigbee2mqtt_pairing_status
    return zigbee2mqtt_pairing_status 

def SET_ZIGBEE2MQTT_PAIRING_STATUS(value):
	global zigbee2mqtt_pairing_status
	zigbee2mqtt_pairing_status = value


def SET_ZIGBEE_PAIRING_TIMER(setting):
	global timer_disable_zigbee_pairing
	if setting == "True":
		timer_disable_zigbee_pairing = datetime.datetime.now() + datetime.timedelta(minutes=30)
	if setting == "False":
		timer_disable_zigbee_pairing = "None"


def START_DISABLE_ZIGBEE_PAIRING_THREAD():
	try:
		Thread = threading.Thread(target=DISABLE_ZIGBEE_PAIRING_THREAD)
		Thread.start()    
		
	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Disable Zigbee Pairing | " + str(e)) 


# disable pairing after 30 minutes automatically
def DISABLE_ZIGBEE_PAIRING_THREAD():
	global timer_disable_zigbee_pairing
	global mqtt_message_queue
	
	while True:

		# check mqtt connection
		if GET_MQTT_CONNECTION_STATUS() == True:  

			try:

				if datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") == timer_disable_zigbee_pairing.strftime("%Y-%m-%d %H:%M:%S"):

					timer_disable_zigbee_pairing = "None"
					zigbee_pairing_disabled      = False
					counter                      = 1

					heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))   

					# check zigbee successfully disabled ? 
					while counter != 10:       
						for message in GET_MQTT_INCOMING_MESSAGES(15):
							if message[1] == "smarthome/zigbee2mqtt/bridge/config":
							
								try:
									data = json.loads(message[2])
									
									if data["permit_join"] == False:
										zigbee_pairing_disabled = True
										break
										
								except:
									pass

						counter = counter + 1
						time.sleep(1)

					if zigbee_pairing_disabled == True:
						WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
						SET_ZIGBEE2MQTT_PAIRING_SETTING("False")										
						SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled") 

					else:
						WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
						SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
						SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")	
										
			except:
				pass

			time.sleep(1)

		else:
			WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | No MQTT connection") 
			SET_ZIGBEE2MQTT_PAIRING_STATUS("No MQTT connection")     


""" ################# """
"""   bad connection  """
""" ################# """

bad_connection_list = []

def START_BAD_CONNECTION_THREAD():
	try:
		Thread = threading.Thread(target=BAD_CONNECTION_THREAD)
		Thread.start()  
		
	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Bad Connection | " + str(e)) 
		SEND_EMAIL("ERROR", "System | Thread | Bad Connection | " + str(e)) 


def BAD_CONNECTION_THREAD():   
	while True:
	
		# delete entries after 6 hours

		try:
			# get the time check value
			time_check = datetime.datetime.now() - datetime.timedelta(hours=6)
			time_check = time_check.strftime("%Y-%m-%d %H:%M:%S")

			for entry in bad_connection_list:

				time_entry = datetime.datetime.strptime(entry[0],"%Y-%m-%d %H:%M:%S")   
				time_limit = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S")

				# remove saved entries after 6 hours
				if time_entry <= time_limit:
					bad_connection_list.remove(entry)

		except:
			pass

		# send bad linkquality message of devices if they have 3 and more entries
	
		try:
			for device in GET_ALL_DEVICES(""):

				counter = 0

				# count bad quality entries of the device
				for entry in bad_connection_list:
					if device.ieeeAddr == entry[1]:
						counter = counter + 1

				if counter >= 3:
					WRITE_LOGFILE_SYSTEM("WARNING", "Network | Device | " + device.name + " | Bad Connection")

					# remove entries of this device
					for entry in bad_connection_list:
						if device.ieeeAddr == entry[1]:
							bad_connection_list.remove(entry)					

		except:
			pass
			
		time.sleep(60)