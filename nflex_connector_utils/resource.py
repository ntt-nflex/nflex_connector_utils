from datetime import datetime
import six
from . import Connections
from . import Metadata
from . import convert_datetime


class Resource(object):
    """
        A representation of a resource. This contains all data common to all resources.

        Args:
            id (str): Unique identifier of this resource type. The ``(id, type)`` tuple uniquely identifies a resource.
            type (str): Type of a resource, e.g. ``server``, ``network``, ``volume``, ...
            name (str): Human readable name of the resource
            provider_created_at (str or datetime): An optional string or datetime object when the resource was created. This should never change.
            native_portal_link (str): An optional url to a page on a provider portal with details of the resource.
            region (:py:class:`nflex_connector_utils.locations.Region`): An optional :py:class:`nflex_connector_utils.locations.Region` object that associates the resource with a CMP location.
            connections (:py:class:`nflex_connector_utils.connections.Connections`)_: An optional :py:class:`nflex_connector_utils.connections.Connections` object
            metadata (:py:class:`nflex_connector_utils.metadata.Metadata`): An optional :py:class:`nflex_connector_utils.metadata.Metadata` object

    """  # noqa
    def __init__(self, id=None, name=None, type=None, region=None,
                 provider_created_at=None, metadata=None,
                 native_portal_link=None, connections=None):
        self.id = id
        self.name = name
        self.type = type
        self._check_not_none_str_value('id', self.id)
        self._check_not_none_str_value('name', self.name)
        self._check_not_none_str_value('type', self.type)

        self._provider_created_at = provider_created_at

        if connections is None:
            connections = Connections()
        self._connections = connections

        if metadata is None:
            metadata = Metadata()
        self._metadata = metadata
        self._region = region
        self._native_portal_link = native_portal_link

    def _check_not_none_str_value(self, name, value):
        if value is None or not isinstance(value, six.string_types):
            raise ValueError('%s must be a string and have a value' % name)

    def serialize(self):
        """Serialize the contents"""

        provider_created_at = convert_datetime(self._provider_created_at)

        regions = []
        if self._region is not None:
            regions = [self._region.serialize()]

        results = {
            "id": self.id,
            "type": self.type,
            "base": {
                "name": self.name,
                "regions": regions,
                "provider_created_at": provider_created_at,
                'last_seen_at': convert_datetime(datetime.utcnow()),
            },
            "connections": self._connections.serialize(),
            "metadata": self._metadata.serialize(),
        }

        if self._native_portal_link is not None:
            results['base']['native_portal_link'] = self._native_portal_link

        return results
