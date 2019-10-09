import datetime
import os
import shutil
import csv
import json
import pandas as pd
import yaml

from flask import send_from_directory
from werkzeug.utils import secure_filename

from app import app


""" #### """
""" path """
""" #### """


# windows
if os.name == "nt":                 
    PATH = os.path.abspath("") 
# linux
else:                               
    PATH = "/home/pi/watering_control/"


def GET_PATH():
    return (PATH)


""" #### """
""" logs """
""" #### """

def CREATE_LOGFILE(filename):
    try:
        # create csv file
        file = PATH + "/data/logs/" + filename + ".csv"
        
        with open(file, 'w', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)    

            if filename == "log_devices":                   
                filewriter.writerow(['Timestamp','Channel','Message'])              
            if filename == "log_system":                   
                filewriter.writerow(['Timestamp','Type','Description'])                
            
            csvfile.close()

        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/logs/" + filename + ".csv | created")   
        return True   
           
    except Exception as e:
        if filename != "log_system":
            WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/logs/" + filename + ".csv | " + str(e))  
        return(e)

        
def RESET_LOGFILE(filename):
    if os.path.isfile(PATH + "/data/logs/" + filename + ".csv"):
        os.remove (PATH + "/data/logs/" + filename + ".csv")

        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/logs/" + filename + ".csv | deleted")
        
    result = CREATE_LOGFILE(filename)
    
    if result:
        return True
    else:
        return result
        

def WRITE_LOGFILE_DEVICES(channel, msg):
    
    # create file if not exist
    if os.path.isfile(PATH + "/data/logs/log_devices.csv") is False:
        CREATE_LOGFILE("log_devices")
        
    # replace file if size > 2,5 mb
    file_size = os.path.getsize(PATH + "/data/logs/log_devices.csv")
    file_size = round(file_size / 1024 / 1024, 2)
    
    if file_size > 2.5:
        RESET_LOGFILE("log_devices")

    try:
        
        # open csv file
        file = PATH + "/data/logs/log_devices.csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                                        
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), str(channel), msg ])
            csvfile.close()
            return True
       
    except Exception as e:
        return(e)


def WRITE_LOGFILE_SYSTEM(log_type, description):

    # create file if not exist
    if os.path.isfile(PATH + "/data/logs/log_system.csv") is False:
        CREATE_LOGFILE("log_system")

    # replace file if size > 2.5 mb
    file_size = os.path.getsize(PATH + "/data/logs/log_system.csv")
    file_size = round(file_size / 1024 / 1024, 2)
    
    if file_size > 2.5:
        RESET_LOGFILE("log_system")

    try:
        # open csv file
        file = PATH + "/data/logs/log_system.csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)   
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), log_type, description])
            csvfile.close()
            return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/logs/log_system.csv | " + str(e))
        return (e)
        
    
def GET_LOGFILE_SYSTEM(selected_log_types, rows, search):   
    
    try:
        # open csv file
        file = PATH + "/data/logs/log_system.csv"
        
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
                        
                        if search != "" and search in element[2]:
                            data_reversed_filtered.append(element)
                            
                        if search == "":
                            data_reversed_filtered.append(element)
                except:
                    pass

            return data_reversed_filtered[0:rows]
            
    
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/logs/log_system.csv | " + str(e)) 
        return (e)   


""" ############# """
"""  file config  """
""" ############# """

try:
    # open config file
    with open(PATH + "/data/config.yaml", "r") as file_config:
        config = yaml.load(file_config, Loader=yaml.SafeLoader)
        file_config.close()

except Exception as e:
    print("##### ERROR: config file not founded #####")
    WRITE_LOGFILE_SYSTEM("ERROR", "File | data/config.ymal | " + str(e) + " | !!! DEFAULT SETTINGS LOADED !!! ")


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
        
def GET_SPOTIFY_CLIENT_ID():
    try:
        return str(config['spotify']['client_id'])
    except:
        return ""        

