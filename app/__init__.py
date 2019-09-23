from flask            import Flask
from flask_bootstrap  import Bootstrap
from flask_mail       import Mail

# load RES
from app import assets  

import time
import netifaces
import os


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY']                     = "randon"        #os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#app.config.from_object('app.configuration.ProductionConfig')
#app.config.from_object('app.configuration.DevelopmentConfig')

# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )

from app.sites                   import index, dashboard, tasks, plants, devices, users, system, system_log, errors
from app.database.models         import *


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



app.run(host = GET_HOST_NETWORK().lan_ip_address, port = 80, debug=True)