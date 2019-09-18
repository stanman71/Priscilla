from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


from app        import app
from app.common import COMMON, STATUS, DATATYPE

import datetime

db = SQLAlchemy(app)


def WRITE_LOGFILE_SYSTEM(value1, value2):
    pass


class MQTT(db.Model):
    __tablename__ = 'mqtt'
    id       = db.Column(db.Integer, primary_key=True, autoincrement = True)
    broker   = db.Column(db.String(50))
    user     = db.Column(db.String(50))
    password = db.Column(db.String(50))

class MQTT_Devices(db.Model):
    __tablename__ = 'mqtt_devices'
    id                            = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                          = db.Column(db.String(50), unique=True)
    ieeeAddr                      = db.Column(db.String(50), unique=True)  
    device_type                   = db.Column(db.String(50))
    description                   = db.Column(db.String(200))
    input_values                  = db.Column(db.String(200))
    input_events                  = db.Column(db.String(200))
    commands                      = db.Column(db.String(200))    
    last_contact                  = db.Column(db.String(50))
    last_values                   = db.Column(db.String(200))  
    last_values_formated          = db.Column(db.String(200)) 

class Plants(db.Model):
    __tablename__  = 'plants'
    id                     = db.Column(db.Integer, primary_key=True, autoincrement = True)   
    name                   = db.Column(db.String(50), unique=True)
    mqtt_device_ieeeAddr   = db.Column(db.String(50), db.ForeignKey('mqtt_devices.ieeeAddr'))   
    mqtt_device            = db.relationship('MQTT_Devices')  
    pumptime               = db.Column(db.Integer)        
    pump_mode              = db.Column(db.String(50))
    pump_duration_auto     = db.Column(db.Integer)  
    pump_duration_manually = db.Column(db.Integer)       
    sensor_watertank       = db.Column(db.String(50))     
    sensor_moisture        = db.Column(db.String(50))         
    moisture_level         = db.Column(db.String(50)) 

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


# create default mqtt settings
if MQTT.query.filter_by().first() is None:
    mqtt = MQTT(
        user     = "",
        password = "",
    )
    db.session.add(mqtt)
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


""" ################### """
""" ################### """
"""          mqtt       """
""" ################### """
""" ################### """


def GET_MQTT_BROKER_SETTINGS():
    return MQTT.query.filter_by().first()


def SET_MQTT_BROKER_SETTINGS(broker, user, password):
    entry = MQTT.query.filter_by().first()

    if (entry.broker != broker or entry.user != user or entry.password != password):
 
        entry.broker   = broker
        entry.user     = user
        entry.password = password
        db.session.commit()
	
        WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Broker Settings changed")


""" ################### """
""" ################### """
"""     mqtt devices    """
""" ################### """
""" ################### """


def GET_MQTT_DEVICE_BY_ID(id):
    return MQTT_Devices.query.filter_by(id=id).first()


def GET_MQTT_DEVICE_BY_NAME(name):
    for device in MQTT_Devices.query.all():
        
        if device.name.lower() == name.lower():
            return device 
    
    
def GET_MQTT_DEVICE_BY_IEEEADDR(ieeeAddr):
    return MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()   


def GET_ALL_MQTT_DEVICES(selector):
    device_list = []
    devices     = MQTT_Devices.query.all()
  
    if selector == "":
        for device in devices:
            
            device_list.append(device)     

    if selector == "watering_controller":
        for device in devices:
            if device.device_type == "watering_controller":
                
                device_list.append(device)       
          
    return device_list
        

def ADD_MQTT_DEVICE(name, ieeeAddr, device_type = "", description = "", 
                    input_values = "", input_events = "", commands = "", last_contact = ""):
        
    # path exist ?
    if not GET_MQTT_DEVICE_BY_IEEEADDR(ieeeAddr):   
            
        # find a unused id
        for i in range(1,51):
            
            if MQTT_Devices.query.filter_by(id=i).first():
                pass
                
            else:
                # add the new device            
                device = MQTT_Devices(
                        id               = i,
                        name             = name,                   
                        ieeeAddr         = ieeeAddr,
                        device_type      = device_type,
                        description      = description,
                        input_values     = str(input_values),
                        input_events     = str(input_events),
                        commands         = str(commands),                    
                        last_contact     = last_contact,
                        )
                        
                db.session.add(device)
                db.session.commit()
                
                SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr)   
                
                return ""

        return "Gerätelimit erreicht (50)"                           
                
    else:
        SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr)  


def SET_MQTT_DEVICE_NAME(ieeeAddr, new_name):
    entry = MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Device - " + entry.name + 
                         " | Gateway - " + entry.gateway +
                         " | Name changed" + 
                         " || Name - " + new_name)
    
    entry.name = new_name
    db.session.commit()       


def SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr):
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
    entry = MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.last_contact = timestamp
    db.session.commit()       


def SET_MQTT_DEVICE_LAST_VALUES(ieeeAddr, last_values):
    entry = MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    
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

    
def UPDATE_MQTT_DEVICE(id, name, device_type = "", description = "", input_values = "", input_events = "", commands = ""):
    entry = MQTT_Devices.query.filter_by(id=id).first()
    
    # values changed ?
    if (entry.name != name or entry.device_type != device_type or entry.description != description 
        or entry.input_values != input_values or entry.input_events != input_events or entry.commands != commands):
        
        entry.device_type     = device_type
        entry.description     = description
        entry.input_values    = str(input_values)
        entry.input_events    = str(input_events)
        entry.commands        = str(commands)        
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Device - " + entry.name + " | changed" + 
                             " || Name - " + name + 
                             " | ieeeAddr - " + entry.ieeeAddr + 
                             " | device_type - " + entry.device_type +
                             " | description - " + entry.description +
                             " | Input_values - " + str(input_values) + 
                             " | Input_events - " + str(input_events) + 
                             " | Commands - " + str(commands))

        entry.name = name
        db.session.commit()    
   
    
