from flask             import Flask
from flask_bootstrap   import Bootstrap
from flask_mail        import Mail
from flask_apscheduler import APScheduler
from threading         import Lock
from flask             import Flask, render_template, session, request, copy_current_request_context
from flask_socketio    import SocketIO, emit
from flask_mobility    import Mobility

# load RES
from app import assets  

import time
import netifaces
import os
import heapq
import json


""" ###### """
"""  path  """
""" ###### """

# windows
if os.name == "nt":                 
    PATH = os.path.abspath("") 
# linux
else:                               
    PATH = "/home/pi/smarthome/"


""" ####### """
"""  flask  """
""" ####### """

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY']                     = "random"        #os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + PATH + '/data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT']      = 1
app.config['UPLOAD_FOLDER']                  = PATH + "firmwares/"
app.config['MAX_CONTENT_LENGTH']             = 2 * 1024 * 1024  # 2 MB

Mobility(app)

# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )


from app.backend.database_models  import *
from app.backend.spotify          import *
from app.backend.shared_resources import *


""" ######### """
""" socket IO """
""" ######### """

async_mode  = None
socketio    = SocketIO(app, async_mode=async_mode)
thread      = None
thread_lock = Lock()

def background_thread():
    
    while True:
        socketio.sleep(0.5)

        # ##########
        # system_log
        # ##########

        try:

            selected_log_types = ["EVENT", "DATABASE", "SUCCESS", "WARNING", "ERROR"]
            log_search         = ""

            # get log entries
            if GET_LOGFILE_SYSTEM(selected_log_types, log_search, 10) != None:
                data_log_system = GET_LOGFILE_SYSTEM(selected_log_types, log_search, 10)
            else:
                data_log_system = ""

            socketio.emit('system_log',
                         {'data_0_title': data_log_system[0][1] + " ||| " + data_log_system[0][0], 'data_0_content': data_log_system[0][2], 
                          'data_1_title': data_log_system[1][1] + " ||| " + data_log_system[1][0], 'data_1_content': data_log_system[1][2], 
                          'data_2_title': data_log_system[2][1] + " ||| " + data_log_system[2][0], 'data_2_content': data_log_system[2][2], 
                          'data_3_title': data_log_system[3][1] + " ||| " + data_log_system[3][0], 'data_3_content': data_log_system[3][2], 
                          'data_4_title': data_log_system[4][1] + " ||| " + data_log_system[4][0], 'data_4_content': data_log_system[4][2], 
                          'data_5_title': data_log_system[5][1] + " ||| " + data_log_system[5][0], 'data_5_content': data_log_system[5][2], 
                          'data_6_title': data_log_system[6][1] + " ||| " + data_log_system[6][0], 'data_6_content': data_log_system[6][2], 
                          'data_7_title': data_log_system[7][1] + " ||| " + data_log_system[7][0], 'data_7_content': data_log_system[7][2], 
                          'data_8_title': data_log_system[8][1] + " ||| " + data_log_system[8][0], 'data_8_content': data_log_system[8][2], 
                          'data_9_title': data_log_system[9][1] + " ||| " + data_log_system[9][0], 'data_9_content': data_log_system[9][2]},                                                    
                          namespace='/socketIO')

        except:
            socketio.emit('system_log',
                         {'data_0_title': "" + " ||| " + "", 'data_0_content': "", 
                          'data_1_title': "" + " ||| " + "", 'data_1_content': "", 
                          'data_2_title': "" + " ||| " + "", 'data_2_content': "", 
                          'data_3_title': "" + " ||| " + "", 'data_3_content': "", 
                          'data_4_title': "" + " ||| " + "", 'data_4_content': "", 
                          'data_5_title': "" + " ||| " + "", 'data_5_content': "", 
                          'data_6_title': "" + " ||| " + "", 'data_6_content': "", 
                          'data_7_title': "" + " ||| " + "", 'data_7_content': "", 
                          'data_8_title': "" + " ||| " + "", 'data_8_content': "", 
                          'data_9_title': "" + " ||| " + "", 'data_9_content': ""},                                                    
                          namespace='/socketIO')            

        # #####
        # music
        # #####

        try:
            spotify_token = GET_SPOTIFY_TOKEN()

            if spotify_token != "":

                tupel_current_playback = GET_SPOTIFY_CURRENT_PLAYBACK(spotify_token)

                current_device   = tupel_current_playback[0]
                current_state    = tupel_current_playback[2]
                current_track    = tupel_current_playback[4]
                current_artists  = tupel_current_playback[5]
                current_progress = tupel_current_playback[6]
                current_playlist = tupel_current_playback[7]

                socketio.emit('music',
                             {'current_device': current_device, 'current_state': current_state, 'current_track': current_track, 
                              'current_artists': current_artists, 'current_progress': current_progress, 'current_playlist': current_playlist},                                                               
                              namespace='/socketIO')

            else:
                socketio.emit('music',
                             {'current_device': "", 'current_state': "", 'current_track': "", 'current_artists': "", 'current_progress': "", 'current_playlist': ""},                                                               
                               namespace='/socketIO')          

        except:
            socketio.emit('music',
                         {'current_device': "", 'current_state': "", 'current_track': "", 'current_artists': "", 'current_progress': "", 'current_playlist': ""},                                                               
                           namespace='/socketIO')                 

        # ########
        # programs
        # ########

        try:
            socketio.emit('program_thread_1',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_1()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_1()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_1()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_1()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_1',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')       

        try:
            socketio.emit('program_thread_2',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_2()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_2()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_2()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_2()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_2',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_3',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_3()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_3()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_3()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_3()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_3',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_4',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_4()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_4()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_4()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_4()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_4',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_5',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_5()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_5()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_5()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_5()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_5',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_6',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_6()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_6()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_6()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_6()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_6',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_7',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_7()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_7()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_7()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_7()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_7',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_8',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_8()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_8()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_8()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_8()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_8',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')     

        try:
            socketio.emit('program_thread_9',
                         {'program_name': GET_PROGRAM_THREAD_STATUS_9()[0], 
                          'line': GET_PROGRAM_THREAD_STATUS_9()[1], 
                          'lines_total': GET_PROGRAM_THREAD_STATUS_9()[2],
                          'command': GET_PROGRAM_THREAD_STATUS_9()[3]},
                           namespace='/socketIO')

        except:
            socketio.emit('program_thread_9',
                         {'program_name':"", 
                          'line': "", 
                          'lines_total': "",
                          'command': ""},
                           namespace='/socketIO')                                


        # ###########################
        # zigbee device update status
        # ###########################

        try:
            socketio.emit('zigbee_device_update',
                        {'zigbee_device_update_status': GET_ZIGBEE_DEVICE_UPDATE_STATUS()},                                                               
                          namespace='/socketIO')
 
        except:
             socketio.emit('zigbee_device_update',
                        {'zigbee_device_update_status': "Status Error"},                                                               
                          namespace='/socketIO')    


        # ##########################
        # zigbee2mqtt pairing status
        # ##########################

        try:
            socketio.emit('zigbee2mqtt_pairing',
                        {'zigbee2mqtt_pairing_status': GET_ZIGBEE2MQTT_PAIRING_STATUS()},                                                               
                          namespace='/socketIO')
 
        except:
             socketio.emit('zigbee2mqtt_pairing',
                        {'zigbee2mqtt_pairing_status': "Status Error"},                                                               
                          namespace='/socketIO')           


