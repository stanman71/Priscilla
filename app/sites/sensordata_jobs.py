from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.database.models          import *
from app.backend.file_management  import GET_PATH, GET_SENSORDATA_FILES, WRITE_LOGFILE_SYSTEM
from app.common                   import COMMON, STATUS
from app.assets                   import *


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


@app.route('/sensordata/jobs', methods=['GET', 'POST'])
@login_required
@permission_required
def sensordata_jobs():
    page_title = 'Smarthome | Sensordata | Jobs'
    page_description = 'The sensordata jobs configuration page.'

    success_message_change_settings = []      
    error_message_change_settings   = []    
    success_message_add_job         = False       
    error_message_add_job           = []
    error_message_datafile          = ""

    # delete message
    if session.get('delete_job_success', None) != None:
        success_message_change_settings.append(session.get('delete_job_success')) 
        session['delete_job_success'] = None
        
    if session.get('delete_job_error', None) != None:
        error_message_change_settings.append(session.get('delete_job_error'))
        session['delete_job_error'] = None       

    # error download datafile
    if session.get('error_download_datafile', None) != None:
        error_message_datafile = session.get('error_download_datafile') 
        session['error_download_datafile'] = None


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

                error_founded = False            

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
                    error_message_change_settings.append(sensordata_job.name + " || Name - " + input_name + " - bereits vergeben")  
                    error_founded = True
                    name = sensordata_job.name

                # no input commited
                else:                          
                    name = GET_SENSORDATA_JOB_BY_ID(i).name
                    error_message_change_settings.append(sensordata_job.name + " || Keinen Namen angegeben") 
                    error_founded = True  


                # ################
                # filename setting
                # ################

                if request.form.get("set_filename_" + str(i)) != "":
                    filename = request.form.get("set_filename_" + str(i)).strip()   
                else:
                    filename = GET_SENSORDATA_JOB_BY_ID(i).filename 
                    error_message_change_settings.append(sensordata_job.name + " >>> Keine Datei angegeben")  


                # ##############
                # device setting
                # ##############

                device = request.form.get("set_device_" + str(i)) 

                if GET_DEVICE_BY_IEEEADDR(device):
                    device_ieeeAddr = GET_DEVICE_BY_IEEEADDR(device).ieeeAddr
                elif GET_DEVICE_BY_ID(device):
                    device_ieeeAddr = GET_DEVICE_BY_ID(device).ieeeAddr
                else:
                    error_message_change_settings.append(sensordata_job.name + " >>> Kein Gerät angegeben") 
                    device_ieeeAddr = ""
                    sensor_key      = ""
  

                # ##############
                # sensor setting
                # ##############

                if device_ieeeAddr == "":
                    error_message_change_settings.append(sensordata_job.name + " >>> Keinen Sensor angegeben") 

                else:
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


                # input setting
                always_active = request.form.get("radio_input_setting_" + str(i))

                # save settings
                if error_founded == False: 

                    if SET_SENSORDATA_JOB_SETTINGS(i, name, filename, device_ieeeAddr, sensor_key, always_active):
                        success_message_change_settings.append(name + " || Einstellungen gespeichert") 


    list_sensordata_jobs  = GET_ALL_SENSORDATA_JOBS()
    dropdown_list_devices = GET_ALL_DEVICES("sensors") 
    list_sensordata_files = GET_SENSORDATA_FILES()
    list_sensors          = GET_ALL_DEVICES("sensors") 

    data = {'navigation': 'sensordata'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # get sensor list
    try:
        device_1_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(1).input_values
        device_1_input_values = device_1_input_values.replace(" ", "")
    except:
        device_1_input_values = ""
    try:
        device_2_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(2).input_values
        device_2_input_values = device_2_input_values.replace(" ", "")
    except:
        device_2_input_values = ""
    try:        
        device_3_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(3).input_values
        device_3_input_values = device_3_input_values.replace(" ", "")
    except:
        device_3_input_values = ""
    try:        
        device_4_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(4).input_values
        device_4_input_values = device_4_input_values.replace(" ", "")
    except:
        device_4_input_values = ""
    try:        
        device_5_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(5).input_values
        device_5_input_values = device_5_input_values.replace(" ", "")
    except:
        device_5_input_values = ""
    try:        
        device_6_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(6).input_values
        device_6_input_values = device_6_input_values.replace(" ", "")
    except:
        device_6_input_values = ""
    try:        
        device_7_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(7).input_values
        device_7_input_values = device_7_input_values.replace(" ", "")
    except:
        device_7_input_values = ""
    try:        
        device_8_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(8).input_values
        device_8_input_values = device_8_input_values.replace(" ", "")
    except:
        device_8_input_values = ""
    try:        
        device_9_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(9).input_values
        device_9_input_values = device_9_input_values.replace(" ", "")
    except:
        device_9_input_values = ""
    try:        
        device_10_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(10).input_values
        device_10_input_values = device_10_input_values.replace(" ", "")
    except:
        device_10_input_values = ""
    try:        
        device_11_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(11).input_values
        device_11_input_values = device_11_input_values.replace(" ", "")
    except:
        device_11_input_values = ""
    try:        
        device_12_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(12).input_values
        device_12_input_values = device_12_input_values.replace(" ", "")
    except:
        device_12_input_values = ""
    try:        
        device_13_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(13).input_values
        device_13_input_values = device_13_input_values.replace(" ", "")
    except:
        device_13_input_values = ""
    try:        
        device_14_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(14).input_values
        device_14_input_values = device_14_input_values.replace(" ", "")
    except:
        device_14_input_values = ""
    try:        
        device_15_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(15).input_values
        device_15_input_values = device_15_input_values.replace(" ", "")
    except:
        device_15_input_values = ""    
    try:        
        device_16_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(16).input_values
        device_16_input_values = device_16_input_values.replace(" ", "")
    except:
        device_16_input_values = ""
    try:        
        device_17_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(17).input_values
        device_17_input_values = device_17_input_values.replace(" ", "")
    except:
        device_17_input_values = ""
    try:        
        device_18_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(18).input_values
        device_18_input_values = device_18_input_values.replace(" ", "")
    except:
        device_18_input_values = ""
    try:        
        device_19_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(19).input_values
        device_19_input_values = device_19_input_values.replace(" ", "")
    except:
        device_19_input_values = ""
    try:        
        device_20_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(20).input_values
        device_20_input_values = device_20_input_values.replace(" ", "")
    except:
        device_20_input_values = ""   
    try:        
        device_21_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(21).input_values
        device_21_input_values = device_21_input_values.replace(" ", "")
    except:
        device_21_input_values = ""   
    try:        
        device_22_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(22).input_values
        device_22_input_values = device_22_input_values.replace(" ", "")
    except:
        device_22_input_values = ""   
    try:        
        device_23_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(23).input_values
        device_23_input_values = device_23_input_values.replace(" ", "")
    except:
        device_23_input_values = ""   
    try:        
        device_24_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(24).input_values
        device_24_input_values = device_24_input_values.replace(" ", "")
    except:
        device_24_input_values = ""   
    try:        
        device_25_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(25).input_values
        device_25_input_values = device_25_input_values.replace(" ", "")
    except:
        device_25_input_values = ""


    return render_template('layouts/default.html',
                            data=data,  
                            title=page_title,        
                            description=page_description,                                 
                            content=render_template( 'pages/sensordata_jobs.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_job=success_message_add_job,                            
                                                    error_message_add_job=error_message_add_job, 
                                                    error_message_datafile=error_message_datafile,    
                                                    list_sensordata_jobs=list_sensordata_jobs,  
                                                    dropdown_list_devices=dropdown_list_devices,
                                                    list_sensordata_files=list_sensordata_files,
                                                    list_sensors=list_sensors,
                                                    device_1_input_values=device_1_input_values,
                                                    device_2_input_values=device_2_input_values,
                                                    device_3_input_values=device_3_input_values,
                                                    device_4_input_values=device_4_input_values,
                                                    device_5_input_values=device_5_input_values,
                                                    device_6_input_values=device_6_input_values,
                                                    device_7_input_values=device_7_input_values,
                                                    device_8_input_values=device_8_input_values,
                                                    device_9_input_values=device_9_input_values,
                                                    device_10_input_values=device_10_input_values,
                                                    device_11_input_values=device_11_input_values,
                                                    device_12_input_values=device_12_input_values,
                                                    device_13_input_values=device_13_input_values,
                                                    device_14_input_values=device_14_input_values,
                                                    device_15_input_values=device_15_input_values,
                                                    device_16_input_values=device_16_input_values,
                                                    device_17_input_values=device_17_input_values,
                                                    device_18_input_values=device_18_input_values,
                                                    device_19_input_values=device_19_input_values,
                                                    device_20_input_values=device_20_input_values,  
                                                    device_21_input_values=device_21_input_values,
                                                    device_22_input_values=device_22_input_values,  
                                                    device_23_input_values=device_23_input_values,
                                                    device_24_input_values=device_24_input_values,
                                                    device_25_input_values=device_25_input_values,        
                                                    timestamp=timestamp,                                                         
                                                    ) 
                           )


# change jobs position 
@app.route('/sensordata/jobs/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_sensordata_jobs_position(id, direction):
    CHANGE_SENSORDATA_JOBS_POSITION(id, direction)
    return redirect(url_for('sensordata_jobs'))


# delete job
@app.route('/sensordata/jobs/delete/<int:id>')
@login_required
@permission_required
def delete_sensordata_jobs(id):
    job    = GET_SENSORDATA_JOB_BY_ID(id).name  
    result = DELETE_SENSORDATA_JOB(id)

    if result == True:
        session['delete_job_success'] = job + " || Erfolgreich gelöscht"
    else:
        session['delete_job_error'] = job + " || " + str(result)

    return redirect(url_for('sensordata_jobs'))


# download sensordata file
@app.route('/sensordata/download/file/<path:filepath>')
@login_required
@permission_required
def download_sensordata_file(filepath):
    try:
        path = GET_PATH() + "/data/csv/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "System | File | /data/csv/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filepath + " | " + str(e)) 
        session['error_download_datafile'] = "Download Datafile || " + str(e)


# delete sensordata file
@app.route('/sensordata/delete/<string:filename>')
@login_required
@permission_required
def delete_sensordata_file(filename):
    DELETE_SENSORDATA_FILE(filename)
    return redirect(url_for('sensordata_jobs'))