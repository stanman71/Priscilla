from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.shared_resources import *
from app.backend.tasks            import START_TASK

from difflib import SequenceMatcher


""" ################################ """
""" ################################ """
"""  command hold break loop thread  """
""" ################################ """
""" ################################ """


command_hold_break_loop = False

def START_COMMAND_HOLD_BREAK_LOOP_THREAD():
	try:
		Thread = threading.Thread(target=COMMAND_HOLD_BREAK_LOOP_THREAD)
		Thread.start()  
		
	except Exception as e:
		WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Break Loop Thread | " + str(e)) 
		SEND_EMAIL("ERROR", "System | Thread | Break Loop Thread | " + str(e))     
    

def COMMAND_HOLD_BREAK_LOOP_THREAD():   
    global command_hold_break_loop

    limit = 0

    while True:

        # search for release message
        for message in GET_MQTT_INCOMING_MESSAGES(1):   
            if "release" in str(message[2]):
                command_hold_break_loop = True
                return

        # limit 3 seconds
        if limit == 30:
            command_hold_break_loop = True
            return

        limit = limit + 1
        time.sleep(0.1)


""" ################################ """
""" ################################ """
"""        process controller        """
""" ################################ """
""" ################################ """


def PROCESS_CONTROLLER(ieeeAddr, msg):
    global command_hold_break_loop

    for controller in GET_ALL_CONTROLLER():
        
        if controller.device_ieeeAddr == ieeeAddr:
            
            # #########
            # command_1
            # #########
            
            try:                                                                                    
                if str(controller.command_1)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_1, "Controller", controller.device.name + " - " + controller.command_1[1:-1].replace('"',''))    

                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_1, "Controller", controller.device.name + " - " + controller.command_1[1:-1].replace('"',''))                      
                        return
          
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_2
            # #########
            
            try:

                if str(controller.command_2)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()

                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_2, "Controller", controller.device.name + " - " + controller.command_2[1:-1].replace('"',''))    

                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_2, "Controller", controller.device.name + " - " + controller.command_2[1:-1].replace('"',''))                      
                        return
                          
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):

                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_3
            # #########

            try:

                if str(controller.command_3)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()

                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_3, "Controller", controller.device.name + " - " + controller.command_3[1:-1].replace('"',''))    

                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_3, "Controller", controller.device.name + " - " + controller.command_3[1:-1].replace('"',''))                      
                        return

            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                                           
            # #########
            # command_4
            # #########
            
            try:

                if str(controller.command_4)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_4, "Controller", controller.device.name + " - " + controller.command_4[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_4, "Controller", controller.device.name + " - " + controller.command_4[1:-1].replace('"',''))                      
                        return
                            
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):

                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_5
            # #########
            
            try:

                if str(controller.command_5)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_5, "Controller", controller.device.name + " - " + controller.command_5[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_5, "Controller", controller.device.name + " - " + controller.command_5[1:-1].replace('"',''))                      
                        return
                            
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_6
            # #########
            
            try:

                if str(controller.command_6)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_6, "Controller", controller.device.name + " - " + controller.command_6[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_6, "Controller", controller.device.name + " - " + controller.command_6[1:-1].replace('"',''))                      
                        return
                               
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_7
            # #########
            
            try:
           
                if str(controller.command_7)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_7, "Controller", controller.device.name + " - " + controller.command_7[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_7, "Controller", controller.device.name + " - " + controller.command_7[1:-1].replace('"',''))                      
                        return                  
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_8
            # #########
            
            try:                                            
                                                
                if str(controller.command_8)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_8, "Controller", controller.device.name + " - " + controller.command_8[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_8, "Controller", controller.device.name + " - " + controller.command_8[1:-1].replace('"',''))                      
                        return
                            
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    
                               
            # #########
            # command_9
            # #########
            
            try:

                if str(controller.command_9)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_9, "Controller", controller.device.name + " - " + controller.command_9[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_9, "Controller", controller.device.name + " - " + controller.command_9[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))     

            # ##########
            # command_10
            # ##########
            
            try:                                              
                                            
                if str(controller.command_10)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_10, "Controller", controller.device.name + " - " + controller.command_10[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_10, "Controller", controller.device.name + " - " + controller.command_10[1:-1].replace('"',''))                      
                        return
        
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_11
            # ##########
            
            try:
                                                                       
                if str(controller.command_11)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_11, "Controller", controller.device.name + " - " + controller.command_11[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_11, "Controller", controller.device.name + " - " + controller.command_11[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_12
            # ##########
            
            try:

                if str(controller.command_12)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_12, "Controller", controller.device.name + " - " + controller.command_12[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_12, "Controller", controller.device.name + " - " + controller.command_12[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))     

            # ##########
            # command_13
            # ##########
            
            try:

                if str(controller.command_13)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_13, "Controller", controller.device.name + " - " + controller.command_13[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_13, "Controller", controller.device.name + " - " + controller.command_13[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_14
            # ##########
            
            try:

                if str(controller.command_14)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_14, "Controller", controller.device.name + " - " + controller.command_14[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_14, "Controller", controller.device.name + " - " + controller.command_14[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_15
            # ##########
            
            try:

                if str(controller.command_15)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_15, "Controller", controller.device.name + " - " + controller.command_15[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_15, "Controller", controller.device.name + " - " + controller.command_15[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):

                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_16
            # ##########
            
            try:

                if str(controller.command_16)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_16, "Controller", controller.device.name + " - " + controller.command_16[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_16, "Controller", controller.device.name + " - " + controller.command_16[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))     

            # ##########
            # command_17
            # ##########
            
            try:

                if str(controller.command_17)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_17, "Controller", controller.device.name + " - " + controller.command_17[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_17, "Controller", controller.device.name + " - " + controller.command_17[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))     

            # ##########
            # command_18
            # ##########
            
            try:

                if str(controller.command_18)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_18, "Controller", controller.device.name + " - " + controller.command_18[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_18, "Controller", controller.device.name + " - " + controller.command_18[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))    

            # ##########
            # command_19
            # ##########
            
            try:

                if str(controller.command_19)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                        
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_19, "Controller", controller.device.name + " - " + controller.command_19[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_19, "Controller", controller.device.name + " - " + controller.command_19[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))     

            # ##########
            # command_20
            # ##########
            
            try:

                if str(controller.command_20)[1:-1] in str(msg):

                    # special case "hold" command (Xiaomi Opple)
                    if "hold" in str(msg):                       
                        START_COMMAND_HOLD_BREAK_LOOP_THREAD()
                         
                        while command_hold_break_loop == False:     
                            START_TASK(controller.task_20, "Controller", controller.device.name + " - " + controller.command_20[1:-1].replace('"',''))    
                            
                        command_hold_break_loop = False

                    else:
                        START_TASK(controller.task_20, "Controller", controller.device.name + " - " + controller.command_20[1:-1].replace('"',''))                      
                        return
           
            except Exception as e:
                if ("list index out of range" not in str(e) and 
                    "Expecting value: line 1 column 1 (char 0)" not in str(e) and                 
                    "'NoneType' object is not subscriptable" not in str(e) and 
                    "argument of type 'NoneType' is not iterable" not in str(e)):
                   
                    WRITE_LOGFILE_SYSTEM("ERROR", "Network | Controller - " + controller.device.name + " | Command - " + controller.command_2[1:-1].replace('"','') + " | " + str(e))                                            