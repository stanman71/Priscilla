from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import UPDATE_DEVICES, CHECK_ZIGBEE2MQTT_NAME_CHANGED, CHECK_ZIGBEE2MQTT_DEVICE_DELETED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.file_management  import GET_PATH, RESET_LOGFILE, WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import mqtt_message_queue, GET_DEVICE_CONNECTION_MQTT, GET_DEVICE_CONNECTION_ZIGBEE2MQTT, SET_ZIGBEE2MQTT_PAIRING_STATUS
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


@app.route('/settings/devices', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_devices():
    page_title       = 'Smarthome | Settings | Devices'
    page_description = 'The devices configuration page.'

    error_message_mqtt_connection               = False
    error_message_zigbee2mqtt_connection        = False    
    success_message_change_settings_devices     = []         
    error_message_change_settings_devices       = []    
    success_message_change_settings_exceptions  = False
    success_message_zigbee_pairing              = []
    error_message_zigbee_pairing                = []
    success_message_logfile                     = False
    error_message_logfile                       = ""

    exceptions_collapse_open = False

    if GET_DEVICE_CONNECTION_MQTT() == False:
        error_message_mqtt_connection = True

    if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":
        if GET_DEVICE_CONNECTION_ZIGBEE2MQTT() == False:
            error_message_zigbee2mqtt_connection = True

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
                                      
                    device     = GET_DEVICE_BY_ID(i)
                    input_name = request.form.get("set_name_" + str(i)).strip()  

                    if input_name != device.name:  

                        # name already exist ?         
                        if not GET_DEVICE_BY_NAME(input_name):  
                            ieeeAddr = device.ieeeAddr   
                            gateway  = device.gateway

                            # add new name
                            if gateway == "mqtt":
                                SET_DEVICE_NAME(ieeeAddr, input_name)   
                                success_message_change_settings_devices.append(input_name + " || Settings successfully saved")  
                           
                            if gateway == "zigbee2mqtt":

                                # check mqtt connection
                                if GET_DEVICE_CONNECTION_MQTT() == True:

                                    # check zigbee service
                                    if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":                                     
                                        channel  = "smarthome/zigbee2mqtt/bridge/config/rename"
                                        msg      = '{"old": "' + device.name + '", "new": "' + input_name + '"}'

                                        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))

                                        if CHECK_ZIGBEE2MQTT_NAME_CHANGED(device.name, input_name):
                                            SET_DEVICE_NAME(ieeeAddr, input_name)  
                                            success_message_change_settings_devices.append(input_name + " || Settings successfully saved")       
                                        else:
                                            error_message_change_settings_devices.append(device.name + " || Name could not be changed")       

                                    else:
                                        error_message_change_settings_devices.append(device.name + " || Zigbee is disabled")    
                        
                        else: 
                            error_message_change_settings_devices.append(device.name + " || Invalid input | Name - " + input_name + " - already taken") 

                    # nothing changed 
                    elif input_name == device.name:  
                        pass

                    else: 
                        error_message_change_settings_devices.append(device.name + " || Invalid input") 


                else:
                    name = device.name
                    error_message_change_settings_devices.append(name + " || Invalid input | No name given")    


    # update device list
    if request.form.get("update_devices") != None:     

        # check mqtt connection
        if GET_DEVICE_CONNECTION_MQTT() == True:  

            result_mqtt        = UPDATE_DEVICES("mqtt")
            result_zigbee2mqtt = UPDATE_DEVICES("zigbee2mqtt")

            if result_mqtt == True and result_zigbee2mqtt == True:
                success_message_change_settings_devices.append("Devices || Successfully updated")
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

        exceptions_collapse_open = True
                
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
                        try:
                            exception_value_1 = request.form.get("set_exception_value_1_" + str(i)).strip()  
                        except:
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

    def DISABLE_ZIGBEE_PAIRING_THREAD():
        
        # check mqtt connection
        if GET_DEVICE_CONNECTION_MQTT() == True:  

            time.sleep(1800)

            SET_ZIGBEE2MQTT_PAIRING("false")

            channel  = "smarthome/zigbee2mqtt/bridge/config/permit_join"
            msg      = "false"

            heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   
            time.sleep(1)

            if CHECK_ZIGBEE2MQTT_PAIRING("false"):             
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled") 
            else:             
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")


    # change pairing setting
    if request.form.get("set_zigbee_pairing") != None: 

        # check mqtt connection
        if GET_DEVICE_CONNECTION_MQTT() != True:  
            error_message_zigbee_pairing.append("No MQTT connection")  

        # check zigbee service
        elif GET_SYSTEM_SETTINGS().zigbee2mqtt_active != "True":  
            error_message_zigbee_pairing.append("Zigbee is disabled")              

        else:
            setting_pairing = str(request.form.get("radio_zigbee2mqtt_pairing"))
            
            if setting_pairing == "True":               
                channel  = "smarthome/zigbee2mqtt/bridge/config/permit_join"
                msg      = "true"

                heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   

                Thread = threading.Thread(target=DISABLE_ZIGBEE_PAIRING_THREAD)
                Thread.start()                      
                time.sleep(1)

                if CHECK_ZIGBEE2MQTT_PAIRING("True"):             
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing enabled | successful") 
                    SET_ZIGBEE2MQTT_PAIRING(setting_pairing)
                    success_message_zigbee_pairing.append("Settings successfully saved") 
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 
                else:             
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Pairing enabled | Setting not confirmed")   
                    error_message_zigbee_pairing.append("Setting not confirmed") 
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")
                                            
            else:         
                channel  = "smarthome/zigbee2mqtt/bridge/config/permit_join"
                msg      = "false"

                heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   
                time.sleep(1)

                if CHECK_ZIGBEE2MQTT_PAIRING("False"):                 
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                    SET_ZIGBEE2MQTT_PAIRING(setting_pairing)
                    success_message_zigbee_pairing.append("Settings successfully saved") 
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled")
                else:             
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                    error_message_zigbee_pairing.append("Setting not confirmed") 
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")


    # request zigbee topology
    if request.form.get("update_zigbee_topology") != None: 

        # check mqtt connection
        if GET_DEVICE_CONNECTION_MQTT() == True and GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

            channel  = "smarthome/zigbee2mqtt/bridge/networkmap"
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
    
    list_devices        = GET_ALL_DEVICES("")
    zigbee2mqtt_pairing = GET_ZIGBEE2MQTT_PAIRING()
    system_services     = GET_SYSTEM_SETTINGS()  

    data = {'navigation': 'settings'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    error_message_device_exceptions = CHECK_DEVICE_EXCEPTION_SETTINGS(GET_ALL_DEVICES("devices")) 

    # get sensor list
    try:
        device_1_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(1).input_values
        device_1_input_values = device_1_input_values.strip()
    except:
        device_1_input_values = ""
    try:
        device_2_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(2).input_values
        device_2_input_values = device_2_input_values.strip()
    except:
        device_2_input_values = ""
    try:        
        device_3_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(3).input_values
        device_3_input_values = device_3_input_values.strip()
    except:
        device_3_input_values = ""
    try:        
        device_4_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(4).input_values
        device_4_input_values = device_4_input_values.strip()
    except:
        device_4_input_values = ""
    try:        
        device_5_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(5).input_values
        device_5_input_values = device_5_input_values.strip()
    except:
        device_5_input_values = ""
    try:        
        device_6_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(6).input_values
        device_6_input_values = device_6_input_values.strip()
    except:
        device_6_input_values = ""
    try:        
        device_7_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(7).input_values
        device_7_input_values = device_7_input_values.strip()
    except:
        device_7_input_values = ""
    try:        
        device_8_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(8).input_values
        device_8_input_values = device_8_input_values.strip()
    except:
        device_8_input_values = ""
    try:        
        device_9_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(9).input_values
        device_9_input_values = device_9_input_values.strip()
    except:
        device_9_input_values = ""
    try:        
        device_10_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(10).input_values
        device_10_input_values = device_10_input_values.strip()
    except:
        device_10_input_values = ""
    try:        
        device_11_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(11).input_values
        device_11_input_values = device_11_input_values.strip()
    except:
        device_11_input_values = ""
    try:        
        device_12_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(12).input_values
        device_12_input_values = device_12_input_values.strip()
    except:
        device_12_input_values = ""
    try:        
        device_13_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(13).input_values
        device_13_input_values = device_13_input_values.strip()
    except:
        device_13_input_values = ""
    try:        
        device_14_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(14).input_values
        device_14_input_values = device_14_input_values.strip()
    except:
        device_14_input_values = ""
    try:        
        device_15_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(15).input_values
        device_15_input_values = device_15_input_values.strip()
    except:
        device_15_input_values = ""    
    try:        
        device_16_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(16).input_values
        device_16_input_values = device_16_input_values.strip()
    except:
        device_16_input_values = ""
    try:        
        device_17_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(17).input_values
        device_17_input_values = device_17_input_values.strip()
    except:
        device_17_input_values = ""
    try:        
        device_18_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(18).input_values
        device_18_input_values = device_18_input_values.strip()
    except:
        device_18_input_values = ""
    try:        
        device_19_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(19).input_values
        device_19_input_values = device_19_input_values.strip()
    except:
        device_19_input_values = ""
    try:        
        device_20_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(20).input_values
        device_20_input_values = device_20_input_values.strip()
    except:
        device_20_input_values = ""   
    try:        
        device_21_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(21).input_values
        device_21_input_values = device_21_input_values.strip()
    except:
        device_21_input_values = ""   
    try:        
        device_22_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(22).input_values
        device_22_input_values = device_22_input_values.strip()
    except:
        device_22_input_values = ""   
    try:        
        device_23_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(23).input_values
        device_23_input_values = device_23_input_values.strip()
    except:
        device_23_input_values = ""   
    try:        
        device_24_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(24).input_values
        device_24_input_values = device_24_input_values.strip()
    except:
        device_24_input_values = ""   
    try:        
        device_25_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(25).input_values
        device_25_input_values = device_25_input_values.strip()
    except:
        device_25_input_values = ""


    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/settings_devices.html',
                                                    error_message_mqtt_connection=error_message_mqtt_connection,
                                                    error_message_zigbee2mqtt_connection=error_message_zigbee2mqtt_connection,
                                                    success_message_change_settings_devices=success_message_change_settings_devices,
                                                    error_message_change_settings_devices=error_message_change_settings_devices, 
                                                    success_message_change_settings_exceptions=success_message_change_settings_exceptions,
                                                    error_message_device_exceptions=error_message_device_exceptions,
                                                    success_message_zigbee_pairing=success_message_zigbee_pairing,
                                                    error_message_zigbee_pairing=error_message_zigbee_pairing,
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,      
                                                    system_services=system_services,                                            
                                                    list_devices=list_devices,
                                                    list_exception_devices=list_exception_devices,
                                                    list_exception_sensors=list_exception_sensors,
                                                    dropdown_list_exception_options=dropdown_list_exception_options,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    zigbee2mqtt_pairing=zigbee2mqtt_pairing,
                                                    timestamp=timestamp,    
                                                    exceptions_collapse_open=exceptions_collapse_open,  
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

    try:
        device_name    = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
        device_gateway = GET_DEVICE_BY_IEEEADDR(ieeeAddr).gateway

        if device_gateway == "mqtt":
            result = DELETE_DEVICE(ieeeAddr)
        
            if result == True:
                session['delete_device_success'] = device_name + " || Device successfully deleted"
            else:
                session['delete_device_error'] = device_name + " || " + str(result)

        if device_gateway == "zigbee2mqtt":

            # check zigbee service
            if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":     

                result = DELETE_DEVICE(ieeeAddr)

                if result == True:
                    channel  = "smarthome/zigbee2mqtt/bridge/config/remove"
                    msg      = device_name

                    heapq.heappush(mqtt_message_queue, (20, (channel, msg)))

                    if CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):
                        session['delete_device_success'] = device_name + " || Device successfully deleted"    

                    # device didn't response (e.g. sensor with battery), force removing from database   
                    else:
                        channel  = "smarthome/zigbee2mqtt/bridge/config/force_remove"
                        msg      = device_name        

                        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))

                        if CHECK_ZIGBEE2MQTT_DEVICE_DELETED(device_name):
                            session['delete_device_success'] = device_name + " || Device successfully deleted"       
                        else:
                            session['delete_device_error'] = device_name + " || Deletion not confirmed"      

                else:
                    session['delete_device_error'] = device_name + " || " + str(result)                   

            else:
                session['delete_device_error'] = device_name + " || Zigbee is disabled"      
               
        return redirect(url_for('settings_devices'))


    except Exception as e:
        session['delete_device_error'] = device_name + " || Error | + " + str(e)            
        return redirect(url_for('settings_devices'))        


 # download zigbee2mqtt log
