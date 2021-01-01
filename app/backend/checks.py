from app                         import app
from app.backend.database_models import *

from croniter import croniter

import re

""" ################### """
"""  device exceptions  """
""" ################### """

def CHECK_DEVICE_EXCEPTION_SETTINGS(device_exceptions): 
   error_message_settings = []

   for exception in device_exceptions:

      device = GET_DEVICE_BY_IEEEADDR(exception.device_ieeeAddr)

      # exception command
      if exception.exception_command == "None":
         error_message_settings.append(device.name + " || No Command selected")

      # exception setting 
      if exception.exception_option == "None":
         error_message_settings.append(device.name + " || No Option selected")

      # exception setting ip_address
      elif exception.exception_option == "IP-Address":

         # search for wrong chars
         for element in exception.exception_value_1:
            if not element.isdigit() and element != "." and element != "," and element != " ":
               error_message_settings.append(device.name + " || Invalid IP-Address")
               break
            
      # exception setting sensor
      else: 
         
         if exception.exception_value_1 == "None" or exception.exception_value_1 == None:
            error_message_settings.append(device.name + " || No Sensor selected")

         if exception.exception_value_2 == "None" or exception.exception_value_2 == None:
            error_message_settings.append(device.name + " || No Operator selected >>> Options || < || > || =")

         if exception.exception_value_3 == "None" or exception.exception_value_3 == None:
            error_message_settings.append(device.name + " || No check_value selected")
                  
   return error_message_settings


""" ####################### """
"""  check lighting groups  """
""" ####################### """

def CHECK_LIGHTING_GROUP_SETTINGS(lighting_groups):
   list_errors = []

   # check setting open light_slots in groups
   for group in lighting_groups:
      
      if group.light_ieeeAddr_1 == None or group.light_ieeeAddr_1 == "None":
          list_errors.append("Missing setting || Light 1")        
      if group.active_light_2 == "True" and (group.light_ieeeAddr_2 == None or group.light_ieeeAddr_2 == "None"):
          list_errors.append("Missing setting || Light 2") 
      if group.active_light_3 == "True" and (group.light_ieeeAddr_3 == None or group.light_ieeeAddr_3 == "None"):
          list_errors.append("Missing setting || Light 3") 
      if group.active_light_4 == "True" and (group.light_ieeeAddr_4 == None or group.light_ieeeAddr_4 == "None"):
          list_errors.append("Missing setting || Light 4") 
      if group.active_light_5 == "True" and (group.light_ieeeAddr_5 == None or group.light_ieeeAddr_5 == "None"):
          list_errors.append("Missing setting || Light 5") 
      if group.active_light_6 == "True" and (group.light_ieeeAddr_6 == None or group.light_ieeeAddr_6 == "None"):
          list_errors.append("Missing setting || Light 6") 
      if group.active_light_7 == "True" and (group.light_ieeeAddr_7 == None or group.light_ieeeAddr_7 == "None"):
          list_errors.append("Missing setting || Light 7") 
      if group.active_light_8 == "True" and (group.light_ieeeAddr_8 == None or group.light_ieeeAddr_8 == "None"):
          list_errors.append("Missing setting || Light 8") 
      if group.active_light_9 == "True" and (group.light_ieeeAddr_9 == None or group.light_ieeeAddr_9 == "None"):
          list_errors.append("Missing setting || Light 9")   
               
      if list_errors != []:
         list_group_errors = ""
         
         for error in list_errors:   
            list_group_errors = list_group_errors + "," + error      

         SET_LIGHTING_GROUP_ERRORS(group.id, list_group_errors[1:]) 

      else:
         SET_LIGHTING_GROUP_ERRORS(group.id, "") 

      # reset errors
      list_errors = []      


""" ############################## """
"""  check scheduler job settings  """
""" ############################## """

