from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


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
    url             = db.Column(db.String(50))
    user            = db.Column(db.String(50))
    password        = db.Column(db.String(50))   

class Controller(db.Model):
    __tablename__   = 'controller'
    id              = db.Column(db.Integer, primary_key=True, autoincrement = True)
    device_ieeeAddr = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr')) 
    device          = db.relationship('Devices') 
    command_1       = db.Column(db.String(50))
    task_1          = db.Column(db.String(50))
    command_2       = db.Column(db.String(50))
    task_2          = db.Column(db.String(50))
    command_3       = db.Column(db.String(50))
    task_3          = db.Column(db.String(50))    
    command_4       = db.Column(db.String(50))
    task_4          = db.Column(db.String(50))
    command_5       = db.Column(db.String(50))
    task_5          = db.Column(db.String(50))
    command_6       = db.Column(db.String(50))
    task_6          = db.Column(db.String(50))   
    command_7       = db.Column(db.String(50))
    task_7          = db.Column(db.String(50))
    command_8       = db.Column(db.String(50))
    task_8          = db.Column(db.String(50))
    command_9       = db.Column(db.String(50))
    task_9          = db.Column(db.String(50))   
    command_10      = db.Column(db.String(50))
    task_10         = db.Column(db.String(50))   
    command_11      = db.Column(db.String(50))
    task_11         = db.Column(db.String(50))   
    command_12      = db.Column(db.String(50))
    task_12         = db.Column(db.String(50))       
    command_13      = db.Column(db.String(50))
    task_13         = db.Column(db.String(50))       
    command_14      = db.Column(db.String(50))
    task_14         = db.Column(db.String(50))       
    command_15      = db.Column(db.String(50))
    task_15         = db.Column(db.String(50))       
    command_16      = db.Column(db.String(50))
    task_16         = db.Column(db.String(50))       
    command_17      = db.Column(db.String(50))
    task_17         = db.Column(db.String(50))       
    command_18      = db.Column(db.String(50))
    task_18         = db.Column(db.String(50))       
    command_19      = db.Column(db.String(50))
    task_19         = db.Column(db.String(50))       
    command_20      = db.Column(db.String(50))
    task_20         = db.Column(db.String(50))       
    collapse        = db.Column(db.String(50))        

class Devices(db.Model):
    __tablename__ = 'devices'
    id                            = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                          = db.Column(db.String(50), unique=True)
    gateway                       = db.Column(db.String(50)) 
    ieeeAddr                      = db.Column(db.String(50), unique=True)  
    model                         = db.Column(db.String(50))
    device_type                   = db.Column(db.String(50))
    description                   = db.Column(db.String(200))
    input_values                  = db.Column(db.String(200))
    input_events                  = db.Column(db.String(200))
    commands                      = db.Column(db.String(200))    
    commands_json                 = db.Column(db.String(200))     
    last_contact                  = db.Column(db.String(50))
    last_values_json              = db.Column(db.String(200))  
    last_values_string            = db.Column(db.String(200)) 
    exception_option              = db.Column(db.String(50), server_default=("None")) 
    exception_setting             = db.Column(db.String(50), server_default=("None"))     
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
    light_ieeeAddr_1        = db.Column(db.String(50))
    light_name_1            = db.Column(db.String(50))
    light_device_type_1     = db.Column(db.String(50))
    active_light_2          = db.Column(db.String(50))
    light_ieeeAddr_2        = db.Column(db.String(50))           
    light_name_2            = db.Column(db.String(50))
    light_device_type_2     = db.Column(db.String(50))
    active_light_3          = db.Column(db.String(50))
    light_ieeeAddr_3        = db.Column(db.String(50))           
    light_name_3            = db.Column(db.String(50))
    light_device_type_3     = db.Column(db.String(50))
    active_light_4          = db.Column(db.String(50))
    light_ieeeAddr_4        = db.Column(db.String(50))       
    light_name_4            = db.Column(db.String(50))
    light_device_type_4     = db.Column(db.String(50))
    active_light_5          = db.Column(db.String(50))
    light_ieeeAddr_5        = db.Column(db.String(50))         
    light_name_5            = db.Column(db.String(50)) 
    light_device_type_5     = db.Column(db.String(50))
    active_light_6          = db.Column(db.String(50))
    light_ieeeAddr_6        = db.Column(db.String(50))
    light_name_6            = db.Column(db.String(50))
    light_device_type_6     = db.Column(db.String(50))
    active_light_7          = db.Column(db.String(50))
    light_ieeeAddr_7        = db.Column(db.String(50))
    light_name_7            = db.Column(db.String(50))
    light_device_type_7     = db.Column(db.String(50))
    active_light_8          = db.Column(db.String(50))
    light_ieeeAddr_8        = db.Column(db.String(50))
    light_name_8            = db.Column(db.String(50))
    light_device_type_8     = db.Column(db.String(50))
    active_light_9          = db.Column(db.String(50))
    light_ieeeAddr_9        = db.Column(db.String(50))
    light_name_9            = db.Column(db.String(50)) 
    light_device_type_9     = db.Column(db.String(50))
    collapse                = db.Column(db.String(50))    
    current_scene           = db.Column(db.String(50), server_default=("OFF"))
    current_brightness      = db.Column(db.Integer, server_default=("0"))

