from datetime import (
    datetime,
    timedelta,
)

_DEFAULT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
_DEFAULT_POLL_INTERVAL = 60 * 15  # 15 minutes


def setup_time_interval(event, backfill_time=0, interval=0,
                        skew=0, time_format=_DEFAULT_TIME_FORMAT):

    """
    sets up a time interval based on a combination of event data (last_update)
    and provider restriction (skew logic)

    Returns:
        (tuple):
            * start_time (datetime): interval start
            * end_time (datetime): interval end
            * info (str): info regarding usage of last_update and backfill_time to log if necessary to log out if necessary

    Args:

        event (dict): module's event that contains:

            * last_update (datetime): event's last_update which specifies the last time when data was fetched from provider
            * poll_interval (int): event's poll_interval in seconds which describes the time interval on when to fetch data from the provider (time of the execution - poll_interval)

        interval (int): additional interval parameter in seconds to add to existing poll interval when generating interval start time (optional)

        backfill_time (int): the time required in seconds to backfill to ensure no data is missed (optional)

        time_format (str): the time format used to parse last_update datetime optional and defaults to %Y-%m-%dT%H:%M:%S.%fZ format

        skew (int): time in seconds used to discount from end time (optional)

    Examples:
        set up time interval::

            event = {
                'last_update':datetime.utcnow(),
                'resource': {
                    'poll_interval': 15*60,
                },
            }

            output = setup_time_interval(
                event=event,
                backfill_time=3600,
                interval=5*60,
                skew=5*60,
            )

        parse and use the values::

            start_time, end_time, info = output
            print('time interval log: %s' % info)

    """  # noqa

    last_update = event.get('last_update', None)
    poll_interval = event['resource']. \
        get('poll_interval', _DEFAULT_POLL_INTERVAL)

    info = ''
    end_time = datetime.utcnow() - timedelta(seconds=skew)

    if last_update is None:
        start_time = end_time - timedelta(seconds=(poll_interval + interval))
        info += "no last_update specified and use %d mins prior to " \
                "now as start_time\n" \
                % ((poll_interval + skew) / 60)

    else:
        start_time = datetime.strptime(last_update, time_format)
        diff = (end_time - start_time).total_seconds()
        if diff > backfill_time:
            end_time = start_time + timedelta(seconds=backfill_time)
            info += "Backfilling start_time %s end_time %s" \
                    "\nMax backfill time is %s hours" \
                    % (start_time, end_time, backfill_time / 3600)

    return start_time, end_time, info
