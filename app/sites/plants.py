from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.shared_resources import mqtt_message_queue, GET_DEVICE_CONNECTION_MQTT
from app.common                   import COMMON, STATUS
from app.assets                   import *

import datetime
import heapq

# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "user" or current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/plants', methods=['GET', 'POST'])
@login_required
@permission_required
def plants():
    success_message_change_settings = []      
    error_message_change_settings   = []    
    success_message_add_plant       = False       
    error_message_add_plant         = []


    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # test message
    if session.get('test_pump_success', None) != None:
        success_message_change_settings.append(session.get('test_pump_success')) 
        session['test_pump_success'] = None

    if session.get('test_pump_error', None) != None:
        error_message_change_settings.append(session.get('test_pump_error'))
        session['test_pump_error'] = None       

    # delete message
    if session.get('delete_plant_success', None) != None:
        success_message_change_settings.append(session.get('delete_plant_success')) 
        session['delete_plant_success'] = None
        
    if session.get('delete_plant_error', None) != None:
        error_message_change_settings.append(session.get('delete_plant_error'))
        session['delete_plant_error'] = None       


    """ ########### """
    """  add plant  """
    """ ########### """   

    if request.form.get("add_plant") != None: 
        result = ADD_PLANT()   
        if result != True: 
            error_message_add_plant.append(result)         

        else:       
            success_message_add_plant = True


    """ ############## """
    """  table plants  """
    """ ############## """   

    if request.form.get("save_plants_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                error_founded = False     

                # ############
                # name setting
                # ############

                plant      = GET_PLANT_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i))                    

                # add new name
                if ((input_name != "") and (GET_PLANT_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == plant.name:
                    name = plant.name                        
                    
                # name already exist
                elif ((GET_PLANT_BY_NAME(input_name) != None) and (plant.name != input_name)):
                    error_message_change_settings.append(plant.name + " || Name bereits vergeben")  
                    name = plant.name
                    error_founded = True  

                # no input commited
                else:                          
                    name = GET_PLANT_BY_ID(i).name
                    error_message_change_settings.append(plant.name + " || Keinen Namen angegeben") 
                    error_founded = True  

                # ##############
                # device setting
                # ##############

                # no input commited                
                if request.form.get("set_watering_controller_ieeeAddr") == "None":
                    error_message_change_settings.append("Kein Gerät angegeben")
                    error_founded = True                      

                # device already in use
                elif (GET_PLANT_BY_IEEEADDR(request.form.get("set_watering_controller_ieeeAddr")) and 
                    request.form.get("set_watering_controller_ieeeAddr") != GET_PLANT_BY_ID(i).device_ieeeAddr):
                    
                    error_message_change_settings.append("Gerät mehrmals vergeben")    
                    error_founded = True  

                # add new device
                else:
                    device_ieeeAddr = request.form.get("set_watering_controller_ieeeAddr")

                # #############
                # group setting
                # #############

                if request.form.get("set_group_" + str(i)) != "":
                    group = request.form.get("set_group_" + str(i))

                else:
                    group = 1

                # #####################
                # pump duration setting
                # #####################

                if request.form.get("set_pump_duration_" + str(i)) != "":
                    pump_duration = request.form.get("set_pump_duration_" + str(i))

                    try: 
                        if not 5 <= int(pump_duration) <= 200:
                            error_message_change_settings.append(plant.name + " || Pumpzeit muss eine Zahl zwischen 5 und 200 sein") 
                            error_founded = True 
                    except:
                        error_message_change_settings.append(plant.name + " || Pumpzeit muss eine Zahl zwischen 5 und 200 sein") 
                        error_founded = True        

                else:
                    error_message_change_settings.append(plant.name + " || Pumpzeit muss eine Zahl zwischen 5 und 200 sein") 
                    error_founded = True                         


                # #############
                # save settings
                # #############

                if error_founded == False: 

                    if SET_PLANT_SETTINGS(i, name, device_ieeeAddr, group, pump_duration):
                        success_message_change_settings.append(plant.name + " || Einstellungen gespeichert") 

                    name = ""

    dropdown_list_watering_controller = GET_ALL_DEVICES("watering_controller")

    list_plants = GET_ALL_PLANTS()

    data = {'navigation': 'plants'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/plants.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_plant=success_message_add_plant,                            
                                                    error_message_add_plant=error_message_add_plant,                                                                                              
                                                    dropdown_list_watering_controller=dropdown_list_watering_controller, 
                                                    list_plants=list_plants,     
                                                    ) 
                           )


# change plants position 
@app.route('/plants/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_plants_position(id, direction):
    CHANGE_PLANTS_POSITION(id, direction)
    return redirect(url_for('plants'))


# test pump
@app.route('/plants/test_pump/<int:id>')
@login_required
@permission_required
def test_pump(id):

    if GET_DEVICE_CONNECTION_MQTT() == True:

        session['test_pump_success'] = GET_PLANT_BY_ID(id).name + " || Pumpe gestartet (5 Sekunden)" 

        channel  =  "miranda/mqtt/" + GET_PLANT_BY_ID(id).device_ieeeAddr + "/set"
        msg      = '{"pump":"ON","pump_time":5}'

        heapq.heappush(mqtt_message_queue, (20, (channel, msg)))   
        
    else:
        session['test_pump_error'] = "Keine MQTT-Verbindung" 
    

    return redirect(url_for('plants'))


# delete plant
@app.route('/plants/delete/<int:id>')
@login_required
@permission_required
def delete_plant(id):
    plant  = GET_PLANT_BY_ID(id).name  
    result = DELETE_PLANT(id)

    if result:
        session['delete_plant_success'] = plant + " || Erfolgreich gelöscht"
    else:
        session['delete_plant_error'] = plant + " || " + str(result)

    return redirect(url_for('plants'))
