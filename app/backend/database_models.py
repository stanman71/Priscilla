from flask_sqlalchemy import SQLAlchemy
from flask_login      import UserMixin

from app                         import app
from app.backend.file_management import *
from app.common                  import COMMON, STATUS, DATATYPE

import datetime
import re

db = SQLAlchemy(app)

class Camera(db.Model):
    __tablename__   = 'camera'
    id              = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name            = db.Column(db.String(50))
    url             = db.Column(db.String(50), server_default=(""))
    user            = db.Column(db.String(50), server_default=(""))
    password        = db.Column(db.String(50), server_default=(""))   

class Controller(db.Model):
    __tablename__   = 'controller'
    id              = db.Column(db.Integer, primary_key=True, autoincrement = True)
    device_ieeeAddr = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr')) 
    device          = db.relationship('Devices') 
    command_1       = db.Column(db.String(50), server_default=("None")) 
    task_1          = db.Column(db.String(50), server_default=("None")) 
    command_2       = db.Column(db.String(50), server_default=("None")) 
    task_2          = db.Column(db.String(50), server_default=("None")) 
    command_3       = db.Column(db.String(50), server_default=("None")) 
    task_3          = db.Column(db.String(50), server_default=("None"))     
    command_4       = db.Column(db.String(50), server_default=("None")) 
    task_4          = db.Column(db.String(50), server_default=("None")) 
    command_5       = db.Column(db.String(50), server_default=("None")) 
    task_5          = db.Column(db.String(50), server_default=("None")) 
    command_6       = db.Column(db.String(50), server_default=("None")) 
    task_6          = db.Column(db.String(50), server_default=("None"))    
    command_7       = db.Column(db.String(50), server_default=("None")) 
    task_7          = db.Column(db.String(50), server_default=("None")) 
    command_8       = db.Column(db.String(50), server_default=("None")) 
    task_8          = db.Column(db.String(50), server_default=("None")) 
    command_9       = db.Column(db.String(50), server_default=("None")) 
    task_9          = db.Column(db.String(50), server_default=("None"))    
    command_10      = db.Column(db.String(50), server_default=("None")) 
    task_10         = db.Column(db.String(50), server_default=("None"))    
    command_11      = db.Column(db.String(50), server_default=("None")) 
    task_11         = db.Column(db.String(50), server_default=("None"))    
    command_12      = db.Column(db.String(50), server_default=("None")) 
    task_12         = db.Column(db.String(50), server_default=("None"))        
    command_13      = db.Column(db.String(50), server_default=("None")) 
    task_13         = db.Column(db.String(50), server_default=("None"))        
    command_14      = db.Column(db.String(50), server_default=("None")) 
    task_14         = db.Column(db.String(50), server_default=("None"))       
    command_15      = db.Column(db.String(50), server_default=("None")) 
    task_15         = db.Column(db.String(50), server_default=("None"))        
    command_16      = db.Column(db.String(50), server_default=("None")) 
    task_16         = db.Column(db.String(50), server_default=("None"))        
    command_17      = db.Column(db.String(50), server_default=("None"))
    task_17         = db.Column(db.String(50), server_default=("None"))        
    command_18      = db.Column(db.String(50), server_default=("None")) 
    task_18         = db.Column(db.String(50), server_default=("None"))        
    command_19      = db.Column(db.String(50), server_default=("None")) 
    task_19         = db.Column(db.String(50), server_default=("None"))        
    command_20      = db.Column(db.String(50), server_default=("None")) 
    task_20         = db.Column(db.String(50), server_default=("None"))        
    collapse        = db.Column(db.String(50))  
    task_errors     = db.Column(db.String(50))      

class Devices(db.Model):
    __tablename__ = 'devices'
    id                 = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name               = db.Column(db.String(50), unique=True)
    gateway            = db.Column(db.String(50)) 
    ieeeAddr           = db.Column(db.String(50), unique=True)  
    model              = db.Column(db.String(50))
    device_type        = db.Column(db.String(50))
    version            = db.Column(db.String(50))       
    description        = db.Column(db.String(200)) 
    auto_update        = db.Column(db.String(50), server_default=("False")) 
    input_values       = db.Column(db.String(200))
    input_events       = db.Column(db.String(200))
    commands           = db.Column(db.String(200))    
    commands_json      = db.Column(db.String(200))     
    last_contact       = db.Column(db.String(50))
    last_values_json   = db.Column(db.String(200))  
    last_values_string = db.Column(db.String(200)) 
    update_available   = db.Column(db.String(50), server_default=("False")) 

class Device_Exceptions(db.Model):
    __tablename__ = 'device_exceptions'
    id                            = db.Column(db.Integer, primary_key=True, autoincrement = True)
    device_ieeeAddr               = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr')) 
    device                        = db.relationship('Devices') 
    exception_option              = db.Column(db.String(50), server_default=("None")) 
    exception_command             = db.Column(db.String(50), server_default=("None"))     
    exception_sensor_ieeeAddr     = db.Column(db.String(50), server_default=("None"))   
    exception_sensor_input_values = db.Column(db.String(50), server_default=("None"))     
    exception_value_1             = db.Column(db.String(50), server_default=("None"))
    exception_value_2             = db.Column(db.String(50), server_default=("None"))
    exception_value_3             = db.Column(db.String(50), server_default=("None"))

class eMail(db.Model):
    __tablename__  = 'email'
    id             = db.Column(db.Integer, primary_key=True, autoincrement = True)
    server_address = db.Column(db.String(50))
    server_port    = db.Column(db.Integer)
    encoding       = db.Column(db.String(50))
    username       = db.Column(db.String(50))
    password       = db.Column(db.String(50)) 

class Lighting_Groups(db.Model):
    __tablename__         = 'lighting_groups'
    id                      = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                    = db.Column(db.String(50), unique = True)
    light_ieeeAddr_1        = db.Column(db.String(50), server_default=("None"))
    light_name_1            = db.Column(db.String(50), server_default=("None"))
    light_device_type_1     = db.Column(db.String(50), server_default=("None"))
    active_light_2          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_2        = db.Column(db.String(50), server_default=("None"))           
    light_name_2            = db.Column(db.String(50), server_default=("None"))
    light_device_type_2     = db.Column(db.String(50), server_default=("None"))
    active_light_3          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_3        = db.Column(db.String(50), server_default=("None"))           
    light_name_3            = db.Column(db.String(50), server_default=("None"))
    light_device_type_3     = db.Column(db.String(50), server_default=("None"))
    active_light_4          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_4        = db.Column(db.String(50), server_default=("None"))       
    light_name_4            = db.Column(db.String(50), server_default=("None"))
    light_device_type_4     = db.Column(db.String(50), server_default=("None"))
    active_light_5          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_5        = db.Column(db.String(50), server_default=("None"))         
    light_name_5            = db.Column(db.String(50), server_default=("None")) 
    light_device_type_5     = db.Column(db.String(50), server_default=("None"))
    active_light_6          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_6        = db.Column(db.String(50), server_default=("None"))
    light_name_6            = db.Column(db.String(50), server_default=("None"))
    light_device_type_6     = db.Column(db.String(50), server_default=("None"))
    active_light_7          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_7        = db.Column(db.String(50), server_default=("None"))
    light_name_7            = db.Column(db.String(50), server_default=("None"))
    light_device_type_7     = db.Column(db.String(50), server_default=("None"))
    active_light_8          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_8        = db.Column(db.String(50), server_default=("None"))
    light_name_8            = db.Column(db.String(50), server_default=("None"))
    light_device_type_8     = db.Column(db.String(50), server_default=("None"))
    active_light_9          = db.Column(db.String(50), server_default=("False"))
    light_ieeeAddr_9        = db.Column(db.String(50), server_default=("None"))
    light_name_9            = db.Column(db.String(50), server_default=("None")) 
    light_device_type_9     = db.Column(db.String(50), server_default=("None"))
    collapse                = db.Column(db.String(50))    
    current_scene           = db.Column(db.String(50), server_default=("OFF"))
    current_brightness      = db.Column(db.Integer, server_default=("0"))
    group_errors            = db.Column(db.String(50))    

class Lighting_Scenes(db.Model):
    __tablename__ = 'lighting_scenes'
    id             = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name           = db.Column(db.String(50), unique = True) 
    red_1          = db.Column(db.Integer, server_default=("255")) 
    green_1        = db.Column(db.Integer, server_default=("255")) 
    blue_1         = db.Column(db.Integer, server_default=("255")) 
    brightness_1   = db.Column(db.Integer, server_default=("255")) 
    active_light_2 = db.Column(db.String(50), server_default=("False"))
    red_2          = db.Column(db.Integer, server_default=("255")) 
    green_2        = db.Column(db.Integer, server_default=("255")) 
    blue_2         = db.Column(db.Integer, server_default=("255")) 
    brightness_2   = db.Column(db.Integer, server_default=("255"))     
    active_light_3 = db.Column(db.String(50), server_default=("False"))
    red_3          = db.Column(db.Integer, server_default=("255")) 
    green_3        = db.Column(db.Integer, server_default=("255")) 
    blue_3         = db.Column(db.Integer, server_default=("255")) 
    brightness_3   = db.Column(db.Integer, server_default=("255")) 
    active_light_4 = db.Column(db.String(50), server_default=("False"))
    red_4          = db.Column(db.Integer, server_default=("255")) 
    green_4        = db.Column(db.Integer, server_default=("255")) 
    blue_4         = db.Column(db.Integer, server_default=("255")) 
    brightness_4   = db.Column(db.Integer, server_default=("255")) 
    active_light_5 = db.Column(db.String(50), server_default=("False"))
    red_5          = db.Column(db.Integer, server_default=("255")) 
    green_5        = db.Column(db.Integer, server_default=("255")) 
    blue_5         = db.Column(db.Integer, server_default=("255")) 
    brightness_5   = db.Column(db.Integer, server_default=("255")) 
    active_light_6 = db.Column(db.String(50), server_default=("False"))
    red_6          = db.Column(db.Integer, server_default=("255")) 
    green_6        = db.Column(db.Integer, server_default=("255")) 
    blue_6         = db.Column(db.Integer, server_default=("255")) 
    brightness_6   = db.Column(db.Integer, server_default=("255")) 
    active_light_7 = db.Column(db.String(50), server_default=("False"))
    red_7          = db.Column(db.Integer, server_default=("255")) 
    green_7        = db.Column(db.Integer, server_default=("255")) 
    blue_7         = db.Column(db.Integer, server_default=("255")) 
    brightness_7   = db.Column(db.Integer, server_default=("255")) 
    active_light_8 = db.Column(db.String(50), server_default=("False"))
    red_8          = db.Column(db.Integer, server_default=("255")) 
    green_8        = db.Column(db.Integer, server_default=("255")) 
    blue_8         = db.Column(db.Integer, server_default=("255")) 
    brightness_8   = db.Column(db.Integer, server_default=("255")) 
    active_light_9 = db.Column(db.String(50), server_default=("False"))
    red_9          = db.Column(db.Integer, server_default=("255")) 
    green_9        = db.Column(db.Integer, server_default=("255")) 
    blue_9         = db.Column(db.Integer, server_default=("255")) 
    brightness_9   = db.Column(db.Integer, server_default=("255")) 
    collapse       = db.Column(db.String(50))        

class Programs(db.Model):
    __tablename__ = 'programs'
    id                = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name              = db.Column(db.String(50), unique = True)
    line_active_1     = db.Column(db.String(50), server_default=("True"))
    line_content_1    = db.Column(db.String(50), server_default=(""))
    line_active_2     = db.Column(db.String(50), server_default=(""))
    line_content_2    = db.Column(db.String(50), server_default=(""))
    line_active_3     = db.Column(db.String(50), server_default=(""))
    line_content_3    = db.Column(db.String(50), server_default=(""))
    line_active_4     = db.Column(db.String(50), server_default=(""))
    line_content_4    = db.Column(db.String(50), server_default=(""))
    line_active_5     = db.Column(db.String(50), server_default=(""))
    line_content_5    = db.Column(db.String(50), server_default=(""))
    line_active_6     = db.Column(db.String(50), server_default=(""))
    line_content_6    = db.Column(db.String(50), server_default=(""))
    line_active_7     = db.Column(db.String(50), server_default=(""))
    line_content_7    = db.Column(db.String(50), server_default=(""))
    line_active_8     = db.Column(db.String(50), server_default=(""))
    line_content_8    = db.Column(db.String(50), server_default=(""))
    line_active_9     = db.Column(db.String(50), server_default=(""))
    line_content_9    = db.Column(db.String(50), server_default=(""))
    line_active_10    = db.Column(db.String(50), server_default=(""))
    line_content_10   = db.Column(db.String(50), server_default=(""))
    line_active_11    = db.Column(db.String(50), server_default=(""))
    line_content_11   = db.Column(db.String(50), server_default=(""))
    line_active_12    = db.Column(db.String(50), server_default=(""))
    line_content_12   = db.Column(db.String(50), server_default=(""))
    line_active_13    = db.Column(db.String(50), server_default=(""))
    line_content_13   = db.Column(db.String(50), server_default=(""))
    line_active_14    = db.Column(db.String(50), server_default=(""))
    line_content_14   = db.Column(db.String(50), server_default=(""))
    line_active_15    = db.Column(db.String(50), server_default=(""))
    line_content_15   = db.Column(db.String(50), server_default=(""))
    line_active_16    = db.Column(db.String(50), server_default=(""))
    line_content_16   = db.Column(db.String(50), server_default=(""))
    line_active_17    = db.Column(db.String(50), server_default=(""))
    line_content_17   = db.Column(db.String(50), server_default=(""))
    line_active_18    = db.Column(db.String(50), server_default=(""))
    line_content_18   = db.Column(db.String(50), server_default=(""))
    line_active_19    = db.Column(db.String(50), server_default=(""))
    line_content_19   = db.Column(db.String(50), server_default=(""))
    line_active_20    = db.Column(db.String(50), server_default=(""))
    line_content_20   = db.Column(db.String(50), server_default=(""))
    line_active_21    = db.Column(db.String(50), server_default=(""))
    line_content_21   = db.Column(db.String(50), server_default=(""))
    line_active_22    = db.Column(db.String(50), server_default=(""))
    line_content_22   = db.Column(db.String(50), server_default=(""))
    line_active_23    = db.Column(db.String(50), server_default=(""))
    line_content_23   = db.Column(db.String(50), server_default=(""))
    line_active_24    = db.Column(db.String(50), server_default=(""))
    line_content_24   = db.Column(db.String(50), server_default=(""))
    line_active_25    = db.Column(db.String(50), server_default=(""))
    line_content_25   = db.Column(db.String(50), server_default=(""))
    line_active_26    = db.Column(db.String(50), server_default=(""))
    line_content_26   = db.Column(db.String(50), server_default=(""))
    line_active_27    = db.Column(db.String(50), server_default=(""))
    line_content_27   = db.Column(db.String(50), server_default=(""))
    line_active_28    = db.Column(db.String(50), server_default=(""))
    line_content_28   = db.Column(db.String(50), server_default=(""))
    line_active_29    = db.Column(db.String(50), server_default=(""))
    line_content_29   = db.Column(db.String(50), server_default=(""))
    line_active_30    = db.Column(db.String(50), server_default=(""))
    line_content_30   = db.Column(db.String(50), server_default=(""))    

class Scheduler_Tasks(db.Model):
    __tablename__ = 'scheduler_tasks'
    id                          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                        = db.Column(db.String(50), unique=True)
    task                        = db.Column(db.String(50))
    visible                     = db.Column(db.String(50))    
    trigger_time                = db.Column(db.String(50), server_default=("False"))  
    trigger_sun_position        = db.Column(db.String(50), server_default=("False")) 
    trigger_sensors             = db.Column(db.String(50), server_default=("False")) 
    trigger_position            = db.Column(db.String(50), server_default=("False")) 
    option_repeat               = db.Column(db.String(50), server_default=("False")) 
    option_pause                = db.Column(db.String(50), server_default=("False")) 
    day                         = db.Column(db.String(50), server_default=("None")) 
    hour                        = db.Column(db.String(50), server_default=("None")) 
    minute                      = db.Column(db.String(50), server_default=("None")) 
    option_sunrise              = db.Column(db.String(50), server_default=("False")) 
    option_sunset               = db.Column(db.String(50), server_default=("False")) 
    latitude                    = db.Column(db.String(50), server_default=("None")) 
    longitude                   = db.Column(db.String(50), server_default=("None"))    
    sunrise                     = db.Column(db.String(50), server_default=("None")) 
    sunset                      = db.Column(db.String(50), server_default=("None"))     
    device_ieeeAddr_1           = db.Column(db.String(50), server_default=("None")) 
    device_name_1               = db.Column(db.String(50), server_default=("None")) 
    device_input_values_1       = db.Column(db.String(50), server_default=("None")) 
    sensor_key_1                = db.Column(db.String(50), server_default=("None")) 
    value_1                     = db.Column(db.String(50), server_default=("None")) 
    operator_1                  = db.Column(db.String(50), server_default=("None")) 
    main_operator_second_sensor = db.Column(db.String(50), server_default=("None"))
    device_ieeeAddr_2           = db.Column(db.String(50), server_default=("None")) 
    device_name_2               = db.Column(db.String(50), server_default=("None")) 
    device_input_values_2       = db.Column(db.String(50), server_default=("None")) 
    sensor_key_2                = db.Column(db.String(50), server_default=("None")) 
    value_2                     = db.Column(db.String(50), server_default=("None")) 
    operator_2                  = db.Column(db.String(50), server_default=("None")) 
    option_home                 = db.Column(db.String(50), server_default=("None")) 
    option_away                 = db.Column(db.String(50), server_default=("None")) 
    ip_addresses                = db.Column(db.String(50), server_default=("None")) 
    collapse                    = db.Column(db.String(50)) 
    task_errors                 = db.Column(db.String(50)) 
    task_setting_errors         = db.Column(db.String(50))     

