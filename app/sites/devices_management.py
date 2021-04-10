from flask                        import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                  import current_user, login_required
from werkzeug.exceptions          import HTTPException, NotFound, abort
from werkzeug.utils               import secure_filename
from functools                    import wraps

from app                          import app
from app.backend.database_models  import *
from app.backend.mqtt             import UPDATE_DEVICES, CHECK_ZIGBEE2MQTT_NAME_CHANGED, CHECK_ZIGBEE2MQTT_DEVICE_DELETED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.file_management  import GET_PATH, RESET_LOGFILE, WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.backend.checks           import CHECK_DEVICE_EXCEPTION_SETTINGS
from app.backend.user_id          import SET_CURRENT_USER_ID
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
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################")
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
        result = "No file found"

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
            device_found = False

            for device in GET_ALL_DEVICES("mqtt"):  

                if firmware_device_model.lower() == device.model.lower() and device.device_type != "client_music":
                    device_found = True 
            
            if device_found == False:
                result = "Device_Model not found"   
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


@app.route('/devices/management', methods=['GET', 'POST'])
@login_required
@permission_required
def devices_management():
    page_title       = 'Bianca | Devices | Management'
    page_description = 'The devices configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    error_message_mqtt_connection            = False
    error_message_zigbee2mqtt_connection     = False    
    success_message_change_settings_devices  = []     
    error_message_change_settings_devices    = []    
    success_message_add_device_exception     = False
    error_message_add_device_exception       = []        
    success_message_change_device_exceptions = []
    error_message_change_device_exceptions   = []
    success_message_mqtt_manually_adding     = False
    error_message_mqtt_manually_adding       = []
    success_message_mqtt_firmware_upload     = False
    error_message_mqtt_firmware_upload       = ""
    error_message_zigbee_device_update       = False
    success_message_zigbee_pairing           = []
    error_message_zigbee_pairing             = []
    success_message_logfile                  = False
    error_message_logfile                    = ""
    error_message_mqtt_firmware              = ""
    error_download_log_zigbee2mqtt           = ""
    error_download_topology_zigbee2mqtt      = ""    

    device_exceptions_collapse_open          = False    
    mqtt_device_update_collapse_open         = False
    zigbee_device_update_collapse_open       = False
    zigbee_topology_exist                    = False


    # error firmware
    if session.get('error_mqtt_firmware', None) != None:
        error_message_mqtt_firmware = session.get('error_mqtt_firmware') 
        session['error_mqtt_firmware'] = None

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


    if GET_MQTT_CONNECTION_STATUS() == False:
        error_message_mqtt_connection = True

    if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":
        if GET_ZIGBEE2MQTT_CONNECTION_STATUS() == False:
            error_message_zigbee2mqtt_connection = True

    # delete device message
    if session.get('delete_device_success', None) != None:
        success_message_change_settings_devices.append(session.get('delete_device_success'))
        session['delete_device_success'] = None
        
    if session.get('delete_device_error', None) != None:
        error_message_change_settings_devices.append(session.get('delete_device_error'))
        session['delete_device_error'] = None      

    # delete device exception message
    if session.get('delete_device_exception_success', None) != None:
        device_exceptions_collapse_open = True
        success_message_change_device_exceptions.append(session.get('delete_device_exception_success'))
        session['delete_device_exception_success'] = None
        
    if session.get('delete_device_exception_error', None) != None:
        device_exceptions_collapse_open = True
        error_message_change_settings_devices.append(session.get('delete_device_exception_error'))
        session['delete_device_exception_error'] = None      

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
                                if GET_MQTT_CONNECTION_STATUS() == True:

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
        if GET_MQTT_CONNECTION_STATUS() == True:  

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


    """ ########################## """
    """  add mqtt device manually  """
    """ ########################## """

    if request.form.get("add_mqtt_device_manually") != None: 

        ieeeAddr = request.form.get("set_mqtt_device_ieeeAddr_manually_adding")
        model    = request.form.get("set_mqtt_device_model_manually_adding")

        # no ieeeAddr found        
        if ieeeAddr == "":  
            error_message_mqtt_manually_adding.append("Invalid input | No ieeeAddr found")
           
        # ieeeAddr already taken
        if GET_DEVICE_BY_IEEEADDR(ieeeAddr) != None:
            error_message_mqtt_manually_adding.append("Invalid input | ieeeAddr - " + ieeeAddr + " - already taken")

        # no model selected
        if model == "":
            error_message_mqtt_manually_adding.append("Invalid input | No Device selected")   

        # no errors found
        if error_message_mqtt_manually_adding == []:

            new_device = GET_MQTT_DEVICE_MANUALLY_ADDING_INFORMATIONS(model)
        
            name          = ieeeAddr
            gateway       = "mqtt"
            device_type   = new_device[0]
            version       = ""                                            
            description   = new_device[1]
            input_values  = new_device[2]
            input_trigger = new_device[3]  
            commands      = new_device[4]                                
            commands_json = new_device[5] 

            result = ADD_DEVICE(name, gateway, ieeeAddr, model, device_type, version, description, input_values, input_trigger, commands, commands_json) 

            if result == True:
                success_message_mqtt_manually_adding = True
            else:
                error_message_mqtt_manually_adding.append(result)
        

    """ ######################### """
    """  table device exceptions  """
    """ ######################### """

    if request.form.get("add_device_exception") != None:  
        device_exceptions_collapse_open = True

        ieeeAddr = request.form.get("set_mqtt_device_exception_ieeeAddr")

        if ieeeAddr != "":    

            result = ADD_DEVICE_EXCEPTION(ieeeAddr)

            if result == True:
                success_message_add_device_exception = True
            else:
                error_message_add_device_exception = result

        else:
            error_message_add_device_exception = ["Invalid input | No Device selected"]                        


    if request.form.get("save_device_exceptions") != None:  
        device_exceptions_collapse_open = True

        for i in range (1,26):

            if request.form.get("set_exception_option_" + str(i)) != None:
                
                # #################
                # Exception Options
                # #################

                exception_option  = request.form.get("set_exception_option_" + str(i)).strip()
                exception_command = request.form.get("set_exception_command_" + str(i))
                                        
                if exception_command == "" or exception_command == None:
                    exception_command = "None"  

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
                    if exception_option == "IP-ADDRESS":
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

                elif exception_option == "IP-ADDRESS":
                    
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

                if UPDATE_DEVICE_EXCEPTION(i, exception_option, exception_command,
                                           exception_sensor_ieeeAddr, exception_sensor_input_values,
                                           exception_value_1, exception_value_2, exception_value_3):
                    
                    device_exception = GET_DEVICE_EXCEPTION_BY_ID(i)

                    success_message_change_device_exceptions.append(device_exception.device.name + " || Settings successfully saved") 
                

    """ ###################### """
    """  mqtt firmware update  """
    """ ###################### """

    if request.form.get("upload_mqtt_firmware") != None: 
        mqtt_device_update_collapse_open = True

        # check if the post request has the file part
        if "file" not in request.files:
            error_message_mqtt_firmware_upload = "No file found"

        else:
            file   = request.files['file']
            result = UPLOAD_FIRMWARE(file)

            if result == True:
                success_message_mqtt_firmware_upload = True

            else:
                error_message_mqtt_firmware_upload = result


    """ ################ """
    """  zigbee pairing  """
    """ ################ """

    # change pairing setting
    if request.form.get("set_zigbee_pairing") != None: 

        # check mqtt connection
        if GET_MQTT_CONNECTION_STATUS() != True:  
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

        if result == True:
            success_message_logfile = True 
        else:
            error_message_logfile = "Reset Log || " + str(result)


    list_device_exceptions = GET_ALL_DEVICE_EXCEPTIONS()
    list_exception_sensors = GET_ALL_DEVICES("sensors")    

    dropdown_list_exception_devices = GET_ALL_DEVICES("devices")    
    dropdown_list_exception_options = ["IP-ADDRESS"] 
    dropdown_list_operators         = ["=", ">", "<"]
    
    list_manually_adding_devices = GET_ALL_MQTT_DEVICES_MANUALLY_ADDING()

    list_devices                = GET_ALL_DEVICES("")
    zigbee2mqtt_pairing_setting = GET_ZIGBEE2MQTT_PAIRING_SETTING()
    system_services             = GET_SYSTEM_SETTINGS()   
    list_mqtt_firmware_files    = GET_ALL_MQTT_FIRMWARE_FILES()

    if GET_ZIGBEE_DEVICE_UPDATE_STATUS() != "No Device Update available":
        show_zigbee_device_updates = True
    else:
        show_zigbee_device_updates = False

    # check zigbee topology exist
    if os.path.isfile(GET_PATH() + "/app/static/temp/zigbee_topology.png"):
        zigbee_topology_exist = True

    data = {'navigation': 'devices_management'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    error_message_device_exception_settings = CHECK_DEVICE_EXCEPTION_SETTINGS(GET_ALL_DEVICE_EXCEPTIONS()) 

    # get sensor list
    device_input_values_list = []  

    try:
        for device in GET_ALL_DEVICES(""):
            device_input_values = "Sensor,------------------," + device.input_values
            device_input_values = device_input_values.replace(" ", "")
            device_input_values_list.append(device_input_values)
    except:
        pass 


    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/devices_management.html',
                                                    error_message_mqtt_connection=error_message_mqtt_connection,
                                                    error_message_zigbee2mqtt_connection=error_message_zigbee2mqtt_connection,
                                                    success_message_change_settings_devices=success_message_change_settings_devices,
                                                    error_message_change_settings_devices=error_message_change_settings_devices, 
                                                    success_message_add_device_exception=success_message_add_device_exception,
                                                    error_message_add_device_exception=error_message_add_device_exception,      
                                                    success_message_change_device_exceptions=success_message_change_device_exceptions,
                                                    error_message_change_device_exceptions=error_message_change_device_exceptions,
                                                    error_message_device_exception_settings=error_message_device_exception_settings,
                                                    success_message_mqtt_manually_adding=success_message_mqtt_manually_adding,
                                                    error_message_mqtt_manually_adding=error_message_mqtt_manually_adding,
                                                    success_message_mqtt_firmware_upload=success_message_mqtt_firmware_upload,
                                                    error_message_mqtt_firmware_upload=error_message_mqtt_firmware_upload,
                                                    error_message_zigbee_device_update=error_message_zigbee_device_update,
                                                    success_message_zigbee_pairing=success_message_zigbee_pairing,
                                                    error_message_zigbee_pairing=error_message_zigbee_pairing,
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,   
                                                    error_message_mqtt_firmware=error_message_mqtt_firmware,  
                                                    error_download_log_zigbee2mqtt=error_download_log_zigbee2mqtt,
                                                    error_download_topology_zigbee2mqtt=error_download_topology_zigbee2mqtt,
                                                    system_services=system_services,                                            
                                                    list_devices=list_devices,
                                                    list_device_exceptions=list_device_exceptions,
                                                    list_exception_sensors=list_exception_sensors,
                                                    dropdown_list_exception_devices=dropdown_list_exception_devices,
                                                    dropdown_list_exception_options=dropdown_list_exception_options,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    list_manually_adding_devices=list_manually_adding_devices,
                                                    list_mqtt_firmware_files=list_mqtt_firmware_files,
                                                    zigbee2mqtt_pairing_setting=zigbee2mqtt_pairing_setting,
                                                    timestamp=timestamp,  
                                                    show_zigbee_device_updates=show_zigbee_device_updates,                                                      
                                                    zigbee_device_update_collapse_open=zigbee_device_update_collapse_open,
                                                    mqtt_device_update_collapse_open=mqtt_device_update_collapse_open,
                                                    device_exceptions_collapse_open=device_exceptions_collapse_open,  
                                                    zigbee_topology_exist=zigbee_topology_exist,
                                                    device_input_values_list=device_input_values_list,                                                     
                                                    ) 
                           )