class Lighting_Scenes(db.Model):
    __tablename__ = 'lighting_scenes'
    id             = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name           = db.Column(db.String(50), unique = True) 
    red_1          = db.Column(db.Integer) 
    green_1        = db.Column(db.Integer) 
    blue_1         = db.Column(db.Integer) 
    brightness_1   = db.Column(db.Integer) 
    active_light_2 = db.Column(db.String(50))
    red_2          = db.Column(db.Integer) 
    green_2        = db.Column(db.Integer) 
    blue_2         = db.Column(db.Integer) 
    brightness_2   = db.Column(db.Integer)     
    active_light_3 = db.Column(db.String(50))
    red_3          = db.Column(db.Integer) 
    green_3        = db.Column(db.Integer) 
    blue_3         = db.Column(db.Integer) 
    brightness_3   = db.Column(db.Integer) 
    active_light_4 = db.Column(db.String(50))
    red_4          = db.Column(db.Integer) 
    green_4        = db.Column(db.Integer) 
    blue_4         = db.Column(db.Integer) 
    brightness_4   = db.Column(db.Integer) 
    active_light_5 = db.Column(db.String(50))
    red_5          = db.Column(db.Integer) 
    green_5        = db.Column(db.Integer) 
    blue_5         = db.Column(db.Integer) 
    brightness_5   = db.Column(db.Integer) 
    active_light_6 = db.Column(db.String(50))
    red_6          = db.Column(db.Integer) 
    green_6        = db.Column(db.Integer) 
    blue_6         = db.Column(db.Integer) 
    brightness_6   = db.Column(db.Integer) 
    active_light_7 = db.Column(db.String(50))
    red_7          = db.Column(db.Integer) 
    green_7        = db.Column(db.Integer) 
    blue_7         = db.Column(db.Integer) 
    brightness_7   = db.Column(db.Integer) 
    active_light_8 = db.Column(db.String(50))
    red_8          = db.Column(db.Integer) 
    green_8        = db.Column(db.Integer) 
    blue_8         = db.Column(db.Integer) 
    brightness_8   = db.Column(db.Integer) 
    active_light_9 = db.Column(db.String(50))
    red_9          = db.Column(db.Integer) 
    green_9        = db.Column(db.Integer) 
    blue_9         = db.Column(db.Integer) 
    brightness_9   = db.Column(db.Integer) 
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
    trigger_time                = db.Column(db.String(50)) 
    trigger_sun_position        = db.Column(db.String(50))
    trigger_sensors             = db.Column(db.String(50))
    trigger_position            = db.Column(db.String(50))
    option_repeat               = db.Column(db.String(50))
    option_pause                = db.Column(db.String(50))
    day                         = db.Column(db.String(50))
    hour                        = db.Column(db.String(50))
    minute                      = db.Column(db.String(50))
    option_sunrise              = db.Column(db.String(50))
    option_sunset               = db.Column(db.String(50))
    latitude                    = db.Column(db.String(50))
    longitude                   = db.Column(db.String(50))    
    sunrise                     = db.Column(db.String(50))
    sunset                      = db.Column(db.String(50))    
    device_ieeeAddr_1           = db.Column(db.String(50))
    device_name_1               = db.Column(db.String(50))
    device_input_values_1       = db.Column(db.String(50))
    sensor_key_1                = db.Column(db.String(50))
    value_1                     = db.Column(db.String(50))
    operator_1                  = db.Column(db.String(50))
    main_operator_second_sensor = db.Column(db.String(50), server_default=("None"))
    device_ieeeAddr_2           = db.Column(db.String(50))
    device_name_2               = db.Column(db.String(50))
    device_input_values_2       = db.Column(db.String(50))
    sensor_key_2                = db.Column(db.String(50))
    value_2                     = db.Column(db.String(50))
    operator_2                  = db.Column(db.String(50))
    option_home                 = db.Column(db.String(50))
    option_away                 = db.Column(db.String(50))
    ip_addresses                = db.Column(db.String(50))
    collapse                    = db.Column(db.String(50))

