from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from werkzeug.utils      import secure_filename
from functools           import wraps

from app                          import app
from app.backend.database_models  import *
from app.backend.mqtt             import UPDATE_DEVICES, CHECK_ZIGBEE2MQTT_NAME_CHANGED, CHECK_ZIGBEE2MQTT_DEVICE_DELETED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.file_management  import GET_PATH, RESET_LOGFILE, WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.backend.checks           import CHECK_DEVICE_EXCEPTION_SETTINGS
from app.common                   import COMMON, STATUS
from app.assets                   import *


import datetime
import os
import heapq
import time
import threading
import urllib.request


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
"""  upload firmware  """
""" ################# """   

def UPLOAD_FIRMWARE(file):
    ALLOWED_EXTENSIONS = set(['bin'])

    def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    

    # check fileformat
    try:
        firmware_device_model = str(file.filename.rsplit("_", 1)[0])
        firmware_version      = float(file.filename.rsplit("_", 1)[1].replace(".bin",""))

    except:
        firmware_device_model = None
        firmware_version      = None         

    if file.filename == '':
        result = "No file founded"

    elif ".bin" not in file.filename:
        result = "Invalid file ending (only .bin)"

    elif "_" not in file.filename:
        result = "Invalid filename (Format: [Device_Model]_[Version].bin || NO SPACES)" 
    
    elif isinstance(firmware_device_model, str) == False or isinstance(firmware_version, float) == False:
        result = "Invalid filename (Format: [Device_Model]_[Version].bin || NO SPACES)"      

    elif file.filename in GET_ALL_MQTT_FIRMWARE_FILES():
        result = "File already exist" 

    elif file and allowed_file(file.filename):

        try:
            # check existing device_models     
            device_founded = False

            for device in GET_ALL_DEVICES("mqtt"):  

                if firmware_device_model.lower() == device.model.lower() and device.device_type != "client_music":
                    device_founded = True 
            
            if device_founded == False:
                result = "Device_Model not founded"   
                return result    

            # check existing firmwares
            for firmware in GET_ALL_MQTT_FIRMWARE_FILES():
                if firmware_device_model in firmware:
                    
                    if firmware_version < float(firmware.rsplit("_", 1)[1].replace(".bin","")):
                        result = "Newer Firmware already exist" 
                        return result

                    else:
                        DELETE_MQTT_FIRMWARE(firmware)

        except Exception as e:
            return ("Error Firmware upload: " + str(e))            

        # upload new file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result = True
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /firmwares/" + file.filename + " | uploaded")

    else:
        result = "File upload error" 

    return result




