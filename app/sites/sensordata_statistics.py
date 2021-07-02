from flask                       import json, url_for, redirect, render_template, flash, g, session, jsonify, request
from flask_login                 import current_user, login_required
from werkzeug.exceptions         import HTTPException, NotFound, abort
from functools                   import wraps

from app                         import app
from app.backend.database_models import *
from app.backend.file_management import WRITE_LOGFILE_SYSTEM, READ_SENSORDATA_FILE, GET_ALL_SENSORDATA_FILES
from app.backend.build_graph     import BUILD_GRAPH
from app.backend.user_id         import SET_CURRENT_USER_ID
from app.common                  import COMMON, STATUS
from app.assets                  import *

import datetime as dt
import pandas as pd

dropdown_list_dates_temp = []


# access rights
def permission_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        try:
            if current_user.role == "user" or current_user.role == "administrator":
                return f(*args, **kwargs)
            else:
                return redirect(url_for('logout'))
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "System | " + str(e))  
            print("#################")
            print("ERROR: " + str(e))
            print("#################")
            return redirect(url_for('logout'))
        
    return wrap


@app.route('/sensordata/statistics', methods=['GET', 'POST'])
@login_required
@permission_required
def sensordata_statistics():
    page_title       = 'Bianca | Sensordata | Statistics'
    page_description = 'The sensordata statistics page'

    SET_CURRENT_USER_ID(current_user.id)  

    global dropdown_list_dates_temp

    error_message_select_datafiles = []    
    error_message_create_graph     = []

    devices       = ""
    sensors       = ""
    data_file_1   = "None"
    data_file_2   = "None"
    data_file_3   = "None"
    
    dropdown_list_dates = []
    date_start          = ""
    date_stop           = ""
    
    graph_created = False


    """ ############## """
    """  select files  """
    """ ############## """   

    if request.form.get("select_datafiles") != None: 
        data_file_1 = request.form.get("get_file_1")
        data_file_2 = request.form.get("get_file_2")
        data_file_3 = request.form.get("get_file_3")

        if data_file_1 != "None" or data_file_2 != "None" or data_file_3 != "None":

            df_1 = READ_SENSORDATA_FILE(data_file_1)     

            # merge data sources
            if data_file_1 != data_file_2 and data_file_1 != data_file_3 and data_file_2 != data_file_3:

                try:
                    df_2 = READ_SENSORDATA_FILE(data_file_2)
                    df_1 = pd.concat([df_1, df_2], ignore_index=True)
                except:
                    pass           
                try:
                    df_3 = READ_SENSORDATA_FILE(data_file_3)
                    df_1 = pd.concat([df_1, df_3], ignore_index=True)
                except:
                    pass

                df = df_1

            else:
                df = df_1
                if data_file_2 == data_file_3 and data_file_2 != "" and data_file_2 != "None":
                    error_message_select_datafiles.append("File " + data_file_2 + " selected several times")
                if data_file_1 == data_file_2 or data_file_1 == data_file_3:
                    error_message_select_datafiles.append("File " + data_file_1 + " selected several times")  

            # format data
            try:
                devices  = df.Device.unique().tolist()
                devices  = str(devices)
                devices  = devices[1:]
                devices  = devices[:-1]
                devices  = devices.replace("'", "") 
                sensors  = df.Sensor.unique().tolist()
                sensors  = str(sensors)                
                sensors  = sensors[1:]
                sensors  = sensors[:-1]
                sensors  = sensors.replace("'", "")
                
                for date in pd.to_datetime(df['Timestamp']).dt.date.unique().tolist():
                    
                    date_temp = ""
                    date_temp = date_temp + str(date.year) + "-" 
                    
                    if len(str(date.month)) == 1:
                        date_temp = date_temp + "0" + str(date.month) + "-" 
                    else:
                        date_temp = date_temp + str(date.month) + "-" 
                    
                    if len(str(date.day)) == 1:
                        date_temp = date_temp + "0" + str(date.day)
                    else:
                        date_temp = date_temp + str(date.day)
                            
                    dropdown_list_dates.append(date_temp)        
                
            except Exception as e:
                error_message_select_datafiles.append("Error opening files || " + str(e))

        else:
            error_message_select_datafiles.append("No file selected")
        
        
    # update dropdown_list_dates_temp or get former dropdown_list_dates
    if dropdown_list_dates != []:
        dropdown_list_dates_temp = dropdown_list_dates             
        date_start               = dropdown_list_dates[0]
        date_stop                = dropdown_list_dates[-1]   
    else:
        dropdown_list_dates      = dropdown_list_dates_temp


    """ ############## """
    """  create table  """
    """ ############## """   

    if request.form.get("create_graph") != None: 
        data_file_1 = request.form.get("get_file_1")
        data_file_2 = request.form.get("get_file_2")
        data_file_3 = request.form.get("get_file_3")

        df_1 = READ_SENSORDATA_FILE(data_file_1)     

        # merge data sources
        if data_file_1 != data_file_2 and data_file_1 != data_file_3 and data_file_2 != data_file_3:

            try:
                df_2 = READ_SENSORDATA_FILE(data_file_2)
                df_1 = pd.concat([df_1, df_2], ignore_index=True)
            except:
                pass           
            try:
                df_3 = READ_SENSORDATA_FILE(data_file_3)
                df_1 = pd.concat([df_1, df_3], ignore_index=True)
            except:
                pass

            df = df_1

        else:
            df = df_1


        try:
            devices    = request.form.get("set_devices").strip()  
            sensors    = request.form.get("set_sensors").strip()  
            date_start = request.form.get("set_date_start")
            date_stop  = request.form.get("set_date_stop") 

            selected_devices = devices.replace(" ", "")
            selected_devices = selected_devices.split(",")
            selected_sensors = sensors.replace(" ", "")
            selected_sensors = selected_sensors.split(",")

            # complete list
            df_devices = df.loc[df['Device'].isin(selected_devices)]

            # selected divices
            df_sensors = df_devices.loc[df['Sensor'].isin(selected_sensors)]
            
            # date_start value < date_stop value ?
            if dropdown_list_dates.index(date_start) < dropdown_list_dates.index(date_stop):
        
                minimum_from_gui = date_start + " 00:00:00"
                maximum_from_gui = date_stop  + " 00:00:00"
                df_sensors_filtered_min = df_sensors[df_sensors['Timestamp']>=minimum_from_gui]
                df_sensors_filtered_max = df_sensors[df_sensors['Timestamp']<=maximum_from_gui]

                df_sensors = pd.merge(df_sensors_filtered_min, df_sensors_filtered_max, how='inner')

                # set datetime as index and remove former row datetime
                df_sensors['date'] = pd.to_datetime(df_sensors['Timestamp'], format='%Y-%m-%d %H:%M:%S', utc=True).values
                
                df_sensors = df_sensors.set_index('date')
                df_sensors = df_sensors.drop(columns=['Timestamp'])
                
                result = BUILD_GRAPH(df_sensors)

                if result != True:
                    error_message_create_graph.append(result)
                else:
                    graph_created = True
         
            else:
                error_message_create_graph.append("Time || First date must be earlier than second date")

        except Exception as e:
            error_message_create_graph.append("Data could not be processed || " + str(e))

    dropdown_list_sensordata_files = GET_ALL_SENSORDATA_FILES() 

    data = {'navigation': 'sensordata_statistics'}

    return render_template('layouts/default.html',
                            data=data,   
                            title=page_title,        
                            description=page_description,                                
                            content=render_template( 'pages/sensordata_statistics.html',
                                                    error_message_select_datafiles=error_message_select_datafiles,
                                                    error_message_create_graph=error_message_create_graph,
                                                    dropdown_list_sensordata_files=dropdown_list_sensordata_files,
                                                    dropdown_list_dates=dropdown_list_dates,                           
                                                    date_start=date_start,
                                                    date_stop=date_stop,
                                                    devices=devices,
                                                    sensors=sensors,
                                                    data_file_1=data_file_1,
                                                    data_file_2=data_file_2,
                                                    data_file_3=data_file_3,
                                                    graph_created=graph_created,
                                                    ) 
                           )