class Sensordata_Jobs(db.Model):
    __tablename__  = 'sensordata_jobs'
    id              = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name            = db.Column(db.String(50), unique=True)
    filename        = db.Column(db.String(50))
    device_ieeeAddr = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr'))  
    device          = db.relationship('Devices')  
    sensor_key      = db.Column(db.String(50)) 
    always_active   = db.Column(db.String(50))

class Spotify_Settings(db.Model):
    __tablename__ = 'spotify_settings'
    id                    = db.Column(db.Integer, primary_key=True, autoincrement = True)
    client_id             = db.Column(db.String(50))
    client_secret         = db.Column(db.String(50))   
    refresh_token         = db.Column(db.String(50))   
    default_device_id     = db.Column(db.String(50))   
    default_device_name   = db.Column(db.String(50))       
    default_playlist_uri  = db.Column(db.String(50))   
    default_playlist_name = db.Column(db.String(50))   
    default_volume        = db.Column(db.Integer, server_default=("0"))

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
    email              = db.Column(db.String(120), unique = True)
    role               = db.Column(db.String(50))   
    password           = db.Column(db.String(100))
    email_notification = db.Column(db.String(20))


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

update_devices_founded       = False
backup_database_founded      = False
reset_log_files_founded      = False

for task in Scheduler_Tasks.query.all():
    if task.name.lower() == "update_devices":
        update_devices_founded = True
    if task.name.lower() == "backup_database":
        backup_database_founded = True
    if task.name.lower() == "reset_log_files":
        reset_log_files_founded = True


if update_devices_founded == False:
    scheduler_task_update_devices = Scheduler_Tasks(
        name           = "update_devices",
        task           = "update_devices",
        visible        = "False",
        trigger_time   = "True",
        option_repeat  = "True",
        day            = "*",        
        hour           = "*",
        minute         = "30",       
    )
    db.session.add(scheduler_task_update_devices)
    db.session.commit()

if backup_database_founded == False:
    scheduler_task_backup_database = Scheduler_Tasks(
        name          = "backup_database",
        task          = "backup_database",
        visible       = "False",        
        trigger_time  = "True",
        option_repeat = "True",
        day           = "*",        
        hour          = "00",
        minute        = "00",        
    )
    db.session.add(scheduler_task_backup_database)
    db.session.commit()
    
