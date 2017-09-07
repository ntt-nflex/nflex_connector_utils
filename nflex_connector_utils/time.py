from datetime import (
    datetime,
    timedelta,
)

_DEFAULT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def setup_time_interval(last_update, poll_interval, backfill_time, interval=0,
                        skew=0, time_format=_DEFAULT_TIME_FORMAT):

    """
    sets up a time interval based on a combination of event data (last_update)
    and provider restriction (skew logic)

    :return: dict: start_time, end_time as datetime and debug with information
    regarding usage of last_update and backfill_time to log if necessary
    :rtype: dict

    Args:
        last_update (datetime): event's last_update which specifies the last time
        when data was fetched from provider
        poll_interval (int): event's poll_interval in seconds which describes
        the time interval on when to fetch data from the provider
        (time of the execution - poll_interval)
        interval (int): additional interval parameter in seconds to add to
        existing poll interval when generating interval start time (optional)
        backfill_time (int): the time required in seconds to backfill to
        ensure no data is missed
        time_format (str): the time format used to parse last_update datetime
        optional and defaults to %Y-%m-%dT%H:%M:%S.%fZ format
        skew (int): time in seconds used to discount from end time (optional)

    Examples:
        set up time interval::

            output = setup_time_interval(
                last_update=datetime.utcnow(),
                poll_interval=15*60,
                backfill_time=3600,
                interval=5*60,
                skew=5*60,
            )

        parse and use the values::

            start_time = output['start_time']
            end_time = output['end_time']

            print('time interval log: %s' % output['debug'])

    """  # noqa

    debug = ''
    end_time = datetime.utcnow() - timedelta(seconds=skew)

    if last_update is None:
        start_time = end_time - timedelta(seconds=(poll_interval + interval))
        debug += "no last_update specified and use %d mins prior to " \
                 "now as start_time\n" \
                 % ((poll_interval + skew) / 60)

    else:
        start_time = datetime.strptime(last_update, time_format)
        diff = (end_time - start_time).total_seconds()
        if diff > backfill_time:
            end_time = start_time + timedelta(seconds=backfill_time)
            debug += "Backfilling start_time %s end_time %s" \
                     "\nMax backfill time is %s hours" \
                     % (start_time, end_time, backfill_time / 3600)

    return {
        'start_time': start_time,
        'end_time': end_time,
        'debug': debug,
    }
