from flask             import Flask
from flask_bootstrap   import Bootstrap
from flask_mail        import Mail
from flask_apscheduler import APScheduler


# load RES
from app import assets  

import time
import netifaces
import os
import heapq


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY']                     = "randon"        #os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )

from app.sites                      import index, dashboard, scheduler, programs, plants, led_scenes, led_groups, cameras, sensordata_jobs, sensordata_statistics, devices, settings_system, settings_controller, settings_speechcontrol, settings_users, settings_system_log, errors
from app.database.models            import *
from app.backend.shared_resources   import process_management_queue
from app.backend.process_management import PROCESS_MANAGEMENT_THREAD
from app.backend.shared_resources   import REFRESH_MQTT_INPUT_MESSAGES_THREAD
from app.backend.mqtt               import MQTT_RECEIVE_THREAD, MQTT_PUBLISH_THREAD, CHECK_ZIGBEE2MQTT, CHECK_ZIGBEE2MQTT_PAIRING
from app.backend.email              import SEND_EMAIL
from app.backend.file_management    import GET_LOCATION_COORDINATES
from app.backend.process_scheduler  import GET_SUNRISE_TIME, GET_SUNSET_TIME


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
    MQTT_RECEIVE_THREAD()
    MQTT_PUBLISH_THREAD()
    REFRESH_MQTT_INPUT_MESSAGES_THREAD()

except Exception as e:
    print("ERROR: MQTT | " + str(e))
    WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e)) 


""" ###### """
""" zigbee """
""" ###### """
 
time.sleep(3)

if CHECK_ZIGBEE2MQTT():  
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


""" ################## """
""" process management """
""" ################## """

PROCESS_MANAGEMENT_THREAD()


app.run(host = GET_HOST_NETWORK().lan_ip_address, port = 80, debug=False)