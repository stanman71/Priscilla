import datetime
import time
import json
import os
import requests
import heapq
import spotipy
import re
import threading

from app                          import app
from app.backend.database_models  import *
from app.backend.lighting         import *
from app.backend.mqtt             import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM, BACKUP_DATABASE
from app.backend.shared_resources import process_management_queue, mqtt_message_queue
from app.backend.process_program  import *
from app.backend.spotify          import *
from app.backend.email            import SEND_EMAIL

from ping3   import ping
from difflib import SequenceMatcher


""" ################################ """
""" ################################ """
"""        scheduler process         """
""" ################################ """
""" ################################ """


def PROCESS_SCHEDULER(task, ieeeAddr):

   start_task = False

   # check time   
   if task.trigger_time == "True":
      if CHECK_SCHEDULER_TIME(task) == False:
         return
      else:
         start_task = True

   # check sensors
   if task.trigger_sensors == "True":

      # find sensor jobs with fitting ieeeAddr only
      if (task.device_ieeeAddr_1 == ieeeAddr or task.device_ieeeAddr_2 == ieeeAddr):
         if CHECK_SCHEDULER_SENSORS(task) == False:
            return
         else:
            start_task = True

      else:
         return

   # check sun_position
   if task.trigger_sun_position == "True": 

      if task.option_sunrise == "True":
         if CHECK_SCHEDULER_SUNRISE(task) == False:
            return   
         else:
            start_task = True

      if task.option_sunset == "True":
         if CHECK_SCHEDULER_SUNSET(task) == False:
            return     
         else:
            start_task = True

   # check position
   if task.trigger_position == "True": 
   
      if task.option_home == "True" or task.option_away == "True":
         ping_result = CHECK_SCHEDULER_PING(task)
  
         if task.option_home == "True" and ping_result == False: 
            return          
         elif task.option_away == "True" and ping_result == True:
            return
         else:
            start_task = True


   if start_task == True:
      START_SCHEDULER_TASK(task)


""" ################################ """
""" ################################ """
"""         scheduler checks         """
""" ################################ """
""" ################################ """


