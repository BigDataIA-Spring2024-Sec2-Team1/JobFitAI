'''
This file will be used across the project for using and defining constants, getting time, and some validation and conversion functions
'''

import datetime
import time
import pytz

def current_datetime():
    return datetime.datetime.now(pytz.timezone('America/New_York'))

def formatted_time():
    return datetime.datetime.strptime(str(current_datetime()).split('.')[0], '%Y-%m-%d %H:%M:%S')

def formatted_time_create(get_date):
    return datetime.datetime.strptime(str(get_date), '%Y-%m-%d %H:%M:%S')

def formatted_date_only(get_date):
    return datetime.datetime.strptime(str(get_date), '%Y-%m-%d %H:%M:%S')

def get_time(date_time):
    return datetime.datetime.strftime(datetime.datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S'), "%I:%M %p")

def get_date_time(date_time):
    try:
        return datetime.datetime.strftime(datetime.datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""

def get_timestamp_from_date(get_date):
    return str(int(time.mktime(formatted_time_create(get_date).timetuple())))

def get_timestamp():
    return str(int(time.mktime(formatted_time().timetuple())))

def later_one_hour():
    return formatted_time() - datetime.timedelta(0, 60 * 60)

def after():
    return formatted_time() + datetime.timedelta(0, 30 * 60)
