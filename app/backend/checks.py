from app                         import app
from app.database.models         import *

import datetime


""" ################### """
"""  device exceptions  """
""" ################### """

def CHECK_DEVICE_EXCEPTION_SETTINGS(devices): 
   error_message_settings = []

   for device in devices:

      if device.exception_option != "None":

         if device.exception_setting == "None" or device.exception_setting == None:
            error_message_settings.append(device.name + " || Keine Aufgabe ausgewählt")         

         # exception setting ip_address
         if device.exception_option == "IP-Address":

            # search for wrong chars
            for element in device.exception_value_1:
               if not element.isdigit() and element != "." and element != "," and element != " ":
                  error_message_settings.append(device.name + " || Ungültige IP-Adresse")
                  break
               
         # exception setting sensor
         if device.exception_option != "IP-Address": 
            
            if device.exception_value_1 == "None" or device.exception_value_1 == None:
               error_message_settings.append(device.name + " || Keinen Sensor ausgewählt")

            if device.exception_value_2 == "None" or device.exception_value_2 == None:
               error_message_settings.append(device.name + " || Keinen Operator (<, >, =) eingetragen")

            if device.exception_value_3 == "None" or device.exception_value_3 == None:
               error_message_settings.append(device.name + " || Keinen Vergleichswert eingetragen")
                  
   return error_message_settings


""" ###################### """
"""  check ighting groups  """
""" ###################### """