def CHECK_SCHEDULER_TIME(task):

   now = datetime.datetime.now()
   current_day    = now.strftime('%a')
   current_hour   = now.strftime('%H')
   current_minute = now.strftime('%M')

   passing = False


   # #########
   # check day
   # #########

   if "," in task.day:
       
      days = task.day.replace(" ", "")       
      days = days.split(",")
      
      for element in days:
          
         if element.lower() == current_day.lower():
            passing = True
            break
   else:
       
      if task.day.lower() == current_day.lower() or task.day == "*":
         passing = True


   # ###########
   # check hours
   # ###########

   if passing == True:

      hours = task.hour.replace(" ", "")  

      # without range

      if "-" not in hours:

         list_all_hours = hours.split(",")

         # find exceptions
         list_exception_hours = []
         list_valid_hours     = []

         for hour in list_all_hours:
            if "!" in hour:
               list_exception_hours.append(int(hour[1:]))   
            else:
               list_valid_hours.append(hour)   

         # check passing  
         if int(current_hour) not in list_exception_hours:

            for hour in list_valid_hours:

               if str(hour) == "*": 
                  passing = True
                  break                  
               
               elif int(hour) == int(current_hour):         
                  passing = True
                  break

               else:
                  passing = False

         else:
            passing = False         

      # with range

      else:

         list_hours = hours.split(",")

         # find exceptions
         list_exception_hours = []

         for hour in list_hours:
            if "!" in hour:
               list_exception_hours.append(int(hour[1:]))

         # find min_hour and max_hour
         for hour in list_hours:            
            if "-" in hour:
               min_hour = hour.split("-")[0]
               max_hour = hour.split("-")[1]

         list_hours_all = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", 
                           "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]      

         # find positions
         for i, hour in enumerate(list_hours_all):
            if int(hour) == int(min_hour):
               position_min = i
            if int(hour) == int(max_hour):
               position_max = i   

         # check passing  
         if int(current_hour) not in list_exception_hours:

            for hour in list_hours_all[position_min:position_max + 1]:
               
               if int(hour) == int(current_hour):         
                  passing = True
                  break
               
               else:
                  passing = False

         else:
            passing = False     


   # ############
   # check minute
   # ############

   if passing == True:

      minutes = task.minute.replace(" ", "")  

      # without range

      if "-" not in minutes:

         list_all_minutes = minutes.split(",")

         # find exceptions
         list_exception_minutes = []
         list_valid_minutes     = []

         for minute in list_all_minutes:
            if "!" in minute:
               list_exception_minutes.append(int(minute[1:]))   
            else:
               list_valid_minutes.append(minute)   

         # check passing  
         if int(current_minute) not in list_exception_minutes:

            for minute in list_valid_minutes:
               
               if str(minute) == "*": 
                  passing = True
                  break                  

               elif int(minute) == int(current_minute):         
                  passing = True
                  break
               
               else:
                  passing = False

         else:
            passing = False         

      # with range

      else:

         list_minutes = minutes.split(",")

         # find exceptions
         list_exception_minutes = []

         for minute in list_minutes:
            if "!" in minute:
               list_exception_minutes.append(int(minute[1:]))

         # find min_minute and max_minute
         for minute in list_minutes:            
            if "-" in minute:
               min_minute = minute.split("-")[0]
               max_minute = minute.split("-")[1]

         list_minutes_all = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", 
                             "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                             "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", 
                             "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", 
                             "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

         position_min = 0
         position_max = 0

         # find positions
         for i, minute in enumerate(list_minutes_all):
            if int(minute) == int(min_minute):
               position_min = i 
            if int(minute) == int(max_minute):
               position_max = i    

         # check passing  
         if int(current_minute) not in list_exception_minutes:

            for minute in list_minutes_all[position_min:position_max + 1]:
               
               if int(minute) == int(current_minute):         
                  passing = True
                  break
               
               else:
                  passing = False

         else:
            passing = False         


   return passing


def CHECK_SCHEDULER_SUNRISE(task):

   # get current time
   now = datetime.datetime.now()
   current_hour   = now.strftime('%H')
   current_minute = now.strftime('%M')

   # get sunrise time
   sunrise_data = GET_SCHEDULER_TASK_SUNRISE(task.id)
         
   try:
      sunrise_data = sunrise_data.split(":")
      
      if int(current_hour) == int(sunrise_data[0]) and int(current_minute) == int(sunrise_data[1]):
         return True
         
      else:
         return False
         
   except:
      return False
   
   
def CHECK_SCHEDULER_SUNSET(task):

   # get current time
   now = datetime.datetime.now()
   current_hour   = now.strftime('%H')
   current_minute = now.strftime('%M')

   # get sunset time
   sunset_data = GET_SCHEDULER_TASK_SUNSET(task.id)
   
   try:
      sunset_data = sunset_data.split(":")
      
      if int(current_hour) == int(sunset_data[0]) and int(current_minute) == int(sunset_data[1]):
         return True
         
      else:
         return False
         
   except:
      return False


