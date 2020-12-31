from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import *
from app.backend.shared_resources import *
from app.backend.tasks            import START_TASK

import threading

stop_program_thread_1 = False
stop_program_thread_2 = False
stop_program_thread_3 = False
stop_program_thread_4 = False
stop_program_thread_5 = False
stop_program_thread_6 = False
stop_program_thread_7 = False
stop_program_thread_8 = False
stop_program_thread_9 = False


""" ################# """
"""  process program  """
""" ################# """

def PROCESS_PROGRAM(command, program, blocked_program_thread_id = 0):

    if command == "start":
        START_PROGRAM_THREAD(program)

    if command == "stop":
        STOP_PROGRAM_THREAD_BY_NAME(program, blocked_program_thread_id)


""" ###################### """
"""  start program thread  """
""" ###################### """

def START_PROGRAM_THREAD(program_id):

    try:

        if GET_PROGRAM_THREAD_STATUS_1()[0] == "None":
            thread_id    = 1
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_1 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_1.start()   
   
            SET_PROGRAM_THREAD_STATUS_1(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True
    
        elif GET_PROGRAM_THREAD_STATUS_2()[0] == "None":
            thread_id    = 2
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_2 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_2.start()   
   
            SET_PROGRAM_THREAD_STATUS_2(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_3()[0] == "None":
            thread_id    = 3
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_3 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_3.start()   
   
            SET_PROGRAM_THREAD_STATUS_3(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_4()[0] == "None":
            thread_id    = 4
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_4 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_4.start()   
   
            SET_PROGRAM_THREAD_STATUS_4(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_5()[0] == "None":
            thread_id    = 5
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_5 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_5.start()   
   
            SET_PROGRAM_THREAD_STATUS_5(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_6()[0] == "None":
            thread_id    = 6
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_6 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_6.start()   
   
            SET_PROGRAM_THREAD_STATUS_6(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_7()[0] == "None":
            thread_id    = 7
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_7 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_7.start()   
   
            SET_PROGRAM_THREAD_STATUS_7(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_8()[0] == "None":
            thread_id    = 8
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_8 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_8.start()   
   
            SET_PROGRAM_THREAD_STATUS_8(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_9()[0] == "None":
            thread_id    = 9
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_9 = threading.Thread(target = PROGRAM_THREAD, args=(thread_id,program_id, )) 
            program_thread_9.start()   
   
            SET_PROGRAM_THREAD_STATUS_9(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | started") 
            return True            

        else:
            return ("No empty program tread found")

    except Exception as e:
        return e


""" ################ """
"""  program thread  """
""" ################ """
   
def PROGRAM_THREAD(thread_id, program_id):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5    
    global stop_program_thread_6   
    global stop_program_thread_7   
    global stop_program_thread_8   
    global stop_program_thread_9   

    try:

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


        program_name = GET_PROGRAM_BY_ID(program_id).name
        line_number  = 1

        # get total lines
        lines_total = 0

        for line in list_lines:
            if line[0] == "True":
                lines_total = lines_total + 1


        for line in list_lines:

            # program stopped
            if thread_id == 1 and stop_program_thread_1 == True:
                stop_program_thread_1 = False   
                
                SET_PROGRAM_THREAD_STATUS_1("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 2 and stop_program_thread_2 == True:
                stop_program_thread_2 = False  
                
                SET_PROGRAM_THREAD_STATUS_2("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 3 and stop_program_thread_3 == True:
                stop_program_thread_3 = False   
                
                SET_PROGRAM_THREAD_STATUS_3("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 4 and stop_program_thread_4 == True:
                stop_program_thread_4 = False    
                
                SET_PROGRAM_THREAD_STATUS_4("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 5 and stop_program_thread_5 == True:
                stop_program_thread_5 = False    
                
                SET_PROGRAM_THREAD_STATUS_5("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 6 and stop_program_thread_6 == True:
                stop_program_thread_6 = False   
                
                SET_PROGRAM_THREAD_STATUS_6("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 7 and stop_program_thread_7 == True:
                stop_program_thread_7 = False   
                
                SET_PROGRAM_THREAD_STATUS_7("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 8 and stop_program_thread_8 == True:
                stop_program_thread_8 = False 
                
                SET_PROGRAM_THREAD_STATUS_8("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return

            if thread_id == 9 and stop_program_thread_9 == True:
                stop_program_thread_9 = False   
                
                SET_PROGRAM_THREAD_STATUS_9("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program | " + program_name + " | stopped")
                return            


            # program keep running
            else:

                # update program status
                if thread_id == 1:
                    SET_PROGRAM_THREAD_STATUS_1(program_name,line_number,lines_total,line[1])
                if thread_id == 2:
                    SET_PROGRAM_THREAD_STATUS_2(program_name,line_number,lines_total,line[1])
                if thread_id == 3:
                    SET_PROGRAM_THREAD_STATUS_3(program_name,line_number,lines_total,line[1])
                if thread_id == 4:
                    SET_PROGRAM_THREAD_STATUS_4(program_name,line_number,lines_total,line[1])
                if thread_id == 5:
                    SET_PROGRAM_THREAD_STATUS_5(program_name,line_number,lines_total,line[1])
                if thread_id == 6:
                    SET_PROGRAM_THREAD_STATUS_6(program_name,line_number,lines_total,line[1])
                if thread_id == 7:
                    SET_PROGRAM_THREAD_STATUS_7(program_name,line_number,lines_total,line[1])
                if thread_id == 8:
                    SET_PROGRAM_THREAD_STATUS_8(program_name,line_number,lines_total,line[1])
                if thread_id == 9:
                    SET_PROGRAM_THREAD_STATUS_9(program_name,line_number,lines_total,line[1])


                # line active ?
                if line[0] == "True":


                    # #####
                    # break
                    # #####
                            
                    if "break" in line[1]:
                            
                        line_content = line[1].split(" # ")

                        second = 0

                        while second != int(line_content[1].strip()):
                            second = second + 1
                            time.sleep(1)

                            # program stopped ?
                            if thread_id == 1 and stop_program_thread_1 == True:
                                break
                            if thread_id == 2 and stop_program_thread_2 == True:
                                break
                            if thread_id == 3 and stop_program_thread_3 == True:
                                break
                            if thread_id == 4 and stop_program_thread_4 == True:
                                break
                            if thread_id == 5 and stop_program_thread_5 == True:
                                break
                            if thread_id == 6 and stop_program_thread_6 == True:
                                break                            
                            if thread_id == 7 and stop_program_thread_7 == True:
                                break       
                            if thread_id == 8 and stop_program_thread_8 == True:
                                break       
                            if thread_id == 9 and stop_program_thread_9 == True:
                                break       

                    else: 
                        START_TASK(line[1], "Program", program_name, thread_id)

                    line_number = line_number + 1
                    time.sleep(1)


        # program regulary finished
        if thread_id == 1:
            SET_PROGRAM_THREAD_STATUS_1("None","","","")  
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 2:
            SET_PROGRAM_THREAD_STATUS_2("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 3:
            SET_PROGRAM_THREAD_STATUS_3("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 4:
            SET_PROGRAM_THREAD_STATUS_4("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 5:
            SET_PROGRAM_THREAD_STATUS_5("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 6:
            SET_PROGRAM_THREAD_STATUS_6("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 7:
            SET_PROGRAM_THREAD_STATUS_7("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 8:
            SET_PROGRAM_THREAD_STATUS_8("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")

        if thread_id == 9:
            SET_PROGRAM_THREAD_STATUS_9("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program | " + program_name + " | finished")            


    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Programm | " + GET_PROGRAM_BY_ID(program_id).name + " | " + str(e))
        return str(e)


""" #################### """
"""  stop program by id  """
""" #################### """

def STOP_PROGRAM_THREAD_BY_ID(thread_id):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5    
    global stop_program_thread_6   
    global stop_program_thread_7   
    global stop_program_thread_8   
    global stop_program_thread_9   

    if thread_id == 1:
        stop_program_thread_1 = True
        program_name = GET_PROGRAM_THREAD_STATUS_1()[0]
        SET_PROGRAM_THREAD_STATUS_1(program_name,"","","STOPPED")
        return True

    if thread_id == 2:
        stop_program_thread_2 = True
        program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
        SET_PROGRAM_THREAD_STATUS_2(program_name,"","","STOPPED")
        return True

    if thread_id == 3:
        stop_program_thread_3 = True
        program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
        SET_PROGRAM_THREAD_STATUS_3(program_name,"","","STOPPED")
        return True

    if thread_id == 4:
        stop_program_thread_4 = True
        program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
        SET_PROGRAM_THREAD_STATUS_4(program_name,"","","STOPPED")
        return True

    if thread_id == 5:
        stop_program_thread_5 = True
        program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
        SET_PROGRAM_THREAD_STATUS_5(program_name,"","","STOPPED")
        return True

    if thread_id == 6:
        stop_program_thread_6 = True
        program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
        SET_PROGRAM_THREAD_STATUS_6(program_name,"","","STOPPED")
        return True

    if thread_id == 7:
        stop_program_thread_7 = True
        program_name = GET_PROGRAM_THREAD_STATUS_7()[0]
        SET_PROGRAM_THREAD_STATUS_7(program_name,"","","STOPPED")
        return True

    if thread_id == 8:
        stop_program_thread_8 = True
        program_name = GET_PROGRAM_THREAD_STATUS_8()[0]
        SET_PROGRAM_THREAD_STATUS_8(program_name,"","","STOPPED")
        return True

    if thread_id == 9:
        stop_program_thread_9 = True
        program_name = GET_PROGRAM_THREAD_STATUS_9()[0]
        SET_PROGRAM_THREAD_STATUS_9(program_name,"","","STOPPED")
        return True


""" ###################### """
"""  stop program by name  """
""" ###################### """

def STOP_PROGRAM_THREAD_BY_NAME(program_name, blocked_program_thread_id = 0):
    global stop_program_thread_1
    global stop_program_thread_2
    global stop_program_thread_3
    global stop_program_thread_4
    global stop_program_thread_5    
    global stop_program_thread_6   
    global stop_program_thread_7   
    global stop_program_thread_8   
    global stop_program_thread_9   

    try:
        if blocked_program_thread_id != 1:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_1()[0].lower():
                stop_program_thread_1 = True
                program_name = GET_PROGRAM_THREAD_STATUS_1()[0]
                SET_PROGRAM_THREAD_STATUS_1(program_name,"","","STOPPED")            

        if blocked_program_thread_id != 2:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_2()[0].lower():
                stop_program_thread_2 = True
                program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
                SET_PROGRAM_THREAD_STATUS_2(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 3:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_3()[0].lower():
                stop_program_thread_3 = True
                program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
                SET_PROGRAM_THREAD_STATUS_3(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 4:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_4()[0].lower():
                stop_program_thread_4 = True
                program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
                SET_PROGRAM_THREAD_STATUS_4(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 5:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_5()[0].lower():
                stop_program_thread_5 = True
                program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
                SET_PROGRAM_THREAD_STATUS_5(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 6:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_6()[0].lower():
                stop_program_thread_6 = True
                program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
                SET_PROGRAM_THREAD_STATUS_6(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 7:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_7()[0].lower():
                stop_program_thread_7 = True
                program_name = GET_PROGRAM_THREAD_STATUS_7()[0]
                SET_PROGRAM_THREAD_STATUS_7(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 8:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_8()[0].lower():
                stop_program_thread_8 = True
                program_name = GET_PROGRAM_THREAD_STATUS_8()[0]
                SET_PROGRAM_THREAD_STATUS_8(program_name,"","","STOPPED")                   

        if blocked_program_thread_id != 9:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_9()[0].lower():
                stop_program_thread_9 = True
                program_name = GET_PROGRAM_THREAD_STATUS_9()[0]
                SET_PROGRAM_THREAD_STATUS_9(program_name,"","","STOPPED")                   

    except:
        pass