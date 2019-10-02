from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import CHECK_MQTT, UPDATE_DEVICES, CHECK_ZIGBEE2MQTT_NAME_CHANGED, CHECK_ZIGBEE2MQTT_DEVICE_DELETED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.file_management  import GET_PATH, RESET_LOGFILE, WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import mqtt_message_queue
from app.backend.checks           import CHECK_DEVICE_EXCEPTION_SETTINGS
from app.common                   import COMMON, STATUS
from app.assets                   import *

import datetime
import os
import heapq
import time
import threading

# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        #try:
        if current_user.role == "administrator":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout'))
        #except Exception as e:
        #    print(e)
        #    return redirect(url_for('logout'))
        
    return wrap


@app.route('/devices', methods=['GET', 'POST'])
@login_required
@permission_required
def devices():
    error_message_mqtt = ""
    success_message_change_settings_devices     = []         
    error_message_change_settings_devices       = []    
    success_message_change_settings_exceptions  = False
    success_message_change_settings_mqtt_broker = ""         
    error_message_change_settings_mqtt_broker   = []   
    success_message_zigbee_pairing              = []
    error_message_zigbee_pairing                = []
    success_message_logfile                     = False
    error_message_logfile                       = ""

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # check mqtt
    result = CHECK_MQTT()
    if result != True:
        error_message_mqtt = result

    # delete message
    if session.get('delete_device_success', None) != None:
        success_message_change_settings_devices.append(session.get('delete_device_success'))
        session['delete_device_success'] = None
        
    if session.get('delete_device_error', None) != None:
        error_message_change_settings_devices.append(session.get('delete_device_error'))
        session['delete_device_error'] = None      

    # error download logfile
    if session.get('error_download_log', None) != None:
        error_message_logfile = session.get('error_download_log')
        session['error_download_log'] = None

    """ ############### """
    """  table devices  """
    """ ############### """

    if request.form.get("save_device_settings") != None:  

        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                # rename devices   
                if request.form.get("set_name_" + str(i)) != "":
                                      
                    new_name = request.form.get("set_name_" + str(i))
                    old_name = GET_DEVICE_BY_ID(i).name

                    if new_name != old_name:  

                        # name already exist ?         
                        if not GET_DEVICE_BY_NAME(new_name):  
                            ieeeAddr = GET_DEVICE_BY_ID(i).ieeeAddr   
                            gateway  = GET_DEVICE_BY_ID(i).gateway

                            if gateway == "mqtt":
                                SET_DEVICE_NAME(ieeeAddr, new_name)   
                                success_message_change_settings_devices.append(new_name + " || Einstellungen gespeichert")  
                           
                            if gateway == "zigbee2mqtt":

                                # check mqtt
                                result = CHECK_MQTT()
                                if result != True:
                                    error_message_change_settings_devices.append(result)  
                                
                                else:
                                    channel  = "miranda/zigbee2mqtt/bridge/config/rename"
                                    msg      = '{"old": "' + old_name + '", "new": "' + new_name + '"}'

                                    heapq.heappush(mqtt_message_queue, (20, (channel, msg)))

                                    if CHECK_ZIGBEE2MQTT_NAME_CHANGED(old_name, new_name):
                                        SET_DEVICE_NAME(ieeeAddr, new_name)  
                                        success_message_change_settings_devices.append(new_name + " || Einstellungen gespeichert")       
                                    else:
                                        error_message_change_settings_devices.append(old_name + " || Name konnte nicht verändert werden")       
                        
                        else: 
                            error_message_change_settings_devices.append(old_name + " || Ungültige Eingabe || Name bereits vergeben")  

                else:
                    name = GET_DEVICE_BY_ID(i).name
                    error_message_change_settings_devices.append(name + " || Ungültige Eingabe || Keinen Namen angegeben")    


    # update device list
    if request.form.get("update_devices") != None:     
        result_mqtt        = UPDATE_DEVICES("mqtt")
        result_zigbee2mqtt = UPDATE_DEVICES("zigbee2mqtt")

        if result_mqtt == True and result_zigbee2mqtt == True:
            success_message_change_settings_devices.append("Geräte || Erfolgreich aktualisiert")
        elif result_mqtt != True and result_zigbee2mqtt == True:
            error_message_change_settings_devices.append(result_mqtt)
        elif result_mqtt == True and result_zigbee2mqtt != True:
            error_message_change_settings_devices.append(result_zigbee2mqtt)
        else:
            error_message_change_settings_devices.append(result_mqtt)
            error_message_change_settings_devices.append(result_zigbee2mqtt)


    """ ################## """
    """  table exceptions  """
    """ ################## """

    if request.form.get("save_device_exceptions") != None:  
                
        for i in range (1,21):
            
            try:     
                device = GET_DEVICE_BY_ID(i)
                
                if device in GET_ALL_DEVICES("devices"):
                    
                    
                    # ####################
                    #   Exception Options
                    # ####################

                    exception_option  = request.form.get("set_exception_option_" + str(i))
                    exception_option  = exception_option.replace(" ","")
                    exception_setting = request.form.get("set_exception_setting_" + str(i))
                                            
                    if exception_setting == "" or exception_setting == None:
                        exception_setting = "None"  
        
                    # ######
                    # Sensor
                    # ######

                    if GET_DEVICE_BY_NAME(exception_option) or exception_option.isdigit(): 

                        if exception_option.isdigit():        
                            exception_sensor_ieeeAddr     = GET_DEVICE_BY_ID(exception_option).ieeeAddr
                            exception_sensor_input_values = GET_DEVICE_BY_ID(exception_option).input_values       
                            exception_option              = GET_DEVICE_BY_ID(exception_option).name
                            
                        else:
                            exception_sensor_ieeeAddr     = GET_DEVICE_BY_NAME(exception_option).ieeeAddr
                            exception_sensor_input_values = GET_DEVICE_BY_NAME(exception_option).input_values                                  
                    
                        # set device exception value 1
                        if device.exception_option == "IP-Address":
                            exception_value_1 = "None" 
                    
                        else:
                            exception_value_1 = request.form.get("set_exception_value_1_" + str(i))

                            if exception_value_1 != None:                  
                                exception_value_1 = exception_value_1.replace(" ", "")

                                # replace array_position to sensor name 
                                if exception_value_1.isdigit():
                                    
                                    # first two array elements are no sensors
                                    if exception_value_1 == "0" or exception_value_1 == "1":
                                        exception_value_1 = "None"
                                        
                                    else:           
                                        sensor_list       = GET_DEVICE_BY_IEEEADDR(exception_sensor_ieeeAddr).input_values
                                        sensor_list       = sensor_list.split(",")
                                        exception_value_1 = sensor_list[int(exception_value_1)-2]
                                        
                            else:
                                exception_value_1 = "None" 


                        # set device exception value 2
                        exception_value_2 = request.form.get("set_exception_value_2_" + str(i))
                        
                        if exception_value_2 == "" or exception_value_2 == None:
                            exception_value_2 = "None"       
                        
                        
                        # set device exception value 3
                        exception_value_3 = request.form.get("set_exception_value_3_" + str(i))
                        
                        if exception_value_3 == "" or exception_value_3 == None:
                            exception_value_3 = "None"       


                    # ##########
                    # IP Address
                    # ##########

                    elif exception_option == "IP-Address":
                        
                        # set device exception value 1
                        exception_value_1 = request.form.get("set_exception_value_1_" + str(i))
                        
                        if exception_value_1 == "" or exception_value_1 == None:
                            exception_value_1 = "None" 
                                
                        exception_sensor_ieeeAddr     = "None"
                        exception_sensor_input_values = "None"
                        exception_value_2             = "None"                        
                        exception_value_3             = "None"   
            
                                                            
                    else:
                        
                        exception_option              = "None" 
                        exception_value_1             = "None" 
                        exception_value_2             = "None"  
                        exception_value_3             = "None"  
                        exception_sensor_ieeeAddr     = "None"
                        exception_sensor_input_values = "None"                                                            

                    if SET_DEVICE_EXCEPTION(device.ieeeAddr, exception_option, exception_setting,
                                            exception_sensor_ieeeAddr, exception_sensor_input_values,
                                            exception_value_1, exception_value_2, exception_value_3):
                        
                        success_message_change_settings_exceptions = True  
                
                
                else:
                    
                    if exception_option == "None":
                    
                        exception_setting             = "None" 
                        exception_value_1             = "None" 
                        exception_value_2             = "None"  
                        exception_value_3             = "None"  
                        exception_sensor_ieeeAddr     = "None"
                        exception_sensor_input_values = "None"                                                            

                        SET_DEVICE_EXCEPTION(device.ieeeAddr, exception_option, exception_setting, exception_sensor_ieeeAddr,
                                             exception_sensor_input_values, exception_value_1, exception_value_2, exception_value_3)                   
            
            except Exception as e:
                if "NoneType" not in str(e):
                    print(e)                        


    """ ############# """
    """  mqtt broker  """
    """ ############# """

    if request.form.get("save_mqtt_broker_settings") != None:

        if request.form.get("set_mqtt_broker") != "":                 
            mqtt_broker = request.form.get("set_mqtt_broker")
        else:
            mqtt_broker = ""
            error_message_change_settings_mqtt_broker.append("MQTT Broker || Keinen Broker angegeben")   
             
        mqtt_broker_user     = request.form.get("set_mqtt_broker_user")
        mqtt_broker_password = request.form.get("set_mqtt_broker_password")

        if mqtt_broker != "":
            if SET_MQTT_BROKER_SETTINGS(mqtt_broker, mqtt_broker_user, mqtt_broker_password):
                success_message_change_settings_mqtt_broker = "Einstellungen erfolgreich geändert"


    if request.form.get("restore_mqtt_broker_settings") != None:
        RESTORE_MQTT_BROKER_SETTINGS()
        success_message_change_settings_mqtt_broker = "Einstellungen erfolgreich wiederhergestellt"


    """ ######## """
    """  zigbee  """
    """ ######## """

    def DISABLE_ZIGBEE_PAIRING():
        
        time.sleep(1800)

        SET_ZIGBEE2MQTT_PAIRING("false")

        channel  = "miranda/zigbee2mqtt/bridge/config/permit_join"
        msg      = "false"

        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   
        time.sleep(1)

        if CHECK_ZIGBEE2MQTT_PAIRING("false"):             
            WRITE_LOGFILE_SYSTEM("SUCCESS", "ZigBee2MQTT | Pairing disabled") 
        else:             
            WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | Pairing disabled | Setting not confirmed")  


    # change pairing setting
    if request.form.get("save_zigbee_pairing") != None: 

        # check mqtt
        result = CHECK_MQTT()
        if result != True:  
            error_message_zigbee_pairing.append(result)  

        else:
            setting_pairing = str(request.form.get("radio_zigbee_pairing"))
            
            if setting_pairing == "True":
                    
                channel  = "miranda/zigbee2mqtt/bridge/config/permit_join"
                msg      = "true"

                heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   

                Thread = threading.Thread(target=DISABLE_ZIGBEE_PAIRING)
                Thread.start()                      
                time.sleep(1)

                if CHECK_ZIGBEE2MQTT_PAIRING("true"):             
                    WRITE_LOGFILE_SYSTEM("WARNING", "ZigBee2MQTT | Pairing enabled") 
                    SET_ZIGBEE2MQTT_PAIRING(setting_pairing)
                    success_message_zigbee_pairing.append("Einstellung erfolgreich übernommen") 
                else:             
                    WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | Pairing enabled | Setting not confirmed")   
                    error_message_zigbee_pairing.append("Einstellung nicht bestätigt") 
                                            
            else:
                
                channel  = "miranda/zigbee2mqtt/bridge/config/permit_join"
                msg      = "false"

                heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   
                time.sleep(1)

                if CHECK_ZIGBEE2MQTT_PAIRING("false"):                 
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "ZigBee2MQTT | Pairing disabled") 
                    SET_ZIGBEE2MQTT_PAIRING(setting_pairing)
                    success_message_zigbee_pairing.append("Einstellung erfolgreich übernommen") 
                else:             
                    WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                    error_message_zigbee_pairing.append("Einstellung nicht bestätigt") 


    # request zigbee topology
    if request.form.get("update_zigbee_topology") != None: 
        channel  = "miranda/zigbee2mqtt/bridge/networkmap"
        msg      = "graphviz"

        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))
        time.sleep(5)


    """ ############ """
    """  device log  """
    """ ############ """

    # reset logfile
    if request.form.get("reset_logfile") != None: 
        result = RESET_LOGFILE("log_devices")  

        if result:
            success_message_logfile = True 
        else:
            error_message_logfile = "Reset Log || " + str(result)


    list_exception_devices = GET_ALL_DEVICES("devices")
    list_exception_sensors = GET_ALL_DEVICES("sensors")    

    dropdown_list_exception_options = ["IP-Address"] 
    dropdown_list_operators         = ["=", ">", "<"]
    
    list_devices   = GET_ALL_DEVICES("")
    mqtt_broker    = GET_MQTT_BROKER_SETTINGS()
    zigbee_pairing = GET_ZIGBEE2MQTT_PAIRING()

    data = {'navigation': 'devices', 'notification': ''}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    error_message_device_exceptions = CHECK_DEVICE_EXCEPTION_SETTINGS(GET_ALL_DEVICES("devices")) 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/devices.html',
                                                    error_message_mqtt=error_message_mqtt,
                                                    success_message_change_settings_devices=success_message_change_settings_devices,
                                                    error_message_change_settings_devices=error_message_change_settings_devices, 
                                                    success_message_change_settings_exceptions=success_message_change_settings_exceptions,
                                                    error_message_device_exceptions=error_message_device_exceptions,
                                                    success_message_change_settings_mqtt_broker=success_message_change_settings_mqtt_broker,                                                       
                                                    error_message_change_settings_mqtt_broker=error_message_change_settings_mqtt_broker,    
                                                    success_message_zigbee_pairing=success_message_zigbee_pairing,
                                                    error_message_zigbee_pairing=error_message_zigbee_pairing,
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,                                                  
                                                    list_devices=list_devices,
                                                    list_exception_devices=list_exception_devices,
                                                    list_exception_sensors=list_exception_sensors,
                                                    dropdown_list_exception_options=dropdown_list_exception_options,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    mqtt_broker=mqtt_broker,
                                                    zigbee_pairing=zigbee_pairing,
                                                    timestamp=timestamp,                                               
                                                    ) 
                           )


