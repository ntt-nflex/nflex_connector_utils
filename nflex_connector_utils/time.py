from datetime import (
    datetime,
    timedelta,
)

_DEFAULT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
_DEFAULT_POLL_INTERVAL = 60 * 15  # 15 minutes


def setup_time_interval(event, backfill_time=None, initial_interval=0,
                        skew=0, time_format=_DEFAULT_TIME_FORMAT, logger=None):

    """
    sets up a time interval based on a combination of event data (last_update)
    and provider restriction (skew logic)

    Returns:
        (tuple):
            * start_time (datetime): interval start
            * end_time (datetime): interval end

    Args:

        event (dict): module's event that contains:

            * last_update (datetime): event's last_update which specifies the last time when data was fetched from provider
            * poll_interval (int): event's poll-interval in seconds which describes the time interval on when to fetch data from the provider (time of the execution - poll_interval)

        initial_interval (int): additional interval parameter in seconds to add to existing poll interval when generating interval start time (optional)

        backfill_time (int): the time required in seconds to backfill to ensure no data is missed (optional)

        time_format (str): the time format used to parse last_update datetime optional and defaults to %Y-%m-%dT%H:%M:%S.%fZ format

        skew (int): time in seconds used to discount from end time (optional)

        logger (option): nflex connector util's :class:`~nflex_connector_utils.logger` that allows to log info regarding usage of last_update and backfill_time


    Examples:
        set up time interval::

            event = {
                'last_update':datetime.utcnow(),
                'resource': {
                    'poll_interval': 15*60,
                },
            }

        (optional) set up logger::

            # get these values from nflex handler which has event and context
            logger = Logger(
                context=context,
                customer_id=customer_id
                account_id=account_id,
                resource_id=resource_id,
            )

        setup time interval::

            output = setup_time_interval(
                event=event,
                backfill_time=3600,
                initial_interval=5*60,
                skew=5*60,
                logger=logger,
            )

        parse and use the values::

            start_time, end_time = output

    """  # noqa

    last_update = event.get('last_update', None)
    poll_interval = event['resource']. \
        get('poll-interval', _DEFAULT_POLL_INTERVAL)

    info = ''
    end_time = datetime.utcnow() - timedelta(seconds=skew)

    if last_update is None:
        start_time = end_time - timedelta(
            seconds=(poll_interval + initial_interval)
        )
        info += "no last_update specified and use %d mins prior to " \
                "now as start_time\n" \
                % ((poll_interval + skew) / 60)

    else:
        start_time = datetime.strptime(last_update, time_format)
        diff = (end_time - start_time).total_seconds()
        if backfill_time and diff > backfill_time:
            end_time = start_time + timedelta(seconds=backfill_time)
            info += "Backfilling start_time %s end_time %s" \
                    "\nMax backfill time is %s hours" \
                    % (start_time, end_time, backfill_time / 3600)

        if logger:
            logger.info(info)

    return start_time, end_time
