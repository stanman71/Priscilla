from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.checks          import CHECK_TASKS
from app.common                  import COMMON, STATUS
from app.assets                  import *


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


@app.route('/settings/speechcontrol', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_speechcontrol():
    success_message_change_settings        = []      
    error_message_change_settings          = []    
    success_message_add_speechcontrol_task = False       
    error_message_add_speechcontrol_task   = []

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'


    # delete message
    if session.get('delete_speechcontrol_task_success', None) != None:
        success_message_change_settings.append(session.get('delete_speechcontrol_task_success')) 
        session['delete_speechcontrol_task_success'] = None
        
    if session.get('delete_speechcontrol_task_error', None) != None:
        error_message_change_settings.append(session.get('delete_speechcontrol_task_error'))
        session['delete_speechcontrol_task_error'] = None       


    """ ######################## """
    """  add speechcontrol task  """
    """ ######################## """   

    if request.form.get("add_speechcontrol_task") != None: 
        result = ADD_SPEECHCONTROL_TASK()   
        if result != True: 
            error_message_add_speechcontrol_task.append(result)         

        else:       
            success_message_add_speechcontrol_task = True


    """ ########################### """
    """  table speechcontrol tasks  """
    """ ########################### """   

    if request.form.get("save_speechcontrol_task_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                error_founded = False     

                # ############
                # name setting
                # ############

                speechcontrol_task = GET_SPEECHCONTROL_TASK_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i))                    

                # add new name
                if ((input_name != "") and (GET_SPEECHCONTROL_TASK_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == speechcontrol_task.name:
                    name = speechcontrol_task.name                        
                    
                # name already exist
                elif ((GET_SPEECHCONTROL_TASK_BY_NAME(input_name) != None) and (speechcontrol_task.name != input_name)):
                    error_message_change_settings.append(speechcontrol_task.name + " || Name bereits vergeben")  
                    name = speechcontrol_task.name
                    error_founded = True  

                # no input commited
                else:                          
                    name = GET_SPEECHCONTROL_TASK_BY_ID(i).name
                    error_message_change_settings.append(speechcontrol_task.name + " || Keinen Namen angegeben") 
                    error_founded = True  

                # ############
                # task setting
                # ############

                if request.form.get("set_task_" + str(i)) != "":
                    task = request.form.get("set_task_" + str(i))

                else:
                    error_message_change_settings.append(speechcontrol_task.name + " || Keine Aufgabe angegeben") 
                    error_founded = True                      

                # ###############
                # keyword setting
                # ###############

                if request.form.get("set_keywords_" + str(i)) != "":
                    keywords = request.form.get("set_keywords_" + str(i))

                else:
                    error_message_change_settings.append(speechcontrol_task.name + " || Keine Schlüsselwörter angegeben") 
                    error_founded = True            

                # ############
                # option pause
                # ############

                # set checkbox pause
                if request.form.get("checkbox_option_pause_" + str(i)):
                    option_pause = "True"
                else:
                    option_pause = ""  

                # #############
                # save settings
                # #############

                if error_founded == False: 

                    if SET_SPEECHCONTROL_TASK(i, name, task, keywords, option_pause):
                        success_message_change_settings.append(speechcontrol_task.name + " || Einstellungen gespeichert") 


    list_speechcontrol_tasks = GET_ALL_SPEECHCONTROL_TASKS()

    error_message_speechcontrol_tasks = CHECK_TASKS(GET_ALL_SPEECHCONTROL_TASKS(), "speechcontrol")

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_speechcontrol.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_speechcontrol_task=success_message_add_speechcontrol_task,                            
                                                    error_message_add_speechcontrol_task=error_message_add_speechcontrol_task,     
                                                    error_message_speechcontrol_tasks=error_message_speechcontrol_tasks,                                                                                         
                                                    list_speechcontrol_tasks=list_speechcontrol_tasks, 
                                                    ) 
                           )


# change speechcontrol tasks position 
@app.route('/settings/speechcontrol/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_speechcontrol_tasks_position(id, direction):
    CHANGE_SPEECHCONTROL_TASKS_POSITION(id, direction)
    return redirect(url_for('settings_speechcontrol'))


# delete speechcontrol task
@app.route('/settings/speechcontrol/delete/<int:id>')
@login_required
@permission_required
def delete_speechcontrol_task(id):
    speechcontrol_task_name = GET_SPEECHCONTROL_TASK_BY_ID(id).name  
    result                  = DELETE_SPEECHCONTROL_TASK(id)

    if result:
        session['delete_speechcontrol_task_success'] = speechcontrol_task_name + " || Erfolgreich gelöscht"
    else:
        session['delete_speechcontrol_task_error'] = speechcontrol_task_name + " || " + str(result)

    return redirect(url_for('settings_speechcontrol'))