# change device position 
@app.route('/devices/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_device_position(id, direction):
    CHANGE_DEVICE_POSITION(id, direction)
    return redirect(url_for('devices'))


# remove device
@app.route('/devices/delete/<string:ieeeAddr>')
@login_required
@permission_required
def remove_device(ieeeAddr):
    device_name    = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
    device_gateway = GET_DEVICE_BY_IEEEADDR(ieeeAddr).gateway
    
    result = DELETE_DEVICE(ieeeAddr)
    
    if result == True and device_gateway == "mqtt":
        session['delete_device_success'] = device_name + " || Erfolgreich gelöscht"

    elif result == True and device_gateway == "zigbee2mqtt":
        
        if device_gateway == "zigbee2mqtt":
            channel  = "miranda/zigbee2mqtt/bridge/config/remove"
            msg      = device_name

            heapq.heappush(mqtt_message_queue, (20, (channel, msg)))

            if CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):
                session['delete_device_success'] = device_name + " || Erfolgreich gelöscht"       
            else:
                session['delete_device_error'] = device_name + " || Löschung nicht bestätigt"         
        
    else:
        session['delete_device_error'] = device_name + " || " + str(result)
             
    return redirect(url_for('devices'))
     
  
# download network topology 
@app.route('/devices/topology/<path:filepath>')
@login_required
@permission_required
def download_devices_topology(filepath): 
    path = GET_PATH() + "/data/"
    
    if os.path.isfile(path + filepath) is False:
        return redirect(url_for('devices'))
    
    else:
        return send_from_directory(path, filepath)

  
# download devices logfile
@app.route('/devices/download/<path:filepath>')
@login_required
@permission_required
def download_devices_logfile(filepath): 
    path = GET_PATH() + "/data/logs/"  

    try:
        if os.path.isfile(path + filepath) is False:
            RESET_LOGFILE("log_devices")  
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /data/logs/" + filepath + " | downloaded") 

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /data/logs/" + filepath + " | " + str(e))
        session['error_download_log'] = "Download Log || " + str(e)

    return send_from_directory(path, filepath)