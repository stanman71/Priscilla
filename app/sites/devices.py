from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.mqtt             import MQTT_PUBLISH, UPDATE_DEVICES
from app.backend.file_management  import GET_PATH, RESET_LOGFILE, WRITE_LOGFILE_SYSTEM
from app.common                   import COMMON, STATUS
from app.assets                   import *

import datetime
import os

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
    success_message_change_settings_devices = []         
    error_message_change_settings_devices   = []    
    success_message_change_settings_broker  = ""         
    error_message_change_settings_broker    = []   
    success_message_logfile                 = False
    error_message_logfile                   = ""

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # check mqtt
    result = MQTT_PUBLISH("miranda/mqtt/test", "") 
    if result != None:
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

    """ ######### """
    """  devices  """
    """ ######### """

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
                            SET_DEVICE_NAME(ieeeAddr, new_name)   
                            success_message_change_settings_devices.append(new_name + " || Einstellungen gespeichert")                                  
                        else: 
                            error_message_change_settings_devices.append(old_name + " || Ungültige Eingabe Name || Bereits vergeben")  

                else:
                    name = GET_DEVICE_BY_ID(i).name
                    error_message_change_settings_devices.append(name + " || Ungültige Eingabe Name || Keinen Wert angegeben")    


    # update device list
    if request.form.get("update_devices") != None:     
        result = UPDATE_DEVICES()

        if result == "Success":
            success_message_change_settings_devices.append("Geräte || Erfolgreich aktualisiert")
        else:
            error_message_change_settings_devices.append(result)


    """ ############# """
    """  mqtt broker  """
    """ ############# """

    if request.form.get("save_broker_settings") != None:

        if request.form.get("set_broker") != "":                 
            broker = request.form.get("set_broker")
        else:
            broker = ""
            error_message_change_settings_broker.append("Broker || Keinen Broker angegeben")   
             
        user     = request.form.get("set_user")
        password = request.form.get("set_password")

        if broker != "":
            if SET_MQTT_BROKER_SETTINGS(broker, user, password):
                success_message_change_settings_broker = "Einstellungen erfolgreich geändert"


    if request.form.get("restore_broker_settings") != None:
        RESTORE_MQTT_BROKER_SETTINGS()
        success_message_change_settings_broker = "Einstellungen erfolgreich wiederhergestellt"

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


    list_devices = GET_ALL_DEVICES("")
    
    broker = GET_MQTT_BROKER_SETTINGS()

    data = {'navigation': 'devices', 'notification': ''}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/devices.html',
                                                    error_message_mqtt=error_message_mqtt,
                                                    success_message_change_settings_devices=success_message_change_settings_devices,
                                                    error_message_change_settings_devices=error_message_change_settings_devices, 
                                                    success_message_change_settings_broker=success_message_change_settings_broker,                                                       
                                                    error_message_change_settings_broker=error_message_change_settings_broker,    
                                                    success_message_logfile=success_message_logfile,     
                                                    error_message_logfile=error_message_logfile,                                                  
                                                    list_devices=list_devices,
                                                    broker=broker,
                                                    timestamp=timestamp,                         
                                                    ) 
                           )


# change device position 
@app.route('/devices/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_device_position(id, direction, device_type):
    CHANGE_DEVICE_POSITION(id, device_type, direction)
    return redirect(url_for('devices'))


# remove device
@app.route('/devices/delete/<string:ieeeAddr>')
@login_required
@permission_required
def remove_device(ieeeAddr):
    device_name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
    result      = DELETE_DEVICE(ieeeAddr) 
    if result == True:
        session['delete_device_success'] = device_name + " || Erfolgreich gelöscht"
    else:
        session['delete_device_error'] = device_name + " || " + str(result)
        
    return redirect(url_for('devices'))
     
     
# download devices logfile
@app.route('/devices/download/<path:filepath>')
@login_required
@permission_required
def download_devices_logfile(filepath): 
    path = GET_PATH() + "/logs/"  

    try:
        if os.path.isfile(path + filepath) is False:
            RESET_LOGFILE("log_devices")  
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filepath + " | downloaded") 

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filepath + " | " + str(e))
        session['error_download_log'] = "Download Log || " + str(e)

    return send_from_directory(path, filepath)