if reset_log_files_founded == False:
    scheduler_task_reset_log_files = Scheduler_Tasks(
        name          = "reset_log_files",
        task          = "reset_log_files",
        visible       = "False",        
        trigger_time  = "True",
        option_repeat = "True",
        day           = "*",        
        hour          = "01",
        minute        = "00",        
    )
    db.session.add(scheduler_task_reset_log_files)
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
        id                 = 0,
        name               = "admin",
        email              = "member@example.com",
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
    entry = Camera.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.url != url or entry.user != user or entry.password != password):

        entry.name     = name
        entry.url      = url
        entry.user     = user     
        entry.password = password                       
        db.session.commit()  
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Camera - " + old_name + " | changed")

        return True


def CHANGE_CAMERAS_POSITION(id, direction): 
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
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Camera - " + camera_name + " | deleted")   
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

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Controller - " + controller_name + " | Changed")  
        return True


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

    if selector == "controller":
        for device in devices:
            if device.device_type == "controller":        
                device_list.append(device)      
 
    if selector == "devices":
        for device in devices:
            if (device.device_type == "power_switch" or
                device.device_type == "blind" or
                device.device_type == "heater_thermostat" or
                device.device_type == "watering_controller"):
                
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
                device.device_type == "heater_thermostat" or
                device.device_type == "watering_controller"):
                
                device_list.append(device)   
 
    return device_list    
        

def ADD_DEVICE(name, gateway, ieeeAddr, model = "", device_type = "", description = "", input_values = "", 
               input_events = "", commands = "", commands_json = "", last_contact = ""):
        
    # path exist ?
    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):   
            
        # find a unused id
        for i in range(1,51):
            
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
                        description      = description,
                        input_values     = str(input_values),
                        input_events     = str(input_events),
                        commands         = str(commands),   
                        commands_json    = str(commands_json),                                           
                        last_contact     = last_contact,
                        exception_option = "None"
                        )
                        
                db.session.add(device)
                db.session.commit()
                
                SET_DEVICE_LAST_CONTACT(ieeeAddr)   

                if device_type == "controller":
                    ADD_CONTROLLER(ieeeAddr)
                
                return True

        return "Limit reached (100)"                           
                
    else:
        SET_DEVICE_LAST_CONTACT(ieeeAddr)  


def SET_DEVICE_NAME(ieeeAddr, new_name):
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + entry.name + " | Name changed" + " || Name - " + new_name)
    
    entry.name = new_name
    db.session.commit()       


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


        # special case eurotronic heater_thermostat 
        if GET_DEVICE_BY_IEEEADDR(ieeeAddr).model == "SPZB0001":

            # reduce string statement 
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
                battery_value = int(int(data['battery']) * 5) 

                last_values_string = last_values_string_modified + "battery: " + str(battery_value)

            except:
                last_values_string = last_values_string_modified

        
        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        entry.last_values_json   = last_values
        entry.last_values_string = last_values_string
        entry.last_contact       = timestamp
        db.session.commit()   
    
    except:
        pass


def UPDATE_DEVICE(id, name, gateway, model, device_type = "", description = "", input_values = "", input_events = "", commands = "", commands_json = ""):
    entry = Devices.query.filter_by(id=id).first()

    # values changed ?
    if (entry.name != name or entry.model != model or entry.device_type != device_type or entry.description != description or entry.input_values != input_values or 
        entry.input_events != input_events or entry.commands != commands or entry.commands_json != commands_json):
        
        entry.name          = name
        entry.model         = model
        entry.device_type   = device_type
        entry.description   = description
        entry.input_values  = str(input_values)
        entry.input_events  = str(input_events)
        entry.commands      = str(commands)   
        entry.commands_json = str(commands_json)               
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + entry.name + " | changed")
   
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