def CHECK_LIGHTING_GROUP_SETTINGS(settings):
   list_errors = []

   # check setting open light_slots in groups
   for element in settings:
      
      if element.light_ieeeAddr_1 == None or element.light_ieeeAddr_1 == "None":
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 1")        
      if element.active_light_2 == "True" and (element.light_ieeeAddr_2 == None or element.light_ieeeAddr_2 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 2") 
      if element.active_light_3 == "True" and (element.light_ieeeAddr_3 == None or element.light_ieeeAddr_3 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 3") 
      if element.active_light_4 == "True" and (element.light_ieeeAddr_4 == None or element.light_ieeeAddr_4 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 4") 
      if element.active_light_5 == "True" and (element.light_ieeeAddr_5 == None or element.light_ieeeAddr_5 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 5") 
      if element.active_light_6 == "True" and (element.light_ieeeAddr_6 == None or element.light_ieeeAddr_6 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 6") 
      if element.active_light_7 == "True" and (element.light_ieeeAddr_7 == None or element.light_ieeeAddr_7 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 7") 
      if element.active_light_8 == "True" and (element.light_ieeeAddr_8 == None or element.light_ieeeAddr_8 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 8") 
      if element.active_light_9 == "True" and (element.light_ieeeAddr_9 == None or element.light_ieeeAddr_9 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> Lichtquelle 9")   
          
   return list_errors


""" ############## """
"""  check program """
""" ############## """

def CHECK_PROGRAM_TASKS(program_id):
   list_errors = []
   
   list_lines = [[GET_PROGRAM_BY_ID(program_id).line_active_1,  GET_PROGRAM_BY_ID(program_id).line_content_1],
                 [GET_PROGRAM_BY_ID(program_id).line_active_2,  GET_PROGRAM_BY_ID(program_id).line_content_2],
                 [GET_PROGRAM_BY_ID(program_id).line_active_3,  GET_PROGRAM_BY_ID(program_id).line_content_3],
                 [GET_PROGRAM_BY_ID(program_id).line_active_4,  GET_PROGRAM_BY_ID(program_id).line_content_4],
                 [GET_PROGRAM_BY_ID(program_id).line_active_5,  GET_PROGRAM_BY_ID(program_id).line_content_5],
                 [GET_PROGRAM_BY_ID(program_id).line_active_6,  GET_PROGRAM_BY_ID(program_id).line_content_6],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_7,  GET_PROGRAM_BY_ID(program_id).line_content_7],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_8,  GET_PROGRAM_BY_ID(program_id).line_content_8],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_9,  GET_PROGRAM_BY_ID(program_id).line_content_9],                 
                 [GET_PROGRAM_BY_ID(program_id).line_active_10, GET_PROGRAM_BY_ID(program_id).line_content_10],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_11, GET_PROGRAM_BY_ID(program_id).line_content_11],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_12, GET_PROGRAM_BY_ID(program_id).line_content_12],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_13, GET_PROGRAM_BY_ID(program_id).line_content_13],
                 [GET_PROGRAM_BY_ID(program_id).line_active_14, GET_PROGRAM_BY_ID(program_id).line_content_14],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_15, GET_PROGRAM_BY_ID(program_id).line_content_15],
                 [GET_PROGRAM_BY_ID(program_id).line_active_16, GET_PROGRAM_BY_ID(program_id).line_content_16],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_17, GET_PROGRAM_BY_ID(program_id).line_content_17],
                 [GET_PROGRAM_BY_ID(program_id).line_active_18, GET_PROGRAM_BY_ID(program_id).line_content_18],   
                 [GET_PROGRAM_BY_ID(program_id).line_active_19, GET_PROGRAM_BY_ID(program_id).line_content_19],            
                 [GET_PROGRAM_BY_ID(program_id).line_active_20, GET_PROGRAM_BY_ID(program_id).line_content_20],                  
                 [GET_PROGRAM_BY_ID(program_id).line_active_21, GET_PROGRAM_BY_ID(program_id).line_content_21],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_22, GET_PROGRAM_BY_ID(program_id).line_content_22],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_23, GET_PROGRAM_BY_ID(program_id).line_content_23],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_24, GET_PROGRAM_BY_ID(program_id).line_content_24],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_25, GET_PROGRAM_BY_ID(program_id).line_content_25],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_26, GET_PROGRAM_BY_ID(program_id).line_content_26],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_27, GET_PROGRAM_BY_ID(program_id).line_content_27],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_28, GET_PROGRAM_BY_ID(program_id).line_content_28], 
                 [GET_PROGRAM_BY_ID(program_id).line_active_29, GET_PROGRAM_BY_ID(program_id).line_content_29],  
                 [GET_PROGRAM_BY_ID(program_id).line_active_30, GET_PROGRAM_BY_ID(program_id).line_content_30]] 

   line_number = 0
            
   try:
   
      for line in list_lines:           
         line_number = line_number + 1

         # line active ?
         if line[0] == "True":
         
            
            # #####
            # break
            # #####
                  
            if "break" in line[1]:     
                     
               try: 
                  line_content = line[1].split(" # ")
                  
                  # check delay value            
                  if line_content[1].isdigit():
                     continue
                  else:
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> fehlende Einstellung >>> Sekunden")
                     
               except:
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")


            # ########
            # lighting     
            # ########    
            

            # start scene
            elif "lighting" in line[1] and "scene" in line[1]:
               
               try:        
                  line_content = line[1].split(" # ")

                  # check scene setting
                  if GET_LIGHTING_GROUP_BY_NAME(line_content[2]) == None: 
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Gruppe nicht gefunden >>> " + line_content[2])
                  
                  if GET_LIGHTING_SCENE_BY_NAME(line_content[3]) == None: 
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Szene nicht gefunden >>> " + line_content[3])

                  if not line_content[4].isdigit() or not (0 <= int(line_content[4]) <= 100):
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Helligkeitswert")

               except:
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")               
                        

            # turn_off
            elif "lighting" in line[1] and "turn_off" in line[1]:

               try:
                  line_content = line[1].split(" # ")

                  # check turn_off group setting
                  if line_content[2].lower() == "group":

                     for group_name in line_content[3].split(","):
                        if GET_LIGHTING_GROUP_BY_NAME(group_name.strip()) == None: 
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Gruppe nicht gefunden >>> " + group_name.strip())  

                  # check turn_off all setting
                  elif line_content[2].lower() == "all":
                     pass

                  else:
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")                            

               except:
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")


            # ######
            # device
            # ######

            elif "device" in line[1]:

               try:
                  line_content = line[1].split(" # ")

                  # check device names
                  for device_name in line_content[1].split(","):

                     if GET_DEVICE_BY_NAME(group_name.strip()) == None: 
                        list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> falsche Einstellung >>> Gerät nicht gefunden >>> " + device_name)       

                     # check commands
                     else:
                        
                        device  = GET_DEVICE_BY_NAME(device_name.strip())  
                        setting = task[2]

                        if setting.lower() not in device.commands_json.lower():
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> falsche Einstellung >>> Befehl ungültig >>> " + setting)


               except:
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")


            # ##################
            # request_sensordata
            # ##################
            
            elif "request_sensordata" in line[1]:

               try:        
                  line_content = line[1].split(" # ")     

                  if not GET_SENSORDATA_JOB_BY_NAME(line_content[1]):
                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Job nicht vorhanden")

               except:        
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")


            # #######
            # spotify 
            # #######
            
            elif "spotify" in line[1]:
               
               try:        
                  line_content = line[1].split(" # ")       
                  
                  if (line_content[1].lower() != "play" and
                      line_content[1].lower() != "previous" and
                      line_content[1].lower() != "next" and
                      line_content[1].lower() != "stop" and
                      line_content[1].lower() != "volume" and
                      line_content[1].lower() != "playlist" and
                      line_content[1].lower() != "track" and
                      line_content[1].lower() != "album"):

                     list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Befehl")

                  # volume

                  if line_content[1].lower() == "volume":
                     
                     try:
                        if not line_content[2].isdigit():
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")
                     
                        else:
                           if not 0 <= int(line_content[2]) <= 100:
                              list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")
                              
                     except:
                        list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                  # playlist
      
                  if line_content[1].lower() == "playlist": 
                     
                     try:
                        device_name   = line_content[2]                                    
                        playlist_name = line_content[3]
                        
                        try:
                           if not line_content[4].isdigit():
                              list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")
                           
                           else:
                              if not 0 <= int(line_content[4]) <= 100:
                                 list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")

                        except:
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                     except:
                        list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Unvollständige Angaben")

                  # track
                        
                  if line_content[1].lower() == "track": 
                     
                     try:
                        device_name  = line_content[2]                                    
                        track_title  = line_content[3]
                        track_artist = line_content[4]
                        
                        try:
                           if not line_content[5].isdigit():
                              list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                           else:
                              if not 0 <= int(line_content[5]) <= 100:
                                 list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")

                        except:
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                     except:
                        list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Unvollständige Angaben")

                  # album

                  if line_content[1].lower() == "album": 
                     
                     try:
                        device_name  = line_content[2]                                    
                        album_title  = line_content[3]
                        album_artist = line_content[4]
                        
                        try:
                           if not line_content[5].isdigit():
                              list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                           else:
                              if not 0 <= int(line_content[5]) <= 100:
                                 list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")

                        except:
                           list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültiger Lautstärkewert")

                     except:
                        list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Unvollständige Angaben")

               except:
                  list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> Ungültige Formatierung")

         # ####
         # None
         # ####

            elif line[1] == "None":
               pass

            #  other

            elif line[1] != "":
               list_errors.append("Zeile " + str(line_number) + " - " + line[1] + " >>> falsche Einstellung >>> Eingabetyp nicht gefunden")
             
   except:
      pass

   return list_errors


