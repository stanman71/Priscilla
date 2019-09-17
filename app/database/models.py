from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


from app        import app
from app.common import COMMON, STATUS, DATATYPE

db = SQLAlchemy(app)


def WRITE_LOGFILE_SYSTEM(value1, value2):
    pass



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

# create default user
if User.query.filter_by(username='admin').first() is None:
    user = User(
        username           = "admin",
        email              = "member@example.com",
        role               = "administrator",
        password           = "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339",    
        email_notification = "all"
    )           
    
    db.session.add(user)
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
                    username = username,
                    email    = email,
                    password = password,
                    role     = "user",
                )
            db.session.add(new_user)
            db.session.commit()

            WRITE_LOGFILE_SYSTEM("DATABASE", "User - " + username + " | added") 

            return ""

        else:
            return "eMail-Adresse bereits vorhanden"               

    else:
        return "Name bereits vorhanden"    


def SET_USER_SETTINGS(id, username, email, role, email_notification):    
    
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