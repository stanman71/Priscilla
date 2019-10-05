from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.checks          import CHECK_TASKS
from app.common                  import COMMON, STATUS
from app.assets                  import *


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        #try:
        if current_user.role == "administrator":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout'))
        #except Exception as e:
        #    print(e)
        #    return redirect(url_for('logout'))
        
    return wrap


@app.route('/led/scenes', methods=['GET', 'POST'])
@login_required
@permission_required
def led_scenes():
    success_message_change_settings           = []
    error_message_change_settings             = []    
    success_message_change_settings_led_scene = ""
    error_message_change_settings_led_scene   = []    
    success_message_add_led_scene             = False
    error_message_add_led_scene               = []
    name = ""

    RESET_LED_SCENE_COLLAPSE()


    """ ################# """
    """  table led scenes """
    """ ################# """   


    # set collapse open for option change led number
    if session.get("set_collapse_open", None) != None:
        SET_LED_SCENE_COLLAPSE_OPEN(session.get('set_collapse_open'))
        session['set_collapse_open'] = None

    for i in range (1,11):

        # change scene
        if request.form.get("save_led_scene_settings") != None:

            if request.form.get("set_name_" + str(i)) != None:
                
                SET_LED_SCENE_COLLAPSE_OPEN(i)      

                # ############
                # name setting
                # ############

                led_scene_data = GET_LED_SCENE_BY_ID(i)
                new_name       = request.form.get("set_name_" + str(i))                    

                # add new name
                if ((new_name != "") and (GET_LED_SCENE_BY_NAME(new_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif new_name == led_scene_data.name:
                    name = led_scene_data.name                        
                    
                # name already exist
                elif ((GET_LED_SCENE_BY_NAME(new_name) != None) and (led_scene_data.name != new_name)):
                    name = led_scene_data.name 
                    error_message_change_settings_led_scene = {"scene_number": i,"message": "Name schon vergeben"}

                # no input commited
                else:                          
                    name = GET_LED_SCENE_BY_ID(i).name 
                    error_message_change_settings_led_scene = {"scene_number": i,"message": "Keinen Namen angegeben"}


                #######
                ## 1 ##
                #######

                # check rgb
                rgb_1 = request.form.get("set_rgb_1_" + str(i))

                try:
                    rgb_1   = re.findall(r'\d+', rgb_1)
                    red_1   = rgb_1[0]
                    green_1 = rgb_1[1]           
                    blue_1  = rgb_1[2]      
                except:
                    red_1   = 0
                    green_1 = 0
                    blue_1  = 0 
                                
                #######
                ## 2 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_2 == "True":

                    # check rgb
                    rgb_2 = request.form.get("set_rgb_2_" + str(i))

                    try:
                        rgb_2   = re.findall(r'\d+', rgb_2)
                        red_2   = rgb_2[0]
                        green_2 = rgb_2[1]           
                        blue_2  = rgb_2[2]      
                    except:
                        red_2   = 0
                        green_2 = 0
                        blue_2  = 0 

                else:
                    red_2 = 0
                    green_2 = 0
                    blue_2 = 0

                #######
                ## 3 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_3 == "True":

                    # check rgb
                    rgb_3 = request.form.get("set_rgb_3_" + str(i))

                    try:
                        rgb_3   = re.findall(r'\d+', rgb_3)
                        red_3   = rgb_3[0]
                        green_3 = rgb_3[1]           
                        blue_3  = rgb_3[2]      
                    except:
                        red_3   = 0
                        green_3 = 0
                        blue_3  = 0 

                else:
                    red_3 = 0
                    green_3 = 0
                    blue_3 = 0

                #######
                ## 4 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_4 == "True":

                    # check rgb
                    rgb_4 = request.form.get("set_rgb_4_" + str(i))

                    try:
                        rgb_4   = re.findall(r'\d+', rgb_4)
                        red_4   = rgb_4[0]
                        green_4 = rgb_4[1]           
                        blue_4  = rgb_4[2]      
                    except:
                        red_4   = 0
                        green_4 = 0
                        blue_4  = 0 

                else:
                    red_4 = 0
                    green_4 = 0
                    blue_4 = 0

                #######
                ## 5 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_5 == "True":

                    # check rgb
                    rgb_5 = request.form.get("set_rgb_5_" + str(i))

                    try:
                        rgb_5   = re.findall(r'\d+', rgb_5)
                        red_5   = rgb_5[0]
                        green_5 = rgb_5[1]           
                        blue_5  = rgb_5[2]      
                    except:
                        red_5   = 0
                        green_5 = 0
                        blue_5  = 0 

                else:
                    red_5 = 0
                    green_5 = 0
                    blue_5 = 0

                #######
                ## 6 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_6 == "True":

                    # check rgb
                    rgb_6 = request.form.get("set_rgb_6_" + str(i))

                    try:
                        rgb_6   = re.findall(r'\d+', rgb_6)
                        red_6   = rgb_6[0]
                        green_6 = rgb_6[1]           
                        blue_6  = rgb_6[2]      
                    except:
                        red_6   = 0
                        green_6 = 0
                        blue_6  = 0 

                else:
                    red_6 = 0
                    green_6 = 0
                    blue_6 = 0

                #######
                ## 7 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_7 == "True":

                    # check rgb
                    rgb_7 = request.form.get("set_rgb_7_" + str(i))

                    try:
                        rgb_7   = re.findall(r'\d+', rgb_7)
                        red_7   = rgb_7[0]
                        green_7 = rgb_7[1]           
                        blue_7  = rgb_7[2]      
                    except:
                        red_7   = 0
                        green_7 = 0
                        blue_7  = 0 

                else:
                    red_7 = 0
                    green_7 = 0
                    blue_7 = 0

                #######
                ## 8 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_8 == "True":

                    # check rgb
                    rgb_8 = request.form.get("set_rgb_8_" + str(i))

                    try:
                        rgb_8   = re.findall(r'\d+', rgb_8)
                        red_8   = rgb_8[0]
                        green_8 = rgb_8[1]           
                        blue_8  = rgb_8[2]      
                    except:
                        red_8   = 0
                        green_8 = 0
                        blue_8  = 0 

                else:
                    red_8 = 0
                    green_8 = 0
                    blue_8 = 0

                #######
                ## 9 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_9 == "True":

                    # check rgb
                    rgb_9 = request.form.get("set_rgb_9_" + str(i))

                    try:
                        rgb_9   = re.findall(r'\d+', rgb_9)
                        red_9   = rgb_9[0]
                        green_9 = rgb_9[1]           
                        blue_9  = rgb_9[2]      
                    except:
                        red_9   = 0
                        green_9 = 0
                        blue_9  = 0 

                else:
                    red_9 = 0
                    green_9 = 0
                    blue_9 = 0


                if SET_LED_SCENE(i, name, red_1, green_1, blue_1, red_2, green_2, blue_2, 
                                          red_3, green_3, blue_3, red_4, green_4, blue_4, 
                                          red_5, green_5, blue_5, red_6, green_6, blue_6, 
                                          red_7, green_7, blue_7, red_8, green_8, blue_8, 
                                          red_9, green_9, blue_9):

                    success_message_change_settings_led_scene = i


    """ ############### """
    """  add led scene  """
    """ ############### """   

    if request.form.get("add_led_scene") != None: 

        # check name
        if request.form.get("set_name") == "":
            error_message_add_led_scene.append("Keinen Namen angegeben")
        elif GET_LED_SCENE_BY_NAME(request.form.get("set_name")):  
            error_message_add_led_scene.append("Name bereits vergeben")               
        else:    
            name = request.form.get("set_name")                 
            result = ADD_LED_SCENE(name)   
            if result != True: 
                error_message_add_led_scene.append(result)         

            else:       
                success_message_add_led_scene = True
                name = ""


    """ ################## """
    """  delete led scene  """
    """ ################## """   

    for i in range (1,11):

        if request.form.get("delete_led_scene_" + str(i)) != None:
            scene  = GET_LED_SCENE_BY_ID(i).name  
            result = DELETE_LED_SCENE(i)            

            if result:
                success_message_change_settings.append(scene + " || Erfolgreich gelöscht") 
            else:
                error_message_change_settings.append(scene + " || " + str(result))



    list_led_scenes = GET_ALL_LED_SCENES()

    data = {'navigation': 'led', 'notification': ''} 

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/led_scenes.html', 
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings_led_scene=success_message_change_settings_led_scene,
                                                    error_message_change_settings_led_scene=error_message_change_settings_led_scene,  
                                                    success_message_add_led_scene=success_message_add_led_scene,
                                                    error_message_add_led_scene=error_message_add_led_scene,
                                                    list_led_scenes=list_led_scenes,
                                                    name=name,
                                                    rgb="rgb(0, 0, 255)",
                                                    ) 
                           )


# change led_scenes position 
@app.route('/led/scenes/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_led_scenes_position(id, direction):
    CHANGE_LED_SCENES_POSITION(id, direction)
    return redirect(url_for('led_scenes'))


# led scenes option add / remove led
@app.route('/led/scenes/<string:option>/<int:id>')
@login_required
@permission_required
def change_led_scenes_options(id, option):
    if option == "add_led":
        ADD_LED_SCENE_SETTING(id)
        session['set_collapse_open'] = id
        
    if option == "remove_led":
        REMOVE_LED_SCENE_SETTING(id)
        session['set_collapse_open'] = id

    return redirect(url_for('led_scenes'))


@app.route("/RGB" ,methods=['POST'])
def RGB():
    if request.method == 'POST':
        colorpicker = request.json['colorpicker']        
        rgb_values  = request.json['rgb_values']
        print(rgb_values)
        print(colorpicker)


	
    return json.dumps({'Status':'OK'})