def CHECK_SCHEDULER_SENSORS(task):
   
   passing = False   

   # #######
   # one row
   # #######
   
   if task.main_operator_second_sensor == "None" or task.main_operator_second_sensor == None:


      ##################
      # get sensordata 1
      ##################     

      device_ieeeAddr_1  = task.device_ieeeAddr_1
      sensor_key_1       = task.sensor_key_1.replace(" ","")    
      data_1             = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).last_values_json)
      sensor_value_1     = data_1[sensor_key_1]


      ####################
      # compare conditions
      ####################
      
      passing_1 = False

      if task.operator_1 == "=" and not task.value_1.isdigit():
         if str(sensor_value_1).lower() == str(task.value_1).lower():
            passing = True
         else:
            passing = False
      if task.operator_1 == "=" and task.value_1.isdigit():
         if int(sensor_value_1) == int(task.value_1):
            passing = True    
         else:
            passing = False
      if task.operator_1 == "<" and task.value_1.isdigit():
         if int(sensor_value_1) < int(task.value_1):
            passing = True
         else:
            passing = False
      if task.operator_1 == ">" and task.value_1.isdigit():
         if int(sensor_value_1) > int(task.value_1):
            passing = True 
         else:
            passing = False


   # ########
   # two rows
   # ########
   
   if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
             
     
      ##################
      # get sensordata 1
      ##################     

      device_ieeeAddr_1  = task.device_ieeeAddr_1
      sensor_key_1       = task.sensor_key_1.replace(" ","")    
      data_1             = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).last_values_json)
      sensor_value_1     = data_1[sensor_key_1]


      ##################
      # get sensordata 2
      ##################     

      device_ieeeAddr_2  = task.device_ieeeAddr_2
      sensor_key_2       = task.sensor_key_2.replace(" ","")    
      data_2             = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2).last_values_json)
      sensor_value_2     = data_2[sensor_key_2]
         

      ####################
      # compare conditions
      ####################
      
      passing_1 = False
      passing_2 = False
      
      # Options: <, >, =
   
      if task.main_operator_second_sensor == ">" or task.main_operator_second_sensor == "<" or task.main_operator_second_sensor == "=":
         
         if task.main_operator_second_sensor == "=":
            try:
               if int(sensor_value_1) == int(sensor_value_2):
                  passing = True    
               else:
                  passing = False
            except:
               if str(sensor_value_1).lower() == str(sensor_value_2).lower():
                  passing = True    
               else:
                  passing = False           
                  
         if task.main_operator_second_sensor == "<":
            if int(sensor_value_1) < int(sensor_value_2):
               passing = True
            else:
               passing = False
               
         if task.main_operator_second_sensor == ">":
            if int(sensor_value_1) > int(sensor_value_2):
               passing = True 
            else:
               passing = False         
     
      # Options: and, or
               
      if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
         
         # get passing value one
         
         passing_1 = False
         
         try:
            if task.operator_1 == "=" and not task.value_1.isdigit():
               if str(sensor_value_1).lower() == str(task.value_1).lower():
                  passing_1 = True
               else:
                  passing_1 = False
         except:
            pass
            
         try:  
            if task.operator_1 == "=" and task.value_1.isdigit():
               if int(sensor_value_1) == int(task.value_1):
                  passing_1 = True    
               else:
                  passing_1 = False
         except:
            pass
            
         try:                   
            if task.operator_1 == "<" and task.value_1.isdigit():
               if int(sensor_value_1) < int(task.value_1):
                  passing_1 = True
               else:
                  passing_1 = False
         except:
            pass
            
         try:                       
            if task.operator_1 == ">" and task.value_1.isdigit():
               if int(sensor_value_1) > int(task.value_1):
                  passing_1 = True 
               else:
                  passing_1 = False   
         except:
            pass                    
               
         
         # get passing value two
         
         passing_2 = False
            
         try:             
            if task.operator_2 == "=" and not task.value_2.isdigit():
               if str(sensor_value_2).lower() == str(task.value_2).lower():
                  passing_2 = True
               else:
                  passing_2 = False
         except:
            pass
            
         try: 
            if task.operator_2 == "=" and task.value_2.isdigit():
               if int(sensor_value_2) == int(task.value_2):
                  passing_2 = True    
               else:
                  passing_2 = False
         except:
            pass
            
         try: 
            if task.operator_2 == "<" and task.value_2.isdigit():
               if int(sensor_value_2) < int(task.value_2):
                  passing_2 = True
               else:
                  passing_2 = False
         except:
            pass
            
         try:                                
            if task.operator_2 == ">" and task.value_2.isdigit():
               if int(sensor_value_2) > int(task.value_2):
                  passing_2 = True 
               else:
                  passing_2 = False   
         except:
            pass                    
               
               
         # get result
         
         if task.main_operator_second_sensor == "and":
            if passing_1 == True and passing_2 == True:
               passing = True
            else:
               passing = False
                     
         if task.main_operator_second_sensor == "or":
            if passing_1 == True or passing_2 == True:
               passing = True         
            else:
               passing = False
      
   # Options ended                                 
   return passing


