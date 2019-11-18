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

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'


    """ ########################### """
    """  table speechcontrol tasks  """
    """ ########################### """   

    if request.form.get("save_speechcontrol_task_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_keywords_" + str(i)) != None:

                speechcontrol_task = GET_SPEECHCONTROL_TASK_BY_ID(i)

                # ###############
                # keyword setting
                # ###############

                keywords = request.form.get("set_keywords_" + str(i))


                # #############
                # save settings
                # #############

                if SET_SPEECHCONTROL_TASK(i, keywords):
                    success_message_change_settings.append(speechcontrol_task.name + " || Einstellungen gespeichert") 


    list_speechcontrol_tasks = GET_ALL_SPEECHCONTROL_TASKS()

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_speechcontrol.html',
                                                    success_message_change_settings=success_message_change_settings,                                                                                                                    
                                                    list_speechcontrol_tasks=list_speechcontrol_tasks, 
                                                    ) 
                           )