@app.route('/settings/devices', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_devices():
    page_title       = 'homatiX | Settings | Devices'
    page_description = 'The devices configuration page.'

    error_message_mqtt_connection               = False
    error_message_zigbee2mqtt_connection        = False    
    success_message_change_settings_devices     = []         
    error_message_change_settings_devices       = []    
    success_message_change_settings_exceptions  = False
    success_message_mqtt_firmware_upload        = False
    error_message_firmware_upload               = ""
    error_message_zigbee_device_update          = False
    success_message_zigbee_pairing              = []
    error_message_zigbee_pairing                = []
    success_message_logfile                     = False
    error_message_logfile                       = ""
    error_message_firmware                      = ""
    error_download_log_zigbee2mqtt              = ""
    error_download_topology_zigbee2mqtt         = ""    

    exceptions_collapse_open                    = False    
    mqtt_device_update_collapse_open            = False
    zigbee_device_update_collapse_open          = False


    # error firmware
    if session.get('error_firmware', None) != None:
        error_message_firmware = session.get('error_firmware') 
        session['error_firmware'] = None

    # error download log_zigbee2mqtt  
    if session.get('error_download_log_zigbee2mqtt', None) != None:
        error_download_log_zigbee2mqtt = session.get('error_download_log_zigbee2mqtt') 
        session['error_download_log_zigbee2mqtt'] = None

    # error download topology_zigbee2mqtt  
    if session.get('error_download_topology_zigbee2mqtt', None) != None:
        error_download_topology_zigbee2mqtt = session.get('error_download_topology_zigbee2mqtt') 
        session['error_download_topology_zigbee2mqtt'] = None

    # error log_devices  
    if session.get('error_download_log_devices', None) != None:
        error_message_logfile = session.get('error_download_log_devices') 
        session['error_download_log_devices'] = None


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


    # zigbee device update started
    if session.get('zigbee_device_update_started', None) != None:
        session['zigbee_device_update_started'] = None
        zigbee_device_update_collapse_open      = True

    # error zigbee device update
    if session.get('zigbee_device_update_running', None) != None:
        error_message_zigbee_device_update      = True
        session['zigbee_device_update_running'] = None
        zigbee_device_update_collapse_open      = True


    """ ############### """
    """  table devices  """
    """ ############### """

    if request.form.get("save_device_settings") != None:  

        for i in range (1,100):

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


                    # auto update setting
                    if request.form.get("set_checkbox_auto_update_" + str(i)):
                        auto_update = "True"
                    else:
                        auto_update = "False"

                    SET_DEVICE_AUTO_UPDATE(device.ieeeAddr, auto_update)

       
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

        for i in range (1,100):

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


    """ ###### """
    """  mqtt  """
    """ ###### """

    if request.form.get("upload_mqtt_firmware") != None: 
        mqtt_device_update_collapse_open = True

        # check if the post request has the file part
        if "file" not in request.files:
            error_message_firmware_upload = "No file founded"

        else:
            file   = request.files['file']
            result = UPLOAD_FIRMWARE(file)

            if result == True:
                success_message_mqtt_firmware_upload = True

            else:
                error_message_firmware_upload = result


    """ ######## """
    """  zigbee  """
    """ ######## """

    # change pairing setting
    if request.form.get("set_zigbee_pairing") != None: 

        # check mqtt connection
        if GET_DEVICE_CONNECTION_MQTT() != True:  
            error_message_zigbee_pairing.append("No MQTT connection")  

        # check zigbee service
        elif GET_SYSTEM_SETTINGS().zigbee2mqtt_active != "True":  
            error_message_zigbee_pairing.append("Zigbee is disabled")              

        else:
            setting_pairing = str(request.form.get("radio_zigbee2mqtt_pairing_setting"))
            
            if setting_pairing == "True":               
                heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "true")))   

                SET_ZIGBEE_PAIRING_TIMER("True")          

                if CHECK_ZIGBEE2MQTT_PAIRING("True"):             
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing enabled | successful") 

                    SET_ZIGBEE2MQTT_PAIRING_SETTING("True")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Searching for new Devices...") 
                    success_message_zigbee_pairing.append("Setting successfully changed")                     
                else:             
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing enabled | Setting not confirmed")   
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")
                    error_message_zigbee_pairing.append("Setting not confirmed")                     
                                            
            else:         
                heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))   
               
                SET_ZIGBEE_PAIRING_TIMER("False")

                if CHECK_ZIGBEE2MQTT_PAIRING("False"):                 
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("False")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled")
                    success_message_zigbee_pairing.append("Setting successfully changed") 
                else:             
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")
                    error_message_zigbee_pairing.append("Setting not confirmed") 


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
    
    list_devices                = GET_ALL_DEVICES("")
    zigbee2mqtt_pairing_setting = GET_ZIGBEE2MQTT_PAIRING_SETTING()
    system_services             = GET_SYSTEM_SETTINGS()   
    list_mqtt_firmware_files    = GET_ALL_MQTT_FIRMWARE_FILES()

    if GET_ZIGBEE_DEVICE_UPDATE_STATUS() != "No Device Update available":
        show_zigbee_device_updates = True
    else:
        show_zigbee_device_updates = False

    data = {'navigation': 'settings_devices'}

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
    try:        
        device_26_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(26).input_values
        device_26_input_values = device_26_input_values.strip()
    except:
        device_26_input_values = ""
    try:        
        device_27_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(27).input_values
        device_27_input_values = device_27_input_values.strip()
    except:
        device_27_input_values = ""
    try:        
        device_28_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(28).input_values
        device_28_input_values = device_28_input_values.strip()
    except:
        device_28_input_values = ""
    try:        
        device_29_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(29).input_values
        device_29_input_values = device_29_input_values.strip()
    except:
        device_29_input_values = ""
    try:        
        device_30_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(30).input_values
        device_30_input_values = device_30_input_values.strip()
    except:
        device_30_input_values = ""
    try:        
        device_31_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(31).input_values
        device_31_input_values = device_31_input_values.strip()
    except:
        device_31_input_values = ""
    try:        
        device_32_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(32).input_values
        device_32_input_values = device_32_input_values.strip()
    except:
        device_32_input_values = ""
    try:        
        device_33_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(33).input_values
        device_33_input_values = device_33_input_values.strip()
    except:
        device_33_input_values = ""
    try:        
        device_34_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(34).input_values
        device_34_input_values = device_34_input_values.strip()
    except:
        device_34_input_values = ""
    try:        
        device_35_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(35).input_values
        device_35_input_values = device_35_input_values.strip()
    except:
        device_35_input_values = ""
    try:        
        device_36_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(36).input_values
        device_36_input_values = device_36_input_values.strip()
    except:
        device_36_input_values = ""
    try:        
        device_37_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(37).input_values
        device_37_input_values = device_37_input_values.strip()
    except:
        device_37_input_values = ""
    try:        
        device_38_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(38).input_values
        device_38_input_values = device_38_input_values.strip()
    except:
        device_38_input_values = ""
    try:        
        device_39_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(39).input_values
        device_39_input_values = device_39_input_values.strip()
    except:
        device_39_input_values = ""
    try:        
        device_40_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(40).input_values
        device_40_input_values = device_40_input_values.strip()
    except:
        device_40_input_values = ""
    try:        
        device_41_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(41).input_values
        device_41_input_values = device_41_input_values.strip()
    except:
        device_41_input_values = ""
    try:        
        device_42_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(42).input_values
        device_42_input_values = device_42_input_values.strip()
    except:
        device_42_input_values = ""
    try:        
        device_43_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(43).input_values
        device_43_input_values = device_43_input_values.strip()
    except:
        device_43_input_values = ""
    try:        
        device_44_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(44).input_values
        device_44_input_values = device_44_input_values.strip()
    except:
        device_44_input_values = ""
    try:        
        device_45_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(45).input_values
        device_45_input_values = device_45_input_values.strip()
    except:
        device_45_input_values = ""
    try:        
        device_46_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(46).input_values
        device_46_input_values = device_46_input_values.strip()
    except:
        device_46_input_values = ""
    try:        
        device_47_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(47).input_values
        device_47_input_values = device_47_input_values.strip()
    except:
        device_47_input_values = ""
    try:        
        device_48_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(48).input_values
        device_48_input_values = device_48_input_values.strip()
    except:
        device_48_input_values = ""
    try:        
        device_49_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(49).input_values
        device_49_input_values = device_49_input_values.strip()
    except:
        device_49_input_values = ""
    try:        
        device_50_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(50).input_values
        device_50_input_values = device_50_input_values.strip()
    except:
        device_50_input_values = ""
    try:        
        device_51_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(51).input_values
        device_51_input_values = device_51_input_values.strip()
    except:
        device_51_input_values = ""
    try:        
        device_52_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(52).input_values
        device_52_input_values = device_52_input_values.strip()
    except:
        device_52_input_values = ""
    try:        
        device_53_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(53).input_values
        device_53_input_values = device_53_input_values.strip()
    except:
        device_53_input_values = ""
    try:        
        device_54_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(54).input_values
        device_54_input_values = device_54_input_values.strip()
    except:
        device_54_input_values = ""
    try:        
        device_55_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(55).input_values
        device_55_input_values = device_55_input_values.strip()
    except:
        device_55_input_values = ""
    try:        
        device_56_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(56).input_values
        device_56_input_values = device_56_input_values.strip()
    except:
        device_56_input_values = ""
    try:        
        device_57_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(57).input_values
        device_57_input_values = device_57_input_values.strip()
    except:
        device_57_input_values = ""
    try:        
        device_58_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(58).input_values
        device_58_input_values = device_58_input_values.strip()
    except:
        device_58_input_values = ""
    try:        
        device_59_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(59).input_values
        device_59_input_values = device_59_input_values.strip()
    except:
        device_59_input_values = ""
    try:        
        device_60_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(60).input_values
        device_60_input_values = device_60_input_values.strip()
    except:
        device_60_input_values = ""
    try:        
        device_61_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(61).input_values
        device_61_input_values = device_61_input_values.strip()
    except:
        device_61_input_values = ""
    try:        
        device_62_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(62).input_values
        device_62_input_values = device_62_input_values.strip()
    except:
        device_62_input_values = ""
    try:        
        device_63_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(63).input_values
        device_63_input_values = device_63_input_values.strip()
    except:
        device_63_input_values = ""
    try:        
        device_64_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(64).input_values
        device_64_input_values = device_64_input_values.strip()
    except:
        device_64_input_values = ""
    try:        
        device_65_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(65).input_values
        device_65_input_values = device_65_input_values.strip()
    except:
        device_65_input_values = ""
    try:        
        device_66_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(66).input_values
        device_66_input_values = device_66_input_values.strip()
    except:
        device_66_input_values = ""
    try:        
        device_67_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(67).input_values
        device_67_input_values = device_67_input_values.strip()
    except:
        device_67_input_values = ""
    try:        
        device_68_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(68).input_values
        device_68_input_values = device_68_input_values.strip()
    except:
        device_68_input_values = ""
    try:        
        device_69_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(69).input_values
        device_69_input_values = device_69_input_values.strip()
    except:
        device_69_input_values = ""
    try:        
        device_70_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(70).input_values
        device_70_input_values = device_70_input_values.strip()
    except:
        device_70_input_values = ""
    try:        
        device_71_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(71).input_values
        device_71_input_values = device_71_input_values.strip()
    except:
        device_71_input_values = ""
    try:        
        device_72_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(72).input_values
        device_72_input_values = device_72_input_values.strip()
    except:
        device_72_input_values = ""
    try:        
        device_73_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(73).input_values
        device_73_input_values = device_73_input_values.strip()
    except:
        device_73_input_values = ""
    try:        
        device_74_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(74).input_values
        device_74_input_values = device_74_input_values.strip()
    except:
        device_74_input_values = ""
    try:        
        device_75_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(75).input_values
        device_75_input_values = device_75_input_values.strip()
    except:
        device_75_input_values = ""
    try:        
        device_76_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(76).input_values
        device_76_input_values = device_76_input_values.strip()
    except:
        device_76_input_values = ""
    try:        
        device_77_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(77).input_values
        device_77_input_values = device_77_input_values.strip()
    except:
        device_77_input_values = ""
    try:        
        device_78_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(78).input_values
        device_78_input_values = device_78_input_values.strip()
    except:
        device_78_input_values = ""
    try:        
        device_79_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(79).input_values
        device_79_input_values = device_79_input_values.strip()
    except:
        device_79_input_values = ""
    try:        
        device_80_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(80).input_values
        device_80_input_values = device_80_input_values.strip()
    except:
        device_80_input_values = ""
    try:        
        device_81_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(81).input_values
        device_81_input_values = device_81_input_values.strip()
    except:
        device_81_input_values = ""
    try:        
        device_82_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(82).input_values
        device_82_input_values = device_82_input_values.strip()
    except:
        device_82_input_values = ""
    try:        
        device_83_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(83).input_values
        device_83_input_values = device_83_input_values.strip()
    except:
        device_83_input_values = ""
    try:        
        device_84_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(84).input_values
        device_84_input_values = device_84_input_values.strip()
    except:
        device_84_input_values = ""
    try:        
        device_85_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(85).input_values
        device_85_input_values = device_85_input_values.strip()
    except:
        device_85_input_values = ""
    try:        
        device_86_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(86).input_values
        device_86_input_values = device_86_input_values.strip()
    except:
        device_86_input_values = ""
    try:        
        device_87_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(87).input_values
        device_87_input_values = device_87_input_values.strip()
    except:
        device_87_input_values = ""
    try:        
        device_88_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(88).input_values
        device_88_input_values = device_88_input_values.strip()
    except:
        device_88_input_values = ""
    try:        
        device_89_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(89).input_values
        device_89_input_values = device_89_input_values.strip()
    except:
        device_89_input_values = ""
    try:        
        device_90_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(90).input_values
        device_90_input_values = device_90_input_values.strip()
    except:
        device_90_input_values = ""
    try:        
        device_91_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(91).input_values
        device_91_input_values = device_91_input_values.strip()
    except:
        device_91_input_values = ""
    try:        
        device_92_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(92).input_values
        device_92_input_values = device_92_input_values.strip()
    except:
        device_92_input_values = ""
    try:        
        device_93_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(93).input_values
        device_93_input_values = device_93_input_values.strip()
    except:
        device_93_input_values = ""
    try:        
        device_94_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(94).input_values
        device_94_input_values = device_94_input_values.strip()
    except:
        device_94_input_values = ""
    try:        
        device_95_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(95).input_values
        device_95_input_values = device_95_input_values.strip()
    except:
        device_95_input_values = ""
    try:        
        device_96_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(96).input_values
        device_96_input_values = device_96_input_values.strip()
    except:
        device_96_input_values = ""
    try:        
        device_97_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(97).input_values
        device_97_input_values = device_97_input_values.strip()
    except:
        device_97_input_values = ""
    try:        
        device_98_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(98).input_values
        device_98_input_values = device_98_input_values.strip()
    except:
        device_98_input_values = ""
    try:        
        device_99_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(99).input_values
        device_99_input_values = device_99_input_values.strip()
    except:
        device_99_input_values = ""        

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
                                                    success_message_mqtt_firmware_upload=success_message_mqtt_firmware_upload,
                                                    error_message_firmware_upload=error_message_firmware_upload,
                                                    error_message_zigbee_device_update=error_message_zigbee_device_update,
                                                    success_message_zigbee_pairing=success_message_zigbee_pairing,
                                                    error_message_zigbee_pairing=error_message_zigbee_pairing,
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,   
                                                    error_message_firmware=error_message_firmware,  
                                                    error_download_log_zigbee2mqtt=error_download_log_zigbee2mqtt,
                                                    error_download_topology_zigbee2mqtt=error_download_topology_zigbee2mqtt,
                                                    system_services=system_services,                                            
                                                    list_devices=list_devices,
                                                    list_exception_devices=list_exception_devices,
                                                    list_exception_sensors=list_exception_sensors,
                                                    dropdown_list_exception_options=dropdown_list_exception_options,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    list_mqtt_firmware_files=list_mqtt_firmware_files,
                                                    zigbee2mqtt_pairing_setting=zigbee2mqtt_pairing_setting,
                                                    timestamp=timestamp,  
                                                    show_zigbee_device_updates=show_zigbee_device_updates,                                                      
                                                    zigbee_device_update_collapse_open=zigbee_device_update_collapse_open,
                                                    mqtt_device_update_collapse_open=mqtt_device_update_collapse_open,
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
                                                    device_26_input_values=device_26_input_values,  
                                                    device_27_input_values=device_27_input_values,  
                                                    device_28_input_values=device_28_input_values,  
                                                    device_29_input_values=device_29_input_values,  
                                                    device_30_input_values=device_30_input_values,     
                                                    device_31_input_values=device_31_input_values,  
                                                    device_32_input_values=device_32_input_values,  
                                                    device_33_input_values=device_33_input_values,  
                                                    device_34_input_values=device_34_input_values,  
                                                    device_35_input_values=device_35_input_values,     
                                                    device_36_input_values=device_36_input_values,  
                                                    device_37_input_values=device_37_input_values,  
                                                    device_38_input_values=device_38_input_values,  
                                                    device_39_input_values=device_39_input_values,          
                                                    device_40_input_values=device_40_input_values,     
                                                    device_41_input_values=device_41_input_values,  
                                                    device_42_input_values=device_42_input_values,  
                                                    device_43_input_values=device_43_input_values,  
                                                    device_44_input_values=device_44_input_values,  
                                                    device_45_input_values=device_45_input_values,     
                                                    device_46_input_values=device_46_input_values,  
                                                    device_47_input_values=device_47_input_values,  
                                                    device_48_input_values=device_48_input_values,  
                                                    device_49_input_values=device_49_input_values,     
                                                    device_50_input_values=device_50_input_values,     
                                                    device_51_input_values=device_51_input_values,  
                                                    device_52_input_values=device_52_input_values,  
                                                    device_53_input_values=device_53_input_values,  
                                                    device_54_input_values=device_54_input_values,  
                                                    device_55_input_values=device_55_input_values,     
                                                    device_56_input_values=device_56_input_values,  
                                                    device_57_input_values=device_57_input_values,  
                                                    device_58_input_values=device_58_input_values,  
                                                    device_59_input_values=device_59_input_values,     
                                                    device_60_input_values=device_60_input_values,     
                                                    device_61_input_values=device_61_input_values,  
                                                    device_62_input_values=device_62_input_values,  
                                                    device_63_input_values=device_63_input_values,  
                                                    device_64_input_values=device_64_input_values,  
                                                    device_65_input_values=device_65_input_values,     
                                                    device_66_input_values=device_66_input_values,  
                                                    device_67_input_values=device_67_input_values,  
                                                    device_68_input_values=device_68_input_values,  
                                                    device_69_input_values=device_69_input_values,     
                                                    device_70_input_values=device_70_input_values,     
                                                    device_71_input_values=device_71_input_values,  
                                                    device_72_input_values=device_72_input_values,  
                                                    device_73_input_values=device_73_input_values,  
                                                    device_74_input_values=device_74_input_values,  
                                                    device_75_input_values=device_75_input_values,     
                                                    device_76_input_values=device_76_input_values,  
                                                    device_77_input_values=device_77_input_values,  
                                                    device_78_input_values=device_78_input_values,  
                                                    device_79_input_values=device_79_input_values,     
                                                    device_80_input_values=device_80_input_values,     
                                                    device_81_input_values=device_81_input_values,  
                                                    device_82_input_values=device_82_input_values,  
                                                    device_83_input_values=device_83_input_values,  
                                                    device_84_input_values=device_84_input_values,  
                                                    device_85_input_values=device_85_input_values,     
                                                    device_86_input_values=device_86_input_values,  
                                                    device_87_input_values=device_87_input_values,  
                                                    device_88_input_values=device_88_input_values,  
                                                    device_89_input_values=device_89_input_values,     
                                                    device_90_input_values=device_90_input_values,     
                                                    device_91_input_values=device_91_input_values,  
                                                    device_92_input_values=device_92_input_values,  
                                                    device_93_input_values=device_93_input_values,  
                                                    device_94_input_values=device_94_input_values,  
                                                    device_95_input_values=device_95_input_values,     
                                                    device_96_input_values=device_96_input_values,  
                                                    device_97_input_values=device_97_input_values,  
                                                    device_98_input_values=device_98_input_values,  
                                                    device_99_input_values=device_99_input_values,                                                         
                                                    ) 
                           )


