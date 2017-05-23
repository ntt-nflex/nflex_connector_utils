from datetime import datetime
import six
from . import Connections
from . import Metadata
from . import convert_datetime


class Resource(object):
    def __init__(self, id=None, name=None, type=None, region=None,
                 provider_created_at=None, metadata=None,
                 native_portal_link=None, connections=None):
        self.id = id
        self.name = name
        self.type = type
        self._check_not_none_str_value('id', self.id)
        self._check_not_none_str_value('name', self.name)
        self._check_not_none_str_value('type', self.type)

        self.provider_created_at = provider_created_at

        if connections is None:
            connections = Connections()
        self.connections = connections

        if metadata is None:
            metadata = Metadata()
        self.metadata = metadata
        self.region = region
        self.native_portal_link = native_portal_link

    def _check_not_none_str_value(self, name, value):
        if value is None or not isinstance(value, six.string_types):
            raise ValueError('%s must be a string and have a value' % name)

    def serialize(self):
        provider_created_at = convert_datetime(self.provider_created_at)

        regions = []
        if self.region is not None:
            regions = [self.region.serialize()]

        results = {
            "id": self.id,
            "type": self.type,
            "base": {
                "name": self.name,
                "regions": regions,
                "provider_created_at": provider_created_at,
                'last_seen_at': convert_datetime(datetime.utcnow()),
            },
            "connections": self.connections.serialize(),
            "metadata": self.metadata.serialize(),
        }

        if self.native_portal_link is not None:
            results['base']['native_portal_link'] = self.native_portal_link

        return results