def GET_SPOTIFY_CLIENT_SECRET():
    try:
        return str(config['spotify']['client_secret'])
    except:
        return ""     

def GET_SPOTIFY_REFRESH_TOKEN():
    try:
        return str(config['spotify']['refresh_token'])
    except:
        return ""     

def SET_SPOTIFY_REFRESH_TOKEN(REFRESH_TOKEN):
    
    try:
        with open(PATH + "/data/config.yaml") as file_config:
            upload_config = yaml.load(file_config)

        upload_config['spotify']['refresh_token'] = REFRESH_TOKEN

        with open(PATH + "/data/config.yaml", 'w') as file_config:
            yaml.dump(upload_config, file_config)
            
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/config.yaml | " + str(e))  
        return ("ERROR: " + str(e))
        

""" ################ """
"""  file locations  """
""" ################ """

def GET_ALL_LOCATIONS():
    try:
        # open locations file
        with open(PATH + "/data/locations.ymal", "r") as file_locations:
            locations = yaml.load(file_locations, Loader=yaml.SafeLoader)
            file_locations.close()

        return (locations["Locations"].keys())
        
    except Exception as e:    
        return ("ERROR: Locations Import || " + str(e))
        WRITE_LOGFILE_SYSTEM("ERROR", "File | data/locations.ymal | " + str(e))
        

def GET_LOCATION_COORDINATES(location):
    try:
        # open locations file
        with open(PATH + "/data/locations.ymal", "r") as file_locations:
            locations = yaml.load(file_locations, Loader=yaml.SafeLoader)
            file_locations.close()

        return (locations["Locations"][location])
        
    except Exception as e:    
        return ("ERROR: Locations Import || " + str(e))
        WRITE_LOGFILE_SYSTEM("ERROR", "File | data/locations.ymal | " + str(e))



""" ############## """
""" network config """
""" ############## """

def UPDATE_NETWORK_SETTINGS_FILE(lan_dhcp, lan_ip_address, lan_gateway):
    
    try:
        file = "/etc/network/interfaces"
        with open(file, 'w', encoding='utf-8') as conf_file:

            conf_file.write("source /etc/network/interfaces.d/*\n")
            conf_file.write("# Network is managed by Network manager\n")
            conf_file.write("auto lo\n")
            conf_file.write("iface lo inet loopback\n")
    
            if lan_dhcp != "True":

                conf_file.write("\n")
                conf_file.write("auto eth0\n")
                conf_file.write("iface eth0 inet static\n")
                conf_file.write("  address " + str(lan_ip_address) + "\n")
                conf_file.write("  netmask 255.255.255.0\n")        
                conf_file.write("  gateway " + str(lan_gateway) + "\n")    

            conf_file.close()
            return True

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /etc/network/interfaces | " + str(e))  
        return(e)


""" ############### """
""" backup database """
""" ############### """


# get backup path
backup_location_path = PATH + '/data/backup/'


def GET_BACKUP_FILES():
    file_list = []
    for files in os.walk(backup_location_path):  
        file_list.append(files)

    if file_list == []:
        return "No Files founded"
    else:
        file_list = file_list[0][2]
        file_list = sorted(file_list, reverse=True)
        return file_list 


def BACKUP_DATABASE():  
    try:
        shutil.copyfile(PATH + '/app/database/database.db', 
                        backup_location_path + str(datetime.datetime.now().date()) + '_database.db')
                
        # if more then 10 backups saved, delete oldest backup file
        list_of_files = os.listdir(PATH + '/backup/')    
        full_path     = [backup_location_path + '{0}'.format(x) for x in list_of_files]

        if len([name for name in list_of_files]) > 7:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)        
        
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Database | Backup created")
        return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Database | " + str(e)) 
        return (e)


def RESTORE_DATABASE(filename):
    try:
        if filename.split("_")[1] == "database.db":
            shutil.copyfile(backup_location_path + filename, PATH + '/app/database/database.db')
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Database_Backup | " + filename + " | restored")
            return True
            
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Database_Backup | " + str(e))  
        return (e)
        
        
