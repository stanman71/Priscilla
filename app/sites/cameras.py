from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, Response
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps

from app                         import app
from app.backend.database_models import *
from app.common                  import COMMON, STATUS
from app.assets                  import *

from ping3 import ping

import cv2


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


try:
    camera_1_url = "rtsp://" + GET_CAMERA_BY_ID(1).user + ":" + GET_CAMERA_BY_ID(1).password + "@" + GET_CAMERA_BY_ID(1).url 
except:
    camera_1_url = None
 
try:
    camera_2_url = "rtsp://" + GET_CAMERA_BY_ID(2).user + ":" + GET_CAMERA_BY_ID(2).password + "@" + GET_CAMERA_BY_ID(2).url
except:
    camera_2_url = None
    
try:
    camera_3_url = "rtsp://" + GET_CAMERA_BY_ID(3).user + ":" + GET_CAMERA_BY_ID(3).password + "@" + GET_CAMERA_BY_ID(3).url            
except:
    camera_3_url = None

try:
    camera_4_url = "rtsp://" + GET_CAMERA_BY_ID(4).user + ":" + GET_CAMERA_BY_ID(4).password + "@" + GET_CAMERA_BY_ID(4).url              
except:
    camera_4_url = None

try:
    camera_5_url = "rtsp://" + GET_CAMERA_BY_ID(5).user + ":" + GET_CAMERA_BY_ID(5).password + "@" + GET_CAMERA_BY_ID(5).url             
except:
    camera_5_url = None
    
try:
    camera_6_url = "rtsp://" + GET_CAMERA_BY_ID(6).user + ":" + GET_CAMERA_BY_ID(6).password + "@" + GET_CAMERA_BY_ID(6).url               
except:
    camera_6_url = None
    

