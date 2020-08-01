from app                          import app
from app.backend.database_models  import *
from app.backend.file_management  import WRITE_LOGFILE_SYSTEM
from app.backend.tasks            import START_TASK

from ping3    import ping
from difflib  import SequenceMatcher
from croniter import croniter

import requests
import datetime


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

    if croniter.match(job.timedate, datetime.datetime.now()):
        return True
    else:
        return False


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

    def is_between(time, time_range):
        if time_range[1] < time_range[0]:
            return time >= time_range[0] or time <= time_range[1]

        return time_range[0] <= time <= time_range[1]

    # get current time
    now            = datetime.datetime.now()
    current_hour   = now.strftime('%H')
    current_minute = now.strftime('%M')

    try:
        if is_between(current_hour + ":" + current_minute, (GET_SCHEDULER_JOB_SUNRISE(job.id), GET_SCHEDULER_JOB_SUNSET(job.id))) == True:
            return True

        else:
            return False

    except:
        return False


def CHECK_SCHEDULER_NIGHT(job):

    def is_between(time, time_range):
        if time_range[1] < time_range[0]:
            return time >= time_range[0] or time <= time_range[1]

        return time_range[0] <= time <= time_range[1]

    # get current time
    now            = datetime.datetime.now()
    current_hour   = now.strftime('%H')
    current_minute = now.strftime('%M')

    try:
        if is_between(current_hour + ":" + current_minute, (GET_SCHEDULER_JOB_SUNSET(job.id), GET_SCHEDULER_JOB_SUNRISE(job.id))) == True:
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


# https://stackoverflow.com/questions/41072147/python-retrieve-the-sunrise-and-sunset-times-from-google

def GET_SUNRISE_TIME(lat, long):

    try:

        link     = "http://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0" % (lat, long)
        response = requests.get(link)
        data     = response.text

        # get sunrise data
        sunrise = data[34:42]
        sunrise = sunrise.split(":")

        sunrise_hour   = str(sunrise[0])
        sunrise_minute = str(sunrise[1])

        if len(sunrise_minute) == 1:
            sunrise_minute = str(0) + sunrise_minute

        sunrise = sunrise_hour + ":" + sunrise_minute

        return (sunrise)

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunrise | " + str(e))


def GET_SUNSET_TIME(lat, long):

    try:

        link     = "http://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0" % (lat, long)
        response = requests.get(link)
        data     = response.text

        # get sunset data
        sunset = data[71:79]
        sunset = sunset.split(":")

        sunset_hour   = str(sunset[0])
        sunset_minute = str(sunset[1])

        if len(sunset_minute) == 1:
            sunset_minute = str(0) + sunset_minute

        sunset = sunset_hour + ":" + sunset_minute

        return (sunset)

    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "Scheduler | Update Sunset | " + str(e))