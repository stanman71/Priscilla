from flask                     import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login               import current_user, login_required
from werkzeug.exceptions       import HTTPException, NotFound, abort
from functools                 import wraps
from flask_mobility.decorators import mobile_template

from app                          import app, socketio
from app.backend.database_models  import *


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


@app.route('/devices/gpio', methods=['GET', 'POST'])
@login_required
@permission_required
def devices_gpio():
    page_title       = 'Bianca | Devices | GPIO'
    page_description = 'The GPIO configuration page'



    data = {'navigation': 'devices_gpio'}

    return render_template('layouts/default.html',
                            async_mode=socketio.async_mode,
                            data=data,
                            title=page_title,        
                            description=page_description,                               
                            content=render_template( 'pages/devices_gpio.html', 
                                           

                                                    ) 
                           )      