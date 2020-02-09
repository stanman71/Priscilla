from app                         import app
from app.backend.database_models import *

import datetime


""" ################### """
"""  device exceptions  """
""" ################### """

def CHECK_DEVICE_EXCEPTION_SETTINGS(devices): 
   error_message_settings = []

   for device in devices:

      if device.exception_option != "None":

         if device.exception_setting == "None" or device.exception_setting == None:
            error_message_settings.append(device.name + " || No task selected")         

         # exception setting ip_address
         if device.exception_option == "IP-Address":

            # search for wrong chars
            for element in device.exception_value_1:
               if not element.isdigit() and element != "." and element != "," and element != " ":
                  error_message_settings.append(device.name + " || Invalid IP-Address")
                  break
               
         # exception setting sensor
         if device.exception_option != "IP-Address": 
            
            if device.exception_value_1 == "None" or device.exception_value_1 == None:
               error_message_settings.append(device.name + " || No Sensor selected")

            if device.exception_value_2 == "None" or device.exception_value_2 == None:
               error_message_settings.append(device.name + " || No Operator (<, >, =) selected")

            if device.exception_value_3 == "None" or device.exception_value_3 == None:
               error_message_settings.append(device.name + " || No check_value selected")
                  
   return error_message_settings


""" ###################### """
"""  check ighting groups  """
""" ###################### """