def DELETE_DATABASE_BACKUP(filename):
    try:
        os.remove (backup_location_path + filename)
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/backup/" + filename + " | deleted")
        return True
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/backup/" + filename + " | " + str(e))  
        return (e)


""" ###### """
""" plants """
""" ###### """

def GET_PLANTS_DATAFILES():
    file_list = []
    for files in os.walk(PATH + "/data/csv/"):  
        file_list.append(files)   

    if file_list == []:
        return "No Files founded"
    else:
        return file_list[0][2]    


def CREATE_PLANTS_DATAFILE(filename):
    if os.path.isfile(PATH + "/data/csv/" + filename + ".csv") is False:

        try:
            # create csv file
            file = PATH + "/data/csv/" + filename + ".csv"
            with open(file, 'w', encoding='utf-8') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                       
                filewriter.writerow(["Timestamp","Device","Pumptime","Moisture","Watertank"])
                csvfile.close()

            WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/csv/" + filename + ".csv | created") 
            return True 
                
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/csv/" + filename + ".csv | " + str(e))
            return(e)


def WRITE_PLANTS_DATAFILE(filename, device, pumptime, moisture, watertank):
    if os.path.isfile(PATH + "/csv/" + filename + ".csv") is False:
        CREATE_PLANTS_DATAFILE(filename)

    try:
        # open csv file
        file = PATH + "/data/csv/" + filename + ".csv"
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                                        
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), str(device), str(pumptime), str(moisture), str(watertank)])
            csvfile.close()
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/csv/" + filename + ".csv | " + str(e))
        return(e)


def READ_PLANTS_DATAFILE(filename):
    try:
        # open csv file with pandas
        file = PATH + "/data/csv/" + filename
        
        df = pd.read_csv(file, sep = ",", skiprows = 1, names = ["Timestamp","Device","Pumptime","Moisture","Watertank"])
        return df

    except Exception as e:
        if "Error tokenizing data. C error: Calling read(nbytes) on source failed. Try engine='python'." not in str(e):
            WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/csv/" + filename + " | " + str(e))   
            return(e) 


def RENAME_PLANTS_DATAFILE(old_filename, new_filename):
    try:
        os.rename(PATH + '/data/csv/' + old_filename + ".csv", PATH + '/data/csv/' + new_filename + ".csv") 
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/csv/" + old_filename + " | renamed | New name - " + new_filename)
        return True
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/csv/" + old_filename + " | " + str(e))  
        return(e)


def DELETE_PLANTS_DATAFILE(filename):
    try:
        os.remove (PATH + '/data/csv/' + filename + ".csv")
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/csv/" + filename + " | deleted")
        return True
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/csv/" + filename + " | " + str(e))  
        return(e)



""" ################################ """
"""  file zigbee device informations """
""" ################################ """

def GET_DEVICE_INFORMATIONS(model):
    
    try:
        with open(PATH + "/data/zigbee_device_informations.json", 'r') as data_file:
            data_loaded = json.load(data_file)

        for device in data_loaded["data"]:

            if str(device["model"]) == str(model):

                try:
                    device_type  = device['device_type']
                except:
                    device_type  = ""                 
                  
                try:
                    description  = device['description']
                except:
                    description  = ""

                try:
                    input_values = device['input_values']
                    input_values = ','.join(input_values)   
                    input_values = input_values.replace("'", '"')
                except:
                    input_values = ""
                  
                try:
                    input_events = device['input_events']
                    input_events = ','.join(input_events)
                    input_events = input_events.replace("'", '"')
                    input_events = input_events.replace("},{", '} {')     
                except:
                    input_events = ""
                    
                try:
                    commands     = device['commands']   
                    commands     = ','.join(commands)
                    commands     = commands.replace("'", '"')  
                    commands     = commands.replace("},{", '} {')                               
                except:
                    commands     = ""
                
                return (device_type, description, input_values, input_events, commands)
                
        return ("", "", "", "", "")   
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/zigbee_device_informations.json | " + str(e))   
