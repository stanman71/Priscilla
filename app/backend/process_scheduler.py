import datetime
import time
import json
import os
import requests
import heapq
import spotipy
import re

from app                          import app
from app.database.models          import *
from app.backend.led              import *
from app.backend.mqtt             import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM, GET_LOCATION_COORDINATES, BACKUP_DATABASE
from app.backend.shared_resources import process_management_queue, mqtt_message_queue
from app.backend.process_program  import START_PROGRAM_THREAD, STOP_PROGRAM_THREAD
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
   if task.option_time == "True":
      if not CHECK_SCHEDULER_TIME(task):
         return
      else:
         start_task = True

   # check sensors
   if task.option_sensors == "True":

      # find sensor jobs with fitting ieeeAddr only
      if (task.device_ieeeAddr_1 == ieeeAddr or task.device_ieeeAddr_2 == ieeeAddr):
         if not CHECK_SCHEDULER_SENSORS(task):
            return
         else:
            start_task = True

   # check sun
   if task.option_sunrise == "True":
      if not CHECK_SCHEDULER_SUNRISE(task):
         return   
      else:
         start_task = True

   if task.option_sunset == "True":
      if not CHECK_SCHEDULER_SUNSET(task):
         return     
      else:
         start_task = True

   # check position
   if task.option_position == "True": 
   
      if task.option_home == "True" or task.option_away == "True":
         ping_result = CHECK_SCHEDULER_PING(task)
  
         if task.option_home == "True" and ping_result == "False": 
            return          
         elif task.option_away == "True" and ping_result == "True":
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

   # check day
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


   # check minute
   if passing == True:

      if "," in task.hour:
          
         hours = task.hour.replace(" ", "")         
         hours = hours.split(",")
         
         for element in hours:
             
            if str(element) == str(current_hour):
               passing = True
               break
            
            else:
               passing = False
      else:
          
         if str(task.hour) == str(current_hour) or str(task.hour) == "*":
            passing = True
            
         else:
            passing = False              


   # check minute
   if passing == True:

      if "," in task.minute:
          
         minutes = task.minute.replace(" ", "")          
         minutes = minutes.split(",")
         
         for element in minutes:
             
            if str(element) == str(current_minute):
               passing = True
               break
            
            else:
               passing = False
               
      else:
          
         if str(task.minute) == str(current_minute) or str(task.minute) == "*":
            passing = True
            
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
   
      if ((task.main_operator_second_sensor == ">" or task.main_operator_second_sensor == "<" or task.main_operator_second_sensor == "=") and
          (sensor_value_1 != "Message nicht gefunden" and sensor_value_2 != "Message nicht gefunden")):
         
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
            if task.operator_1 == "=" and not task.value_1.isdigit() and sensor_value_1 != "Message nicht gefunden":
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
            if task.operator_2 == "=" and not task.value_2.isdigit() and sensor_value_1 != "Message nicht gefunden":
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
            return "True"
            break  
     
   return "False"


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
      WRITE_LOGFILE_SYSTEM("ERROR", "Update Sunrise / Sunset | " + str(e))
      SEND_EMAIL("ERROR", "Update Sunrise / Sunset | " + str(e))


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
      WRITE_LOGFILE_SYSTEM("ERROR", "Update Sunrise / Sunset | " + str(e))
      SEND_EMAIL("ERROR", "Update Sunrise / Sunset | " + str(e))


""" ################################ """
""" ################################ """
"""          scheduler tasks         """
""" ################################ """
""" ################################ """


