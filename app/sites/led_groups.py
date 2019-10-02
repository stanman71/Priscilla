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


@app.route('/led/groups', methods=['GET', 'POST'])
@login_required
@permission_required
def led_groups():

    data = {'navigation': 'led', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/led_groups.html', 
                                                    ) 
                           )


# change led_groups position 
@app.route('/led/groups/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_led_groups_position(id, direction):
    CHANGE_LED_GROUPS_POSITION(id, direction)
    return redirect(url_for('led_groups'))