# change device position 
@app.route('/devices/management/device/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_device_position(id, direction):
    CHANGE_DEVICE_POSITION(id, direction)
    return redirect(url_for('devices_management'))


# remove device
@app.route('/devices/management/device/delete/<string:ieeeAddr>')
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
               
        return redirect(url_for('devices_management'))


    except Exception as e:
        session['delete_device_error'] = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name + " || Error | + " + str(e)            
        return redirect(url_for('devices_management'))        


# change device exception position 
@app.route('/devices/management/device_exception/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_device_exception_position(id, direction):
    CHANGE_DEVICE_EXCEPTION_POSITION(id, direction)
    return redirect(url_for('devices_management'))


# remove device exception
@app.route('/devices/management/device_exception/delete/<int:id>')
@login_required
@permission_required
def remove_device_exception(id):
    try:
        result = DELETE_DEVICE_EXCEPTION(id)

        if result == True:
            session['delete_device_exception_success'] = "Device Exception successfully deleted"       
        else:
            session['delete_device_exception_error'] = "Device Exception || Deletion not confirmed"      

        return redirect(url_for('devices_management'))


    except Exception as e:
        session['delete_device_exception_error'] = "Device Exception || Error | + " + str(e)            
        return redirect(url_for('devices_management'))        


# download mqtt firmware
@app.route('/devices/management/firmware/download/<string:filename>')
@login_required
@permission_required
def download_mqtt_firmware(filename):
    try:
        path = GET_PATH() + "/firmwares/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /firmwares/" + filename + " | downloaded")
        return send_from_directory(path, filename)
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /firmwares/" + filename + " | " + str(e)) 
        session['error_mqtt_firmware'] = "Download Firmware || " + str(e)


# delete mqtt firmware
@app.route('/devices/management/firmware/delete/<string:filename>')
@login_required
@permission_required
def delete_mqtt_firmware(filename):
    result = DELETE_MQTT_FIRMWARE(filename)

    if result != True:
        session['error_mqtt_firmware'] = result

    return redirect(url_for('devices_management'))


# update zigbee device 
@app.route('/devices/management/firmware/update/<string:ieeeAddr>')
@login_required
@permission_required
def update_zigbee_device(ieeeAddr):
    if GET_ZIGBEE_DEVICE_UPDATE_STATUS() == "" or GET_ZIGBEE_DEVICE_UPDATE_STATUS() == "Device Update found":
        channel  = "smarthome/zigbee2mqtt/bridge/ota_update/update"
        msg      = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name

        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))
        session['zigbee_device_update_started'] = "True" 

    else:
        session['zigbee_device_update_running'] = "True"

    return redirect(url_for('devices_management'))


