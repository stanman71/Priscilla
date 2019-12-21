from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
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


@app.route('/settings/controller', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_controller():
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
                                                            
                if SET_CONTROLLER_TASKS(i, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10, task_11, task_12):
                    success_message_change_settings_controller = i

                                                    
    """ ######################## """
    """  controller task options """
    """ ######################## """   

    # list led group options    
    list_led_group_options = []

    for group in GET_ALL_LED_GROUPS():
        list_led_group_options.append(group.name)

    # list led scene options    
    list_led_scene_options = []

    for scene in GET_ALL_LED_SCENES():
        list_led_scene_options.append(scene.name)

    # list sensordata job options    
    list_sensordata_job_options = []

    for job in GET_ALL_SENSORDATA_JOBS():
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


    error_message_controller_tasks = CHECK_TASKS(GET_ALL_CONTROLLER(), "controller")
        
    list_controller = GET_ALL_CONTROLLER()

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_controller.html', 
                                                    success_message_change_settings_controller=success_message_change_settings_controller,
                                                    error_message_controller_tasks=error_message_controller_tasks, 
                                                    list_controller=list_controller,
                                                    list_led_group_options=list_led_group_options,
                                                    list_led_scene_options=list_led_scene_options,
                                                    list_sensordata_job_options=list_sensordata_job_options,
                                                    list_program_options=list_program_options,                                                       
                                                    list_device_command_options=list_device_command_options,
                                                    list_spotify_devices=list_spotify_devices,     
                                                    list_spotify_playlists=list_spotify_playlists,    
                                                    ) 
                           )


# change controller position 
@app.route('/settings/controller/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_controller_position(id, direction):
    CHANGE_CONTROLLER_POSITION(id, direction)
    return redirect(url_for('settings_controller'))
