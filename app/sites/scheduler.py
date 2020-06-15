from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                           import app
from app.backend.database_models   import *
from app.backend.checks            import CHECK_TASKS, CHECK_SCHEDULER_JOB_SETTINGS
from app.backend.process_scheduler import GET_SUNRISE_TIME, GET_SUNSET_TIME
from app.backend.spotify           import GET_SPOTIFY_TOKEN
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
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/scheduler', methods=['GET', 'POST'])
@login_required
@permission_required
def scheduler():
    page_title       = 'Bianca | Scheduler'
    page_description = 'The scheduler configuration page.'

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
                if request.form.get("set_checkbox_trigger_time_" + str(i)):
                    trigger_time = "True"
                else:
                    trigger_time = "False"  

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


                # #############
                # time settings
                # #############

                # set day
                if request.form.get("set_day_" + str(i)) != "" and request.form.get("set_day_" + str(i)) != None:
                    day = request.form.get("set_day_" + str(i)).strip()
                else:
                    day = GET_SCHEDULER_JOB_BY_ID(i).day

                # set hour
                if request.form.get("set_hour_" + str(i)) != "" and request.form.get("set_hour_" + str(i)) != None:
                    hour = request.form.get("set_hour_" + str(i)).strip()
                else:
                    hour = GET_SCHEDULER_JOB_BY_ID(i).hour

                # set minute
                if request.form.get("set_minute_" + str(i)) != "" and request.form.get("set_minute_" + str(i)) != None:
                    minute = request.form.get("set_minute_" + str(i)).strip()
                else:
                    minute = GET_SCHEDULER_JOB_BY_ID(i).minute 


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
                                         trigger_time, trigger_sun_position, trigger_sensors, trigger_position, option_repeat, option_pause,
                                         day, hour, minute,
                                         option_sunrise, option_sunset, latitude, longitude,
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

            if result:
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
    try:        
        device_26_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(26).input_values
        device_26_input_values = device_26_input_values.strip()
    except:
        device_26_input_values = ""
    try:        
        device_27_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(27).input_values
        device_27_input_values = device_27_input_values.strip()
    except:
        device_27_input_values = ""
    try:        
        device_28_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(28).input_values
        device_28_input_values = device_28_input_values.strip()
    except:
        device_28_input_values = ""
    try:        
        device_29_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(29).input_values
        device_29_input_values = device_29_input_values.strip()
    except:
        device_29_input_values = ""
    try:        
        device_30_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(30).input_values
        device_30_input_values = device_30_input_values.strip()
    except:
        device_30_input_values = ""
    try:        
        device_31_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(31).input_values
        device_31_input_values = device_31_input_values.strip()
    except:
        device_31_input_values = ""
    try:        
        device_32_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(32).input_values
        device_32_input_values = device_32_input_values.strip()
    except:
        device_32_input_values = ""
    try:        
        device_33_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(33).input_values
        device_33_input_values = device_33_input_values.strip()
    except:
        device_33_input_values = ""
    try:        
        device_34_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(34).input_values
        device_34_input_values = device_34_input_values.strip()
    except:
        device_34_input_values = ""
    try:        
        device_35_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(35).input_values
        device_35_input_values = device_35_input_values.strip()
    except:
        device_35_input_values = ""
    try:        
        device_36_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(36).input_values
        device_36_input_values = device_36_input_values.strip()
    except:
        device_36_input_values = ""
    try:        
        device_37_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(37).input_values
        device_37_input_values = device_37_input_values.strip()
    except:
        device_37_input_values = ""
    try:        
        device_38_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(38).input_values
        device_38_input_values = device_38_input_values.strip()
    except:
        device_38_input_values = ""
    try:        
        device_39_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(39).input_values
        device_39_input_values = device_39_input_values.strip()
    except:
        device_39_input_values = ""
    try:        
        device_40_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(40).input_values
        device_40_input_values = device_40_input_values.strip()
    except:
        device_40_input_values = ""
    try:        
        device_41_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(41).input_values
        device_41_input_values = device_41_input_values.strip()
    except:
        device_41_input_values = ""
    try:        
        device_42_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(42).input_values
        device_42_input_values = device_42_input_values.strip()
    except:
        device_42_input_values = ""
    try:        
        device_43_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(43).input_values
        device_43_input_values = device_43_input_values.strip()
    except:
        device_43_input_values = ""
    try:        
        device_44_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(44).input_values
        device_44_input_values = device_44_input_values.strip()
    except:
        device_44_input_values = ""
    try:        
        device_45_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(45).input_values
        device_45_input_values = device_45_input_values.strip()
    except:
        device_45_input_values = ""
    try:        
        device_46_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(46).input_values
        device_46_input_values = device_46_input_values.strip()
    except:
        device_46_input_values = ""
    try:        
        device_47_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(47).input_values
        device_47_input_values = device_47_input_values.strip()
    except:
        device_47_input_values = ""
    try:        
        device_48_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(48).input_values
        device_48_input_values = device_48_input_values.strip()
    except:
        device_48_input_values = ""
    try:        
        device_49_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(49).input_values
        device_49_input_values = device_49_input_values.strip()
    except:
        device_49_input_values = ""
    try:        
        device_50_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(50).input_values
        device_50_input_values = device_50_input_values.strip()
    except:
        device_50_input_values = ""
    try:        
        device_51_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(51).input_values
        device_51_input_values = device_51_input_values.strip()
    except:
        device_51_input_values = ""
    try:        
        device_52_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(52).input_values
        device_52_input_values = device_52_input_values.strip()
    except:
        device_52_input_values = ""
    try:        
        device_53_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(53).input_values
        device_53_input_values = device_53_input_values.strip()
    except:
        device_53_input_values = ""
    try:        
        device_54_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(54).input_values
        device_54_input_values = device_54_input_values.strip()
    except:
        device_54_input_values = ""
    try:        
        device_55_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(55).input_values
        device_55_input_values = device_55_input_values.strip()
    except:
        device_55_input_values = ""
    try:        
        device_56_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(56).input_values
        device_56_input_values = device_56_input_values.strip()
    except:
        device_56_input_values = ""
    try:        
        device_57_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(57).input_values
        device_57_input_values = device_57_input_values.strip()
    except:
        device_57_input_values = ""
    try:        
        device_58_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(58).input_values
        device_58_input_values = device_58_input_values.strip()
    except:
        device_58_input_values = ""
    try:        
        device_59_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(59).input_values
        device_59_input_values = device_59_input_values.strip()
    except:
        device_59_input_values = ""
    try:        
        device_60_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(60).input_values
        device_60_input_values = device_60_input_values.strip()
    except:
        device_60_input_values = ""
    try:        
        device_61_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(61).input_values
        device_61_input_values = device_61_input_values.strip()
    except:
        device_61_input_values = ""
    try:        
        device_62_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(62).input_values
        device_62_input_values = device_62_input_values.strip()
    except:
        device_62_input_values = ""
    try:        
        device_63_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(63).input_values
        device_63_input_values = device_63_input_values.strip()
    except:
        device_63_input_values = ""
    try:        
        device_64_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(64).input_values
        device_64_input_values = device_64_input_values.strip()
    except:
        device_64_input_values = ""
    try:        
        device_65_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(65).input_values
        device_65_input_values = device_65_input_values.strip()
    except:
        device_65_input_values = ""
    try:        
        device_66_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(66).input_values
        device_66_input_values = device_66_input_values.strip()
    except:
        device_66_input_values = ""
    try:        
        device_67_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(67).input_values
        device_67_input_values = device_67_input_values.strip()
    except:
        device_67_input_values = ""
    try:        
        device_68_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(68).input_values
        device_68_input_values = device_68_input_values.strip()
    except:
        device_68_input_values = ""
    try:        
        device_69_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(69).input_values
        device_69_input_values = device_69_input_values.strip()
    except:
        device_69_input_values = ""
    try:        
        device_70_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(70).input_values
        device_70_input_values = device_70_input_values.strip()
    except:
        device_70_input_values = ""
    try:        
        device_71_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(71).input_values
        device_71_input_values = device_71_input_values.strip()
    except:
        device_71_input_values = ""
    try:        
        device_72_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(72).input_values
        device_72_input_values = device_72_input_values.strip()
    except:
        device_72_input_values = ""
    try:        
        device_73_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(73).input_values
        device_73_input_values = device_73_input_values.strip()
    except:
        device_73_input_values = ""
    try:        
        device_74_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(74).input_values
        device_74_input_values = device_74_input_values.strip()
    except:
        device_74_input_values = ""
    try:        
        device_75_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(75).input_values
        device_75_input_values = device_75_input_values.strip()
    except:
        device_75_input_values = ""
    try:        
        device_76_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(76).input_values
        device_76_input_values = device_76_input_values.strip()
    except:
        device_76_input_values = ""
    try:        
        device_77_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(77).input_values
        device_77_input_values = device_77_input_values.strip()
    except:
        device_77_input_values = ""
    try:        
        device_78_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(78).input_values
        device_78_input_values = device_78_input_values.strip()
    except:
        device_78_input_values = ""
    try:        
        device_79_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(79).input_values
        device_79_input_values = device_79_input_values.strip()
    except:
        device_79_input_values = ""
    try:        
        device_80_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(80).input_values
        device_80_input_values = device_80_input_values.strip()
    except:
        device_80_input_values = ""
    try:        
        device_81_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(81).input_values
        device_81_input_values = device_81_input_values.strip()
    except:
        device_81_input_values = ""
    try:        
        device_82_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(82).input_values
        device_82_input_values = device_82_input_values.strip()
    except:
        device_82_input_values = ""
    try:        
        device_83_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(83).input_values
        device_83_input_values = device_83_input_values.strip()
    except:
        device_83_input_values = ""
    try:        
        device_84_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(84).input_values
        device_84_input_values = device_84_input_values.strip()
    except:
        device_84_input_values = ""
    try:        
        device_85_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(85).input_values
        device_85_input_values = device_85_input_values.strip()
    except:
        device_85_input_values = ""
    try:        
        device_86_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(86).input_values
        device_86_input_values = device_86_input_values.strip()
    except:
        device_86_input_values = ""
    try:        
        device_87_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(87).input_values
        device_87_input_values = device_87_input_values.strip()
    except:
        device_87_input_values = ""
    try:        
        device_88_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(88).input_values
        device_88_input_values = device_88_input_values.strip()
    except:
        device_88_input_values = ""
    try:        
        device_89_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(89).input_values
        device_89_input_values = device_89_input_values.strip()
    except:
        device_89_input_values = ""
    try:        
        device_90_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(90).input_values
        device_90_input_values = device_90_input_values.strip()
    except:
        device_90_input_values = ""
    try:        
        device_91_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(91).input_values
        device_91_input_values = device_91_input_values.strip()
    except:
        device_91_input_values = ""
    try:        
        device_92_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(92).input_values
        device_92_input_values = device_92_input_values.strip()
    except:
        device_92_input_values = ""
    try:        
        device_93_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(93).input_values
        device_93_input_values = device_93_input_values.strip()
    except:
        device_93_input_values = ""
    try:        
        device_94_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(94).input_values
        device_94_input_values = device_94_input_values.strip()
    except:
        device_94_input_values = ""
    try:        
        device_95_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(95).input_values
        device_95_input_values = device_95_input_values.strip()
    except:
        device_95_input_values = ""
    try:        
        device_96_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(96).input_values
        device_96_input_values = device_96_input_values.strip()
    except:
        device_96_input_values = ""
    try:        
        device_97_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(97).input_values
        device_97_input_values = device_97_input_values.strip()
    except:
        device_97_input_values = ""
    try:        
        device_98_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(98).input_values
        device_98_input_values = device_98_input_values.strip()
    except:
        device_98_input_values = ""
    try:        
        device_99_input_values = "Sensor,------------------," + GET_DEVICE_BY_ID(99).input_values
        device_99_input_values = device_99_input_values.strip()
    except:
        device_99_input_values = ""        

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
                                                    device_26_input_values=device_26_input_values,  
                                                    device_27_input_values=device_27_input_values,  
                                                    device_28_input_values=device_28_input_values,  
                                                    device_29_input_values=device_29_input_values,  
                                                    device_30_input_values=device_30_input_values,     
                                                    device_31_input_values=device_31_input_values,  
                                                    device_32_input_values=device_32_input_values,  
                                                    device_33_input_values=device_33_input_values,  
                                                    device_34_input_values=device_34_input_values,  
                                                    device_35_input_values=device_35_input_values,     
                                                    device_36_input_values=device_36_input_values,  
                                                    device_37_input_values=device_37_input_values,  
                                                    device_38_input_values=device_38_input_values,  
                                                    device_39_input_values=device_39_input_values,          
                                                    device_40_input_values=device_40_input_values,     
                                                    device_41_input_values=device_41_input_values,  
                                                    device_42_input_values=device_42_input_values,  
                                                    device_43_input_values=device_43_input_values,  
                                                    device_44_input_values=device_44_input_values,  
                                                    device_45_input_values=device_45_input_values,     
                                                    device_46_input_values=device_46_input_values,  
                                                    device_47_input_values=device_47_input_values,  
                                                    device_48_input_values=device_48_input_values,  
                                                    device_49_input_values=device_49_input_values,     
                                                    device_50_input_values=device_50_input_values,     
                                                    device_51_input_values=device_51_input_values,  
                                                    device_52_input_values=device_52_input_values,  
                                                    device_53_input_values=device_53_input_values,  
                                                    device_54_input_values=device_54_input_values,  
                                                    device_55_input_values=device_55_input_values,     
                                                    device_56_input_values=device_56_input_values,  
                                                    device_57_input_values=device_57_input_values,  
                                                    device_58_input_values=device_58_input_values,  
                                                    device_59_input_values=device_59_input_values,     
                                                    device_60_input_values=device_60_input_values,     
                                                    device_61_input_values=device_61_input_values,  
                                                    device_62_input_values=device_62_input_values,  
                                                    device_63_input_values=device_63_input_values,  
                                                    device_64_input_values=device_64_input_values,  
                                                    device_65_input_values=device_65_input_values,     
                                                    device_66_input_values=device_66_input_values,  
                                                    device_67_input_values=device_67_input_values,  
                                                    device_68_input_values=device_68_input_values,  
                                                    device_69_input_values=device_69_input_values,     
                                                    device_70_input_values=device_70_input_values,     
                                                    device_71_input_values=device_71_input_values,  
                                                    device_72_input_values=device_72_input_values,  
                                                    device_73_input_values=device_73_input_values,  
                                                    device_74_input_values=device_74_input_values,  
                                                    device_75_input_values=device_75_input_values,     
                                                    device_76_input_values=device_76_input_values,  
                                                    device_77_input_values=device_77_input_values,  
                                                    device_78_input_values=device_78_input_values,  
                                                    device_79_input_values=device_79_input_values,     
                                                    device_80_input_values=device_80_input_values,     
                                                    device_81_input_values=device_81_input_values,  
                                                    device_82_input_values=device_82_input_values,  
                                                    device_83_input_values=device_83_input_values,  
                                                    device_84_input_values=device_84_input_values,  
                                                    device_85_input_values=device_85_input_values,     
                                                    device_86_input_values=device_86_input_values,  
                                                    device_87_input_values=device_87_input_values,  
                                                    device_88_input_values=device_88_input_values,  
                                                    device_89_input_values=device_89_input_values,     
                                                    device_90_input_values=device_90_input_values,     
                                                    device_91_input_values=device_91_input_values,  
                                                    device_92_input_values=device_92_input_values,  
                                                    device_93_input_values=device_93_input_values,  
                                                    device_94_input_values=device_94_input_values,  
                                                    device_95_input_values=device_95_input_values,     
                                                    device_96_input_values=device_96_input_values,  
                                                    device_97_input_values=device_97_input_values,  
                                                    device_98_input_values=device_98_input_values,  
                                                    device_99_input_values=device_99_input_values,                                                                                                            
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