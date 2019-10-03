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

    # delete message
    if session.get('delete_led_scene_success', None) != None:
        success_message_change_settings.append(session.get('delete_led_scene_success')) 
        session['delete_led_scene_success'] = None
        
    if session.get('delete_led_scene_error', None) != None:
        error_message_change_settings.append(session.get('delete_led_scene_error'))
        session['delete_led_scene_error'] = None       

    """ ################# """
    """  table led scenes """
    """ ################# """   

    for i in range (1,21):

        # add led setting
        if request.form.get("add_setting_" + str(i)) != None:
            ADD_LED_SCENE_SETTING(i)
            SET_LED_SCENE_COLLAPSE_OPEN(i)
            
        # remove led setting
        if request.form.get("remove_setting_" + str(i)) != None:
            REMOVE_LED_SCENE_SETTING(i)
            SET_LED_SCENE_COLLAPSE_OPEN(i)

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

                try:
                    hex_1 = request.form.get("set_hex_1_" + str(i))  
                except:
                    hex_1 = 0  
                                    
                # check color_temp
                color_temp_1 = request.form.get("set_color_temp_1_" + str(i))  

                # check brightness
                brightness_1 = request.form.get("set_brightness_1_" + str(i))   

                #######
                ## 2 ##
                #######

                if GET_LED_SCENE_BY_ID(i).active_setting_2 == "True":

                    try:
                        red_2   = request.form.get("set_red_2_" + str(i))
                        green_2 = request.form.get("set_green_2_" + str(i))          
                        blue_2  = request.form.get("set_blue_2_" + str(i))    
                    except:
                        red_2   = 0
                        green_2 = 0
                        blue_2  = 0 

                    # check color_temp
                    color_temp_2 = request.form.get("set_color_temp_2_" + str(i))  

                    # check brightness
                    brightness_2 = request.form.get("set_brightness_2_" + str(i))   

                else:
                    red_2 = 0
                    green_2 = 0
                    blue_2 = 0
                    color_temp_2 = 0                    
                    brightness_2 = 254

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

                    # check color_temp
                    color_temp_3 = request.form.get("set_color_temp_3_" + str(i))  

                    # check brightness
                    brightness_3 = request.form.get("set_brightness_3_" + str(i))   

                else:
                    red_3 = 0
                    green_3 = 0
                    blue_3 = 0
                    color_temp_3 = 0                    
                    brightness_3 = 254

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

                    # check color_temp
                    color_temp_4 = request.form.get("set_color_temp_4_" + str(i))  

                    # check brightness
                    brightness_4 = request.form.get("set_brightness_4_" + str(i))   

                else:
                    red_4 = 0
                    green_4 = 0
                    blue_4 = 0
                    color_temp_4 = 0                   
                    brightness_4 = 254

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

                    # check color_temp
                    color_temp_5 = request.form.get("set_color_temp_5_" + str(i))  

                    # check brightness
                    brightness_5 = request.form.get("set_brightness_5_" + str(i))   

                else:
                    red_5 = 0
                    green_5 = 0
                    blue_5 = 0
                    color_temp_5 = 0                    
                    brightness_5 = 254

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

                    # check color_temp
                    color_temp_6 = request.form.get("set_color_temp_6_" + str(i))  

                    # check brightness
                    brightness_6 = request.form.get("set_brightness_6_" + str(i))   

                else:
                    red_6 = 0
                    green_6 = 0
                    blue_6 = 0
                    color_temp_6 = 0                   
                    brightness_6 = 254

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

                    # check color_temp
                    color_temp_7 = request.form.get("set_color_temp_7_" + str(i))  

                    # check brightness
                    brightness_7 = request.form.get("set_brightness_7_" + str(i))   

                else:
                    red_7 = 0
                    green_7 = 0
                    blue_7 = 0
                    color_temp_7 = 0                    
                    brightness_7 = 254

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

                    # check color_temp
                    color_temp_8 = request.form.get("set_color_temp_8_" + str(i))  

                    # check brightness
                    brightness_8 = request.form.get("set_brightness_8_" + str(i))   

                else:
                    red_8 = 0
                    green_8 = 0
                    blue_8 = 0
                    color_temp_8 = 0                    
                    brightness_8 = 254

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

                    # check color_temp
                    color_temp_9 = request.form.get("set_color_temp_9_" + str(i))  

                    # check brightness
                    brightness_9 = request.form.get("set_brightness_9_" + str(i))   

                else:
                    red_9 = 0
                    green_9 = 0
                    blue_9 = 0
                    color_temp_9 = 0
                    brightness_9 = 254        

                
                print(request.form.get("set_hue_" + str(i)))
                print(request.form.get("set_saturation_" + str(i)))
                print(request.form.get("set_brightness_" + str(i)))
                    
                    
                if SET_LED_SCENE(i, name, hex_1, color_temp_1, brightness_1,
                                red_2, green_2, blue_2, color_temp_2, brightness_2,
                                red_3, green_3, blue_3, color_temp_3, brightness_3,
                                red_4, green_4, blue_4, color_temp_4, brightness_4,
                                red_5, green_5, blue_5, color_temp_5, brightness_5,
                                red_6, green_6, blue_6, color_temp_6, brightness_6,
                                red_7, green_7, blue_7, color_temp_7, brightness_7,
                                red_8, green_8, blue_8, color_temp_8, brightness_8,
                                red_9, green_9, blue_9, color_temp_9, brightness_9):

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
            error = ADD_LED_SCENE(name)   
            if error != None: 
                error_message_add_led_scene.append(error)         

            else:       
                success_message_add_led_scene = True
                name = ""

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
                                                    ) 
                           )


# change led_scenes position 
@app.route('/led/scenes/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_led_scenes_position(id, direction):
    CHANGE_LED_SCENES_POSITION(id, direction)
    return redirect(url_for('led_scenes'))


# delete scene
@app.route('/led/scenes/delete/<int:id>')
@login_required
@permission_required
def delete_led_scene(id):
    scene  = GET_LED_SCENE_BY_ID(id).name  
    result = DELETE_LED_SCENE(id)

    if result:
        session['delete_led_scene_success'] = scene + " || Erfolgreich gelöscht"
    else:
        session['delete_led_scene_error'] = scene + " || " + str(result)

    return redirect(url_for('led_scenes'))