def CHECK_LIGHTING_GROUP_SETTINGS(settings):
   list_errors = []

   # check setting open light_slots in groups
   for element in settings:
      
      if element.light_ieeeAddr_1 == None or element.light_ieeeAddr_1 == "None":
          list_errors.append(element.name + " || Missing setting | Light 1")        
      if element.active_light_2 == "True" and (element.light_ieeeAddr_2 == None or element.light_ieeeAddr_2 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 2") 
      if element.active_light_3 == "True" and (element.light_ieeeAddr_3 == None or element.light_ieeeAddr_3 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 3") 
      if element.active_light_4 == "True" and (element.light_ieeeAddr_4 == None or element.light_ieeeAddr_4 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 4") 
      if element.active_light_5 == "True" and (element.light_ieeeAddr_5 == None or element.light_ieeeAddr_5 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 5") 
      if element.active_light_6 == "True" and (element.light_ieeeAddr_6 == None or element.light_ieeeAddr_6 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 6") 
      if element.active_light_7 == "True" and (element.light_ieeeAddr_7 == None or element.light_ieeeAddr_7 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 7") 
      if element.active_light_8 == "True" and (element.light_ieeeAddr_8 == None or element.light_ieeeAddr_8 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 8") 
      if element.active_light_9 == "True" and (element.light_ieeeAddr_9 == None or element.light_ieeeAddr_9 == "None"):
          list_errors.append(element.name + " || Missing setting | Light 9")   
          
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
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Missing setting | Seconds")
                  
            except:
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")


         # ########
         # lighting     
         # ########    
         

         # start scene
         elif "lighting" in line[1] and "start_scene" in line[1]:
            
            try:        
               line_content = line[1].split(" # ")

               # check scene setting
               if GET_LIGHTING_GROUP_BY_NAME(line_content[2]) == None: 
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Group not founded | " + line_content[2])
               
               if GET_LIGHTING_SCENE_BY_NAME(line_content[3]) == None: 
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Scene not founded | " + line_content[3])

               if not line_content[4].isdigit() or not (0 <= int(line_content[4]) <= 100):
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid brightness_value")

            except:
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")               
                     

         # turn_off
         elif "lighting" in line[1] and "turn_off" in line[1]:

            try:
               line_content = line[1].split(" # ")

               # check turn_off group setting
               if line_content[2].lower() == "group":

                  for group_name in line_content[3].split(","):
                     if GET_LIGHTING_GROUP_BY_NAME(group_name.strip()) == None: 
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Group not founded | " + group_name.strip())  

               # check turn_off all setting
               elif line_content[2].lower() == "all":
                  pass

               else:
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")                            

            except:
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")


         # ######
         # device
         # ######

         elif "device" in line[1]:

            try:
               line_content = line[1].split(" # ")

               # check device names
               for device_name in line_content[1].split(","):

                  if GET_DEVICE_BY_NAME(group_name.strip()) == None: 
                     list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Device not founded | " + device_name)       

                  # check commands
                  else:
                     
                     device  = GET_DEVICE_BY_NAME(device_name.strip())  
                     setting = task[2]

                     if setting.lower() not in device.commands_json.lower():
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid command | " + setting)


            except:
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")


         # ##################
         # request_sensordata
         # ##################
         
         elif "request_sensordata" in line[1]:

            try:        
               line_content = line[1].split(" # ")     

               if not GET_SENSORDATA_JOB_BY_NAME(line_content[1]):
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Job not founded")

            except:        
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")


         # #######
         # program
         # #######
         
         elif "program" in line[1]:

            try:        
               line_content = line[1].split(" # ")     

               if not GET_PROGRAM_BY_NAME(line_content[1].lower()):
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Program not founded")

               if line_content[2].strip() != "START" and line_content[2].strip() != "STOP":
                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " | Invalid command")

            except:        
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")


         # #####
         # music 
         # #####
         
         elif "music" in line[1]:
            
            try:        
               line_content = line[1].split(" # ")       
               
               if (line_content[1].strip() != "PLAY" and
                     line_content[1].strip() != "PREVIOUS" and
                     line_content[1].strip() != "NEXT" and
                     line_content[1].strip() != "STOP" and
                     line_content[1].strip() != "VOLUME" and
                     line_content[1].strip() != "playlist" and
                     line_content[1].strip() != "track" and
                     line_content[1].strip() != "album"):

                  list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid Command")

               # volume

               if line_content[1].strip() == "volume":
                  
                  try:
                     if not line_content[2].isdigit():
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")
                  
                     else:
                        if not 0 <= int(line_content[2]) <= 100:
                           list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value (0 - 100)")
                           
                  except:
                     list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

               # playlist
   
               if line_content[1].strip() == "playlist": 
                  
                  try:
                     device_name   = line_content[2]                                    
                     playlist_name = line_content[3]
                     
                     try:
                        if not line_content[4].isdigit():
                           list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")
                        
                        else:
                           if not 0 <= int(line_content[4]) <= 100:
                              list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value (0 - 100)")

                     except:
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

                  except:
                     list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

               # track
                     
               if line_content[1].strip() == "track": 
                  
                  try:
                     device_name  = line_content[2]                                    
                     track_title  = line_content[3]
                     track_artist = line_content[4]
                     
                     try:
                        if not line_content[5].isdigit():
                           list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

                        else:
                           if not 0 <= int(line_content[5]) <= 100:
                              list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value (0 - 100)")

                     except:
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

                  except:
                     list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

               # album

               if line_content[1].strip() == "album": 
                  
                  try:
                     device_name  = line_content[2]                                    
                     album_title  = line_content[3]
                     album_artist = line_content[4]
                     
                     try:
                        if not line_content[5].isdigit():
                           list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

                        else:
                           if not 0 <= int(line_content[5]) <= 100:
                              list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value (0 - 100)")

                     except:
                        list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

                  except:
                     list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid volume_value")

            except:
               list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")

      # ####
      # None
      # ####

         elif line[1] == "None":
            pass

         #  other

         elif line[1] != "":
            list_errors.append("Line " + str(line_number) + " - " + line[1] + " || Invalid formatting")
             
   return list_errors


""" ######################### """
"""  check scheduler settings """
""" ######################### """


def CHECK_SCHEDULER_TASKS_SETTINGS(scheduler_tasks): 
   list_errors = []  

   for task in scheduler_tasks:

      if task.trigger_time != "True" and task.trigger_sun_position != "True" and task.trigger_sensors != "True" and task.trigger_position != "True":    
         list_errors.append(task.name + " || No trigger selected")          


      if task.trigger_time == "True":

         ### check day

         try:
            if "," in task.day:
                  days = task.day.replace(" ", "")
                  days = days.split(",")
                  for element in days:
                     if element.lower() not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                        list_errors.append(task.name + " || Wrong time | Day")
                        break                                 
            else:
                  if task.day.lower() not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "*"] and task.day != "*":
                     list_errors.append(task.name + " || Wrong time | Day") 
         except:
            list_errors.append(task.name + " || Wrong time | Day")

         ### check hour
            
         try:
            if "," in task.hour:
                  hours = task.hour.replace(" ", "")                
                  hours = hours.split(",")
                  
                  for element in hours:
 
                     if len(element) == 1 and element != "*":
                        list_errors.append(task.name + " || Wrong time | Hour")
                        break
                    
                     try:
                        if not (0 <= int(element) <= 24):
                           list_errors.append(task.name + " || Wrong time | Hour")
                           break
                        
                     except:
                        list_errors.append(task.name + " || Wrong time | Hour")
                        break   
            else:
                  
               if len(task.hour) == 1 and task.hour != "*":
                  list_errors.append(task.name + " || Wrong time | Hour")
                  break
                
               try:
                  if not (0 <= int(task.hour) <= 24) and task.hour != "*":
                     list_errors.append(task.name + " || Wrong time | Hour") 
               except:
                  if task.hour != "*":
                     list_errors.append(task.name + " || Wrong time | Hour")    

         except:
            list_errors.append(task.name + " || Wrong time | Hour")

         ### check minute

         try:
            if "," in task.minute:
                  minutes = task.minute.replace(" ", "")                 
                  minutes = minutes.split(",")
                  
                  for element in minutes:
                      
                     if len(element) == 1 and element != "*":
                        list_errors.append(task.name + " || Wrong time | Minute")
                        break                      
                      
                     try:
                        if not (0 <= int(element) <= 60):
                           list_errors.append(task.name + " || Wrong time | Minute") 
                           break
                        
                     except:
                        list_errors.append(task.name + " || Wrong time | Minute") 
                        break   
            else:
                
               if len(task.minute) == 1 and task.minute != "*":
                  list_errors.append(task.name + " || Wrong time | Minute")
                  break
                
               try:
                  if not (0 <= int(task.minute) <= 60) and task.minute != "*":
                     list_errors.append(task.name + " || Wrong time | Minute") 
               except:
                  if task.minute != "*":
                     list_errors.append(task.name + " || Wrong time | Minute") 
      
         except:
            list_errors.append(task.name + " || Wrong time | Minute") 


      if task.trigger_sun_position == "True":

         # check coordinates 
         if task.option_sunrise == "True" or task.option_sunset == "True":
            if task.latitude == "None" or task.longitude == "None":
               list_errors.append(task.name + " || Coordinates not complete")
         else:
            list_errors.append(task.name + " || Missing setting | Sunrise or Sunset")


      if task.trigger_sensors == "True":

         # check mqtt devices
         if task.device_ieeeAddr_1 == "None" or task.device_ieeeAddr_1 == "" or task.device_ieeeAddr_1 == None:
            list_errors.append(task.name + " || Missing setting | Device 1") 

         if task.device_ieeeAddr_2 == "None" or task.device_ieeeAddr_2 == "" or task.device_ieeeAddr_2 == None:
            if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
               list_errors.append(task.name + " || Missing setting | Device 2") 
                  
         # check sensors
         if task.sensor_key_1 == "None" or task.sensor_key_1 == None:
            list_errors.append(task.name + " || Missing setting | Sensor 1") 
            
         if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
            if task.sensor_key_2 == "None" or task.sensor_key_2 == None:
               list_errors.append(task.name + " || Missing setting | Sensor 2")  
               
         # check operators
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":
            if task.operator_1 == "" or task.operator_1 == "None" or task.operator_1 == None: 
               list_errors.append(task.name + " || Missing setting | Operator 1")
         
         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.operator_2 == "None" or task.operator_2 == "" or task.operator_2 == None: 
               list_errors.append(task.name + " || Missing setting | Operator 2")  

         # check values
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":   
            if task.value_1 == "" or task.value_1 == "None" or task.value_1 == None: 
               list_errors.append(task.name + " || Missing setting | Value 1")   
                  
            elif (task.operator_1 == "<" or task.operator_1 == ">") and not task.value_1.isdigit():
               list_errors.append(task.name + 
               " || Invalid input | Value 1 | Only numbers can be used with the selected operator") 

         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.value_2 == "" or task.value_2 == "None" or task.value_2 == None:
               list_errors.append(task.name + " || Missing setting | Value 2")  
            elif (task.operator_2 == "<" or task.operator_2 == ">") and not task.value_2.isdigit():
               list_errors.append(task.name + 
               " || Invalid input | Value 2 | Only numbers can be used with the selected operator")                 
  
               
      if task.trigger_position == "True":

         # check setting choosed
         if task.option_home != "True" and task.option_away != "True":
            list_errors.append(task.name + " || Missing setting | Home or Away")

         # check setting home / away
         if task.option_home == "True" and task.option_away == "True":
            list_errors.append(task.name + " || Home or Away can be selected separately only")

         # check setting ip-addresses
         if task.option_home == "True" or task.option_away == "True":

            if task.ip_addresses != "None":
               
               # search for wrong chars
               for element in task.ip_addresses:
                  if not element.isdigit() and element != "." and element != "," and element != " ":
                     list_errors.append(task.name + " || Invalid IP-Addresses")
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

         if controller.command_10 != None and controller.command_10 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_10, name, task_type, controller.command_10)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_11 != None and controller.command_11 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_11, name, task_type, controller.command_11)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_12 != None and controller.command_12 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_12, name, task_type, controller.command_12)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_13 != None and controller.command_13 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_13, name, task_type, controller.command_13)
            
            if result != []: 
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_14 != None and controller.command_14 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_14, name, task_type, controller.command_14)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_15 != None and controller.command_15 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_15, name, task_type, controller.command_15)
            
            if result != []:   
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_16 != None and controller.command_16 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_16, name, task_type, controller.command_16)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_17 != None and controller.command_17 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_17, name, task_type, controller.command_17)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_18 != None and controller.command_18 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_18, name, task_type, controller.command_18)
            
            if result != []:
               for error in result:   
                  list_task_errors.append(error)         

         if controller.command_19 != None and controller.command_19 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_19, name, task_type, controller.command_19)
            
            if result != []: 
               for error in result:   
                  list_task_errors.append(error)                                             

         if controller.command_20 != None and controller.command_20 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_20, name, task_type, controller.command_20)
            
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
      
      if "lighting" in task and "start_scene" in task:
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 

            try:

               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 

                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Group not founded | " + task[2].strip())  
                  else:                               
                     list_task_errors.append(name + " || Group not founded | " + task[2].strip())  

            except:
               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Missing setting | Group")
               else:
                  list_task_errors.append(name + " || Missing setting | Group")

            # check scene setting    

            try:

               if GET_LIGHTING_SCENE_BY_NAME(task[3].strip()) == None: 

                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Scene not founded | " + task[3].strip())  
                  else:                               
                     list_task_errors.append(name + " || Scene not founded | " + task[3].strip())  
                  
            except:

               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Missing setting | Scene")
               else:               
                  list_task_errors.append(name + " || Missing setting | Scene")

            # check brightness    

            try:

               if task[4].isdigit():
                  if 1 <= int(task[4]) <= 100:
                     return list_task_errors

                  else:
                     if task_type == "controller":
                        list_task_errors.append(name + " || " + controller_command + " | Invalid brightness_value")
                     else:                        
                        list_task_errors.append(name + " || Invalid brightness_value") 
                     return list_task_errors    

               else:
                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Invalid brightness_value")
                  else:                     
                     list_task_errors.append(name + " || Invalid brightness_value")
                  return list_task_errors

            except:
               return list_task_errors

         else:
            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
            else:                
               list_task_errors.append(name + " || Invalid formatting")
            return list_task_errors
     

      # ############
      # rotate_scene
      # ############
      
      if "lighting" in task and "rotate_scene" in task and task_type == "controller":
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 
            try:

               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 
                  list_task_errors.append(name + " || " + controller_command + " | Group not founded | " + task[2].strip()) 
                  return list_task_errors 

               else:
                  return list_task_errors 

            except:
               list_task_errors.append(name + " || " + controller_command + " | Missing setting | Group")
               return list_task_errors


         else:
            list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
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
                  list_task_errors.append(name + " || " + controller_command + " | Group not founded | " + task[2])   
                                    
            except:
               list_task_errors.append(name + " || " + controller_command + " | Missing setting | Group")      

            # check brightness setting    
            try:
               if task[3].lower() == "turn_up" or task[3].lower() == "turn_down":
                  return list_task_errors
                  
               else:
                  list_task_errors.append(name + " || " + controller_command + " | TURN_UP or TURN_DOWN ?")
                  return list_task_errors
                  
            except:
               list_task_errors.append(name + " || " + controller_command + " | Missing setting | TURN_UP or TURN_DOWN")    
               return list_task_errors

         else:
            list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
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
                           list_task_errors.append(name + " || " + controller_command + " | Group not founded | " + group_name.strip())  
                        else:                               
                           list_task_errors.append(name + " || Group not founded | " + group_name.strip())  
                     
                  return list_task_errors

               except:

                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Missing setting | Group")
                  else:                            
                     list_task_errors.append(name + " || Missing setting | Group")
                  
                  return list_task_errors
                        
   
            # check turn off all lights
            elif task[2].lower() == "all": 
               return list_task_errors


            else:
               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Invalid Input | 'all' or 'group'")
               else:                   
                  list_task_errors.append(name + " || Invalid Input | 'all' or 'group' ?")
               return list_task_errors  


         else:
            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Invalid formatting") 
            else:                   
               list_task_errors.append(name + " || Invalid formatting")     
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
                        list_task_errors.append(name + " || " + controller_command + " | Device no founded | " + device_name)
                     else:
                        list_task_errors.append(name + " || Device no founded | " + device_name)           

                  # check commands
                  else:

                     device  = GET_DEVICE_BY_NAME(device_name.strip())  
                     setting = task[2]

                     if setting.lower() not in device.commands_json.lower():
                  
                        if task_type == "controller":
                           list_task_errors.append(name + " || " + controller_command + " | Invalid command | " + setting)
                        else:
                           list_task_errors.append(name + " || Invalid command | " + setting)
                             
               return list_task_errors                  
              
            except:
               
               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
               else:                
                  list_task_errors.append(name + " || Invalid formatting")       

               return list_task_errors

         else:
            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
            else:                
               list_task_errors.append(name + " || Invalid formatting")   

            return list_task_errors
            

      # #######
      # program
      # #######
      
      if "program" in task:
         if " # " in task:
            task = task.split(" # ") 

            try:
               program = GET_PROGRAM_BY_NAME(task[1].strip())
               setting = task[2].strip()
                  
               if program == None:
               
                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Program not founded | " + task[1])
                  else:
                     list_task_errors.append(name + " || " + task[1] + " Program not founded")                  
                  
               if setting != "START" and setting != "STOP":
                  
                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Invalid command | " + task[2])
                  else:
                     list_task_errors.append(name + " || Invalid command | " + task[2])
 
               return list_task_errors
      
      
            except:
               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
               else:
                  list_task_errors.append(name + " || Invalid formatting")
               return list_task_errors
         
         
         else:
            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
            else:                
               list_task_errors.append(name + " || Invalid formatting")
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


      # ###############
      # reset_log_files
      # ###############
      
      if task == "reset_log_files" and task_type == "scheduler":
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
                     list_task_errors.append(name + " || " + controller_command + " | Job not founded | " + task[1])
                  else:
                     list_task_errors.append(name + " || Job not founded | " + task[1])

                  return list_task_errors   

            except:

                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Missing setting | Job")
                  else:
                     list_task_errors.append(name + " || Missing setting | Job") 

                  return list_task_errors

         else:

            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Missing setting | Job")
            else:
               list_task_errors.append(name + " || Missing setting | Job") 

            return list_task_errors


      # #####
      # music     
      # #####
        
      if "music" in task:
         if " # " in task:
            task = task.split(" # ")

            # check settings
            try:   
                   
               if task[1].strip() == "PLAY":
                  return list_task_errors

               elif task[1].strip() == "PLAY/STOP":
                  return list_task_errors

               elif task[1].strip() == "PREVIOUS":
                  return list_task_errors
             
               elif task[1].strip() == "NEXT":
                  return list_task_errors   
                  
               elif task[1].strip() == "STOP":
                  return list_task_errors
             
               elif task[1].strip() == "VOLUME_UP":
                  return list_task_errors                     
                                 
               elif task[1].strip() == "VOLUME_DOWN":
                  return list_task_errors
             
               elif task[1].strip() == "VOLUME":             
             
                  try:
                     if not task[2].isdigit():
                        list_task_errors.append(name + " || " + task[2] + " | Invalid volume_value") 
                     else:
                        if not 0 <= int(task[2]) <= 100:
                           list_task_errors.append(name + " || " + task[2] + " | Invalid volume_value")
                           
                     return list_task_errors
                           
                  except:
                     list_task_errors.append(name + " || " + task[2] + " | Invalid volume_value") 
                     return list_task_errors
                  
               elif task[1].strip() == "playlist": 

                  try:
                     if not task[4].isdigit():
                        list_task_errors.append(name + " || " + task[4] + " | Invalid volume_value") 
                     else:
                        if not 0 <= int(task[4]) <= 100:
                           list_task_errors.append(name + " || " + task[4] + " | Invalid volume_value")
                           
                     return list_task_errors
                              
                  except:
                     list_task_errors.append(name + " || " + task[4] + " | Invalid volume_value") 
                     return list_task_errors
   
                     
               elif task[1].lower() == "track": 
                  
                  try:
                     device_name  = task[2]                                    
                     track_title  = task[3]
                     track_artist = task[4]
                     
                     try:
                        if not task[5].isdigit():
                           list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value")
                              
                        return list_task_errors
                                 
                     except:
                        list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value") 
                        return list_task_errors
                        
                  except:
                     list_task_errors.append(name + " || " + str(task) + " | Invalid volume_value") 
                     return list_task_errors  

               elif task[1].lower() == "album": 
                  
                  try:
                     device_name  = task[2]                                    
                     album_title  = task[3]
                     album_artist = task[4]
                     
                     try:
                        if not task[5].isdigit():
                           list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value")
                        
                        return list_task_errors
                                 
                     except:
                        list_task_errors.append(name + " || " + task[5] + " | Invalid volume_value") 
                        return list_task_errors
                        
                  except:
                     list_task_errors.append(name + " || " + str(task) + " | Invalid volume_value") 
                     return list_task_errors                   

               else:
                  if task_type == "controller":
                     list_task_errors.append(name + " || " + controller_command + " | Invalid command | " + task[1])
                  else:
                     list_task_errors.append(name + " || " + task[1] + " | Invalid command")
                  return list_task_errors


            except:
               if task_type == "controller":
                  list_task_errors.append(name + " || " + controller_command + " | Missing setting | Command") 
               else:
                  list_task_errors.append(name + " || Missing setting | Command") 
               return list_task_errors

                               
         else:
            if task_type == "controller":
               list_task_errors.append(name + " || " + controller_command + " | Invalid formatting")
            else:
               list_task_errors.append(name + " || Invalid formatting")   
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
         list_task_errors.append(name + " || " + controller_command + " | Invalid task") 
      else:
         list_task_errors.append(name + " || Invalid task")
         
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
         list_task_errors.append(name + " || " + controller_command + " | Invalid task")   
         return list_task_errors

      else:
         list_task_errors.append(name + " || Invalid task")        
         return list_task_errors
