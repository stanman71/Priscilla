from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                 import app
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *

import datetime

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


@app.route('/devices.html', methods=['GET', 'POST'])
@login_required
@permission_required
def devices():
    error_message_mqtt = ""
    error_message_change_settings_devices   = [] 
    success_message_change_settings_devices = False          
    error_message_change_settings_broker    = [] 
    success_message_change_settings_broker  = False     

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # check mqtt
    try:
        CHECK_MQTT()
    except Exception as e:
        error_message_mqtt = "Fehler MQTT >>> " + str(e)
        WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e)) 
        #SEND_EMAIL("ERROR", "MQTT | " + str(e)) 


    """ ############## """
    """  mqtt devices  """
    """ ############## """

    if request.form.get("save_device_settings") != None:  

        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                # rename devices   
                if request.form.get("set_name_" + str(i)) != "":
                                      
                    new_name = request.form.get("set_name_" + str(i))
                    old_name = GET_MQTT_DEVICE_BY_ID(i).name

                    if new_name != old_name:  

                        # name already exist ?         
                        if not GET_MQTT_DEVICE_BY_NAME(new_name):  
                            ieeeAddr = GET_MQTT_DEVICE_BY_ID(i).ieeeAddr                  
                            SET_MQTT_DEVICE_NAME(ieeeAddr, new_name)   
                            success_message_change_settings_devices = True                                 
                        else: 
                            error_message_change_settings_devices.append(old_name + " >>> Ungültige Eingabe >>> Name bereits vergeben")  

                else:
                    name = GET_MQTT_DEVICE_BY_ID(i).name
                    error_message_change_settings_devices.append(old_name + " >>> Ungültige Eingabe >>> Keinen Namen angegeben")    


    # update device list
    if request.form.get("update_mqtt_devices") != None:
        pass
        #error_message_change_settings = UPDATE_MQTT_DEVICES("mqtt")


    """ ############# """
    """  mqtt broker  """
    """ ############# """

    if request.form.get("save_broker_settings") != None:

        if request.form.get("set_broker") != "":                 
            broker = request.form.get("set_broker")
        else:
            broker = ""
            error_message_change_settings_broker.append("Broker >>> Keinen Broker angegeben")   
             
        user     = request.form.get("set_user")
        password = request.form.get("set_password")

        if broker != "":
            SET_MQTT_BROKER_SETTINGS(broker, user, password)
            success_message_change_settings_broker = True


    if request.form.get("restore_broker_settings") != None:
        RESTORE_MQTT_BROKER_SETTINGS()
        success_message_change_settings_broker = True

    list_devices = GET_ALL_MQTT_DEVICES("")
    
    broker = GET_MQTT_BROKER_SETTINGS()

    data = {'navigation': 'devices', 'notification': ''}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/devices.html',
                                                    error_message_mqtt=error_message_mqtt,
                                                    error_message_change_settings_devices=error_message_change_settings_devices,   
                                                    success_message_change_settings_devices=success_message_change_settings_devices, 
                                                    error_message_change_settings_broker=error_message_change_settings_broker,   
                                                    success_message_change_settings_broker=success_message_change_settings_broker,                                                     
                                                    list_devices=list_devices,
                                                    broker=broker,
                                                    timestamp=timestamp,                         
                                                    ) 
                           )