def CHECK_SCHEDULER_PING(task):

   ip_addresses = task.ip_addresses.split(",")

   for ip_address in ip_addresses:

      for x in range(3):
         if ping(ip_address, timeout=1) != None:    
            return True
            break  
     
   return False


""" ################################ """
""" ################################ """
"""         sunrise / sunset         """
""" ################################ """
""" ################################ """
   
   
# https://stackoverflow.com/questions/41072147/python-retrieve-the-sunrise-and-sunset-times-from-google

def GET_SUNRISE_TIME(lat, long):
   
   try:
   
      link     = "http://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0" % (lat, long)
      response = requests.get(link)
      data     = response.text
      
      # get sunrise data
      sunrise  = data[34:42]
      sunrise  = sunrise.split(":")
      
      # add one hour for CEST
      sunrise_hour   = str(int(sunrise[0]) + 1)
      sunrise_minute = str(sunrise[1])
      
      if len(sunrise_minute) == 1:
         sunrise_minute = str(0) + sunrise_minute
      
      sunrise = sunrise_hour + ":" + sunrise_minute

      return (sunrise)
      
      
   except Exception as e:    
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunrise / Sunset | " + str(e))
      SEND_EMAIL("ERROR", "Scheduler | Update Sunrise / Sunset | " + str(e))


def GET_SUNSET_TIME(lat, long):
 
   try:
      
      link     = "http://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0" % (lat, long)
      response = requests.get(link)
      data     = response.text
      
      # get sunset data
      sunset   = data[71:79]
      sunset   = sunset.split(":")
      
      # add one hour for CEST
      sunset_hour   = str(int(sunset[0]) + 1)
      sunset_minute = str(sunset[1]) 

      if len(sunset_minute) == 1:
         sunset_minute = str(0) + sunset_minute

      sunset = sunset_hour + ":" + sunset_minute

      return (sunset)


   except Exception as e:    
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunrise / Sunset | " + str(e))
      SEND_EMAIL("ERROR", "Scheduler | Update Sunrise / Sunset | " + str(e))


""" ################################ """
""" ################################ """
"""          scheduler tasks         """
""" ################################ """
""" ################################ """


