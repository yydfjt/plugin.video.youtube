__author__ = 'bromix'

from datetime import date, datetime, timedelta, time
import re

from .exceptions import KodionException


def parse(datetime_string):
    def _to_int(value):
        if value is None:
            return 0
        return int(value)

    # match time only '00:45:10'
    time_only_match = re.match('^(?P<hour>[0-9]{2})([:]?(?P<minute>[0-9]{2})([:]?(?P<second>[0-9]{2}))?)?$',
                               datetime_string)
    if time_only_match:
        return time(hour=_to_int(time_only_match.group('hour')),
                    minute=_to_int(time_only_match.group('minute')),
                    second=_to_int(time_only_match.group('second')))

    # match date only '2014-11-08'
    date_only_match = re.match('^(?P<year>[0-9]{4})[-]?(?P<month>[0-9]{2})[-]?(?P<day>[0-9]{2})$', datetime_string)
    if date_only_match:
        return date(_to_int(date_only_match.group('year')),
                    _to_int(date_only_match.group('month')),
                    _to_int(date_only_match.group('day')))

    # full date time
    date_time_match = re.match(
        "^(?P<year>[0-9]{4})[-]?(?P<month>[0-9]{2})[-]?(?P<day>[0-9]{2})[' ''T'](?P<hour>[0-9]{2})[:]?(?P<minute>[0-9]{2})[:]?(?P<second>[0-9]{2})",
        datetime_string)
    if date_time_match:
        return datetime(_to_int(date_time_match.group('year')),
                        _to_int(date_time_match.group('month')),
                        _to_int(date_time_match.group('day')),
                        _to_int(date_time_match.group('hour')),
                        _to_int(date_time_match.group('minute')),
                        _to_int(date_time_match.group('second')))

    # period - at the moment we support only hours, minutes and seconds (e.g. videos and audio)
    period_match = re.match(
        'P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<days>\d+)D)?(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?)?',
        datetime_string)
    if period_match:
        return timedelta(hours=_to_int(period_match.group('hours')),
                         minutes=_to_int(period_match.group('minutes')),
                         seconds=_to_int(period_match.group('seconds')))

    # abbreviated match
    abbreviated_match = re.match(
        r"(\w+), (?P<day>\d+) (?P<month>\w+) (?P<year>\d+) (?P<hour>\d+)\:(?P<minute>\d+)\:(?P<second>\d+)",
        datetime_string)
    if abbreviated_match:
        month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 'Jun': 6, 'July': 7, 'Jul': 7, 'Aug': 8,
                 'Sept': 9, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        return datetime(year=_to_int(abbreviated_match.group('year')),
                        month=month[abbreviated_match.group('month')],
                        day=_to_int(abbreviated_match.group('day')),
                        hour=_to_int(abbreviated_match.group('hour')),
                        minute=_to_int(abbreviated_match.group('minute')),
                        second=_to_int(abbreviated_match.group('second')))
        pass

    raise KodionException("Could not parse iso 8601 timestamp '%s'" % datetime_string)