# change devices position 
@app.route('/settings/devices/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_devices_position(id, direction):
    CHANGE_DEVICES_POSITION(id, direction)
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


# download mqtt firmware
@app.route('/settings/devices/firmware/download/<string:filename>')
@login_required
@permission_required
def download_mqtt_firmware(filename):
    try:
        path = GET_PATH() + "/firmwares/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /firmwares/" + filename + " | downloaded")
        return send_from_directory(path, filename)
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /firmwares/" + filename + " | " + str(e)) 
        session['error_firmware'] = "Download Firmware || " + str(e)


# request mqtt firmware
@app.route('/settings/devices/firmware/request', methods=['GET', 'POST'])
def request_mqtt_firmware():
    try:
        path = GET_PATH() + "/firmwares/"     

        device_ieeeAddr = request.args.get('device_ieeeAddr', default=None)
        current_version = request.args.get('current_version', default=None)

        device = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr)

        if device.auto_update == "True":

            # load existing firmware files
            for firmware in GET_ALL_MQTT_FIRMWARE_FILES():
                firmware_device_model = str(firmware.rsplit("_", 1)[0])
                firmware_version      = float(firmware.rsplit("_", 1)[1].replace(".bin",""))

                if device.model.lower() == firmware_device_model.lower() and float(current_version) < firmware_version:     
                    return send_from_directory(path, firmware, as_attachment=True, mimetype='application/octet-stream', attachment_filename=firmware)

        return 'No update needed', 304
        
    except Exception as e:
        return 'Error: ' + str(e), 400


