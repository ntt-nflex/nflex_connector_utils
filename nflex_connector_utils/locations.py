import six


class Region(object):
    """
        A representation of a region. When using this, the ``id`` is looked up
        in CMP and associated with a name and optional geographical data.

        Args:
            id (str): id
    """

    def __init__(self, id=None):
        self._id = id
        if self._id is None or not isinstance(self._id, six.string_types):
            raise ValueError('id must be a string and have a value')

    def serialize(self):
        """Serialize the contents"""

        return {'id': self._id}


class Locations(object):
    """
        A representation of a list of locations. Flexible in terms of what parts
        can be set based on the spec defined for locations.

        Args:
            locations (list): list of location dicts with keys as specified below:
            location (dict): keys id, name, latitude, longitude - optional
            city (dict): keys id, name, latitude, longitude - optional
            state (dict): keys id, name, latitude, longitude - optional
            country (dict): keys id, name, latitude, longitude - optional
            region (dict): keys id, name, latitude, longitude - optional
            type (str): one of 'customer' or 'provider' - optional

        Requirement for each lower level dict is:
            id (str)
            name (str) - one of id or name is required
            latitude (float) - optional
            longitude (float) - optional

        Example:
            This shows how to associate a paris location::

                locations = Locations([{
                    'country': {'name': 'France'},
                    'city': {'name': 'Paris'},
                    'location': {
                        'name': 'Legendary Paris Place',
                        'latitude': 48.860764,
                        'longitude': 2.393646,
                    }
                }])

                server = Server(
                    id='server-2',
                    name='Server with lots of details',
                    locations=locations
                )

    """  # noqa

    def __init__(self, locations=None):
        if locations is None:
            raise ValueError('locations must be a list of location hashes')
        self._data = []
        for location in locations:
            for attr in ('location', 'city', 'state', 'country', 'region'):
                if attr in location:
                    elem = location[attr]
                    if 'id' not in elem and 'name' not in elem:
                        raise ValueError('one of id or name must be specified')
                    if 'id' in elem and not isinstance(elem['id'],
                                                       six.string_types):
                        raise ValueError('id must be a string')
                    if 'name' in elem and not isinstance(elem['name'],
                                                         six.string_types):
                        raise ValueError('name must be a string')

            self._data.append(location)

    def serialize(self):
        """Serialize the contents"""

        return self._data
