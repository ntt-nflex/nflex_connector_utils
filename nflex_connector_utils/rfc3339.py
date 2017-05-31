from dateutil import parser
import pytz
import six


def convert_datetime(dt):
    """
        Convert a datetime or timestamp string to an RFC 3339 timestamp. A
        ``None`` is returned as a ``None``.

        Args:
            dt (str, datetime or None): Input. This can be a string timestamp to be parsed, a datetime object or a ``None``.

        Returns:
            str: A RFC 3339 timestamp
    """  # noqa

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
