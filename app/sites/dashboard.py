from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                 import app, socketio
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *

import os, shutil, re, cgi


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "dashboard_only" or current_user.role == "user" or current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/dashboard')
@login_required
@permission_required
def dashboard():

    # custommize your page title / description here
    page_title       = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    dropdown_list_led_scenes = GET_ALL_LED_SCENES()
    list_led_groups          = GET_ALL_LED_GROUPS()

    data = {'navigation': 'dashboard'}

    return render_template('layouts/default.html',
                            async_mode=socketio.async_mode,
                            data=data,
                            content=render_template( 'pages/dashboard.html', 
                                                    list_led_groups=list_led_groups,
                                                    dropdown_list_led_scenes=dropdown_list_led_scenes,                       
                                                    ) 
                           )      