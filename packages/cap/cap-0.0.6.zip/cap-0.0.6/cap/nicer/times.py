__author__ = 'netanelrevah'

from datetime import datetime, timedelta
import time


def current_datetime():
    return datetime.now()


def seconds_from_datetime(value):
    """
    :type value: datetime
    """
    return int(time.mktime(value.timetuple()))


def microseconds_from_datetime(value):
    """
    :type value: datetime
    """
    return value.microsecond


def seconds_from_timedelta(value):
    """
    :type value: timedelta
    """
    return .0 + value.days * 24 * 60 * 60 + value.seconds + value.microseconds / 100000.


def hours_from_timedelta(value):
    """
    :type value: timedelta
    """
    return seconds_from_timedelta(value) / 60


def hours_delta(hours):
    if isinstance(hours, int):
        hours = timedelta(hours=hours)
    if not isinstance(hours, timedelta):
        raise TypeError("Not Supported Type!")
    return hours


def datetime_from_timestamp(value):
    return datetime.fromtimestamp(value)


def datetime_from_seconds_and_microseconds(seconds, microseconds):
    return datetime.fromtimestamp(seconds) + timedelta(microseconds=microseconds)
