import heapq
import re
import threading
import time

from app import app
from app.database.models          import *
from app.backend.file_management  import SAVE_DATABASE, WRITE_LOGFILE_SYSTEM
from app.backend.mqtt             import UPDATE_DEVICES
from app.backend.email            import SEND_EMAIL
from app.backend.shared_resources import process_management_queue


""" ################ """
""" management queue """
""" ################ """

# https://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php

def PROCESS_MANAGEMENT_THREAD():

    try:
        Thread = threading.Thread(target=PROCESS_MANAGEMENT)
        Thread.start() 
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Thread | Process Management | " + str(e)) 
        SEND_EMAIL("ERROR", "Thread | Process Management | " + str(e))      


def PROCESS_MANAGEMENT():
    
    while True:

        try:
            process = heapq.heappop(process_management_queue)[1]
        
            # ###########
            #  scheduler
            # ###########
                                    
            if process[0] == "scheduler":                        

                if process[1] == "update_devices":
                    UPDATE_DEVICES()

                if process[1] == "create_database_backup":  
                    SAVE_DATABASE()                  
  
        except Exception as e:         
            try:
            
                if "index out of range" not in str(e):
                    WRITE_LOGFILE_SYSTEM("ERROR", "Process Management | Process - " + process + " | " + str(e))  
                    SEND_EMAIL("ERROR", "Process Management | Process - " + process + " | " + str(e))               
                    print(str(e))
                    
            except:
                pass
                
              
        time.sleep(0.5)