from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, Response
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app         import app
from app.common  import COMMON, STATUS
from app.assets  import *


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "user" or current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/about', methods=['GET', 'POST'])
@login_required
@permission_required
def about():
    page_title       = 'Callisto | About'
    page_description = 'The information and update page.'

    version = "2.5"

    data = {'navigation': 'about'}

    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,               
                            content=render_template( 'pages/about.html',
                                                     version=version,                                                   
                                                    ) 
                           )

