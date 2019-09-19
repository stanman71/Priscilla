from flask               import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login         import current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from functools           import wraps
from ping3               import ping

from app                 import app
from app.database.models import *
from app.common          import COMMON, STATUS
from app.assets          import *

import datetime
import os
import time
import threading


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            print(e)
            return redirect(url_for('logout'))
        
    return wrap


""" ################# """
"""  system functions """
""" ################# """

def GET_CPU_TEMPERATURE():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n"," C"))


def CHECK_IP_ADDRESS(ip_address):
    try:
        for element in ip_address:
            if not element.isdigit() and element != ".":
                return False
              
        if len(ip_address.split(".")) != 4:
            return False
        
        for element in ip_address.split("."):
            if not 0 <= int(element) <= 254:
                return False
            
        return True
    
    except:
        return False
  
  
def PING_IP_ADDRESS(ip_address):
    try:
    
        if ping(ip_address, timeout=1) != None:
            return True
        if ping(ip_address, timeout=1) != None:
            return True

        return False
    
    except:
        return False


def HOST_REBOOT():
    time.sleep(10)
    os.system("sudo shutdown -r now")


def HOST_SHUTDOWN():
    time.sleep(10)
    os.system("sudo shutdown -h now")


@app.route('/system.html', methods=['GET', 'POST'])
@login_required
@permission_required
def system():
    error_message_change_settings   = []
    success_message_change_settings = False
    
    message_shutdown         = "" 
    message_ip_config_change = False


    # ###############
    # start / restart
    # ###############             
        
    # restart raspi 
    if request.form.get("restart") != None:
        Thread = threading.Thread(target=HOST_REBOOT)
        Thread.start()    
        message_shutdown = "System wird in 10 Sekunden neugestartet"
        
    # shutdown raspi 
    if request.form.get("shutdown") != None:
        Thread = threading.Thread(target=HOST_SHUTDOWN)
        Thread.start()    
        message_shutdown = "System wird in 10 Sekunden heruntergefahren"
                

    # ################
    # network settings
    # ################    
                
    if request.form.get("change_host_settings") != None:
        
        save_input = True

        # check dhcp
        
        if request.form.get("set_lan_dhcp"):
            lan_dhcp = "checked" 
        else:
            lan_dhcp = ""            
        
        if request.form.get("set_wlan_dhcp"):
            wlan_dhcp = "checked" 
        else:
            wlan_dhcp = ""               

        lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
        lan_gateway       = GET_HOST_NETWORK().lan_gateway  
        wlan_ip_address   = GET_HOST_NETWORK().wlan_ip_address
        wlan_gateway      = GET_HOST_NETWORK().wlan_gateway 


        # no dhcp ?
        
        if lan_dhcp != "checked" or wlan_dhcp != "checked":

            # lan
        
            if lan_dhcp != "checked":
                
                if request.form.get("set_lan_ip_address") != None:
                    lan_ip_address  = request.form.get("set_lan_ip_address")
                    
                if request.form.get("set_lan_gateway") != None:
                    lan_gateway     = request.form.get("set_lan_gateway")            

                if CHECK_IP_ADDRESS(lan_ip_address) == False:
                    error_message_change_settings.append("Ungültige LAN IP-Adresse angegeben")
                    save_input = False
                
                if PING_IP_ADDRESS(lan_ip_address) == True and lan_ip_address != GET_HOST_NETWORK().lan_ip_address:
                    error_message_change_settings.append("LAN IP-Adresse bereits vergeben")
                    save_input = False
                
                if CHECK_IP_ADDRESS(lan_gateway) == False:
                    error_message_change_settings.append("Ungültiges LAN Gateway angegeben")
                    save_input = False
                    
                if CHECK_IP_ADDRESS(lan_gateway) == True and PING_IP_ADDRESS(lan_gateway) == False:
                    error_message_change_settings.append("LAN Gateway nicht gefunden")
                    save_input = False

            # wlan
            
            if wlan_dhcp != "checked":                    
                    
                if request.form.get("set_wlan_ip_address") != None:
                    wlan_ip_address  = request.form.get("set_wlan_ip_address")
                    
                if request.form.get("set_wlan_gateway") != None:
                    wlan_gateway     = request.form.get("set_wlan_gateway")   
                                            
                if CHECK_IP_ADDRESS(wlan_ip_address) == False:
                    error_message_change_settings.append("Ungültige WLAN IP-Adresse angegeben")
                    save_input = False
                
                if PING_IP_ADDRESS(wlan_ip_address) == True and wlan_ip_address != GET_HOST_NETWORK().wlan_ip_address:
                    error_message_change_settings.append("WLAN IP-Adresse bereits vergeben")
                    save_input = False
                
                if CHECK_IP_ADDRESS(wlan_gateway) == False:
                    error_message_change_settings.append("Ungültiges WLAN Gateway angegeben")
                    save_input = False

                if CHECK_IP_ADDRESS(wlan_gateway) == True and PING_IP_ADDRESS(wlan_gateway) == False:
                    error_message_change_settings.append("WLAN Gateway nicht gefunden")
                    save_input = False

            
            # lan + wlan
            
            if lan_dhcp != "checked" and wlan_dhcp != "checked":                     
                
                if lan_ip_address == "" and wlan_ip_address == "":
                    error_message_change_settings.append("Keine IP-Adresse angegeben")
                    save_input = False
                    
                if lan_ip_address == wlan_ip_address:
                    error_message_change_settings.append("Gleiche IP-Adressen (LAN + WLAN) angegeben")
                    save_input = False


        # wlan credentials              
            
        wlan_ssid       = request.form.get("set_wlan_ssid")
        wlan_password   = request.form.get("set_wlan_password")    
            
        if wlan_ssid == "" or wlan_password == "":
            error_message_change_settings.append("WLAN Zugangsdaten unvollständig")
            save_input = False                    
        
        
        # default interface
        
        default_interface = request.form.get("set_default_interface")
        
        if (default_interface == "LAN" and (lan_ip_address == "" or lan_gateway == "" or
            CHECK_IP_ADDRESS(lan_ip_address) == False or CHECK_IP_ADDRESS(lan_gateway) == False)):
            
            error_message_change_settings.append("Unvollständige Angeben LAN-Netzwerk")
            default_interface = GET_HOST_NETWORK().default_interface
            save_input = False
        
        if (default_interface == "WLAN" and (wlan_ip_address == "" or wlan_gateway == "" or
            CHECK_IP_ADDRESS(wlan_ip_address) == False or CHECK_IP_ADDRESS(wlan_gateway) == False)):
            
            error_message_change_settings.append("Unvollständige Angeben WLAN-Netzwerk")
            default_interface = GET_HOST_NETWORK().default_interface
            save_input = False


        # port
        
        port = request.form.get("set_port") 
        
        if port == "":
            error_message_change_settings.append("Keinen Port angegeben")
            save_input = False
            
        if port.isdigit() == False:
            error_message_change_settings.append("Ungültigen Port angegeben (Zahl von 0 bis 65535)")
            save_input = False
            
        if not 0 <= int(port) <= 65535:
            error_message_change_settings.append("Ungültigen Port angegeben (Zahl von 0 bis 65535)")
            save_input = False           
            
            
        # save settings  
            
        if save_input == True:
            SET_HOST_NETWORK(lan_ip_address, lan_gateway, wlan_ip_address, wlan_gateway)
            UPDATE_NETWORK_SETTINGS_FILE(lan_dhcp, lan_ip_address, lan_gateway, wlan_dhcp, wlan_ip_address, wlan_gateway)
            
            SET_WLAN_CREDENTIALS(wlan_ssid, wlan_password)
            UPDATE_WLAN_CREDENTIALS_FILE(wlan_ssid, wlan_password)
            
            SET_HOST_DHCP(lan_dhcp, wlan_dhcp)
            SET_HOST_DEFAULT_INTERFACE(default_interface)  
            SET_HOST_PORT(port)        
    
            success_message_change_settings = True
               
        
    cpu_temperature   = GET_CPU_TEMPERATURE()
 
    lan_dhcp          = GET_HOST_NETWORK().lan_dhcp
    lan_ip_address    = GET_HOST_NETWORK().lan_ip_address
    lan_gateway       = GET_HOST_NETWORK().lan_gateway
    wlan_dhcp         = GET_HOST_NETWORK().wlan_dhcp  
    wlan_ip_address   = GET_HOST_NETWORK().wlan_ip_address
    wlan_gateway      = GET_HOST_NETWORK().wlan_gateway
    wlan_ssid         = GET_HOST_NETWORK().wlan_ssid
    wlan_password     = GET_HOST_NETWORK().wlan_password    
    default_interface = GET_HOST_NETWORK().default_interface
    port              = GET_HOST_NETWORK().port       
 

    if (wlan_ssid != "" or wlan_password != "") and wlan_ip_address == "":
        error_message_change_settings.append("Falsche WLAN Zugangsdaten eingegeben")


    data = {'navigation': 'system', 'notification': ''}

    return render_template('layouts/default.html',
                            data=data,    
                            content=render_template( 'pages/system.html',   
                                                    error_message_host_settings=error_message_change_settings,
                                                    success_message_host_settings=success_message_change_settings,                                                    
                                                    message_shutdown=message_shutdown,
                                                    cpu_temperature=cpu_temperature,
                                                    lan_dhcp=lan_dhcp,
                                                    lan_ip_address=lan_ip_address,
                                                    lan_gateway=lan_gateway,
                                                    wlan_dhcp=wlan_dhcp,
                                                    wlan_ip_address=wlan_ip_address,
                                                    wlan_gateway=wlan_gateway,
                                                    wlan_ssid=wlan_ssid,
                                                    wlan_password=wlan_password,                           
                                                    default_interface=default_interface,
                                                    port=port,                                 
                                                    ) 
                            )
