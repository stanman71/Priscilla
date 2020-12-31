from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.backend.tasks            import START_TASK

from difflib import SequenceMatcher


def PROCESS_CONTROLLER(ieeeAddr, msg):
    
    for controller in GET_ALL_CONTROLLER():
        
        if controller.device_ieeeAddr == ieeeAddr:
            
            # #########
            # command_1
            # #########

            try:                                                                                    
                if controller.command_1 != "None" and str(controller.command_1)[1:-1] in str(msg):
                    START_TASK(controller.task_1, "Controller", controller.device.name + " | " + controller.command_1[1:-1].replace('"',''))                      
                    return
          
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_1[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_2
            # #########
            
            try:
                if controller.command_2 != "None" and str(controller.command_2)[1:-1] in str(msg):
                    START_TASK(controller.task_2, "Controller", controller.device.name + " | " + controller.command_2[1:-1].replace('"',''))                      
                    return
                          
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_2[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_3
            # #########

            try:
                if controller.command_3 != "None" and str(controller.command_3)[1:-1] in str(msg):
                    START_TASK(controller.task_3, "Controller", controller.device.name + " | " + controller.command_3[1:-1].replace('"',''))         
                    return             

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_3[1:-1].replace('"','') + " | " + str(e))   
                                           
            # #########
            # command_4
            # #########
            
            try:
                if controller.command_4 != "None" and str(controller.command_4)[1:-1] in str(msg):
                    START_TASK(controller.task_4, "Controller", controller.device.name + " | " + controller.command_4[1:-1].replace('"',''))       
                    return               
                            
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_4[1:-1].replace('"','') + " | " + str(e))     
                               
            # #########
            # command_5
            # #########
            
            try:
                if controller.command_5 != "None" and str(controller.command_5)[1:-1] in str(msg):
                    START_TASK(controller.task_5, "Controller", controller.device.name + " | " + controller.command_5[1:-1].replace('"','')) 
                    return
                            
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_5[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_6
            # #########
            
            try:
                if controller.command_6 != "None" and str(controller.command_6)[1:-1] in str(msg):
                    START_TASK(controller.task_6, "Controller", controller.device.name + " | " + controller.command_6[1:-1].replace('"',''))                      
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_6[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_7
            # #########
            
            try: 
                if controller.command_7 != "None" and str(controller.command_7)[1:-1] in str(msg):
                    START_TASK(controller.task_7, "Controller", controller.device.name + " | " + controller.command_7[1:-1].replace('"',''))                                   
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_7[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_8
            # #########
            
            try:                                                                                    
                if controller.command_8 != "None" and str(controller.command_8)[1:-1] in str(msg):
                    START_TASK(controller.task_8, "Controller", controller.device.name + " | " + controller.command_8[1:-1].replace('"',''))                      
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_8[1:-1].replace('"','') + " | " + str(e))   
                               
            # #########
            # command_9
            # #########
            
            try:
                if controller.command_9 != "None" and str(controller.command_9)[1:-1] in str(msg):
                    START_TASK(controller.task_9, "Controller", controller.device.name + " | " + controller.command_9[1:-1].replace('"',''))                      
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_9[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_10
            # ##########
            
            try:                                                                                      
                if controller.command_10 != "None" and str(controller.command_10)[1:-1] in str(msg):
                    START_TASK(controller.task_10, "Controller", controller.device.name + " | " + controller.command_10[1:-1].replace('"',''))                      
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_10[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_11
            # ##########
            
            try:                                                                  
                if controller.command_11 != "None" and str(controller.command_11)[1:-1] in str(msg):
                    START_TASK(controller.task_11, "Controller", controller.device.name + " | " + controller.command_11[1:-1].replace('"',''))                      
                    return

            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_11[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_12
            # ##########
            
            try:
                if controller.command_12 != "None" and str(controller.command_12)[1:-1] in str(msg):
                    START_TASK(controller.task_12, "Controller", controller.device.name + " | " + controller.command_12[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_12[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_13
            # ##########
            
            try:
                if controller.command_13 != "None" and str(controller.command_13)[1:-1] in str(msg):
                    START_TASK(controller.task_13, "Controller", controller.device.name + " | " + controller.command_13[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_13[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_14
            # ##########
            
            try:
                if controller.command_14 != "None" and str(controller.command_14)[1:-1] in str(msg):
                    START_TASK(controller.task_14, "Controller", controller.device.name + " | " + controller.command_14[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_14[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_15
            # ##########
            
            try:
                if controller.command_15 != "None" and str(controller.command_15)[1:-1] in str(msg):
                    START_TASK(controller.task_15, "Controller", controller.device.name + " | " + controller.command_15[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_15[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_16
            # ##########
            
            try:
                if controller.command_16 != "None" and str(controller.command_16)[1:-1] in str(msg):
                    START_TASK(controller.task_16, "Controller", controller.device.name + " | " + controller.command_16[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_16[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_17
            # ##########
            
            try:
                if controller.command_17 != "None" and str(controller.command_17)[1:-1] in str(msg):
                    START_TASK(controller.task_17, "Controller", controller.device.name + " | " + controller.command_17[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_17[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_18
            # ##########
            
            try:
                if controller.command_18 != "None" and str(controller.command_18)[1:-1] in str(msg):
                    START_TASK(controller.task_18, "Controller", controller.device.name + " | " + controller.command_18[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_18[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_19
            # ##########
            
            try:
                if controller.command_19 != "None" and str(controller.command_19)[1:-1] in str(msg):
                    START_TASK(controller.task_19, "Controller", controller.device.name + " | " + controller.command_19[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_19[1:-1].replace('"','') + " | " + str(e))   

            # ##########
            # command_20
            # ##########
            
            try:
                if controller.command_20 != "None" and str(controller.command_20)[1:-1] in str(msg):
                    START_TASK(controller.task_20, "Controller", controller.device.name + " | " + controller.command_20[1:-1].replace('"',''))                      
                    return
           
            except Exception as e:
                WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller | " + controller.device.name + " | Command | " + controller.command_20[1:-1].replace('"','') + " | " + str(e))                                            