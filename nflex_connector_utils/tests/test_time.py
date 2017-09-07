from nflex_connector_utils.time import (
    setup_time_interval
)

from datetime import (
    datetime,
    timedelta,
)

from unittest import TestCase
from freezegun import freeze_time


@freeze_time('2017-09-06 06:21:34')
class TestSetupTimeInterval(TestCase):
    def test_time_interval(self):
        time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        now = datetime.utcnow()

        o1 = setup_time_interval(
                last_update=now.strftime(time_format),
                poll_interval=15*60,
                backfill_time=3600,
                interval=5*60,
                skew=10*60,
        )

        self.assertEqual(o1['start_time'], now)
        self.assertEqual(
            o1['end_time'],
            now - timedelta(seconds=10*60),
        )
        self.assertEqual(o1['debug'], '')

        o2 = setup_time_interval(
                last_update=None,
                poll_interval=25*60,
                backfill_time=3600,
                interval=11*60,
        )

        self.assertEqual(
            o2['start_time'],
            now - timedelta(seconds=25*60 + 11*60)
        )
        self.assertEqual(o2['end_time'], now)
        self.assertNotEqual(o2['debug'], '')

        o3 = setup_time_interval(
                last_update=(now - timedelta(hours=2)).strftime(time_format),
                poll_interval=25*60,
                backfill_time=3600,
                interval=11*60,
        )

        self.assertEqual(o3['start_time'], now - timedelta(hours=2))
        self.assertEqual(o3['end_time'], now - timedelta(seconds=3600))
        self.assertNotEqual(o3['debug'], '')
