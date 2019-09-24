from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


from app                         import app
from app.common                  import COMMON, STATUS, DATATYPE
from app.backend.file_management import WRITE_LOGFILE_SYSTEM, WRITE_PLANTS_DATAFILE, CREATE_PLANTS_DATAFILE, RENAME_PLANTS_DATAFILE, DELETE_PLANTS_DATAFILE

import datetime
import re

db = SQLAlchemy(app)

class Devices(db.Model):
    __tablename__ = 'devices'
    id                   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                 = db.Column(db.String(50), unique=True)
    ieeeAddr             = db.Column(db.String(50), unique=True)  
    model                = db.Column(db.String(50))    
    device_type          = db.Column(db.String(50))
    inputs               = db.Column(db.String(200))
    commands             = db.Column(db.String(200))    
    last_contact         = db.Column(db.String(50))
    last_values          = db.Column(db.String(200))  
    last_values_formated = db.Column(db.String(200)) 

class eMail(db.Model):
    __tablename__  = 'email'
    id             = db.Column(db.Integer, primary_key=True, autoincrement = True)
    server_address = db.Column(db.String(50))
    server_port    = db.Column(db.Integer)
    encoding       = db.Column(db.String(50))
    username       = db.Column(db.String(50))
    password       = db.Column(db.String(50)) 

class Host(db.Model):
    __tablename__ = 'host'
    id                = db.Column(db.Integer, primary_key=True, autoincrement = True)
    lan_dhcp          = db.Column(db.String(50), server_default=("True"))    
    lan_ip_address    = db.Column(db.String(50))
    lan_gateway       = db.Column(db.String(50))

class MQTT_Broker(db.Model):
    __tablename__     = 'mqtt_broker'
    id                = db.Column(db.Integer, primary_key=True, autoincrement = True)
    broker            = db.Column(db.String(50))
    user              = db.Column(db.String(50))
    password          = db.Column(db.String(50))
    previous_broker   = db.Column(db.String(50))
    previous_user     = db.Column(db.String(50))
    previous_password = db.Column(db.String(50))    

class Plants(db.Model):
    __tablename__  = 'plants'
    id                     = db.Column(db.Integer, primary_key=True, autoincrement = True)   
    name                   = db.Column(db.String(50), unique=True)
    device_ieeeAddr        = db.Column(db.String(50), db.ForeignKey('devices.ieeeAddr'))   
    device                 = db.relationship('Devices')  
    group                  = db.Column(db.Integer)        
    pump_duration_auto     = db.Column(db.Integer)  
    pump_duration_manually = db.Column(db.Integer)            
    moisture_level         = db.Column(db.String(50)) 

class Scheduler_Tasks(db.Model):
    __tablename__ = 'scheduler_tasks'
    id     = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name   = db.Column(db.String(50), unique=True)
    task   = db.Column(db.String(50))  
    hour   = db.Column(db.Integer)  
    minute = db.Column(db.Integer)         
    pause  = db.Column(db.String(50))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id                 = db.Column(db.Integer,     primary_key=True)
    username           = db.Column(db.String(64),  unique = True)
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


# create default email
if eMail.query.filter_by().first() is None:
    email = eMail(
        id = 1,
    )
    db.session.add(email)
    db.session.commit()


# create default host settings
if Host.query.filter_by().first() is None:
    host = Host(
    )
    db.session.add(host)
    db.session.commit()


# create default mqtt broker settings
if MQTT_Broker.query.filter_by().first() is None:
    mqtt_broker = MQTT_Broker(
        user     = "",
        password = "",
    )
    db.session.add(mqtt_broker)
    db.session.commit()


# create default mqtt broker settings
if Scheduler_Tasks.query.filter_by().first() is None:
    scheduler_task_plants_group_1 = Scheduler_Tasks(
        name   = "plants_group_1",
    )
    db.session.add(scheduler_task_plants_group_1)

    scheduler_task_plants_group_2 = Scheduler_Tasks(
        name   = "plants_group_2",
    )
    db.session.add(scheduler_task_plants_group_2)

    scheduler_task_plants_group_3 = Scheduler_Tasks(
        name   = "plants_group_3",
    )
    db.session.add(scheduler_task_plants_group_3)

    scheduler_task_update_devices = Scheduler_Tasks(
        name   = "update_devices",
        task   = "update_devices",
        hour   = "*",
        minute = "15",       
    )
    db.session.add(scheduler_task_update_devices)

    scheduler_task_backup = Scheduler_Tasks(
        name   = "backup_database",
        task   = "create_database_backup",
        hour   = "0",
        minute = "0",        
    )
    db.session.add(scheduler_task_backup)
    db.session.commit()

