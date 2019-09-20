import datetime
import os
import shutil
import csv
import yaml
import json

import pandas as pd

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
    PATH = os.path.abspath("") 

def GET_PATH():
    return (PATH)

backup_location_temp_path = ""


""" #### """
""" logs """
""" #### """

def CREATE_LOGFILE(filename):
    try:
        # create csv file
        file = PATH + "/logs/" + filename + ".csv"
        
        with open(file, 'w', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)    

            if filename == "log_mqtt":                   
                filewriter.writerow(['Timestamp','Channel','Message'])              
            if filename == "log_system":                   
                filewriter.writerow(['Timestamp','Type','Description'])                
            
            csvfile.close()

        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filename + ".csv | created")      
           
    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filename + ".csv | " + str(e))  

        
def RESET_LOGFILE(filename):
    if os.path.isfile(PATH + "/logs/" + filename + ".csv"):
        os.remove (PATH + "/logs/" + filename + ".csv")

        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filename + ".csv | deleted")
        
    CREATE_LOGFILE(filename)
        

def WRITE_LOGFILE_MQTT(gateway, channel, msg):
    
    # create file if not exist
    if os.path.isfile(PATH + "/logs/log_" + gateway + ".csv") is False:
        CREATE_LOGFILE("log_" + gateway)
        
    # replace file if size > 2,5 mb
    file_size = os.path.getsize(PATH + "/logs/log_" + gateway + ".csv")
    file_size = round(file_size / 1024 / 1024, 2)
    
    if file_size > 2.5:
        RESET_LOGFILE("log_" + gateway)

    try:
        
        # open csv file
        file = PATH + "/logs/log_" + gateway + ".csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)                                        
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), str(channel), msg ])
            csvfile.close()
       
    except Exception as e:
        print(str(e))


def WRITE_LOGFILE_SYSTEM(log_type, description):

    # create file if not exist
    if os.path.isfile(PATH + "/logs/log_system.csv") is False:
        CREATE_LOGFILE("log_system")

    # replace file if size > 2.5 mb
    file_size = os.path.getsize(PATH + "/logs/log_system.csv")
    file_size = round(file_size / 1024 / 1024, 2)
    
    if file_size > 2.5:
        RESET_LOGFILE("log_system")

    try:
        # open csv file
        file = PATH + "/logs/log_system.csv"
        
        with open(file, 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)   
            filewriter.writerow( [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), log_type, description])
            csvfile.close()
        
    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/log_system.csv | " + str(e))
        return ("ERROR: " + str(e))
        
    
def GET_LOGFILE_SYSTEM(selected_log_types, rows, search):   
    
    try:
        # open csv file
        file = PATH + "/logs/log_system.csv"
        
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
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/log_system.csv | " + str(e)) 
        return ("ERROR: " + str(e))        


""" ############## """
""" network config """
""" ############## """

def UPDATE_NETWORK_SETTINGS_FILE(lan_dhcp, lan_ip_address, lan_gateway):
    
    try:
        file = "/etc/dhcpcd.conf"
        with open(file, 'w', encoding='utf-8') as conf_file:
            conf_file.write("# A sample configuration for dhcpcd.\n")
            conf_file.write("# See dhcpcd.conf(5) for details.\n")
            conf_file.write("\n")
            conf_file.write("# Inform the DHCP server of our hostname for DDNS.\n")
            conf_file.write("hostname\n")
            conf_file.write("\n")
            conf_file.write("# Use the hardware address of the interface for the Client ID.\n")
            conf_file.write("clientid\n")
            conf_file.write("\n")
            conf_file.write("# Persist interface configuration when dhcpcd exits.\n")
            conf_file.write("persistent\n")
            conf_file.write("\n")
            conf_file.write("# on the server to actually work.\n")
            conf_file.write("option rapid_commit\n")
            conf_file.write("\n")
            conf_file.write("# A list of options to request from the DHCP server.\n")
            conf_file.write("option domain_name_servers, domain_name, domain_search, host_name\n")
            conf_file.write("option classless_static_routes\n")
            conf_file.write("\n")
            conf_file.write("# Respect the network MTU. This is applied to DHCP routes.\n")
            conf_file.write("option interface_mtu\n")
            conf_file.write("\n")
            conf_file.write("# A ServerID is required by RFC2131.\n")
            conf_file.write("require dhcp_server_identifier\n")
            conf_file.write("\n")
            conf_file.write("# Generate SLAAC address using the Hardware Address of the interface\n")
            conf_file.write("#slaac hwaddr\n")
            conf_file.write("# OR generate Stable Private IPv6 Addresses based from the DUID\n")
            conf_file.write("slaac private\n")
        
            if lan_dhcp != "True":

                conf_file.write("\n")
                conf_file.write("interface eth0\n")
                conf_file.write("inform " + str(lan_ip_address) + "/24\n")             
                conf_file.write("static routers=" + str(lan_gateway) + "\n")    

            conf_file.close()

    except Exception as e:
        print(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /etc/dhcpcd.conf | " + str(e))  
        return ("ERROR: " + str(e))


""" ############### """
""" backup database """
""" ############### """

"""
# get backup path
backup_location_path = GET_CONFIG_BACKUP_LOCATION()


def GET_BACKUP_FILES():
    file_list = []
    for files in os.walk(backup_location_path):  
        file_list.append(files)

    if file_list == []:
        return ""
    else:
        file_list = file_list[0][2]
        file_list = sorted(file_list, reverse=True)
        return file_list 


def SAVE_DATABASE():  

    try:
        # save database
        shutil.copyfile(PATH + '/app/database/db_miranda.sqlite3', 
                        backup_location_path + str(datetime.datetime.now().date()) + '_db_miranda.sqlite3')
                
        # if more then 10 backups saved, delete oldest backup file
        list_of_files = os.listdir(PATH + '/backup/')    
        full_path     = [backup_location_path + '{0}'.format(x) for x in list_of_files]

        if len([name for name in list_of_files]) > 10:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)        
        
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Database_Backup | saved")
        return ""
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Database_Backup | " + str(e)) 
        return str(e)


def RESTORE_DATABASE(filename):
    # check file
    try:
        if filename.split("_")[1] == "smarthome.sqlite3":
            shutil.copyfile(backup_location_path + filename, PATH + '/app/database/db_miranda.sqlite3')
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Database_Backup | " + filename + " | restored")
            
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Database_Backup | " + str(e))  
        return ("ERROR: " + str(e))
        
        
def DELETE_DATABASE_BACKUP(filename):
    try:
        os.remove (backup_location_path + filename)
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /backup/" + filename + " | deleted")
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /backup/" + filename + " | " + str(e))  
        return ("ERROR: " + str(e))
"""