from flask          import send_from_directory
from werkzeug.utils import secure_filename

from app import app

import datetime
import os
import shutil
import csv
import json
import pandas as pd
import yaml
import time
import threading

sensordata_messages_list = []


""" ###### """
"""  path  """
""" ###### """

def GET_PATH():

    # windows
    if os.name == "nt":                 
        return(os.path.abspath("")) 

    # linux
    else:                               
        return("/home/pi/smarthome/")


""" ###### """
"""  logs  """
""" ###### """

def CREATE_LOGFILE(filename):

    try:
        # create csv file
        file = GET_PATH() + "/data/logs/" + filename + ".csv"
        
        with open(file, 'w', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)    

            if filename == "log_devices":                   
                filewriter.writerow(['Timestamp','Channel','Message'])              
            if filename == "log_system":                   
                filewriter.writerow(['Timestamp','Type','Description'])                
            
            csvfile.close()

        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/" + filename + ".csv | created")   
        return True   
           
    except Exception as e:
        if filename != "log_system":
            WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/logs/" + filename + ".csv | " + str(e))  
        return(e)

        
def RESET_LOGFILE(filename):

    # remove old log file
    if os.path.isfile(GET_PATH() + "/data/logs/" + filename + "_old" + ".csv"):
        os.remove (GET_PATH() + "/data/logs/" + filename + "_old" + ".csv")

        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/" + filename + "_old" + ".csv | deleted")

    # rename current log file      
    if os.path.isfile(GET_PATH() + "/data/logs/" + filename + ".csv"):
        os.rename (GET_PATH() + "/data/logs/" + filename + ".csv", GET_PATH() + "/data/logs/" + "_old" + filename + ".csv")
 
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/" + filename + ".csv | renamed")

    result = CREATE_LOGFILE(filename)
    
    if result:
        return True
    else:
        return result
        

def WRITE_LOGFILE_DEVICES(channel, msg):
    
    # create file if not exist
    if os.path.isfile(GET_PATH() + "/data/logs/log_devices.csv") is False:
        CREATE_LOGFILE("log_devices")
        
    try: 
        # open csv file
        file = GET_PATH() + "/data/logs/log_devices.csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                                        
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), str(channel), msg ])
            csvfile.close()
            return True
       
    except Exception as e:
        return(e)


def WRITE_LOGFILE_SYSTEM(log_type, description):

    # create file if not exist
    if os.path.isfile(GET_PATH() + "/data/logs/log_system.csv") is False:
        CREATE_LOGFILE("log_system")

    try:
        # open csv file
        file = GET_PATH() + "/data/logs/log_system.csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)   
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), log_type, description])
            csvfile.close()
            return True
        
    except Exception as e:
        return(e)


def GET_LOGFILE_SYSTEM(selected_log_types, search, rows):   
    
    try:
        # open csv file
        file = GET_PATH() + "/data/logs/log_system.csv"
        
        with open(file, 'r', newline='', encoding='utf-8') as csvfile:
            rowReader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            data = [row for row in rowReader] 
            csvfile.close()
            
            headers = data.pop(0)                 # get headers and remove from data
            data_reversed = data[::-1]            # reverse the data

            # get the selected log entries
            data_reversed_filtered = []

            for element in data_reversed:

                try:
                    if element[1] in selected_log_types:

                        if search == "":
                            data_reversed_filtered.append(element)

                        # search for keywords
                        else:                       
                            search_list = search.split(" ")
                            search_list = map(str.lower, search_list)

                            if all(word in element[2].lower() for word in search_list):
                                data_reversed_filtered.append(element)
                            
                except:
                    pass

            return data_reversed_filtered[0:rows]
            
    except Exception as e:
        RESET_LOGFILE("log_system")
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/logs/log_system.csv | " + str(e)) 


""" ###################### """
"""  linux network config  """
""" ###################### """

def UPDATE_NETWORK_SETTINGS_LINUX(dhcp, ip_address, gateway):
    
    try:
        file = "/etc/network/interfaces"
        with open(file, 'w', encoding='utf-8') as conf_file:

            conf_file.write("source /etc/network/interfaces.d/*\n")
            conf_file.write("# Network is managed by Network manager\n")
            conf_file.write("auto lo\n")
            conf_file.write("iface lo inet loopback\n")
    
            if dhcp != "True":

                conf_file.write("\n")
                conf_file.write("auto eth0\n")
                conf_file.write("iface eth0 inet static\n")
                conf_file.write("  address " + str(ip_address) + "\n")
                conf_file.write("  netmask 255.255.255.0\n")        
                conf_file.write("  gateway " + str(gateway) + "\n")    

            conf_file.close()
            return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /etc/network/interfaces | " + str(e))  


""" ################# """
"""  backup database  """
""" ################# """