def SET_DEVICE_EXCEPTION(ieeeAddr, exception_option, exception_setting, exception_sensor_ieeeAddr, 
                         exception_sensor_input_values, exception_value_1, exception_value_2, exception_value_3):
              
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
             
    # values changed ?
    if (entry.exception_option != exception_option or entry.exception_setting != exception_setting or
        entry.exception_sensor_ieeeAddr != exception_sensor_ieeeAddr or 
        entry.exception_sensor_input_values != exception_sensor_input_values or 
        entry.exception_value_1 != exception_value_1 or entry.exception_value_2 != exception_value_2 or 
        entry.exception_value_3 != exception_value_3):              
                                         
        entry.exception_option              = exception_option
        entry.exception_setting             = exception_setting          
        entry.exception_sensor_ieeeAddr     = exception_sensor_ieeeAddr
        entry.exception_sensor_input_values = exception_sensor_input_values
        entry.exception_value_1             = exception_value_1
        entry.exception_value_2             = exception_value_2 
        entry.exception_value_3             = exception_value_3            
        db.session.commit()  
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + entry.name + " | Exception Settings | changed") 

        return True

    
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
                
                device_1.id = 99
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
                
                device_1.id = 99
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
            
            if device.device_type == "controller":
                DELETE_CONTROLLER(ieeeAddr)

            Devices.query.filter_by(ieeeAddr=ieeeAddr).delete()
            db.session.commit() 
            
            WRITE_LOGFILE_SYSTEM("DATABASE", "Network | Device - " + device_name + " | deleted")                      
            return True

        except Exception as e:
            return str(e)


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

        entry.server_address = server_address
        entry.server_port    = server_port
        entry.encoding       = encoding
        entry.username       = username
        entry.password       = password
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | eMail Settings | changed") 
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

    entry = Lighting_Groups.query.filter_by(id=id).first()

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

        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Group - " + name + " | Settings | changed")  
        return True 


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


def CHANGE_LIGHTING_GROUPS_POSITION(id, direction):
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
        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Group - " + name + " | deleted")   
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

    entry = Lighting_Scenes.query.filter_by(id=id).first()

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

        WRITE_LOGFILE_SYSTEM("DATABASE", "Light | Scene - " + name + " | Settings | changed") 
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


def CHANGE_LIGHTING_SCENES_POSITION(id, direction):
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
        WRITE_LOGFILE_SYSTEM("DATABASE", "Lighting | Scene - " + name + " | deleted") 
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

    entry = Programs.query.filter_by(id=id).first()

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

        WRITE_LOGFILE_SYSTEM("DATABASE", "Program | " + entry.name + " | changed")  
        return True


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


def CHANGE_PROGRAMS_LINE_POSITION(id, line, direction):
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
        WRITE_LOGFILE_SYSTEM("DATABASE", "Program | " + name + " | deleted")  
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
                             
    entry = Scheduler_Tasks.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.task != task or entry.trigger_time != trigger_time or
        entry.trigger_sun_position != trigger_sun_position or entry.trigger_sensors != trigger_sensors or 
        entry.trigger_position != trigger_position or entry.option_repeat != option_repeat or entry.option_pause != option_pause or 
        entry.day != day or entry.hour != hour or entry.minute != minute or
        entry.option_sunrise != option_sunrise or entry.option_sunset != option_sunset or entry.latitude != latitude or entry.longitude != longitude or 
        entry.device_ieeeAddr_1 != device_ieeeAddr_1 or entry.sensor_key_1 != sensor_key_1 or 
        entry.operator_1 != operator_1 or entry.value_1 != value_1  or entry.main_operator_second_sensor != main_operator_second_sensor or 
        entry.device_ieeeAddr_2 != device_ieeeAddr_2 or entry.sensor_key_2 != sensor_key_2 or 
        entry.operator_2 != operator_2 or entry.value_2 != value_2 or
        entry.option_home != option_home or entry.option_away != option_away or entry.ip_addresses != ip_addresses):
            
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

        WRITE_LOGFILE_SYSTEM("DATABASE", "Scheduler | Task - " + entry.name + " | changed") 
        return True


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


def CHANGE_SCHEDULER_TASKS_POSITION(id, direction):
    
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
        WRITE_LOGFILE_SYSTEM("DATABASE", "Scheduler | Task - " + entry.name + " | deleted")   
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
    

def FIND_SENSORDATA_JOB_INPUT(incoming_ieeeAddr):
    entries = Sensordata_Jobs.query.all()
    
    list_jobs = []

    for entry in entries:
        if entry.device.ieeeAddr == incoming_ieeeAddr and entry.always_active == "True":
            list_jobs.append(entry.id)

    return list_jobs


