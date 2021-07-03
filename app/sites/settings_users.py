from flask                       import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                 import current_user, login_required
from werkzeug.security           import generate_password_hash
from werkzeug.exceptions         import HTTPException, NotFound, abort
from functools                   import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.checks          import CHECK_USERS
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


@app.route('/settings/users', methods=['GET', 'POST'])
@login_required
@permission_required
def settings_users():
    page_title       = 'Bianca | Settings | Users'
    page_description = 'The users configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    success_message_add_user        = False
    error_message_add_user          = []
    error_message_missing_passwords = []
    success_message_change_settings = []
    error_message_change_settings   = []

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

            if request.form.get("set_email_" + str(i)) != None:

                error_found     = False
                hashed_password = None


                # ############
                # name setting
                # ############

                user       = GET_USER_BY_ID(i)

                if user.name != "admin":

                    input_name = request.form.get("set_name_" + str(i)).strip()    
                
                    # add new name
                    if ((input_name != "") and (GET_USER_BY_NAME(input_name) == None)):
                        name = request.form.get("set_name_" + str(i)) 
                        
                    # nothing changed 
                    elif input_name == user.name:
                        name = user.name                        
                        
                    # name already exist
                    elif ((GET_USER_BY_NAME(input_name) != None) and (user.name != input_name)):
                        error_message_change_settings.append(user.name + " || Name - " + input_name + " - already taken")  
                        error_found = True
                        name = user.name

                    # no input commited
                    else:                          
                        name = GET_USER_BY_ID(i).name
                        error_message_change_settings.append(user.name + " || No name given") 
                        error_found = True  

                else:
                    name = user.name   


                # #############
                # email setting
                # #############

                input_email = request.form.get("set_email_" + str(i)).strip()        

                # add new email
                if GET_USER_BY_EMAIL(input_email) == None:
                    email = request.form.get("set_email_" + str(i)).strip()   
                    
                # nothing changed 
                elif input_email == user.email:
                    email = user.email                        

                # email already exist
                else:
                    error_message_change_settings.append(user.name + " || eMail - " + input_email + " - already taken")  
                    error_found = True
                    email       = user.email


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
                                error_message_change_settings.append(user.name + " || Passwords are not identical")
                            
                        else:    
                            error_message_change_settings.append(user.name + " || Password must have between 8 and 20 characters")
                            
                    except:
                        error_message_change_settings.append(user.name + " || Password must have between 8 and 20 characters")

                # role
                role = request.form.get("set_radio_role_" + str(i))

                # system_notifications
                if request.form.get("set_checkbox_system_notifications_" + str(i)):

                    if email == "":
                        error_message_change_settings.append(user.name + " || No eMail address found >>> Deactivate System Notifications")
                        system_notifications = "False"

                    else:
                        system_notifications = "True"

                else:
                    system_notifications = "False"

                # sensor_notifications
                if request.form.get("set_checkbox_sensor_notifications_" + str(i)):

                    if email == "":
                        error_message_change_settings.append(user.name + " || No eMail address found >>> Deactivate Sensor Notifications")
                        sensor_notifications = "False"

                    else:
                        sensor_notifications = "True"

                else:
                    sensor_notifications = "False"


                # save settings
                if error_found == False: 

                    changes_saved = False

                    if UPDATE_USER_SETTINGS(i, name, email, role, system_notifications, sensor_notifications):   
                        changes_saved = True

                    if hashed_password != None:                             
                        if CHANGE_USER_PASSWORD(i, hashed_password):
                            changes_saved = True

                    if changes_saved == True:
                        success_message_change_settings.append(name + " || Settings successfully saved") 

    list_users = GET_ALL_USERS()


    # check passwords
    try:                                        
        if GET_USER_BY_NAME("admin").password == "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339":
            message_admin_password_not_changed = "admin || Password must be changed"
    except:
        pass

    error_message_settings = CHECK_USERS(GET_ALL_USERS())

    data = {'navigation': 'settings_users'}

    return render_template('layouts/default.html',
                            data=data,  
                            title=page_title,        
                            description=page_description, 
                            content=render_template( 'pages/settings_users.html',
                                                     error_message_change_settings=error_message_change_settings,                            
                                                     error_message_add_user=error_message_add_user,
                                                     message_admin_password_not_changed=message_admin_password_not_changed,
                                                     success_message_change_settings=success_message_change_settings,                                                     
                                                     success_message_add_user=success_message_add_user,    
                                                     error_message_settings=error_message_settings,            
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
        session['delete_user_success'] = name + " || User successfully deleted"
    else:
        session['delete_user_error'] = name + " || " + str(result)

    return redirect(url_for('settings_users'))