""" ######################### """
"""  check scheduler settings """
""" ######################### """


def CHECK_SCHEDULER_TASKS_SETTINGS(scheduler_tasks): 
   list_errors = []  

   for task in scheduler_tasks:

      if task.option_time != "True" and task.option_sun != "True" and task.option_sensors != "True" and task.option_position != "True":    
         list_errors.append(task.name + " >>> Keine Bedingungsoption ausgewählt")          


      if task.option_time == "True":

         # check settings sunrise / sunset option
         if task.option_sun == "True":
            list_errors.append(task.name + " >>> Ungültige Kombination >>> Zeit und Sonne nur getrennt verwenden")         

         ### check day

         try:
            if "," in task.day:
                  days = task.day.replace(" ", "")
                  days = days.split(",")
                  for element in days:
                     if element.lower() not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                        list_errors.append(task.name + " >>> falsche Zeitangabe >>> Tag >>> Gültig: Mon, Tue, Wed, Thu, Fri, Sat, Sun, *")
                        break                                 
            else:
                  if task.day.lower() not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "*"] and task.day != "*":
                     list_errors.append(task.name + " >>> falsche Zeitangabe >>> Tag >>> Gültig: Mon, Tue, Wed, Thu, Fri, Sat, Sun, *") 
         except:
            list_errors.append(task.name + " >>> falsche Zeitangabe >>> Tag >>> Gültig: Mon, Tue, Wed, Thu, Fri, Sat, Sun, *")

         ### check hour
            
         try:
            if "," in task.hour:
                  hours = task.hour.replace(" ", "")                
                  hours = hours.split(",")
                  
                  for element in hours:
 
                     if len(element) == 1 and element != "*":
                        list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")
                        break
                    
                     try:
                        if not (0 <= int(element) <= 24):
                           list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")
                           break
                        
                     except:
                        list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")
                        break   
            else:
                  
               if len(task.hour) == 1 and task.hour != "*":
                  list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")
                  break
                
               try:
                  if not (0 <= int(task.hour) <= 24) and task.hour != "*":
                     list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *") 
               except:
                  if task.hour != "*":
                     list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")    

         except:
            list_errors.append(task.name + " >>> falsche Zeitangabe >>> Stunde >>> Gültig: 00 - 23, *")

         ### check minute

         try:
            if "," in task.minute:
                  minutes = task.minute.replace(" ", "")                 
                  minutes = minutes.split(",")
                  
                  for element in minutes:
                      
                     if len(element) == 1 and element != "*":
                        list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *")
                        break                      
                      
                     try:
                        if not (0 <= int(element) <= 60):
                           list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *") 
                           break
                        
                     except:
                        list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *") 
                        break   
            else:
                
               if len(task.minute) == 1 and task.minute != "*":
                  list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *")
                  break
                
               try:
                  if not (0 <= int(task.minute) <= 60) and task.minute != "*":
                     list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *") 
               except:
                  if task.minute != "*":
                     list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *") 
      
         except:
            list_errors.append(task.name + " >>> falsche Zeitangabe >>> Minute >>> Gültig: 00 - 59, *") 


      if task.option_sun == "True":

         # check setting location
         if task.option_sunrise == "True" or task.option_sunset == "True":
            if task.location == "None":
               list_errors.append(task.name + " >>> Zone wurde noch nicht eingestellt")

      if task.option_sensors == "True":

         # check mqtt devices
         if task.device_ieeeAddr_1 == "None" or task.device_ieeeAddr_1 == "" or task.device_ieeeAddr_1 == None:
            list_errors.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 1") 

         if task.device_ieeeAddr_2 == "None" or task.device_ieeeAddr_2 == "" or task.device_ieeeAddr_2 == None:
            if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
               list_errors.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 2") 
                  
         # check sensors
         if task.sensor_key_1 == "None" or task.sensor_key_1 == None:
            list_errors.append(task.name + " >>> fehlende Einstellung >>> Sensor 1") 
            
         if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
            if task.sensor_key_2 == "None" or task.sensor_key_2 == None:
               list_errors.append(task.name + " >>> fehlende Einstellung >>> Sensor 2")  
               
         # check operators
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":
            if task.operator_1 == "" or task.operator_1 == "None" or task.operator_1 == None: 
               list_errors.append(task.name + " >>> fehlende Einstellung >>> Operator 1")
         
         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.operator_2 == "None" or task.operator_2 == "" or task.operator_2 == None: 
               list_errors.append(task.name + " >>> fehlende Einstellung >>> Operator 2")  

         # check values
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":   
            if task.value_1 == "" or task.value_1 == "None" or task.value_1 == None: 
               list_errors.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 1")   
                  
            elif (task.operator_1 == "<" or task.operator_1 == ">") and not task.value_1.isdigit():
               list_errors.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 1 >>> nur Zahlen können mit dem gewählten Operator verwendet werden") 

         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.value_2 == "" or task.value_2 == "None" or task.value_2 == None:
               list_errors.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 2")  
            elif (task.operator_2 == "<" or task.operator_2 == ">") and not task.value_2.isdigit():
               list_errors.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 2 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")                 
  
               
      if task.option_position == "True":

         # check setting choosed
         if task.option_home != "True" and task.option_away != "True":
            list_errors.append(task.name + " >>> fehlende Einstellung >>> HOME oder AWAY")

         # check setting home / away
         if task.option_home == "True" and task.option_away == "True":
            list_errors.append(task.name + " >>> Es kann nur HOME oder AWAY separat gewählt werden")

         # check setting ip-addresses
         if task.option_home == "True" or task.option_away == "True":

            if task.ip_addresses != "None":
               
               # search for wrong chars
               for element in task.ip_addresses:
                  if not element.isdigit() and element != "." and element != "," and element != " ":
                     list_errors.append(task.name + " >>> Ungültige IP-Adressen")
                     break

   return list_errors


