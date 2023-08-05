from datetime import datetime

from dateutil import parser, tz


def now():
    """
    Utility to get current datetime with local timezone data.
    :return: datetime object with current time and timezone
    """

    return datetime.now(tz=tz.tzlocal())


def parse(datetime_str):
    """
    Utility to parse datetime and timezone from string formatted as specified in AFM REST API.
    :param datetime_str: datetime string with timezone data e.g. '2012-04-23T18:25:43.511Z'
    :return: datetime object with timezone data
    """

    datetime = parser.parse(datetime_str)
    if not datetime.tzinfo:
        raise Exception("No time zone info in date time input!")
    return datetime


def format(dt):
    """
    Utility to format date as specified in AFM REST API.
    :param dt: datetime object to format
    :return:
    """
    return dt.isoformat()
