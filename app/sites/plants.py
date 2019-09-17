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
        try:
            if current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/plants.html', methods=['GET', 'POST'])
@login_required
@permission_required
def plants():
    error_message_add_plant = []
    name = ""
    error_message_change_settings = ""
    pumptime = ""
    moisture_level = ""
    mqtt_device_ieeeAddr = ""
    mqtt_device_name     = ""
    control_sensor_moisture = ""
    control_sensor_watertank = ""

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    if request.form.get("add_plant") != None: 

        # check name
        if request.form.get("set_name") == "":
            error_message_add_plant.append("Keinen Namen angegeben")
        else:
            name = request.form.get("set_name")

        # check device
        if request.form.get("set_mqtt_device_ieeeAddr") == "None":
            error_message_add_plant.append("Kein Gerät angegeben")
        else:
            mqtt_device_ieeeAddr = request.form.get("set_watering_controller_ieeeAddr")
            #mqtt_device_name     = GET_MQTT_DEVICE_BY_IEEEADDR(mqtt_device_ieeeAddr).name
            
        if name != "" and mqtt_device_ieeeAddr != "":
                        
            #error = ADD_PLANT(name, mqtt_device_ieeeAddr)   
            #if error != None: 
            #    error_message_add_plant.append(error)                

            name                 = ""
            mqtt_device_ieeeAddr = ""
            mqtt_device_name     = ""

    # save mqtt broker setting
    if request.form.get("save_plants_settings") != None:
        pass
                        


    dropdown_list_watering_controller = ""

    dropdown_list_groups              = [1, 2, 3, 4, 5]
    dropdown_list_pumptime            = ["15", "30", "60", "90", "120"]
    dropdown_list_moisture_level      = ["less", "normal", "much"]
    
    list_plants = ""

    data = {'navigation': 'plants', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/plants.html',
                                                    list_plants=list_plants,
                                                    dropdown_list_watering_controller=dropdown_list_watering_controller,
                                                    dropdown_list_groups=dropdown_list_groups,
                                                    dropdown_list_pumptime=dropdown_list_pumptime,
                                                    dropdown_list_moisture_level=dropdown_list_moisture_level,              
                                                    ) 
                           )
