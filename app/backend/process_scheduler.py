from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.tasks            import START_TASK

from ping3          import ping
from croniter       import croniter
from timezonefinder import TimezoneFinder
from datetime       import date

import datetime
import astral


""" ################################ """
""" ################################ """
"""        scheduler process         """
""" ################################ """
""" ################################ """


def PROCESS_SCHEDULER(job, ieeeAddr):
    start_job = False

    # check time
    if job.trigger_timedate == "True":
        if CHECK_SCHEDULER_TIME(job) == False:
            return
        else:
            start_job = True

    # check sensors
    if job.trigger_sensors == "True":

        # find sensor jobs with fitting ieeeAddr only
        if (job.device_ieeeAddr_1 == ieeeAddr or job.device_ieeeAddr_2 == ieeeAddr):
            if CHECK_SCHEDULER_SENSORS(job) == False:
                return
            else:
                start_job = True

        else:
            return

    # check sun_position
    if job.trigger_sun_position == "True":

        if job.option_sunrise == "True":
            if CHECK_SCHEDULER_SUNRISE(job) == False:
                return
            else:
                start_job = True

        if job.option_sunset == "True":
            if CHECK_SCHEDULER_SUNSET(job) == False:
                return
            else:
                start_job = True

        if job.option_day == "True":
            if CHECK_SCHEDULER_DAY(job) == False:
                return
            else:
                start_job = True

        if job.option_night == "True":          
            if CHECK_SCHEDULER_NIGHT(job) == False:
                return
            else:
                start_job = True

    # check position
    if job.trigger_position == "True":

        if job.option_home == "True" or job.option_away == "True":
            ping_result = CHECK_SCHEDULER_PING(job)

            if job.option_home == "True" and ping_result == False:
                return
            elif job.option_away == "True" and ping_result == True:
                return
            else:
                start_job = True

    if start_job == True:
        START_TASK(job.task, "Scheduler", job.name)

        # remove scheduler job without repeat
        if job.option_repeat != "True":
            DELETE_SCHEDULER_JOB(job.id)


""" ################################ """
""" ################################ """
"""         scheduler checks         """
""" ################################ """
""" ################################ """


def CHECK_SCHEDULER_TIME(job):

    try:
        if croniter.match(job.timedate, datetime.datetime.now()):
            return True
        else:
            return False
    
    except:
        False


def CHECK_SCHEDULER_SUNRISE(job):

    # get current time
    now            = datetime.datetime.now()
    current_hour   = now.strftime('%H')
    current_minute = now.strftime('%M')

    # get sunrise time
    sunrise_data = GET_SCHEDULER_JOB_SUNRISE(job.id)

    try:
        sunrise_data = sunrise_data.split(":")

        if int(current_hour) == int(sunrise_data[0]) and int(current_minute) == int(sunrise_data[1]):
            return True

        else:
            return False

    except:
        return False


def CHECK_SCHEDULER_SUNSET(job):

    # get current time
    now            = datetime.datetime.now()
    current_hour   = now.strftime('%H')
    current_minute = now.strftime('%M')

    # get sunset time
    sunset_data = GET_SCHEDULER_JOB_SUNSET(job.id)

    try:
        sunset_data = sunset_data.split(":")

        if int(current_hour) == int(sunset_data[0]) and int(current_minute) == int(sunset_data[1]):
            return True

        else:
            return False

    except:
        return False


def CHECK_SCHEDULER_DAY(job):

    try:    

        sunrise = GET_SCHEDULER_JOB_SUNRISE(job.id).split(":")
        sunset  = GET_SCHEDULER_JOB_SUNSET(job.id).split(":")

        now_time = datetime.datetime.now().time()
        start    = datetime.time(int(sunrise[0]), int(sunrise[1]))
        end      = datetime.time(int(sunset[0]), int(sunset[1]))

        if start <= now_time <= end:
            return True
        else:
            return False

    except:
        return False


def CHECK_SCHEDULER_NIGHT(job):

    try:    

        sunset  = GET_SCHEDULER_JOB_SUNSET(job.id).split(":")
        sunrise = GET_SCHEDULER_JOB_SUNRISE(job.id).split(":")

        now_time = datetime.datetime.now().time()
        start    = datetime.time(int(sunset[0]), int(sunset[1]))
        end      = datetime.time(int(sunrise[0]), int(sunrise[1]))

        if now_time >= start or now_time <= end:
            return True
        else:
            return False

    except:
        return False


