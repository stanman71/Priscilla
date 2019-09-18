from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                 import app
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *

import datetime

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


@app.route('/devices.html', methods=['GET', 'POST'])
@login_required
@permission_required
def devices():
    

    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    # save mqtt broker setting
    if request.form.get("save_device_settings") != None:
                        
        broker   = request.form.get("set_broker")
        user     = request.form.get("set_user")
        password = request.form.get("set_password")
        
        #SET_MQTT_BROKER_SETTINGS(broker, user, password)

        #mqtt_update_hour   = request.form.get("get_mqtt_update_hour")
        #mqtt_update_minute = request.form.get("get_mqtt_update_minute")

        #mqtt_update_task = GET_SCHEDULER_TASK_BY_NAME("mqtt_update")
        


    list_devices = ""

    data = {'navigation': 'devices', 'notification': ''}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/devices.html',
                                                    list_devices=list_devices,
                                                    timestamp=timestamp,                         
                                                    ) 
                           )