class Sensordata_Jobs(db.Model):
    __tablename__  = 'sensordata_jobs'
    id              = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name            = db.Column(db.String(50), unique=True)
    filename        = db.Column(db.String(50), server_default=(""))
    device_ieeeAddr = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr'))  
    device          = db.relationship('Devices')  
    sensor_key      = db.Column(db.String(50)) 
    always_active   = db.Column(db.String(50), server_default=("True"))

class Spotify_Settings(db.Model):
    __tablename__ = 'spotify_settings'
    id                    = db.Column(db.Integer, primary_key=True, autoincrement = True)
    client_id             = db.Column(db.String(50), server_default=("120de7bdb90e4c139546f0f55919f8c0"))
    client_secret         = db.Column(db.String(50), server_default=("8454b2fcaf134dff99e582507f0ad428"))   
    refresh_token         = db.Column(db.String(50), server_default=(""))   
    default_device_id     = db.Column(db.String(50))   
    default_device_name   = db.Column(db.String(50))       
    default_playlist_uri  = db.Column(db.String(50))   
    default_playlist_name = db.Column(db.String(50))   
    default_volume        = db.Column(db.Integer, server_default=("0"))
    default_shuffle       = db.Column(db.String(50), server_default=("False"))   

class System(db.Model):
    __tablename__ = 'system'
    id                 = db.Column(db.Integer, primary_key=True, autoincrement = True)   
    ip_address         = db.Column(db.String(50))
    gateway            = db.Column(db.String(50))
    port               = db.Column(db.String(50), server_default=("80"))    
    dhcp               = db.Column(db.String(50), server_default=("True"))     
    zigbee2mqtt_active = db.Column(db.String(50), server_default=("False"))
    lms_active         = db.Column(db.String(50), server_default=("False"))   
    squeezelite_active = db.Column(db.String(50), server_default=("False"))   

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id                 = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name               = db.Column(db.String(64), unique = True)
    email              = db.Column(db.String(120), unique = True, server_default=(""))
    role               = db.Column(db.String(50), server_default=("user"))   
    password           = db.Column(db.String(100), server_default=(""))
    email_notification = db.Column(db.String(20), server_default=("False"))


""" ################################ """
""" ################################ """
""" create tables and default values """
""" ################################ """
""" ################################ """


# create all database tables
db.create_all()

# #####
# email
# #####

if eMail.query.filter_by().first() == None:
    email = eMail(
        id = 1,
    )
    db.session.add(email)
    db.session.commit()
   
# ###############
# scheduler tasks
# ###############

update_devices_found  = False
backup_database_found = False
reset_log_files_found = False
reset_system_found    = False

for task in Scheduler_Tasks.query.all():
    if task.name.lower() == "update_devices":
        update_devices_found = True
    if task.name.lower() == "backup_database":
        backup_database_found = True
    if task.name.lower() == "reset_log_files":
        reset_log_files_found = True
    if task.name.lower() == "reset_system":
        reset_system_found = True

if update_devices_found == False:
    scheduler_task_update_devices = Scheduler_Tasks(
        name           = "update_devices",
        task           = "update_devices",
        visible        = "False",
        trigger_time   = "True",
        option_repeat  = "True",
        day            = "*",        
        hour           = "00",
        minute         = "00",       
    )
    db.session.add(scheduler_task_update_devices)
    db.session.commit()

if backup_database_found == False:
    scheduler_task_backup_database = Scheduler_Tasks(
        name          = "backup_database",
        task          = "backup_database",
        visible       = "False",        
        trigger_time  = "True",
        option_repeat = "True",
        day           = "*",        
        hour          = "00",
        minute        = "15",        
    )
    db.session.add(scheduler_task_backup_database)
    db.session.commit()
    
if reset_log_files_found == False:
    scheduler_task_reset_log_files = Scheduler_Tasks(
        name          = "reset_log_files",
        task          = "reset_log_files",
        visible       = "False",        
        trigger_time  = "True",
        option_repeat = "True",
        day           = "*",        
        hour          = "00",
        minute        = "30",        
    )
    db.session.add(scheduler_task_reset_log_files)
    db.session.commit()

if reset_system_found == False:
    scheduler_task_reset_system = Scheduler_Tasks(
        name          = "reset_system",
        task          = "reset_system",
        visible       = "False",        
        trigger_time  = "True",
        option_repeat = "True",
        day           = "*",        
        hour          = "05",
        minute        = "00",        
    )
    db.session.add(scheduler_task_reset_system)
    db.session.commit()

# #######
# spotify
# #######

if Spotify_Settings.query.filter_by().first() == None:
    spotify_settings = Spotify_Settings(
        id = 1,
    )
    db.session.add(spotify_settings)
    db.session.commit()

# ######
# system 
# ######

if System.query.filter_by().first() == None:
    system = System(
        id = 1,
    )
    db.session.add(system)
    db.session.commit()

# ####
# user
# ####

if User.query.filter_by(name='admin').first() is None:
    user = User(
        id                 = 1,
        name               = "admin",
        email              = "admin@example.com",
        role               = "administrator",
        password           = "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339",    
        email_notification = "True"
    )           
    db.session.add(user)
    db.session.commit()


""" ################## """
""" ################## """
"""       Cameras      """
""" ################## """
""" ################## """


def GET_CAMERA_BY_ID(id):
    return Camera.query.filter_by(id=id).first()
    
    
def GET_CAMERA_BY_NAME(name):
    return Camera.query.filter_by(name=name).first()
    

def GET_CAMERA_BY_URL(url):
    return Camera.query.filter_by(url=url).first()

    
def GET_ALL_CAMERAS():   
    return Camera.query.all()
        

def ADD_CAMERA():
    for i in range(1,7):
        if Camera.query.filter_by(id=i).first():
            pass
        else:
            # add the new camera
            camera = Camera(
                    id       = i,
                    name     = "new_camera_" + str(i),                            
                )
            db.session.add(camera)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Camera - " + "new_camera_" + str(i) + " | added")               
            return True
            
    return "Limit reached (6)"


def SET_CAMERA_SETTINGS(id, name, url, user, password):         
    entry         = Camera.query.filter_by(id=id).first()
    previous_name = entry.name

    # values changed ?
    if (entry.name != name or entry.url != url or entry.user != user or entry.password != password):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + str(entry.name) + " >>> " + str(name)
        if entry.url != url:
            changes = changes + " || url || " + str(entry.url) + " >>> " + str(url)            
        if entry.user != user:
            changes = changes + " || user || " + str(entry.user) + " >>> " + str(user)        
        if entry.password != password:
            changes = changes + " || password || " + str(entry.password) + " >>> " + str(password)       

        entry.name     = name
        entry.url      = url
        entry.user     = user     
        entry.password = password                       
        db.session.commit()  
   
        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Camera - " + str(previous_name) + " | changed" + changes)

        return True


def CHANGE_CAMERA_POSITION(id, direction): 
    if direction == "up":
        camera_list = GET_ALL_CAMERAS()
        camera_list = camera_list[::-1]
        
        for camera in camera_list:
            
            if camera.id < id:  
                new_id = camera.id
                
                # change ids
                camera_1 = GET_CAMERA_BY_ID(id)
                camera_2 = GET_CAMERA_BY_ID(new_id)
                
                camera_1.id = 99
                db.session.commit()
                
                camera_2.id = id
                camera_1.id = new_id
                db.session.commit()    
                return 

    if direction == "down":
        for camera in GET_ALL_CAMERAS():
            if camera.id > id:    
                new_id = camera.id
                
                # change ids
                camera_1 = GET_CAMERA_BY_ID(id)
                camera_2 = GET_CAMERA_BY_ID(new_id)
                
                camera_1.id = 99
                db.session.commit()
                
                camera_2.id = id
                camera_1.id = new_id
                db.session.commit()    
                return 


def DELETE_CAMERA(id):
    camera_name = GET_CAMERA_BY_ID(id).name

    Camera.query.filter_by(id=id).delete()
    db.session.commit() 
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Camera - " + str(camera_name) + " | deleted")   
    return True


""" ################## """
""" ################## """
"""     Controller     """
""" ################## """
""" ################## """


def GET_CONTROLLER_BY_ID(id):
    return Controller.query.filter_by(id=id).first()
    
    
def GET_CONTROLLER_BY_IEEEADDR(device_ieeeAddr):
    return Controller.query.filter_by(device_ieeeAddr=device_ieeeAddr).first()
    
    
def GET_ALL_CONTROLLER():   
    return Controller.query.all()
        

def ADD_CONTROLLER(device_ieeeAddr):

    # controller exist ?
    if not GET_CONTROLLER_BY_IEEEADDR(device_ieeeAddr):
        
        # find a unused id
        for i in range(1,21):
            if Controller.query.filter_by(id=i).first():
                pass
            else:
                # add new controller
                controller = Controller(
                                        id              = i,
                                        device_ieeeAddr = device_ieeeAddr,
                                        )
                db.session.add(controller)
                db.session.commit()
                
                UPDATE_CONTROLLER_EVENTS()
                return True


def UPDATE_CONTROLLER_EVENTS(): 
    for controller in GET_ALL_CONTROLLER():
    
        device_input_events = GET_DEVICE_BY_IEEEADDR(controller.device_ieeeAddr).input_events
        device_input_events = device_input_events.split(",")

        try:
            controller.command_1 = device_input_events[0]
        except:
            controller.command_1 = "None"
        try:
            controller.command_2 = device_input_events[1]
        except:
            controller.command_2 = "None"
        try:
            controller.command_3 = device_input_events[2]
        except:
            controller.command_3 = "None"
        try:
            controller.command_4 = device_input_events[3]
        except:
            controller.command_4 = "None"
        try:
            controller.command_5 = device_input_events[4]
        except:
            controller.command_5 = "None"
        try:
            controller.command_6 = device_input_events[5]
        except:
            controller.command_6 = "None"            
        try:
            controller.command_7 = device_input_events[6]
        except:
            controller.command_7 = "None"
        try:
            controller.command_8 = device_input_events[7]
        except:
            controller.command_8 = "None"
        try:
            controller.command_9 = device_input_events[8]
        except:
            controller.command_9 = "None"      
        try:
            controller.command_10 = device_input_events[9]
        except:
            controller.command_10 = "None"      
        try:
            controller.command_11 = device_input_events[10]
        except:
            controller.command_11 = "None"      
        try:
            controller.command_12 = device_input_events[11]
        except:
            controller.command_12 = "None"      
        try:
            controller.command_13 = device_input_events[12]
        except:
            controller.command_13 = "None"      
        try:
            controller.command_14 = device_input_events[13]
        except:
            controller.command_14 = "None"      
        try:
            controller.command_15 = device_input_events[14]
        except:
            controller.command_15 = "None"      
        try:
            controller.command_16 = device_input_events[15]
        except:
            controller.command_16 = "None"      
        try:
            controller.command_17 = device_input_events[16]
        except:
            controller.command_17 = "None"      
        try:
            controller.command_18 = device_input_events[17]
        except:
            controller.command_18 = "None"      
        try:
            controller.command_19 = device_input_events[18]
        except:
            controller.command_19 = "None"      
        try:
            controller.command_20 = device_input_events[19]
        except:
            controller.command_20 = "None"      

        db.session.commit()


def SET_CONTROLLER_COLLAPSE_OPEN(id):
    list_controller = Controller.query.all()
    
    for controller in list_controller:
        controller.collapse = ""
        db.session.commit()   
  
    entry = Controller.query.filter_by(id=id).first()
    
    entry.collapse = "True"
    db.session.commit()   


def RESET_CONTROLLER_COLLAPSE():
    list_controller = Controller.query.all()
    
    for controller in list_controller:
        controller.collapse = ""
        db.session.commit()   


def SET_CONTROLLER_TASKS(id, task_1  = "", task_2  = "", task_3  = "", task_4  = "", task_5  = "", task_6  = "", 
                             task_7  = "", task_8  = "", task_9  = "", task_10 = "", task_11 = "", task_12 = "",
                             task_13 = "", task_14 = "", task_15 = "", task_16 = "", task_17 = "", task_18 = "",          
                             task_19 = "", task_20 = ""):  

    entry = Controller.query.filter_by(id=id).first()

    if (entry.task_1  != task_1  or entry.task_2  != task_2  or entry.task_3  != task_3  or entry.task_4  != task_4  or entry.task_5  != task_5  or 
        entry.task_6  != task_6  or entry.task_7  != task_7  or entry.task_8  != task_8  or entry.task_9  != task_9  or entry.task_10 != task_10 or 
        entry.task_11 != task_11 or entry.task_12 != task_12 or entry.task_13 != task_13 or entry.task_14 != task_14 or entry.task_15 != task_15 or 
        entry.task_16 != task_16 or entry.task_17 != task_17 or entry.task_18 != task_18 or entry.task_19 != task_19 or entry.task_20 != task_20):

        changes = ""

        if entry.task_1 != task_1:
            changes = changes + " || task_1 || " + str(entry.task_1) + " >>> " + str(task_1)
        if entry.task_2 != task_2:
            changes = changes + " || task_2 || " + str(entry.task_2) + " >>> " + str(task_2)            
        if entry.task_3 != task_3:
            changes = changes + " || task_3 || " + str(entry.task_3) + " >>> " + str(task_3)        
        if entry.task_4 != task_4:
            changes = changes + " || task_4 || " + str(entry.task_4) + " >>> " + str(task_4)       
        if entry.task_5 != task_5:
            changes = changes + " || task_5 || " + str(entry.task_5) + " >>> " + str(task_5)
        if entry.task_6 != task_6:
            changes = changes + " || task_6 || " + str(entry.task_6) + " >>> " + str(task_6)            
        if entry.task_7 != task_7:
            changes = changes + " || task_7 || " + str(entry.task_7) + " >>> " + str(task_7)        
        if entry.task_8 != task_8:
            changes = changes + " || task_8 || " + str(entry.task_8) + " >>> " + str(task_8)       
        if entry.task_9 != task_9:
            changes = changes + " || task_9 || " + str(entry.task_9) + " >>> " + str(task_9)
        if entry.task_10 != task_10:
            changes = changes + " || task_10 || " + str(entry.task_10) + " >>> " + str(task_10)            
        if entry.task_11 != task_11:
            changes = changes + " || task_11 || " + str(entry.task_11) + " >>> " + str(task_11)        
        if entry.task_12 != task_12:
            changes = changes + " || task_12 || " + str(entry.task_12) + " >>> " + str(task_12)       
        if entry.task_13 != task_13:
            changes = changes + " || task_13 || " + str(entry.task_13) + " >>> " + str(task_13)
        if entry.task_14 != task_14:
            changes = changes + " || task_14 || " + str(entry.task_14) + " >>> " + str(task_14)            
        if entry.task_15 != task_15:
            changes = changes + " || task_15 || " + str(entry.task_15) + " >>> " + str(task_15)        
        if entry.task_16 != task_16:
            changes = changes + " || task_16 || " + str(entry.task_16) + " >>> " + str(task_16)       
        if entry.task_17 != task_17:
            changes = changes + " || task_17 || " + str(entry.task_17) + " >>> " + str(task_17)
        if entry.task_18 != task_18:
            changes = changes + " || task_18 || " + str(entry.task_18) + " >>> " + str(task_18)            
        if entry.task_19 != task_19:
            changes = changes + " || task_19 || " + str(entry.task_19) + " >>> " + str(task_19)        
        if entry.task_20 != task_20:
            changes = changes + " || task_20 || " + str(entry.task_20) + " >>> " + str(task_20)       

        entry.task_1  = task_1
        entry.task_2  = task_2
        entry.task_3  = task_3   
        entry.task_4  = task_4
        entry.task_5  = task_5
        entry.task_6  = task_6     
        entry.task_7  = task_7
        entry.task_8  = task_8
        entry.task_9  = task_9    
        entry.task_10 = task_10              
        entry.task_11 = task_11      
        entry.task_12 = task_12    
        entry.task_13 = task_13   
        entry.task_14 = task_14   
        entry.task_15 = task_15   
        entry.task_16 = task_16   
        entry.task_17 = task_17   
        entry.task_18 = task_18   
        entry.task_19 = task_19   
        entry.task_20 = task_20     
        
        db.session.commit() 

        controller_name = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr).name

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Controller - " + str(controller_name) + " | changed" + changes)  
        return True