@app.route('/settings/devices/download/zigbee2mqtt_log/<path:filepath>')
@login_required
@permission_required
def download_zigbee2mqtt_log(filepath): 
    path = GET_PATH() + "/data/logs/zigbee2mqtt/"
    
    if os.path.isfile(path + filepath) == False:
        return redirect(url_for('settings_devices'))
    
    else:
        return send_from_directory(path, filepath)


# download zigbee2mqtt topology 
@app.route('/settings/devices/download/zigbee2mqtt_topology/<path:filepath>')
@login_required
@permission_required
def download_zigbee2mqtt_topology(filepath): 
    path = GET_PATH() + "/app/static/temp/"
    
    if os.path.isfile(path + filepath) == False:
        return redirect(url_for('settings_devices'))
    
    else:
        return send_from_directory(path, filepath)


# download devices logfile
@app.route('/settings/devices/download/devices_log/<path:filepath>')
@login_required
@permission_required
def download_devices_logfile(filepath): 
    path = GET_PATH() + "/data/logs/"  

    try:
        if os.path.isfile(path + filepath) == False:
            RESET_LOGFILE("log_devices")  
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/logs/" + filepath + " | downloaded") 

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/logs/" + filepath + " | " + str(e))
        session['error_download_log'] = "Download Log || " + str(e)

    return send_from_directory(path, filepath)