import six


class Region(object):
    def __init__(self, id=None):
        self.id = id
        if self.id is None or not isinstance(self.id, six.string_types):
            raise ValueError('id must be a string and have a value')

    def serialize(self):
        return {'id': self.id}
