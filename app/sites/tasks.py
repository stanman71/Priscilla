from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                 import app
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *


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


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
@permission_required
def tasks():
    error_message_change_settings_plants   = []
    success_message_change_settings_plants = []

    # update plants settings
    if request.form.get("update_plants_settings") != None:  

        # plant group 1
        if request.form.get("set_time_plants_group_1") != "":
            time_plants_group_1 = request.form.get("set_time_plants_group_1")

            error_founded = False

            try:
                time   = datetime.datetime.strptime(time_plants_group_1, "%H:%M")
                hour   = time.hour
                minute = time.minute

            except:
                error_message_change_settings_plants.append("Gruppe 1 || Ungültige Uhrzeit || " + time_plants_group_1)
                error_founded = True    

            if request.form.get("checkbox_pause_plants_group_1") != None:
                pause = "True"     
            else:
                pause = "False" 

            # save settings
            if error_founded == False: 

                if UPDATE_SCHEDULER_TASK(1, hour, minute, pause):
                    success_message_change_settings_plants.append("Gruppe 1 || Einstellungen gespeichert") 

        # plant group 2
        if request.form.get("set_time_plants_group_2") != "":
            time_plants_group_2 = request.form.get("set_time_plants_group_2")

            error_founded = False

            try:
                time   = datetime.datetime.strptime(time_plants_group_2, "%H:%M")
                hour   = time.hour
                minute = time.minute

            except:
                error_message_change_settings_plants.append("Gruppe 2 || Ungültige Uhrzeit || " + time_plants_group_2)
                error_founded = True    

            if request.form.get("checkbox_pause_plants_group_2") != None:
                pause = "True"     
            else:
                pause = "False" 

            # save settings
            if error_founded == False: 

                if UPDATE_SCHEDULER_TASK(2, hour, minute, pause):
                    success_message_change_settings_plants.append("Gruppe 2 || Einstellungen gespeichert")                      

        # plant group 3
        if request.form.get("set_time_plants_group_3") != "":
            time_plants_group_3 = request.form.get("set_time_plants_group_3")

            error_founded = False

            try:
                time   = datetime.datetime.strptime(time_plants_group_3, "%H:%M")
                hour   = time.hour
                minute = time.minute

            except:
                error_message_change_settings_plants.append("Gruppe 3 || Ungültige Uhrzeit || " + time_plants_group_3)
                error_founded = True    

            if request.form.get("checkbox_pause_plants_group_3") != None:
                pause = "True"     
            else:
                pause = "False" 

            # save settings
            if error_founded == False: 

                if UPDATE_SCHEDULER_TASK(3, hour, minute, pause):
                    success_message_change_settings_plants.append("Gruppe 3 || Einstellungen gespeichert")     
             

    plants_group_1 = GET_SCHEDULER_TASK_BY_NAME("plants_group_1")
    plants_group_2 = GET_SCHEDULER_TASK_BY_NAME("plants_group_2")
    plants_group_3 = GET_SCHEDULER_TASK_BY_NAME("plants_group_3")

    data = {'navigation': 'tasks', 'notification': ''}    

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/tasks.html',
                                                    error_message_change_settings_plants=error_message_change_settings_plants,
                                                    success_message_change_settings_plants=success_message_change_settings_plants,
                                                    plants_group_1=plants_group_1,
                                                    plants_group_2=plants_group_2,
                                                    plants_group_3=plants_group_3,
                                                    ) 
                           )