def GET_ALL_BACKUP_FILES():

    file_list = []
    for files in os.walk(GET_PATH() + '/data/backup_database/'):  
        file_list.append(files)

    if file_list == []:
        return "No Files found"
    else:
        file_list = file_list[0][2]
        file_list = sorted(file_list, reverse=True)
        return file_list 


def BACKUP_DATABASE():  

    try:
        shutil.copyfile(GET_PATH() + '/data/database.db', 
                        GET_PATH() + '/data/backup_database/' + str(datetime.datetime.now().date()) + '_database.db')
                
        # if more then 10 backups saved, delete oldest backup file
        list_of_files = os.listdir(GET_PATH() + '/data/backup_database/')    
        full_path     = [GET_PATH() + '/data/backup_database/' + '{0}'.format(x) for x in list_of_files]

        if len([name for name in list_of_files]) > 10:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)        
        
        WRITE_LOGFILE_SYSTEM("SUCCESS", "System | Database | Backup created")
        return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Database | " + str(e)) 


def RESTORE_DATABASE(filename):

    try:
        if filename.split("_")[1] == "database.db":
            shutil.copyfile(GET_PATH() + '/data/backup_database/' + filename, GET_PATH() + '/data/database.db')
            WRITE_LOGFILE_SYSTEM("SUCCESS", "System | Database_Backup | " + filename + " | restored")
            return True
            
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Database_Backup | " + str(e))  
        return (e)
        
        
def DELETE_DATABASE_BACKUP(filename):

    try:
        os.remove (GET_PATH() + '/data/backup_database/' + filename)
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/backup_database/" + filename + " | deleted")
        return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/backup_database/" + filename + " | " + str(e))  
        return (e)


""" ############### """
"""  backup zigbee  """
""" ############### """

def BACKUP_ZIGBEE():  

    try:
        os.system("sudo zip -r " + GET_PATH() + '/data/backup_zigbee/' + str(datetime.datetime.now().date()) + ".zip /opt/zigbee2mqtt/data/")
             
        # if more then 10 backups saved, delete oldest backup file
        list_of_files = os.listdir(GET_PATH() + '/data/backup_zigbee/')    
        full_path     = [GET_PATH() + '/data/backup_zigbee/' + '{0}'.format(x) for x in list_of_files]

        if len([name for name in list_of_files]) > 10:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)        
        
        WRITE_LOGFILE_SYSTEM("SUCCESS", "System | Zigbee | Backup created")
        return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Zigbee | " + str(e)) 


""" ################ """
"""  mqtt firmwares  """
""" ################ """

def GET_ALL_MQTT_FIRMWARE_FILES():

    file_list = []
    for files in os.walk(GET_PATH() + "/firmwares/"):  
        file_list.append(files)   

    if file_list == []:
        return ""
    else:
        return file_list[0][2]    


def DELETE_MQTT_FIRMWARE(filename):

    try:
        os.remove (GET_PATH() + '/firmwares/' + filename)
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /firmwares/" + filename + " | deleted")
        return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /firmwares/" + filename + " | " + str(e))  
        return ("Delete Firmware || " + str(e)) 


""" ############ """
"""  sensordata  """
""" ############ """

def GET_ALL_SENSORDATA_FILES():

    file_list = []
    for files in os.walk(GET_PATH() + "/data/csv/"):  
        file_list.append(files)   

    if file_list == []:
        return []
    else:
        return file_list[0][2]    


def CREATE_SENSORDATA_FILE(filename):

    if os.path.isfile(GET_PATH() + "/data/csv/" + filename + ".csv") is False:

        try:
            # create csv file
            file = GET_PATH() + "/data/csv/" + filename + ".csv"
            with open(file, 'w', encoding='utf-8') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                       
                filewriter.writerow(['Timestamp','Device','Sensor','Sensor_Value'])
                csvfile.close()

            WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/csv/" + filename + ".csv | created") 
            return True
                
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filename + ".csv | " + str(e))

    else:
        return True


sensordata_messages_list = []

def START_BLOCK_SENSORDATA_THREAD(message):

	try:
		Thread = threading.Thread(target=BLOCK_SENSORDATA_THREAD, args=(message, ))
		Thread.start()  

	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Block Sensordata | " + str(e)) 


def BLOCK_SENSORDATA_THREAD(message): 
    time.sleep(10)
    sensordata_messages_list.remove(message)


def WRITE_SENSORDATA_FILE(filename, device, sensor, value):

    if os.path.isfile(GET_PATH() + "/data/csv/" + filename + ".csv") is False:
        CREATE_SENSORDATA_FILE(filename)

    # block existing message
    for message in sensordata_messages_list:   
        if message == [filename, device, sensor, value]:
            return

    # add message to block list
    sensordata_messages_list.append([filename, device, sensor, value])
    START_BLOCK_SENSORDATA_THREAD([filename, device, sensor, value])

    try:
        # open csv file
        file = GET_PATH() + "/data/csv/" + filename + ".csv"
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                                        
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), str(device), str(sensor), str(value) ])
            csvfile.close()
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filename + ".csv | " + str(e))


