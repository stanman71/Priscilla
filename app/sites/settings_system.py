from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps
from ping3               import ping

from app                          import app
from app.backend.database_models  import *
from app.backend.email            import SEND_EMAIL
from app.backend.mqtt             import CHECK_ZIGBEE2MQTT_STARTED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.file_management  import UPDATE_NETWORK_SETTINGS_LINUX, GET_ALL_BACKUP_FILES, BACKUP_DATABASE, RESTORE_DATABASE, DELETE_DATABASE_BACKUP, WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.common                   import COMMON, STATUS
from app.assets                   import *

import datetime
import os
import time
import threading
import heapq


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
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################")
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


def SYSTEM_REBOOT():
    time.sleep(10)
    WRITE_LOGFILE_SYSTEM("EVENT", "System | Reboot") 
    os.system("sudo reboot")


def SYSTEM_SHUTDOWN():
    time.sleep(10)
    WRITE_LOGFILE_SYSTEM("EVENT", "System | Shutdown")     
    os.system("sudo shutdown")


@app.route('/settings/system', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_system():
    page_title       = 'Bianca | Settings | System'
    page_description = 'The system configuration page.'

    success_message_change_settings_services = False    
    error_message_change_settings_services   = [] 
    success_message_change_settings_network  = False
    error_message_change_settings_network    = []
    success_message_change_settings_email    = False       
    error_message_change_settings_email      = []     
    success_message_change_settings_spotify  = False       
    error_message_change_settings_spotify    = []     
    success_message_backup_database          = ""    
    error_message_backup_database            = ""

    message_system              = "" 
    message_ip_config_change    = False
    message_test_settings_email = ""

    ip_address = GET_SYSTEM_SETTINGS().ip_address
    gateway    = GET_SYSTEM_SETTINGS().gateway
    dhcp       = GET_SYSTEM_SETTINGS().dhcp

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
        Thread = threading.Thread(target=SYSTEM_REBOOT)
        Thread.start()    
        message_system = "System will restart in 10 seconds"
        
    # shutdown raspi 
    if request.form.get("shutdown_system") != None:
        Thread = threading.Thread(target=SYSTEM_SHUTDOWN)
        Thread.start()    
        message_system = "System will shutdown in 10 seconds"


    """ ################### """
    """  settings services  """
    """ ################### """    

    if request.form.get("update_settings_services") != None:

        zigbee2mqtt_active = request.form.get("set_radio_zigbee2mqtt_active") 
        lms_active         = request.form.get("set_radio_lms_active")
        squeezelite_active = request.form.get("set_radio_squeezelite_active")    


        ########
        # zigbee
        ########

        if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "False" and zigbee2mqtt_active == "True":

            try:
                os.system("sudo systemctl start zigbee2mqtt")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | ZigBee2MQTT | enabled")       
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled")  
                print("System | Services | ZigBee2MQTT | enabled") 
                time.sleep(1)

                # check mqtt connection
                if GET_MQTT_CONNECTION_STATUS() == True:  

                    # check zigbee2mqtt connection      
                    if CHECK_ZIGBEE2MQTT_STARTED():  
                        print("Network | ZigBee2MQTT | connected") 
                        
                        WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | connected")

                        START_DISABLE_ZIGBEE_PAIRING_THREAD()

                        # deactivate pairing at startup
                        if not CHECK_ZIGBEE2MQTT_PAIRING("False"):   

                            heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))    

                            if CHECK_ZIGBEE2MQTT_PAIRING("False"):             
                                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                                SET_ZIGBEE2MQTT_PAIRING_SETTING("False")
                                SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled") 
                            else:             
                                WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                                SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                                SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")

                    else:
                        print("ERROR: Network | ZigBee2MQTT | No Connection") 
                        
                        WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | No Connection")        
                        SEND_EMAIL("ERROR", "Network | ZigBee2MQTT | No Connection")  
                        SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                        SET_ZIGBEE2MQTT_PAIRING_STATUS("No Zigbee2MQTT Connection")        

                else:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | No MQTT connection") 
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("No MQTT connection")                  

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | ZigBee2MQTT | " + str(e)) 
                print("ERROR: System | Services | ZigBee2MQTT | " + str(e))      

        if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True" and zigbee2mqtt_active == "False":

            try:
                os.system("sudo systemctl stop zigbee2mqtt")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | ZigBee2MQTT | disabled")
                SET_ZIGBEE2MQTT_PAIRING_SETTING("False")
                print("System | Services | ZigBee2MQTT | disabled") 
                time.sleep(1)
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | ZigBee2MQTT | " + str(e)) 
                print("ERROR: System | Services | ZigBee2MQTT | " + str(e)) 
    

        #######################
        # logitech media server
        #######################

        if GET_SYSTEM_SETTINGS().lms_active == "False" and lms_active == "True":

            try:
                os.system("sudo systemctl start logitechmediaserver")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | Logitech Media Server | enabled")
                print("System | Services | Logitech Media Server | enabled") 
                time.sleep(1)
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Logitech Media Server | " + str(e)) 
                print("ERROR: System | Services | Logitech Media Server | " + str(e))       

        if GET_SYSTEM_SETTINGS().lms_active == "True" and lms_active == "False":

            try:
                os.system("sudo systemctl stop logitechmediaserver")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services |Logitech Media Server | disabled")
                print("System | Services | Logitech Media Server | disabled") 
                time.sleep(1)
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Logitech Media Server | " + str(e)) 
                print("ERROR: System | Services | Logitech Media Server | " + str(e)) 


        ####################
        # squeezelite player
        ####################

        if GET_SYSTEM_SETTINGS().squeezelite_active == "False" and squeezelite_active == "True":

            try:
                os.system("sudo systemctl start squeezelite")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | Squeezelie Player | enabled")
                print("System | Services | Squeezelie Player | enabled") 
                time.sleep(1)
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Squeezelie Player | " + str(e)) 
                print("ERROR: System | Services | Squeezelie Player | " + str(e))     

        if GET_SYSTEM_SETTINGS().squeezelite_active == "True" and squeezelite_active == "False":

            try:
                os.system("sudo systemctl stop squeezelite")
                WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | Squeezelie Player | disabled")
                print("System | Services | Squeezelie Player | disabled") 
                time.sleep(1)
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Squeezelie Player | " + str(e)) 
                print("ERROR: System | Services | Squeezelie Player | " + str(e)) 


        ###############
        # save settings
        ###############

        if SET_SYSTEM_SERVICE_SETTINGS(zigbee2mqtt_active, lms_active, squeezelite_active):
            success_message_change_settings_services = True


    """ ################## """
    """  settings network  """
    """ ################## """    
                
    if request.form.get("set_settings_network") != None:
        
        if request.form.get("set_checkbox_dhcp"):
            dhcp = "True" 
        else:
            dhcp = "False"  


        # #############
        # dhcp disabled
        # #############

        if dhcp == "False":  

            # first reload of the website after deactivate dhcp, website don't know the values "set_ip_address" and "set_gateway"
            if request.form.get("set_ip_address") != None:          
                save_settings_lan = True
                        
                # ip address
                if request.form.get("set_ip_address") != "":
                    new_ip_address = request.form.get("set_ip_address").strip()  

                    if new_ip_address != ip_address:

                        if CHECK_IP_ADDRESS(new_ip_address) == False:
                            error_message_change_settings_network.append("Network || Invalid IP-Address")
                            save_settings_lan = False
                                
                        elif PING_IP_ADDRESS(new_ip_address) == True or new_ip_address == GET_SYSTEM_SETTINGS().ip_address:
                            error_message_change_settings_network.append("Network || IP-Address already taken")
                            save_settings_lan = False

                        else:
                            ip_address = new_ip_address

                else:
                    error_message_change_settings_network.append("Network || No IP-Address given") 
                    
                # gateway
                if request.form.get("set_gateway") != "":
                    gateway = request.form.get("set_gateway").strip()              

                    if CHECK_IP_ADDRESS(gateway) == False:
                        error_message_change_settings_network.append("Network || Invalid gateway")
                        save_settings_lan = False
                        
                    if CHECK_IP_ADDRESS(gateway) == True and PING_IP_ADDRESS(gateway) == False:
                        error_message_change_settings_network.append("Network || Gateway not found")
                        save_settings_lan = False

                else:
                    error_message_change_settings_network.append("Network || No gateway given") 
                    save_settings_lan = False

                # save settings
                if save_settings_lan == True:
                    changes_saved = False

                    if SET_SYSTEM_NETWORK_SETTINGS(ip_address, gateway, dhcp):
                        changes_saved = True
                    if UPDATE_NETWORK_SETTINGS_LINUX(dhcp, ip_address, gateway):
                        changes_saved = True

                    if changes_saved == True:
                        success_message_change_settings_network = True

            else:
                if SET_SYSTEM_NETWORK_SETTINGS(GET_SYSTEM_SETTINGS().ip_address, GET_SYSTEM_SETTINGS().gateway, dhcp):
                    success_message_change_settings_network = True       


        # ##############
        # dhcp activated
        # ##############

        else:   
            if SET_SYSTEM_NETWORK_SETTINGS(GET_SYSTEM_SETTINGS().ip_address, GET_SYSTEM_SETTINGS().gateway, dhcp):
                success_message_change_settings_network = True            


    """ ################ """
    """  settings email  """
    """ ################ """    
    
    # update email settings
    if request.form.get("update_settings_email") != None:  
        
        server_address = request.form.get("set_server_address").strip()        
        server_port    = request.form.get("set_server_port").strip()  
        encoding       = request.form.get("radio_encoding")
        username       = request.form.get("set_username").strip()  
        password       = request.form.get("set_password").strip()  

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

            message_test_settings_email = "eMail settings are incomplete"    

        else:   
            message_test_settings_email = SEND_EMAIL("TEST", "TEST")


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
    """  backup database """
    """ ################ """    
 
    if request.form.get("backup_database") != None:
        result = BACKUP_DATABASE() 
        
        if result:
            success_message_backup_database = "Backup || Successfully deleted"
        else:
            error_message_backup_database = "Backup || " + str(result)

    system_settings   = GET_SYSTEM_SETTINGS()     
    spotify_settings  = GET_SPOTIFY_SETTINGS()
    email_settings    = GET_EMAIL_SETTINGS()
    list_backup_files = GET_ALL_BACKUP_FILES()

    data = {'navigation': 'settings_system'}

    return render_template('layouts/default.html',
                            data=data,   
                            title=page_title,        
                            description=page_description,                                
                            content=render_template( 'pages/settings_system.html',   
                                                    success_message_change_settings_services=success_message_change_settings_services,
                                                    error_message_change_settings_services=error_message_change_settings_services,
                                                    success_message_change_settings_network=success_message_change_settings_network,                             
                                                    error_message_change_settings_network=error_message_change_settings_network, 
                                                    success_message_change_settings_email=success_message_change_settings_email,                                                       
                                                    error_message_change_settings_email=error_message_change_settings_email,
                                                    message_test_settings_email=message_test_settings_email,                                                     
                                                    success_message_change_settings_spotify=success_message_change_settings_spotify,       
                                                    error_message_change_settings_spotify=error_message_change_settings_spotify,
                                                    error_message_backup_database=error_message_backup_database,                                                       
                                                    success_message_backup_database=success_message_backup_database,                                                                                                     
                                                    message_system=message_system,
                                                    system_settings=system_settings,
                                                    spotify_settings=spotify_settings,
                                                    email_settings=email_settings,                                            
                                                    list_backup_files=list_backup_files,                    
                                                    ) 
                            )

# restore database backup
@app.route('/settings/system/backup_database/restore/<string:filename>')
@login_required
@permission_required
def restore_database_backup(filename):
    result = RESTORE_DATABASE(filename)

    if result == True:
        session['restore_database_success'] = filename + " || Successfully restored"
    else:
        session['restore_database_error'] = filename + " || " + str(result)

    return redirect(url_for('settings_system'))


# delete database backup
@app.route('/settings/system/backup_database/delete/<string:filename>')
@login_required
@permission_required
def delete_database_backup(filename):
    result = DELETE_DATABASE_BACKUP(filename)

    if result == True:
        session['delete_database_success'] = filename + " || Successfully deleted"
    else:
        session['delete_database_error'] = filename + " || " + str(result)

    return redirect(url_for('settings_system'))