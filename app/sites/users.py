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


@app.route('/users', methods=['GET', 'POST'])
@login_required
@permission_required
def users():
    success_message_add_user           = False
    error_message_add_user             = []
    success_message_change_settings    = []
    error_message_change_settings      = []

    message_admin_password_not_changed = ""

    username        = ""
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


    """ ############### """
    """  user settings  """
    """ ############### """    

    if request.form.get("save_user_settings") != None:
        
        for i in range (1,26): 
            
            if request.form.get("set_username_" + str(i)) != None:
                
                check_administrator = False
                error_founded       = False
                hashed_password     = None
                current_username    = GET_USER_BY_ID(i).username

                # current user has administrator rights ?
                if request.form.get("checkbox_administrator_" + str(i)) != None:
                    check_administrator = True
                    
                else:
                    
                    # another user has administrator rights ?
                    for j in range (1,26): 
                        
                        try:
                            if (i != j) and GET_USER_BY_ID(j).role == "administrator":      
                                check_administrator = True
                                continue      
                                
                        except:
                            pass


                # one user has administrator rights
                if check_administrator == True: 

                    # change username   
                    if request.form.get("set_username_" + str(i)) != "":
                                        
                        new_username = request.form.get("set_username_" + str(i))

                        if new_username != current_username:       

                            # username already exist ?    
                            if not GET_USER_BY_NAME(new_username):  
                                username = new_username                            
                            else: 
                                error_message_change_settings.append(current_username + " || Name bereits vergeben")  
                                error_founded = True
                                username = current_username

                        else:
                            username = current_username

                    else:
                        username = GET_USER_BY_ID(i).username
                        error_message_change_settings.append(current_username + " || Keinen Namen angegeben") 
                        error_founded = True  
               

                    # change email  
                    if request.form.get("set_email_" + str(i)) != "":
                                        
                        new_email = request.form.get("set_email_" + str(i))
                        old_email = GET_USER_BY_ID(i).email

                        if new_email != old_email: 

                            # email already exist ?         
                            if not GET_USER_BY_EMAIL(new_email):  
                                email = new_email                            
                            else: 
                                error_message_change_settings.append(current_username + " || eMail-Adresse bereits vergeben")   
                                error_founded = True 
                                email = old_email

                        else:
                            email = old_email

                    else:
                        email = GET_USER_BY_ID(i).email
                        error_message_change_settings.append(current_username + " || Keine eMail-Adresse angegeben")   
                        error_founded = True

                     # change password
                    if request.form.get("set_password_" + str(i)) != "":                        
                        password = request.form.get("set_password_" + str(i))
                        
                        try:              
                            if 8 <= len(password) <= 20:
                                
                                if str(password) == str(request.form.get("set_password_repeat_" + str(i))):
                                    hashed_password = generate_password_hash(password, method='sha256')
                                       
                                else:
                                    error_message_change_settings.append(current_username + " || Eingegebene Passwörter sind nicht identisch")
                                
                            else:    
                                error_message_change_settings.append(current_username + " || Passwort muss zwischen 8 und 20 Zeichen haben")
                                
                        except:
                            error_message_change_settings.append(current_username + " || Passwort muss zwischen 8 und 20 Zeichen haben")

                    # role
                    if request.form.get("checkbox_administrator_" + str(i)) != None:
                        role = "administrator"
                    else:
                        role = "user"

                    # notification
                    if request.form.get("checkbox_email_notification_" + str(i)) != None:
                        email_notification = "True"
                    else:
                        email_notification = "False"


                    # save settings
                    if error_founded == False: 

                        changes_saved = False

                        if UPDATE_USER_SETTINGS(i, username, email, role, email_notification):   
                            changes_saved = True

                        if hashed_password != None:                             
                            if CHANGE_USER_PASSWORD(i, hashed_password):
                                changes_saved = True

                        if changes_saved == True:
                            success_message_change_settings.append(username + " || Einstellungen erfolgreich gespeichert") 

                    username        = ""
                    email           = ""
                    password        = ""      
                    password_repeat = "" 
                                        
                # no user has administrator rights
                else:    
                    error_message_change_settings.append("Mindestens ein Benutzer muss Administrator sein")  


    """ ########## """
    """  add user  """
    """ ########## """    

    if request.form.get("add_user") != None: 
        
        if request.form.get("set_username") != None:
            # missing name
            if request.form.get("set_username") == "":
                error_message_add_user.append("Keinen Benutzernamen angegeben")   
            elif GET_USER_BY_NAME(request.form.get("set_username")):  
                error_message_add_user.append("Benutzername bereits vergeben")                                                   
            else:         
                username = request.form.get("set_username")
                
        if request.form.get("set_email") != None:
            # missing email address
            if request.form.get("set_email") == "":
                error_message_add_user.append("Keine eMail-Adresse angegeben") 
            elif GET_USER_BY_EMAIL(request.form.get("set_email")):  
                error_message_add_user.append("eMail-Adresse bereits vergeben")   
            else:         
                email = request.form.get("set_email")  
    
        if request.form.get("set_password") != None:
            # missing password
            if request.form.get("set_password") == "":
                error_message_add_user.append("Kein Passwort angegeben")    
            elif request.form.get("set_password_repeat") == "":
                error_message_add_user.append("Passwort nicht bestätigt")                                    
            else:         
                password        = request.form.get("set_password")
                password_repeat = request.form.get("set_password_repeat")

                if password == password_repeat:

                    if 8 <= len(password) <= 20:                
                        hashed_password = generate_password_hash(password, method='sha256')
                    else:
                        error_message_add_user.append("Passwort muss zwischen 8 und 20 Zeichen haben")

                else:
                    error_message_add_user.append("Passworter nicht identisch")  

        if username != "" and email != "" and hashed_password != "":
            error = ADD_USER(username, email, hashed_password)

            if error != None:
                error_message_add_user.append(error)

            else:
                success_message_add_user = True
                username        = ""
                email           = ""
                password        = ""
                password_repeat = ""


    user_list = GET_ALL_USERS()

    try:                                        
        if GET_USER_BY_NAME("admin").password == "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339":
            message_admin_password_not_changed = "admin || Passwort muss geändert werden"
    except:
        pass

    list_users = GET_ALL_USERS()

    data = {'navigation': 'users', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/users.html',
                                                     error_message_change_settings=error_message_change_settings,                            
                                                     error_message_add_user=error_message_add_user,
                                                     message_admin_password_not_changed=message_admin_password_not_changed,
                                                     success_message_change_settings=success_message_change_settings,                                                     
                                                     success_message_add_user=success_message_add_user,
                                                     username=username,
                                                     email=email,
                                                     password=password,  
                                                     password_repeat=password_repeat,                      
                                                     list_users=list_users,
                                                    ) 
                           )


# delete user
@app.route('/users/delete/<int:id>')
@login_required
@permission_required
def delete_user(id):
    username = GET_USER_BY_ID(id).username
    result   = DELETE_USER(id)

    if result:
        session['delete_user_success'] = username + " || Erfolgreich gelöscht"
    else:
        session['delete_user_error'] = username + " || " + str(result)

    return redirect(url_for('users'))