import heapq
import threading
import time

from app                            import app
from app.backend.database_models    import *
from app.backend.file_management    import WRITE_LOGFILE_SYSTEM
from app.backend.email              import SEND_EMAIL
from app.backend.shared_resources   import process_management_queue
from app.backend.process_controller import PROCESS_CONTROLLER
from app.backend.process_program    import PROCESS_PROGRAM
from app.backend.process_scheduler  import PROCESS_SCHEDULER


""" ########################## """
"""  process management queue  """
""" ########################## """

# https://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php

def PROCESS_MANAGEMENT_THREAD():

    try:
        Thread = threading.Thread(target=PROCESS_MANAGEMENT)
        Thread.start() 
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "System | Thread | Process Management | " + str(e)) 
        SEND_EMAIL("ERROR", "System | Thread | Process Management | " + str(e))      


def PROCESS_MANAGEMENT():
    
    while True:

        try:
            process = heapq.heappop(process_management_queue)[1]

            # ##########
            # controller
            # ##########
            
            if process[0] == "controller":
                ieeeAddr = process[1]
                msg      = process[2]
                
                PROCESS_CONTROLLER(ieeeAddr, msg)           


            # #######
            # program
            # #######
                                    
            if process[0] == "program": 

                if process[1] == "start":   
                    program_id = process[2]

                    PROCESS_PROGRAM("start", program_id) 

                if process[1] == "stop":   
                    program_name              = process[2]
                    blocked_program_thread_id = process[3]

                    PROCESS_PROGRAM("stop", program_name, blocked_program_thread_id) 


            # #########
            # scheduler
            # #########
                                    
            if process[0] == "scheduler":         
                task     = GET_SCHEDULER_JOB_BY_ID(process[1])
                ieeeAddr = process[2]
                
                PROCESS_SCHEDULER(task, ieeeAddr)


        except Exception as e:         
            try:   
                if "index out of range" not in str(e) and "argument of type 'NoneType' is not iterable" not in str(e):
                    WRITE_LOGFILE_SYSTEM("ERROR", "System | Process Management | " + str(process) + " | " + str(e))  

            except:
                pass
                
              
        time.sleep(0.1)