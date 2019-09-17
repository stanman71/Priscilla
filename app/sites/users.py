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


@app.route('/users.html', methods=['GET', 'POST'])
@login_required
@permission_required
def users():
    error_message_add_user = []
    error_message_change_settings = []
    message_admin_password_not_changed = ""
    
    username        = ""
    email           = ""
    password        = ""
    hashed_password = ""

    if request.method == "POST":
        
        # add user
        if request.form.get("add_user") != None: 
            
            if request.form.get("set_username") != None:
                # missing name
                if request.form.get("set_username") == "":
                    error_message_add_user.append("Keinen Benutzernamen angegeben")                                    
                else:         
                    username = request.form.get("set_username")
                    
            if request.form.get("set_email") != None:
                # missing email address
                if request.form.get("set_email") == "":
                    error_message_add_user.append("Keine eMail-Adresse angegeben")                                    
                else:         
                    email = request.form.get("set_email")  
        
            if request.form.get("set_password") != None:
                # missing password
                if request.form.get("set_password") == "":
                    error_message_add_user.append("Kein Passwort angegeben")                                    
                else:         
                    password = request.form.get("set_password")

                    if 8 <= len(password) <= 20:                
                        hashed_password = generate_password_hash(password, method='sha256')
                    else:
                        error_message_add_user.append("Passwort muss zwischen 8 und 20 Zeichen haben")


            if username != "" and email != "" and hashed_password != "":
                error = ADD_USER(username, email, hashed_password)

                if error != "":
                    error_message_add_user.append(error)
                
                username = ""
                email    = ""
                password = ""


        # change user settings
        if request.form.get("save_user_settings") != None:
            
            for i in range (1,26): 
                
                if request.form.get("set_username_" + str(i)) != None:
                    
                    check_administrator = False
            
                    # current user has permission_system ?
                    if request.form.get("set_role_" + str(i)) == "administrator":
                        check_administrator = True
                        
                    else:
                        
                        # another user has permission_system ?
                        for j in range (1,26): 
                            
                            try:
                                if (i != j) and GET_USER_BY_ID(j).role == "administrator":      
                                    check_administrator = True
                                    continue      
                                    
                            except:
                                pass


                    # one user has administrator rights
                    if check_administrator == True: 

                        # check name
                        if (request.form.get("set_username_" + str(i)) != "" and 
                            GET_USER_BY_NAME(request.form.get("set_username_" + str(i))) == None):
                            username = request.form.get("set_username_" + str(i)) 
                            
                        elif request.form.get("set_username_" + str(i)) == GET_USER_BY_ID(i).username:
                            username = GET_USER_BY_ID(i).username
                            
                        else:
                            username = GET_USER_BY_ID(i).username 
                            error_message_change_settings.append(username + " >>> Ungültige Eingabe >>> Keinen Name angegeben")                         
                        
                        
                        # check email
                        if (request.form.get("set_email_" + str(i)) != "" and 
                            GET_USER_BY_EMAIL(request.form.get("set_email_" + str(i))) == None):
                            email = request.form.get("set_email_" + str(i)) 
                        
                        elif request.form.get("set_email_" + str(i)) == GET_USER_BY_ID(i).email:
                            email = GET_USER_BY_ID(i).email
                        
                        else:
                            email = GET_USER_BY_ID(i).email 
                            error_message_change_settings.append(username + " >>> Ungültige Eingabe >>> Keine eMail-Adresse angegeben")

                        # role
                        role = request.form.get("set_role_" + str(i))

                        # notification
                        email_notification = request.form.get("set_email_notification_" + str(i))
                          
                        SET_USER_SETTINGS(i, username, email, role, email_notification)    
        
        
                        # reset password
                        if request.form.get("set_password_" + str(i)) != "":                        
                            password = request.form.get("set_password_" + str(i))
                            
                            try:
                                
                                if 8 <= len(password) <= 20:
                                    
                                    if str(password) == str(request.form.get("set_password_check_" + str(i))):
                                        
                                        hashed_password = generate_password_hash(password, method='sha256')
                            
                                        RESET_USER_PASSWORD(i, hashed_password)
                                         
                                    else:
                                        error_message_change_settings.append(username + " >>> Eingegebene Passwörter sind nicht identisch")
                                    
                                else:    
                                    error_message_change_settings.append(username + " >>> Passwort muss zwischen 8 und 20 Zeichen haben")
                                    
                            except:
                                error_message_change_settings.append(username + " >>> Passwort muss zwischen 8 und 20 Zeichen haben")
                                
             
                    # no user has administrator rights
                    else:    
                        error_message_change_settings.append("Mindestens ein Benutzer muss Administrator sein")  
           
    user_list = GET_ALL_USERS()

    try:                                        
        if GET_USER_BY_NAME("admin").password == "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339":
            message_admin_password_not_changed = "Passwort von Benutzer >admin< muss geändert werden"
    except:
        pass

    list_users = GET_ALL_USERS()

    dropdown_list_roles               = ["user", "administrator"]
    dropdown_list_email_notifications = ["none", "warnings", "all"]

    data = {'navigation': 'users', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/users.html',
                                                     error_message_add_user=error_message_add_user,
                                                     error_message_change_settings=error_message_change_settings,
                                                     message_admin_password_not_changed=message_admin_password_not_changed,
                                                     username=username,
                                                     email=email,
                                                     password=password,                         
                                                     list_users=list_users,
                                                     dropdown_list_roles=dropdown_list_roles,
                                                     dropdown_list_email_notifications=dropdown_list_email_notifications,
                                                    ) 
                           )


# delete user
@app.route('/users.html/delete/<int:id>')
@login_required
@permission_required
def delete_user(id):
    DELETE_USER(id)
    return redirect(url_for('users'))