def CHECK_SCHEDULER_SENSORS(job):

    passing = False

    # #######
    # one row
    # #######

    if job.main_operator_second_sensor == "None" or job.main_operator_second_sensor == None:

        ##################
        # get sensordata 1
        ##################

        device_ieeeAddr_1 = job.device_ieeeAddr_1
        sensor_key_1      = job.sensor_key_1.strip()
        data_1            = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).last_values_json)
        sensor_value_1    = data_1[sensor_key_1]

        ####################
        # compare conditions
        ####################

        passing_1 = False

        if job.operator_1 == "=" and not job.value_1.isdigit():

            if str(sensor_value_1).lower() == str(job.value_1).lower():
                passing = True
            else:
                passing = False

        if job.operator_1 == "=" and job.value_1.isdigit():

            if int(sensor_value_1) == int(job.value_1):
                passing = True
            else:
                passing = False

        if job.operator_1 == "<" and job.value_1.isdigit():

            if int(sensor_value_1) < int(job.value_1):
                passing = True
            else:
                passing = False

        if job.operator_1 == ">" and job.value_1.isdigit():

            if int(sensor_value_1) > int(job.value_1):
                passing = True
            else:
                passing = False

    # ########
    # two rows
    # ########

    if job.main_operator_second_sensor != "None" and job.main_operator_second_sensor != None:


        ##################
        # get sensordata 1
        ##################

        device_ieeeAddr_1 = job.device_ieeeAddr_1
        sensor_key_1      = job.sensor_key_1.strip()
        data_1            = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_1).last_values_json)
        sensor_value_1    = data_1[sensor_key_1]


        ##################
        # get sensordata 2
        ##################

        device_ieeeAddr_2 = job.device_ieeeAddr_2
        sensor_key_2      = job.sensor_key_2.strip()
        data_2            = json.loads(GET_DEVICE_BY_IEEEADDR(device_ieeeAddr_2).last_values_json)
        sensor_value_2    = data_2[sensor_key_2]


        ####################
        # compare conditions
        ####################

        passing_1 = False
        passing_2 = False

        # Options: <, >, =

        if job.main_operator_second_sensor == ">" or job.main_operator_second_sensor == "<" or job.main_operator_second_sensor == "=":

            if job.main_operator_second_sensor == "=":
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

            if job.main_operator_second_sensor == "<":

                if int(sensor_value_1) < int(sensor_value_2):
                    passing = True
                else:
                    passing = False

            if job.main_operator_second_sensor == ">":

                if int(sensor_value_1) > int(sensor_value_2):
                    passing = True
                else:
                    passing = False

        # Options: and, or

        if job.main_operator_second_sensor == "and" or job.main_operator_second_sensor == "or":

            # get passing value one

            passing_1 = False

            try:
                if job.operator_1 == "=" and not job.value_1.isdigit():

                    if str(sensor_value_1).lower() == str(job.value_1).lower():
                        passing_1 = True
                    else:
                        passing_1 = False
            except:
                pass

            try:
                if job.operator_1 == "=" and job.value_1.isdigit():

                    if int(sensor_value_1) == int(job.value_1):
                        passing_1 = True
                    else:
                        passing_1 = False
            except:
                pass

            try:
                if job.operator_1 == "<" and job.value_1.isdigit():

                    if int(sensor_value_1) < int(job.value_1):
                        passing_1 = True
                    else:
                        passing_1 = False
            except:
                pass

            try:
                if job.operator_1 == ">" and job.value_1.isdigit():

                    if int(sensor_value_1) > int(job.value_1):
                        passing_1 = True
                    else:
                        passing_1 = False
            except:
                pass

            # get passing value two

            passing_2 = False

            try:
                if job.operator_2 == "=" and not job.value_2.isdigit():

                    if str(sensor_value_2).lower() == str(job.value_2).lower():
                        passing_2 = True
                    else:
                        passing_2 = False
            except:
                pass

            try:
                if job.operator_2 == "=" and job.value_2.isdigit():

                    if int(sensor_value_2) == int(job.value_2):
                        passing_2 = True
                    else:
                        passing_2 = False
            except:
                pass

            try:
                if job.operator_2 == "<" and job.value_2.isdigit():

                    if int(sensor_value_2) < int(job.value_2):
                        passing_2 = True
                    else:
                        passing_2 = False
            except:
                pass

            try:
                if job.operator_2 == ">" and job.value_2.isdigit():

                    if int(sensor_value_2) > int(job.value_2):
                        passing_2 = True
                    else:
                        passing_2 = False
            except:
                pass

            # get result

            if job.main_operator_second_sensor == "and":

                if passing_1 == True and passing_2 == True:
                    passing = True
                else:
                    passing = False

            if job.main_operator_second_sensor == "or":

                if passing_1 == True or passing_2 == True:
                    passing = True
                else:
                    passing = False


    return passing


def CHECK_SCHEDULER_PING(job):

    ip_addresses = job.ip_addresses.split(",")

    for ip_address in ip_addresses:

        for x in range(5):
            if ping(ip_address, timeout=1) != None:
                return True

    return False


""" ################################ """
""" ################################ """
"""         sunrise / sunset         """
""" ################################ """
""" ################################ """


def GET_SUNRISE_TIME(longitude, latitude):

    try:

        # get timezone
        obj      = TimezoneFinder()
        timezone = obj.timezone_at(lng=longitude, lat=latitude)

        # get sunposition
        loc = astral.Location(('', '', longitude, latitude, timezone, 510))

        for event in loc.sun(date.today()).items():
            if event[0] == "dawn":
                sunrise = str(event[1].hour + 1) + ":" + str(event[1].minute)

        return (sunrise)

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunrise | " + str(e))


def GET_SUNSET_TIME(longitude, latitude):

    try:

        # get timezone
        obj      = TimezoneFinder()
        timezone = obj.timezone_at(lng=longitude, lat=latitude)

        # get sunposition
        loc = astral.Location(('', '', longitude, latitude, timezone, 510))

        for event in loc.sun(date.today()).items():
            if event[0] == "sunset":
                sunset = str(event[1].hour - 1) + ":" + str(event[1].minute)

        return (sunset)

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunset | " + str(e))