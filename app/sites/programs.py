from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.process_program import * 
from app.backend.checks          import CHECK_PROGRAM_TASKS
from app.backend.spotify         import GET_SPOTIFY_TOKEN
from app.common                  import COMMON, STATUS
from app.assets                  import *


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


@app.route('/programs', methods=['GET', 'POST'])
@login_required
@permission_required
def programs():
    page_title       = 'Smarthome | Programs'
    page_description = 'The programs configuration page.'

    success_message_add_program             = False       
    error_message_add_program               = []
    success_message_change_settings         = []
    error_message_change_settings           = []
    success_message_change_settings_program = []
    error_message_change_settings_program   = []

    selected_program = ""

    # selected program
    if session.get('selected_program_id', None) != None:
        selected_program = GET_PROGRAM_BY_ID(int(session.get('selected_program_id'))) 
        session['selected_program_id'] = None


    """ ############# """
    """  add program  """
    """ ############# """   

    if request.form.get("add_program") != None: 
        result = ADD_PROGRAM()   
        if result != True: 
            error_message_add_program.append(result)         

        else:       
            success_message_add_program = True


    """ ################ """
    """  select program  """
    """ ################ """  

    if request.form.get("select_program") != None: 
        
        # get the selected program
        selected_program = request.form.get("select_program") 
        
        if selected_program != None:
            selected_program = GET_PROGRAM_BY_NAME(selected_program)   
            

    """ ################# """
    """  program settings """
    """ ################# """  

    if request.form.get("save_program_settings") != None: 
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                error_founded = False   

                # ############
                # name setting
                # ############

                selected_program = GET_PROGRAM_BY_ID(i)
                input_name       = request.form.get("set_name_" + str(i)).strip()                    

                # add new name
                if ((input_name != "") and (GET_PROGRAM_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == selected_program.name:
                    name = selected_program.name                        
                    
                # name already exist
                elif ((GET_PROGRAM_BY_NAME(input_name) != None) and (selected_program.name != input_name)):
                    error_message_change_settings_program.append(selected_program.name + " || Name - " + input_name + " - already taken")  
                    name = selected_program.name
                    error_founded = True  

                # no input commited
                else:                          
                    name = GET_PROGRAM_BY_ID(i).name
                    error_message_change_settings_program.append(selected_program.name + " || No name given") 
                    error_founded = True  

                try:
                    line_content_1  = request.form.get("set_line_content_1_"  + str(i)).strip()
                except:
                    line_content_1 = "None"

                try:
                    line_content_2  = request.form.get("set_line_content_2_"  + str(i)).strip()
                except:
                    line_content_2 = "None"                

                try:                
                    line_content_3  = request.form.get("set_line_content_3_"  + str(i)).strip()       
                except:
                    line_content_3 = "None"   

                try:                                  
                    line_content_4  = request.form.get("set_line_content_4_"  + str(i)).strip()    
                except:
                    line_content_4 = "None"  

                try:                                  
                    line_content_5  = request.form.get("set_line_content_5_"  + str(i)).strip() 
                except:
                    line_content_5 = "None"   

                try:                                     
                    line_content_6  = request.form.get("set_line_content_6_"  + str(i)).strip()  
                except:
                    line_content_6 = "None"

                try:                    
                    line_content_7  = request.form.get("set_line_content_7_"  + str(i)).strip()  
                except:
                    line_content_7 = "None"

                try:                    
                    line_content_8  = request.form.get("set_line_content_8_"  + str(i)).strip()  
                except:
                    line_content_8 = "None"

                try:                    
                    line_content_9  = request.form.get("set_line_content_9_"  + str(i)).strip()  
                except:
                    line_content_9 = "None"

                try:                    
                    line_content_10 = request.form.get("set_line_content_10_" + str(i)).strip() 
                except:
                    line_content_10 = "None"

                try:                    
                    line_content_11 = request.form.get("set_line_content_11_" + str(i)).strip()  
                except:
                    line_content_11 = "None"

                try:                    
                    line_content_12 = request.form.get("set_line_content_12_" + str(i)).strip()  
                except:
                    line_content_12 = "None"

                try:                    
                    line_content_13 = request.form.get("set_line_content_13_" + str(i)).strip()  
                except:
                    line_content_13 = "None"

                try:                    
                    line_content_14 = request.form.get("set_line_content_14_" + str(i)).strip() 
                except:
                    line_content_14 = "None"

                try:                    
                    line_content_15 = request.form.get("set_line_content_15_" + str(i)).strip()  
                except:
                    line_content_15 = "None"

                try:                    
                    line_content_16 = request.form.get("set_line_content_16_" + str(i)).strip()  
                except:
                    line_content_16 = "None"

                try:                    
                    line_content_17 = request.form.get("set_line_content_17_" + str(i)).strip()  
                except:
                    line_content_17 = "None"

                try:                    
                    line_content_18 = request.form.get("set_line_content_18_" + str(i)).strip() 
                except:
                    line_content_18 = "None"

                try:                    
                    line_content_19 = request.form.get("set_line_content_19_" + str(i)).strip()  
                except:
                    line_content_19 = "None"

                try:                    
                    line_content_20 = request.form.get("set_line_content_20_" + str(i)).strip()     
                except:
                    line_content_20 = "None"

                try:                    
                    line_content_21 = request.form.get("set_line_content_21_" + str(i)).strip()     
                except:
                    line_content_21 = "None"

                try:                    
                    line_content_22 = request.form.get("set_line_content_22_" + str(i)).strip()     
                except:
                    line_content_22 = "None"

                try:                    
                    line_content_23 = request.form.get("set_line_content_23_" + str(i)).strip()     
                except:
                    line_content_23 = "None"

                try:                    
                    line_content_24 = request.form.get("set_line_content_24_" + str(i)).strip()     
                except:
                    line_content_24 = "None"

                try:                    
                    line_content_25 = request.form.get("set_line_content_25_" + str(i)).strip()     
                except:
                    line_content_25 = "None"

                try:                    
                    line_content_26 = request.form.get("set_line_content_26_" + str(i)).strip()     
                except:
                    line_content_26 = "None"

                try:                    
                    line_content_27 = request.form.get("set_line_content_27_" + str(i)).strip()     
                except:
                    line_content_27 = "None"

                try:                    
                    line_content_28 = request.form.get("set_line_content_28_" + str(i)).strip()     
                except:
                    line_content_28 = "None"

                try:                    
                    line_content_29 = request.form.get("set_line_content_29_" + str(i)).strip()     
                except:
                    line_content_29 = "None"

                try:                    
                    line_content_30 = request.form.get("set_line_content_30_" + str(i)).strip()     
                except:
                    line_content_30 = "None"


                if error_founded == False:           

                    if SET_PROGRAM_SETTINGS(i, name, line_content_1,line_content_2, line_content_3, line_content_4, line_content_5, 
                                                     line_content_6, line_content_7, line_content_8, line_content_9, line_content_10,
                                                     line_content_11, line_content_12, line_content_13, line_content_14, line_content_15, 
                                                     line_content_16, line_content_17, line_content_18, line_content_19, line_content_20,
                                                     line_content_21, line_content_22, line_content_23, line_content_24, line_content_25, 
                                                     line_content_26, line_content_27, line_content_28, line_content_29, line_content_30):

                        success_message_change_settings_program.append("Settings successfully saved")           


    """ ############### """
    """  start program  """
    """ ############### """   

    for i in range (1,31):
        if request.form.get("start_program_" + str(i)) != None:
            result           = START_PROGRAM_THREAD(i)
            selected_program = GET_PROGRAM_BY_ID(i)

            if result:
                success_message_change_settings_program.append("Program successfully started")
            else:
                success_message_change_settings_program.append("ERROR || " + str(result))


    """ ################ """
    """  delete program  """
    """ ################ """   

    for i in range (1,31):

        if request.form.get("delete_program_" + str(i)) != None:
            program = GET_PROGRAM_BY_ID(i).name  
            result  = DELETE_PROGRAM(i)    

            if result:
                success_message_change_settings.append(program + " || Program successfully deleted") 
            else:
                error_message_change_settings.append(program + " || " + str(result))


    """ ##################### """
    """  program task options """
    """ ##################### """   

    # list lighting group options    
    list_lighting_group_options = []

    for group in GET_ALL_LIGHTING_GROUPS():
        list_lighting_group_options.append(group.name)

    # list lighting scene options    
    list_lighting_scene_options = []

    for scene in GET_ALL_LIGHTING_SCENES():
        list_lighting_scene_options.append(scene.name)

    # list sensordata job options    
    list_sensordata_job_options = []

    for job in GET_ALL_SENSORDATA_JOBS():
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


    dropdown_list_programs = GET_ALL_PROGRAMS()

    if selected_program != "":
        error_message_program_tasks = CHECK_PROGRAM_TASKS(selected_program.id)        
    else:
        error_message_program_tasks = []

    data = {'navigation': 'programs'}    

    return render_template('layouts/default.html',
                            data=data, 
                            title=page_title,        
                            description=page_description,                                  
                            content=render_template( 'pages/programs.html',
                                                    success_message_add_program=success_message_add_program,
                                                    error_message_add_program=error_message_add_program,
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings_program=success_message_change_settings_program,
                                                    error_message_change_settings_program=error_message_change_settings_program,
                                                    error_message_program_tasks=error_message_program_tasks,
                                                    dropdown_list_programs=dropdown_list_programs,
                                                    selected_program=selected_program,
                                                    list_lighting_group_options=list_lighting_group_options,
                                                    list_lighting_scene_options=list_lighting_scene_options,
                                                    list_sensordata_job_options=list_sensordata_job_options,                                                    
                                                    list_device_command_options=list_device_command_options,
                                                    list_program_options=list_program_options,                                                     
                                                    list_spotify_devices=list_spotify_devices,     
                                                    list_spotify_playlists=list_spotify_playlists, 
                                                    ) 
                           )


# programs option add line / remove line
@app.route('/programs/<string:option>/<int:id>')
@login_required
@permission_required
def change_programs_options(id, option):
    if option == "add_line":
        ADD_PROGRAM_LINE(id)
        session['selected_program_id'] = id
        
    if option == "remove_line":
        REMOVE_PROGRAM_LINE(id)
        session['selected_program_id'] = id

    return redirect(url_for('programs'))


# change lines position 
@app.route('/programs/position/<string:direction>/<int:line>/<int:id>')
@login_required
@permission_required
def change_programs_line_position(id, line, direction):
    CHANGE_PROGRAMS_LINE_POSITION(id, line, direction)
    session['selected_program_id'] = id

    return redirect(url_for('programs'))