def CHECK_SCHEDULER_JOB_SETTINGS(scheduler_jobs): 
   list_errors = []  

   for task in scheduler_jobs:

      if task.trigger_timedate != "True" and task.trigger_sun_position != "True" and task.trigger_sensors != "True" and task.trigger_position != "True":    
         list_errors.append("No trigger selected")          


      if task.trigger_timedate == "True":

         ### check timedate
         try:
            if croniter.is_valid(task.timedate) is False:
               list_errors.append("Invalid TimeDate")

         except Exception as e:
            list_errors.append("Invalid TimeDate")


      if task.trigger_sun_position == "True":

         # check setting sunrise / sunset / day / night
         if task.option_sunrise != "True" and task.option_sunset != "True" and task.option_day != "True" and task.option_night != "True":
            list_errors.append("Missing setting || Sunrise / Sunset / Day / Night")

         # check setting sunrise / sunset / day / night
         if (task.option_sunrise == "True" or task.option_sunset == "True") and (task.option_day == "True" or task.option_night == "True"):
            list_errors.append("Wrong Settings || Sunrise / Sunset or Day / Night")

         # check coordinates
         if task.latitude == "None":
            list_errors.append("No latitude coordinates found")
         else:
            try:
               if type(float(task.latitude)) is not float:
                  list_errors.append("Invalid latitude coordinates")
               if not -90.0 <= float(task.latitude) <= 90.0:
                  list_errors.append("Invalid latitude coordinates")
            except:
               list_errors.append("Invalid latitude coordinates")

         if task.longitude == "None":
            list_errors.append("No longitude coordinates found")
         else:
            try:
               if type(float(task.longitude)) is not float:
                  list_errors.append("Invalid longitude coordinates")
               if not -180.0 <= float(task.longitude) <= 180.0:
                  list_errors.append("Invalid longitude coordinates")                  
            except:
               list_errors.append("Invalid longitude coordinates")
         

      if task.trigger_sensors == "True":

         # check mqtt devices
         if task.device_ieeeAddr_1 == "None" or task.device_ieeeAddr_1 == "" or task.device_ieeeAddr_1 == None:
            list_errors.append("Missing setting || Device 1") 

         if task.device_ieeeAddr_2 == "None" or task.device_ieeeAddr_2 == "" or task.device_ieeeAddr_2 == None:
            if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
               list_errors.append("Missing setting || Device 2") 
                  
         # check sensors
         if task.sensor_key_1 == "None" or task.sensor_key_1 == None:
            list_errors.append("Missing setting || Sensor 1") 
            
         if task.main_operator_second_sensor != "None" and task.main_operator_second_sensor != None:
            if task.sensor_key_2 == "None" or task.sensor_key_2 == None:
               list_errors.append("Missing setting || Sensor 2")  
               
         # check operators
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":
            if task.operator_1 == "" or task.operator_1 == "None" or task.operator_1 == None: 
               list_errors.append("Missing setting || Operator 1")
         
         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.operator_2 == "None" or task.operator_2 == "" or task.operator_2 == None: 
               list_errors.append("Missing setting || Operator 2")  

         # check values
         if task.main_operator_second_sensor != "<" and task.main_operator_second_sensor != ">" and task.main_operator_second_sensor != "=":   
            if task.value_1 == "" or task.value_1 == "None" or task.value_1 == None: 
               list_errors.append("Missing setting || Value 1")   
                  
            elif (task.operator_1 == "<" or task.operator_1 == ">") and not task.value_1.isdigit():
               list_errors.append(task.name + 
               " || Invalid input | Value 1 | Only numbers can be used with the selected operator") 

         if task.main_operator_second_sensor == "and" or task.main_operator_second_sensor == "or":
            if task.value_2 == "" or task.value_2 == "None" or task.value_2 == None:
               list_errors.append("Missing setting | Value 2")  
            elif (task.operator_2 == "<" or task.operator_2 == ">") and not task.value_2.isdigit():
               list_errors.append(task.name + 
               " || Invalid input | Value 2 | Only numbers can be used with the selected operator")                 
  
               
      if task.trigger_position == "True":

         # check setting choosed
         if task.option_home != "True" and task.option_away != "True":
            list_errors.append("Missing setting || Home or Away")

         # check setting home / away
         if task.option_home == "True" and task.option_away == "True":
            list_errors.append("Home or Away can be selected separately only")

         # check setting ip-addresses
         if task.option_home == "True" or task.option_away == "True":

            if task.ip_addresses != "None":
               
               # search for wrong chars
               for element in task.ip_addresses:
                  if not element.isdigit() and element != "." and element != "," and element != " ":
                     list_errors.append("Invalid IP-Addresses")
                     break

      if list_errors != []:
         list_task_setting_errors = ""

         for error in list_errors:   
            list_task_setting_errors = list_task_setting_errors + "," + error      

         SET_SCHEDULER_JOB_SETTING_ERRORS(task.id, list_task_setting_errors[1:]) 

      else:
         SET_SCHEDULER_JOB_SETTING_ERRORS(task.id, "") 

      # reset errors
      list_errors = []


