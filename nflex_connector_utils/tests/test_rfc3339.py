import pytz
from datetime import datetime

from nflex_connector_utils import convert_datetime


class TestRFC3339(object):
    def test_rfc_3339(self):
        def cdt(*args):
            return convert_datetime(*args)

        assert cdt(None) is None
        assert cdt('') is None
        assert cdt('1970-01-01') == '1970-01-01T00:00:00Z'
        assert cdt('1970-01-01T00:00:00Z') == '1970-01-01T00:00:00Z'
        assert cdt('2017-01-01T00:00:00+10') == '2016-12-31T14:00:00Z'
        assert cdt('1970-01-01T00:00:00.10Z') == '1970-01-01T00:00:00.100000Z'

        assert cdt(datetime(2017, 1, 1)) == '2017-01-01T00:00:00Z'

        naive_dt = datetime(2013, 9, 3, 16, 0)
        dt = pytz.timezone("Europe/Paris").localize(naive_dt, is_dst=None)
        assert cdt(dt) == '2013-09-03T14:00:00Z'
