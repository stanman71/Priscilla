from flask_mail import Mail, Message

from app                         import app
from app.backend.database_models import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM

import os


def SEND_EMAIL(subject, message):

    def CHECK_EMAIL_SETTINGS():     
        settings = GET_EMAIL_SETTINGS()

        if settings.encoding == "ssl":
            mail_settings = {
                "MAIL_SERVER"  : settings.server_address,
                "MAIL_PORT"    : settings.server_port,  
                "MAIL_USE_TLS" : False,
                "MAIL_USE_SSL" : True,
                "MAIL_USERNAME": settings.username,
                "MAIL_PASSWORD": settings.password,
            }

            return mail_settings 
            
        elif settings.encoding == "tls":
            mail_settings = {
                "MAIL_SERVER"  : settings.server_address,
                "MAIL_PORT"    : settings.server_port,  
                "MAIL_USE_TLS" : True,
                "MAIL_USE_SSL" : False,
                "MAIL_USERNAME": settings.username,
                "MAIL_PASSWORD": settings.password,
            }  

            return mail_settings 

        else:
            return "None"


    if CHECK_EMAIL_SETTINGS() != "None":

        app.config.update(CHECK_EMAIL_SETTINGS())
        mail = Mail(app)

        recipients = GET_EMAIL_ADDRESSES(subject)

        if recipients != None and recipients != "None":

            try:
                with app.app_context():
                    msg = Message(subject    = "SMARTHOME | " + subject + " | " + message,
                                sender     = app.config.get("MAIL_USERNAME"),
                                recipients = recipients,
                                body       = "")
                    
                    """                            
                    ### attachment ###

                    # pictures
                    with app.open_resource("/home/pi/SmartHome/app/static/images/background.jpg") as fp:
                        msg.attach("background.jpg","image/jpg", fp.read())
                    with app.open_resource("/home/pi/SmartHome/app/static/images/background-panal.jpg") as fp:
                        msg.attach("background-panal.jpg","image/jpg", fp.read())   
                    
                    # text
                    with app.open_resource("C:/Users/mstan/Downloads/uzt.txt") as fp:
                        msg.attach("uzt.txt","text/plain", fp.read())   
                    """

                    mail.send(msg)

                return   
                
            except Exception as e:
                if str(e) != "No recipients have been added":
                    WRITE_LOGFILE_SYSTEM("ERROR", "System | eMail | " + str(recipients) + " | " + subject + " | " + message + " | " + str(e))  
                    return ("ERROR eMail || " + str(e))  