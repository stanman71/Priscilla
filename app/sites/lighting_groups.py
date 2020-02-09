from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.checks          import CHECK_LIGHTING_GROUP_SETTINGS
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


@app.route('/lighting/groups', methods=['GET', 'POST'])
@login_required
@permission_required
def lighting_groups():
    page_title       = 'Smarthome | Lighting | Groups'
    page_description = 'The lighting groups configuration page.'

    success_message_change_settings                = []
    error_message_change_settings                  = []
    success_message_change_settings_lighting_group = ""
    error_message_change_settings_lighting_group   = []    
    success_message_add_lighting_group             = False
    error_message_add_lighting_group               = []
    name = ""

    RESET_LIGHTING_GROUP_COLLAPSE()
    UPDATE_LIGHTING_GROUP_LIGHT_NAMES()


    """ #################### """
    """  add lighting group  """
    """ #################### """   

    if request.form.get("add_lighting_group") != None:                 
        result = ADD_LIGHTING_GROUP()   
        if result != True: 
            error_message_add_lighting_group.append(result)         

        else:       
            success_message_add_lighting_group = True


    """ ####################### """
    """  table lighting groups  """
    """ ####################### """   


    # set collapse open for option change lighting number
    if session.get("set_collapse_open", None) != None:
        SET_LIGHTING_GROUP_COLLAPSE_OPEN(session.get('set_collapse_open'))
        session['set_collapse_open'] = None

    for i in range (1,11):

        # change group
        if request.form.get("save_lighting_group_settings") != None:

            if request.form.get("set_name_" + str(i)) != None:
                
                SET_LIGHTING_GROUP_COLLAPSE_OPEN(i)      

                # ############
                # name setting
                # ############

                lighting_group  = GET_LIGHTING_GROUP_BY_ID(i)
                input_name      = request.form.get("set_name_" + str(i)).strip()                    

                # add new name
                if ((input_name != "") and (GET_LIGHTING_GROUP_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == lighting_group.name:
                    name = lighting_group.name                        
                    
                # name already exist
                elif ((GET_LIGHTING_GROUP_BY_NAME(input_name) != None) and (lighting_group.name != input_name)):
                    name = lighting_group.name 
                    error_message_change_settings_lighting_group = {"group_number": i,"message": "Name - " + input_name + " - already taken"}

                # no input commited
                else:                          
                    name = GET_LIGHTING_GROUP_BY_ID(i).name 
                    error_message_change_settings_lighting_group = {"group_number": i,"message": "No name given"}


                # ################
                # lighting setting
                # ################

                # lighting exist multiple times ?

                lighting_list = []

                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_1_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_2_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_3_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_4_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_5_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_6_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_7_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_8_" + str(i)))
                except:
                    pass
                try: 
                    lighting_list.append(request.form.get("set_light_ieeeAddr_9_" + str(i)))
                except:
                    pass

                for light_ieeeAddr in lighting_list:
                    num = lighting_list.count(light_ieeeAddr)
                
                    # light exist multiple times
                    if num > 1:

                        if light_ieeeAddr != "None" and light_ieeeAddr != None:
                            error_message_change_settings_lighting_group = {"group_number": i, "message": "Light selected several times || " + GET_DEVICE_BY_IEEEADDR(light_ieeeAddr).name}  
                            break

                    else:

                        #######
                        ## 1 ##
                        #######

                        try: 
                            light_ieeeAddr_1    = request.form.get("set_light_ieeeAddr_1_" + str(i))
                            light_name_1        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_1).name   
                            light_device_type_1 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_1).device_type         

                        except:
                            light_ieeeAddr_1    = "None"
                            light_name_1        = "None"
                            light_device_type_1 = "None"

                        #######
                        ## 2 ##
                        #######

                        try: 
                            light_ieeeAddr_2    = request.form.get("set_light_ieeeAddr_2_" + str(i))
                            light_name_2        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_2).name   
                            light_device_type_2 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_2).device_type         

                        except:
                            light_ieeeAddr_2    = "None"
                            light_name_2        = "None"
                            light_device_type_2 = "None"

                        #######
                        ## 3 ##
                        #######

                        try: 
                            light_ieeeAddr_3    = request.form.get("set_light_ieeeAddr_3_" + str(i))
                            light_name_3        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_3).name   
                            light_device_type_3 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_3).device_type         

                        except:
                            light_ieeeAddr_3    = "None"
                            light_name_3        = "None"
                            light_device_type_3 = "None"

                        #######
                        ## 4 ##
                        #######

                        try: 
                            light_ieeeAddr_4    = request.form.get("set_light_ieeeAddr_4_" + str(i))
                            light_name_4        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_4).name   
                            light_device_type_4 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_4).device_type         

                        except:
                            light_ieeeAddr_4    = "None"
                            light_name_4        = "None"
                            light_device_type_4 = "None"

                        #######
                        ## 5 ##
                        #######

                        try: 
                            light_ieeeAddr_5    = request.form.get("set_light_ieeeAddr_5_" + str(i))
                            light_name_5        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_5).name   
                            light_device_type_5 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_5).device_type         

                        except:
                            light_ieeeAddr_5    = "None"
                            light_name_5        = "None"
                            light_device_type_5 = "None"

                        #######
                        ## 6 ##
                        #######

                        try: 
                            light_ieeeAddr_6    = request.form.get("set_light_ieeeAddr_6_" + str(i))
                            light_name_6        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_6).name   
                            light_device_type_6 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_6).device_type         

                        except:
                            light_ieeeAddr_6    = "None"
                            light_name_6        = "None"
                            light_device_type_6 = "None"

                        #######
                        ## 7 ##
                        #######

                        try: 
                            light_ieeeAddr_7    = request.form.get("set_light_ieeeAddr_7_" + str(i))
                            light_name_7        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_7).name   
                            light_device_type_7 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_7).device_type         

                        except:
                            light_ieeeAddr_7    = "None"
                            light_name_7        = "None"
                            light_device_type_7 = "None"

                        #######
                        ## 8 ##
                        #######

                        try: 
                            light_ieeeAddr_8    = request.form.get("set_light_ieeeAddr_8_" + str(i))
                            light_name_8        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_8).name   
                            light_device_type_8 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_8).device_type         

                        except:
                            light_ieeeAddr_8    = "None"
                            light_name_8        = "None"
                            light_device_type_8 = "None"

                        #######
                        ## 9 ##
                        #######

                        try: 
                            light_ieeeAddr_9    = request.form.get("set_light_ieeeAddr_9_" + str(i))
                            light_name_9        = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_9).name   
                            light_device_type_9 = GET_DEVICE_BY_IEEEADDR(light_ieeeAddr_9).device_type         

                        except:
                            light_ieeeAddr_9    = "None"
                            light_name_9        = "None"
                            light_device_type_9 = "None"

                        if SET_LIGHTING_GROUP(i, name, light_ieeeAddr_1, light_name_1, light_device_type_1,
                                                       light_ieeeAddr_2, light_name_2, light_device_type_2,
                                                       light_ieeeAddr_3, light_name_3, light_device_type_3,
                                                       light_ieeeAddr_4, light_name_4, light_device_type_4,
                                                       light_ieeeAddr_5, light_name_5, light_device_type_5,
                                                       light_ieeeAddr_6, light_name_6, light_device_type_6,
                                                       light_ieeeAddr_7, light_name_7, light_device_type_7,
                                                       light_ieeeAddr_8, light_name_8, light_device_type_8,
                                                       light_ieeeAddr_9, light_name_9, light_device_type_9):
                            
                            success_message_change_settings_lighting_group = i


    """ ####################### """
    """  delete lighting group  """
    """ ####################### """   

    for i in range (1,21):

        if request.form.get("delete_lighting_group_" + str(i)) != None:
            group  = GET_LIGHTING_GROUP_BY_ID(i).name  
            result = DELETE_LIGHTING_GROUP(i)            

            if result:
                success_message_change_settings.append(group + " || Group successfully deleted") 
            else:
                error_message_change_settings.append(group + " || " + str(result))

    error_message_settings = CHECK_LIGHTING_GROUP_SETTINGS(GET_ALL_LIGHTING_GROUPS())

    dropdown_list_lights = GET_ALL_DEVICES("light")
    list_lighting_groups = GET_ALL_LIGHTING_GROUPS()

    data = {'navigation': 'lighting'}

    return render_template('layouts/default.html',
                            data=data,  
                            title=page_title,        
                            description=page_description,                                 
                            content=render_template( 'pages/lighting_groups.html', 
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings_lighting_group=success_message_change_settings_lighting_group,
                                                    error_message_change_settings_lighting_group=error_message_change_settings_lighting_group,
                                                    error_message_settings=error_message_settings,
                                                    success_message_add_lighting_group=success_message_add_lighting_group,
                                                    error_message_add_lighting_group=error_message_add_lighting_group,
                                                    list_lighting_groups=list_lighting_groups,
                                                    dropdown_list_lights=dropdown_list_lights,                       
                                                    ) 
                           )


# change lighting_groups position 
@app.route('/lighting/groups/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_lighting_groups_position(id, direction):
    CHANGE_LIGHTING_GROUPS_POSITION(id, direction)
    return redirect(url_for('lighting_groups'))


# lighting groups option add / remove light
@app.route('/lighting/groups/<string:option>/<int:id>')
@login_required
@permission_required
def change_lighting_groups_options(id, option):
    if option == "add_light":
        ADD_LIGHTING_GROUP_OBJECT(id)
        session['set_collapse_open'] = id
        
    if option == "remove_light":
        REMOVE_LIGHTING_GROUP_OBJECT(id)
        session['set_collapse_open'] = id

    return redirect(url_for('lighting_groups'))