def START_SCHEDULER_TASK(task_object):

   # ####################
   # start lighting scene
   # ####################

   try:
      if "lighting" in task_object.task and "start_scene" in task_object.task:

         task = task_object.task.split(" # ")
         
         group = GET_LIGHTING_GROUP_BY_NAME(task[2].strip())
         scene = GET_LIGHTING_SCENE_BY_NAME(task[3].strip())

         # group existing ?
         if group != None:

               # scene existing ?
               if scene != None:

                  try:
                     brightness = int(task[4].strip())
                  except:
                     brightness = 100

                  WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')                      
                  
                  SET_LIGHTING_GROUP_SCENE(group.id, scene.id, brightness)
                  CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

               else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Scene - " + task[3] + " - not founded")

         else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Group - " + task[2] + " - not founded")


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))


    # ###########
    # start light
    # ###########

   try:
      if "lighting" in task_object.task and "light" in task_object.task and "start_scene" not in task_object.task and "turn_off" not in task_object.task:

         task = task_object.task.split(" # ")
                     
         device = GET_DEVICE_BY_NAME(task[2].strip())

         # device existing ?
         if device != None:

               try:
                  rgb_values = re.findall(r'\d+', task[3])
               except:
                  rgb_values = []                                        

               try:
                  brightness = int(task[4].strip())
               except:
                  brightness = 100     

               if rgb_values != []:    
                  SET_LIGHT_RGB_THREAD(device.ieeeAddr, rgb_values[0], rgb_values[1], rgb_values[2], brightness)
                  CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "ON", 10)

               else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Network | Scheduler | Task - " + task_object.name + " | Invalid settings")  

         else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Light - " + task[2] + " - not founded") 

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))


   # #########
   # light off
   # #########

   try:
      if "lighting" in task_object.task and "turn_off" in task_object.task:
         
         task = task_object.task.split(" # ")

         if task[2].lower() == "group":

               # get input group names and lower the letters
               try:
                  list_groups = task[3].split(",")
               except:
                  list_groups = [task[3]]

               for input_group_name in list_groups: 
                  input_group_name = input_group_name.strip()

                  group_founded = False

                  # get exist group names 
                  for group in GET_ALL_LIGHTING_GROUPS():

                     WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')    

                     if input_group_name.lower() == group.name.lower():
                           group_founded = True   
                              
                           SET_LIGHTING_GROUP_TURN_OFF(group.id)
                           CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   

                  if group_founded == False:
                     WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Group - " + input_group_name + " - not founded")     


         if task[2].lower() == "light":

            device = GET_DEVICE_BY_NAME(task[3].strip())

            # device existing ?
            if device != None:                            
               SET_LIGHT_TURN_OFF_THREAD(device.ieeeAddr)
               CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "OFF", 10)

            else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Light - " + task[3].strip() + " - not founded")    


         if task[2].lower() == "all":

               WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')

               for light in GET_ALL_DEVICES("light"):
                  Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(light.ieeeAddr, ))
                  Thread.start()     

               for group in GET_ALL_LIGHTING_GROUPS():
                  CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   
                        

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))      


   # ######
   # device
   # ######

   try:
      if "device" in task_object.task and "update" not in task_object.task:
         
         task = task_object.task.split(" # ")

         # get input group names 
         for device_name in task[1].split(","): 
            device = GET_DEVICE_BY_NAME(device_name.strip())

            # device founded ?
            if device != None:
               scheduler_setting = task[2].strip()
               
               # check device exception
               check_result = CHECK_DEVICE_EXCEPTIONS(device.id, scheduler_setting)
                           
               if check_result == True:           

                  WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')    

                  if device.gateway == "mqtt":
                        channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                  if device.gateway == "zigbee2mqtt":   
                        channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                  command_position  = 0
                  list_command_json = device.commands_json.replace("},{", "};{")                       
                  list_command_json = list_command_json.split(";")
                  
                  # get the json command statement and start process
                  for command in device.commands.split(","):     
                                              
                     if str(scheduler_setting.lower()) == command.lower():
                        heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                        CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, scheduler_setting, 60)      
                        continue

                     command_position = command_position + 1


               else:
                  WRITE_LOGFILE_SYSTEM("WARNING", "Scheduler | Task - " + task_object.name + " | " + check_result)

            else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Device - " + device_name.strip() + " - not founded")                  


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))     


   # ########
   # programs
   # ########

   try:
      if "program" in task_object.task:
         
         task    = task_object.task.split(" # ")         
         program = GET_PROGRAM_BY_NAME(task[1].strip())

         if program != None:

               WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')

               if task[2].strip() == "START":
                  START_PROGRAM_THREAD(program.id)
                  
               elif task[2].strip() == "STOP":
                  STOP_PROGRAM_THREAD_BY_NAME(program.name) 
                        
               else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Invalid command")

         else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Program not founded")           


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))      


   # ###############
   # backup database 
   # ###############

   try:  
      if "backup_database" in task_object.task:
         BACKUP_DATABASE() 

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))     


   # ##############
   # update devices
   # ##############

   try:
      if "update_devices" in task_object.task:
         UPDATE_DEVICES("mqtt")
         UPDATE_DEVICES("zigbee2mqtt")

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))      


   # ###############
   # reset log files
   # ###############

   try:
      if "reset_log_files" in task_object.task:

         # reset device log if size > 2,5 mb
         file_size = os.path.getsize(PATH + "/data/logs/log_devices.csv")
         file_size = round(file_size / 1024 / 1024, 2)
         
         if file_size > 2.5:
            RESET_LOGFILE("log_devices")

         # reset system log if size > 2.5 mb
         file_size = os.path.getsize(PATH + "/data/logs/log_system.csv")
         file_size = round(file_size / 1024 / 1024, 2)
         
         if file_size > 2.5:
            RESET_LOGFILE("log_system")

         # delete system2mqtt log if size > 5 mb
         file_size = os.path.getsize(PATH + "/data/logs/zigbee2mqtt.txt")
         file_size = round(file_size / 1024 / 1024, 2)   

         if file_size > 5:
            os.remove (PATH + "/data/logs/zigbee2mqtt.txt")


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))      


   # ############
   # reset system 
   # ############

   try:
      if "reset_system" in task_object.task:
         WRITE_LOGFILE_SYSTEM("EVENT", "System | Reboot") 
         os.system("sudo reboot")         

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))     


   # ###############
   # shutdown system 
   # ###############

   try:
      if "shutdown_system" in task_object.task:
         WRITE_LOGFILE_SYSTEM("EVENT", "System | Shutdown")     
         os.system("sudo shutdown")     

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))     


   # ##################
   # request sensordata
   # ##################

   try:
      if "request_sensordata" in task_object.task:
         task = task_object.task.split(" # ")
         REQUEST_SENSORDATA(task[1].strip())  

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))              


   # #####
   # music
   # #####

   try:

      if "music" in task_object.task:
         task = task_object.task.split(" # ")

         spotify_token = GET_SPOTIFY_TOKEN()

         # check spotify login 
         if spotify_token != "":

               WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')
               
               sp       = spotipy.Spotify(auth=spotify_token)
               sp.trace = False
                          
               # basic control 

               if (task[1].strip() == "PLAY" or
                   task[1].strip() == "PREVIOUS" or
                   task[1].strip() == "NEXT" or
                   task[1].strip() == "STOP" or
                   task[1].strip() == "VOLUME"):
              
                  try: 
                     spotify_volume = sp.current_playback(market=None)['device']['volume_percent']
                  except:
                     spotify_volume = GET_SPOTIFY_SETTINGS().default_volume
                  
                  if task[1].strip() == "PLAY":
                     SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       
         
                  if task[1].strip() == "PREVIOUS":
                     SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                  if task[1].strip() == "NEXT":
                     SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                  if task[1].strip() == "STOP": 
                     SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                  if task[1].strip() == "VOLUME":            
                     spotify_volume = int(task[2])
                     SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  

               # start playlist
                     
               if task[1].strip() == "playlist": 

                  spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip())
                  playlist_uri      = GET_SPOTIFY_PLAYLIST(spotify_token, task[3].strip(), 20)
                  playlist_volume   = int(task[4].strip())
                  
                  SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
         
               # start track
                     
               if task[1].strip() == "track": 
                  
                  spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip())
                  track_uri         = SPOTIFY_SEARCH_TRACK(spotify_token, task[3].strip(), task[4].strip(), 1) [0][2]
                  track_volume      = int(task[5].strip())
                  
                  SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)
                  
               # start album
                     
               if task[1].strip() == "album": 
                                 
                  spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, task[2].strip())
                  album_uri         = SPOTIFY_SEARCH_ALBUM(spotify_token, task[3].strip(), task[4].strip(), 1) [0][2]
                  album_volume      = int(task[5].strip())
                  
                  SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)

         else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | No Spotify Token founded")   


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))    


   # ####################################
   # remove scheduler task without repeat
   # ####################################

   if task_object.option_repeat != "True":
      DELETE_SCHEDULER_TASK(task_object.id)
