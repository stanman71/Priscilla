from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                 import app
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *

import os, shutil, re, cgi
        

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


# Used only for static export
@app.route('/dashboard.html')
@login_required
@permission_required
def dashboard():

    # custommize your page title / description here
    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    data = {'navigation': 'dashboard', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,
                            content=render_template( 'pages/dashboard.html') )


# Used only for static export
@app.route('/user.html')
@login_required
@permission_required
def user():

    # custommize your page title / description here
    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    data = {'navigation': '', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/user.html') )


# Used only for static export
@app.route('/icons.html')
@login_required
@permission_required
def icons():

    # custommize your page title / description here
    page_title = 'Icons - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the icons page.'

    data = {'navigation': 'icons', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/icons.html') )

# Used only for static export
@app.route('/tables.html')
@login_required
@permission_required
def tables():

    # custommize your page title / description here
    page_title = 'Tables - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    data = {'navigation': '', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/tables.html') )

# Used only for static export
@app.route('/notifications.html')
@login_required
@permission_required
def notifications():

    # custommize your page title / description here
    page_title = 'Tables - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    data = {'navigation': '', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/notifications.html') )

# Used only for static export
@app.route('/typography.html')
@login_required
@permission_required
def typography():

    # custommize your page title / description here
    page_title = 'Typography - Flask Dark Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Dark Dashboard, the tables page.'

    data = {'navigation': '', 'notification': ''}

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/typography.html') )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    content = None

    try:

        # try to match the pages defined in -> themes/light-bootstrap/pages/
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
    except:
        abort(404)