# delete mqtt firmware
@app.route('/settings/devices/firmware/delete/<string:filename>')
@login_required
@permission_required
def delete_mqtt_firmware(filename):
    result = DELETE_MQTT_FIRMWARE(filename)

    if result != True:
        session['error_firmware'] = result

    return redirect(url_for('settings_devices'))


# update zigbee device 
@app.route('/settings/devices/firmware/update/<string:ieeeAddr>')
@login_required
@permission_required
def update_zigbee_device(ieeeAddr):
    if GET_ZIGBEE_DEVICE_UPDATE_STATUS() == "" or GET_ZIGBEE_DEVICE_UPDATE_STATUS() == "Device Update founded":
        channel  = "smarthome/zigbee2mqtt/bridge/ota_update/update"
        msg      = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name

        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))
        session['zigbee_device_update_started'] = "True" 

    else:
        session['zigbee_device_update_running'] = "True"

    return redirect(url_for('settings_devices'))


# download zigbee topology 
@app.route('/settings/devices/topology/download/<string:filename>')
@login_required
@permission_required
def download_zigbee_topology(filename): 
    path = GET_PATH() + "/app/static/temp/"
    
    if os.path.isfile(path + filename) == False:
        session['error_download_topology_zigbee2mqtt'] = "Download Topology || File not founded" 
        return redirect(url_for('settings_devices'))
    
    else:
        return send_from_directory(path, filename)


# download logs
@app.route('/settings/devices/log/download/<string:filename>')
@login_required
@permission_required
def download_logs(filename): 
    path = GET_PATH() + "/data/logs/"
    
    if os.path.isfile(path + filename) == False:

        if filename == "zigbee2mqtt.txt":
            session['error_download_log_zigbee2mqtt'] = "Download Log || File not founded" 
            return redirect(url_for('settings_devices'))

        if filename == "log_devices.csv":
            session['error_download_log_devices'] = "Download Log || File not founded"  
    
    else:
        return send_from_directory(path, filename)