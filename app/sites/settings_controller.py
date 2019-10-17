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
                if request.form.get("set_task_1_" + str(i)) != "":
                    task_1 = request.form.get("set_task_1_" + str(i))
                else:
                    task_1 = "None"                   
                if request.form.get("set_task_2_" + str(i)) != "":
                    task_2 = request.form.get("set_task_2_" + str(i))
                else:
                    task_2 = "None"  
                if request.form.get("set_task_3_" + str(i)) != "":
                    task_3 = request.form.get("set_task_3_" + str(i))
                else:
                    task_3 = "None"  
                if request.form.get("set_task_4_" + str(i)) != "":
                    task_4 = request.form.get("set_task_4_" + str(i))
                else:
                    task_4 = "None"                   
                if request.form.get("set_task_5_" + str(i)) != "":
                    task_5 = request.form.get("set_task_5_" + str(i))
                else:
                    task_5 = "None"  
                if request.form.get("set_task_6_" + str(i)) != "":
                    task_6 = request.form.get("set_task_6_" + str(i))
                else:
                    task_6 = "None"  
                if request.form.get("set_task_7_" + str(i)) != "":
                    task_7 = request.form.get("set_task_7_" + str(i))
                else:
                    task_7 = "None"                   
                if request.form.get("set_task_8_" + str(i)) != "":
                    task_8 = request.form.get("set_task_8_" + str(i))
                else:
                    task_8 = "None"  
                if request.form.get("set_task_9_" + str(i)) != "":
                    task_9 = request.form.get("set_task_9_" + str(i))
                else:
                    task_9 = "None"  
                    
                if SET_CONTROLLER_TASKS(i, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9):
                    success_message_change_settings_controller = i

                                                    
    """ ######################## """
    """  controller task options """
    """ ######################## """   

    # list device command option    
    list_device_command_options = []
    
    for device in GET_ALL_DEVICES("devices"):
        list_device_command_options.append((device.name, device.commands))
         
    # list spotify devices / playlists
    spotify_token = GET_SPOTIFY_TOKEN()    
    
    try:
        sp       = spotipy.Spotify(auth=spotify_token)
        sp.trace = False
        
        spotify_devices   = sp.devices()["devices"]        
        spotify_playlists = sp.current_user_playlists(limit=20)["items"]   
        
    except:
        spotify_devices   = ""       
        spotify_playlists = ""      


    error_message_controller_tasks = CHECK_TASKS(GET_ALL_CONTROLLER(), "controller")
        
    list_controller = GET_ALL_CONTROLLER()

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_controller.html', 
                                                    success_message_change_settings_controller=success_message_change_settings_controller,
                                                    error_message_controller_tasks=error_message_controller_tasks, 
                                                    list_controller=list_controller,
                                                    list_device_command_options=list_device_command_options,
                                                    spotify_devices=spotify_devices,     
                                                    spotify_playlists=spotify_playlists,      
                                                    ) 
                           )


# change controller position 
@app.route('/settings/controller/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_controller_position(id, direction):
    CHANGE_CONTROLLER_POSITION(id, direction)
    return redirect(url_for('settings_controller'))