@socketio.on('connect', namespace='/socketIO')
def connect_system_log():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


""" ################## """
""" update ip settings """
""" ################## """

time.sleep(1)

try:
    ip_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]["addr"]  
except:
    ip_address = ""
    
try:
    gateway = ""
    
    for element in netifaces.gateways()[2]: 
        if element[1] == "eth0":
            gateway = element[0]
        
except:
    gateway = ""
    
SET_SYSTEM_NETWORK_SETTINGS(ip_address, gateway, GET_SYSTEM_SETTINGS().port, GET_SYSTEM_SETTINGS().dhcp)


""" ################################## """
""" update zigbee device update status """
""" ################################## """

SET_ZIGBEE_DEVICE_UPDATE_STATUS("No Device Update available")

for device in GET_ALL_DEVICES(""):
    if device.update_available == "True":
        SET_ZIGBEE_DEVICE_UPDATE_STATUS("Device Update found")


""" ####### """
""" imports """
""" ####### """

from app.sites                      import index, about, dashboard, scheduler, programs, lighting_scenes, lighting_groups, cameras, music, sensordata_jobs, sensordata_statistics, settings_system, settings_threads, settings_devices, settings_controller, settings_users, settings_system_log, errors
from app.backend.process_management import PROCESS_MANAGEMENT_THREAD
from app.backend.mqtt               import START_MQTT_RECEIVE_THREAD, START_MQTT_PUBLISH_THREAD, START_MQTT_CONTROL_THREAD, CHECK_ZIGBEE2MQTT_STARTED, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.email              import SEND_EMAIL
from app.backend.process_scheduler  import GET_SUNRISE_TIME, GET_SUNSET_TIME
from app.backend.spotify            import START_REFRESH_SPOTIFY_TOKEN_THREAD


""" ######### """
""" scheduler """
""" ######### """

from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.start()   


@scheduler.task('cron', id='update_sunrise_sunset', hour='*')
def update_sunrise_sunset():
    for task in GET_ALL_SCHEDULER_TASKS():

        if task.trigger_sun_position == "True":
            if task.option_sunrise == "True" or task.option_sunset == "True":

                # get coordinates
                if task.latitude != "None" and task.latitude != None and task.longitude != "None" and task.longitude:

                    # update sunrise / sunset
                    SET_SCHEDULER_TASK_SUNRISE(task.id, GET_SUNRISE_TIME(float(task.latitude), float(task.longitude)))
                    SET_SCHEDULER_TASK_SUNSET(task.id, GET_SUNSET_TIME(float(task.latitude), float(task.longitude)))
                            