# create default user
if User.query.filter_by(username='admin').first() is None:
    user = User(
        username           = "admin",
        email              = "member@example.com",
        role               = "administrator",
        password           = "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339",    
        email_notification = "True"
    )           
    
    db.session.add(user)
    db.session.commit()


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
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "eMail | Server Settings | changed")
        
        return True



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

    if selector == "watering_controller":
        for device in devices:
            if device.device_type == "watering_controller auto" or device.device_type == "watering_controller manually":
                
                device_list.append(device)       
          
    return device_list
        

def ADD_DEVICE(name, ieeeAddr, model, device_type = "", description = "", inputs = "", commands = "", last_contact = ""):
        
    # ieeeAddr exist ?
    if not GET_DEVICE_BY_IEEEADDR(ieeeAddr):   
            
        # find a unused id
        for i in range(1,51):
            
            if Devices.query.filter_by(id=i).first():
                pass
                
            else:
                # add the new device            
                device = Devices(
                        id           = i,
                        name         = name,                   
                        ieeeAddr     = ieeeAddr,
                        model        = model,
                        device_type  = device_type,
                        inputs       = str(inputs),
                        commands     = str(commands),                    
                        last_contact = last_contact,
                        )
                        
                db.session.add(device)
                db.session.commit()
                
                SET_DEVICE_LAST_CONTACT(ieeeAddr)   
                
                return ""

        return "Gerätelimit erreicht (50)"                           
                
    else:
        SET_DEVICE_LAST_CONTACT(ieeeAddr)  


def SET_DEVICE_NAME(ieeeAddr, new_name):
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "Device | " + entry.name + " | Name changed" + " || Name - " + new_name)
    
    entry.name = new_name
    db.session.commit()       


def SET_DEVICE_LAST_CONTACT(ieeeAddr):
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.last_contact = timestamp
    db.session.commit()       


def SET_DEVICE_LAST_VALUES(ieeeAddr, last_values):
    entry = Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    
    last_values_formated = last_values.replace("{","")
    last_values_formated = last_values_formated.replace("}","")
    last_values_formated = last_values_formated.replace('"',"")
    last_values_formated = last_values_formated.replace(":",": ")
    last_values_formated = last_values_formated.replace(",",", ")
    
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    entry.last_values          = last_values
    entry.last_values_formated = last_values_formated
    entry.last_contact         = timestamp
    db.session.commit()   

    # write data_file
    for plant in GET_ALL_PLANTS():
        if plant.device_ieeeAddr == ieeeAddr:
            device_name = GET_DEVICE_BY_IEEEADDR(ieeeAddr).name
            
            # extract numbers
            list_values = re.findall(r'\b\d+\b', last_values_formated)
            WRITE_PLANTS_DATAFILE(plant.name, device_name, list_values[0], list_values[1], list_values[2])

    
def UPDATE_DEVICE(id, name, model = "", device_type = "", inputs = "", commands = ""):
    entry = Devices.query.filter_by(id=id).first()
    
    # values changed ?
    if (entry.name != name or entry.model != model or entry.device_type != device_type or entry.inputs != inputs or entry.commands != commands):
        
        entry.device_type = device_type
        entry.model       = model
        entry.inputs      = str(inputs)
        entry.commands    = str(commands)        
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Device | " + entry.name + " | changed" + " || Name - " + name + " | Model - " + entry.model)

        entry.name = name
        db.session.commit()    
   
    
def CHANGE_DEVICE_POSITION(id, device_type, direction):
    
    if direction == "up":
        device_list = GET_ALL_DEVICES(device_type)
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
        for device in GET_ALL_DEVICES(device_type):
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

    # check plants
    entries = GET_ALL_PLANTS()
    for entry in entries:
        if entry.device_ieeeAddr == ieeeAddr:
            device = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + "," + device.name + " eingetragen in Pflanzen"
    
    if error_list != "":
        return error_list[1:]   
               
    else:      
        device      = GET_DEVICE_BY_IEEEADDR(ieeeAddr)
        device_name = device.name
        
        Devices.query.filter_by(ieeeAddr=ieeeAddr).delete()
        db.session.commit() 
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Device | " + device_name + " | deleted")
        return True


""" ################### """
""" ################### """
"""         host        """
""" ################### """
""" ################### """


def GET_HOST_NETWORK():
    return Host.query.filter_by().first()


