from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.checks          import CHECK_TASKS
from app.backend.spotify         import GET_SPOTIFY_TOKEN
from app.common                  import COMMON, STATUS
from app.assets                  import *

import spotipy

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


@app.route('/devices/controller', methods=['GET', 'POST'])
@login_required
@permission_required
def devices_controller():
    page_title       = 'Bianca | Devices | Controller'
    page_description = 'The controller configuration page.'

    success_message_change_settings_controller = False

    RESET_CONTROLLER_COLLAPSE()
    UPDATE_CONTROLLER_EVENTS()


    """ #################### """
    """  controller settings """
    """ #################### """   

    if request.form.get("save_controller_settings") != None: 

        for i in range (1,21):

            if request.form.get("set_task_1_" + str(i)) != None:
                
                SET_CONTROLLER_COLLAPSE_OPEN(i)   

                ### set tasks
                if request.form.get("set_task_1_" + str(i)) != "" and request.form.get("set_task_1_" + str(i)) != None:
                    task_1 = request.form.get("set_task_1_" + str(i)).strip()
                else:
                    task_1 = "None"              

                if request.form.get("set_task_2_" + str(i)) != "" and request.form.get("set_task_2_" + str(i)) != None:
                    task_2 = request.form.get("set_task_2_" + str(i)).strip()
                else:
                    task_2 = "None"  

                if request.form.get("set_task_3_" + str(i)) != "" and request.form.get("set_task_3_" + str(i)) != None:
                    task_3 = request.form.get("set_task_3_" + str(i)).strip()
                else:
                    task_3 = "None"  

                if request.form.get("set_task_4_" + str(i)) != "" and request.form.get("set_task_4_" + str(i)) != None:
                    task_4 = request.form.get("set_task_4_" + str(i)).strip()
                else:
                    task_4 = "None"    

                if request.form.get("set_task_5_" + str(i)) != "" and request.form.get("set_task_5_" + str(i)) != None:
                    task_5 = request.form.get("set_task_5_" + str(i)).strip()
                else:
                    task_5 = "None"  
                    
                if request.form.get("set_task_6_" + str(i)) != "" and request.form.get("set_task_6_" + str(i)) != None:
                    task_6 = request.form.get("set_task_6_" + str(i)).strip()
                else:
                    task_6 = "None"  

                if request.form.get("set_task_7_" + str(i)) != "" and request.form.get("set_task_7_" + str(i)) != None:
                    task_7 = request.form.get("set_task_7_" + str(i)).strip()
                else:
                    task_7 = "None"    
                                  
                if request.form.get("set_task_8_" + str(i)) != "" and request.form.get("set_task_8_" + str(i)) != None:
                    task_8 = request.form.get("set_task_8_" + str(i)).strip()
                else:
                    task_8 = "None"  

                if request.form.get("set_task_9_" + str(i)) != "" and request.form.get("set_task_9_" + str(i)) != None:
                    task_9 = request.form.get("set_task_9_" + str(i)).strip()
                else:
                    task_9 = "None"  

                if request.form.get("set_task_10_" + str(i)) != "" and request.form.get("set_task_10_" + str(i)) != None:
                    task_10 = request.form.get("set_task_10_" + str(i)).strip()
                else:
                    task_10 = "None"  

                if request.form.get("set_task_11_" + str(i)) != "" and request.form.get("set_task_11_" + str(i)) != None:
                    task_11 = request.form.get("set_task_11_" + str(i)).strip()
                else:
                    task_11 = "None"  
                    
                if request.form.get("set_task_12_" + str(i)) != "" and request.form.get("set_task_12_" + str(i)) != None:
                    task_12 = request.form.get("set_task_12_" + str(i)).strip()
                else:
                    task_12 = "None"  

                if request.form.get("set_task_13_" + str(i)) != "" and request.form.get("set_task_13_" + str(i)) != None:
                    task_13 = request.form.get("set_task_13_" + str(i)).strip()
                else:
                    task_13 = "None"  

                if request.form.get("set_task_14_" + str(i)) != "" and request.form.get("set_task_14_" + str(i)) != None:
                    task_14 = request.form.get("set_task_14_" + str(i)).strip()
                else:
                    task_14 = "None"  

                if request.form.get("set_task_15_" + str(i)) != "" and request.form.get("set_task_15_" + str(i)) != None:
                    task_15 = request.form.get("set_task_15_" + str(i)).strip()
                else:
                    task_15 = "None"  

                if request.form.get("set_task_15_" + str(i)) != "" and request.form.get("set_task_15_" + str(i)) != None:
                    task_15 = request.form.get("set_task_15_" + str(i)).strip()
                else:
                    task_15 = "None"  

                if request.form.get("set_task_16_" + str(i)) != "" and request.form.get("set_task_16_" + str(i)) != None:
                    task_16 = request.form.get("set_task_16_" + str(i)).strip()
                else:
                    task_16 = "None"  

                if request.form.get("set_task_17_" + str(i)) != "" and request.form.get("set_task_17_" + str(i)) != None:
                    task_17 = request.form.get("set_task_17_" + str(i)).strip()
                else:
                    task_17 = "None"  

                if request.form.get("set_task_18_" + str(i)) != "" and request.form.get("set_task_18_" + str(i)) != None:
                    task_18 = request.form.get("set_task_18_" + str(i)).strip()
                else:
                    task_18 = "None"  

                if request.form.get("set_task_19_" + str(i)) != "" and request.form.get("set_task_19_" + str(i)) != None:
                    task_19 = request.form.get("set_task_19_" + str(i)).strip()
                else:
                    task_19 = "None"  

                if request.form.get("set_task_20_" + str(i)) != "" and request.form.get("set_task_20_" + str(i)) != None:
                    task_20 = request.form.get("set_task_20_" + str(i)).strip()
                else:
                    task_20 = "None"  

                if SET_CONTROLLER_TASKS(i, task_1,  task_2,  task_3,  task_4,  task_5,  task_6,  task_7,  task_8,  task_9,  task_10, 
                                           task_11, task_12, task_13, task_14, task_15, task_16, task_17, task_18, task_19, task_20):
                                           
                    success_message_change_settings_controller = i

                                                    
    """ ######################## """
    """  controller task options """
    """ ######################## """   

    # list lighting group options    
    list_lighting_group_options = []

    for group in GET_ALL_LIGHTING_GROUPS():
        list_lighting_group_options.append(group.name)

    # list lighting scene options    
    list_lighting_scene_options = []

    for scene in GET_ALL_LIGHTING_SCENES():
        list_lighting_scene_options.append(scene.name)

    # list light options
    list_light_options = []

    for device in GET_ALL_DEVICES("light"):
        list_light_options.append(device.name)

    # list sensordata job options    
    list_sensordata_job_options = []

    for job in GET_ALL_SENSORDATA_JOBS():
        if job.device.model == "sensor_active": 
            list_sensordata_job_options.append(job.name)

    # list program options    
    list_program_options = []

    for program in GET_ALL_PROGRAMS():
        list_program_options.append(program.name)

    # list device command options    
    list_device_command_options = []
    
    for device in GET_ALL_DEVICES("devices"):
        list_device_command_options.append((device.name, device.commands))
         
    # list spotify devices / playlists
    spotify_token = GET_SPOTIFY_TOKEN()    
    
    try:
        sp       = spotipy.Spotify(auth=spotify_token)
        sp.trace = False
        
        list_spotify_devices   = sp.devices()["devices"]        
        list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]   
        
    except:
        list_spotify_devices   = ""       
        list_spotify_playlists = ""      


    CHECK_TASKS(GET_ALL_CONTROLLER(), "controller")
        
    list_controller = GET_ALL_CONTROLLER()

    data = {'navigation': 'devices_controller'}

    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/devices_controller.html', 
                                                    success_message_change_settings_controller=success_message_change_settings_controller,
                                                    list_controller=list_controller,
                                                    list_lighting_group_options=list_lighting_group_options,
                                                    list_lighting_scene_options=list_lighting_scene_options,
                                                    list_light_options=list_light_options,                                                    
                                                    list_sensordata_job_options=list_sensordata_job_options,
                                                    list_program_options=list_program_options,                                                       
                                                    list_device_command_options=list_device_command_options,
                                                    list_spotify_devices=list_spotify_devices,     
                                                    list_spotify_playlists=list_spotify_playlists,    
                                                    ) 
                           )


# change controller position 
@app.route('/devices/controller/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_controller_position(id, direction):
    CHANGE_CONTROLLER_POSITION(id, direction)
    return redirect(url_for('settings_controller'))