def SET_CONTROLLER_TASK_ERRORS(id, task_errors):
    entry = Controller.query.filter_by(id=id).first()

    if entry.task_errors != task_errors:
        entry.task_errors = task_errors       
        db.session.commit()     


def CHANGE_CONTROLLER_POSITION(id, direction):
    if direction == "up":
        controller_list = GET_ALL_CONTROLLER()
        controller_list = controller_list[::-1]
        
        for controller in controller_list:
            
            if controller.id < id:     
                new_id = controller.id
                
                # change ids
                controller_1 = GET_CONTROLLER_BY_ID(id)
                controller_2 = GET_CONTROLLER_BY_ID(new_id)
                
                controller_1.id = 99
                db.session.commit()
                
                controller_2.id = id
                controller_1.id = new_id
                db.session.commit()     
                return 

    if direction == "down":
        for controller in GET_ALL_CONTROLLER():
            if controller.id > id:       
                new_id = controller.id
                
                # change ids
                controller_1 = GET_CONTROLLER_BY_ID(id)
                controller_2 = GET_CONTROLLER_BY_ID(new_id)
                
                controller_1.id = 99
                db.session.commit()
                
                controller_2.id = id
                controller_1.id = new_id
                db.session.commit()     
                return 


def DELETE_CONTROLLER(device_ieeeAddr):
    Controller.query.filter_by(device_ieeeAddr=device_ieeeAddr).delete()
    db.session.commit()


""" ################### """
""" ################### """
"""       devices       """
""" ################### """
""" ################### """


def GET_DEVICE_BY_ID(id):
    return Devices.query.filter_by(id=id).first()


def GET_DEVICE_BY_NAME(name):
    for device in Devices.query.all():
        
        if device.name.lower() == name.lower():
            return device 
    
    
def GET_DEVICE_BY_IEEEADDR(ieeeAddr):
    return Devices.query.filter_by(ieeeAddr=ieeeAddr).first()   


def GET_ALL_DEVICES(selector):
    device_list = []
    devices     = Devices.query.all()
  
    if selector == "":
        for device in devices:      
            device_list.append(device)     

    if selector == "mqtt":
        for device in devices:   
            if device.gateway == "mqtt":               
                device_list.append(device)     

    if selector == "controller":
        for device in devices:
            if device.device_type == "controller":        
                device_list.append(device)      
 
    if selector == "devices":
        for device in devices:
            if (device.device_type == "power_switch" or
                device.device_type == "blind" or
                device.device_type == "vacuum_cleaner" or                
                device.device_type == "heater_thermostat" or
                device.device_type == "aromatic_diffuser" or 
                device.device_type == "engine_module" or 
                device.device_type == "relais_module"):
                
                device_list.append(device)      

    if selector == "light":
        for device in devices:
            if (device.device_type == "led_rgb" or 
                device.device_type == "led_simple"):
                    
                device_list.append(device)    

    if selector == "client_music":
        for device in devices:
            if (device.device_type == "client_music"):        
                device_list.append(device)        

    if selector == "sensors":
        for device in devices:     
            if (device.device_type == "sensor_passiv" or 
                device.device_type == "sensor_active" or
                device.device_type == "heater_thermostat"):
                
                device_list.append(device)   
 
    return device_list    
        

def ADD_DEVICE(name, gateway, ieeeAddr, model = "", device_type = "", version = "", description = "", 
               input_values = "", input_events = "", commands = "", commands_json = "", last_contact = ""):
        
    # path exist ?
    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):   
            
        # find a unused id
        for i in range(1,100):
            
            if Devices.query.filter_by(id=i).first():
                pass
                
            else:
                # add the new device            
                device = Devices(
                        id               = i,
                        name             = name,
                        gateway          = gateway,                    
                        ieeeAddr         = ieeeAddr,
                        model            = model,
                        device_type      = device_type,
                        version          = version,
                        description      = description,
                        input_values     = str(input_values),
                        input_events     = str(input_events),
                        commands         = str(commands),   
                        commands_json    = str(commands_json),                                           
                        last_contact     = last_contact,
                        )
                        
                db.session.add(device)
                db.session.commit()
                
                SET_DEVICE_LAST_CONTACT(ieeeAddr)   

                if device_type == "controller":
                    ADD_CONTROLLER(ieeeAddr)

                WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(name) + " | added")     
                
                return True

        return "Limit reached (99)"                           
                
    else:
        SET_DEVICE_LAST_CONTACT(ieeeAddr)  


def SET_DEVICE_NAME(ieeeAddr, name):
    entry         = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    previous_name = entry.name

    # values changed ?
    if entry.name != name:    

        entry.name = name    
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(previous_name) + " | changed || name || " + str(previous_name) + " >>> " + str(entry.name))


def SET_DEVICE_AUTO_UPDATE(ieeeAddr, auto_update):
    entry            = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    previous_setting = entry.auto_update

    # values changed ?
    if entry.auto_update != auto_update:    

        entry.auto_update = auto_update        
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(entry.name) + " | changed || auto_update || " + str(previous_setting) + " >>> " + str(entry.auto_update))


def SET_DEVICE_LAST_CONTACT(ieeeAddr):
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.last_contact = timestamp
    db.session.commit()       


def SAVE_DEVICE_LAST_VALUES(ieeeAddr, last_values):
 
    try:
        entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
        
        last_values_string = last_values.replace("{","")
        last_values_string = last_values_string.replace("}","")
        last_values_string = last_values_string.replace('"',"")
        last_values_string = last_values_string.replace(":",": ")
        last_values_string = last_values_string.replace(",",", ")

        # manage device updates
        if "update_available: true" in last_values_string:
            last_values_string = last_values_string.replace(", update_available: true","")

        if "update_available: false" in last_values_string:
            last_values_string = last_values_string.replace(", update_available: false","")

        # special case eurotronic heater_thermostat >>> reduce string statement 
        if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "SPZB0001":

            last_values_string_modified = ""

            for element in last_values_string.split(","):
                if "local_temperature" in element:
                    last_values_string_modified = last_values_string_modified + element + ", "
                if "current_heating_setpoint" in element:
                    last_values_string_modified = last_values_string_modified + element + ", "                   
                if "system_mode" in element and "eurotronic" not in element:
                    last_values_string_modified = last_values_string_modified + element + ", "
                if "eurotronic_error_status" in element:
                    last_values_string_modified = last_values_string_modified + element + ", "

            try:
                # change battery_level scale to max_value = 100
                data          = json.loads(last_values) 
                battery_value = int(int(data['battery']) * 4) 

                if battery_value > 100:
                    battery_value = 100

                last_values_string = last_values_string_modified + "battery: " + str(battery_value)

            except:
                last_values_string = last_values_string_modified

        # special case roborock s50 >>> ignore attributes messages
        if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "roborock_s50":
            if "cleanTime" in last_values_string:
                return

        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        entry.last_values_json   = last_values
        entry.last_values_string = last_values_string
        entry.last_contact       = timestamp
        db.session.commit()   
    
    except:
        pass


def UPDATE_DEVICE(id, name, gateway, model, device_type = "", version = "", description = "", input_values = "", input_events = "", commands = "", commands_json = ""):
    entry = Devices.query.filter_by(id=id).first()

    # values changed ?
    if (entry.name != name or entry.model != model or entry.device_type != device_type or entry.version != version or entry.description != description or
        entry.input_values != input_values or entry.input_events != input_events or entry.commands != commands or entry.commands_json != commands_json):
        
        entry.name          = name
        entry.model         = model
        entry.device_type   = device_type
        entry.version       = version        
        entry.description   = description
        entry.input_values  = str(input_values)
        entry.input_events  = str(input_events)
        entry.commands      = str(commands)   
        entry.commands_json = str(commands_json)               
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(entry.name) + " | updated")
   
        if device_type == "controller":
            ADD_CONTROLLER(GET_DEVICE_BY_ID(id).ieeeAddr)
            UPDATE_CONTROLLER_EVENTS()


def UPDATE_DEVICE_EXCEPTION_SENSOR_NAMES():

    try:
        for device in GET_ALL_DEVICES("device"):
            
            if device.exception_sensor_ieeeAddr != "None":
                device.exception_option = GET_DEVICE_BY_IEEEADDR(device.exception_sensor_ieeeAddr).name
            
        db.session.commit()
        
    except:
        pass


def UPDATE_MQTT_DEVICE_VERSION(ieeeAddr, version):
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.version = version
    db.session.commit()    
    

def SET_ZIGBEE_DEVICE_UPDATE_AVAILABLE(ieeeAddr, update_available):
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.update_available = update_available
    db.session.commit()       

    
def CHANGE_DEVICE_POSITION(id, direction):
    if direction == "up":
        device_list = GET_ALL_DEVICES("")
        device_list = device_list[::-1]
        
        for device in device_list:
            
            if device.id < id:
                
                new_id = device.id
                
                # change ids
                device_1 = GET_DEVICE_BY_ID(id)
                device_2 = GET_DEVICE_BY_ID(new_id)
                
                device_1.id = 111
                db.session.commit()
                
                device_2.id = id
                device_1.id = new_id
                db.session.commit()       
                return 

    if direction == "down":
        for device in GET_ALL_DEVICES(""):
            if device.id > id:
                
                new_id = device.id
                
                # change ids
                device_1 = GET_DEVICE_BY_ID(id)
                device_2 = GET_DEVICE_BY_ID(new_id)
                
                device_1.id = 111
                db.session.commit()
                
                device_2.id = id
                device_1.id = new_id
                db.session.commit()           
                return 


def DELETE_DEVICE(ieeeAddr):
    error_list = ""

    # check scheduler sensor
    entries = GET_ALL_SCHEDULER_TASKS()
    for entry in entries:
        if (entry.device_ieeeAddr_1 == ieeeAddr) or (entry.device_ieeeAddr_2 == ieeeAddr):
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in scheduler"
    
    # check sensordata
    entries = GET_ALL_SENSORDATA_JOBS()
    for entry in entries:
        if entry.device_ieeeAddr == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in sensordata / jobs"

    # check lighting groups
    entries = GET_ALL_LIGHTING_GROUPS()
    for entry in entries:
        if entry.light_ieeeAddr_1 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_2 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_3 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups" 
        if entry.light_ieeeAddr_4 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_5 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_6 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_7 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_8 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"
        if entry.light_ieeeAddr_9 == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + ", " + device.name + " used in lighting / groups"            
        
    if error_list != "":
        return error_list[2:]   
               
    else:
        
        try:
            device      = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            device_name = device.name
            
            # delete controller entries
            if device.device_type == "controller":
                DELETE_CONTROLLER(ieeeAddr)

            # delete device exceptions
            for exception in GET_ALL_DEVICE_EXCEPTIONS():
                if exception.device_ieeeAddr == ieeeAddr:
                    DELETE_DEVICE_EXCEPTION(exception.id)

            Devices.query.filter_by(ieeeAddr=ieeeAddr).delete()
            db.session.commit() 
      
            WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(device_name) + " | deleted")                      
            return True

        except Exception as e:
            return str(e)


""" ################### """
""" ################### """
"""  device exceptions  """
""" ################### """
""" ################### """


def GET_DEVICE_EXCEPTION_BY_ID(id):
    return Device_Exceptions.query.filter_by(id=id).first()   


def GET_DEVICE_EXCEPTION_BY_IEEEADDR(device_ieeeAddr):
    return Device_Exceptions.query.filter_by(device_ieeeAddr=device_ieeeAddr).first()   


def GET_ALL_DEVICE_EXCEPTIONS():   
    return Device_Exceptions.query.all()


def ADD_DEVICE_EXCEPTION(device_ieeeAddr):
    for i in range(1,26):
        if Device_Exceptions.query.filter_by(id=i).first():
            pass
        else:
            # add the new device exception
            device_exception = Device_Exceptions(
                    id              = i,
                    device_ieeeAddr = device_ieeeAddr,           
                )
            db.session.add(device_exception)
            db.session.commit()

            device = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr)

            WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(device.name) + " | Exception | added")                   
            return True

    return "Limit reached (25)"


def UPDATE_DEVICE_EXCEPTION(id, exception_option, exception_command, exception_sensor_ieeeAddr, 
                            exception_sensor_input_values, exception_value_1, exception_value_2, exception_value_3):
              
    entry = Device_Exceptions.query.filter_by(id=id).first()
             
    # values changed ?
    if (entry.exception_option != exception_option or entry.exception_command != exception_command or
        entry.exception_sensor_ieeeAddr != exception_sensor_ieeeAddr or 
        entry.exception_sensor_input_values != exception_sensor_input_values or 
        entry.exception_value_1 != exception_value_1 or entry.exception_value_2 != exception_value_2 or 
        entry.exception_value_3 != exception_value_3):              

        changes = ""

        if entry.exception_option != exception_option:
            changes = changes + " || exception_option || " + str(entry.exception_option) + " >>> " + str(exception_option)
        if entry.exception_command != exception_command:
            changes = changes + " || exception_command || " + str(entry.exception_command) + " >>> " + str(exception_command)            
        if entry.exception_sensor_ieeeAddr != exception_sensor_ieeeAddr:
            changes = changes + " || exception_sensor_ieeeAddr || " + str(entry.exception_sensor_ieeeAddr) + " >>> " + str(exception_sensor_ieeeAddr)        
        if entry.exception_sensor_input_values != exception_sensor_input_values:
            changes = changes + " || exception_sensor_input_values || " + str(entry.exception_sensor_input_values) + " >>> " + str(exception_sensor_input_values)       
        if entry.exception_value_1 != exception_value_1:
            changes = changes + " || exception_value_1 || " + str(entry.exception_value_1) + " >>> " + str(exception_value_1)   
        if entry.exception_value_2 != exception_value_2:
            changes = changes + " || exception_value_2 || " + str(entry.exception_value_2) + " >>> " + str(exception_value_2)       
        if entry.exception_value_3 != exception_value_3:
            changes = changes + " || exception_value_3 || " + str(entry.exception_value_3) + " >>> " + str(exception_value_3)   

        entry.exception_option              = exception_option
        entry.exception_command             = exception_command       
        entry.exception_sensor_ieeeAddr     = exception_sensor_ieeeAddr
        entry.exception_sensor_input_values = exception_sensor_input_values
        entry.exception_value_1             = exception_value_1
        entry.exception_value_2             = exception_value_2 
        entry.exception_value_3             = exception_value_3            
        db.session.commit()  
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(entry.device.name) + " | Exception | changed" + changes) 

        return True


def CHANGE_DEVICE_EXCEPTION_POSITION(id, direction):
    if direction == "up":
        device_exception_list = GET_ALL_DEVICE_EXCEPTIONS()
        device_exception_list = device_exception_list[::-1]
        
        for device_exception in device_exception_list:
            
            if device_exception.id < id:
                
                new_id = device_exception.id
                
                # change ids
                device_exception_1 = GET_DEVICE_EXCEPTION_BY_ID(id)
                device_exception_2 = GET_DEVICE_EXCEPTION_BY_ID(new_id)
                
                device_exception_1.id = 111
                db.session.commit()
                
                device_exception_2.id = id
                device_exception_1.id = new_id
                db.session.commit()       
                return 

    if direction == "down":
        for device_exception in GET_ALL_DEVICE_EXCEPTIONS():
            if device_exception.id > id:
                
                new_id = device_exception.id
                
                # change ids
                device_exception_1 = GET_DEVICE_EXCEPTION_BY_ID(id)
                device_exception_2 = GET_DEVICE_EXCEPTION_BY_ID(new_id)
                
                device_exception_1.id = 111
                db.session.commit()
                
                device_exception_2.id = id
                device_exception_1.id = new_id
                db.session.commit()           
                return 


