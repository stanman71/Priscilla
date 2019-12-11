from flask             import Flask
from flask_bootstrap   import Bootstrap
from flask_mail        import Mail
from flask_apscheduler import APScheduler


from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit

# load RES
from app import assets  

import time
import netifaces
import os
import heapq
import json


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY']                     = "random"        #os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.database.models import *

# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )


""" ######### """
""" socket IO """
""" ######### """

async_mode  = None
socketio    = SocketIO(app, async_mode=async_mode)
thread      = None
thread_lock = Lock()

def background_thread_system_log():

    while True:
        socketio.sleep(5)

        selected_log_types = ["WARNING", "ERROR"]
        log_search         = ""

        # get log entries
        if GET_LOGFILE_SYSTEM(selected_log_types, 500, log_search) != None:
            data_log_system = GET_LOGFILE_SYSTEM(selected_log_types, 500, log_search)
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
                       'data_9_title': data_log_system[9][1] + " ||| " + data_log_system[9][0], 'data_9_content': data_log_system[9][2],                                           
                      },
                      namespace='/socketIO/system_log')

# system_log
@socketio.on('connect', namespace='/socketIO/system_log')
def connect_system_log():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread_system_log)




@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


""" ################## """
""" update ip settings """
""" ################## """

time.sleep(1)

try:
    lan_ip_address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]["addr"]  
except:
    lan_ip_address = ""
    
try:
    lan_gateway = ""
    
    for element in netifaces.gateways()[2]: 
        if element[1] == "eth0":
            lan_gateway = element[0]
        
except:
    lan_gateway = ""
    
UPDATE_HOST_INTERFACE_LAN(lan_ip_address, lan_gateway)


""" ####### """
""" imports """
""" ####### """

from app.sites                      import index, dashboard, scheduler, programs, plants, led_scenes, led_groups, cameras, music, sensordata_jobs, sensordata_statistics, settings_system, settings_devices, settings_controller, settings_users, settings_system_log, errors
from app.backend.shared_resources   import process_management_queue
from app.backend.process_management import PROCESS_MANAGEMENT_THREAD
from app.backend.shared_resources   import REFRESH_MQTT_INPUT_MESSAGES_THREAD
from app.backend.mqtt               import START_MQTT_RECEIVE_THREAD, START_MQTT_PUBLISH_THREAD, START_MQTT_CONTROL_THREAD, CHECK_ZIGBEE2MQTT_AT_STARTUP, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.email              import SEND_EMAIL
from app.backend.file_management    import GET_LOCATION_COORDINATES
from app.backend.process_scheduler  import GET_SUNRISE_TIME, GET_SUNSET_TIME
from app.backend.spotify            import REFRESH_SPOTIFY_TOKEN_THREAD


""" ######### """
""" scheduler """
""" ######### """

from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.start()   


@scheduler.task('cron', id='update_sunrise_sunset', hour='*')
def update_sunrise_sunset():
    for task in GET_ALL_SCHEDULER_TASKS():

        if task.option_sunrise == "True" or task.option_sunset == "True":

            # get coordinates
            coordinates = GET_LOCATION_COORDINATES(task.location)

            if coordinates != "None" and coordinates != None: 

                # update sunrise / sunset
                SET_SCHEDULER_TASK_SUNRISE(task.id, GET_SUNRISE_TIME(float(coordinates[0]), float(coordinates[1])))
                SET_SCHEDULER_TASK_SUNSET(task.id, GET_SUNSET_TIME(float(coordinates[0]), float(coordinates[1])))
                            

@scheduler.task('cron', id='scheduler_time', minute='*')
def scheduler_time():
    for task in GET_ALL_SCHEDULER_TASKS():
        if (task.option_time == "True" or task.option_sun == "True") and task.option_pause != "True":
            heapq.heappush(process_management_queue, (20, ("scheduler", "time", task.id)))         
    

@scheduler.task('cron', id='scheduler_ping', second='0, 10, 20, 30, 40, 50')
def scheduler_ping(): 
    for task in GET_ALL_SCHEDULER_TASKS():
        if task.option_position == "True" and task.option_pause != "True":
            heapq.heappush(process_management_queue, (20, ("scheduler", "ping", task.id)))


""" #### """
""" mqtt """
""" #### """

try:
    print("###### Start MQTT ######")
    START_MQTT_RECEIVE_THREAD()
    START_MQTT_PUBLISH_THREAD()
    START_MQTT_CONTROL_THREAD()    
    REFRESH_MQTT_INPUT_MESSAGES_THREAD()

    time.sleep(3)    

except Exception as e:
    print("ERROR: MQTT | " + str(e))
    WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e)) 


""" ######## """
""" services """
""" ######## """
 
if GET_SYSTEM_SERVICES().zigbee2mqtt_active == "True":

    if CHECK_ZIGBEE2MQTT_AT_STARTUP():  
        print("ZigBee2MQTT | Connected") 
        
        WRITE_LOGFILE_SYSTEM("EVENT", "ZigBee2MQTT | Connected")

        # deactivate pairing at startup
        SET_ZIGBEE2MQTT_PAIRING("False")
        
        channel = "miranda/zigbee2mqtt/bridge/config/permit_join"
        msg     = "false"

        heapq.heappush(process_management_queue, (20, ("send_mqtt_message", channel, msg)))   
        time.sleep(1)

        if CHECK_ZIGBEE2MQTT_PAIRING("false"):                        
            WRITE_LOGFILE_SYSTEM("EVENT", "ZigBee2MQTT | Pairing disabled") 
        else:             
            WRITE_LOGFILE_SYSTEM("WARNING", "ZigBee2MQTT | Pairing disabled | Setting not confirmed")    
            
    else:
        print("ERROR: ZigBee2MQTT | No connection") 
        
        WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | No Connection")        
        SEND_EMAIL("ERROR", "ZigBee2MQTT | No Connection")          

else:
    os.system("sudo systemctl stop zigbee2mqtt")
    WRITE_LOGFILE_SYSTEM("EVENT", "ZigBee2MQTT | Disabled")
    print("ZigBee2MQTT | Disabled") 


if GET_SYSTEM_SERVICES().lms_active != "True":
    try:
        os.system("sudo systemctl stop logitechmediaserver")
        WRITE_LOGFILE_SYSTEM("EVENT", "Logitech Media Server | Disabled")
        print("Logitech Media Server | Disabled") 
        time.sleep(1)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Logitech Media Server | " + str(e)) 
        print("ERROR: Logitech Media Server | " + str(e)) 


if GET_SYSTEM_SERVICES().squeezelite_active != "True":
    try:
        os.system("sudo systemctl stop squeezelite")
        WRITE_LOGFILE_SYSTEM("EVENT", "Squeezelie Player | Disabled")
        print("Squeezelie Player | Disabled") 
        time.sleep(1)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Squeezelie Player | " + str(e)) 
        print("ERROR: Squeezelie Player | " + str(e)) 


""" #################### """
""" background processes """
""" #################### """

PROCESS_MANAGEMENT_THREAD()
REFRESH_SPOTIFY_TOKEN_THREAD(3000)

socketio.run(app, host = GET_HOST_NETWORK().lan_ip_address, port = 80, debug=False)