def UPDATE_HOST_INTERFACE_LAN_DHCP(lan_dhcp):
    entry = Host.query.filter_by().first()
    
    # values changed ?
    if entry.lan_dhcp != lan_dhcp:   
    
        entry.lan_dhcp        = lan_dhcp    
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Host | Network settings changed " +
                             "| DHCP LAN - " +  str(lan_dhcp))    

        return True 


def UPDATE_HOST_INTERFACE_LAN(lan_ip_address, lan_gateway):
    entry = Host.query.filter_by().first()
    
    # values changed ?
    if entry.lan_ip_address != lan_ip_address or entry.lan_gateway != lan_gateway:   
     
        entry.lan_ip_address  = lan_ip_address
        entry.lan_gateway     = lan_gateway  
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Host | Network settings changed " +
                             "| LAN - " + str(lan_ip_address) + " : " + str(lan_gateway)) 

        return True


""" ################### """
""" ################### """
"""     mqtt broker     """
""" ################### """
""" ################### """


def GET_MQTT_BROKER_SETTINGS():
    return MQTT_Broker.query.filter_by().first()


def SET_MQTT_BROKER_SETTINGS(broker, user, password):
    entry = MQTT_Broker.query.filter_by().first()

    if (entry.broker != broker or entry.user != user or entry.password != password):
 
        entry.previous_broker   = entry.broker
        entry.previous_user     = entry.user
        entry.previous_password = entry.password
        entry.broker            = broker
        entry.user              = user
        entry.password          = password

        db.session.commit()  
    
        WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Broker Settings changed")

        return True


def RESTORE_MQTT_BROKER_SETTINGS():
    entry = MQTT_Broker.query.filter_by().first()

    broker                  = entry.broker
    user                    = entry.user
    password                = entry.password

    entry.broker            = entry.previous_broker
    entry.user              = entry.previous_user
    entry.password          = entry.previous_password
    entry.previous_broker   = broker
    entry.previous_user     = user
    entry.previous_password = password

    db.session.commit()

    WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Broker Settings restored")


""" ################### """
""" ################### """
"""       plants        """
""" ################### """
""" ################### """


def GET_PLANT_BY_ID(id):
    return Plants.query.filter_by(id=id).first()


def GET_PLANT_BY_NAME(name):
    for plant in Plants.query.all():
        
        if plant.name.lower() == name.lower():
            return plant    
    

def GET_ALL_PLANTS():
    return Plants.query.all()


def ADD_PLANT(name, device_ieeeAddr):
    # name exist ?
    if not GET_PLANT_BY_NAME(name):
        
        # find a unused id
        for i in range(1,26):
            if Plants.query.filter_by(id=i).first():
                pass
            else:
                # add the new plant
                plant = Plants(
                        id                     = i,
                        name                   = name, 
                        device_ieeeAddr        = device_ieeeAddr,     
                        group                  = 1,
                        pump_duration_auto     = 0, 
                        pump_duration_manually = 30,                                               
                    )
                db.session.add(plant)
                db.session.commit()

                WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + name + " | added")  

                # create data_file
                CREATE_PLANTS_DATAFILE(name)
                return
  
                          
        return "Pflanzenlimit erreicht (25)"

    else:
        return "Name bereits vergeben"


def UPDATE_PLANT_SETTINGS(id, name, group):         
    entry = Plants.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.group != int(group)):

        entry.name  = name
        entry.group = group        
        
        db.session.commit()  
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + old_name + " | changed || Name - " + entry.name + " | Group - " + str(entry.group))

        # rename data_file
        if old_name != name:
            RENAME_PLANTS_DATAFILE(old_name, name)

        return True


def SET_PLANT_MOISTURE_LEVEL(id, moisture_level):         
    entry = Plants.query.filter_by(id=id).first()

    # values changed ?
    if entry.moisture_level != moisture_level: 

        entry.moisture_level = moisture_level
        db.session.commit()  
        
        if entry.moisture_level != "None":
            WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Moisture_Level - " + str(entry.moisture_level))   

        return True 

    
def SET_PLANT_PUMP_DURATION_AUTO(id, pump_duration_auto):         
    entry = Plants.query.filter_by(id=id).first()

    # values changed ?
    if entry.pump_duration_auto != int(pump_duration_auto):      

        entry.pump_duration_auto = pump_duration_auto
        db.session.commit()  
        
        if entry.pump_duration_auto != "None":
            WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Pump_Duration_Auto - " + str(entry.pump_duration_auto)) 

        return True    