""" ################### """
"""     check tasks     """
""" ################### """

def CHECK_TASKS(tasks, task_type):
   list_task_errors = []

   # controller
   
   if task_type == "controller": 

      for controller in tasks:

         name = GET_DEVICE_BY_IEEEADDR(controller.device_ieeeAddr).name

         if controller.command_1 != None and controller.command_1 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_1, name, task_type, controller.command_1)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)    
               
         if controller.command_2 != None and controller.command_2 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_2, name, task_type, controller.command_2)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)        
                         
         if controller.command_3 != None and controller.command_3 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_3, name, task_type, controller.command_3)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)                 
               
         if controller.command_4 != None and controller.command_4 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_4, name, task_type, controller.command_4)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)       
               
         if controller.command_5 != None and controller.command_5 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_5, name, task_type, controller.command_5)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)                     
               
         if controller.command_6 != None and controller.command_6 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_6, name, task_type, controller.command_6)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)       
               
         if controller.command_7 != None and controller.command_7 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_7, name, task_type, controller.command_7)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)                   
               
         if controller.command_8 != None and controller.command_8 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_8, name, task_type, controller.command_8)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)                   
                                             
         if controller.command_9 != None and controller.command_9 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_9, name, task_type, controller.command_9)
            
            if result != []:
               
               for error in result:   
                  list_task_errors.append(error)            

   # scheduler

   if task_type == "scheduler":

      for element in tasks:
         result = CHECK_TASK_OPERATION(element.task, element.name, task_type)
         
         if result != []:
            
            for error in result:   
               list_task_errors.append(error)


   return list_task_errors