def DELETE_DEVICE_EXCEPTION(id):
    entry = Device_Exceptions.query.filter_by(id=id).first()

    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + str(entry.device.name) + " | Exception | deleted")   
    except:
        pass         
    
    Device_Exceptions.query.filter_by(id=id).delete()
    db.session.commit()
    return True


""" ################## """
""" ################## """
"""        eMail       """
""" ################## """
""" ################## """


def GET_EMAIL_SETTINGS():   
    return eMail.query.filter_by().first()


def GET_EMAIL_ADDRESSES(address_type): 
    if address_type == "TEST":
        mail_list = []
        mail_list.append(eMail.query.filter_by().first().username)
        return mail_list

    if address_type == "NOTIFICATION":
        mail_list = []
        users = User.query.all()
        for user in users:
            if user.email_notification == "True":
                mail_list.append(user.email)
        return mail_list


def SET_EMAIL_SETTINGS(server_address, server_port, encoding, username, password): 
    entry = eMail.query.filter_by().first()

    if (entry.server_address != server_address or entry.server_port != server_port or entry.encoding != encoding or entry.username != username or entry.password != password):

        changes = ""

        if entry.server_address != server_address:
            changes = changes + " || server_address || " + str(entry.server_address) + " >>> " + str(server_address)
        if entry.server_port != server_port:
            changes = changes + " || server_port || " + str(entry.server_port) + " >>> " + str(server_port)            
        if entry.encoding != encoding:
            changes = changes + " || encoding || " + str(entry.encoding) + " >>> " + str(encoding)        
        if entry.username != username:
            changes = changes + " || username || " + str(entry.username) + " >>> " + str(username)       
        if entry.password != password:
            changes = changes + " || password || " + str(entry.password) + " >>> " + str(password)

        entry.server_address = server_address
        entry.server_port    = server_port
        entry.encoding       = encoding
        entry.username       = username
        entry.password       = password
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | eMail Settings | changed" + changes) 
        return True


""" ################### """
""" ################### """
"""    light groups     """
""" ################### """
""" ################### """


def GET_ALL_LIGHTING_GROUPS():
    return Lighting_Groups.query.all()   
  
    
def GET_ALL_ACTIVE_LIGHTING_GROUPS():
    list_active_groups = []

    for group in Lighting_Groups.query.all():
        if group.light_ieeeAddr_1 != None and group.light_ieeeAddr_1 != "None":
            list_active_groups.append(group)
            
    return list_active_groups
          

def GET_LIGHTING_GROUP_BY_ID(id):
    return Lighting_Groups.query.filter_by(id=id).first()


def GET_LIGHTING_GROUP_BY_NAME(name):

    for group in Lighting_Groups.query.all():
        
        if group.name.lower() == name.lower():
            return group
        

def ADD_LIGHTING_GROUP():
    for i in range(1,21):
        if Lighting_Groups.query.filter_by(id=i).first():
            pass
        else:
            # add the new program
            group = Lighting_Groups(
                    id = i,
                    name = "new_group_" + str(i),
                )
            db.session.add(group)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Group - " + "new_group_" + str(i) + " | added")  
            return True

    return "Limit reached (20)"


def SET_LIGHTING_GROUP(id, name, light_ieeeAddr_1, light_name_1, light_device_type_1, 
                                 light_ieeeAddr_2, light_name_2, light_device_type_2,
                                 light_ieeeAddr_3, light_name_3, light_device_type_3,
                                 light_ieeeAddr_4, light_name_4, light_device_type_4,
                                 light_ieeeAddr_5, light_name_5, light_device_type_5,
                                 light_ieeeAddr_6, light_name_6, light_device_type_6,
                                 light_ieeeAddr_7, light_name_7, light_device_type_7,
                                 light_ieeeAddr_8, light_name_8, light_device_type_8,
                                 light_ieeeAddr_9, light_name_9, light_device_type_9):

    entry         = Lighting_Groups.query.filter_by(id=id).first()
    previous_name = entry.name

    if (entry.name != name or
        entry.light_ieeeAddr_1 != light_ieeeAddr_1 or entry.light_name_1 != light_name_1 or entry.light_device_type_1 != light_device_type_1 or 
        entry.light_ieeeAddr_2 != light_ieeeAddr_2 or entry.light_name_2 != light_name_2 or entry.light_device_type_2 != light_device_type_2 or
        entry.light_ieeeAddr_3 != light_ieeeAddr_3 or entry.light_name_3 != light_name_3 or entry.light_device_type_3 != light_device_type_3 or
        entry.light_ieeeAddr_4 != light_ieeeAddr_4 or entry.light_name_4 != light_name_4 or entry.light_device_type_4 != light_device_type_4 or
        entry.light_ieeeAddr_5 != light_ieeeAddr_5 or entry.light_name_5 != light_name_5 or entry.light_device_type_5 != light_device_type_5 or
        entry.light_ieeeAddr_6 != light_ieeeAddr_6 or entry.light_name_6 != light_name_6 or entry.light_device_type_6 != light_device_type_6 or
        entry.light_ieeeAddr_7 != light_ieeeAddr_7 or entry.light_name_7 != light_name_7 or entry.light_device_type_7 != light_device_type_7 or
        entry.light_ieeeAddr_8 != light_ieeeAddr_8 or entry.light_name_8 != light_name_8 or entry.light_device_type_8 != light_device_type_8 or
        entry.light_ieeeAddr_9 != light_ieeeAddr_9 or entry.light_name_9 != light_name_9 or entry.light_device_type_9 != light_device_type_9):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + str(entry.name) + " >>> " + str(name)
        if entry.light_name_1 != light_name_1:
            changes = changes + " || light_name_1 || " + str(entry.light_name_1) + " >>> " + str(light_name_1)            
        if entry.light_name_2 != light_name_2:
            changes = changes + " || light_name_2 || " + str(entry.light_name_2) + " >>> " + str(light_name_2)        
        if entry.light_name_3 != light_name_3:
            changes = changes + " || light_name_3 || " + str(entry.light_name_3) + " >>> " + str(light_name_3)       
        if entry.light_name_4 != light_name_4:
            changes = changes + " || light_name_4 || " + str(entry.light_name_4) + " >>> " + str(light_name_4)
        if entry.light_name_5 != light_name_5:
            changes = changes + " || light_name_5 || " + str(entry.light_name_5) + " >>> " + str(light_name_5)
        if entry.light_name_6 != light_name_6:
            changes = changes + " || light_name_6 || " + str(entry.light_name_6) + " >>> " + str(light_name_6)           
        if entry.light_name_7 != light_name_7:
            changes = changes + " || light_name_7 || " + str(entry.light_name_7) + " >>> " + str(light_name_7)        
        if entry.light_name_8 != light_name_8:
            changes = changes + " || light_name_8 || " + str(entry.light_name_8) + " >>> " + str(light_name_8)       
        if entry.light_name_9 != light_name_9:
            changes = changes + " || light_name_9 || " + str(entry.light_name_9) + " >>> " + str(light_name_9)

        entry.name                = name
        entry.light_ieeeAddr_1    = light_ieeeAddr_1
        entry.light_name_1        = light_name_1
        entry.light_device_type_1 = light_device_type_1
        entry.light_ieeeAddr_2    = light_ieeeAddr_2
        entry.light_name_2        = light_name_2
        entry.light_device_type_2 = light_device_type_2 
        entry.light_ieeeAddr_3    = light_ieeeAddr_3
        entry.light_name_3        = light_name_3
        entry.light_device_type_3 = light_device_type_3
        entry.light_ieeeAddr_4    = light_ieeeAddr_4
        entry.light_name_4        = light_name_4
        entry.light_device_type_4 = light_device_type_4
        entry.light_ieeeAddr_5    = light_ieeeAddr_5
        entry.light_name_5        = light_name_5
        entry.light_device_type_5 = light_device_type_5
        entry.light_ieeeAddr_6    = light_ieeeAddr_6
        entry.light_name_6        = light_name_6
        entry.light_device_type_6 = light_device_type_6 
        entry.light_ieeeAddr_7    = light_ieeeAddr_7
        entry.light_name_7        = light_name_7
        entry.light_device_type_7 = light_device_type_7
        entry.light_ieeeAddr_8    = light_ieeeAddr_8
        entry.light_name_8        = light_name_8
        entry.light_device_type_8 = light_device_type_8
        entry.light_ieeeAddr_9    = light_ieeeAddr_9
        entry.light_name_9        = light_name_9
        entry.light_device_type_9 = light_device_type_9
        
        db.session.commit()  

        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Group - " + str(previous_name) + " | changed" + changes)  
        return True 


def SET_LIGHTING_GROUP_ERRORS(id, group_errors):
    entry = Lighting_Groups.query.filter_by(id=id).first()

    if entry.group_errors != group_errors:
        entry.group_errors = group_errors       
        db.session.commit()     


def SET_LIGHTING_GROUP_COLLAPSE_OPEN(id):
    for lighting_group in Lighting_Groups.query.all():
        lighting_group.collapse = ""
        db.session.commit()   
  
    entry = Lighting_Groups.query.filter_by(id=id).first()
    
    entry.collapse = "True"
    db.session.commit()   


def RESET_LIGHTING_GROUP_COLLAPSE():
    for lighting_group in Lighting_Groups.query.all():
        lighting_group.collapse = ""
        db.session.commit()   


def SET_LIGHTING_GROUP_NAME(id, name):
    entry = Lighting_Groups.query.filter_by(id=id).first()
    entry.name = name     
    db.session.commit()  


def SET_LIGHTING_GROUP_CURRENT_SCENE(id, current_scene):
    entry = Lighting_Groups.query.filter_by(id=id).first()
    entry.current_scene = current_scene     
    db.session.commit()  


def SET_LIGHTING_GROUP_CURRENT_BRIGHTNESS(id, current_brightness):
    entry = Lighting_Groups.query.filter_by(id=id).first()
    entry.current_brightness = current_brightness     
    db.session.commit()  


def UPDATE_LIGHTING_GROUP_LIGHT_NAMES():
    groups = GET_ALL_LIGHTING_GROUPS()
    
    for group in groups:
        
        entry = Lighting_Groups.query.filter_by(id=group.id).first()
        
        try:
            entry.light_name_1        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_1).name
            entry.light_device_type_1 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_1).device_type
        except:
            pass
        try:
            entry.light_name_2        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_2).name
            entry.light_device_type_2 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_2).device_type
        except:
            pass
        try:
            entry.light_name_3        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_3).name
            entry.light_device_type_3 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_3).device_type
        except:
            pass
        try:
            entry.light_name_4        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_4).name
            entry.light_device_type_4 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_4).device_type
        except:
            pass
        try:
            entry.light_name_5        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_5).name
            entry.light_device_type_5 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_5).device_type
        except:
            pass
        try:
            entry.light_name_6        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_6).name
            entry.light_device_type_6 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_6).device_type
        except:
            pass
        try:
            entry.light_name_7        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_7).name
            entry.light_device_type_7 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_7).device_type
        except:
            pass
        try:
            entry.light_name_8        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_8).name
            entry.light_device_type_8 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_8).device_type
        except:
            pass
        try:
            entry.light_name_9        = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_9).name
            entry.light_device_type_9 = GET_DEVICE_BY_IEEEADDR(entry.light_ieeeAddr_9).device_type
        except:
            pass            
        
    db.session.commit()


def ADD_LIGHTING_GROUP_OBJECT(id):
    entry = Lighting_Groups.query.filter_by(id=id).first()

    if entry.active_light_2 != "True":
        entry.active_light_2 = "True"
        db.session.commit()
        return
    if entry.active_light_3 != "True":
        entry.active_light_3 = "True"
        db.session.commit()
        return
    if entry.active_light_4 != "True":
        entry.active_light_4 = "True"
        db.session.commit()
        return
    if entry.active_light_5 != "True":
        entry.active_light_5 = "True"
        db.session.commit()
        return
    if entry.active_light_6 != "True":
        entry.active_light_6 = "True"
        db.session.commit()
        return
    if entry.active_light_7 != "True":
        entry.active_light_7 = "True"
        db.session.commit()
        return
    if entry.active_light_8 != "True":
        entry.active_light_8 = "True"
        db.session.commit()
        return       
    if entry.active_light_9 != "True":
        entry.active_light_9 = "True"
        db.session.commit()
        return  


def REMOVE_LIGHTING_GROUP_OBJECT(id):
    entry = Lighting_Groups.query.filter_by(id=id).first()

    if entry.active_light_9 == "True":
        entry.active_light_9      = "None"
        entry.light_ieeeAddr_9    = "None"
        entry.light_name_9        = "None"
        entry.light_device_type_9 = "None"
        db.session.commit()
        return 

    if entry.active_light_8 == "True":
        entry.active_light_8      = "None"
        entry.light_ieeeAddr_8    = "None"
        entry.light_name_8        = "None"
        entry.light_device_type_8 = "None"
        db.session.commit()  
        return 
    
    if entry.active_light_7 == "True":
        entry.active_light_7      = "None"
        entry.light_ieeeAddr_7    = "None"
        entry.light_name_7        = "None"
        entry.light_device_type_7 = "None"
        db.session.commit()
        return 

    if entry.active_light_6 == "True":
        entry.active_light_6      = "None"
        entry.light_ieeeAddr_6    = "None"
        entry.light_name_6        = "None"
        entry.light_device_type_6 = "None"
        db.session.commit()
        return
    
    if entry.active_light_5 == "True":
        entry.active_light_5      = "None"
        entry.light_ieeeAddr_5    = "None"
        entry.light_name_5        = "None"
        entry.light_device_type_5 = "None"
        db.session.commit()
        return     

    if entry.active_light_4 == "True":
        entry.active_light_4      = "None"
        entry.light_ieeeAddr_4    = "None"
        entry.light_name_4        = "None"
        entry.light_device_type_4 = "None"
        db.session.commit()
        return 

    if entry.active_light_3 == "True":
        entry.active_light_3      = "None"
        entry.light_ieeeAddr_3    = "None"
        entry.light_name_3        = "None"
        entry.light_device_type_3 = "None"
        db.session.commit()
        return     

    if entry.active_light_2 == "True":
        entry.active_light_2      = "None"
        entry.light_ieeeAddr_2    = "None"
        entry.light_name_2        = "None"
        entry.light_device_type_2 = "None"
        db.session.commit()
        return 


def CHANGE_LIGHTING_GROUP_POSITION(id, direction):
    if direction == "up":
        groups_list = GET_ALL_LIGHTING_GROUPS()
        groups_list = groups_list[::-1]
        
        for group in groups_list:
            
            if group.id < id: 
                new_id = group.id
                
                # change ids
                group_1 = GET_LIGHTING_GROUP_BY_ID(id)
                group_2 = GET_LIGHTING_GROUP_BY_ID(new_id)
                
                group_1.id = 99
                db.session.commit()
                
                group_2.id = id
                group_1.id = new_id
                db.session.commit()           
                return 

    if direction == "down":
        for group in GET_ALL_LIGHTING_GROUPS():
            if group.id > id:
                new_id = group.id
                
                # change ids
                group_1 = GET_LIGHTING_GROUP_BY_ID(id)
                group_2 = GET_LIGHTING_GROUP_BY_ID(new_id)
                
                group_1.id = 99
                db.session.commit()
                
                group_2.id = id
                group_1.id = new_id
                db.session.commit()           
                return 


def DELETE_LIGHTING_GROUP(id):
    name = GET_LIGHTING_GROUP_BY_ID(id).name
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Group - " + str(name) + " | deleted")   
    except:
        pass     
    
    Lighting_Groups.query.filter_by(id=id).delete()
    db.session.commit() 
    return True


""" ################### """
""" ################### """
"""    light scenes     """
""" ################### """
""" ################### """


def GET_ALL_LIGHTING_SCENES():
    return Lighting_Scenes.query.all()   


def GET_LIGHTING_SCENE_BY_ID(id):
    return Lighting_Scenes.query.filter_by(id=id).first()


def GET_LIGHTING_SCENE_BY_NAME(name):
    for scene in Lighting_Scenes.query.all():
        
        if scene.name.lower() == name.lower():
            return scene    
            

def ADD_LIGHTING_SCENE():
    for i in range(1,21):
        if Lighting_Scenes.query.filter_by(id=i).first():
            pass
        else:
            # add the new scene
            scene = Lighting_Scenes(
                    id           = i,
                    name         = "new_scene_" + str(i),
                    red_1        = 255,
                    green_1      = 255,
                    blue_1       = 255, 
                    brightness_1 = 255,                                
                )
            db.session.add(scene)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Scene - " + "new_scene_" + str(i) + " | added")  
            return True

    return "Limit reached (20)"


