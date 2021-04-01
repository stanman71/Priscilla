from flask                         import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login                   import current_user, login_required
from werkzeug.exceptions           import HTTPException, NotFound, abort
from functools                     import wraps

from app                           import app
from app.backend.database_models   import *
from app.backend.checks            import CHECK_TASKS, CHECK_SCHEDULER_JOB_SETTINGS
from app.backend.process_scheduler import GET_SUNRISE_TIME, GET_SUNSET_TIME
from app.backend.spotify           import GET_SPOTIFY_TOKEN
from app.backend.file_management   import WRITE_LOGFILE_SYSTEM
from app.backend.user_id           import SET_CURRENT_USER_ID
from app.common                    import COMMON, STATUS
from app.assets                    import *

import spotipy


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


@app.route('/scheduler', methods=['GET', 'POST'])
@login_required
@permission_required
def scheduler():
    page_title       = 'Bianca | Scheduler'
    page_description = 'The scheduler configuration page'

    SET_CURRENT_USER_ID(current_user.id)  

    success_message_change_settings               = []
    error_message_change_settings                 = []       
    success_message_add_scheduler_job             = []
    error_message_add_scheduler_job               = []
    success_message_change_settings_scheduler_job = "" 

    RESET_SCHEDULER_JOB_COLLAPSE()
    UPDATE_SCHEDULER_JOBS_DEVICE_NAMES()


    """ ################### """
    """  add scheduler job  """
    """ ################### """   

    if request.form.get("add_scheduler_job") != None: 
        result = ADD_SCHEDULER_JOB()   
        if result != True: 
            error_message_add_scheduler_job.append(result)         
        else:       
            success_message_add_scheduler_job = True


    """ ###################### """
    """  table scheduler jobs  """
    """ ###################### """   

    # set collapse open 
    if session.get("set_collapse_open", None) != None:
        SET_SCHEDULER_JOB_COLLAPSE_OPEN(session.get('set_collapse_open'))
        session['set_collapse_open'] = None

    if request.form.get("save_scheduler_settings") != None: 

        for i in range (1,31):
            
            if request.form.get("set_name_" + str(i)) != None:
                
                SET_SCHEDULER_JOB_COLLAPSE_OPEN(i)    

                error_found = False          

                # ############
                # name setting
                # ############

                scheduler_job = GET_SCHEDULER_JOB_BY_ID(i)
                input_name    = request.form.get("set_name_" + str(i)).strip()                    

                # add new name
                if ((input_name != "") and (GET_SCHEDULER_JOB_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == scheduler_job.name:
                    name = scheduler_job.name                        
                    
                # name already exist
                elif ((GET_SCHEDULER_JOB_BY_NAME(input_name) != None) and (scheduler_job.name != input_name)):
                    error_message_change_settings.append(scheduler_job.name + " || Name - " + input_name + " - already taken")  
                    error_found = True
                    name = scheduler_job.name

                # no input commited
                else:                          
                    name = GET_SCHEDULER_JOB_BY_ID(i).name
                    error_message_change_settings.append(scheduler_job.name + " || No name given") 
                    error_found = True  


                # ############
                # task setting
                # ############

                if request.form.get("set_task_" + str(i)) != "":                   
                    task = request.form.get("set_task_" + str(i)).strip()
                else:
                    task = GET_SCHEDULER_JOB_BY_ID(i).task


                # #################
                # checkbox settings
                # #################

                # set checkbox time
                if request.form.get("set_checkbox_trigger_timedate_" + str(i)):
                    trigger_timedate = "True"
                else:
                    trigger_timedate = "False"  

                # set checkbox sun
                if request.form.get("set_checkbox_trigger_sun_position_" + str(i)):
                    trigger_sun_position = "True"
                else:
                    trigger_sun_position = "False" 

                # set checkbox sensors
                if request.form.get("set_checkbox_trigger_sensors_" + str(i)):
                    trigger_sensors = "True"
                else:
                    trigger_sensors = "False"  

                # set checkbox position
                if request.form.get("set_checkbox_trigger_position_" + str(i)):
                    trigger_position = "True"
                else:
                    trigger_position = "False"  
                                       
                # set checkbox repeat
                if request.form.get("set_checkbox_option_repeat_" + str(i)):
                    option_repeat = "True"
                else:
                    option_repeat = "False"  

                # set checkbox pause
                if request.form.get("set_checkbox_option_pause_" + str(i)):
                    option_pause = "True"
                else:
                    option_pause = "False"  


                # #################
                # timedate settings
                # #################

                # set timedate
                if request.form.get("set_timedate_" + str(i)) != "" and request.form.get("set_timedate_" + str(i)) != None:
                    timedate = request.form.get("set_timedate_" + str(i)).strip()
                else:
                    timedate = GET_SCHEDULER_JOB_BY_ID(i).timedate


                # ############
                # sun settings
                # ############

                # set option sunrise
                if request.form.get("set_checkbox_option_sunrise_" + str(i)):
                    option_sunrise = "True"
                else:
                    option_sunrise = "False"  

                # set option sunset
                if request.form.get("set_checkbox_option_sunset_" + str(i)):
                    option_sunset = "True"
                else:              
                    option_sunset = "False"  

                # set option day
                if request.form.get("set_checkbox_option_day_" + str(i)):
                    option_day = "True"
                else:              
                    option_day = "False"  

                # set option night
                if request.form.get("set_checkbox_option_night_" + str(i)):
                    option_night = "True"
                else:              
                    option_night = "False"  

                # set coordinates
                latitude  = request.form.get("set_latitude_" + str(i))

                if latitude == "" or latitude == None:           
                    latitude = "None"  

                longitude = request.form.get("set_longitude_" + str(i))
                
                if longitude == "" or longitude == None:           
                    longitude = "None"  

                try:                
                    # update sunrise / sunset  
                    if latitude != "None" and longitude != "None":  
                        latitude  = latitude.replace(",",".")
                        longitude = longitude.replace(",",".")

                        # valid values ?
                        if -90.0 <= float(latitude) <= 90.0 and -180.0 <= float(longitude) <= 180.0:       
                            SET_SCHEDULER_JOB_SUNRISE(i, GET_SUNRISE_TIME(float(latitude), float(longitude)))
                            SET_SCHEDULER_JOB_SUNSET(i, GET_SUNSET_TIME(float(latitude), float(longitude)))

                        else:
                            SET_SCHEDULER_JOB_SUNRISE(i, "None")
                            SET_SCHEDULER_JOB_SUNSET(i, "None")                            

                    else:
                        SET_SCHEDULER_JOB_SUNRISE(i, "None")
                        SET_SCHEDULER_JOB_SUNSET(i, "None")       

                except:
                    SET_SCHEDULER_JOB_SUNRISE(i, "None")
                    SET_SCHEDULER_JOB_SUNSET(i, "None")                   


                # ###############
                # sensor settings
                # ###############              

                # set device 1
                device_1 = request.form.get("set_device_1_" + str(i))

                if GET_DEVICE_BY_IEEEADDR(device_1):
                    device_ieeeAddr_1 = device_1
                elif GET_DEVICE_BY_ID(device_1):
                    device_ieeeAddr_1 = GET_DEVICE_BY_ID(device_1).ieeeAddr
                else:
                    device_ieeeAddr_1 = "None"
                                        
                # set device 2
                device_2 = request.form.get("set_device_2_" + str(i))

                if GET_DEVICE_BY_IEEEADDR(device_2):
                    device_ieeeAddr_2 = device_2
                elif GET_DEVICE_BY_ID(device_2):
                    device_ieeeAddr_2 = GET_DEVICE_BY_ID(device_2).ieeeAddr
                else:
                    device_ieeeAddr_2 = "None"
                                                
                operator_1                  = request.form.get("set_operator_1_" + str(i))
                operator_2                  = request.form.get("set_operator_2_" + str(i))  
                main_operator_second_sensor = request.form.get("set_main_operator_second_sensor_" + str(i))

                if operator_1 == None:
                    operator_1 = "None"
                if operator_2 == None:
                    operator_2 = "None"         
                if main_operator_second_sensor == None:
                    main_operator_second_sensor = "None"

                try: 
                    value_1 = request.form.get("set_value_1_" + str(i)).strip()
                except:
                    value_1 = "None"

                try: 
                    value_2 = request.form.get("set_value_2_" + str(i)).strip()
                except:
                    value_2 = "None" 

                # get device 1
                try:
                    device_name_1         = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).name
                    device_input_values_1 = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).input_values

                    # get sensorkey value
                    sensor_key_1 = request.form.get("set_sensor_1_" + str(i))
                    sensor_key_1 = sensor_key_1.replace(" ", "") 
                    if sensor_key_1.isdigit():
                        if sensor_key_1 == "0" or sensor_key_1 == "1":
                            sensor_key_1 = "None"
                        else:                                
                            sensor_list  = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).input_values
                            sensor_list  = sensor_list.split(",")
                            sensor_key_1 = sensor_list[int(sensor_key_1)-2]
                        
                except:  
                    sensor_key_1          = "None"
                    device_ieeeAddr_1     = "None"
                    device_name_1         = "None"
                    device_input_values_1 = "None"  


                # get device 2
                try:
                    device_name_2         = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2).name
                    device_input_values_2 = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2).input_values

                    # get sensorkey value
                    sensor_key_2 = request.form.get("set_sensor_2_" + str(i))
                    sensor_key_2 = sensor_key_2.replace(" ", "") 
                    if sensor_key_2.isdigit():
                        if sensor_key_2 == "0" or sensor_key_2 == "1":
                            sensor_key_2 = "None"
                        else:                                
                            sensor_list  = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2).input_values
                            sensor_list  = sensor_list.split(",")
                            sensor_key_2 = sensor_list[int(sensor_key_2)-2]
                        
                except:
                    sensor_key_2          = "None"
                    device_ieeeAddr_2     = "None"
                    device_name_2         = "None"
                    device_input_values_2 = "None"   


                # #################
                # position settings
                # #################   

                # set option home
                if request.form.get("set_checkbox_option_home_" + str(i)):
                    option_home = "True"
                else:
                    option_home = "False"  

                # set option away
                if request.form.get("set_checkbox_option_away_" + str(i)):
                    option_away = "True"
                else:
                    option_away = "False"  

                # set ip_addresses
                if request.form.get("set_ip_addresses_" + str(i)) != "" and request.form.get("set_ip_addresses_" + str(i)) != None:
                    ip_addresses = request.form.get("set_ip_addresses_" + str(i)).strip()
                else:
                    ip_addresses = "None"


                if error_found == False: 

                    if SET_SCHEDULER_JOB(i, name, task, 
                                         trigger_timedate, trigger_sun_position, trigger_sensors, trigger_position, option_repeat, option_pause,
                                         timedate,
                                         option_sunrise, option_sunset, option_day, option_night, latitude, longitude,
                                         device_ieeeAddr_1, device_name_1, device_input_values_1, 
                                         sensor_key_1, operator_1, value_1, main_operator_second_sensor,
                                         device_ieeeAddr_2, device_name_2, device_input_values_2, 
                                         sensor_key_2, operator_2, value_2, 
                                         option_home, option_away, ip_addresses):

                        success_message_change_settings_scheduler_job = i


    """ ###################### """
    """  delete scheduler job  """
    """ ###################### """   

    for i in range (1,31):

        if request.form.get("delete_scheduler_job_" + str(i)) != None:
            scene  = GET_SCHEDULER_JOB_BY_ID(i).name  
            result = DELETE_SCHEDULER_JOB(i)            

            if result == True:
                success_message_change_settings.append(scene + " || Job successfully deleted") 
            else:
                error_message_change_settings.append(scene + " || " + str(result))


    """ ####################### """
    """  scheduler job options  """
    """ ####################### """   

    # list lighting group options    
    list_lighting_group_options = []

    for group in GET_ALL_LIGHTING_GROUPS():
        list_lighting_group_options.append(group.name)

    # list lighting scene options    
    list_lighting_scene_options = []

    for scene in GET_ALL_LIGHTING_SCENES():
        list_lighting_scene_options.append(scene.name)

    # list light options
    list_light_options = []

    for device in GET_ALL_DEVICES("light"):
        list_light_options.append(device.name)

    # list sensordata job options    
    list_sensordata_job_options = []

    for job in GET_ALL_SENSORDATA_JOBS():
        if job.device.model == "sensor_active": 
            list_sensordata_job_options.append(job.name)

    # list program options    
    list_program_options = []

    for program in GET_ALL_PROGRAMS():
        list_program_options.append(program.name)

    # list device command options    
    list_device_command_options = []
    
    for device in GET_ALL_DEVICES("devices"):
        list_device_command_options.append((device.name, device.commands))
         
    # list spotify devices / playlists
    spotify_token = GET_SPOTIFY_TOKEN()    
    
    try:
        sp       = spotipy.Spotify(auth=spotify_token)
        sp.trace = False
        
        list_spotify_devices   = sp.devices()["devices"]        
        list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]   
        
    except:
        list_spotify_devices   = ""       
        list_spotify_playlists = ""      


    CHECK_SCHEDULER_JOB_SETTINGS(GET_ALL_SCHEDULER_JOBS())
    CHECK_TASKS(GET_ALL_SCHEDULER_JOBS(), "scheduler")

    list_scheduler_jobs = GET_ALL_SCHEDULER_JOBS()

    dropdown_list_devices                     = GET_ALL_DEVICES("sensors")
    dropdown_list_operators                   = ["=", ">", "<"]
    dropdown_list_main_operator_second_sensor = ["and", "or", "=", ">", "<"]

    data = {'navigation': 'scheduler'}    

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
                            content=render_template( 'pages/scheduler.html',
                                                    list_scheduler_jobs=list_scheduler_jobs,
                                                    dropdown_list_devices=dropdown_list_devices,
                                                    dropdown_list_operators=dropdown_list_operators,
                                                    dropdown_list_main_operator_second_sensor=dropdown_list_main_operator_second_sensor,
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,                         
                                                    success_message_add_scheduler_job=success_message_add_scheduler_job,
                                                    error_message_add_scheduler_job=error_message_add_scheduler_job,
                                                    success_message_change_settings_scheduler_job=success_message_change_settings_scheduler_job,
                                                    list_lighting_group_options=list_lighting_group_options,
                                                    list_lighting_scene_options=list_lighting_scene_options,
                                                    list_light_options=list_light_options,                                                    
                                                    list_sensordata_job_options=list_sensordata_job_options,   
                                                    list_program_options=list_program_options,                                                 
                                                    list_device_command_options=list_device_command_options,
                                                    list_spotify_devices=list_spotify_devices,     
                                                    list_spotify_playlists=list_spotify_playlists,     
                                                    device_input_values_list=device_input_values_list,                                                                                                                        
                                                    ) 
                           )


# change scheduler job position 
@app.route('/scheduler/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_scheduler_job_position(id, direction):
    CHANGE_SCHEDULER_JOB_POSITION(id, direction)
    return redirect(url_for('scheduler'))


# scheduler jobs option add sensor / remove sensor
@app.route('/scheduler/<string:option>/<int:id>')
@login_required
@permission_required
def change_scheduler_job_options(id, option):
    if option == "add_sensor":
        ADD_SCHEDULER_JOB_SECOND_SENSOR(id)
        session['set_collapse_open'] = id
        
    if option == "remove_sensor":
        REMOVE_SCHEDULER_JOB_SECOND_SENSOR(id)
        session['set_collapse_open'] = id

    return redirect(url_for('scheduler'))