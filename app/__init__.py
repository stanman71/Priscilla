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
app.config['SECRET_KEY']                     = os.urandom(20).hex()
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#app.config.from_object('app.configuration.ProductionConfig')
#app.config.from_object('app.configuration.DevelopmentConfig')

# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )

from app.sites                   import index, plants, devices, users, system, system_log, views, errors
from app.database.models         import *
from app.backend.file_management import READ_WLAN_CREDENTIALS_FILE


""" ################## """
""" update ip settings """
""" ################## """

time.sleep(10)

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

# wlan

try:
    wlan_ip_address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]["addr"]
except:
    wlan_ip_address = ""
    
try:
    wlan_gateway = ""
    
    for element in netifaces.gateways()[2]: 
        if element[1] == "wlan0":
            wlan_gateway = element[0]
                     
except:
    wlan_gateway = ""       

# no seperate wlan gateway 
if wlan_ip_address != "" and wlan_gateway == "":
    wlan_gateway = lan_gateway
    
UPDATE_HOST_INTERFACE_WLAN(wlan_ip_address, wlan_gateway)


# get wlan credentials
try:
    wlan_ssid     = READ_WLAN_CREDENTIALS_FILE()[0]
    wlan_password = READ_WLAN_CREDENTIALS_FILE()[1]

    UPDATE_HOST_INTERFACE_WLAN_CREDENTIALS(wlan_ssid, wlan_password)
    
except:
    pass


# check credential error
if (GET_HOST_NETWORK().wlan_ssid != "" or GET_HOST_NETWORK().wlan_password != "") and GET_HOST_NETWORK().wlan_ip_address == "":
    print("ERROR: WLAN | Wrong Credentials")
    WRITE_LOGFILE_SYSTEM("ERROR", "WLAN | Wrong Credentials")      
    #SEND_EMAIL("ERROR", "WLAN | Wrong Credentials")       

# set default interface
if GET_HOST_NETWORK().default_interface != "lan" and GET_HOST_NETWORK().default_interface != "wlan":
    UPDATE_HOST_DEFAULT_INTERFACE("lan")
          
# check default interface
if wlan_ip_address == "" and lan_ip_address != "" and GET_HOST_NETWORK().default_interface == "wlan":
    UPDATE_HOST_DEFAULT_INTERFACE("lan") 
    
if lan_ip_address == "" and wlan_ip_address != "" and GET_HOST_NETWORK().default_interface == "lan":
    UPDATE_HOST_DEFAULT_INTERFACE("wlan") 

# check port
if GET_HOST_PORT() == 5000:
    UPDATE_HOST_PORT(5000)

app.run(host = GET_HOST_DEFAULT_NETWORK(), port = GET_HOST_PORT(), debug=True)