def SET_LIGHTING_SCENE(id, name, red_1, green_1, blue_1, brightness_1, red_2, green_2, blue_2, brightness_2, red_3, green_3, blue_3, brightness_3, 
                                 red_4, green_4, blue_4, brightness_4, red_5, green_5, blue_5, brightness_5, red_6, green_6, blue_6, brightness_6, 
                                 red_7, green_7, blue_7, brightness_7, red_8, green_8, blue_8, brightness_8, red_9, green_9, blue_9, brightness_9):

    entry         = Lighting_Scenes.query.filter_by(id=id).first()
    previous_name = entry.name

    if (entry.name != name or 
        entry.red_1 != int(red_1) or entry.green_1 != int(green_1) or entry.blue_1 != int(blue_1) or entry.brightness_1 != int(brightness_1) or
        entry.red_2 != int(red_2) or entry.green_2 != int(green_2) or entry.blue_2 != int(blue_2) or entry.brightness_2 != int(brightness_2) or 
        entry.red_3 != int(red_3) or entry.green_3 != int(green_3) or entry.blue_3 != int(blue_3) or entry.brightness_3 != int(brightness_3) or
        entry.red_4 != int(red_4) or entry.green_4 != int(green_4) or entry.blue_4 != int(blue_4) or entry.brightness_4 != int(brightness_4) or 
        entry.red_5 != int(red_5) or entry.green_5 != int(green_5) or entry.blue_5 != int(blue_5) or entry.brightness_5 != int(brightness_5) or 
        entry.red_6 != int(red_6) or entry.green_6 != int(green_6) or entry.blue_6 != int(blue_6) or entry.brightness_6 != int(brightness_6) or 
        entry.red_7 != int(red_7) or entry.green_7 != int(green_7) or entry.blue_7 != int(blue_7) or entry.brightness_7 != int(brightness_7) or 
        entry.red_8 != int(red_8) or entry.green_8 != int(green_8) or entry.blue_8 != int(blue_8) or entry.brightness_8 != int(brightness_8) or 
        entry.red_9 != int(red_9) or entry.green_9 != int(green_9) or entry.blue_9 != int(blue_9) or entry.brightness_9 != int(brightness_9)):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + entry.name + " >>> " + name
        if entry.red_1 != int(red_1) or entry.green_1 != int(green_1) or entry.blue_1 != int(blue_1) or entry.brightness_1 != int(brightness_1):
            changes = (changes + " || light_1_settings || " + str(entry.red_1) + "," + str(entry.green_1) + "," + str(entry.blue_1) + "/" + str(entry.brightness_1) + 
                                 " >>> " + str(red_1) + "," + str(green_1) + "," + str(blue_1) + "/" + str(brightness_1))
        if entry.red_2 != int(red_2) or entry.green_2 != int(green_2) or entry.blue_2 != int(blue_2) or entry.brightness_2 != int(brightness_2):
            changes = (changes + " || light_2_settings || " + str(entry.red_2) + "," + str(entry.green_2) + "," + str(entry.blue_2) + "/" + str(entry.brightness_2) + 
                                 " >>> " + str(red_2) + "," + str(green_2) + "," + str(blue_2) + "/" + str(brightness_2))
        if entry.red_3 != int(red_3) or entry.green_3 != int(green_3) or entry.blue_3 != int(blue_3) or entry.brightness_3 != int(brightness_3):
            changes = (changes + " || light_3_settings || " + str(entry.red_3) + "," + str(entry.green_3) + "," + str(entry.blue_3) + "/" + str(entry.brightness_3) + 
                                 " >>> " + str(red_3) + "," + str(green_3) + "," + str(blue_3) + "/" + str(brightness_3))
        if entry.red_4 != int(red_4) or entry.green_4 != int(green_4) or entry.blue_4 != int(blue_4) or entry.brightness_4 != int(brightness_4):
            changes = (changes + " || light_4_settings || " + str(entry.red_4) + "," + str(entry.green_4) + "," + str(entry.blue_4) + "/" + str(entry.brightness_4) + 
                                 " >>> " + str(red_4) + "," + str(green_4) + "," + str(blue_4) + "/" + str(brightness_4))
        if entry.red_5 != int(red_5) or entry.green_5 != int(green_5) or entry.blue_5 != int(blue_5) or entry.brightness_5 != int(brightness_5):
            changes = (changes + " || light_5_settings || " + str(entry.red_5) + "," + str(entry.green_5) + "," + str(entry.blue_5) + "/" + str(entry.brightness_5) + 
                                 " >>> " + str(red_5) + "," + str(green_5) + "," + str(blue_5) + "/" + str(brightness_5))
        if entry.red_6 != int(red_6) or entry.green_6 != int(green_6) or entry.blue_6 != int(blue_6) or entry.brightness_6 != int(brightness_6):
            changes = (changes + " || light_6_settings || " + str(entry.red_6) + "," + str(entry.green_6) + "," + str(entry.blue_6) + "/" + str(entry.brightness_6) + 
                                 " >>> " + str(red_6) + "," + str(green_6) + "," + str(blue_6) + "/" + str(brightness_6))
        if entry.red_7 != int(red_7) or entry.green_7 != int(green_7) or entry.blue_7 != int(blue_7) or entry.brightness_7 != int(brightness_7):
            changes = (changes + " || light_7_settings || " + str(entry.red_7) + "," + str(entry.green_7) + "," + str(entry.blue_7) + "/" + str(entry.brightness_7) + 
                                 " >>> " + str(red_7) + "," + str(green_7) + "," + str(blue_7) + "/" + str(brightness_7))
        if entry.red_8 != int(red_8) or entry.green_8 != int(green_8) or entry.blue_8 != int(blue_8) or entry.brightness_8 != int(brightness_8):
            changes = (changes + " || light_8_settings || " + str(entry.red_8) + "," + str(entry.green_8) + "," + str(entry.blue_8) + "/" + str(entry.brightness_8) + 
                                 " >>> " + str(red_8) + "," + str(green_8) + "," + str(blue_8) + "/" + str(brightness_8))
        if entry.red_9 != int(red_9) or entry.green_9 != int(green_9) or entry.blue_9 != int(blue_9) or entry.brightness_9 != int(brightness_9):
            changes = (changes + " || light_9_settings || " + str(entry.red_9) + "," + str(entry.green_9) + "," + str(entry.blue_9) + "/" + str(entry.brightness_9) + 
                                 " >>> " + str(red_9) + "," + str(green_9) + "," + str(blue_9) + "/" + str(brightness_9))

        entry.name         = name
        entry.red_1        = red_1
        entry.green_1      = green_1  
        entry.blue_1       = blue_1
        entry.brightness_1 = brightness_1
        entry.red_2        = red_2
        entry.green_2      = green_2   
        entry.blue_2       = blue_2
        entry.brightness_2 = brightness_2        
        entry.red_3        = red_3
        entry.green_3      = green_3   
        entry.blue_3       = blue_3 
        entry.brightness_3 = brightness_3        
        entry.red_4        = red_4
        entry.green_4      = green_4   
        entry.blue_4       = blue_4
        entry.brightness_4 = brightness_4        
        entry.red_5        = red_5
        entry.green_5      = green_5   
        entry.blue_5       = blue_5
        entry.brightness_5 = brightness_5       
        entry.red_6        = red_6
        entry.green_6      = green_6   
        entry.blue_6       = blue_6
        entry.brightness_6 = brightness_6        
        entry.red_7        = red_7
        entry.green_7      = green_7   
        entry.blue_7       = blue_7
        entry.brightness_7 = brightness_7        
        entry.red_8        = red_8
        entry.green_8      = green_8   
        entry.blue_8       = blue_8
        entry.brightness_8 = brightness_8        
        entry.red_9        = red_9
        entry.green_9      = green_9   
        entry.blue_9       = blue_9 
        entry.brightness_9 = brightness_9                       
        db.session.commit()  

        WRITE_LOGFILE_SYSTEM("DATABASE", "Light | Scene - " + str(previous_name) + " | changed" + changes) 
        return True


def ADD_LIGHTING_SCENE_OBJECT(id):
    entry = Lighting_Scenes.query.filter_by(id=id).first()

    if entry.active_light_2 != "True":
        entry.active_light_2 = "True" 
        entry.red_2          = 255
        entry.green_2        = 255
        entry.blue_2         = 255  
        entry.brightness_2   = 255                  
        db.session.commit()
        return

    if entry.active_light_3 != "True":
        entry.active_light_3 = "True"     
        entry.red_3          = 255
        entry.green_3        = 255
        entry.blue_3         = 255    
        entry.brightness_3   = 255               
        db.session.commit()
        return

    if entry.active_light_4 != "True":
        entry.active_light_4 = "True"   
        entry.red_4          = 255
        entry.green_4        = 255
        entry.blue_4         = 255     
        entry.brightness_4   = 255             
        db.session.commit()
        return

    if entry.active_light_5 != "True":
        entry.active_light_5 = "True"  
        entry.red_5          = 255
        entry.green_5        = 255
        entry.blue_5         = 255  
        entry.brightness_5   = 255                 
        db.session.commit()
        return

    if entry.active_light_6 != "True":
        entry.active_light_6 = "True"   
        entry.red_6          = 255
        entry.green_6        = 255
        entry.blue_6         = 255   
        entry.brightness_6   = 255      
        db.session.commit()
        return

    if entry.active_light_7 != "True":
        entry.active_light_7 = "True"  
        entry.red_7          = 255
        entry.green_7        = 255
        entry.blue_7         = 255    
        entry.brightness_7   = 255   
        db.session.commit()
        return

    if entry.active_light_8 != "True":
        entry.active_light_8 = "True"     
        entry.red_8          = 255
        entry.green_8        = 255
        entry.blue_8         = 255     
        entry.brightness_8   = 255           
        db.session.commit()
        return    

    if entry.active_light_9 != "True":
        entry.active_light_9 = "True"
        entry.red_9          = 255
        entry.green_9        = 255
        entry.blue_9         = 255    
        entry.brightness_9   = 255 
        db.session.commit()
        return  


def REMOVE_LIGHTING_SCENE_OBJECT(id):
    entry = Lighting_Scenes.query.filter_by(id=id).first()

    if entry.active_light_9 == "True":
        entry.active_light_9 = "None"
        entry.red_9          = 0
        entry.green_9        = 0
        entry.blue_9         = 0
        entry.brightness_9   = 0  
        db.session.commit()
        return

    if entry.active_light_8 == "True":
        entry.active_light_8 = "None"
        entry.red_8          = 0
        entry.green_8        = 0
        entry.blue_8         = 0
        entry.brightness_8   = 0          
        db.session.commit()
        return

    if entry.active_light_7 == "True":
        entry.active_light_7 = "None"
        entry.red_7          = 0
        entry.green_7        = 0
        entry.blue_7         = 0
        entry.brightness_7   = 0          
        db.session.commit()
        return

    if entry.active_light_6 == "True":
        entry.active_light_6 = "None"
        entry.red_6          = 0
        entry.green_6        = 0
        entry.blue_6         = 0
        entry.brightness_6   = 0          
        db.session.commit()
        return

    if entry.active_light_5 == "True":
        entry.active_light_5 = "None"
        entry.red_5          = 0
        entry.green_5        = 0
        entry.blue_5         = 0
        entry.brightness_5   = 0          
        db.session.commit()
        return

    if entry.active_light_4 == "True":
        entry.active_light_4 = "None"
        entry.red_4          = 0
        entry.green_4        = 0
        entry.blue_4         = 0
        entry.brightness_4   = 0          
        db.session.commit()
        return

    if entry.active_light_3 == "True":
        entry.active_light_3 = "None"
        entry.red_3          = 0
        entry.green_3        = 0
        entry.blue_3         = 0
        entry.brightness_3   = 0          
        db.session.commit()
        return

    if entry.active_light_2 == "True":
        entry.active_light_2 = "None"
        entry.red_2          = 0
        entry.green_2        = 0
        entry.blue_2         = 0
        entry.brightness_2   = 0          
        db.session.commit()
        return


def SET_LIGHTING_SCENE_COLLAPSE_OPEN(id):
    for lighting_scene in Lighting_Scenes.query.all():
        lighting_scene.collapse = ""
        db.session.commit()   
  
    entry = Lighting_Scenes.query.filter_by(id=id).first()
    
    entry.collapse = "True"
    db.session.commit()   


def RESET_LIGHTING_SCENE_COLLAPSE():
    for lighting_scene in Lighting_Scenes.query.all():
        lighting_scene.collapse = ""
        db.session.commit()   


def CHANGE_LIGHTING_SCENE_POSITION(id, direction):
    if direction == "up":
        scenes_list = GET_ALL_LIGHTING_SCENES()
        scenes_list = scenes_list[::-1]
        
        for scene in scenes_list:
            
            if scene.id < id:    
                new_id = scene.id
                
                # change ids
                scene_1 = GET_LIGHTING_SCENE_BY_ID(id)
                scene_2 = GET_LIGHTING_SCENE_BY_ID(new_id)
                
                scene_1.id = 99
                db.session.commit()
                
                scene_2.id = id
                scene_1.id = new_id
                db.session.commit()     
                return 

    if direction == "down":
        for scene in GET_ALL_LIGHTING_SCENES():
            if scene.id > id:   
                new_id = scene.id
                
                # change ids
                scene_1 = GET_LIGHTING_SCENE_BY_ID(id)
                scene_2 = GET_LIGHTING_SCENE_BY_ID(new_id)
                
                scene_1.id = 99
                db.session.commit()
                
                scene_2.id = id
                scene_1.id = new_id
                db.session.commit()          
                return 


def DELETE_LIGHTING_SCENE(id):
    name = GET_LIGHTING_SCENE_BY_ID(id).name
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Scene - " + str(name) + " | deleted") 
    except:
        pass 

    Lighting_Scenes.query.filter_by(id=id).delete()
    db.session.commit() 
    return True


""" ################### """
""" ################### """
"""       programs      """
""" ################### """
""" ################### """


def GET_ALL_PROGRAMS():
    return Programs.query.all()   


def GET_PROGRAM_BY_NAME(name):
    for program in Programs.query.all():
        
        if program.name.lower() == name.lower():
            return program    
    

def GET_PROGRAM_BY_ID(id):
    return Programs.query.filter_by(id=id).first()


def ADD_PROGRAM():
    for i in range(1,31):
        if Programs.query.filter_by(id=i).first():
            pass
        else:
            # add the new program
            program = Programs(
                    id = i,
                    name = "new_program_" + str(i), 
                )
            db.session.add(program)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Program | " + "new_program_" + str(i) + " | added")  

            return True

    return "Limit reached (30)"


