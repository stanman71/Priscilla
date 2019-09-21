from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps
from ping3               import ping

from app                         import app
from app.database.models         import *
from app.backend.file_management import UPDATE_NETWORK_SETTINGS_FILE, GET_BACKUP_FILES, SAVE_DATABASE, RESTORE_DATABASE, DELETE_DATABASE_BACKUP
from app.common                  import COMMON, STATUS
from app.assets                  import *

import datetime
import os
import time
import threading


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


""" ################# """
"""  system functions """
""" ################# """

def GET_CPU_TEMPERATURE():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n"," C"))


def CHECK_IP_ADDRESS(ip_address):
    try:
        for element in ip_address:
            if not element.isdigit() and element != ".":
                return False
              
        if len(ip_address.split(".")) != 4:
            return False
        
        for element in ip_address.split("."):
            if not 0 <= int(element) <= 254:
                return False
            
        return True
    
    except:
        return False
  
  
def PING_IP_ADDRESS(ip_address):
    try:
    
        if ping(ip_address, timeout=1) != None:
            return True
        if ping(ip_address, timeout=1) != None:
            return True

        return False
    
    except:
        return False


def HOST_REBOOT():
    time.sleep(10)
    os.system("sudo shutdown -r now")


def HOST_SHUTDOWN():
    time.sleep(10)
    os.system("sudo shutdown -h now")


@app.route('/system', methods=['GET', 'POST'])
@login_required
@permission_required
def system():
    error_message_change_settings   = []
    success_message_change_settings = False
    
    message_shutdown         = "" 
    message_ip_config_change = False

    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway


    """ #################### """
    """  restart / shutdown  """
    """ #################### """              
        
    # restart raspi 
    if request.form.get("restart") != None:
        Thread = threading.Thread(target=HOST_REBOOT)
        Thread.start()    
        message_shutdown = "System wird in 10 Sekunden neugestartet"
        
    # shutdown raspi 
    if request.form.get("shutdown") != None:
        Thread = threading.Thread(target=HOST_SHUTDOWN)
        Thread.start()    
        message_shutdown = "System wird in 10 Sekunden heruntergefahren"


    """ ############## """
    """  lan settings  """
    """ ############## """    
                
    if request.form.get("set_lan_settings") != None:
        
        if request.form.get("checkbox_lan_dhcp"):
            lan_dhcp = "True" 
        else:
            lan_dhcp = "False"  

        UPDATE_HOST_INTERFACE_LAN_DHCP(lan_dhcp)

        if lan_dhcp == "False":  

            save_settings_lan = True
                     
            if request.form.get("set_lan_ip_address") != "":
                new_lan_ip_address = request.form.get("set_lan_ip_address")

                if new_lan_ip_address != lan_ip_address:

                    if CHECK_IP_ADDRESS(new_lan_ip_address) == False:
                        error_message_change_settings.append("LAN || Ungültige IP-Adresse angegeben")
                        save_settings_lan = False
                            
                    elif PING_IP_ADDRESS(new_lan_ip_address) == True or new_lan_ip_address == GET_HOST_NETWORK().lan_ip_address:
                        error_message_change_settings.append("LAN || IP-Adresse bereits vergeben")
                        save_settings_lan = False

                    else:
                        lan_ip_address = new_lan_ip_address

            else:
                error_message_change_settings.append("LAN || Keine IP-Adresse angegeben") 
                
            if request.form.get("set_lan_gateway") != "":
                lan_gateway = request.form.get("set_lan_gateway")            

                if CHECK_IP_ADDRESS(lan_gateway) == False:
                    error_message_change_settings.append("LAN || Ungültiges Gateway angegeben")
                    save_settings_lan = False
                    
                if CHECK_IP_ADDRESS(lan_gateway) == True and PING_IP_ADDRESS(lan_gateway) == False:
                    error_message_change_settings.append("LAN || Gateway nicht gefunden")
                    save_settings_lan = False

            else:
                error_message_change_settings.append("LAN || Kein Gateway angegeben") 

            if save_settings_lan == True:
                UPDATE_HOST_INTERFACE_LAN(lan_ip_address, lan_gateway)
                UPDATE_NETWORK_SETTINGS_FILE(lan_dhcp, lan_ip_address, lan_gateway)


    """ ######### """
    """  backups  """
    """ ######### """    
 
    # save database   
    if request.form.get("database_save") is not None:
        SAVE_DATABASE() 
 
    list_backup_files = GET_BACKUP_FILES()
        
    dropdown_list_hours = [ "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                            "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"] 


    cpu_temperature   = GET_CPU_TEMPERATURE()
 
    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway
     

    data = {'navigation': 'system', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/system.html',   
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings=success_message_change_settings,                                                    
                                                    message_shutdown=message_shutdown,
                                                    cpu_temperature=cpu_temperature,
                                                    lan_dhcp=lan_dhcp,
                                                    lan_ip_address=lan_ip_address,
                                                    lan_gateway=lan_gateway,  
                                                    list_backup_files=list_backup_files,                        
                                                    ) 
                            )

# restore database backup
@app.route('/system/backup/restore/backup_database/<string:filename>')
@login_required
@permission_required
def restore_database_backup(filename):
    RESTORE_DATABASE(filename)
    return redirect(url_for('system'))


# delete database backup
@app.route('/system/backup/delete/backup_database/<string:filename>')
@login_required
@permission_required
def delete_database_backup(filename):
    DELETE_DATABASE_BACKUP(filename)
    return redirect(url_for('system'))
