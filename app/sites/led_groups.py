from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.database.models         import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM
from app.backend.checks          import CHECK_LED_GROUP_SETTINGS
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


@app.route('/led/groups', methods=['GET', 'POST'])
@login_required
@permission_required
def led_groups():
    success_message_change_settings           = []
    error_message_change_settings             = []
    success_message_change_settings_led_group = ""
    error_message_change_settings_led_group   = []    
    success_message_add_led_group             = False
    error_message_add_led_group               = []
    name = ""

    RESET_LED_GROUP_COLLAPSE()
    UPDATE_LED_GROUP_LED_NAMES()


    """ ############### """
    """  add led group  """
    """ ############### """   

    if request.form.get("add_led_group") != None:                 
        result = ADD_LED_GROUP()   
        if result != True: 
            error_message_add_led_group.append(result)         

        else:       
            success_message_add_led_group = True


    """ ################## """
    """  table led groups  """
    """ ################## """   


    # set collapse open for option change led number
    if session.get("set_collapse_open", None) != None:
        SET_LED_GROUP_COLLAPSE_OPEN(session.get('set_collapse_open'))
        session['set_collapse_open'] = None

    for i in range (1,11):

        # change group
        if request.form.get("save_led_group_settings") != None:

            if request.form.get("set_name_" + str(i)) != None:
                
                SET_LED_GROUP_COLLAPSE_OPEN(i)      

                # ############
                # name setting
                # ############

                led_group  = GET_LED_GROUP_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i))                    

                # check spaces at the end
                if input_name != input_name.strip():
                    error_message_change_settings_led_group.append(led_group.name + " || Name - " + input_name + " - hat ungültige Leerzeichen") 
                    error_founded = True      

                # add new name
                if ((input_name != "") and (GET_LED_GROUP_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == led_group.name:
                    name = led_group.name                        
                    
                # name already exist
                elif ((GET_LED_GROUP_BY_NAME(input_name) != None) and (led_group.name != input_name)):
                    name = led_group.name 
                    error_message_change_settings_led_group = {"group_number": i,"message": "Name - " + input_name + " - bereits vergeben"}

                # no input commited
                else:                          
                    name = GET_LED_GROUP_BY_ID(i).name 
                    error_message_change_settings_led_group = {"group_number": i,"message": "Keinen Namen angegeben"}


                # ###########
                # led setting
                # ###########

                # led exist multiple times ?

                led_list = []

                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_1_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_2_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_3_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_4_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_5_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_6_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_7_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_8_" + str(i)))
                except:
                    pass
                try: 
                    led_list.append(request.form.get("set_led_ieeeAddr_9_" + str(i)))
                except:
                    pass

                for led_ieeeAddr in led_list:
                    num = led_list.count(led_ieeeAddr)
                
                    # led exist multiple times
                    if num > 1:

                        if led_ieeeAddr != "None" and led_ieeeAddr != None:
                            error_message_change_settings_led_group = {"group_number": i, "message": "LED mehrmals eingetragen || " + GET_DEVICE_BY_IEEEADDR(led_ieeeAddr).name}  
                            break

                    else:

                        #######
                        ## 1 ##
                        #######

                        try: 
                            led_ieeeAddr_1    = request.form.get("set_led_ieeeAddr_1_" + str(i))
                            led_name_1        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_1).name   
                            led_device_type_1 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_1).device_type         

                        except:
                            led_ieeeAddr_1    = "None"
                            led_name_1        = "None"
                            led_device_type_1 = "None"

                        #######
                        ## 2 ##
                        #######

                        try: 
                            led_ieeeAddr_2    = request.form.get("set_led_ieeeAddr_2_" + str(i))
                            led_name_2        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_2).name   
                            led_device_type_2 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_2).device_type         

                        except:
                            led_ieeeAddr_2    = "None"
                            led_name_2        = "None"
                            led_device_type_2 = "None"

                        #######
                        ## 3 ##
                        #######

                        try: 
                            led_ieeeAddr_3    = request.form.get("set_led_ieeeAddr_3_" + str(i))
                            led_name_3        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_3).name   
                            led_device_type_3 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_3).device_type         

                        except:
                            led_ieeeAddr_3    = "None"
                            led_name_3        = "None"
                            led_device_type_3 = "None"

                        #######
                        ## 4 ##
                        #######

                        try: 
                            led_ieeeAddr_4    = request.form.get("set_led_ieeeAddr_4_" + str(i))
                            led_name_4        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_4).name   
                            led_device_type_4 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_4).device_type         

                        except:
                            led_ieeeAddr_4    = "None"
                            led_name_4        = "None"
                            led_device_type_4 = "None"

                        #######
                        ## 5 ##
                        #######

                        try: 
                            led_ieeeAddr_5    = request.form.get("set_led_ieeeAddr_5_" + str(i))
                            led_name_5        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_5).name   
                            led_device_type_5 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_5).device_type         

                        except:
                            led_ieeeAddr_5    = "None"
                            led_name_5        = "None"
                            led_device_type_5 = "None"

                        #######
                        ## 6 ##
                        #######

                        try: 
                            led_ieeeAddr_6    = request.form.get("set_led_ieeeAddr_6_" + str(i))
                            led_name_6        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_6).name   
                            led_device_type_6 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_6).device_type         

                        except:
                            led_ieeeAddr_6    = "None"
                            led_name_6        = "None"
                            led_device_type_6 = "None"

                        #######
                        ## 7 ##
                        #######

                        try: 
                            led_ieeeAddr_7    = request.form.get("set_led_ieeeAddr_7_" + str(i))
                            led_name_7        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_7).name   
                            led_device_type_7 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_7).device_type         

                        except:
                            led_ieeeAddr_7    = "None"
                            led_name_7        = "None"
                            led_device_type_7 = "None"

                        #######
                        ## 8 ##
                        #######

                        try: 
                            led_ieeeAddr_8    = request.form.get("set_led_ieeeAddr_8_" + str(i))
                            led_name_8        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_8).name   
                            led_device_type_8 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_8).device_type         

                        except:
                            led_ieeeAddr_8    = "None"
                            led_name_8        = "None"
                            led_device_type_8 = "None"

                        #######
                        ## 9 ##
                        #######

                        try: 
                            led_ieeeAddr_9    = request.form.get("set_led_ieeeAddr_9_" + str(i))
                            led_name_9        = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_9).name   
                            led_device_type_9 = GET_DEVICE_BY_IEEEADDR(led_ieeeAddr_9).device_type         

                        except:
                            led_ieeeAddr_9    = "None"
                            led_name_9        = "None"
                            led_device_type_9 = "None"

                        if SET_LED_GROUP(i, name, led_ieeeAddr_1, led_name_1, led_device_type_1,
                                                  led_ieeeAddr_2, led_name_2, led_device_type_2,
                                                  led_ieeeAddr_3, led_name_3, led_device_type_3,
                                                  led_ieeeAddr_4, led_name_4, led_device_type_4,
                                                  led_ieeeAddr_5, led_name_5, led_device_type_5,
                                                  led_ieeeAddr_6, led_name_6, led_device_type_6,
                                                  led_ieeeAddr_7, led_name_7, led_device_type_7,
                                                  led_ieeeAddr_8, led_name_8, led_device_type_8,
                                                  led_ieeeAddr_9, led_name_9, led_device_type_9):
                            
                            success_message_change_settings_led_group = i


    """ ################## """
    """  delete led group  """
    """ ################## """   

    for i in range (1,21):

        if request.form.get("delete_led_group_" + str(i)) != None:
            group  = GET_LED_GROUP_BY_ID(i).name  
            result = DELETE_LED_GROUP(i)            

            if result:
                success_message_change_settings.append(group + " || Erfolgreich gelöscht") 
            else:
                error_message_change_settings.append(group + " || " + str(result))

    error_message_settings = CHECK_LED_GROUP_SETTINGS(GET_ALL_LED_GROUPS())

    dropdown_list_leds = GET_ALL_DEVICES("led")
    list_led_groups    = GET_ALL_LED_GROUPS()

    data = {'navigation': 'led'}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/led_groups.html', 
                                                    success_message_change_settings=success_message_change_settings,
                                                    error_message_change_settings=error_message_change_settings,
                                                    success_message_change_settings_led_group=success_message_change_settings_led_group,
                                                    error_message_change_settings_led_group=error_message_change_settings_led_group,
                                                    error_message_settings=error_message_settings,
                                                    success_message_add_led_group=success_message_add_led_group,
                                                    error_message_add_led_group=error_message_add_led_group,
                                                    list_led_groups=list_led_groups,
                                                    dropdown_list_leds=dropdown_list_leds,                       
                                                    ) 
                           )


# change led_groups position 
@app.route('/led/groups/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_led_groups_position(id, direction):
    CHANGE_LED_GROUPS_POSITION(id, direction)
    return redirect(url_for('led_groups'))


# led groups option add / remove led
@app.route('/led/groups/<string:option>/<int:id>')
@login_required
@permission_required
def change_led_groups_options(id, option):
    if option == "add_led":
        ADD_LED_GROUP_OBJECT(id)
        session['set_collapse_open'] = id
        
    if option == "remove_led":
        REMOVE_LED_GROUP_OBJECT(id)
        session['set_collapse_open'] = id

    return redirect(url_for('led_groups'))