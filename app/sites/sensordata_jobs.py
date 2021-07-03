from flask                       import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                 import current_user, login_required
from werkzeug.exceptions         import HTTPException, NotFound, abort
from functools                   import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.file_management import GET_PATH, GET_ALL_SENSORDATA_FILES, WRITE_LOGFILE_SYSTEM
from app.backend.checks          import CHECK_SENSORDATA_JOBS
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.user_id         import SET_CURRENT_USER_ID
from app.common                  import COMMON, STATUS
from app.assets                  import *


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
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################")
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/sensordata/jobs', methods=['GET', 'POST'])
@login_required
@permission_required
def sensordata_jobs():
    page_title       = 'Bianca | Sensordata | Jobs'
    page_description = 'The sensordata jobs configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    success_message_change_settings = []      
    error_message_change_settings   = []    
    success_message_add_job         = False       
    error_message_add_job           = []
    error_message_datafile          = ""


    # delete message
    if session.get('delete_sensordata_job_success', None) != None:
        success_message_change_settings.append(session.get('delete_sensordata_job_success')) 
        session['delete_job_success'] = None
        
    if session.get('delete_sensordata_job_error', None) != None:
        error_message_change_settings.append(session.get('delete_sensordata_job_error'))
        session['delete_job_error'] = None       

    # error download datafile
    if session.get('error_datafile', None) != None:
        error_message_datafile = session.get('error_datafile') 
        session['error_datafile'] = None


    """ ######### """
    """  add job  """
    """ ######### """   

    if request.form.get("add_sensordata_job") != None: 
        result = ADD_SENSORDATA_JOB()   
        if result != True: 
            error_message_add_job.append(result)         
        else:       
            success_message_add_job = True


    """ ############ """
    """  table jobs  """
    """ ############ """   

    if request.form.get("save_sensordata_jobs_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:
                error_found = False            

                # ############
                # name setting
                # ############

                sensordata_job = GET_SENSORDATA_JOB_BY_ID(i)
                input_name     = request.form.get("set_name_" + str(i)).strip()                      

                # add new name
                if ((input_name != "") and (GET_SENSORDATA_JOB_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == sensordata_job.name:
                    name = sensordata_job.name                        
                    
                # name already exist
                elif ((GET_SENSORDATA_JOB_BY_NAME(input_name) != None) and (sensordata_job.name != input_name)):
                    error_message_change_settings.append(sensordata_job.name + " || Name - " + input_name + " - already taken")  
                    error_found = True
                    name = sensordata_job.name

                # no input commited
                else:                          
                    name = GET_SENSORDATA_JOB_BY_ID(i).name
                    error_message_change_settings.append(sensordata_job.name + " || No name given") 
                    error_found = True  


                # ################
                # filename setting
                # ################

                # add new filename
                if request.form.get("set_filename_" + str(i)) != "":
                    filename = request.form.get("set_filename_" + str(i)).strip()   

                # no input commited
                elif request.form.get("set_filename_" + str(i)) == "":                         
                    error_message_change_settings.append(sensordata_job.name + " || No filename given") 
                    error_found = True  
                    filename = sensordata_job.filename 

                # nothing changed 
                else:
                    filename = sensordata_job.filename 


                # ##############
                # device setting
                # ##############

                device = request.form.get("set_device_" + str(i)) 

                if GET_DEVICE_BY_IEEEADDR(device):
                    device_ieeeAddr = GET_DEVICE_BY_IEEEADDR(device).ieeeAddr
                elif GET_DEVICE_BY_ID(device):
                    device_ieeeAddr = GET_DEVICE_BY_ID(device).ieeeAddr
                else:
                    error_message_change_settings.append(sensordata_job.name + " || No device given") 
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
                    error_message_change_settings.append(sensordata_job.name + " || No sensor given") 
                    error_found = True        


                # #############
                # input setting
                # #############

                # input setting
                always_active = request.form.get("set_radio_input_setting_" + str(i))


                # save settings
                if error_found == False: 

                    if SET_SENSORDATA_JOB_SETTINGS(i, name, filename, device_ieeeAddr, sensor_key, always_active):
                        success_message_change_settings.append(name + " || Settings successfully saved") 


    list_sensordata_jobs  = GET_ALL_SENSORDATA_JOBS()
    dropdown_list_devices = GET_ALL_DEVICES("sensors") 
    list_sensordata_files = GET_ALL_SENSORDATA_FILES()
    list_sensors          = GET_ALL_DEVICES("sensors") 


    error_message_settings = CHECK_SENSORDATA_JOBS(GET_ALL_SENSORDATA_JOBS())

    data = {'navigation': 'sensordata_jobs'}

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


    return render_template('layouts/default.html',
                            data=data,  
                            title=page_title,        
                            description=page_description,                                 
                            content=render_template( 'pages/sensordata_jobs.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_job=success_message_add_job,                            
                                                    error_message_add_job=error_message_add_job, 
                                                    error_message_settings=error_message_settings,
                                                    error_message_datafile=error_message_datafile,    
                                                    list_sensordata_jobs=list_sensordata_jobs,  
                                                    dropdown_list_devices=dropdown_list_devices,
                                                    list_sensordata_files=list_sensordata_files,
                                                    list_sensors=list_sensors,
                                                    device_input_values_list=device_input_values_list,                                        
                                                    timestamp=timestamp,                                                         
                                                    ) 
                           )


# change job position 
@app.route('/sensordata/jobs/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_sensordata_job_position(id, direction):
    CHANGE_SENSORDATA_JOB_POSITION(id, direction)
    return redirect(url_for('sensordata_jobs'))


# delete job
@app.route('/sensordata/jobs/delete/<int:id>')
@login_required
@permission_required
def delete_sensordata_jobs(id):
    job    = GET_SENSORDATA_JOB_BY_ID(id).name  
    result = DELETE_SENSORDATA_JOB(id)

    if result == True:
        session['delete_sensordata_job_success'] = job + " || Job successfully deleted"
    else:
        session['delete_sensordata_job_error'] = job + " || " + str(result)

    return redirect(url_for('sensordata_jobs'))


# download sensordata file
@app.route('/sensordata/download/file/<string:filename>')
@login_required
@permission_required
def download_sensordata_file(filename):
    try:
        path = GET_PATH() + "/data/csv/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/csv/" + filename + " | downloaded")
        return send_from_directory(path, filename)
        
    except Exception as e:
        session['error_datafile'] = "Download Datafile || " + str(e)


# delete sensordata file
@app.route('/sensordata/delete/<string:filename>')
@login_required
@permission_required
def delete_sensordata_file(filename):
    result = DELETE_SENSORDATA_FILE(filename)

    if result != True:
        session['error_datafile'] = result

    return redirect(url_for('sensordata_jobs'))