def ADD_SENSORDATA_JOB():
    for i in range(1,26):
        if Sensordata_Jobs.query.filter_by(id=i).first():
            pass
        else:
            # add the new job
            sensordata_job = Sensordata_Jobs(
                    id             = i,
                    name           = "new_job_" + str(i), 
                    always_active  = "True",           
                )
            db.session.add(sensordata_job)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + "new_job_" + str(i) + " | added")                    
            return True

    return "Limit reached (25)"


def SET_SENSORDATA_JOB_SETTINGS(id, name, filename, device_ieeeAddr, sensor_key, always_active):        
    entry = Sensordata_Jobs.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed?
    if (entry.name != name or entry.filename != filename or entry.device_ieeeAddr != device_ieeeAddr or 
        entry.sensor_key != sensor_key or entry.always_active != always_active):

        entry.name = name
        entry.filename = filename
        entry.device_ieeeAddr =device_ieeeAddr
        entry.sensor_key = sensor_key
        entry.always_active = always_active
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + entry.name + " | changed")   
        return True 


def CHANGE_SENSORDATA_JOBS_POSITION(id, direction): 
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
        WRITE_LOGFILE_SYSTEM("DATABASE", "Sensordata | Job - " + entry.name + " | deleted")
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

        entry.client_id     = client_id
        entry.client_secret = client_secret   
        db.session.commit()

        WRITE_LOGFILE_SYSTEM("DATABASE", "Music | Spotify Settings | changed") 
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


def SET_SPOTIFY_DEFAULT_SETTINGS(default_device_id, default_device_name, default_playlist_uri, default_playlist_name, default_volume):
    entry = Spotify_Settings.query.filter_by().first()

    # values changed ?
    if (entry.default_device_id != default_device_id or entry.default_device_name != default_device_name or
        entry.default_playlist_uri != default_playlist_uri or entry.default_playlist_name != default_playlist_name or
        entry.default_volume != default_volume):    

        entry.default_device_id     = default_device_id
        entry.default_device_name   = default_device_name
        entry.default_playlist_uri  = default_playlist_uri
        entry.default_playlist_name = default_playlist_name
        entry.default_volume        = default_volume        
        db.session.commit()

        WRITE_LOGFILE_SYSTEM("DATABASE", "Music | Spotify Default Settings | changed") 
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

        entry.zigbee2mqtt_active   = zigbee2mqtt_active    
        entry.lms_active           = lms_active   
        entry.squeezelite_active   = squeezelite_active               
        db.session.commit()   

        WRITE_LOGFILE_SYSTEM("DATABASE", "System | Services | changed") 
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
                    id                 = i,
                    name               = "new_user_" + str(i),
                    role               = "user",
                    email_notification = "False",
                )
            db.session.add(new_user)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + "new_user_" + str(i) + " | added") 
            return True

    return "Limit reached (10)"        


def UPDATE_USER_SETTINGS(id, name, email, role, email_notification):    
    
    entry = User.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.email != email or entry.role != role or entry.email_notification != email_notification):

        entry.name               = name
        entry.email              = email
        entry.role               = role 
        entry.email_notification = email_notification
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + old_name + " | changed")

        return True


def CHANGE_USER_PASSWORD(id, hashed_password):
    entry = User.query.filter_by(id=id).first()

    # values changed ?
    if entry.password != hashed_password:    
    
        entry.password = hashed_password    
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + entry.name + " | Password changed")
        return True
    

def DELETE_USER(user_id):
    entry = GET_USER_BY_ID(user_id)

    if entry.name != "admin":

        try:
            WRITE_LOGFILE_SYSTEM("DATABASE", "System | User - " + entry.name + " | deleted")    
            User.query.filter_by(id=user_id).delete()
            db.session.commit()    
            return True

        except Exception as e:
                return(e)

    else:
        return "User 'admin' cannot be deleted"