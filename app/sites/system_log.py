from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import RESET_LOGFILE, GET_LOGFILE_SYSTEM, GET_PATH, WRITE_LOGFILE_SYSTEM
from app.common                  import COMMON, STATUS
from app.assets                  import *

import datetime
import os

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


@app.route('/system_log', methods=['GET', 'POST'])
@login_required
@permission_required
def system_log():
    success_message_logfile = False
    error_message_logfile   = ""
    
    selected_type_event    = "selected"
    selected_type_status   = "selected"
    selected_type_database = "selected"    
    selected_type_success  = "selected"   
    selected_type_warning  = "selected"                                                      
    selected_type_error    = "selected"
    log_search             = ""    

    # error download logfile
    if session.get('error_download_log', None) != None:
        error_message_logfile = session.get('error_download_log')
        session['error_download_log'] = None

    # create log types list
    selected_log_types = ["EVENT", "STATUS", "DATABASE", "SUCCESS", "WARNING", "ERROR"]     
   
    # change log selection 
    if request.form.get("get_log_output") != None:   
   
        selected_type_event    = ""
        selected_type_status   = ""
        selected_type_database = ""        
        selected_type_success  = ""   
        selected_type_warning  = ""                                                     
        selected_type_error    = ""
        
        selected_log_types = [] 
   
        list_selection = request.form.getlist('set_log_types[]')

        for element in list_selection:
            
            if element == "EVENT":
                selected_type_event = "selected"
                selected_log_types.append("EVENT")
            if element == "STATUS":
                selected_type_status = "selected"
                selected_log_types.append("STATUS")    
            if element == "DATABASE":
                selected_type_database = "selected"
                selected_log_types.append("DATABASE")                               
            if element == "SUCCESS":
                selected_type_success = "selected"
                selected_log_types.append("SUCCESS")                
            if element == "WARNING":
                selected_type_warning = "selected"
                selected_log_types.append("WARNING")                
            if element == "ERROR":
                selected_type_error = "selected"
                selected_log_types.append("ERROR")     

        log_search = request.form.get('set_log_search')
       
   
    # reset logfile
    if request.form.get("reset_logfile") != None: 
        result = RESET_LOGFILE("log_system")  

        if result:
            success_message_logfile = True 
        else:
            error_message_logfile = "Reset Log || " + str(result)

    # get log entries
    if GET_LOGFILE_SYSTEM(selected_log_types, 50, log_search) != None:
        data_log_system = GET_LOGFILE_SYSTEM(selected_log_types, 50, log_search)
    else:
        data_log_system = ""

    # check data_log_system is string ?
    if isinstance(data_log_system, str):   
        error_message_logfile = data_log_system                

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    data = {'navigation': 'system_log', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/system_log.html', 
                                                    error_message_logfile=error_message_logfile,
                                                    success_message_logfile=success_message_logfile,
                                                    timestamp=timestamp,
                                                    selected_type_event=selected_type_event,
                                                    selected_type_status=selected_type_status,
                                                    selected_type_database=selected_type_database,                            
                                                    selected_type_success=selected_type_success,    
                                                    selected_type_warning=selected_type_warning,                                                      
                                                    selected_type_error=selected_type_error,                    
                                                    data_log_system=data_log_system,  
                                                    log_search=log_search,                                     
                                                    ) 
                           )


# download system logfile
@app.route('/system_log/download/<path:filepath>')
@login_required
@permission_required
def download_system_log(filepath): 
    path = GET_PATH() + "/logs/"  

    try:
        if os.path.isfile(path + filepath) is False:
            RESET_LOGFILE("log_system")  
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filepath + " | downloaded") 

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filepath + " | " + str(e))
        session['error_download_log'] = "Download Log || " + str(e)

    return send_from_directory(path, filepath)