def READ_SENSORDATA_FILE(filename):

    try:
        file = GET_PATH() + "/data/csv/" + filename

        df = pd.read_csv(file, sep = ",", skiprows = 1, names = ["Timestamp","Device","Sensor","Sensor_Value"])
        return df

    except Exception as e:
        if "Error tokenizing data. C error: Calling read(nbytes) on source failed. Try engine='python'." not in str(e):
            WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filename + " | " + str(e))    


def DELETE_SENSORDATA_FILE(filename):
    
    try:
        os.remove (GET_PATH() + '/data/csv/' + filename)
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/csv/" + filename + " | deleted")
        return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filename + " | " + str(e)) 
        return ("Delete Datafile || " + str(e)) 


""" ########################### """
"""  file mqtt manually adding  """
""" ########################### """

def GET_ALL_MQTT_DEVICES_MANUALLY_ADDING():

    try:
        list_devices = []    

        with open(GET_PATH() + "/app/mqtt_manually_adding.json", 'r') as data_file:
            data_loaded = json.load(data_file)

        for device in data_loaded["data"]:

            try:
                device_model       = device['model']                
                device_description = device['description']
            except:
                device_model       = ""                   
                device_description = ""                  
                
            list_devices.append([device_model,device_description])
           
        return list_devices 
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /app/mqtt_manually_adding.json | " + str(e))   


def GET_MQTT_DEVICE_MANUALLY_ADDING_INFORMATIONS(model):

    try:
        with open(GET_PATH() + "/app/mqtt_manually_adding.json", 'r') as data_file:
            data_loaded = json.load(data_file)

        for device in data_loaded["data"]:

            if str(device["model"]) == str(model):

                try:
                    device_type   = device['device_type']
                except:
                    device_type   = ""                 
                  
                try:
                    description   = device['description']
                except:
                    description   = ""

                try:
                    input_values  = device['input_values']
                    input_values  = ','.join(input_values)   
                    input_values  = input_values.replace("'", '"')
                except:
                    input_values  = ""
                  
                try:
                    input_events  = device['input_events']
                    input_events  = ','.join(input_events)
                    input_events  = input_events.replace("'", '"')     
                except:
                    input_events  = ""
                    
                try:
                    commands      = device['commands']   
                    commands      = ','.join(commands)
                    commands      = commands.replace("'", '"')                              
                except:
                    commands      = ""

                try:
                    commands_json = device['commands_json']   
                    commands_json = ','.join(commands_json)
                    commands_json = commands_json.replace("'", '"')                             
                except:
                    commands_json = "" 

                return (device_type, description, input_values, input_events, commands, commands_json)
                
        return ("", "", "", "", "", "")   
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /app/mqtt_manually_adding.json | " + str(e))   


""" ######## """
"""  zigbee  """
""" ######## """

def GET_ZIGBEE_DEVICE_INFORMATIONS(model):
    
    try:
        with open(GET_PATH() + "/app/zigbee_device_informations.json", 'r') as data_file:
            data_loaded = json.load(data_file)

        for device in data_loaded["data"]:

            if str(device["model"]) == str(model):

                try:
                    device_type   = device['device_type']
                except:
                    device_type   = ""                 
                  
                try:
                    description   = device['description']
                except:
                    description   = ""

                try:
                    input_values  = device['input_values']
                    input_values  = ','.join(input_values)   
                    input_values  = input_values.replace("'", '"')
                except:
                    input_values  = ""
                  
                try:
                    input_events  = device['input_events']
                    input_events  = ','.join(input_events)
                    input_events  = input_events.replace("'", '"')     
                except:
                    input_events  = ""
                    
                try:
                    commands      = device['commands']   
                    commands      = ','.join(commands)
                    commands      = commands.replace("'", '"')                              
                except:
                    commands      = ""

                try:
                    commands_json = device['commands_json']   
                    commands_json = ','.join(commands_json)
                    commands_json = commands_json.replace("'", '"')                             
                except:
                    commands_json = "" 

                return (device_type, description, input_values, input_events, commands, commands_json)
                
        return ("", "", "", "", "", "")   
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /app/zigbee_device_informations.json | " + str(e))   


def RESET_ZIGBEE_LOGFILE():

    # remove old log file
    if os.path.isfile(GET_PATH() + "/data/logs/zigbee2mqtt_old.txt"):
        os.remove (GET_PATH() + "/data/logs/zigbee2mqtt_old.txt")

        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/zigbee2mqtt_old.txt | deleted")

    # rename current log file      
    if os.path.isfile(GET_PATH() + "/data/logs/zigbee2mqtt.txt"):
        os.rename (GET_PATH() + "/data/logs/zigbee2mqtt.txt", GET_PATH() + "/data/logs/zigbee2mqtt_old.txt")
 
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/zigbee2mqtt.txt | renamed")