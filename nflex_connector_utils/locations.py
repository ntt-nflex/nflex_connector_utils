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
