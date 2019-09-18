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


@app.route('/plants.html', methods=['GET', 'POST'])
@login_required
@permission_required
def plants():
    error_message_add_plant = []
    error_message_change_settings = []

    name                 = ""
    mqtt_device_ieeeAddr = ""
    mqtt_device_name     = ""


    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    if request.method == "POST":

        # add user
        if request.form.get("add_plant") != None: 

            # check name
            if request.form.get("set_name") == "":
                error_message_add_plant.append("Keinen Namen angegeben")
            else:
                name = request.form.get("set_name")

            # check device
            if request.form.get("set_watering_controller_ieeeAddr") == "None":
                error_message_add_plant.append("Kein Gerät angegeben")
            else:
                mqtt_device_ieeeAddr = request.form.get("set_watering_controller_ieeeAddr")
                mqtt_device_name     = GET_MQTT_DEVICE_BY_IEEEADDR(mqtt_device_ieeeAddr).name
                
            if name != "" and mqtt_device_ieeeAddr != "":
                            
                error = ADD_PLANT(name, mqtt_device_ieeeAddr)   
                if error != None: 
                    error_message_add_plant.append(error)                

                name                 = ""
                mqtt_device_ieeeAddr = ""
                mqtt_device_name     = ""


        # change settings
        if request.form.get("save_plants_settings") != None: 
            
            for i in range (1,26):

                if request.form.get("set_name_" + str(i)) != None:

                    # check name
                    if (request.form.get("set_name_" + str(i)) != "" and 
                        GET_PLANT_BY_NAME(request.form.get("set_name_" + str(i))) == None):
                        name = request.form.get("set_name_" + str(i)) 
                        
                    elif request.form.get("set_name_" + str(i)) == GET_PLANT_BY_ID(i).name:
                        name = GET_PLANT_BY_ID(i).name
                        
                    else:
                        name = GET_PLANT_BY_ID(i).name 
                        error_message_change_settings.append(name + " >>> Ungültige Eingabe >>> Keinen Namen angegeben")                         
                                        
                                                                    
                    pumptime = request.form.get("set_pumptime_" + str(i))
                    
                    if request.form.get("checkbox_pump_mode_" + str(i)) != None:
                        pump_mode = "auto"
                    else:
                        pump_mode = "manually" 
                        
                    if request.form.get("checkbox_sensor_moisture_" + str(i)) != None:
                        sensor_moisture = "True"
                    else:
                        sensor_moisture = "False" 

                    if request.form.get("checkbox_sensor_watertank_" + str(i)) != None:
                        sensor_watertank = "True"
                    else:
                        sensor_watertank = "False" 
                        
                    UPDATE_PLANT_SETTINGS(i, name, pumptime, pump_mode, sensor_moisture, sensor_watertank) 

                    name = ""
                    
                if request.form.get("radio_moisture_level_" + str(i)) != None:
                    moisture_level = request.form.get("radio_moisture_level_" + str(i))
                    SET_PLANT_MOISTURE_LEVEL(i, moisture_level)

                if request.form.get("set_pump_duration_manually_" + str(i)) != None:
                    pump_duration_manually = request.form.get("set_pump_duration_manually_" + str(i))
                    SET_PLANT_PUMP_DURATION_MANUALLY(i, pump_duration_manually)                   


    dropdown_list_watering_controller = GET_ALL_MQTT_DEVICES("watering_controller")

    list_plants = GET_ALL_PLANTS()

    data = {'navigation': 'plants', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/plants.html',
                                                    error_message_add_plant=error_message_add_plant,
                                                    error_message_change_settings=error_message_change_settings,
                                                    dropdown_list_watering_controller=dropdown_list_watering_controller, 
                                                    name=name,
                                                    mqtt_device_ieeeAddr=mqtt_device_ieeeAddr,
                                                    mqtt_device_name=mqtt_device_name,
                                                    list_plants=list_plants,          
                                                    ) 
                           )


# change plants position 
@app.route('/plants.html/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_plants_position(id, direction):
    CHANGE_PLANTS_POSITION(id, direction)
    return redirect(url_for('plants'))


# delete plant
@app.route('/plants.html/delete/<int:id>')
@login_required
@permission_required
def delete_plant(id):
    DELETE_PLANT(id)
    return redirect(url_for('plants'))
