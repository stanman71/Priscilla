import threading
import heapq
import time
import spotipy
import re

from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import *
from app.backend.shared_resources import *
from app.backend.mqtt             import CHECK_DEVICE_EXCEPTIONS, CHECK_DEVICE_SETTING_THREAD, REQUEST_SENSORDATA, CHECK_DEVICE_SETTING_PROCESS
from app.backend.lighting         import *
from app.backend.spotify          import *


stop_program_thread_1 = False
stop_program_thread_2 = False
stop_program_thread_3 = False
stop_program_thread_4 = False
stop_program_thread_5 = False
stop_program_thread_6 = False
stop_program_thread_7 = False
stop_program_thread_8 = False
stop_program_thread_9 = False


def START_PROGRAM_THREAD(program_id):

    try:

        if GET_PROGRAM_THREAD_STATUS_1()[0] == "None":
            thread_id    = 1
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_1 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_1.start()   
   
            SET_PROGRAM_THREAD_STATUS_1(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True
    
        elif GET_PROGRAM_THREAD_STATUS_2()[0] == "None":
            thread_id    = 2
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_2 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_2.start()   
   
            SET_PROGRAM_THREAD_STATUS_2(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_3()[0] == "None":
            thread_id    = 3
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_3 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_3.start()   
   
            SET_PROGRAM_THREAD_STATUS_3(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_4()[0] == "None":
            thread_id    = 4
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_4 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_4.start()   
   
            SET_PROGRAM_THREAD_STATUS_4(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_5()[0] == "None":
            thread_id    = 5
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_5 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_5.start()   
   
            SET_PROGRAM_THREAD_STATUS_5(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_6()[0] == "None":
            thread_id    = 6
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_6 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_6.start()   
   
            SET_PROGRAM_THREAD_STATUS_6(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_7()[0] == "None":
            thread_id    = 7
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_7 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_7.start()   
   
            SET_PROGRAM_THREAD_STATUS_7(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_8()[0] == "None":
            thread_id    = 8
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_8 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_8.start()   
   
            SET_PROGRAM_THREAD_STATUS_8(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True

        elif GET_PROGRAM_THREAD_STATUS_9()[0] == "None":
            thread_id    = 9
            program_name = GET_PROGRAM_BY_ID(program_id).name

            program_thread_9 = threading.Thread(target = PROGRAM_THREAD, args =(thread_id,program_id, )) 
            program_thread_9.start()   
   
            SET_PROGRAM_THREAD_STATUS_9(program_name,0,0,"")
            WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | started") 
            return True            

        else:
            return ("No empty program tread found")

    except Exception as e:
        return e


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

    if thread_id == 2:
        stop_program_thread_2 = True
        program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
        SET_PROGRAM_THREAD_STATUS_2(program_name,"","","STOPPED")

    if thread_id == 3:
        stop_program_thread_3 = True
        program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
        SET_PROGRAM_THREAD_STATUS_3(program_name,"","","STOPPED")

    if thread_id == 4:
        stop_program_thread_4 = True
        program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
        SET_PROGRAM_THREAD_STATUS_4(program_name,"","","STOPPED")

    if thread_id == 5:
        stop_program_thread_5 = True
        program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
        SET_PROGRAM_THREAD_STATUS_5(program_name,"","","STOPPED")

    if thread_id == 6:
        stop_program_thread_6 = True
        program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
        SET_PROGRAM_THREAD_STATUS_6(program_name,"","","STOPPED")

    if thread_id == 7:
        stop_program_thread_7 = True
        program_name = GET_PROGRAM_THREAD_STATUS_7()[0]
        SET_PROGRAM_THREAD_STATUS_7(program_name,"","","STOPPED")

    if thread_id == 8:
        stop_program_thread_8 = True
        program_name = GET_PROGRAM_THREAD_STATUS_8()[0]
        SET_PROGRAM_THREAD_STATUS_8(program_name,"","","STOPPED")

    if thread_id == 9:
        stop_program_thread_9 = True
        program_name = GET_PROGRAM_THREAD_STATUS_9()[0]
        SET_PROGRAM_THREAD_STATUS_9(program_name,"","","STOPPED")


def STOP_PROGRAM_THREAD_BY_NAME(program_name, thread_id = 0):
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
        if thread_id != 1:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_1()[0].lower():
                stop_program_thread_1 = True
                program_name = GET_PROGRAM_THREAD_STATUS_1()[0]
                SET_PROGRAM_THREAD_STATUS_1(program_name,"","","STOPPED")            

        if thread_id != 2:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_2()[0].lower():
                stop_program_thread_2 = True
                program_name = GET_PROGRAM_THREAD_STATUS_2()[0]
                SET_PROGRAM_THREAD_STATUS_2(program_name,"","","STOPPED")                   

        if thread_id != 3:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_3()[0].lower():
                stop_program_thread_3 = True
                program_name = GET_PROGRAM_THREAD_STATUS_3()[0]
                SET_PROGRAM_THREAD_STATUS_3(program_name,"","","STOPPED")                   

        if thread_id != 4:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_4()[0].lower():
                stop_program_thread_4 = True
                program_name = GET_PROGRAM_THREAD_STATUS_4()[0]
                SET_PROGRAM_THREAD_STATUS_4(program_name,"","","STOPPED")                   

        if thread_id != 5:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_5()[0].lower():
                stop_program_thread_5 = True
                program_name = GET_PROGRAM_THREAD_STATUS_5()[0]
                SET_PROGRAM_THREAD_STATUS_5(program_name,"","","STOPPED")                   

        if thread_id != 6:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_6()[0].lower():
                stop_program_thread_6 = True
                program_name = GET_PROGRAM_THREAD_STATUS_6()[0]
                SET_PROGRAM_THREAD_STATUS_6(program_name,"","","STOPPED")                   

        if thread_id != 7:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_7()[0].lower():
                stop_program_thread_7 = True
                program_name = GET_PROGRAM_THREAD_STATUS_7()[0]
                SET_PROGRAM_THREAD_STATUS_7(program_name,"","","STOPPED")                   

        if thread_id != 8:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_8()[0].lower():
                stop_program_thread_8 = True
                program_name = GET_PROGRAM_THREAD_STATUS_8()[0]
                SET_PROGRAM_THREAD_STATUS_8(program_name,"","","STOPPED")                   

        if thread_id != 9:
            if program_name.lower() == GET_PROGRAM_THREAD_STATUS_9()[0].lower():
                stop_program_thread_9 = True
                program_name = GET_PROGRAM_THREAD_STATUS_9()[0]
                SET_PROGRAM_THREAD_STATUS_9(program_name,"","","STOPPED")                   

    except:
        pass

   
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
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 2 and stop_program_thread_2 == True:
                stop_program_thread_2 = False  
                
                SET_PROGRAM_THREAD_STATUS_2("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 3 and stop_program_thread_3 == True:
                stop_program_thread_3 = False  
                
                SET_PROGRAM_THREAD_STATUS_3("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 4 and stop_program_thread_4 == True:
                stop_program_thread_4 = False  
                
                SET_PROGRAM_THREAD_STATUS_4("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 5 and stop_program_thread_5 == True:
                stop_program_thread_5 = False  
                
                SET_PROGRAM_THREAD_STATUS_5("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 6 and stop_program_thread_6 == True:
                stop_program_thread_6 = False  
                
                SET_PROGRAM_THREAD_STATUS_6("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 7 and stop_program_thread_7 == True:
                stop_program_thread_7 = False  
                
                SET_PROGRAM_THREAD_STATUS_7("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 8 and stop_program_thread_8 == True:
                stop_program_thread_8 = False  
                
                SET_PROGRAM_THREAD_STATUS_8("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
                return

            if thread_id == 9 and stop_program_thread_9 == True:
                stop_program_thread_9 = False  
                
                SET_PROGRAM_THREAD_STATUS_9("None","","","")
                WRITE_LOGFILE_SYSTEM("EVENT", "Program - " + program_name + " | stopped")
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

                            # program stopped
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


                    # #####
                    # light
                    # #####

                    if "lighting" in line[1] and "start_scene" in line[1]:

                        line_content = line[1].split(" # ")

                        try:
                            
                            group = GET_LIGHTING_GROUP_BY_NAME(line_content[2].strip())
                            scene = GET_LIGHTING_SCENE_BY_NAME(line_content[3].strip())

                            # group existing ?
                            if group != None:

                                # scene existing ?
                                if scene != None:

                                    try:
                                        brightness = int(line_content[4].strip())
                                    except:
                                        brightness = 100           
                                    
                                    SET_LIGHTING_GROUP_SCENE(group.id, scene.id, brightness)
                                    CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, scene.id, scene.name, brightness, 2, 10)

                                else:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Scene - " + line_content[3] + " - not found")   

                            else:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Group - " + line_content[2] + " - not found")   
         
                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))


                    if "lighting" in line[1] and "light" in line[1] and "start_scene" not in line[1] and "turn_off" not in line[1]:

                        line_content = line[1].split(" # ")

                        try:                     
                            device = GET_DEVICE_BY_NAME(line_content[2].strip())

                            # device existing ?
                            if device != None:

                                try:
                                    rgb_values = re.findall(r'\d+', line_content[3])
                                except:
                                    rgb_values = []                                        

                                try:
                                    brightness = int(line_content[4].strip())
                                except:
                                    brightness = 100     

                                if rgb_values != []:                                  
                                    SET_LIGHT_RGB_THREAD(device.ieeeAddr, rgb_values[0], rgb_values[1], rgb_values[2], brightness)
                                    CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "ON", 10)

                            else:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Device - " + line_content[3] + " - not found")   
         
                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))


                    if "lighting" in line[1] and "turn_off" in line[1]:

                        line_content = line[1].split(" # ")

                        try:
                            
                            # turn off group
                            if line_content[2].lower() == "group":

                                # get input group names and lower the letters
                                try:
                                    list_groups = line_content[3].split(",")
                                except:
                                    list_groups = [line_content[3]]

                                for input_group_name in list_groups:
                                    input_group_name = input_group_name.strip()

                                    group_found = False

                                # get exist group names
                                for group in GET_ALL_LIGHTING_GROUPS():

                                    if input_group_name.lower() == group.name.lower():
                                        group_found = True

                                        SET_LIGHTING_GROUP_TURN_OFF(group.id)
                                        CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   

                                # group not found
                                if group_found == False:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Group - " + input_group_name + " - not found")   


                            # turn off light
                            if line_content[2].lower() == "light":

                                device = GET_DEVICE_BY_NAME(line_content[3].strip())

                                # device existing ?
                                if device != None:                            
                                    SET_LIGHT_TURN_OFF_THREAD(device.ieeeAddr)
                                    CHECK_DEVICE_SETTING_PROCESS(device.ieeeAddr, "OFF", 10)

                                else:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Light - " + line_content[3] + " - not found")   


                            # turn off all
                            if line_content[2].lower() == "all":

                                for light in GET_ALL_DEVICES("light"):
                                    Thread = threading.Thread(target=SET_LIGHT_TURN_OFF_THREAD, args=(light.ieeeAddr, ))
                                    Thread.start()   

                                for group in GET_ALL_LIGHTING_GROUPS():
                                    CHECK_LIGHTING_GROUP_SETTING_THREAD(group.id, 0, "OFF", 0, 5, 20)   


                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))


                    # ######    
                    # device
                    # ######

                    if "device" in line[1]:
                            
                        line_content = line[1].split(" # ")

                        try:
  
                            # get input group names 
                            for device_name in line_content[1].split(","): 
                                device = GET_DEVICE_BY_NAME(device_name.strip())
                                
                                # device found ?
                                if device != None:
                                    program_command = line_content[2]

                                    # check device exception
                                    check_result = CHECK_DEVICE_EXCEPTIONS(device.ieeeAddr, program_command)
     
                                    if check_result == True:         

                                        if device.gateway == "mqtt":

                                            # special case roborock s50
                                            if device.model == "roborock_s50":
                                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/command"  
                                            else:
                                                channel = "smarthome/mqtt/" + device.ieeeAddr + "/set"  

                                        if device.gateway == "zigbee2mqtt":   
                                            channel = "smarthome/zigbee2mqtt/" + device.name + "/set"          

                                        command_position  = 0

                                        # special case roborock s50
                                        if device.model == "roborock_s50":
                                            list_command_json = device.commands_json.split(",")

                                        else:
                                            list_command_json = device.commands_json.replace("},{", "};{")                       
                                            list_command_json = list_command_json.split(";")

                                        # get the json command statement and start process
                                        for command in device.commands.split(","):     
                                                                    
                                            if str(program_command.lower()) == command.lower():
                                                heapq.heappush(mqtt_message_queue, (10, (channel, list_command_json[command_position])))            
                                                CHECK_DEVICE_SETTING_THREAD(device.ieeeAddr, program_command, 60)      
                                                continue

                                            command_position = command_position + 1

                                    else:
                                        WRITE_LOGFILE_SYSTEM("WARNING", "Program - " + program_name + " | " + check_result)

                                else:
                                    WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Device - " + device_name.strip() + " - not found")     
             
                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))


                    # ##################
                    # request sensordata
                    # ##################

                    if "request_sensordata" in line[1]:

                        line_content = line[1].split(" # ")

                        try:
                            REQUEST_SENSORDATA(line_content[1].strip())              

                        except Exception as e:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))


                    # ########
                    # programs
                    # ########

                    if "program" in line[1]:
                        
                        line_content = line[1].split(" # ")

                        program = GET_PROGRAM_BY_NAME(line_content[1].strip())

                        if program != None:

                            if line_content[2].strip() == "START":
                                START_PROGRAM_THREAD(program.id)
                                
                            elif line_content[2].strip() == "STOP":
                                STOP_PROGRAM_THREAD_BY_NAME(program.name, thread_id)

                            else:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | Invalid command")

                        else:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | Program - " + program + " - not found")


                    # #####
                    # music
                    # #####

                    if "music" in line[1]:
                            
                        line_content = line[1].split(" # ")

                        if GET_SPOTIFY_TOKEN() == "" and GET_SPOTIFY_REFRESH_TOKEN() != "":
                            GENERATE_SPOTIFY_TOKEN()

                        spotify_token = GET_SPOTIFY_TOKEN()

                        # check spotify login 
                        if spotify_token != "":
                            
                            try:
                                
                                sp       = spotipy.Spotify(auth=spotify_token)
                                sp.trace = False

                                # basic control 

                                if (line_content[1].strip() == "PLAY" or
                                    line_content[1].strip() == "PREVIOUS" or
                                    line_content[1].strip() == "NEXT" or
                                    line_content[1].strip() == "STOP" or
                                    line_content[1].strip() == "VOLUME"):
                                                    
                                    try: 
                                        spotify_volume = sp.current_playback(market=None)['device']['volume_percent']
                                    except:
                                        spotify_volume = GET_SPOTIFY_SETTINGS().default_volume

                                    if line_content[1].strip() == "PLAY":
                                        SPOTIFY_CONTROL(spotify_token, "play", spotify_volume)       
                            
                                    if line_content[1].strip() == "PREVIOUS":
                                        SPOTIFY_CONTROL(spotify_token, "previous", spotify_volume)   

                                    if line_content[1].strip() == "NEXT":
                                        SPOTIFY_CONTROL(spotify_token, "next", spotify_volume)     

                                    if line_content[1].strip() == "STOP": 
                                        SPOTIFY_CONTROL(spotify_token, "stop", spotify_volume)   

                                    if line_content[1].strip() == "VOLUME":            
                                        spotify_volume = int(line_content[2])
                                        SPOTIFY_CONTROL(spotify_token, "volume", spotify_volume)                  
                                                                                            
                                # start playlist
                                        
                                if line_content[1].strip() == "playlist":             
                                    
                                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, line_content[2].strip())
                                    playlist_uri      = GET_SPOTIFY_PLAYLIST(spotify_token, line_content[3].strip(), 20)
                                    playlist_volume   = int(line_content[4].strip())
                                    
                                    SPOTIFY_START_PLAYLIST(spotify_token, spotify_device_id, playlist_uri, playlist_volume)
                            
                                # start track
                                        
                                if line_content[1].strip() == "track":    

                                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, line_content[2].strip())
                                    track_uri         = SPOTIFY_SEARCH_TRACK(spotify_token, line_content[3].strip(), line_content[4].strip(), 1) [0][2]
                                    track_volume      = int(line_content[5].strip())
                                    
                                    SPOTIFY_START_TRACK(spotify_token, spotify_device_id, track_uri, track_volume)

                                # start album
                                        
                                if line_content[1].strip() == "album": 

                                    spotify_device_id = GET_SPOTIFY_DEVICE_ID(spotify_token, line_content[2].strip())
                                    album_uri         = SPOTIFY_SEARCH_ALBUM(spotify_token, line_content[3].strip(), line_content[4].strip(), 1) [0][2]
                                    album_volume      = int(line_content[5].strip())
                                    
                                    SPOTIFY_START_ALBUM(spotify_token, spotify_device_id, album_uri, album_volume)


                            except Exception as e:
                                WRITE_LOGFILE_SYSTEM("ERROR", "Program - " + program_name + " | Line - " + line[1] + " | " + str(e))
        
                                        
                        else:
                            WRITE_LOGFILE_SYSTEM("ERROR", "Programm - " + GET_PROGRAM_BY_ID(program_id).name + " | No Spotify Token found")   

                        
                    line_number = line_number + 1
                    time.sleep(1)


        # program regulary finished
        if thread_id == 1:
            SET_PROGRAM_THREAD_STATUS_1("None","","","")  
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 2:
            SET_PROGRAM_THREAD_STATUS_2("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 3:
            SET_PROGRAM_THREAD_STATUS_3("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 4:
            SET_PROGRAM_THREAD_STATUS_4("None","","","") 
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 5:
            SET_PROGRAM_THREAD_STATUS_5("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 6:
            SET_PROGRAM_THREAD_STATUS_6("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 7:
            SET_PROGRAM_THREAD_STATUS_7("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 8:
            SET_PROGRAM_THREAD_STATUS_8("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")

        if thread_id == 9:
            SET_PROGRAM_THREAD_STATUS_9("None","","","")   
            time.sleep(10)
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Program - " + program_name + " | finished")            


    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Programm - " + GET_PROGRAM_BY_ID(program_id).name + " | " + str(e))
        return str(e)