def CHANGE_MQTT_DEVICE_POSITION(id, device_type, direction):
    
    if direction == "up":
        device_list = GET_ALL_MQTT_DEVICES(device_type)
        device_list = device_list[::-1]
        
        for device in device_list:
            
            if device.id < id:
                
                new_id = device.id
                
                # change ids
                device_1 = GET_MQTT_DEVICE_BY_ID(id)
                device_2 = GET_MQTT_DEVICE_BY_ID(new_id)
                
                device_1.id = 99
                db.session.commit()
                
                device_2.id = id
                device_1.id = new_id
                db.session.commit()
                
                return 

    if direction == "down":
        for device in GET_ALL_MQTT_DEVICES(device_type):
            if device.id > id:
                
                new_id = device.id
                
                # change ids
                device_1 = GET_MQTT_DEVICE_BY_ID(id)
                device_2 = GET_MQTT_DEVICE_BY_ID(new_id)
                
                device_1.id = 99
                db.session.commit()
                
                device_2.id = id
                device_1.id = new_id
                db.session.commit()
                
                return 


def DELETE_MQTT_DEVICE(ieeeAddr):
    error_list = ""

    # check plants
    entries = GET_ALL_PLANTS()
    for entry in entries:
        if entry.mqtt_device_ieeeAddr == ieeeAddr:
            device = GET_MQTT_DEVICE_BY_IEEEADDR(ieeeAddr)
            error_list = error_list + "," + device.name + " eingetragen in Bewässung"
    
    if error_list != "":
        return error_list[1:]   
               
    else:      
        device      = GET_MQTT_DEVICE_BY_IEEEADDR(ieeeAddr)
        device_name = device.name
        
        MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).delete()
        db.session.commit() 
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "MQTT | Device - " + device_name + " | deleted")
        return True


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


def ADD_PLANT(name, mqtt_device_ieeeAddr):
    # name exist ?
    if not GET_PLANT_BY_NAME(name):
        
        # find a unused id
        for i in range(1,26):
            if Plants.query.filter_by(id=i).first():
                pass
            else:
                # add the new plant
                plant = Plants(
                        id                   = i,
                        name                 = name, 
                        mqtt_device_ieeeAddr = mqtt_device_ieeeAddr,            
                    )
                db.session.add(plant)
                db.session.commit()

                WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + name + " | added")  
                return
  
                          
        return "Pflanzenlimit erreicht (25)"

    else:
        return "Name bereits vergeben"


def UPDATE_PLANT_SETTINGS(id, name, pumptime, pump_mode, sensor_moisture, sensor_watertank):         
    entry = Plants.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.pump_mode != pump_mode or entry.pumptime != pumptime or 
        entry.sensor_moisture != sensor_moisture or entry.sensor_watertank != sensor_watertank):

        entry.name             = name
        entry.pumptime         = pumptime   
        entry.pump_mode        = pump_mode        
        entry.sensor_moisture  = sensor_moisture
        entry.sensor_watertank = sensor_watertank         
        
        db.session.commit()  
        
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + old_name + " | changed || Name - " + entry.name +                             
                             " | PumpTime - " + str(entry.pumptime) + 
                             " | PumpMode - " + str(entry.pump_mode) +                              
                             " | Sensor Moisture - " + entry.sensor_moisture + 
                             " | Sensor Watertank - " + entry.sensor_watertank)
    

def SET_PLANT_MOISTURE_LEVEL(id, moisture_level):         
    entry = Plants.query.filter_by(id=id).first()

    entry.moisture_level = moisture_level
    db.session.commit()  
    
    if entry.moisture_level != "None":
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Moisture_Level - " + str(entry.moisture_level))    

    
def SET_PLANT_PUMP_DURATION_AUTO(id, pump_duration_auto):         
    entry = Plants.query.filter_by(id=id).first()

    entry.pump_duration_auto = pump_duration_auto
    db.session.commit()  
    
    if entry.pump_duration_auto != "None":
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Pump_Duration_Auto - " + str(entry.pump_duration_auto))    


def SET_PLANT_PUMP_DURATION_MANUALLY(id, pump_duration_manually):         
    entry = Plants.query.filter_by(id=id).first()

    entry.pump_duration_manually = pump_duration_manually
    db.session.commit()  
    
    if entry.pump_duration_manually != "None":
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | changed || Pump_Duration_Manually - " + str(entry.pump_duration_manually))                                 


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
    
    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "Plant - " + entry.name + " | deleted")   
    except:
        pass 
    
    Plants.query.filter_by(id=id).delete()
    db.session.commit()


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


def RESET_USER_PASSWORD(id, hashed_password):
    entry = User.query.filter_by(id=id).first()
    
    entry.password = hashed_password    
    db.session.commit()
    
    WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + entry.username + " | Password changed")


def DELETE_USER(user_id):
    entry = GET_USER_BY_ID(user_id)

    try:
        WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + entry.username + " | deleted")    
    except:
        pass
    
    User.query.filter_by(id=user_id).delete()
    db.session.commit()