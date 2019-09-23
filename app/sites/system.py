from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps
from ping3               import ping

from app                         import app
from app.database.models         import *
from app.backend.email           import SEND_EMAIL
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
    error_message_change_settings_network   = []
    success_message_change_settings_network = False
    error_message_change_settings_email     = []
    success_message_change_settings_email   = False    

    message_shutdown            = "" 
    message_ip_config_change    = False
    message_test_settings_email = ""

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

        # no dhcp ?
        if lan_dhcp == "False":  

            # first reload of the website after deactivate dhcp, website don't know the values "set_lan_ip_address" and "set_lan_gateway"
            if request.form.get("set_lan_ip_address") != None:          

                save_settings_lan = True
                        
                if request.form.get("set_lan_ip_address") != "":
                    new_lan_ip_address = request.form.get("set_lan_ip_address")

                    if new_lan_ip_address != lan_ip_address:

                        if CHECK_IP_ADDRESS(new_lan_ip_address) == False:
                            error_message_change_settings_network.append("Netzwerk || Ungültige IP-Adresse angegeben")
                            save_settings_lan = False
                                
                        elif PING_IP_ADDRESS(new_lan_ip_address) == True or new_lan_ip_address == GET_HOST_NETWORK().lan_ip_address:
                            error_message_change_settings_network.append("Netzwerk || IP-Adresse bereits vergeben")
                            save_settings_lan = False

                        else:
                            lan_ip_address = new_lan_ip_address

                else:
                    error_message_change_settings_network.append("Netzwerk || Keine IP-Adresse angegeben") 
                    
                if request.form.get("set_lan_gateway") != "":
                    lan_gateway = request.form.get("set_lan_gateway")            

                    if CHECK_IP_ADDRESS(lan_gateway) == False:
                        error_message_change_settings_network.append("Netzwerk || Ungültiges Gateway angegeben")
                        save_settings_lan = False
                        
                    if CHECK_IP_ADDRESS(lan_gateway) == True and PING_IP_ADDRESS(lan_gateway) == False:
                        error_message_change_settings_network.append("Netzwerk || Gateway nicht gefunden")
                        save_settings_lan = False

                else:
                    error_message_change_settings_network.append("Netzwerk || Kein Gateway angegeben") 
                    save_settings_lan = False

                if save_settings_lan == True:

                    changes_saved = False

                    if UPDATE_HOST_INTERFACE_LAN_DHCP(lan_dhcp):
                        changes_saved = True
                    if UPDATE_HOST_INTERFACE_LAN(lan_ip_address, lan_gateway):
                        changes_saved = True
                    if UPDATE_NETWORK_SETTINGS_FILE(lan_dhcp, lan_ip_address, lan_gateway):
                        changes_saved = True

                    if changes_saved == True:
                        success_message_change_settings_network = True

            else:
                if UPDATE_HOST_INTERFACE_LAN_DHCP(lan_dhcp):
                    success_message_change_settings_network = True       

        else:
            if UPDATE_HOST_INTERFACE_LAN_DHCP(lan_dhcp):
                success_message_change_settings_network = True  


    """ ####### """
    """  email  """
    """ ####### """    
    
    # update email settings
    if request.form.get("update_email_settings") != None:  

        error_founded = False

        if request.form.get("set_server_address") != "":
            server_address = request.form.get("set_server_address")
        else:
            error_message_change_settings_email.append("Ungültige Eingabe Server-Adresse || Keinen Wert angegeben") 
            error_founded = True                  

        if request.form.get("set_server_port") != "":

            try:
                if int(request.form.get("set_server_port")) in [25, 110, 143, 465, 587, 993, 995]:
                    server_port = request.form.get("set_server_port")
            except:
                error_message_change_settings_email.append("Ungültige Eingabe Server-Port || Falscher Port")
                error_founded = True     

        else:
            error_message_change_settings_email.append("Ungültige Eingabe Server-Port || Keinen Wert angegeben") 
            error_founded = True       

        if request.form.get("radio_encoding") != None:
            encoding = request.form.get("radio_encoding")
        else:
            error_message_change_settings_email.append("Ungültige Eingabe Verschlüsselung || Keinen Wert angegeben") 
            error_founded = True     

        if request.form.get("set_username") != "":
            username = request.form.get("set_username")
        else:
            error_message_change_settings_email.append("Ungültige Eingabe Benutzername || Keinen Wert angegeben") 
            error_founded = True     

        if request.form.get("set_password") != "":
            password = request.form.get("set_password")
        else:
            error_message_change_settings_email.append("Ungültige Eingabe Passwort || Keinen Wert angegeben") 
            error_founded = True                 

        if error_founded == False:

            if SET_EMAIL_SETTINGS(server_address, server_port, encoding, username, password):
                success_message_change_settings_email = True


    # test email settings
    if request.form.get("test_email_settings") != None:  
        message_test_settings_email = SEND_EMAIL("TEST", "TEST")


    """ ######### """
    """  backups  """
    """ ######### """    
 
    # save database   
    if request.form.get("database_save") != None:
        SAVE_DATABASE() 

    cpu_temperature   = GET_CPU_TEMPERATURE()
 
    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway
     
    email_settings    = GET_EMAIL_SETTINGS()
    list_backup_files = GET_BACKUP_FILES()

    data = {'navigation': 'system', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/system.html',   
                                                    error_message_change_settings_network=error_message_change_settings_network,
                                                    success_message_change_settings_network=success_message_change_settings_network,     
                                                    error_message_change_settings_email=error_message_change_settings_email,
                                                    success_message_change_settings_email=success_message_change_settings_email,
                                                    message_test_settings_email=message_test_settings_email,                                                                                                         
                                                    message_shutdown=message_shutdown,
                                                    cpu_temperature=cpu_temperature,
                                                    lan_dhcp=lan_dhcp,
                                                    lan_ip_address=lan_ip_address,
                                                    lan_gateway=lan_gateway,  
                                                    email_settings=email_settings,                                            
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