def START_SCHEDULER_TASK(task_object):

   # ###########
   # start scene
   # ###########

   try:
      if "scene" in task_object.task:

         task = task_object.task.split(" # ")
         
         group = GET_LED_GROUP_BY_NAME(task[1])
         scene = GET_LED_SCENE_BY_NAME(task[2])

         # group existing ?
         if group != None:

               # scene existing ?
               if scene != None:

                  try:
                     brightness = int(task[3])
                  except:
                     brightness = 100

                  WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')                      
                  
                  SET_LED_GROUP_SCENE(group.id, scene.id, brightness)
                  CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

               else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Scene - " + task[2] + " - not founded")

         else:
               WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Group - " + task[1] + " - not founded")


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))


   # #######
   # led off
   # #######

   try:
      if "led_off" in task_object.task:
         
         task = task_object.task.split(" # ")

         if task[1] == "group":

               # get input group names and lower the letters
               try:
                  list_groups = task[2].split(",")
               except:
                  list_groups = [task[2]]

               for input_group_name in list_groups: 
                  input_group_name = input_group_name.replace(" ", "")

                  group_founded = False

                  # get exist group names 
                  for group in GET_ALL_LED_GROUPS():

                     if input_group_name.lower() == group.name.lower():
                           group_founded = True   
                              
                           WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')                              
                           
                           SET_LED_GROUP_TURN_OFF(group.id)
                           CHECK_LED_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   

                  if group_founded == False:
                     WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Group - " + input_group_name + " - not founded")     


         if task[1] == "all" or task[1] == "ALL":

               for group in GET_ALL_LED_GROUPS():
                  scene_name = group.current_scene
                  scene      = GET_LED_SCENE_BY_NAME(scene_name)

                  WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')

                  SET_LED_GROUP_TURN_OFF(group.id)
                  CHECK_LED_GROUP_SETTING_THREAD(group.id, scene.id, "OFF", 0, 5, 20)    
                        

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))      


   # ######
   # device
   # ######

   try:
      if "device" in task_object.task and "update" not in task_object.task:
         
         task = task_object.task.split(" # ")

         # get input group names and lower the letters
         try:
            list_devices = task[1].split(",")
         except:
            list_devices = [task[1]]


         for input_device_name in list_devices: 
            input_device_name = input_device_name.replace(" ", "")

            device = GET_DEVICE_BY_NAME(input_device_name.lower())

            # device founded ?
            if device != None:
                  scheduler_setting = task[2]
                  
                  # check device exception
                  check_result = CHECK_DEVICE_EXCEPTIONS(device.id, scheduler_setting)
                            
                  if check_result == True:           

                     WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')    

                     if device.gateway == "mqtt":
                           channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  
                     if device.gateway == "zigbee2mqtt":   
                           channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                     command_position  = 0
                     list_command_json = device.commands_json.split(",")

                     # get the json command statement and start process
                     for command in device.commands.split(","):     
                                          
                           if scheduler_setting in command:
                              heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                              CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, scheduler_setting, 20)      
                              break

                           command_position = command_position + 1

                  else:
                     WRITE_LOGFILE_SYSTEM("WARNING", "Scheduler | Task - " + task_object.name + " | " + check_result)

            else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Device - " + input_device_name + " - not founded")                  


   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))     


   # ########
   # programs
   # ########

   try:
      if "program" in task_object.task:
         
         task    = task_object.task.split(" # ")
         program = GET_PROGRAM_BY_NAME(task[1].lower())

         if program != None:

               WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')

               if task[2] == "start" and GET_PROGRAM_STATUS() == None:
                  START_PROGRAM_THREAD(program.id)
                  
               elif task[2] == "start" and GET_PROGRAM_STATUS() != None:
                  WRITE_LOGFILE_SYSTEM("WARNING", "Scheduler | Task - " + task_object.name + " | Other Program running")  
                  
               elif task[2] == "stop":
                  STOP_PROGRAM_THREAD() 
                  
               else:
                  WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | Command not valid")

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


   # ##################
   # request sensordata
   # ##################

   try:
      if "request_sensordata" in task_object.task:
         task = task_object.task.split(" # ")
         REQUEST_SENSORDATA(task[1])  

   except Exception as e:
      print(e)
      WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Task - " + task_object.name + " | " + str(e))              


   # #######
   # spotify
   # #######

   try:

      if "spotify" in task_object.task:
         task = task_object.task.split(" # ")

         spotify_token = GET_SPOTIFY_TOKEN()

         # check spotify login 
         if spotify_token != "":

               WRITE_LOGFILE_SYSTEM("EVENT", 'Scheduler | Task - ' + task_object.name + ' | started')
               
               sp       = spotipy.Spotify(auth=spotify_token)
               sp.trace = False
               
               
               # basic control
               
               try:
               
                  spotify_device_id = sp.current_playback(market=None)['device']['id']
                  spotify_volume    = sp.current_playback(market=None)['device']['volume_percent']

                  if task[1].lower() == "play":
                     SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       
         
                  if task[1].lower() == "previous":
                     SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                  if task[1].lower() == "next":
                     SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                  if task[1].lower() == "stop": 
                     SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                  if task[1].lower() == "volume":            
                     spotify_volume = int(task[2])
                     SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  

               except:
                  pass
                  
                  
               # start playlist
                     
               if task[1].lower() == "playlist": 

                  # get spotify_device_id
                  device_name          = task[2]                                    
                  list_spotify_devices = sp.devices()["devices"]  
                  spotify_device_id    = 0
                  
                  for device in list_spotify_devices:

                     # spotify client
                     if device['name'].lower() == device_name.lower():
                        spotify_device_id = device['id']  
                        continue      

                     # select multiroom group
                     if device_name.lower() == "multiroom":
                        if "multiroom" in device['name'].lower():
                           spotify_device_id = device['id'] 
                           continue    

                  # if device not founded, reset raspotify on client music               
                  if spotify_device_id == 0:
                     device = GET_DEVICE_BY_NAME(device_name)

                     heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                     time.sleep(5)

                     for device in list_spotify_devices:

                           # spotify client
                           if device['name'].lower() == device_name.lower():
                              spotify_device_id = device['id']  
                              continue      

                           # select multiroom group
                           if device_name.lower() == "multiroom":
                              if "multiroom" in device['name'].lower():
                                 spotify_device_id = device['id'] 
                                 continue                               
                  
                  # get playlist_uri
                  playlist_name          = task[3]
                  list_spotify_playlists = sp.current_user_playlists(limit=20)["items"]
                  
                  for playlist in list_spotify_playlists:
                     if playlist['name'].lower() == playlist_name.lower():
                           playlist_uri = playlist['uri']
                           continue
                        
                  # get volume
                  playlist_volume = int(task[4])
                  
                  SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
         
         
               # start track
                     
               if task[1].lower() == "track": 

                  # get spotify_device_id
                  device_name          = task[2]                                    
                  list_spotify_devices = sp.devices()["devices"]  
                  spotify_device_id    = 0
                  
                  for device in list_spotify_devices:

                     # spotify client
                     if device['name'].lower() == device_name.lower():
                           spotify_device_id = device['id']  
                           continue      

                     # select multiroom group
                     if device_name.lower() == "multiroom":
                           if "multiroom" in device['name'].lower():
                              spotify_device_id = device['id'] 
                              continue    

                  # if device not founded, reset raspotify on client music               
                  if spotify_device_id == 0:
                     device = GET_DEVICE_BY_NAME(device_name)

                     heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                     time.sleep(5)

                     for device in list_spotify_devices:

                           # spotify client
                           if device['name'].lower() == device_name.lower():
                              spotify_device_id = device['id']  
                              continue      

                           # select multiroom group
                           if device_name.lower() == "multiroom":
                              if "multiroom" in device['name'].lower():
                                 spotify_device_id = device['id'] 
                                 continue                                 
                  
                  # get playlist_uri
                  track_uri = SPOTIFY_SEARCH_TRACK(spotify_token, task[3], task[4], 1) [0][2]
                        
                  # get volume
                  track_volume = int(task[5])
                  
                  SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)


               # start album
                     
               if task[1].lower() == "album": 

                  # get spotify_device_id
                  device_name          = task[2]                                    
                  list_spotify_devices = sp.devices()["devices"]  
                  spotify_device_id    = 0
                  
                  for device in list_spotify_devices:

                     # spotify client
                     if device['name'].lower() == device_name.lower():
                           spotify_device_id = device['id']  
                           continue      

                     # select multiroom group
                     if device_name.lower() == "multiroom":
                           if "multiroom" in device['name'].lower():
                              spotify_device_id = device['id'] 
                              continue    

                  # if device not founded, reset raspotify on client music               
                  if spotify_device_id == 0:
                     device = GET_DEVICE_BY_NAME(device_name)

                     heapq.heappush(mqtt_message_queue, (10, ("smarthome/mqtt/" + device.ieeeAddr + "/set", '{"interface":"restart"}')))
                     time.sleep(5)

                     for device in list_spotify_devices:

                           # spotify client
                           if device['name'].lower() == device_name.lower():
                              spotify_device_id = device['id']  
                              continue      

                           # select multiroom group
                           if device_name.lower() == "multiroom":
                              if "multiroom" in device['name'].lower():
                                 spotify_device_id = device['id'] 
                                 continue                                   
                  
                  # get album_uri
                  album_uri = SPOTIFY_SEARCH_ALBUM(spotify_token, task[3], task[4], 1) [0][2]
                        
                  # get volume
                  album_volume = int(task[5])
                  
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
