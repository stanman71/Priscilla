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
        #try:
        if current_user.role == "administrator":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout'))
       # except Exception as e:
       #     print(e)
        #    return redirect(url_for('logout'))
        
    return wrap


@app.route('/scheduler_tasks', methods=['GET', 'POST'])
@login_required
@permission_required
def scheduler_tasks():
    success_message_change_settings    = []
    error_message_change_settings      = []       
    success_message_add_scheduler_task = []
    error_message_add_scheduler_task   = []


    """ #################### """
    """  add scheduler task  """
    """ #################### """   

    if request.form.get("add_scheduler_task") != None: 
        result = ADD_SCHEDULER_TASK()   
        if result != True: 
            error_message_add_scheduler_task.append(result)         

        else:       
            success_message_add_scheduler_task = True


    """ ####################### """
    """  delete scheduler task  """
    """ ####################### """   

    for i in range (1,26):

        if request.form.get("delete_scheduler_task_" + str(i)) != None:
            scene  = GET_SCHEDULER_TASK_BY_ID(i).name  
            result = DELETE_SCHEDULER_TASK(i)            

            if result:
                success_message_change_settings.append(scene + " || Erfolgreich gelöscht") 
            else:
                error_message_change_settings.append(scene + " || " + str(result))



    list_scheduler_tasks           = GET_ALL_SCHEDULER_TASKS()

    data = {'navigation': 'scheduler_tasks', 'notification': ''}    

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/scheduler_tasks.html',
                                                    list_scheduler_tasks=list_scheduler_tasks,   
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,                         
                                                    success_message_add_scheduler_task=success_message_add_scheduler_task,
                                                    error_message_add_scheduler_task=error_message_add_scheduler_task,
                                                    ) 
                           )


# change scheduler tasks position 
@app.route('/scheduler_tasks/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_scheduler_tasks_position(id, direction):
    CHANGE_SCHEDULER_TASKS_POSITION(id, direction)
    return redirect(url_for('scheduler_tasks'))