# download zigbee topology 
@app.route('/devices/management/topology/download/<string:filename>')
@login_required
@permission_required
def download_zigbee_topology(filename): 
    path = GET_PATH() + "/app/static/temp/"
    
    if os.path.isfile(path + filename) == False:
        session['error_download_topology_zigbee2mqtt'] = "Download Topology || File not found" 
        return redirect(url_for('devices_management'))
    
    else:
        return send_from_directory(path, filename)


# download logs
@app.route('/devices/management/log/download/<string:filename>')
@login_required
@permission_required
def download_logs(filename): 
    path = GET_PATH() + "/data/logs/"
    
    if os.path.isfile(path + filename) == False:

        if filename == "zigbee2mqtt.txt":
            session['error_download_log_zigbee2mqtt'] = "Download Log || File not found" 
            return redirect(url_for('devices_management'))

        if filename == "log_devices.csv":
            session['error_download_log_devices'] = "Download Log || File not found"  
    
    else:
        return send_from_directory(path, filename)


""" ################## """
"""  request firmware  """
""" ################## """   

# request mqtt firmware
@app.route('/firmware/request', methods=['GET', 'POST'])
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


##########
# OLD PATH
##########

# request mqtt firmware
@app.route('/settings/devices/firmware/request', methods=['GET', 'POST'])
def request_mqtt_firmware_OLD():
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