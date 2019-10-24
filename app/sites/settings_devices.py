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
        try:
            if current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/settings/devices', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_devices():
    error_message_mqtt = ""
    success_message_change_settings_devices     = []         
    error_message_change_settings_devices       = []    
    success_message_change_settings_exceptions  = False
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
    zigbee_pairing = GET_ZIGBEE2MQTT_PAIRING()

    data = {'navigation': 'settings'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    error_message_device_exceptions = CHECK_DEVICE_EXCEPTION_SETTINGS(GET_ALL_DEVICES("devices")) 

    # get sensor list
    try:
        device_1_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(1).input_values
        device_1_input_values = device_1_input_values.replace(" ", "")
    except:
        device_1_input_values = ""
    try:
        device_2_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(2).input_values
        device_2_input_values = device_2_input_values.replace(" ", "")
    except:
        device_2_input_values = ""
    try:        
        device_3_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(3).input_values
        device_3_input_values = device_3_input_values.replace(" ", "")
    except:
        device_3_input_values = ""
    try:        
        device_4_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(4).input_values
        device_4_input_values = device_4_input_values.replace(" ", "")
    except:
        device_4_input_values = ""
    try:        
        device_5_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(5).input_values
        device_5_input_values = device_5_input_values.replace(" ", "")
    except:
        device_5_input_values = ""
    try:        
        device_6_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(6).input_values
        device_6_input_values = device_6_input_values.replace(" ", "")
    except:
        device_6_input_values = ""
    try:        
        device_7_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(7).input_values
        device_7_input_values = device_7_input_values.replace(" ", "")
    except:
        device_7_input_values = ""
    try:        
        device_8_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(8).input_values
        device_8_input_values = device_8_input_values.replace(" ", "")
    except:
        device_8_input_values = ""
    try:        
        device_9_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(9).input_values
        device_9_input_values = device_9_input_values.replace(" ", "")
    except:
        device_9_input_values = ""
    try:        
        device_10_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(10).input_values
        device_10_input_values = device_10_input_values.replace(" ", "")
    except:
        device_10_input_values = ""
    try:        
        device_11_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(11).input_values
        device_11_input_values = device_11_input_values.replace(" ", "")
    except:
        device_11_input_values = ""
    try:        
        device_12_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(12).input_values
        device_12_input_values = device_12_input_values.replace(" ", "")
    except:
        device_12_input_values = ""
    try:        
        device_13_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(13).input_values
        device_13_input_values = device_13_input_values.replace(" ", "")
    except:
        device_13_input_values = ""
    try:        
        device_14_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(14).input_values
        device_14_input_values = device_14_input_values.replace(" ", "")
    except:
        device_14_input_values = ""
    try:        
        device_15_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(15).input_values
        device_15_input_values = device_15_input_values.replace(" ", "")
    except:
        device_15_input_values = ""    
    try:        
        device_16_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(16).input_values
        device_16_input_values = device_16_input_values.replace(" ", "")
    except:
        device_16_input_values = ""
    try:        
        device_17_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(17).input_values
        device_17_input_values = device_17_input_values.replace(" ", "")
    except:
        device_17_input_values = ""
    try:        
        device_18_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(18).input_values
        device_18_input_values = device_18_input_values.replace(" ", "")
    except:
        device_18_input_values = ""
    try:        
        device_19_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(19).input_values
        device_19_input_values = device_19_input_values.replace(" ", "")
    except:
        device_19_input_values = ""
    try:        
        device_20_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(20).input_values
        device_20_input_values = device_20_input_values.replace(" ", "")
    except:
        device_20_input_values = ""   
    try:        
        device_21_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(21).input_values
        device_21_input_values = device_21_input_values.replace(" ", "")
    except:
        device_21_input_values = ""   
    try:        
        device_22_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(22).input_values
        device_22_input_values = device_22_input_values.replace(" ", "")
    except:
        device_22_input_values = ""   
    try:        
        device_23_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(23).input_values
        device_23_input_values = device_23_input_values.replace(" ", "")
    except:
        device_23_input_values = ""   
    try:        
        device_24_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(24).input_values
        device_24_input_values = device_24_input_values.replace(" ", "")
    except:
        device_24_input_values = ""   
    try:        
        device_25_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(25).input_values
        device_25_input_values = device_25_input_values.replace(" ", "")
    except:
        device_25_input_values = ""

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_devices.html',
                                                    error_message_mqtt=error_message_mqtt,
                                                    success_message_change_settings_devices=success_message_change_settings_devices,
                                                    error_message_change_settings_devices=error_message_change_settings_devices, 
                                                    success_message_change_settings_exceptions=success_message_change_settings_exceptions,
                                                    error_message_device_exceptions=error_message_device_exceptions,
                                                    success_message_zigbee_pairing=success_message_zigbee_pairing,
                                                    error_message_zigbee_pairing=error_message_zigbee_pairing,
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,                                                  
                                                    list_devices=list_devices,
                                                    list_exception_devices=list_exception_devices,
                                                    list_exception_sensors=list_exception_sensors,
                                                    dropdown_list_exception_options=dropdown_list_exception_options,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    zigbee_pairing=zigbee_pairing,
                                                    timestamp=timestamp,      
                                                    device_1_input_values=device_1_input_values,
                                                    device_2_input_values=device_2_input_values,
                                                    device_3_input_values=device_3_input_values,
                                                    device_4_input_values=device_4_input_values,
                                                    device_5_input_values=device_5_input_values,
                                                    device_6_input_values=device_6_input_values,
                                                    device_7_input_values=device_7_input_values,
                                                    device_8_input_values=device_8_input_values,
                                                    device_9_input_values=device_9_input_values,
                                                    device_10_input_values=device_10_input_values,
                                                    device_11_input_values=device_11_input_values,
                                                    device_12_input_values=device_12_input_values,
                                                    device_13_input_values=device_13_input_values,
                                                    device_14_input_values=device_14_input_values,
                                                    device_15_input_values=device_15_input_values,
                                                    device_16_input_values=device_16_input_values,
                                                    device_17_input_values=device_17_input_values,
                                                    device_18_input_values=device_18_input_values,
                                                    device_19_input_values=device_19_input_values,
                                                    device_20_input_values=device_20_input_values,  
                                                    device_21_input_values=device_21_input_values,
                                                    device_22_input_values=device_22_input_values,  
                                                    device_23_input_values=device_23_input_values,
                                                    device_24_input_values=device_24_input_values,
                                                    device_25_input_values=device_25_input_values,                                                                                            
                                                    ) 
                           )


# change device position 
@app.route('/settings/devices/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_device_position(id, direction):
    CHANGE_DEVICE_POSITION(id, direction)
    return redirect(url_for('settings_devices'))


# remove device
@app.route('/settings/devices/delete/<string:ieeeAddr>')
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
             
    return redirect(url_for('settings_devices'))
     
  
# download network topology 
@app.route('/settings/devices/topology/<path:filepath>')
@login_required
@permission_required
def download_devices_topology(filepath): 
    path = GET_PATH() + "/app/static/temp/"
    
    if os.path.isfile(path + filepath) is False:
        return redirect(url_for('settings_devices'))
    
    else:
        return send_from_directory(path, filepath)

  
# download devices logfile
@app.route('/settings/devices/download/<path:filepath>')
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