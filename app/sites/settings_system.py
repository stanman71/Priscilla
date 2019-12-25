from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps
from ping3               import ping

from app                         import app
from app.database.models         import *
from app.backend.email           import SEND_EMAIL
from app.backend.file_management import UPDATE_NETWORK_SETTINGS_FILE, GET_BACKUP_FILES, BACKUP_DATABASE, RESTORE_DATABASE, DELETE_DATABASE_BACKUP
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
    WRITE_LOGFILE_SYSTEM("EVENT", "Host | Reboot") 
    os.system("sudo reboot")


def HOST_SHUTDOWN():
    time.sleep(10)
    WRITE_LOGFILE_SYSTEM("EVENT", "Host | Shutdown")     
    os.system("sudo shutdown")


@app.route('/settings/system', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_system():
    success_message_change_settings_services = False    
    error_message_change_settings_services   = [] 
    success_message_change_settings_network  = False
    error_message_change_settings_network    = []
    success_message_change_settings_spotify  = False       
    error_message_change_settings_spotify    = []     
    success_message_change_settings_email    = False       
    error_message_change_settings_email      = [] 
    success_message_backup_database          = ""    
    error_message_backup_database            = ""

    message_system              = "" 
    message_ip_config_change    = False
    message_test_settings_email = ""

    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway

    # restore message
    if session.get('restore_database_success', None) != None:
        success_message_backup_database = session.get('restore_database_success')
        session['restore_database_success'] = None
        
    if session.get('restore_database_error', None) != None:
        error_message_backup_database = session.get('restore_database_error') 
        session['restore_database_error'] = None       
        
    # delete message
    if session.get('delete_database_success', None) != None:
        success_message_backup_database = session.get('delete_database_success')
        session['delete_database_success'] = None
        
    if session.get('delete_database_error', None) != None:
        error_message_backup_database = session.get('delete_database_error') 
        session['delete_database_error'] = None       
        

    """ #################### """
    """  restart / shutdown  """
    """ #################### """              
        
    # restart raspi 
    if request.form.get("restart_system") != None:
        Thread = threading.Thread(target=HOST_REBOOT)
        Thread.start()    
        message_system = "System wird in 10 Sekunden neugestartet"
        
    # shutdown raspi 
    if request.form.get("shutdown_system") != None:
        Thread = threading.Thread(target=HOST_SHUTDOWN)
        Thread.start()    
        message_system = "System wird in 10 Sekunden heruntergefahren"


    """ ################### """
    """  settings services  """
    """ ################### """    

    if request.form.get("update_settings_services") != None:

        error_founded = False

        if request.form.get("radio_zigbee2mqtt_active") != None:
            zigbee2mqtt_active = request.form.get("radio_zigbee2mqtt_active")
        else:
            error_message_change_settings_services.append("Ungültige Eingabe Zigbee || Keinen Wert angegeben") 
            error_founded = True           

        if request.form.get("radio_lms_active") != None:
            lms_active = request.form.get("radio_lms_active")
        else:
            error_message_change_settings_services.append("Ungültige Eingabe Logitech Media Server || Keinen Wert angegeben") 
            error_founded = True      

        if request.form.get("radio_squeezelite_active") != None:
            squeezelite_active = request.form.get("radio_squeezelite_active")
        else:
            error_message_change_settings_services.append("Ungültige Eingabe Squeezelite Player || Keinen Wert angegeben") 
            error_founded = True          

        if error_founded == False:

            if SET_SYSTEM_SERVICES(zigbee2mqtt_active, lms_active, squeezelite_active):
                success_message_change_settings_services = True

                # zigbee

                if GET_SYSTEM_SERVICES().zigbee2mqtt_active == "True":
                    try:
                        os.system("sudo systemctl start zigbee2mqtt")
                        WRITE_LOGFILE_SYSTEM("EVENT", "ZigBee2MQTT | Activated")
                        print("ZigBee2MQTT | Activated") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | " + str(e)) 
                        print("ERROR: ZigBee2MQTT | " + str(e))      

                else:
                    try:
                        os.system("sudo systemctl stop zigbee2mqtt")
                        WRITE_LOGFILE_SYSTEM("EVENT", "ZigBee2MQTT | Disabled")
                        print("ZigBee2MQTT | Disabled") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | " + str(e)) 
                        print("ERROR: ZigBee2MQTT | " + str(e)) 
           
                # logitech media server

                if GET_SYSTEM_SERVICES().lms_active == "True":
                    try:
                        os.system("sudo systemctl start logitechmediaserver")
                        WRITE_LOGFILE_SYSTEM("EVENT", "Logitech Media Server | Activated")
                        print("Logitech Media Server | Activated") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Logitech Media Server | " + str(e)) 
                        print("ERROR: Logitech Media Server | " + str(e))       
 
                else: 
                    try:
                        os.system("sudo systemctl stop logitechmediaserver")
                        WRITE_LOGFILE_SYSTEM("EVENT", "Logitech Media Server | Disabled")
                        print("Logitech Media Server | Disabled") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Logitech Media Server | " + str(e)) 
                        print("ERROR: Logitech Media Server | " + str(e)) 

                # squeezelite player

                if GET_SYSTEM_SERVICES().squeezelite_active == "True":
                    try:
                        os.system("sudo systemctl start squeezelite")
                        WRITE_LOGFILE_SYSTEM("EVENT", "Squeezelie Player | Activated")
                        print("Squeezelie Player | Activated") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Squeezelie Player | " + str(e)) 
                        print("ERROR: Squeezelie Player | " + str(e))     

                else:
                    try:
                        os.system("sudo systemctl stop squeezelite")
                        WRITE_LOGFILE_SYSTEM("EVENT", "Squeezelie Player | Disabled")
                        print("Squeezelie Player | Disabled") 
                        time.sleep(1)
                    except Exception as e:
                        WRITE_LOGFILE_SYSTEM("ERROR", "Squeezelie Player | " + str(e)) 
                        print("ERROR: Squeezelie Player | " + str(e)) 


    """ ################# """
    """  settings network """
    """ ################# """    
                
    if request.form.get("set_settings_network") != None:
        
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
                    new_lan_ip_address = request.form.get("set_lan_ip_address").strip()  

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
                    lan_gateway = request.form.get("set_lan_gateway").strip()              

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


    """ ################## """
    """  settings spotify  """
    """ ################## """    
    
    # update email settings
    if request.form.get("update_settings_spotify") != None:  

        client_id = request.form.get("set_client_id").strip()  
        client_secret = request.form.get("set_client_secret").strip()  

        if SET_SPOTIFY_SETTINGS(client_id, client_secret):
            success_message_change_settings_spotify = True


    """ ################ """
    """  settings email  """
    """ ################ """    
    
    # update email settings
    if request.form.get("update_settings_email") != None:  

        server_address = request.form.get("set_server_address").strip()        
        server_port = request.form.get("set_server_port").strip()  
        encoding = request.form.get("radio_encoding")
        username = request.form.get("set_username").strip()  
        password = request.form.get("set_password").strip()  

        if SET_EMAIL_SETTINGS(server_address, server_port, encoding, username, password):
            success_message_change_settings_email = True


    # test email settings
    if request.form.get("test_settings_email") != None: 

        # check email settings complete
        settings = GET_EMAIL_SETTINGS()

        if (settings.server_address == "" or 
            settings.server_port == "" or   
            settings.username == "" or 
            settings.password == ""):

            message_test_settings_email = "eMail-Einstellungen sind unvollständig"    

        else:   
            message_test_settings_email = SEND_EMAIL("TEST", "TEST")


    """ ################ """
    """  backup database """
    """ ################ """    
 
    if request.form.get("backup_database") != None:
        result = BACKUP_DATABASE() 
        
        if result:
            success_message_backup_database = "Backup || Erfolgreich erstellt"
        else:
            error_message_backup_database = "Backup || " + str(result)


    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway

    system_services   = GET_SYSTEM_SERVICES()     
    spotify_settings  = GET_SPOTIFY_SETTINGS()
    email_settings    = GET_EMAIL_SETTINGS()
    list_backup_files = GET_BACKUP_FILES()

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_system.html',   
                                                    success_message_change_settings_services=success_message_change_settings_services,
                                                    error_message_change_settings_services=error_message_change_settings_services,
                                                    success_message_change_settings_network=success_message_change_settings_network,                             
                                                    error_message_change_settings_network=error_message_change_settings_network, 
                                                    success_message_change_settings_spotify=success_message_change_settings_spotify,       
                                                    error_message_change_settings_spotify=error_message_change_settings_spotify,
                                                    success_message_change_settings_email=success_message_change_settings_email,                                                       
                                                    error_message_change_settings_email=error_message_change_settings_email,
                                                    message_test_settings_email=message_test_settings_email, 
                                                    error_message_backup_database=error_message_backup_database,                                                       
                                                    success_message_backup_database=success_message_backup_database,                                                                                                     
                                                    message_system=message_system,
                                                    lan_dhcp=lan_dhcp,
                                                    lan_ip_address=lan_ip_address,
                                                    lan_gateway=lan_gateway,  
                                                    system_services=system_services,
                                                    spotify_settings=spotify_settings,
                                                    email_settings=email_settings,                                            
                                                    list_backup_files=list_backup_files,                    
                                                    ) 
                            )

# restore database backup
@app.route('/settings/system/backup/restore/backup_database/<string:filename>')
@login_required
@permission_required
def restore_database_backup(filename):
    result = RESTORE_DATABASE(filename)

    if result == True:
        session['restore_database_success'] = filename + " || Erfolgreich wiederhergestellt"
    else:
        session['restore_database_error'] = filename + " || " + result

    return redirect(url_for('settings_system'))


# delete database backup
@app.route('/settings/system/backup/delete/backup_database/<string:filename>')
@login_required
@permission_required
def delete_database_backup(filename):
    result = DELETE_DATABASE_BACKUP(filename)

    if result == True:
        session['delete_database_success'] = filename + " || Erfolgreich gelöscht"
    else:
        session['delete_database_error'] = filename + " || " + result

    return redirect(url_for('settings_system'))