# generate frame by frame from camera
def GENERATE_FRAME(camera_url):
    try:   
        camera_ip = camera_url.split("@")[1]
        camera_ip = camera_ip.split(":")[0]
    except:
        camera_ip = ""

    if ping(camera_ip, timeout=1) != None:  

        while True:
            # Capture frame-by-frame
            success, frame = cv2.VideoCapture(camera_url).read()       

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/cameras', methods=['GET', 'POST'])
@login_required
@permission_required
def cameras():
    page_title       = 'Smarthome | Cameras'
    page_description = 'The cameras configuration page.'

    success_message_change_settings = []      
    error_message_change_settings   = []    
    success_message_add_camera      = False       
    error_message_add_camera        = []

    selected_camera = ""

    # default camera selection
    if GET_ALL_CAMERAS() != None:
        for camera in GET_ALL_CAMERAS():
            selected_camera = "camera_" + str(camera.id)
            break
    

    # delete message
    if session.get('delete_camera_success', None) != None:
        success_message_change_settings.append(session.get('delete_camera_success')) 
        session['delete_camera_success'] = None
        
    if session.get('delete_camera_error', None) != None:
        error_message_change_settings.append(session.get('delete_camera_error'))
        session['delete_camera_error'] = None       


    """ ################## """
    """  camera selection  """
    """ ################## """   

    if request.form.get("select_camera_1") != None: 
        selected_camera = "camera_1"  

    if request.form.get("select_camera_2") != None: 
        selected_camera = "camera_2"  

    if request.form.get("select_camera_3") != None: 
        selected_camera = "camera_3"  

    if request.form.get("select_camera_4") != None: 
        selected_camera = "camera_4"   

    if request.form.get("select_camera_5") != None: 
        selected_camera = "camera_5"  

    if request.form.get("select_camera_6") != None: 
        selected_camera = "camera_6"  


    """ ############ """
    """  add camera  """
    """ ############ """   

    if request.form.get("add_camera") != None: 
        result = ADD_CAMERA()   
        if result != True: 
            error_message_add_camera.append(result)         
        else:       
            success_message_add_camera = True


    """ ############### """
    """  table cameras  """
    """ ############### """   

    if request.form.get("save_cameras_settings") != None: 
        
        for i in range (1,26):

            if request.form.get("set_name_" + str(i)) != None:

                error_founded = False
        
                # ############
                # name setting
                # ############

                camera    = GET_CAMERA_BY_ID(i)
                input_name = request.form.get("set_name_" + str(i)).strip()                    

                # add new name
                if ((input_name != "") and (GET_CAMERA_BY_NAME(input_name) == None)):
                    name = request.form.get("set_name_" + str(i)) 
                    
                # nothing changed 
                elif input_name == camera.name:
                    name = camera.name                        
                    
                # name already exist
                elif ((GET_CAMERA_BY_NAME(input_name) != None) and (camera.name != input_name)):
                    error_message_change_settings.append(camera.name + " || Name - " + input_name + " - already taken")  
                    error_founded = True
                    name = camera.name

                # no input commited
                else:                          
                    name = GET_CAMERA_BY_ID(i).name
                    error_message_change_settings.append(camera.name + " || No name given") 
                    error_founded = True  


                # ###########
                # url setting
                # ###########

                input_url = request.form.get("set_url_" + str(i)).strip()                      

                # add new url
                if ((input_url != "") and (GET_CAMERA_BY_URL(input_url) == None)):
                    url = request.form.get("set_url_" + str(i)) 
                    
                # nothing changed 
                elif input_url == camera.url:
                    url = camera.url                        
                    
                # url already exist
                elif ((GET_CAMERA_BY_URL(input_url) != None) and (camera.url != input_url)):
                    error_message_change_settings.append(camera.name + " || URL already taken")  
                    error_founded = True
                    url = camera.url

                # no input commited
                else:                          
                    url = GET_CAMERA_BY_ID(i).url
                    error_message_change_settings.append(camera.name + " || No URL given") 
                    error_founded = True  

            
                # ##################
                # credential setting
                # ##################

                user     = request.form.get("set_user_" + str(i)).strip()  
                password = request.form.get("set_password_" + str(i)).strip()  


                # save settings
                if error_founded == False: 
                    if SET_CAMERA_SETTINGS(i, name, url, user, password):
                        success_message_change_settings.append(name + " || Settings successfully saved - System restart nessessary") 


    """ ############# """
    """  camera data  """
    """ ############# """   

    try:
        camera_1 = GET_CAMERA_BY_ID(1)
    except:
        camera_1 = None      
    try:
        camera_2 = GET_CAMERA_BY_ID(2)
    except:
        camera_2 = None       
    try:
        camera_3 = GET_CAMERA_BY_ID(3)
    except:
        camera_3 = None
    try:
        camera_4 = GET_CAMERA_BY_ID(4)
    except:
        camera_4 = None
    try:
        camera_5 = GET_CAMERA_BY_ID(5)
    except:
        camera_5 = None
    try:
        camera_6 = GET_CAMERA_BY_ID(6)
    except:
        camera_6 = None        


    list_cameras = GET_ALL_CAMERAS()

    data = {'navigation': 'cameras'}

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('layouts/default.html',
                            data=data,    
                            title=page_title,        
                            description=page_description,               
                            content=render_template( 'pages/cameras.html',
                                                    success_message_change_settings=success_message_change_settings,                               
                                                    error_message_change_settings=error_message_change_settings,   
                                                    success_message_add_camera=success_message_add_camera,                            
                                                    error_message_add_camera=error_message_add_camera,     
                                                    list_cameras=list_cameras,  
                                                    selected_camera=selected_camera,
                                                    camera_1=camera_1,    
                                                    camera_2=camera_2, 
                                                    camera_3=camera_3,
                                                    camera_4=camera_4,    
                                                    camera_5=camera_5, 
                                                    camera_6=camera_6,                                                             
                                                    ) 
                           )


# change cameras position 
@app.route('/cameras/position/<string:direction>/<int:id>')
@login_required
@permission_required
def change_cameras_position(id, direction):
    CHANGE_CAMERAS_POSITION(id, direction)
    return redirect(url_for('cameras'))


# delete camera
@app.route('/cameras/delete/<int:id>')
@login_required
@permission_required
def delete_camera(id):
    camera  = GET_CAMERA_BY_ID(id).name  
    result  = DELETE_CAMERA(id)

    if result == True:
        session['delete_camera_success'] = camera + " || Camera successfully deleted"
    else:
        session['delete_camera_error'] = camera + " || " + str(result)

    return redirect(url_for('cameras'))


# camera streams
@app.route('/cameras/data/video_feed_1')
def data_video_feed_1():
    return Response(GENERATE_FRAME(camera_1_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras/data/video_feed_2')
def data_video_feed_2():
    return Response(GENERATE_FRAME(camera_2_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras/data/video_feed_3')
def data_video_feed_3():
    return Response(GENERATE_FRAME(camera_3_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/cameras/data/video_feed_4')
def data_video_feed_4():
    return Response(GENERATE_FRAME(camera_4_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 
 
@app.route('/cameras/data/video_feed_5')
def data_video_feed_5():
    return Response(GENERATE_FRAME(camera_5_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras/data/video_feed_6')
def data_video_feed_6():
    return Response(GENERATE_FRAME(camera_6_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')