def SET_PROGRAM_SETTINGS(id, name, line_content_1,  line_content_2,  line_content_3,  line_content_4,  line_content_5, 
                                   line_content_6,  line_content_7,  line_content_8,  line_content_9,  line_content_10,
                                   line_content_11, line_content_12, line_content_13, line_content_14, line_content_15, 
                                   line_content_16, line_content_17, line_content_18, line_content_19, line_content_20, 
                                   line_content_21, line_content_22, line_content_23, line_content_24, line_content_25, 
                                   line_content_26, line_content_27, line_content_28, line_content_29, line_content_30): 

    entry         = Programs.query.filter_by(id=id).first()
    previous_name = entry.name

    if (entry.name != name  or entry.line_content_1  != line_content_1  or entry.line_content_2  != line_content_2  or 
                               entry.line_content_3  != line_content_3  or entry.line_content_4  != line_content_4  or 
                               entry.line_content_5  != line_content_5  or entry.line_content_6  != line_content_6  or 
                               entry.line_content_7  != line_content_7  or entry.line_content_8  != line_content_8  or 
                               entry.line_content_9  != line_content_9  or entry.line_content_10 != line_content_10 or 
                               entry.line_content_11 != line_content_11 or entry.line_content_12 != line_content_12 or
                               entry.line_content_13 != line_content_13 or entry.line_content_14 != line_content_14 or
                               entry.line_content_15 != line_content_15 or entry.line_content_16 != line_content_16 or
                               entry.line_content_17 != line_content_17 or entry.line_content_18 != line_content_18 or 
                               entry.line_content_19 != line_content_19 or entry.line_content_20 != line_content_20 or
                               entry.line_content_21 != line_content_21 or entry.line_content_22 != line_content_22 or
                               entry.line_content_23 != line_content_23 or entry.line_content_24 != line_content_24 or
                               entry.line_content_25 != line_content_25 or entry.line_content_26 != line_content_26 or
                               entry.line_content_27 != line_content_27 or entry.line_content_28 != line_content_28 or 
                               entry.line_content_29 != line_content_29 or entry.line_content_30 != line_content_30):

        changes = ""

        if entry.name != name:
            changes = changes + " || previous name || " + str(entry.name) + " >>> " + str(name)
        if entry.line_content_1 != line_content_1:
            changes = changes + " || line_content_1 || " + str(entry.line_content_1) + " >>> " + str(line_content_1)            
        if entry.line_content_2 != line_content_2:
            changes = changes + " || line_content_2 || " + str(entry.line_content_2) + " >>> " + str(line_content_2)        
        if entry.line_content_3 != line_content_3:
            changes = changes + " || line_content_3 || " + str(entry.line_content_3) + " >>> " + str(line_content_3)       
        if entry.line_content_4 != line_content_4:
            changes = changes + " || line_content_4 || " + str(entry.line_content_4) + " >>> " + str(line_content_4)
        if entry.line_content_5 != line_content_5:
            changes = changes + " || line_content_5 || " + str(entry.line_content_5) + " >>> " + str(line_content_5)
        if entry.line_content_6 != line_content_6:
            changes = changes + " || line_content_6 || " + str(entry.line_content_6) + " >>> " + str(line_content_6)            
        if entry.line_content_7 != line_content_7:
            changes = changes + " || line_content_7 || " + str(entry.line_content_7) + " >>> " + str(line_content_7)        
        if entry.line_content_8 != line_content_8:
            changes = changes + " || line_content_8 || " + str(entry.line_content_8) + " >>> " + str(line_content_8)       
        if entry.line_content_9 != line_content_9:
            changes = changes + " || line_content_9 || " + str(entry.line_content_9) + " >>> " + str(line_content_9)
        if entry.line_content_10 != line_content_10:
            changes = changes + " || line_content_10 || " + str(entry.line_content_10) + " >>> " + str(line_content_10)
        if entry.line_content_11 != line_content_11:
            changes = changes + " || line_content_11 || " + str(entry.line_content_11) + " >>> " + str(line_content_11)            
        if entry.line_content_12 != line_content_12:
            changes = changes + " || line_content_12 || " + str(entry.line_content_12) + " >>> " + str(line_content_12)       
        if entry.line_content_13 != line_content_13:
            changes = changes + " || line_content_13 || " + str(entry.line_content_13) + " >>> " + str(line_content_13)       
        if entry.line_content_14 != line_content_14:
            changes = changes + " || line_content_14 || " + str(entry.line_content_14) + " >>> " + str(line_content_14)
        if entry.line_content_15 != line_content_15:
            changes = changes + " || line_content_15 || " + str(entry.line_content_15) + " >>> " + str(line_content_15)
        if entry.line_content_16 != line_content_16:
            changes = changes + " || line_content_16 || " + str(entry.line_content_16) + " >>> " + str(line_content_16)            
        if entry.line_content_17 != line_content_17:
            changes = changes + " || line_content_17 || " + str(entry.line_content_17) + " >>> " + str(line_content_17)        
        if entry.line_content_18 != line_content_18:
            changes = changes + " || line_content_18 || " + str(entry.line_content_18) + " >>> " + str(line_content_18)       
        if entry.line_content_19 != line_content_19:
            changes = changes + " || line_content_19 || " + str(entry.line_content_19) + " >>> " + str(line_content_19)
        if entry.line_content_20 != line_content_20:
            changes = changes + " || line_content_20 || " + str(entry.line_content_20) + " >>> " + str(line_content_20)
        if entry.line_content_21 != line_content_21:
            changes = changes + " || line_content_21 || " + str(entry.line_content_21) + " >>> " + str(line_content_21)            
        if entry.line_content_22 != line_content_22:
            changes = changes + " || line_content_22 || " + str(entry.line_content_22) + " >>> " + str(line_content_22)        
        if entry.line_content_23 != line_content_23:
            changes = changes + " || line_content_23 || " + str(entry.line_content_23) + " >>> " + str(line_content_23)       
        if entry.line_content_24 != line_content_24:
            changes = changes + " || line_content_24 || " + str(entry.line_content_24) + " >>> " + str(line_content_24)
        if entry.line_content_25 != line_content_25:
            changes = changes + " || line_content_25 || " + str(entry.line_content_25) + " >>> " + str(line_content_25)
        if entry.line_content_26 != line_content_26:
            changes = changes + " || line_content_26 || " + str(entry.line_content_26) + " >>> " + str(line_content_26)           
        if entry.line_content_27 != line_content_27:
            changes = changes + " || line_content_27 || " + str(entry.line_content_27) + " >>> " + str(line_content_27)        
        if entry.line_content_28 != line_content_28:
            changes = changes + " || line_content_28 || " + str(entry.line_content_28) + " >>> " + str(line_content_28)       
        if entry.line_content_29 != line_content_29:
            changes = changes + " || line_content_29 || " + str(entry.line_content_29) + " >>> " + str(line_content_29)
        if entry.line_content_30 != line_content_30:
            changes = changes + " || line_content_30 || " + str(entry.line_content_30) + " >>> " + str(line_content_30)

        entry.name            = name 
        entry.line_content_1  = line_content_1 
        entry.line_content_2  = line_content_2 
        entry.line_content_3  = line_content_3 
        entry.line_content_4  = line_content_4 
        entry.line_content_5  = line_content_5 
        entry.line_content_6  = line_content_6 
        entry.line_content_7  = line_content_7 
        entry.line_content_8  = line_content_8 
        entry.line_content_9  = line_content_9 
        entry.line_content_10 = line_content_10 
        entry.line_content_11 = line_content_11 
        entry.line_content_12 = line_content_12 
        entry.line_content_13 = line_content_13 
        entry.line_content_14 = line_content_14 
        entry.line_content_15 = line_content_15 
        entry.line_content_16 = line_content_16 
        entry.line_content_17 = line_content_17 
        entry.line_content_18 = line_content_18 
        entry.line_content_19 = line_content_19 
        entry.line_content_20 = line_content_20 
        entry.line_content_21 = line_content_21 
        entry.line_content_22 = line_content_22 
        entry.line_content_23 = line_content_23 
        entry.line_content_24 = line_content_24 
        entry.line_content_25 = line_content_25 
        entry.line_content_26 = line_content_26 
        entry.line_content_27 = line_content_27 
        entry.line_content_28 = line_content_28 
        entry.line_content_29 = line_content_29 
        entry.line_content_30 = line_content_30         
        db.session.commit()

        WRITE_LOGFILE_SYSTEM("DATABASE", "Program | " + str(previous_name) + " | changed" + changes)  
        return True


def CHANGE_PROGRAM_POSITION(id, direction):
    if direction == "up":
        program_list = GET_ALL_PROGRAMS()
        program_list = program_list[::-1]
        
        for program in program_list:
            
            if program.id < id:
                
                new_id = program.id
                
                # change ids
                program_1 = GET_PROGRAM_BY_ID(id)
                program_2 = GET_PROGRAM_BY_ID(new_id)
                
                program_1.id = 99
                db.session.commit()
                
                program_2.id = id
                program_1.id = new_id
                db.session.commit()       
                return 

    if direction == "down":
        for program in GET_ALL_PROGRAMS():
            if program.id > id:
                
                new_id = program.id
                
                # change ids
                program_1 = GET_PROGRAM_BY_ID(id)
                program_2 = GET_PROGRAM_BY_ID(new_id)
                
                program_1.id = 99
                db.session.commit()
                
                program_2.id = id
                program_1.id = new_id
                db.session.commit()           
                return 


def ADD_PROGRAM_LINE(id):
    entry = Programs.query.filter_by(id=id).first()

    if entry.line_active_2 != "True":
        entry.line_active_2 = "True"
        db.session.commit()
        return
    if entry.line_active_3 != "True":
        entry.line_active_3 = "True"
        db.session.commit()
        return
    if entry.line_active_4 != "True":
        entry.line_active_4 = "True"
        db.session.commit()
        return
    if entry.line_active_5 != "True":
        entry.line_active_5 = "True"
        db.session.commit()
        return
    if entry.line_active_6 != "True":
        entry.line_active_6 = "True"
        db.session.commit()
        return
    if entry.line_active_7 != "True":
        entry.line_active_7 = "True"
        db.session.commit()
        return
    if entry.line_active_8 != "True":
        entry.line_active_8 = "True"
        db.session.commit()
        return
    if entry.line_active_9 != "True":
        entry.line_active_9 = "True"
        db.session.commit()
        return
    if entry.line_active_10 != "True":
        entry.line_active_10 = "True"
        db.session.commit()
        return
    if entry.line_active_11 != "True":
        entry.line_active_11 = "True"
        db.session.commit()
        return
    if entry.line_active_12 != "True":
        entry.line_active_12 = "True"
        db.session.commit()
        return
    if entry.line_active_13 != "True":
        entry.line_active_13 = "True"
        db.session.commit()
        return
    if entry.line_active_14 != "True":
        entry.line_active_14 = "True"
        db.session.commit()
        return
    if entry.line_active_15 != "True":
        entry.line_active_15 = "True"
        db.session.commit()
        return
    if entry.line_active_16 != "True":
        entry.line_active_16 = "True"
        db.session.commit()
        return
    if entry.line_active_17 != "True":
        entry.line_active_17 = "True"
        db.session.commit()
        return
    if entry.line_active_18 != "True":
        entry.line_active_18 = "True"
        db.session.commit()
        return
    if entry.line_active_19 != "True":
        entry.line_active_19 = "True"
        db.session.commit()
        return
    if entry.line_active_20 != "True":
        entry.line_active_20 = "True"
        db.session.commit()
        return
    if entry.line_active_21 != "True":
        entry.line_active_21 = "True"
        db.session.commit()
        return
    if entry.line_active_22 != "True":
        entry.line_active_22 = "True"
        db.session.commit()
        return
    if entry.line_active_23 != "True":
        entry.line_active_23 = "True"
        db.session.commit()
        return
    if entry.line_active_24 != "True":
        entry.line_active_24 = "True"
        db.session.commit()
        return
    if entry.line_active_25 != "True":
        entry.line_active_25 = "True"
        db.session.commit()
        return
    if entry.line_active_26 != "True":
        entry.line_active_26 = "True"
        db.session.commit()
        return
    if entry.line_active_27 != "True":
        entry.line_active_27 = "True"
        db.session.commit()
        return
    if entry.line_active_28 != "True":
        entry.line_active_28 = "True"
        db.session.commit()
        return
    if entry.line_active_29 != "True":
        entry.line_active_29 = "True"
        db.session.commit()
        return
    if entry.line_active_30 != "True":
        entry.line_active_30 = "True"
        db.session.commit()
        return


def REMOVE_PROGRAM_LINE(id):
    entry = Programs.query.filter_by(id=id).first()

    if entry.line_active_30 == "True":
        entry.line_active_30    = ""
        entry.line_content_30   = ""
        db.session.commit()
        return 
    if entry.line_active_29 == "True":
        entry.line_active_29    = ""
        entry.line_content_29   = ""
        db.session.commit()
        return 
    if entry.line_active_28 == "True":
        entry.line_active_28    = ""
        entry.line_content_28   = ""
        db.session.commit()
        return 
    if entry.line_active_27 == "True":
        entry.line_active_27    = ""
        entry.line_content_27   = ""
        db.session.commit()
        return 
    if entry.line_active_26 == "True":
        entry.line_active_26    = ""
        entry.line_content_26   = ""
        db.session.commit()
        return 
    if entry.line_active_25 == "True":
        entry.line_active_25    = ""
        entry.line_content_25   = ""
        db.session.commit()
        return 
    if entry.line_active_24 == "True":
        entry.line_active_24    = ""
        entry.line_content_24   = ""
        db.session.commit()
        return 
    if entry.line_active_23 == "True":
        entry.line_active_23    = ""
        entry.line_content_23   = ""
        db.session.commit()
        return 
    if entry.line_active_22 == "True":
        entry.line_active_22    = ""
        entry.line_content_22   = ""
        db.session.commit()
        return 
    if entry.line_active_21 == "True":
        entry.line_active_21    = ""
        entry.line_content_21   = ""
        db.session.commit()
        return 
    if entry.line_active_20 == "True":
        entry.line_active_20    = ""
        entry.line_content_20   = ""
        db.session.commit()
        return 
    if entry.line_active_19 == "True":
        entry.line_active_19    = ""
        entry.line_content_19   = ""
        db.session.commit()
        return 
    if entry.line_active_18 == "True":
        entry.line_active_18    = ""
        entry.line_content_18   = ""
        db.session.commit()
        return 
    if entry.line_active_17 == "True":
        entry.line_active_17    = ""
        entry.line_content_17   = ""
        db.session.commit()
        return 
    if entry.line_active_16 == "True":
        entry.line_active_16    = ""
        entry.line_content_16   = ""
        db.session.commit()
        return 
    if entry.line_active_15 == "True":
        entry.line_active_15    = ""
        entry.line_content_15   = ""
        db.session.commit()
        return 
    if entry.line_active_14 == "True":
        entry.line_active_14    = ""
        entry.line_content_14   = ""
        db.session.commit()
        return 
    if entry.line_active_13 == "True":
        entry.line_active_13    = ""
        entry.line_content_13   = ""
        db.session.commit()
        return 
    if entry.line_active_12 == "True":
        entry.line_active_12    = ""
        entry.line_content_12   = ""
        db.session.commit()
        return 
    if entry.line_active_11 == "True":
        entry.line_active_11    = ""
        entry.line_content_11   = ""
        db.session.commit()
        return 
    if entry.line_active_10 == "True":
        entry.line_active_10    = ""
        entry.line_content_10   = ""
        db.session.commit()
        return 
    if entry.line_active_9 == "True":
        entry.line_active_9    = ""
        entry.line_content_9   = ""
        db.session.commit()
        return 
    if entry.line_active_8 == "True":
        entry.line_active_8    = ""
        entry.line_content_8   = ""
        db.session.commit()
        return 
    if entry.line_active_7 == "True":
        entry.line_active_7    = ""
        entry.line_content_7   = ""
        entry.line_exception_7 = ""
        db.session.commit()
        return 
    if entry.line_active_6 == "True":
        entry.line_active_6    = ""
        entry.line_content_6   = ""
        db.session.commit()
        return
    if entry.line_active_5 == "True":
        entry.line_active_5    = ""
        entry.line_content_5   = ""
        db.session.commit()
        return 
    if entry.line_active_4 == "True":
        entry.line_active_4    = ""
        entry.line_content_4   = ""
        db.session.commit()
        return 
    if entry.line_active_3 == "True":
        entry.line_active_3    = ""
        entry.line_content_3   = ""
        db.session.commit()
        return 
    if entry.line_active_2 == "True":
        entry.line_active_2    = ""
        entry.line_content_2   = ""
        db.session.commit()
        return 


