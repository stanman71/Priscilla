from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.checks          import CHECK_TASKS
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
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


lighting_scenes_rgb_values_array = [[0 for x in range(10)] for y in range(20)] 


@app.route('/lighting/scenes', methods=['GET', 'POST'])
@login_required
@permission_required
def lighting_scenes():
    page_title       = 'Smarthome | Lighting | Scenes'
    page_description = 'The lighting scenes configuration page.'

    global lighting_scenes_rgb_values_array

    success_message_change_settings                = []
    error_message_change_settings                  = []    
    success_message_change_settings_lighting_scene = ""
    error_message_change_settings_lighting_scene   = []    
    success_message_add_lighting_scene             = False
    error_message_add_lighting_scene               = []
    name = ""

    RESET_LIGHTING_SCENE_COLLAPSE()


    """ #################### """
    """  add lighting scene  """
    """ #################### """   

    if request.form.get("add_lighting_scene") != None:             
        result = ADD_LIGHTING_SCENE()   
        if result != True: 
            error_message_add_lighting_scene.append(result)         

        else:       
            success_message_add_lighting_scene = True
            

    """ ####################### """
    """  table lighting scenes  """
    """ ####################### """   


    # set collapse open 
    if session.get("set_collapse_open", None) != None:
        SET_LIGHTING_SCENE_COLLAPSE_OPEN(session.get('set_collapse_open'))
        session['set_collapse_open'] = None


    for i in range (1,21):

        # change scene
        if request.form.get("save_lighting_scene_settings") != None:

            if request.form.get("set_name_" + str(i)) != None:
                
                SET_LIGHTING_SCENE_COLLAPSE_OPEN(i)      

                # ############
                # name setting
                # ############

                lighting_scene  = GET_LIGHTING_SCENE_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i)).strip()                    

                # add new name
                if ((input_name != "") and (GET_LIGHTING_SCENE_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == lighting_scene.name:
                    name = lighting_scene.name                        
                    
                # name already exist
                elif ((GET_LIGHTING_SCENE_BY_NAME(input_name) != None) and (lighting_scene.name != input_name)):
                    name = lighting_scene.name 
                    error_message_change_settings_lighting_scene = {"scene_number": i,"message": "Name - " + input_name + " - already taken"}

                # no input commited
                else:                          
                    name = GET_LIGHTING_SCENE_BY_ID(i).name 
                    error_message_change_settings_lighting_scene = {"scene_number": i,"message": "No name given"}


                #######
                ## 1 ##
                #######

                # check rgb
                rgb_1 = lighting_scenes_rgb_values_array[i-1][1-1]

                try:
                    rgb_1   = re.findall(r'\d+', rgb_1)
                    red_1   = rgb_1[0]
                    green_1 = rgb_1[1]           
                    blue_1  = rgb_1[2]      
                
                except:
                    red_1   = 0
                    green_1 = 0
                    blue_1  = 0 

                brightness_1 = request.form.get("set_brightness_1_" + str(i)) 
                                
                #######
                ## 2 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_2 == "True":

                    # check rgb
                    rgb_2 = lighting_scenes_rgb_values_array[i-1][2-1]

                    try:
                        rgb_2   = re.findall(r'\d+', rgb_2)
                        red_2   = rgb_2[0]
                        green_2 = rgb_2[1]           
                        blue_2  = rgb_2[2]    

                    except:
                        red_2   = 0
                        green_2 = 0
                        blue_2  = 0 

                    brightness_2 = request.form.get("set_brightness_2_" + str(i)) 

                else:
                    red_2        = 0
                    green_2      = 0
                    blue_2       = 0
                    brightness_2 = 0

                #######
                ## 3 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_3 == "True":

                    # check rgb
                    rgb_3 = lighting_scenes_rgb_values_array[i-1][3-1]

                    try:
                        rgb_3   = re.findall(r'\d+', rgb_3)
                        red_3   = rgb_3[0]
                        green_3 = rgb_3[1]           
                        blue_3  = rgb_3[2]      

                    except:
                        red_3   = 0
                        green_3 = 0
                        blue_3  = 0 

                    brightness_3 = request.form.get("set_brightness_3_" + str(i)) 

                else:
                    red_3        = 0
                    green_3      = 0
                    blue_3       = 0
                    brightness_3 = 0

                #######
                ## 4 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_4 == "True":

                    # check rgb
                    rgb_4 = lighting_scenes_rgb_values_array[i-1][4-1]

                    try:
                        rgb_4   = re.findall(r'\d+', rgb_4)
                        red_4   = rgb_4[0]
                        green_4 = rgb_4[1]           
                        blue_4  = rgb_4[2]      

                    except:
                        red_4   = 0
                        green_4 = 0
                        blue_4  = 0 

                    brightness_4 = request.form.get("set_brightness_4_" + str(i)) 

                else:
                    red_4        = 0
                    green_4      = 0
                    blue_4       = 0
                    brightness_4 = 0

                #######
                ## 5 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_5 == "True":

                    # check rgb
                    rgb_5 = lighting_scenes_rgb_values_array[i-1][5-1]

                    try:
                        rgb_5   = re.findall(r'\d+', rgb_5)
                        red_5   = rgb_5[0]
                        green_5 = rgb_5[1]           
                        blue_5  = rgb_5[2]      

                    except:
                        red_5   = 0
                        green_5 = 0
                        blue_5  = 0 

                    brightness_5 = request.form.get("set_brightness_5_" + str(i)) 

                else:
                    red_5        = 0
                    green_5      = 0
                    blue_5       = 0
                    brightness_5 = 0

                #######
                ## 6 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_6 == "True":

                    # check rgb
                    rgb_6 = lighting_scenes_rgb_values_array[i-1][6-1]

                    try:
                        rgb_6   = re.findall(r'\d+', rgb_6)
                        red_6   = rgb_6[0]
                        green_6 = rgb_6[1]           
                        blue_6  = rgb_6[2]    

                    except:
                        red_6   = 0
                        green_6 = 0
                        blue_6  = 0 

                    brightness_6 = request.form.get("set_brightness_6_" + str(i)) 

                else:
                    red_6        = 0
                    green_6      = 0
                    blue_6       = 0
                    brightness_6 = 0

                #######
                ## 7 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_7 == "True":

                    # check rgb
                    rgb_7 = lighting_scenes_rgb_values_array[i-1][7-1]

                    try:
                        rgb_7   = re.findall(r'\d+', rgb_7)
                        red_7   = rgb_7[0]
                        green_7 = rgb_7[1]           
                        blue_7  = rgb_7[2]  
                            
                    except:
                        red_7   = 0
                        green_7 = 0
                        blue_7  = 0 

                    brightness_7 = request.form.get("set_brightness_7_" + str(i)) 

                else:
                    red_7        = 0
                    green_7      = 0
                    blue_7       = 0
                    brightness_7 = 0

                #######
                ## 8 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_8 == "True":

                    # check rgb
                    rgb_8 = lighting_scenes_rgb_values_array[i-1][8-1]

                    try:
                        rgb_8   = re.findall(r'\d+', rgb_8)
                        red_8   = rgb_8[0]
                        green_8 = rgb_8[1]           
                        blue_8  = rgb_8[2]  

                    except:
                        red_8   = 0
                        green_8 = 0
                        blue_8  = 0 

                    brightness_8 = request.form.get("set_brightness_8_" + str(i)) 

                else:
                    red_8        = 0
                    green_8      = 0
                    blue_8       = 0
                    brightness_8 = 0

                #######
                ## 9 ##
                #######

                if GET_LIGHTING_SCENE_BY_ID(i).active_light_9 == "True":

                    # check rgb
                    rgb_9 = lighting_scenes_rgb_values_array[i-1][9-1]

                    try:
                        rgb_9   = re.findall(r'\d+', rgb_9)
                        red_9   = rgb_9[0]
                        green_9 = rgb_9[1]           
                        blue_9  = rgb_9[2]  

                    except:
                        red_9   = 0
                        green_9 = 0
                        blue_9  = 0 

                    brightness_9 = request.form.get("set_brightness_9_" + str(i)) 

                else:
                    red_9        = 0
                    green_9      = 0
                    blue_9       = 0
                    brightness_9 = 0


                if SET_LIGHTING_SCENE(i, name, red_1, green_1, blue_1, brightness_1, red_2, green_2, blue_2, brightness_2, red_3, green_3, blue_3, brightness_3, 
                                               red_4, green_4, blue_4, brightness_4, red_5, green_5, blue_5, brightness_5, red_6, green_6, blue_6, brightness_6, 
                                               red_7, green_7, blue_7, brightness_7, red_8, green_8, blue_8, brightness_8, red_9, green_9, blue_9, brightness_9):

                    success_message_change_settings_lighting_scene = i


    """ ####################### """
    """  delete lighting scene  """
    """ ####################### """   

    for i in range (1,21):

        if request.form.get("delete_lighting_scene_" + str(i)) != None:
            scene  = GET_LIGHTING_SCENE_BY_ID(i).name  
            result = DELETE_LIGHTING_SCENE(i)    

            if result:
                success_message_change_settings.append(scene + " || Scene successfully deleted") 
            else:
                error_message_change_settings.append(scene + " || " + str(result))


    scene_1  = GET_LIGHTING_SCENE_BY_ID(1)
    scene_2  = GET_LIGHTING_SCENE_BY_ID(2)
    scene_3  = GET_LIGHTING_SCENE_BY_ID(3)
    scene_4  = GET_LIGHTING_SCENE_BY_ID(4)
    scene_5  = GET_LIGHTING_SCENE_BY_ID(5)
    scene_6  = GET_LIGHTING_SCENE_BY_ID(6)
    scene_7  = GET_LIGHTING_SCENE_BY_ID(7)
    scene_8  = GET_LIGHTING_SCENE_BY_ID(8)
    scene_9  = GET_LIGHTING_SCENE_BY_ID(9)
    scene_10 = GET_LIGHTING_SCENE_BY_ID(10)
    scene_11 = GET_LIGHTING_SCENE_BY_ID(11)
    scene_12 = GET_LIGHTING_SCENE_BY_ID(12)
    scene_13 = GET_LIGHTING_SCENE_BY_ID(13)
    scene_14 = GET_LIGHTING_SCENE_BY_ID(14)
    scene_15 = GET_LIGHTING_SCENE_BY_ID(15)
    scene_16 = GET_LIGHTING_SCENE_BY_ID(16)
    scene_17 = GET_LIGHTING_SCENE_BY_ID(17)
    scene_18 = GET_LIGHTING_SCENE_BY_ID(18)
    scene_19 = GET_LIGHTING_SCENE_BY_ID(19)
    scene_20 = GET_LIGHTING_SCENE_BY_ID(20)

    list_lighting_scenes = GET_ALL_LIGHTING_SCENES()

    data = {'navigation': 'lighting'} 

    return render_template('layouts/default.html',
                            data=data,   
                            title=page_title,        
                            description=page_description,                                
                            content=render_template( 'pages/lighting_scenes.html', 
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings_lighting_scene=success_message_change_settings_lighting_scene,
                                                    error_message_change_settings_lighting_scene=error_message_change_settings_lighting_scene,  
                                                    success_message_add_lighting_scene=success_message_add_lighting_scene,
                                                    error_message_add_lighting_scene=error_message_add_lighting_scene,
                                                    list_lighting_scenes=list_lighting_scenes,
                                                    scene_1=scene_1,
                                                    scene_2=scene_2,      
                                                    scene_3=scene_3,    
                                                    scene_4=scene_4,
                                                    scene_5=scene_5,
                                                    scene_6=scene_6,
                                                    scene_7=scene_7,
                                                    scene_8=scene_8,
                                                    scene_9=scene_9,
                                                    scene_10=scene_10,        
                                                    scene_11=scene_11,  
                                                    scene_12=scene_12,  
                                                    scene_13=scene_13,  
                                                    scene_14=scene_14,  
                                                    scene_15=scene_15,  
                                                    scene_16=scene_16,  
                                                    scene_17=scene_17,  
                                                    scene_18=scene_18,  
                                                    scene_19=scene_19,  
                                                    scene_20=scene_20,                                                      
                                                    ) 
                           )


# change lighting scenes position 
@app.route('/lighting/scenes/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_lighting_scenes_position(id, direction):
    CHANGE_LIGHTING_SCENES_POSITION(id, direction)
    return redirect(url_for('lighting_scenes'))


# lighting scenes option add light / remove light
@app.route('/lighting/scenes/<string:option>/<int:id>')
@login_required
@permission_required
def change_lighting_scenes_options(id, option):
    if option == "add_light":
        ADD_LIGHTING_SCENE_OBJECT(id)
        session['set_collapse_open'] = id
        
    if option == "remove_light":
        REMOVE_LIGHTING_SCENE_OBJECT(id)
        session['set_collapse_open'] = id

    return redirect(url_for('lighting_scenes'))


@app.route("/lighting/scenes/data/rgb_values" ,methods=['POST'])
def data_rgb_values():
    global lighting_scenes_rgb_values_array

    if request.method == 'POST':
        scene_number = request.json['scene_number']     
        light_number = request.json['light_number']    
        rgb_values   = request.json['rgb_values']
        
        lighting_scenes_rgb_values_array[scene_number-1][light_number-1] = rgb_values
	
    return json.dumps({'Status':'OK'})