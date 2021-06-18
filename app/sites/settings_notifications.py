from flask                       import json, url_for, redirect, render_template, flash, g, session, jsonify, request, Response
from flask_login                 import current_user, login_required
from werkzeug.exceptions         import HTTPException, NotFound, abort
from functools                   import wraps

from app                         import app
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.user_id         import SET_CURRENT_USER_ID
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


@app.route('/settings/notifications', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_notifications():
    page_title       = 'Bianca | Settings | Notifications'
    page_description = 'The notification configuration page'

    SET_CURRENT_USER_ID(current_user.id)  



    data = {'navigation': 'settings_notifications'}

    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,               
                            content=render_template( 'pages/settings_notifications.html',


                                                    ) 
                           )