def CHANGE_PROGRAM_LINE_POSITION(id, line, direction):
    entry = Programs.query.filter_by(id=id).first()

    if direction == "up":

        if line == 2:
            line_content_temp      = entry.line_content_1
            entry.line_content_1   = entry.line_content_2
            entry.line_content_2   = line_content_temp
            db.session.commit()
        if line == 3:
            line_content_temp      = entry.line_content_2
            entry.line_content_2   = entry.line_content_3
            entry.line_content_3   = line_content_temp
            db.session.commit()
        if line == 4:
            line_content_temp      = entry.line_content_3
            entry.line_content_3   = entry.line_content_4
            entry.line_content_4   = line_content_temp
            db.session.commit()
        if line == 5:
            line_content_temp      = entry.line_content_4
            entry.line_content_4   = entry.line_content_5
            entry.line_content_5   = line_content_temp
            db.session.commit()
        if line == 6:
            line_content_temp      = entry.line_content_5
            entry.line_content_5   = entry.line_content_6
            entry.line_content_6   = line_content_temp
            db.session.commit()
        if line == 7:
            line_content_temp      = entry.line_content_6
            entry.line_content_6   = entry.line_content_7
            entry.line_content_7   = line_content_temp
            db.session.commit()
        if line == 8:
            line_content_temp      = entry.line_content_7
            entry.line_content_7   = entry.line_content_8
            entry.line_content_8   = line_content_temp
            db.session.commit()
        if line == 9:
            line_content_temp      = entry.line_content_8
            entry.line_content_8   = entry.line_content_9
            entry.line_content_9   = line_content_temp
            db.session.commit()
        if line == 10:
            line_content_temp       = entry.line_content_9
            entry.line_content_9    = entry.line_content_10
            entry.line_content_10   = line_content_temp
            db.session.commit()
        if line == 11:
            line_content_temp       = entry.line_content_10
            entry.line_content_10   = entry.line_content_11
            entry.line_content_11   = line_content_temp
            db.session.commit()
        if line == 12:
            line_content_temp       = entry.line_content_11
            entry.line_content_11   = entry.line_content_12
            entry.line_content_12   = line_content_temp
            db.session.commit()
        if line == 13:
            line_content_temp       = entry.line_content_12
            entry.line_content_12   = entry.line_content_13
            entry.line_content_13   = line_content_temp
            db.session.commit()
        if line == 14:
            line_content_temp       = entry.line_content_13
            entry.line_content_13   = entry.line_content_14
            entry.line_content_14   = line_content_temp
            db.session.commit()
        if line == 15:
            line_content_temp       = entry.line_content_14
            entry.line_content_14   = entry.line_content_15
            entry.line_content_15   = line_content_temp
            db.session.commit()
        if line == 16:
            line_content_temp       = entry.line_content_15
            entry.line_content_15   = entry.line_content_16
            entry.line_content_16   = line_content_temp
            db.session.commit()
        if line == 17:
            line_content_temp       = entry.line_content_16
            entry.line_content_16   = entry.line_content_17
            entry.line_content_17   = line_content_temp
            db.session.commit()
        if line == 18:
            line_content_temp       = entry.line_content_17
            entry.line_content_17   = entry.line_content_18
            entry.line_content_18   = line_content_temp
            db.session.commit()
        if line == 19:
            line_content_temp       = entry.line_content_18
            entry.line_content_18   = entry.line_content_19
            entry.line_content_19   = line_content_temp
            db.session.commit()
        if line == 20:
            line_content_temp       = entry.line_content_19
            entry.line_content_19   = entry.line_content_20
            entry.line_content_20   = line_content_temp
            db.session.commit()
        if line == 21:
            line_content_temp       = entry.line_content_20
            entry.line_content_20   = entry.line_content_21
            entry.line_content_21   = line_content_temp
            db.session.commit()
        if line == 22:
            line_content_temp       = entry.line_content_21
            entry.line_content_21   = entry.line_content_22
            entry.line_content_22   = line_content_temp
            db.session.commit()
        if line == 23:
            line_content_temp       = entry.line_content_22
            entry.line_content_22   = entry.line_content_23
            entry.line_content_23   = line_content_temp
            db.session.commit()
        if line == 24:
            line_content_temp       = entry.line_content_23
            entry.line_content_23   = entry.line_content_24
            entry.line_content_24   = line_content_temp
            db.session.commit()
        if line == 25:
            line_content_temp       = entry.line_content_24
            entry.line_content_24   = entry.line_content_25
            entry.line_content_25   = line_content_temp
            db.session.commit()
        if line == 26:
            line_content_temp       = entry.line_content_25
            entry.line_content_25   = entry.line_content_26
            entry.line_content_26   = line_content_temp
            db.session.commit()
        if line == 27:
            line_content_temp       = entry.line_content_26
            entry.line_content_26   = entry.line_content_27
            entry.line_content_27   = line_content_temp
            db.session.commit()
        if line == 28:
            line_content_temp       = entry.line_content_27
            entry.line_content_27   = entry.line_content_28
            entry.line_content_28   = line_content_temp
            db.session.commit()
        if line == 29:
            line_content_temp       = entry.line_content_28
            entry.line_content_28   = entry.line_content_29
            entry.line_content_29   = line_content_temp
            db.session.commit()
        if line == 30:
            line_content_temp       = entry.line_content_29
            entry.line_content_29   = entry.line_content_30
            entry.line_content_30   = line_content_temp
            db.session.commit()

    if direction == "down":

        if line == 1 and entry.line_active_2 == "True":
            line_content_temp      = entry.line_content_2
            entry.line_content_2   = entry.line_content_1
            entry.line_content_1   = line_content_temp 
            db.session.commit()
        if line == 2 and entry.line_active_3 == "True":
            line_content_temp      = entry.line_content_3
            entry.line_content_3   = entry.line_content_2
            entry.line_content_2   = line_content_temp 
            db.session.commit()
        if line == 3 and entry.line_active_4 == "True":
            line_content_temp      = entry.line_content_4
            entry.line_content_4   = entry.line_content_3
            entry.line_content_3   = line_content_temp 
            db.session.commit()
        if line == 4 and entry.line_active_5 == "True":
            line_content_temp      = entry.line_content_5
            entry.line_content_5   = entry.line_content_4
            entry.line_content_4   = line_content_temp 
            db.session.commit()
        if line == 5 and entry.line_active_6 == "True":
            line_content_temp      = entry.line_content_6
            entry.line_content_6   = entry.line_content_5
            entry.line_content_5   = line_content_temp 
            db.session.commit()
        if line == 6 and entry.line_active_7 == "True":
            line_content_temp      = entry.line_content_7
            entry.line_content_7   = entry.line_content_6
            entry.line_content_6   = line_content_temp 
            db.session.commit()
        if line == 7 and entry.line_active_8 == "True":
            line_content_temp      = entry.line_content_8
            entry.line_content_8   = entry.line_content_7
            entry.line_content_7   = line_content_temp 
            db.session.commit()
        if line == 8 and entry.line_active_9 == "True":
            line_content_temp      = entry.line_content_9
            entry.line_content_9   = entry.line_content_8
            entry.line_content_8   = line_content_temp 
            db.session.commit()
        if line == 9 and entry.line_active_10 == "True":
            line_content_temp      = entry.line_content_10
            entry.line_content_10  = entry.line_content_9
            entry.line_content_9   = line_content_temp 
            db.session.commit()
        if line == 10 and entry.line_active_11 == "True":
            line_content_temp      = entry.line_content_11
            entry.line_content_11  = entry.line_content_10
            entry.line_content_10   = line_content_temp 
            db.session.commit()
        if line == 11 and entry.line_active_12 == "True":
            line_content_temp      = entry.line_content_12
            entry.line_content_12  = entry.line_content_11
            entry.line_content_11   = line_content_temp 
            db.session.commit()
        if line == 12 and entry.line_active_13 == "True":
            line_content_temp      = entry.line_content_13
            entry.line_content_13  = entry.line_content_12
            entry.line_content_12   = line_content_temp 
            db.session.commit()
        if line == 13 and entry.line_active_14 == "True":
            line_content_temp      = entry.line_content_14
            entry.line_content_14  = entry.line_content_13
            entry.line_content_13   = line_content_temp 
            db.session.commit()
        if line == 14 and entry.line_active_15 == "True":
            line_content_temp      = entry.line_content_15
            entry.line_content_15  = entry.line_content_14
            entry.line_content_14   = line_content_temp 
            db.session.commit()
        if line == 15 and entry.line_active_16 == "True":
            line_content_temp      = entry.line_content_16
            entry.line_content_16  = entry.line_content_15
            entry.line_content_15   = line_content_temp 
            db.session.commit()
        if line == 16 and entry.line_active_17 == "True":
            line_content_temp      = entry.line_content_17
            entry.line_content_17  = entry.line_content_16
            entry.line_content_16   = line_content_temp 
            db.session.commit()
        if line == 17 and entry.line_active_18 == "True":
            line_content_temp      = entry.line_content_18
            entry.line_content_18  = entry.line_content_17
            entry.line_content_17   = line_content_temp 
            db.session.commit()
        if line == 18 and entry.line_active_19 == "True":
            line_content_temp      = entry.line_content_19
            entry.line_content_19  = entry.line_content_18
            entry.line_content_18   = line_content_temp 
            db.session.commit()
        if line == 19 and entry.line_active_20 == "True":
            line_content_temp      = entry.line_content_20
            entry.line_content_20  = entry.line_content_19
            entry.line_content_19   = line_content_temp 
            db.session.commit()
        if line == 20 and entry.line_active_21 == "True":
            line_content_temp      = entry.line_content_21
            entry.line_content_21  = entry.line_content_20
            entry.line_content_20   = line_content_temp 
            db.session.commit()
        if line == 21 and entry.line_active_22 == "True":
            line_content_temp      = entry.line_content_22
            entry.line_content_22  = entry.line_content_21
            entry.line_content_21   = line_content_temp 
            db.session.commit()
        if line == 22 and entry.line_active_23 == "True":
            line_content_temp      = entry.line_content_23
            entry.line_content_23  = entry.line_content_22
            entry.line_content_22   = line_content_temp 
            db.session.commit()
        if line == 23 and entry.line_active_24 == "True":
            line_content_temp      = entry.line_content_24
            entry.line_content_24  = entry.line_content_23
            entry.line_content_23   = line_content_temp 
            db.session.commit()
        if line == 24 and entry.line_active_25 == "True":
            line_content_temp      = entry.line_content_25
            entry.line_content_25  = entry.line_content_24
            entry.line_content_24   = line_content_temp 
            db.session.commit()
        if line == 25 and entry.line_active_26 == "True":
            line_content_temp      = entry.line_content_26
            entry.line_content_26  = entry.line_content_25
            entry.line_content_25   = line_content_temp 
            db.session.commit()
        if line == 26 and entry.line_active_27 == "True":
            line_content_temp      = entry.line_content_27
            entry.line_content_27  = entry.line_content_26
            entry.line_content_26   = line_content_temp 
            db.session.commit()
        if line == 27 and entry.line_active_28 == "True":
            line_content_temp      = entry.line_content_28
            entry.line_content_28  = entry.line_content_27
            entry.line_content_27   = line_content_temp 
            db.session.commit()
        if line == 28 and entry.line_active_29 == "True":
            line_content_temp      = entry.line_content_29
            entry.line_content_29  = entry.line_content_28
            entry.line_content_28   = line_content_temp 
            db.session.commit()
        if line == 29 and entry.line_active_30 == "True":
            line_content_temp      = entry.line_content_30
            entry.line_content_30  = entry.line_content_29
            entry.line_content_29   = line_content_temp 
            db.session.commit()


def DELETE_PROGRAM(id):
    name = Programs.query.filter_by(id=id).first().name
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Program | " + str(name) + " | deleted")  
    except:
        pass 

    Programs.query.filter_by(id=id).delete()
    db.session.commit() 
    return True


""" ################## """
""" ################## """
"""      scheduler     """
""" ################## """
""" ################## """


def GET_SCHEDULER_TASK_BY_ID(id):
    return Scheduler_Tasks.query.filter_by(id=id).first()


def GET_SCHEDULER_TASK_BY_NAME(name):
    for task in Scheduler_Tasks.query.all():
        
        if task.name.lower() == name.lower():
            return task    
    

def GET_ALL_SCHEDULER_TASKS():
    return Scheduler_Tasks.query.all()    


def ADD_SCHEDULER_TASK():
    for i in range(1,31):
        if Scheduler_Tasks.query.filter_by(id=i).first():
            pass
        else:
            # add the new task
            new_task = Scheduler_Tasks(
                    id            = i,
                    name          = "new_scheduler_task_" + str(i),
                    visible       = "True",
                    option_repeat = "True",
                )
            db.session.add(new_task)
            db.session.commit()

            SET_SCHEDULER_TASK_COLLAPSE_OPEN(i)
        
            WRITE_LOGFILE_SYSTEM("DATABASE", "Scheduler | Task - " + "new_scheduler_task_" + str(i) + " | added")             
            return True

    return "Limit reached (30)"


def SET_SCHEDULER_TASK(id, name, task,
                       trigger_time, trigger_sun_position, trigger_sensors, trigger_position, option_repeat, option_pause, 
                       day, hour, minute, 
                       option_sunrise, option_sunset, latitude, longitude,
                       device_ieeeAddr_1, device_name_1, device_input_values_1, sensor_key_1, operator_1, value_1, main_operator_second_sensor,
                       device_ieeeAddr_2, device_name_2, device_input_values_2, sensor_key_2, operator_2, value_2, 
                       option_home, option_away, ip_addresses):
                             
    entry         = Scheduler_Tasks.query.filter_by(id=id).first()
    previous_name = entry.name

    # values changed ?
    if (entry.name != name or entry.task != task or entry.trigger_time != trigger_time or
        entry.trigger_sun_position != trigger_sun_position or entry.trigger_sensors != trigger_sensors or 
        entry.trigger_position != trigger_position or entry.option_repeat != option_repeat or entry.option_pause != option_pause or 
        entry.day != day or entry.hour != hour or entry.minute != minute or
        entry.option_sunrise != option_sunrise or entry.option_sunset != option_sunset or str(entry.latitude) != str(latitude) or str(entry.longitude) != str(longitude) or 
        entry.device_ieeeAddr_1 != device_ieeeAddr_1 or entry.sensor_key_1 != sensor_key_1 or 
        entry.operator_1 != operator_1 or str(entry.value_1) != str(value_1)  or entry.main_operator_second_sensor != main_operator_second_sensor or 
        entry.device_ieeeAddr_2 != device_ieeeAddr_2 or entry.sensor_key_2 != sensor_key_2 or 
        entry.operator_2 != operator_2 or str(entry.value_2) != str(value_2) or
        entry.option_home != option_home or entry.option_away != option_away or entry.ip_addresses != ip_addresses):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + str(entry.name) + " >>> " + str(name)
        if entry.task != task:
            changes = changes + " || task || " + str(entry.task) + " >>> " + str(task)           

        if entry.trigger_time != trigger_time or entry.trigger_sun_position != trigger_sun_position or entry.trigger_sensors != trigger_sensors or entry.trigger_position != trigger_position:
            changes = (changes + " || trigger_settings || time: " + str(entry.trigger_time) + ", sun_position: " + str(entry.trigger_sun_position) + ", sensors: " + str(entry.trigger_sensors) + ", position: " + str(entry.trigger_position) + 
                                 " >>> time: " + str(trigger_time) + ", sun_position: " + str(trigger_sun_position) + ", sensors: " + str(trigger_sensors) + ", position: " + str(trigger_position)) 
    
        if entry.option_repeat != option_repeat or entry.option_pause != option_pause:
            changes = (changes + " || options_settings || repeat: " + str(entry.option_repeat) + ", pause: " + str(entry.option_pause) +
                                 " >>> repeat: " + str(option_repeat) + ", pause: " + str(option_pause)) 
      
        if trigger_time == "True": 

            if entry.day != day or entry.hour != hour or entry.minute != minute:
                changes = (changes + " || time_settings || days: " + str(entry.day)  + ", hours: " + str(entry.hour)  + ", minutes: " + str(entry.minute) + 
                                    " >>> days: " + str(day)  + ", hours: " + str(hour)  + ", minutes: " + str(minute))

        if trigger_sun_position == "True":      

            if entry.option_sunrise != option_sunrise or entry.option_sunset != option_sunset or str(entry.latitude) != str(latitude) or str(entry.longitude) != str(longitude):
                changes = (changes + " || sun_position_settings || option_sunrise: " + str(entry.option_sunrise) + ", option_sunset: " + str(entry.option_sunset) + ", latitude: " + str(entry.latitude) + ", longitude: " + str(entry.longitude) +  
                                    " >>> option_sunrise: " + str(option_sunrise) + ", option_sunset: " + str(option_sunset) + ", latitude: " + str(latitude) + ", longitude: " + str(longitude))        
  
        if trigger_sensors == "True":

            previous_device_1 = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_1)
            previous_device_2 = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_2)

            try:
                previous_name_1 = previous_device_1.name
                previous_name_2 = previous_device_2.name

            except:
                previous_name_1 = "None"
                previous_name_2 = "None"               

            new_device_1 = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1)
            new_device_2 = GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2)

            try:
                new_name_1 = new_device_1.name
                new_name_2 = new_device_2.name

            except:
                new_name_1 = "None"
                new_name_2 = "None"       

            if (entry.device_ieeeAddr_1 != device_ieeeAddr_1 or entry.sensor_key_1 != sensor_key_1 or entry.operator_1 != operator_1 or str(entry.value_1) != str(value_1) or entry.main_operator_second_sensor != main_operator_second_sensor or
                entry.device_ieeeAddr_2 != device_ieeeAddr_2 or entry.sensor_key_2 != sensor_key_2 or entry.operator_2 != operator_2 or str(entry.value_2) != str(value_2)):

                changes = (changes + " || sensor_settings || (" + 
                                    str(previous_name_1) + ": " + str(entry.sensor_key_1)  + " " + str(entry.operator_1) + " " + str(entry.value_1) + ") " + str(entry.main_operator_second_sensor) + " (" +
                                    str(previous_name_2) + ": " + str(entry.sensor_key_2)  + " " + str(entry.operator_2) + " " + str(entry.value_2) +
                                    ") >>> (" + str(new_name_1) + ": " + str(sensor_key_1)  + " " + str(operator_1) + " " + str(value_1) + ") " + str(main_operator_second_sensor) + " (" +
                                    str(new_name_2) + ": " + str(sensor_key_2)  + " " + str(operator_2) + " " + str(value_2) + ")")

        if trigger_position == "True":      

            if entry.option_home != option_home or entry.option_away != option_away or entry.ip_addresses != ip_addresses:
                changes = (changes + " || position_settings || option_home: " + str(entry.option_home)  + ", option_away: " + str(entry.option_away)  + ", ip_addresses: " + str(entry.ip_addresses) + 
                                    " >>> option_home: " + str(option_home)  + ", option_away: " + str(option_away)  + ", ip_addresses: " + str(ip_addresses))

        entry.name                        = name
        entry.task                        = task      
        entry.trigger_time                = trigger_time    
        entry.trigger_sun_position        = trigger_sun_position            
        entry.trigger_sensors             = trigger_sensors
        entry.trigger_position            = trigger_position        
        entry.option_repeat               = option_repeat
        entry.option_pause                = option_pause
        entry.day                         = day
        entry.hour                        = hour
        entry.minute                      = minute
        entry.option_sunrise              = option_sunrise
        entry.option_sunset               = option_sunset
        entry.latitude                    = latitude        
        entry.longitude                   = longitude          
        entry.device_ieeeAddr_1           = device_ieeeAddr_1
        entry.device_name_1               = device_name_1
        entry.device_input_values_1       = device_input_values_1
        entry.sensor_key_1                = sensor_key_1
        entry.operator_1                  = operator_1
        entry.value_1                     = value_1
        entry.main_operator_second_sensor = main_operator_second_sensor
        entry.device_ieeeAddr_2           = device_ieeeAddr_2
        entry.device_name_2               = device_name_2
        entry.device_input_values_2       = device_input_values_2
        entry.sensor_key_2                = sensor_key_2
        entry.operator_2                  = operator_2
        entry.value_2                     = value_2         
        entry.option_home                 = option_home
        entry.option_away                 = option_away
        entry.ip_addresses                = ip_addresses

        db.session.commit()   

        WRITE_LOGFILE_SYSTEM("DATABASE", "Scheduler | Task - " + str(previous_name) + " | changed" + changes) 
        return True