""" ################### """
"""     check tasks     """
""" ################### """

def CHECK_TASKS(check_object, task_trigger):

   list_task_errors = ""


   # ##########
   # controller
   # ##########
   
   if task_trigger == "controller": 

      for controller in check_object:

         if controller.command_1 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_1, task_trigger, controller.command_1[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error
               
         if controller.command_2 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_2, task_trigger, controller.command_2[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error       
                         
         if controller.command_3 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_3, task_trigger, controller.command_3[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error               
               
         if controller.command_4 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_4, task_trigger, controller.command_4[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error     
               
         if controller.command_5 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_5, task_trigger, controller.command_5[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error                   
               
         if controller.command_6 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_6, task_trigger, controller.command_6[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error     
               
         if controller.command_7 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_7, task_trigger, controller.command_7[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error                  
               
         if controller.command_8 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_8, task_trigger, controller.command_8[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error                  
                                             
         if controller.command_9 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_9, task_trigger, controller.command_9[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error          

         if controller.command_10 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_10, task_trigger, controller.command_10[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error        

         if controller.command_11 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_11, task_trigger, controller.command_11[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error      

         if controller.command_12 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_12, task_trigger, controller.command_12[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error        

         if controller.command_13 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_13, task_trigger, controller.command_13[1:-1].replace('"',''))
            
            if result != []: 
               for error in result:   
                  list_task_errors = list_task_errors + "," + error         

         if controller.command_14 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_14, task_trigger, controller.command_14[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error       

         if controller.command_15 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_15, task_trigger, controller.command_15[1:-1].replace('"',''))
            
            if result != []:   
               for error in result:   
                  list_task_errors = list_task_errors + "," + error        

         if controller.command_16 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_16, task_trigger, controller.command_16[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error       

         if controller.command_17 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_17, task_trigger, controller.command_17[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error      

         if controller.command_18 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_18, task_trigger, controller.command_18[1:-1].replace('"',''))
            
            if result != []:
               for error in result:   
                  list_task_errors = list_task_errors + "," + error        

         if controller.command_19 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_19, task_trigger, controller.command_19[1:-1].replace('"',''))
            
            if result != []: 
               for error in result:   
                  list_task_errors = list_task_errors + "," + error                                           

         if controller.command_20 != "None": 
            result = CHECK_TASK_OPERATION(controller.task_20, task_trigger, controller.command_20[1:-1].replace('"',''))
            
            if result != []:    
               for error in result:   
                  list_task_errors = list_task_errors + "," + error
        
         SET_CONTROLLER_TASK_ERRORS(controller.id, list_task_errors[1:]) 

         # reset errors
         list_task_errors = ""


   # #######
   # program
   # #######

   if task_trigger == "program":

      list_lines = [[GET_PROGRAM_BY_ID(check_object).line_active_1,  GET_PROGRAM_BY_ID(check_object).line_content_1],
                    [GET_PROGRAM_BY_ID(check_object).line_active_2,  GET_PROGRAM_BY_ID(check_object).line_content_2],
                    [GET_PROGRAM_BY_ID(check_object).line_active_3,  GET_PROGRAM_BY_ID(check_object).line_content_3],
                    [GET_PROGRAM_BY_ID(check_object).line_active_4,  GET_PROGRAM_BY_ID(check_object).line_content_4],
                    [GET_PROGRAM_BY_ID(check_object).line_active_5,  GET_PROGRAM_BY_ID(check_object).line_content_5],
                    [GET_PROGRAM_BY_ID(check_object).line_active_6,  GET_PROGRAM_BY_ID(check_object).line_content_6],                 
                    [GET_PROGRAM_BY_ID(check_object).line_active_7,  GET_PROGRAM_BY_ID(check_object).line_content_7],                 
                    [GET_PROGRAM_BY_ID(check_object).line_active_8,  GET_PROGRAM_BY_ID(check_object).line_content_8],                 
                    [GET_PROGRAM_BY_ID(check_object).line_active_9,  GET_PROGRAM_BY_ID(check_object).line_content_9],                 
                    [GET_PROGRAM_BY_ID(check_object).line_active_10, GET_PROGRAM_BY_ID(check_object).line_content_10],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_11, GET_PROGRAM_BY_ID(check_object).line_content_11],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_12, GET_PROGRAM_BY_ID(check_object).line_content_12],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_13, GET_PROGRAM_BY_ID(check_object).line_content_13],
                    [GET_PROGRAM_BY_ID(check_object).line_active_14, GET_PROGRAM_BY_ID(check_object).line_content_14],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_15, GET_PROGRAM_BY_ID(check_object).line_content_15],
                    [GET_PROGRAM_BY_ID(check_object).line_active_16, GET_PROGRAM_BY_ID(check_object).line_content_16],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_17, GET_PROGRAM_BY_ID(check_object).line_content_17],
                    [GET_PROGRAM_BY_ID(check_object).line_active_18, GET_PROGRAM_BY_ID(check_object).line_content_18],   
                    [GET_PROGRAM_BY_ID(check_object).line_active_19, GET_PROGRAM_BY_ID(check_object).line_content_19],            
                    [GET_PROGRAM_BY_ID(check_object).line_active_20, GET_PROGRAM_BY_ID(check_object).line_content_20],                  
                    [GET_PROGRAM_BY_ID(check_object).line_active_21, GET_PROGRAM_BY_ID(check_object).line_content_21],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_22, GET_PROGRAM_BY_ID(check_object).line_content_22],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_23, GET_PROGRAM_BY_ID(check_object).line_content_23],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_24, GET_PROGRAM_BY_ID(check_object).line_content_24],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_25, GET_PROGRAM_BY_ID(check_object).line_content_25],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_26, GET_PROGRAM_BY_ID(check_object).line_content_26],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_27, GET_PROGRAM_BY_ID(check_object).line_content_27],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_28, GET_PROGRAM_BY_ID(check_object).line_content_28], 
                    [GET_PROGRAM_BY_ID(check_object).line_active_29, GET_PROGRAM_BY_ID(check_object).line_content_29],  
                    [GET_PROGRAM_BY_ID(check_object).line_active_30, GET_PROGRAM_BY_ID(check_object).line_content_30]] 

      line_number = 0

      for line in list_lines:           
         line_number = line_number + 1

         # line active ?
         if line[0] == "True":
            result = CHECK_TASK_OPERATION(line[1], task_trigger, "Line " + str(line_number))
            
            if result != []:         

               for error in result:   
                  list_task_errors = list_task_errors + "," + error   

      return list_task_errors[1:]


   # #########
   # scheduler
   # #########

   if task_trigger == "scheduler":

      for scheduler_job in check_object:
         result = CHECK_TASK_OPERATION(scheduler_job.task, task_trigger, "")
         
         if result != []:
            
            for error in result:   
               list_task_errors = list_task_errors + "," + error      

         SET_SCHEDULER_JOB_ERRORS(scheduler_job.id, list_task_errors[1:]) 

         # reset errors
         list_task_errors = ""