@scheduler.task('cron', id='scheduler_time', minute='*')
def scheduler_time():
    for task in GET_ALL_SCHEDULER_TASKS():
        if (task.trigger_time == "True" or task.trigger_sun_position == "True") and task.option_pause != "True":
            heapq.heappush(process_management_queue, (20, ("scheduler", task.id, "")))         
    

@scheduler.task('cron', id='scheduler_ping', second='0, 15, 30, 45')
def scheduler_ping(): 
    for task in GET_ALL_SCHEDULER_TASKS():
        if task.trigger_position == "True" and task.option_pause != "True":
            heapq.heappush(process_management_queue, (20, ("scheduler", task.id, "")))


""" #### """
""" mqtt """
""" #### """

try:
    print("###### Start MQTT ######")
    START_MQTT_RECEIVE_THREAD()
    START_MQTT_PUBLISH_THREAD()
    START_MQTT_CONTROL_THREAD()    
    START_REFRESH_MQTT_INPUT_MESSAGES_THREAD()

    time.sleep(3)    

except Exception as e:
    print("ERROR: Network | MQTT | " + str(e))
    WRITE_LOGFILE_SYSTEM("ERROR", "Network | MQTT | " + str(e)) 


""" ######## """
""" services """
""" ######## """

if GET_SYSTEM_SETTINGS().zigbee2mqtt_active == "True":

    # check mqtt connection
    if GET_MQTT_CONNECTION_STATUS() == True:  

        # check zigbee2mqtt connection      
        if CHECK_ZIGBEE2MQTT_STARTED():  
            print("Network | ZigBee2MQTT | connected") 
            
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | connected")

            START_DISABLE_ZIGBEE_PAIRING_THREAD()

            # deactivate pairing at startup
            if not CHECK_ZIGBEE2MQTT_PAIRING("False"):   

                heapq.heappush(mqtt_message_queue, (20, ("smarthome/zigbee2mqtt/bridge/config/permit_join", "false")))    

                if CHECK_ZIGBEE2MQTT_PAIRING("False"):             
                    WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("False")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled") 
                else:             
                    WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | Setting not confirmed")  
                    SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
                    SET_ZIGBEE2MQTT_PAIRING_STATUS("Setting not confirmed")

            else:
                WRITE_LOGFILE_SYSTEM("SUCCESS", "Network | ZigBee2MQTT | Pairing disabled | successful") 
                SET_ZIGBEE2MQTT_PAIRING_SETTING("False")
                SET_ZIGBEE2MQTT_PAIRING_STATUS("Disabled")     

        else:
            print("ERROR: Network | ZigBee2MQTT | No Connection") 
            
            WRITE_LOGFILE_SYSTEM("ERROR", "Network | ZigBee2MQTT | No Connection")        
            SEND_EMAIL("ERROR", "Network | ZigBee2MQTT | No Connection")  
            SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
            SET_ZIGBEE2MQTT_PAIRING_STATUS("No Zigbee2MQTT Connection")        

    else:
        WRITE_LOGFILE_SYSTEM("WARNING", "Network | ZigBee2MQTT | Pairing disabled | No MQTT connection") 
        SET_ZIGBEE2MQTT_PAIRING_SETTING("None")
        SET_ZIGBEE2MQTT_PAIRING_STATUS("No MQTT connection")                  

else:
    os.system("sudo systemctl stop zigbee2mqtt")
    WRITE_LOGFILE_SYSTEM("SUCCESS", "System | Services | ZigBee2MQTT | disabled")
    print("System | Services | ZigBee2MQTT | disabled") 


if GET_SYSTEM_SETTINGS().lms_active != "True":
    try:
        os.system("sudo systemctl stop logitechmediaserver")
        WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | Logitech Media Server | disabled")
        print("System | Services | Logitech Media Server | disabled") 
        time.sleep(1)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Logitech Media Server | " + str(e)) 
        print("ERROR: System | Services | Logitech Media Server | " + str(e)) 


if GET_SYSTEM_SETTINGS().squeezelite_active != "True":
    try:
        os.system("sudo systemctl stop squeezelite")
        WRITE_LOGFILE_SYSTEM("EVENT", "System | Services | Squeezelie Player | disabled")
        print("System | Services | Squeezelie Player | disabled") 
        time.sleep(1)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Services | Squeezelie Player | " + str(e)) 
        print("ERROR: System | Services | Squeezelie Player | " + str(e)) 


""" #################### """
""" background processes """
""" #################### """

PROCESS_MANAGEMENT_THREAD()
START_REFRESH_SPOTIFY_TOKEN_THREAD()

socketio.run(app, host = GET_SYSTEM_SETTINGS().ip_address, port = int(GET_SYSTEM_SETTINGS().port), debug=False)