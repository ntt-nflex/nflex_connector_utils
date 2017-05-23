from dateutil import parser
import pytz
import six


def convert_datetime(dt):
    if dt is None or dt == '':
        return None
    if isinstance(dt, six.string_types):
        dt = parser.parse(dt)
    if dt.tzinfo:
        dt = dt.astimezone(pytz.utc).replace(tzinfo=None)
    if dt.microsecond > 0:
        dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return dt