""" ###################### """
"""  check task operation  """
""" ###################### """

def CHECK_TASK_OPERATION(task, task_trigger, details): 
   list_task_errors = []

   try:
      
      # #####
      # break
      # #####
            
      if "break" in task and task_trigger == "program":     
               
         try: 
            task = task.split(" # ")
   
            # check delay value            
            if not task[1].isdigit():
               list_task_errors.append(details + " || Invalid setting | Seconds")
            
         except:
            list_task_errors.append(details + " || Invalid formatting")

         return list_task_errors


      # ###########
      # start_scene
      # ###########
      
      if "lighting" in task and "start_scene" in task and "turn_off" not in task:
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 

            try:
               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 

                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Group not found | " + task[2].strip())  
                  else:                            
                     list_task_errors.append("Group not found || " + task[2].strip())  

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Group")
               else:
                  list_task_errors.append("Missing setting || Group")

            # check scene setting    

            try:
               if GET_LIGHTING_SCENE_BY_NAME(task[3].strip()) == None: 

                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Scene not found | " + task[3].strip())  
                  else:                               
                     list_task_errors.append("Scene not found || " + task[3].strip())  
                  
            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Scene")
               else:               
                  list_task_errors.append("Missing setting || Scene")

            # check brightness    

            try:
               if task[4].isdigit():
                  if not 1 <= int(task[4]) <= 100:

                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid brightness_value")
                     else:                        
                        list_task_errors.append("Invalid brightness_value") 
   
               else:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid brightness_value")
                  else:                     
                     list_task_errors.append("Invalid brightness_value")

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid brightness_value")
               else:                     
                  list_task_errors.append("Invalid brightness_value")

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:                
               list_task_errors.append("Invalid formatting")
            
         return list_task_errors
     

      # ####################
      # start_scene/turn_off
      # ####################
      
      if "lighting" in task and "start_scene" in task and "turn_off" in task and task_trigger == "controller":
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 

            try:
               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 
                  list_task_errors.append(details + " || Group not found | " + task[2].strip())  

            except:
               list_task_errors.append(details + " || Missing setting | Group")

            # check scene setting    

            try:
               if GET_LIGHTING_SCENE_BY_NAME(task[3].strip()) == None: 
                  list_task_errors.append(details + " || Scene not found | " + task[3].strip())  
                  
            except:
               list_task_errors.append(details + " || Missing setting | Scene")


            # check brightness    

            try:
               if task[4].isdigit():
                  if not 1 <= int(task[4]) <= 100:
                     list_task_errors.append(details + " || Invalid brightness_value")

               else:
                  list_task_errors.append(details + " || Invalid brightness_value")

            except:
               list_task_errors.append(details + " || Invalid brightness_value")
               
         else:
            list_task_errors.append(details + " || Invalid formatting")
         
         return list_task_errors
  

      # ############
      # rotate_scene
      # ############
      
      if "lighting" in task and "rotate_scene" in task and task_trigger == "controller":
         if " # " in task:
            task = task.split(" # ") 

            # check group setting 

            try:
               if GET_LIGHTING_GROUP_BY_NAME(task[2].strip()) == None: 
                  list_task_errors.append(details + " || Group not found | " + task[2].strip()) 

            except:
               list_task_errors.append(details + " || Missing setting | Group")
            
         else:
            list_task_errors.append(details + " || Invalid formatting")
         
         return list_task_errors    


      # #################
      # brightness dimmer
      # #################
      
      if "lighting" in task and "brightness" in task:
         if " # " in task:
            task = task.split(" # ") 

            # check group setting

            try:
               if GET_LIGHTING_GROUP_BY_NAME(task[2]):
                  pass
                  
               else:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Group not found | " + task[2])   
                  else:                               
                     list_task_errors.append("Group not found || " + task[2])                    
                                    
            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Group")      
               else:                               
                  list_task_errors.append("Missing setting || Group")                      

            # check brightness setting    

            try:
               if task[3].lower() != "turn_up" and task[3].lower() != "turn_down":
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid setting >>> Options || TURN_UP || TURN_DOWN")
                  else:                               
                     list_task_errors.append("Invalid setting | TURN_UP or TURN_DOWN ?")

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting >>> Options || TURN_UP || TURN_DOWN")   
               else:                               
                  list_task_errors.append("Missing setting >>> Options || TURN_UP || TURN_DOWN")     

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:                               
               list_task_errors.append("Invalid formatting")   

         return list_task_errors


      # #########
      # set_light
      # #########

      if "lighting" in task and "light" in task and "start_scene" not in task and "turn_off" not in task:
         
         if " # " in task:
            task = task.split(" # ") 

            # check light setting 

            try:
               if GET_DEVICE_BY_NAME(task[2].strip()) == None: 

                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Light not found | " + task[2].strip())  
                  else:                               
                     list_task_errors.append("Light not found || " + task[2].strip())  

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Light")
               else:
                  list_task_errors.append("Missing setting || Light")

            # check rgb_values setting 

            try:
               rgb_values = re.findall(r'\d+', task[3])

               if not rgb_values[0].isdigit() or not (0 <= int(rgb_values[0]) <= 255): 
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid rgb_values")
                  else:                               
                     list_task_errors.append("Invalid rgb_values || " + task[3].strip())  

               if not rgb_values[1].isdigit() or not (0 <= int(rgb_values[1]) <= 255): 
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid rgb_values")
                  else:                               
                     list_task_errors.append("Invalid rgb_values || " + task[3].strip())  

               if not rgb_values[2].isdigit() or not (0 <= int(rgb_values[2]) <= 255): 
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid rgb_values")
                  else:                               
                     list_task_errors.append("Invalid rgb_values || " + task[3].strip())                       

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid rgb_values")
               else:                               
                  list_task_errors.append("Invalid rgb_values || " + task[3].strip())     

            # check brightness    

            try:

               if task[4].isdigit():
                  if not 1 <= int(task[4]) <= 255:
                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid brightness_value")
                     else:                        
                        list_task_errors.append("Invalid brightness_value || " + task[4].strip())    

               else:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid brightness_value")
                  else:                     
                     list_task_errors.append("Invalid brightness_value || " + task[4].strip())    

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid brightness_value")
               else:                     
                  list_task_errors.append("Invalid brightness_value || " + task[4].strip())    

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:                
               list_task_errors.append("Invalid formatting")
        
         return list_task_errors


      # ########
      # turn_off
      # ########
      
      if "lighting" in task and "turn_off" in task:

         if " # " in task:
            task = task.split(" # ")
            
            # check turn_off groups

            if task[2].lower() == "group": 

               try:      
                  # check group names 
                  for group_name in task[3].split(","):
                     if GET_LIGHTING_GROUP_BY_NAME(group_name.strip()) == None: 

                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Group not found | " + group_name.strip())  
                        else:                               
                           list_task_errors.append("Group not found || " + group_name.strip())  
                     
               except:

                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Missing setting | Group")
                  else:                            
                     list_task_errors.append("Missing setting || Group")
                  
            # check turn_off light setting

            elif task[2].lower() == "light": 

               try:
                  # check light name
                  if GET_DEVICE_BY_NAME(task[3].strip()) == None: 

                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Light not found | " + task[3].strip())  
                     else:                               
                        list_task_errors.append("Light not found || " + task[3].strip())  

               except:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Missing setting | Light")
                  else:                            
                     list_task_errors.append("Missing setting || Light")
                  
            # check turn off all lights

            elif task[2].lower() == "all": 
               pass

            else:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid Input >>> Options || all || group || light")
               else:                   
                  list_task_errors.append("Invalid Input >>> Options || all || group || light")

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting") 
            else:                   
               list_task_errors.append("Invalid formatting")     
      
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

                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Device no found | " + device_name)
                     else:
                        list_task_errors.append("Device no found || " + device_name)           

                  # check commands
                  else:
                     device  = GET_DEVICE_BY_NAME(device_name.strip())  
                     setting = task[2]

                     if setting.lower() not in device.commands.lower():
                  
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid command | " + setting)
                        else:
                           list_task_errors.append("Invalid command || " + setting)
                             
            except:       
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid formatting")
               else:                
                  list_task_errors.append("Invalid formatting")       

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:                
               list_task_errors.append("Invalid formatting")   

         return list_task_errors
            

      # #######
      # program
      # #######

      if "program" in task:
         if " # " in task:
            task = task.split(" # ") 

            try:
               if GET_PROGRAM_BY_NAME(task[1].strip()) == None:        
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Program not found | " + task[1])
                  else:
                     list_task_errors.append("Program not found || " + task[1])                  
                  
               if task[2].strip() != "START" and task[2].strip() != "STOP":
                  
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid command | " + task[2])
                  else:
                     list_task_errors.append("Invalid command || " + task[2])

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Invalid formatting")
               else:
                  list_task_errors.append("Invalid formatting")

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:                
               list_task_errors.append("Invalid formatting")
      
         return list_task_errors
         

      # ###############
      # backup_database  
      # ###############  
       
      if task == "backup_database" and task_trigger == "scheduler":
         return list_task_errors


      # #############
      # backup_zigbee 
      # #############  
       
      if task == "backup_zigbee" and task_trigger == "scheduler":
         return list_task_errors


      # ##############
      # update_devices
      # ##############
   
      if task == "update_devices" and task_trigger == "scheduler":
         return list_task_errors


      # ####################
      # check_mqtt_connetion
      # ####################
      
      if task == "check_mqtt_connetion" and task_trigger == "scheduler":
         return list_task_errors


      # ###############
      # reset_log_files
      # ###############
      
      if task == "reset_log_files" and task_trigger == "scheduler":
         return list_task_errors


      # ############
      # reset_system
      # ############
      
      if task == "reset_system" and task_trigger == "scheduler":
         return list_task_errors


      # ###############
      # shutdown_system
      # ###############
      
      if task == "shutdown_system" and task_trigger == "scheduler":
         return list_task_errors


      # ##################
      # request_sensordata
      # ##################
        
      if "request_sensordata" in task:
         if " # " in task:
            task = task.split(" # ")

            # check job name setting
            try:     
               if GET_SENSORDATA_JOB_BY_NAME(task[1]) == None:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Job not found | " + task[1])
                  else:
                     list_task_errors.append("Job not found || " + task[1])

            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Job")
               else:
                  list_task_errors.append("Missing setting || Job") 

         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Missing setting | Job")
            else:
               list_task_errors.append("Missing setting || Job") 

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
                  pass
           
               elif task[1].strip() == "PLAY/STOP" and task_trigger == "controller":
                  pass

               elif task[1].strip() == "ROTATE_PLAYLIST" and task_trigger == "controller":
                  pass

               elif task[1].strip() == "PREVIOUS":
                  pass
             
               elif task[1].strip() == "NEXT":
                  pass 
                  
               elif task[1].strip() == "STOP":
                  pass
             
               elif task[1].strip() == "VOLUME_UP":
                  pass                 
                                 
               elif task[1].strip() == "VOLUME_DOWN":
                  pass
             
               elif task[1].strip() == "VOLUME":             
             
                  try:
                     if not task[2].isdigit():
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid volume_value | " + task[2])
                        else:                        
                           list_task_errors.append(task[2] + " || Invalid volume_value") 
                     else:
                        if not 0 <= int(task[2]) <= 100:
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid volume_value | " + task[2])
                           else:                           
                              list_task_errors.append(task[2] + " || Invalid volume_value")
  
                  except:
                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid volume_value | " + task[2])
                     else:                     
                        list_task_errors.append(task[2] + " || Invalid volume_value") 

               # playlist

               elif task[1].strip() == "playlist": 

                  try:
                     device_name = task[2].strip()                                    

                     if device_name.lower() != "multiroom":
                        if GET_DEVICE_BY_NAME(device_name) == None: 
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Device not found | " + device_name)
                           else:                           
                              list_task_errors.append(device_name + " || Device not found")      

                     try:
                        if not task[4].isdigit():
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid volume_value | " + task[4])
                           else:                           
                              list_task_errors.append(task[4] + " || Invalid volume_value") 
                        else:
                           if not 0 <= int(task[4]) <= 100:
                              if task_trigger == "controller" or task_trigger == "program":
                                 list_task_errors.append(details + " || Invalid volume_value | " + task[4])
                              else:                              
                                 list_task_errors.append(task[4] + " || Invalid volume_value")
                                 
                     except:
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid volume_value | " + task[4])
                        else:                        
                           list_task_errors.append(task[4] + " || Invalid volume_value") 

                     try:

                        if str(task[5]) != "True" and str(task[5]) != "False":
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid shuffle setting | " + task[5])
                           else:                        
                              list_task_errors.append(task[5] + " || Invalid shuffle setting") 

                     except:
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid shuffle setting | " + task[5])
                        else:                        
                           list_task_errors.append(task[5] + " || Invalid shuffle setting") 

                  except:
                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid formatting") 
                     else:                     
                        list_task_errors.append(str(task) + " || Invalid formatting") 

               # track

               elif task[1].lower() == "track": 
                  
                  try:
                     device_name = task[2].strip()                                    

                     if device_name.lower() != "multiroom":
                        if GET_DEVICE_BY_NAME(device_name) == None: 
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Device not found | " + device_name)
                           else:                           
                              list_task_errors.append(device_name + " || Device not found")           

                     try:
                        if not task[5].isdigit():
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                           else:                           
                              list_task_errors.append(task[5] + " || Invalid volume_value") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              if task_trigger == "controller" or task_trigger == "program":
                                 list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                              else:                              
                                 list_task_errors.append(task[5] + " || Invalid volume_value")
     
                     except:
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                        else:                        
                           list_task_errors.append(task[5] + " || Invalid volume_value") 
                        
                  except:
                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid formatting")
                     else:                     
                        list_task_errors.append(str(task) + " || Invalid formatting") 
                  
               # album

               elif task[1].lower() == "album": 
                  
                  try:
                     device_name = task[2].strip()                                    

                     if device_name.lower() != "multiroom":
                        if GET_DEVICE_BY_NAME(device_name) == None: 
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Device not found | " + device_name)
                           else:                           
                              list_task_errors.append(device_name + " || Device not found")                  

                     try:
                        if not task[5].isdigit():
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                           else:                           
                              list_task_errors.append(task[5] + " || Invalid volume_value") 
                        else:
                           if not 0 <= int(task[5]) <= 100:
                              if task_trigger == "controller" or task_trigger == "program":
                                 list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                              else:                              
                                 list_task_errors.append(task[5] + " || Invalid volume_value")
                           
                     except:
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid volume_value | " + task[5])
                        else:                        
                           list_task_errors.append(task[5] + " || Invalid volume_value") 

                     try:
                        if str(task[6]) != "True" and str(task[6]) != "False":
                           if task_trigger == "controller" or task_trigger == "program":
                              list_task_errors.append(details + " || Invalid shuffle setting | " + task[6])
                           else:                        
                              list_task_errors.append(task[6] + " || Invalid shuffle setting") 
                     
                     except:
                        if task_trigger == "controller" or task_trigger == "program":
                           list_task_errors.append(details + " || Invalid shuffle setting | " + task[6])
                        else:                        
                           list_task_errors.append(task[6] + " || Invalid shuffle setting") 

                  except:
                     if task_trigger == "controller" or task_trigger == "program":
                        list_task_errors.append(details + " || Invalid formatting")
                     else:                     
                        list_task_errors.append(str(task) + " || Invalid formatting") 

               # interface

               elif task[1].lower() == "interface" and task_trigger == "program": 
                  
                  try:
                     device_name = task[2].strip()                                    

                     if device_name.lower() != "multiroom":
                        if GET_DEVICE_BY_NAME(device_name) == None: 
                           list_task_errors.append(details + " || Device not found | " + device_name)       

                     if device_name.lower() == "multiroom":
                           list_task_errors.append(details + " || Invalid Device | " + task[2])      

                     if task[3].strip() != "spotify" and task[3].strip() != "multiroom":
                           list_task_errors.append(details + " || Invalid interface | " + task[3])        

                     try:
                        if not task[4].isdigit():
                           list_task_errors.append(details + " || Invalid device_volume | " + task[4])     

                        else:
                           if not 100 <= int(task[4]) <= 200:
                              list_task_errors.append(details + " || Invalid volume_value (100 - 200) | " + task[4])    

                     except:
                        list_task_errors.append(details + " || Invalid volume_value | " + task[4])      

                  except:
                     list_task_errors.append(details + " || Invalid formatting")    


               else:
                  if task_trigger == "controller" or task_trigger == "program":
                     list_task_errors.append(details + " || Invalid command | " + task[1])
                  else:
                     list_task_errors.append(task[1] + " || Invalid command")


            except:
               if task_trigger == "controller" or task_trigger == "program":
                  list_task_errors.append(details + " || Missing setting | Command") 
               else:
                  list_task_errors.append("Missing setting || Command") 


         else:
            if task_trigger == "controller" or task_trigger == "program":
               list_task_errors.append(details + " || Invalid formatting")
            else:
               list_task_errors.append("Invalid formatting")   
            
         return list_task_errors
            

      # #####################
      # empty task controller
      # #####################

      if task == None and (task_trigger == "controller" or task_trigger == "program"): 
         return list_task_errors

      if task == "None" and (task_trigger == "controller" or task_trigger == "program"): 
         return list_task_errors

      if task == "" and (task_trigger == "controller" or task_trigger == "program"): 
         return list_task_errors


      # #############
      # nothing found
      # #############
      
      if task_trigger == "controller" or task_trigger == "program":
         list_task_errors.append(details + " || Invalid task") 
      else:
         list_task_errors.append("Invalid task") 
      
      return list_task_errors
   

   except Exception as e:
      if task_trigger == "controller" or task_trigger == "program":
         list_task_errors.append(details + " || Invalid task")   
      else:
         list_task_errors.append("Invalid task")        
      
      return list_task_errors


""" ################# """
"""  sensordata jobs  """
""" ################# """

def CHECK_SENSORDATA_JOBS(jobs): 
   error_message_settings = []

   for job in jobs:

      if job.filename == "":
         error_message_settings.append(job.name + " || Missing setting | Filename") 
      if job.device_ieeeAddr == None or job.device_ieeeAddr == "None":
         error_message_settings.append(job.name + " || Missing setting | Device") 
      if job.sensor_key == None or job.sensor_key == "None":
         error_message_settings.append(job.name + " || Missing setting | Sensor") 
                  
   return error_message_settings


""" ############### """
"""  user settings  """
""" ############### """

def CHECK_USERS(users): 
   error_message_settings = []

   for user in users:

      if user.password == "":
         error_message_settings.append(user.name + " || Missing setting | Password") 
        
   return error_message_settings