def CHECK_TASK_OPERATION(task, name, task_type, controller_command_json = ""):
   
   list_task_errors   = []
   controller_command = controller_command_json[1:-1].replace('"','')

   try:
      

      # ###########
      # start_scene
      # ###########
      
      if "lighting" in task and "scene" in task:
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 

            try:

               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 

                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Gruppe nicht vorhanden >>> " + task[2].strip())  
                  else:                               
                     list_task_errors.append(name + " >>> Gruppe nicht vorhanden >>> " + task[2].strip())  

            except:
               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Gruppe")
               else:
                  list_task_errors.append(name + " >>> fehlende Einstellung >>> Gruppe")

            # check scene setting    

            try:

               if GET_LIGHTING_SCENE_BY_NAME(task[3].strip()) == None: 

                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Szene nicht vorhanden >>> " + task[3].strip())  
                  else:                               
                     list_task_errors.append(name + " >>> Szene nicht vorhanden >>> " + task[3].strip())  
                  
            except:

               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Szene")
               else:               
                  list_task_errors.append(name + " >>> fehlende Einstellung >>> Szene")

            # check brightness    

            try:

               if task[4].isdigit():
                  if 1 <= int(task[4]) <= 100:
                     return list_task_errors

                  else:
                     if task_type == "controller":
                        list_task_errors.append(name + " >>> " + controller_command + " >>> ungültiger Wertebereich >>> Helligkeit")
                     else:                        
                        list_task_errors.append(name + " >>> ungültiger Wertebereich >>> Helligkeit") 
                     return list_task_errors    

               else:
                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> ungültige Einstellung >>> Helligkeit")
                  else:                     
                     list_task_errors.append(name + " >>> ungültige Einstellung >>> Helligkeit")
                  return list_task_errors

            except:
               return list_task_errors

         else:
            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
            else:                
               list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors
     
     
      # #################
      # brightness dimmer
      # #################
      
      if "lighting" in task and "brightness" in task and task_type == "controller":
         if " # " in task:
            task = task.split(" # ") 

            # check group setting
            try:
               if GET_LIGHTING_GROUP_BY_NAME(task[2]):
                  pass
                  
               else:
                  list_task_errors.append(name + " >>> " + controller_command + " >>> Gruppe nicht vorhanden >>> " + task[2])   
                                    
            except:
               list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Gruppe")      

            # check brightness setting    
            try:
               if task[3].lower() == "turn_up" or task[3].lower() == "turn_down":
                  return list_task_errors
                  
               else:
                  list_task_errors.append(name + " >>> " + controller_command + " >>> TURN_UP oder TURN_DOWN ?")
                  return list_task_errors
                  
            except:
               list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> TURN_UP oder TURN_DOWN")    
               return list_task_errors

         else:
            list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
            return list_task_errors


      # ########
      # turn_off
      # ########
      
      if "lighting" in task and "turn_off" in task:
         if " # " in task:
            task = task.split(" # ")
            
            # check turn_off groups
            if "group" in task[2]:

               try:      
                  # check group names 
                  for group_name in task[3].split(","):
                     if GET_LIGHTING_GROUP_BY_NAME(group_name.strip()) == None: 

                        if task_type == "controller":
                           list_task_errors.append(name + " >>> " + controller_command + " >>> Gruppe nicht vorhanden >>> " + group_name.strip())  
                        else:                               
                           list_task_errors.append(name + " >>> Gruppe nicht vorhanden >>> " + group_name.strip())  
                     
                  return list_task_errors

               except:

                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Gruppe")
                  else:                            
                     list_task_errors.append(name + " >>> fehlende Einstellung >>> Gruppe")
                  
                  return list_task_errors
                        
   
            # check turn off all lights
            elif task[2].lower() == "all": 
               return list_task_errors


            else:
               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Eingabe >>> 'all' oder 'group'")
               else:                   
                  list_task_errors.append(name + " >>> Ungültige Eingabe >>> 'all' oder 'group' ?")
               return list_task_errors  


         else:
            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung") 
            else:                   
               list_task_errors.append(name + " >>> Ungültige Formatierung")     
            return list_task_errors


      # ######
      # device
      # ######
      
      if "device" in task and "update" not in task:

         if " # " in task:
            task = task.split(" # ") 

            try:

               # check device names
               for device_name in task[1].split(","):

                  if GET_DEVICE_BY_NAME(device_name.strip()) == None: 

                     if task_type == "controller":
                        list_task_errors.append(name + " >>> " + controller_command + " >>> Gerät nicht gefunden >>> " + device_name)
                     else:
                        list_task_errors.append(name + " >>> Gerät nicht gefunden >>> " + device_name)           

                  # check commands
                  else:

                     device  = GET_DEVICE_BY_NAME(device_name.strip())  
                     setting = task[2]

                     if setting.lower() not in device.commands_json.lower():
                  
                        if task_type == "controller":
                           list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültiger Befehl >>> " + setting)
                        else:
                           list_task_errors.append(name + " >>> Ungültiger Befehl >>> " + setting)
                             
               return list_task_errors                  
              
            except:
               
               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
               else:                
                  list_task_errors.append(name + " >>> Ungültige Formatierung")       

               return list_task_errors

         else:
            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
            else:                
               list_task_errors.append(name + " >>> Ungültige Formatierung")   

            return list_task_errors
            

      # #######
      # program
      # #######
      
      if "program" in task:
         if " # " in task:
            task = task.split(" # ") 

            try:
               program = GET_PROGRAM_BY_NAME(task[1].lower())
               setting = task[2].lower()
                  
               if program == None:
               
                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Programm nicht gefunden >>> " + task[1])
                  else:
                     list_task_errors.append(name + " >>> " + task[1] + " Programm nicht gefunden")                  
                  
               if setting != "start" and setting != "stop" and setting != "repeat" and setting != "force":
                  
                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültiger Befehl >>> " + task[2])
                  else:
                     list_task_errors.append(name + " >>> Ungültiger Befehl >>> " + task[2])
 
               return list_task_errors
      
      
            except:
               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
               else:
                  list_task_errors.append(name + " >>> Ungültige Formatierung")
               return list_task_errors
         
         
         else:
            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
            else:                
               list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors
         

      # ###############
      # backup_database  
      # ###############  
       
      if task == "backup_database" and task_type == "scheduler":
         return list_task_errors


      # ##############
      # update_devices
      # ##############
   
      if task == "update_devices" and task_type == "scheduler":
         return list_task_errors


      # ####################
      # check_mqtt_connetion
      # ####################
      
      if task == "check_mqtt_connetion" and task_type == "scheduler":
         return list_task_errors


      # ##################
      # request_sensordata
      # ##################
        
      if "request_sensordata" in task:
         if " # " in task:
            task = task.split(" # ")

            # check job name setting
            try:     

               if GET_SENSORDATA_JOB_BY_NAME(task[1]):
                  return list_task_errors

               else:
                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Job nicht vorhanden >>> " + task[1])
                  else:
                     list_task_errors.append(name + " >>> Job nicht vorhanden >>> " + task[1])

                  return list_task_errors   

            except:

                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Job-Name")
                  else:
                     list_task_errors.append(name + " >>> fehlende Einstellung >>> Job-Name") 

                  return list_task_errors

         else:

            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Job-Name")
            else:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> Job-Name") 

            return list_task_errors


      # #######
      # spotify     
      # #######
        
      if "spotify" in task:
         if " # " in task:
            task = task.split(" # ")

            # check settings
            try:   
                   
               if task[1].lower() == "play":
                  return list_task_errors

               elif task[1].lower() == "play/stop":
                  return list_task_errors

               elif task[1].lower() == "previous":
                  return list_task_errors
             
               elif task[1].lower() == "next":
                  return list_task_errors   
                  
               elif task[1].lower() == "stop":
                  return list_task_errors
             
               elif task[1].lower() == "volume_up":
                  return list_task_errors                     
                                 
               elif task[1].lower() == "volume_down":
                  return list_task_errors
             
               elif task[1].lower() == "volume":             
             
                  try:
                     if not task[2].isdigit():
                        list_task_errors.append(name + " >>> """ + task[2] + " >>> Ungültiger Lautstärkewert") 
                     else:
                        if not 0 <= int(task[2]) <= 100:
                           list_task_errors.append(name + " >>> """ + task[2] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")
                           
                     return list_task_errors
                           
                  except:
                     list_task_errors.append(name + " >>> """ + task[2] + " >>> Ungültiger Lautstärkewert") 
                     return list_task_errors
                  
               elif task[1].lower() == "playlist": 
                  
                  try:
                     device_name   = task[2]                                    
                     playlist_name = task[3]
                     
                     try:
                        if not task[4].isdigit():
                           list_task_errors.append(name + " >>> """ + task[4] + " >>> Ungültiger Lautstärkewert") 
                        else:
                           if not 0 <= int(task[4]) <= 100:
                              list_task_errors.append(name + " >>> """ + task[4] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")
                              
                        return list_task_errors
                                 
                     except:
                        list_task_errors.append(name + " >>> """ + task[4] + " >>> Ungültiger Lautstärkewert") 
                        return list_task_errors
                        
                  except:
                     list_task_errors.append(name + " >>> """ + str(task) + " >>> Unvollständige Angaben")  
                     return list_task_errors                
                     
               elif task[1].lower() == "track": 
                  
                  try:
                     device_name  = task[2]                                    
                     track_title  = task[3]
                     track_artist = task[4]
                     
                     try:
                        if not task[5].isdigit():
                           list_task_errors.append(name + " >>> """ + task[5] + " >>> Ungültiger Lautstärkewert") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              list_task_errors.append(name + " >>> """ + task[5] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")
                              
                        return list_task_errors
                                 
                     except:
                        list_task_errors.append(name + " >>> """ + task[5] + " >>> Ungültiger Lautstärkewert") 
                        return list_task_errors
                        
                  except:
                     list_task_errors.append(name + " >>> """ + str(task) + " >>> Unvollständige Angaben") 
                     return list_task_errors  

               elif task[1].lower() == "album": 
                  
                  try:
                     device_name  = task[2]                                    
                     album_title  = task[3]
                     album_artist = task[4]
                     
                     try:
                        if not task[5].isdigit():
                           list_task_errors.append(name + " >>> """ + task[5] + " >>> Ungültiger Lautstärkewert") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              list_task_errors.append(name + " >>> """ + task[5] + " >>> Zulässige Lautstärke liegt zwischen 0 % und 100 %")
                        
                        return list_task_errors
                                 
                     except:
                        list_task_errors.append(name + " >>> """ + task[5] + " >>> Ungültiger Lautstärkewert") 
                        return list_task_errors
                        
                  except:
                     list_task_errors.append(name + " >>> """ + str(task) + " >>> Unvollständige Angaben") 
                     return list_task_errors                   

               else:
                  if task_type == "controller":
                     list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültiger Befehl >>> " + task[1])
                  else:
                     list_task_errors.append(name + " >>> """ + task[1] + " >>> Ungültiger Befehl")
                  return list_task_errors


            except:
               if task_type == "controller":
                  list_task_errors.append(name + " >>> " + controller_command + " >>> fehlende Einstellung >>> Befehl") 
               else:
                  list_task_errors.append(name + " >>> Befehl >>> fehlende Einstellung") 
               return list_task_errors

                               
         else:
            if task_type == "controller":
               list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Formatierung")
            else:
               list_task_errors.append(name + " >>> Ungültige Formatierung")   
            return list_task_errors
            

      # #####################
      # empty task controller
      # #####################

      if task == None and task_type == "controller": 
         return list_task_errors

      if task == "None" and task_type == "controller": 
         return list_task_errors

      if task == "" and task_type == "controller": 
         return list_task_errors


      # #############
      # nothing found
      # #############
      
      
      if task_type == "controller":
         list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Aufgabe") 
      else:
         list_task_errors.append(name + " >>> Ungültige Aufgabe")
         
      return list_task_errors
   

   except:

      # #####################
      # empty task controller
      # #####################

      if task == None and task_type == "controller": 
         return list_task_errors

      elif task == "None" and task_type == "controller": 
         return list_task_errors

      elif task == "" and task_type == "controller": 
         return list_task_errors


      # ##########
      # task error
      # ##########

      elif task_type == "controller":
         list_task_errors.append(name + " >>> " + controller_command + " >>> Ungültige Aufgabe")   
         return list_task_errors

      else:
         list_task_errors.append(name + " >>> Ungültige Aufgabe")        
         return list_task_errors
