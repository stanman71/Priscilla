from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.security   import generate_password_hash
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


@app.route('/settings/users', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_users():
    success_message_add_user           = False
    error_message_add_user             = []
    success_message_change_settings    = []
    error_message_change_settings      = []

    message_admin_password_not_changed = ""

    name            = ""
    email           = ""
    password        = ""
    password_repeat = ""
    hashed_password = ""

    # delete message
    if session.get('delete_user_success', None) != None:
        success_message_change_settings.append(session.get('delete_user_success')) 
        session['delete_user_success'] = None
        
    if session.get('delete_user_error', None) != None:
        error_message_change_settings.append(session.get('delete_user_error'))
        session['delete_user_error'] = None       


    """ ########## """
    """  add user  """
    """ ########## """    

    if request.form.get("add_user") != None: 
        result = ADD_USER()

        if result != True:
            error_message_add_user.append(result)
        else:
            success_message_add_user = True


    """ ############# """
    """  table users  """
    """ ############# """    

    if request.form.get("save_user_settings") != None:
        
        for i in range (1,26): 
            
            if request.form.get("set_name_" + str(i)) != None:
                
                error_founded       = False
                hashed_password     = None


                # ############
                # name setting
                # ############

                user       = GET_USER_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i)).strip()    
            
                # add new name
                if ((input_name != "") and (GET_USER_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == user.name:
                    name = user.name                        
                    
                # name already exist
                elif ((GET_USER_BY_NAME(input_name) != None) and (user.name != input_name)):
                    error_message_change_settings.append(user.name + " || Name - " + input_name + " - bereits vergeben")  
                    error_founded = True
                    name = user.name

                # no input commited
                else:                          
                    name = GET_USER_BY_ID(i).name
                    error_message_change_settings.append(user.name + " || Keinen Namen angegeben") 
                    error_founded = True  


                # #############
                # email setting
                # #############

                input_email = request.form.get("set_email_" + str(i)).strip()                    

                # add new name
                if ((input_email != "") and (GET_USER_BY_EMAIL(input_email) == None)):
                    email = request.form.get("set_email_" + str(i)) 
                    
                # nothing changed 
                elif input_email == user.email:
                    email = user.email                        
                    
                # email already exist
                elif ((GET_USER_BY_EMAIL(input_email) != None) and (user.email != input_email)):
                    error_message_change_settings.append(user.name + " || eMail-Adresse - " + input_email + " - bereits vergeben") 
                    error_founded = True
                    email = user.email 

                # no input commited
                else:                          
                    email = GET_USER_BY_ID(i).email
                    error_message_change_settings.append(user.name + " || Keine eMail-Adresse angegeben") 
                    error_founded = True  


                # ################
                # password setting
                # ################
                
                if request.form.get("set_password_" + str(i)) != "":                        
                    password = request.form.get("set_password_" + str(i)).strip()
                    
                    try:              
                        if 8 <= len(password) <= 20:
                            
                            if str(password) == str(request.form.get("set_password_repeat_" + str(i)).strip()):
                                hashed_password = generate_password_hash(password, method='sha256')
                                    
                            else:
                                error_message_change_settings.append(user.name + " || Eingegebene Passwörter sind nicht identisch")
                            
                        else:    
                            error_message_change_settings.append(user.name + " || Passwort muss zwischen 8 und 20 Zeichen haben")
                            
                    except:
                        error_message_change_settings.append(user.name + " || Passwort muss zwischen 8 und 20 Zeichen haben")


                # role
                role = request.form.get("radio_role_" + str(i))

                # notification
                if request.form.get("checkbox_email_notification_" + str(i)) != None:
                    email_notification = "True"
                else:
                    email_notification = "False"


                # save settings
                if error_founded == False: 

                    changes_saved = False

                    if UPDATE_USER_SETTINGS(i, name, email, role, email_notification):   
                        changes_saved = True

                    if hashed_password != None:                             
                        if CHANGE_USER_PASSWORD(i, hashed_password):
                            changes_saved = True

                    if changes_saved == True:
                        success_message_change_settings.append(name + " || Einstellungen erfolgreich gespeichert") 


    user_list = GET_ALL_USERS()

    try:                                        
        if GET_USER_BY_NAME("admin").password == "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339":
            message_admin_password_not_changed = "admin || Passwort muss geändert werden"
    except:
        pass

    list_users = GET_ALL_USERS()

    data = {'navigation': 'settings'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/settings_users.html',
                                                     error_message_change_settings=error_message_change_settings,                            
                                                     error_message_add_user=error_message_add_user,
                                                     message_admin_password_not_changed=message_admin_password_not_changed,
                                                     success_message_change_settings=success_message_change_settings,                                                     
                                                     success_message_add_user=success_message_add_user,                
                                                     list_users=list_users,
                                                    ) 
                           )


# delete user
@app.route('/settings/users/delete/<int:id>')
@login_required
@permission_required
def delete_user(id):
    name   = GET_USER_BY_ID(id).name
    result = DELETE_USER(id)

    if result == True:
        session['delete_user_success'] = name + " || Erfolgreich gelöscht"
    else:
        session['delete_user_error'] = name + " || " + str(result)

    return redirect(url_for('settings_users'))