from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import GET_PATH, GET_PLANTS_DATAFILES
from app.common                  import COMMON, STATUS
from app.assets                  import *

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


@app.route('/plants', methods=['GET', 'POST'])
@login_required
@permission_required
def plants():
    error_message_add_plant = []
    error_message_change_settings = []

    success_message_change_settings = []   
    success_message_add_plant       = False   

    name            = ""
    device_ieeeAddr = ""
    device_name     = ""

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'


    """ ################# """
    """  plants settings  """
    """ ################# """   

    if request.form.get("save_plants_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                error_founded          = False
                moisture_level         = None
                pump_duration_manually = None                
                current_name           = GET_PLANT_BY_ID(i).name

                # rename plants   
                if request.form.get("set_name_" + str(i)) != "":
                                      
                    new_name = request.form.get("set_name_" + str(i))

                    if new_name != current_name:  

                        # name already exist ?         
                        if not GET_PLANT_BY_NAME(new_name):  
                            name = new_name                            
                        else: 
                            error_message_change_settings.append(current_name + " || Ungültige Eingabe Name || Bereits vergeben")  
                            error_founded = True
                            name = current_name

                    else:
                        name = current_name

                else:
                    name = GET_PLANT_BY_ID(i).name
                    error_message_change_settings.append(current_name + " || Ungültige Eingabe Name || Keinen Wert angegeben") 
                    error_founded = True      
                                                            
                if request.form.get("radio_group_" + str(i)) != None:
                    group = request.form.get("radio_group_" + str(i))
                else:
                    group = 1

                if request.form.get("radio_moisture_level_" + str(i)) != None:
                    moisture_level = request.form.get("radio_moisture_level_" + str(i))

                if request.form.get("set_pump_duration_manually_" + str(i)) != None:
                    pump_duration_manually = request.form.get("set_pump_duration_manually_" + str(i))

                    try: 
                        if not 5 < int(pump_duration_manually) < 200:
                            error_message_change_settings.append(current_name + " || Ungültige Eingabe Pumpzeit || Muss eine Zahl zwischen 5 und 200 sein") 
                            error_founded = True 
                    except:
                        error_message_change_settings.append(current_name + " || Ungültige Eingabe Pumpzeit || Muss eine Zahl zwischen 5 und 200 sein") 
                        error_founded = True        

                # save settings
                if error_founded == False: 

                    changes_saved = False

                    if UPDATE_PLANT_SETTINGS(i, name, group):
                        changes_saved = True

                    if moisture_level != None:
                        if SET_PLANT_MOISTURE_LEVEL(i, moisture_level):
                            changes_saved = True

                    if pump_duration_manually != None:
                        if SET_PLANT_PUMP_DURATION_MANUALLY(i, pump_duration_manually):
                            changes_saved = True     

                    if changes_saved == True:    
                        success_message_change_settings.append(name + " || Einstellungen gespeichert") 

                name = ""


    """ ########### """
    """  add plant  """
    """ ########### """   

    if request.form.get("add_plant") != None: 

        # check name
        if request.form.get("set_name") == "":
            error_message_add_plant.append("Keinen Namen angegeben")
        else:
            name = request.form.get("set_name")

        # check device
        if request.form.get("set_watering_controller_ieeeAddr") == "":
            error_message_add_plant.append("Kein Gerät angegeben")
        else:
            device_ieeeAddr = request.form.get("set_watering_controller_ieeeAddr")
            device_name     = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr).name
            
        if name != "" and device_ieeeAddr != "":
                        
            error = ADD_PLANT(name, device_ieeeAddr)   
            if error != None: 
                error_message_add_plant.append(error)         

            else:       
                success_message_add_plant = True
                name            = ""
                device_ieeeAddr = ""
                device_name     = ""


    dropdown_list_watering_controller = GET_ALL_DEVICES("watering_controller")

    list_plants           = GET_ALL_PLANTS()
    list_plants_datafiles = GET_PLANTS_DATAFILES()

    data = {'navigation': 'plants', 'notification': ''}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/plants.html',
                                                    error_message_change_settings=error_message_change_settings,                            
                                                    error_message_add_plant=error_message_add_plant,
                                                    success_message_change_settings=success_message_change_settings,                                                         
                                                    success_message_add_plant=success_message_add_plant,                                               
                                                    dropdown_list_watering_controller=dropdown_list_watering_controller, 
                                                    name=name,
                                                    device_ieeeAddr=device_ieeeAddr,
                                                    device_name=device_name,
                                                    list_plants=list_plants,  
                                                    list_plants_datafiles=list_plants_datafiles,  
                                                    timestamp=timestamp,      
                                                    ) 
                           )


# change plants position 
@app.route('/plants/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_plants_position(id, direction):
    CHANGE_PLANTS_POSITION(id, direction)
    return redirect(url_for('plants'))


# delete plant
@app.route('/plants/delete/<int:id>')
@login_required
@permission_required
def delete_plant(id):
    DELETE_PLANT(id)
    return redirect(url_for('plants'))


# download plants data file
@app.route('/plants/download/file/<path:filepath>')
@login_required
@permission_required
def download_plants_datafile(filepath):
    if filepath is None:
        print("Ungültiger Pfad angegeben")     
    try:
        path = GET_PATH() + "/csv/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /csv/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /csv/" + filepath + " | " + str(e)) 