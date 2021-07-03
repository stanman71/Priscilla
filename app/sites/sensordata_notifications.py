from flask                       import json, url_for, redirect, render_template, flash, g, session, jsonify, request, Response
from flask_login                 import current_user, login_required
from werkzeug.exceptions         import HTTPException, NotFound, abort
from functools                   import wraps

from app                         import app
from app.backend.database_models import *
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


@app.route('/sensordata/notifications', methods=['GET', 'POST'])
@login_required
@permission_required
def sensordata_notifications():
    page_title       = 'Bianca | Sensordata | Notifications'
    page_description = 'The notification configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    success_message_change_settings = []      
    error_message_change_settings   = []    
    success_message_add_job         = False       
    error_message_add_job           = []


    # delete message
    if session.get('delete_notification_job_success', None) != None:
        success_message_change_settings.append(session.get('delete_notification_job_success')) 
        session['delete_notification_job_success'] = None
        
    if session.get('delete_notification_job_error', None) != None:
        error_message_change_settings.append(session.get('delete_notification_job_error'))
        session['delete_notification_job_error'] = None       


    """ ######### """
    """  add job  """
    """ ######### """   

    if request.form.get("add_notification_job") != None: 
        result = ADD_SENSORDATA_NOTIFICATION_JOB()   
        if result != True: 
            error_message_add_job.append(result)         
        else:       
            success_message_add_job = True


    """ ############ """
    """  table jobs  """
    """ ############ """   

    if request.form.get("save_notification_jobs_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:
                error_found = False            

                # ############
                # name setting
                # ############

                notification_job = GET_SENSORDATA_NOTIFICATION_JOB_BY_ID(i)
                input_name     = request.form.get("set_name_" + str(i)).strip()                      

                # add new name
                if ((input_name != "") and (GET_SENSORDATA_NOTIFICATION_JOB_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == notification_job.name:
                    name = notification_job.name                        
                    
                # name already exist
                elif ((GET_SENSORDATA_NOTIFICATION_JOB_BY_NAME(input_name) != None) and (notification_job.name != input_name)):
                    error_message_change_settings.append(notification_job.name + " || Name - " + input_name + " - already taken")  
                    error_found = True
                    name = notification_job.name

                # no input commited
                else:                          
                    name = GET_SENSORDATA_NOTIFICATION_JOB_BY_ID(i).name
                    error_message_change_settings.append(notification_job.name + " || No name given") 
                    error_found = True  


                # ##############
                # device setting
                # ##############

                device = request.form.get("set_device_" + str(i)) 

                if GET_DEVICE_BY_IEEEADDR(device):
                    device_ieeeAddr = GET_DEVICE_BY_IEEEADDR(device).ieeeAddr
                elif GET_DEVICE_BY_ID(device):
                    device_ieeeAddr = GET_DEVICE_BY_ID(device).ieeeAddr
                else:
                    error_message_change_settings.append(notification_job.name + " || No device given") 
                    error_found = True   
  

                # ##############
                # sensor setting
                # ##############

                try:

                    # add new sensor
                    if device_ieeeAddr != "None":

                        # replace array_position to sensor name 
                        sensor_key = request.form.get("set_sensor_" + str(i))
                        sensor_key = sensor_key.replace(" ", "")
                        
                        if sensor_key.isdigit():
                            
                            # first two array elements are no sensors
                            if sensor_key == "0" or sensor_key == "1":
                                sensor_key = "None"
                                
                            else:                                
                                sensor_list = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr).input_values
                                sensor_list = sensor_list.split(",")
                                sensor_key  = sensor_list[int(sensor_key)-2]

                except:
                    error_message_change_settings.append(notification_job.name + " || No sensor given") 
                    error_found = True                      

                # ################
                # operator setting
                # ################

                operator = request.form.get("set_operator_" + str(i))

                if operator == None:
                    operator = "None"


                # #############
                # value setting
                # #############

                try: 
                    value = request.form.get("set_value_" + str(i)).strip()
                except:
                    value = "None"


                # save settings
                if error_found == False: 

                    if SET_SENSORDATA_NOTIFICATION_JOB_SETTINGS(i, name, device_ieeeAddr, sensor_key, operator, value):
                        success_message_change_settings.append(name + " || Settings successfully saved") 


    list_notification_jobs  = GET_ALL_SENSORDATA_NOTIFICATION_JOBS()
    dropdown_list_devices   = GET_ALL_DEVICES("sensors") 
    dropdown_list_operators = ["=", ">", "<"]

    error_message_settings = []
    #error_message_settings = CHECK_NOTIFICATION_JOBS(GET_ALL_NOTIFICATION_JOBS())

    data = {'navigation': 'notification_jobs'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # get sensor list
    device_input_values_list = []  

    try:
        for device in GET_ALL_DEVICES(""):
            device_input_values = "Sensor,------------------," + device.input_values
            device_input_values = device_input_values.replace(" ", "")
            device_input_values_list.append(device_input_values)
    except:
        pass 

    data = {'navigation': 'sensordata_notifications'}

    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,               
                            content=render_template( 'pages/sensordata_notifications.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_job=success_message_add_job,                            
                                                    error_message_add_job=error_message_add_job, 
                                                    error_message_settings=error_message_settings,
                                                    list_notification_jobs=list_notification_jobs,  
                                                    dropdown_list_devices=dropdown_list_devices,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    device_input_values_list=device_input_values_list,                                        
                                                    timestamp=timestamp,   
                                                    ) 
                           )


# change job position 
@app.route('/sensordata/notifications/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_notification_job_position(id, direction):
    CHANGE_SENSORDATA_NOTIFICATION_JOB_POSITION(id, direction)
    return redirect(url_for('sensordata_notifications'))


# delete job
@app.route('/sensordata/notifications/delete/<int:id>')
@login_required
@permission_required
def delete_notification_jobs(id):
    job    = GET_SENSORDATA_NOTIFICATION_JOB_BY_ID(id).name  
    result = DELETE_SENSORDATA_NOTIFICATION_JOB(id)

    if result == True:
        session['delete_notification_job_success'] = job + " || Job successfully deleted"
    else:
        session['delete_notification_job_error'] = job + " || " + str(result)

    return redirect(url_for('sensordata_notifications'))