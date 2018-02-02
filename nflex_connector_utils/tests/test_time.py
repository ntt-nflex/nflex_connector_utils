from nflex_connector_utils.time import (
    setup_time_interval
)

from datetime import (
    datetime,
    timedelta,
)

from unittest import TestCase
from freezegun import freeze_time

_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


@freeze_time('2017-09-06 06:21:34')
class TestSetupTimeInterval(TestCase):
    def test_time_nflex_interval(self):
        now = datetime.utcnow()

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': now.strftime(_TIME_FORMAT),
                    'poll_interval': 15*60,
                },
                backfill_time=3600,
                initial_interval=5*60,
                skew=10*60,
        )

        self.assertEqual(start_time, now)
        self.assertEqual(end_time, now - timedelta(seconds=10*60))

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': None,
                    'poll_interval': 25*60,
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(seconds=25*60 + 11*60))
        self.assertEqual(end_time, now)

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': None,
                    'poll_interval': 25,
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(seconds=25 + 11*60))
        self.assertEqual(end_time, now)

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': None,
                    'poll_interval': 60*60,
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(seconds=60*60 + 11*60))
        self.assertEqual(end_time, now)

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': (now - timedelta(hours=2)).strftime(
                        _TIME_FORMAT
                    ),
                    'poll_interval': 25*60
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(hours=2))
        self.assertEqual(end_time, now - timedelta(seconds=3600))

    def test_time_interval(self):
        now = datetime.utcnow()

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': now.strftime(_TIME_FORMAT),
                    'resource': {
                        'poll_interval': 15*60,
                    },
                },
                backfill_time=3600,
                initial_interval=5*60,
                skew=10*60,
        )

        self.assertEqual(start_time, now)
        self.assertEqual(end_time, now - timedelta(seconds=10*60))

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': None,
                    'resource': {
                        'poll_interval': 25*60,
                    },
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(seconds=25*60 + 11*60))
        self.assertEqual(end_time, now)

        start_time, end_time = setup_time_interval(
                event={
                    'last_update': (now - timedelta(hours=2)).strftime(
                        _TIME_FORMAT
                    ),
                    'resource': {
                        'poll_interval': 25*60,
                    },
                },
                backfill_time=3600,
                initial_interval=11*60,
        )

        self.assertEqual(start_time, now - timedelta(hours=2))
        self.assertEqual(end_time, now - timedelta(seconds=3600))
