from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import GET_PATH, GET_ALL_SENSORDATA_FILES, WRITE_LOGFILE_SYSTEM
from app.backend.checks           import CHECK_SENSORDATA_JOBS
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
    page_title       = 'homatiX | Sensordata | Jobs'
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
                    error_message_change_settings.append(sensordata_job.name + " || Name - " + input_name + " - already taken")  
                    error_founded = True
                    name = sensordata_job.name

                # no input commited
                else:                          
                    name = GET_SENSORDATA_JOB_BY_ID(i).name
                    error_message_change_settings.append(sensordata_job.name + " || No name given") 
                    error_founded = True  


                # ################
                # filename setting
                # ################

                if request.form.get("set_filename_" + str(i)) != "":
                    filename = request.form.get("set_filename_" + str(i)).strip()   
                else:
                    filename = GET_SENSORDATA_JOB_BY_ID(i).filename 


                # ##############
                # device setting
                # ##############

                device = request.form.get("set_device_" + str(i)) 

                if GET_DEVICE_BY_IEEEADDR(device):
                    device_ieeeAddr = GET_DEVICE_BY_IEEEADDR(device).ieeeAddr
                elif GET_DEVICE_BY_ID(device):
                    device_ieeeAddr = GET_DEVICE_BY_ID(device).ieeeAddr
                else:
                    device_ieeeAddr = ""
                    sensor_key      = ""
  

                # ##############
                # sensor setting
                # ##############

                if device_ieeeAddr == "":
                    sensor_key = GET_SENSORDATA_JOB_BY_ID(i).sensor_key 

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
                always_active = request.form.get("set_radio_input_setting_" + str(i))

                # save settings
                if error_founded == False: 

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
        session['delete_job_success'] = job + " || Job successfully deleted"
    else:
        session['delete_job_error'] = job + " || " + str(result)

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
        WRITE_LOGFILE_SYSTEM("ERROR", "System | File | /data/csv/" + filename + " | " + str(e)) 
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