def SET_SCHEDULER_TASK_ERRORS(id, task_errors):
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    if entry.task_errors != task_errors:
        entry.task_errors = task_errors       
        db.session.commit()     


def SET_SCHEDULER_TASK_SETTING_ERRORS(id, task_setting_errors):
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    if entry.task_setting_errors != task_setting_errors:
        entry.task_setting_errors = task_setting_errors       
        db.session.commit()     


def SET_SCHEDULER_TASK_COLLAPSE_OPEN(id):
    list_scheduler_tasks = Scheduler_Tasks.query.all()
    
    for scheduler_task in list_scheduler_tasks:
        scheduler_task.collapse = ""
        db.session.commit()   
  
    entry = Scheduler_Tasks.query.filter_by(id=id).first()
    
    entry.collapse = "True"
    db.session.commit()       
 
 
def RESET_SCHEDULER_TASK_COLLAPSE():
    list_scheduler_tasks = Scheduler_Tasks.query.all()
    
    for scheduler_task in list_scheduler_tasks:
        scheduler_task.collapse = ""
        db.session.commit()   
  

def GET_SCHEDULER_TASK_SUNRISE(id):    
    return (Scheduler_Tasks.query.filter_by(id=id).first().sunrise)
    

def SET_SCHEDULER_TASK_SUNRISE(id, sunrise):    
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    entry.sunrise = sunrise
    db.session.commit()   


def GET_SCHEDULER_TASK_SUNSET(id):    
    return (Scheduler_Tasks.query.filter_by(id=id).first().sunset)


def SET_SCHEDULER_TASK_SUNSET(id, sunset):    
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    entry.sunset = sunset
    db.session.commit()   


def ADD_SCHEDULER_TASK_SECOND_SENSOR(id):
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    if entry.main_operator_second_sensor == "None" or entry.main_operator_second_sensor == None:
        entry.main_operator_second_sensor = "and"

    db.session.commit()


def REMOVE_SCHEDULER_TASK_SECOND_SENSOR(id):
    entry = Scheduler_Tasks.query.filter_by(id=id).first()
    
    if entry.main_operator_second_sensor != "None":
        entry.main_operator_second_sensor = "None"

    db.session.commit()


def CHANGE_SCHEDULER_TASK_POSITION(id, direction):
    
    list_scheduler_tasks = Scheduler_Tasks.query.all() 
    
    if direction == "up":
        
        # reverse task list
        task_list = list_scheduler_tasks[::-1]
        
        for task in task_list:  
            if task.id < id:
                
                new_id = task.id
                
                # change ids
                task_1 = GET_SCHEDULER_TASK_BY_ID(id)
                task_2 = GET_SCHEDULER_TASK_BY_ID(new_id)
                
                task_1.id = 99
                db.session.commit()
                
                task_2.id = id
                task_1.id = new_id
                db.session.commit()         
                return 

    if direction == "down":
        for task in list_scheduler_tasks:
            if task.id > id:       
                new_id = task.id
                
                # change ids
                task_1 = GET_SCHEDULER_TASK_BY_ID(id)
                task_2 = GET_SCHEDULER_TASK_BY_ID(new_id)
                
                task_1.id = 99
                db.session.commit()
                
                task_2.id = id
                task_1.id = new_id
                db.session.commit()      
                return 
       
       
def UPDATE_SCHEDULER_TASKS_DEVICE_NAMES():
    tasks = GET_ALL_SCHEDULER_TASKS()
    
    for task in tasks:
        
        entry = Scheduler_Tasks.query.filter_by(id=task.id).first()
        
        try:
            entry.device_name_1         = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_1).name
            entry.device_input_values_1 = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_1).input_values
        except:
            pass
        try:
            entry.device_name_2         = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_2).name
            entry.device_input_values_2 = GET_DEVICE_BY_IEEEADDR(entry.device_ieeeAddr_2).input_values
        except:
            pass 
        
    db.session.commit()
            

def DELETE_SCHEDULER_TASK(task_id):
    entry = GET_SCHEDULER_TASK_BY_ID(task_id)
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Scheduler | Task - " + str(entry.name) + " | deleted")   
    except:
        pass         
    
    Scheduler_Tasks.query.filter_by(id=task_id).delete()
    db.session.commit()
    return True


""" ################### """
""" ################### """
"""   sensordata jobs   """
""" ################### """
""" ################### """


def GET_SENSORDATA_JOB_BY_ID(id):
    return Sensordata_Jobs.query.filter_by(id=id).first()


def GET_SENSORDATA_JOB_BY_NAME(name):
    for job in Sensordata_Jobs.query.all():
        
        if job.name.lower() == name.lower():
            return job   
            
            
def GET_ALL_SENSORDATA_JOBS():
    return Sensordata_Jobs.query.all()
    

def ADD_SENSORDATA_JOB():
    for i in range(1,26):
        if Sensordata_Jobs.query.filter_by(id=i).first():
            pass
        else:
            # add the new job
            sensordata_job = Sensordata_Jobs(
                    id   = i,
                    name = "new_job_" + str(i),           
                )
            db.session.add(sensordata_job)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + "new_job_" + str(i) + " | added")                    
            return True

    return "Limit reached (25)"


def SET_SENSORDATA_JOB_SETTINGS(id, name, filename, device_ieeeAddr, sensor_key, always_active):        
    entry         = Sensordata_Jobs.query.filter_by(id=id).first()
    previous_name = entry.name

    # values changed?
    if (entry.name != name or entry.filename != filename or entry.device_ieeeAddr != device_ieeeAddr or 
        entry.sensor_key != sensor_key or entry.always_active != always_active):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + str(entry.name) + " >>> " + str(name)
        if entry.filename != filename:
            changes = changes + " || filename || " + str(entry.filename) + " >>> " + str(filename)            
        if entry.sensor_key != sensor_key:
            changes = changes + " || sensor_key || " + str(entry.sensor_key) + " >>> " + str(sensor_key)        
        if entry.always_active != always_active:
            changes = changes + " || always_active || " + str(entry.always_active) + " >>> " + str(always_active)       

        entry.name = name
        entry.filename = filename
        entry.device_ieeeAddr =device_ieeeAddr
        entry.sensor_key = sensor_key
        entry.always_active = always_active
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + str(previous_name) + " | changed" + changes)   
        return True 


def CHANGE_SENSORDATA_JOB_POSITION(id, direction): 
    if direction == "up":
        sensordata_jobs_list = GET_ALL_SENSORDATA_JOBS()
        sensordata_jobs_list = sensordata_jobs_list[::-1]
        
        for sensordata_job in sensordata_jobs_list:
            
            if sensordata_job.id < id:  
                new_id = sensordata_job.id
                
                # change ids
                sensordata_job_1 = GET_SENSORDATA_JOB_BY_ID(id)
                sensordata_job_2 = GET_SENSORDATA_JOB_BY_ID(new_id)
                
                sensordata_job_1.id = 99
                db.session.commit()
                
                sensordata_job_2.id = id
                sensordata_job_1.id = new_id
                db.session.commit()    
                return 

    if direction == "down":
        for sensordata_job in GET_ALL_SENSORDATA_JOBS():
            if sensordata_job.id > id:    
                new_id = sensordata_job.id
                
                # change ids
                sensordata_job_1 = GET_SENSORDATA_JOB_BY_ID(id)
                sensordata_job_2 = GET_SENSORDATA_JOB_BY_ID(new_id)
                
                sensordata_job_1.id = 99
                db.session.commit()
                
                sensordata_job_2.id = id
                sensordata_job_1.id = new_id
                db.session.commit()    
                return 


def DELETE_SENSORDATA_JOB(id):
    entry = GET_SENSORDATA_JOB_BY_ID(id)
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + str(entry.name) + " | deleted")
    except:
        pass     
 
    Sensordata_Jobs.query.filter_by(id=id).delete()
    db.session.commit()
    return True


""" ################### """
""" ################### """
"""       spotitfy      """
""" ################### """
""" ################### """

    
def GET_SPOTIFY_SETTINGS():
    return Spotify_Settings.query.filter_by().first()


def SET_SPOTIFY_SETTINGS(client_id, client_secret):
    entry = Spotify_Settings.query.filter_by().first()

    # values changed ?
    if (entry.client_id != client_id or entry.client_secret != client_secret):    

        changes = ""

        if entry.client_id != client_id:
            changes = changes + " || client_id || " + str(entry.client_id) + " >>> " + str(client_id)
        if entry.client_secret != client_secret:
            changes = changes + " || client_secret || " + str(entry.client_secret) + " >>> " + str(client_secret)      

        entry.client_id     = client_id
        entry.client_secret = client_secret   
        db.session.commit()

        WRITE_LOGFILE_SYSTEM("DATABASE", "Music | Spotify | Client Settings | changed" + changes) 
        return True


def GET_SPOTIFY_REFRESH_TOKEN():
    return Spotify_Settings.query.filter_by().first().refresh_token


def SET_SPOTIFY_REFRESH_TOKEN(refresh_token):
    entry = Spotify_Settings.query.filter_by().first()

    # values changed ?
    if (entry.refresh_token != refresh_token):    

        entry.refresh_token = refresh_token
        db.session.commit()
        return True


def SET_SPOTIFY_DEFAULT_SETTINGS(default_device_id, default_device_name, default_playlist_uri, default_playlist_name, default_volume, default_shuffle):
    entry = Spotify_Settings.query.filter_by().first()

    # values changed ?
    if (entry.default_device_id != default_device_id or entry.default_device_name != default_device_name or
        entry.default_playlist_uri != default_playlist_uri or entry.default_playlist_name != default_playlist_name or
        int(entry.default_volume) != int(default_volume) or entry.default_shuffle != default_shuffle):    

        changes = ""

        if entry.default_device_name != default_device_name:
            changes = changes + " || default_device_name || " + str(entry.default_device_name) + " >>> " + str(default_device_name)
        if entry.default_playlist_name != default_playlist_name:
            changes = changes + " || default_playlist_name || " + str(entry.default_playlist_name) + " >>> " + str(default_playlist_name)            
        if int(entry.default_volume) != int(default_volume):
            changes = changes + " || default_volume || " + str(entry.default_volume) + " >>> " + str(default_volume)        
        if entry.default_shuffle != default_shuffle:
            changes = changes + " || default_shuffle || " + str(entry.default_shuffle) + " >>> " + str(default_shuffle)       

        entry.default_device_id     = default_device_id
        entry.default_device_name   = default_device_name
        entry.default_playlist_uri  = default_playlist_uri
        entry.default_playlist_name = default_playlist_name
        entry.default_volume        = default_volume       
        entry.default_shuffle       = default_shuffle               
        db.session.commit()

        if changes != "":
            WRITE_LOGFILE_SYSTEM("DATABASE", "Music | Spotify | Default Player Settings | changed" + changes) 

        return True


""" ################### """
""" ################### """
"""        system       """
""" ################### """
""" ################### """


def GET_SYSTEM_SETTINGS():
    return System.query.filter_by().first()


def SET_SYSTEM_NETWORK_SETTINGS(ip_address, gateway, port, dhcp):
    entry = System.query.filter_by().first()

    # values changed ?
    if entry.ip_address != ip_address or entry.gateway != gateway or entry.port != port or entry.dhcp != dhcp:   
     
        entry.ip_address = ip_address
        entry.gateway    = gateway  
        entry.port       = port          
        entry.dhcp       = dhcp 
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | Network | changed") 

        return True


def SET_SYSTEM_SERVICE_SETTINGS(zigbee2mqtt_active, lms_active, squeezelite_active):
                             
    entry = System.query.filter_by().first()

    # values changed ?
    if (entry.zigbee2mqtt_active != zigbee2mqtt_active or entry.lms_active != lms_active or entry.squeezelite_active != squeezelite_active):

        changes = ""

        if entry.zigbee2mqtt_active != zigbee2mqtt_active:
            changes = changes + " || zigbee2mqtt_active_setting || " + str(entry.zigbee2mqtt_active) + " >>> " + str(zigbee2mqtt_active)
        if entry.lms_active != lms_active:
            changes = changes + " || lms_active_setting || " + str(entry.lms_active) + " >>> " + str(lms_active)            
        if entry.squeezelite_active != squeezelite_active:
            changes = changes + " || squeezelite_active_setting || " + str(entry.squeezelite_active) + " >>> " + str(squeezelite_active)        

        entry.zigbee2mqtt_active   = zigbee2mqtt_active    
        entry.lms_active           = lms_active   
        entry.squeezelite_active   = squeezelite_active               
        db.session.commit()   

        WRITE_LOGFILE_SYSTEM("DATABASE", "System | Services | changed" + changes) 
        return True


""" ################### """
""" ################### """
"""   user management   """
""" ################### """
""" ################### """


def GET_USER_BY_ID(id):
    return User.query.get(int(id))


def GET_USER_BY_NAME(name):
    for user in User.query.all():
        
        if user.name.lower() == name.lower():
            return user       
 

def GET_USER_BY_EMAIL(email):
    return User.query.filter_by(email=email).first()  


def GET_ALL_USERS():
    return User.query.all()  
    

def ADD_USER():
    for i in range(1,11):
        if User.query.filter_by(id=i).first():
            pass
        else:
            # add the new user
            new_user = User(
                    id   = i,
                    name = "new_user_" + str(i),
                )
            db.session.add(new_user)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + "new_user_" + str(i) + " | added") 
            return True

    return "Limit reached (10)"        


def UPDATE_USER_SETTINGS(id, name, email, role, email_notification):     
    entry         = User.query.filter_by(id=id).first()
    previous_name = entry.name

    # values changed ?
    if (entry.name != name or entry.email != email or entry.role != role or entry.email_notification != email_notification):

        changes = ""

        if entry.name != name:
            changes = changes + " || name || " + str(entry.name) + " >>> " + str(name)
        if entry.email != email:
            changes = changes + " || email || " + str(entry.email) + " >>> " + str(email)            
        if entry.role != role:
            changes = changes + " || role || " + str(entry.role) + " >>> " + str(role)        
        if entry.email_notification != email_notification:
            changes = changes + " || email_notification_setting || " + str(entry.email_notification) + " >>> " + str(email_notification)        

        entry.name               = name
        entry.email              = email
        entry.role               = role 
        entry.email_notification = email_notification
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + str(previous_name) + " | changed" + changes)

        return True


def CHANGE_USER_PASSWORD(id, hashed_password):
    entry = User.query.filter_by(id=id).first()

    # values changed ?
    if entry.password != hashed_password:    
    
        entry.password = hashed_password    
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + str(entry.name) + " | Password changed")
        return True
    

def DELETE_USER(user_id):
    entry = GET_USER_BY_ID(user_id)

    if entry.name != "admin":

        try:
            WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + str(entry.name) + " | deleted")    
            User.query.filter_by(id=user_id).delete()
            db.session.commit()    
            return True

        except Exception as e:
                return(e)

    else:
        return "User 'admin' cannot be deleted"