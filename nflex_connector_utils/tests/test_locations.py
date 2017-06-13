import pytest

from nflex_connector_utils import Region, Locations


class TestRegion(object):
    def test_region(self):
        with pytest.raises(ValueError):
            Region()

        assert Region(id='foo').serialize() == {'id': 'foo'}


class TestLocations(object):
    def test_locations(self):
        with pytest.raises(ValueError):
            Locations()

        with pytest.raises(ValueError):
            Locations(locations=[{'location': {'foo': 'bar'}}])

        with pytest.raises(ValueError):
            Locations(locations=[{'location': {'id': 1}}])

        with pytest.raises(ValueError):
            Locations(locations=[{'location': {'name': 1}}])

        test_locations = [
            {'location': {'id': 'location1'}},
            {'location': {'id': 'location_id', 'name': 'location_name'}},
            {'location': {'id': 'location1'}, 'region': {'id': 'region1'},
             'city': {'id': 'city1'}, 'state': {'id': 'state1'},
             'country': {'id': 'country1'}},
        ]
        for test_location in test_locations:
            assert Locations(locations=[test_location]).serialize() == \
                [test_location]
        assert Locations(locations=test_locations).serialize() == \
            test_locations
