import pytest

from nflex_connector_utils import Region


class TestRegion(object):
    def test_region(self):
        with pytest.raises(ValueError):
            Region()

        assert Region(id='foo').serialize() == {'id': 'foo'}