def SET_PLANT_PUMP_DURATION_MANUALLY(id, pump_duration_manually):         
    entry = Plants.query.filter_by(id=id).first()

    # values changed ?
    if entry.pump_duration_manually != int(pump_duration_manually):       

        entry.pump_duration_manually = pump_duration_manually
        db.session.commit()  
        
        if entry.pump_duration_manually != "None":
            WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Pump_Duration_Manually - " + str(entry.pump_duration_manually))   

        return True                               


def CHANGE_PLANTS_POSITION(id, direction):
    
    if direction == "up":
        plants_list = GET_ALL_PLANTS()
        plants_list = plants_list[::-1]
        
        for plant in plants_list:
            
            if plant.id < id:     
                new_id = plant.id
                
                # change ids
                plant_1 = GET_PLANT_BY_ID(id)
                plant_2 = GET_PLANT_BY_ID(new_id)
                
                plant_1.id = 99
                db.session.commit()
                
                plant_2.id = id
                plant_1.id = new_id
                db.session.commit()
                
                return 

    if direction == "down":
        for plant in GET_ALL_PLANTS():
            if plant.id > id:       
                new_id = plant.id
                
                # change ids
                plant_1 = GET_PLANT_BY_ID(id)
                plant_2 = GET_PLANT_BY_ID(new_id)
                
                plant_1.id = 99
                db.session.commit()
                
                plant_2.id = id
                plant_1.id = new_id
                db.session.commit()
                
                return 


def DELETE_PLANT(id):
    entry = GET_PLANT_BY_ID(id)
    plant_name = entry.name
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + plant_name + " | deleted")   
        Plants.query.filter_by(id=id).delete()
        db.session.commit()

        # delete data_file
        DELETE_PLANTS_DATAFILE(plant_name)
        return True

    except Exception as e:
        return("ERROR: " + str(e))


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


def UPDATE_SCHEDULER_TASK(id, hour, minute, pause): 
    entry = Scheduler_Tasks.query.filter_by(id=id).first()

    # values changed ?
    if (entry.hour != int(hour) or entry.minute != int(minute) or entry.pause != pause):
            
        entry.hour   = hour
        entry.minute = minute        
        entry.pause  = pause      

        db.session.commit()   

        WRITE_LOGFILE_SYSTEM("DATABASE", "Task - " + entry.name + " | changed " +
                             "|| Time - " + str(entry.hour) + ":" + str(entry.minute) + 
                             " | Pause - " + str(entry.pause))     

        return True


""" ################### """
""" ################### """
"""   user management   """
""" ################### """
""" ################### """


def GET_USER_BY_ID(id):
    return User.query.get(int(id))


def GET_USER_BY_NAME(username):
    for user in User.query.all():
        
        if user.username.lower() == username.lower():
            return user       
 

def GET_USER_BY_EMAIL(email):
    return User.query.filter_by(email=email).first()  


def GET_ALL_USERS():
    return User.query.all()  
    

def ADD_USER(username, email, password):
    # username exist ?
    if not GET_USER_BY_NAME(username):

        # email exist ?
        if not GET_USER_BY_EMAIL(email):
        
            # add the new user
            new_user = User(
                    username           = username,
                    email              = email,
                    password           = password,
                    role               = "user",
                    email_notification = "False",
                )
            db.session.add(new_user)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + username + " | added") 

            return 

        else:
            return "eMail-Adresse bereits vorhanden"               

    else:
        return "Name bereits vorhanden"    


def UPDATE_USER_SETTINGS(id, username, email, role, email_notification):    
    
    entry = User.query.filter_by(id=id).first()
    old_username = entry.username

    # values changed ?
    if (entry.username != username or entry.email != email or entry.role != role or entry.email_notification != email_notification):

        entry.username           = username
        entry.email              = email
        entry.role               = role 
        entry.email_notification = email_notification
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + old_username + " | changed || Username - " + entry.username +
                             " | eMail - " + entry.email + " | Role - " + entry.role + " | eMail-Notification - " + entry.email_notification)

        return True


def CHANGE_USER_PASSWORD(id, hashed_password):
    entry = User.query.filter_by(id=id).first()

    # values changed ?
    if entry.password != hashed_password:    
    
        entry.password = hashed_password    
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + entry.username + " | Password changed")

        return True
    

def DELETE_USER(user_id):
    entry = GET_USER_BY_ID(user_id)

    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + entry.username + " | deleted")    
        User.query.filter_by(id=user_id).delete()
        db.session.commit()    
        return True

    except Exception as e:
        return("ERROR: " + str(e))