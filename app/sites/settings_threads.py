from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.process_program import * 
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
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
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################")
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/settings/threads', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_threads():
    page_title       = 'Bianca | Settings | Threads'
    page_description = 'The threads overview page.'

    success_message_program_stop = "" 
    error_message_program_stop   = ""

    # stop message
    if session.get('program_stop_success', None) != None:
        success_message_program_stop = session.get('program_stop_success')
        session['program_stop_success'] = None
        
    if session.get('program_stop_error', None) != None:
        error_message_program_stop = session.get('program_stop_error')
        session['program_stop_error'] = None      


    data = {'navigation': 'settings_threads'}    

    return render_template('layouts/default.html',
                            data=data, 
                            title=page_title,        
                            description=page_description,                                  
                            content=render_template( 'pages/settings_threads.html',
                                                    success_message_program_stop=success_message_program_stop,
                                                    error_message_program_stop=error_message_program_stop,                            
                                                    ) 
                           )


# stop program 
@app.route('/settings/threads/stop/<int:id>')
@login_required
@permission_required
def stop_program(id):
    timer = 0

    while timer < 5:

        if id == 1 and GET_PROGRAM_THREAD_STATUS_1()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 1 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 1 not stopped"

        if id == 2 and GET_PROGRAM_THREAD_STATUS_2()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 2 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 2 not stopped"

        if id == 3 and GET_PROGRAM_THREAD_STATUS_3()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 3 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 3 not stopped"

        if id == 4 and GET_PROGRAM_THREAD_STATUS_4()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 4 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 4 not stopped"

        if id == 5 and GET_PROGRAM_THREAD_STATUS_5()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 5 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 5 not stopped"

        if id == 6 and GET_PROGRAM_THREAD_STATUS_6()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 6 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 6 not stopped"

        if id == 7 and GET_PROGRAM_THREAD_STATUS_7()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 7 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 7 not stopped"

        if id == 8 and GET_PROGRAM_THREAD_STATUS_8()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 8 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 8 not stopped"     

        if id == 9 and GET_PROGRAM_THREAD_STATUS_9()[0] != "None":
            if STOP_PROGRAM_THREAD_BY_ID(id): 
                session['program_stop_success'] = "Thread 9 successfully stopped"
                break
            else:
                session['program_stop_error'] = "Thread 9 not stopped"

        time.sleep(1)
        timer = timer + 1

    return redirect(url_for('settings_threads'))