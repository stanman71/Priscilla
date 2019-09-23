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

from app.sites                      import index, dashboard, tasks, plants, devices, users, system, system_log, errors
from app.database.models            import *
from app.backend.shared_resources   import process_management_queue
from app.backend.process_management import PROCESS_MANAGEMENT_THREAD
from app.backend.shared_resources   import REFRESH_MQTT_INPUT_MESSAGES_THREAD
from app.backend.mqtt               import MQTT_RECEIVE_THREAD


""" ################## """
""" update ip settings """
""" ################## """

time.sleep(1)

# lan

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

scheduler = APScheduler()
scheduler.start()   

@scheduler.task('cron', id='scheduler_tasks', minute='*')
def scheduler_tasks():
    now = datetime.datetime.now()
    current_hour   = now.strftime('%H')
    current_minute = now.strftime('%M')   

    for task in GET_ALL_SCHEDULER_TASKS():
        if (task.hour == int(current_hour) or task.hour == "*") and (task.minute == int(current_minute) or task.minute == "*"):
            heapq.heappush(process_management_queue, (20, ("scheduler", task.task)))  


""" #### """
""" mqtt """
""" #### """

try:
    print("###### Start MQTT ######")
    MQTT_RECEIVE_THREAD()

except Exception as e:
    print("ERROR: MQTT | " + str(e))
    WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e)) 


""" ################## """
""" background threads """
""" ################## """

PROCESS_MANAGEMENT_THREAD()
REFRESH_MQTT_INPUT_MESSAGES_THREAD()


app.run(host = GET_HOST_NETWORK().lan_ip_address, port = 80, debug=False)