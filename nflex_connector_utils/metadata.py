class Metadata(object):
    """
        A representation of an resource metadata. Metadata can be set directly by using ``Metadata()`` or added piece by piece by using the ``add()`` method.

        Args:
            values (list): An optional list of 2 or 3 element tuples. 2-element tuples have ``(key, value)`` and 3-element tuples have ``(namespace, key, value)``.
            default_namespace (str): Optional default namespace. This defaults to ``provider_specific``.

        Examples:
            Create two metadata key/values in the default ``provider_specific`` namespace::

                Metadata([('key1', 'value1'), ('key2', 'value2')])

            Create two metadata key/values in an ``alt-ns`` namespace::

                Metadata([('alt-ns', 'key1', 'value1'), ('alt-ns', 'key2', 'value2')])

            Add metadata using the ``add()`` method::

                m = Metadata()
                m.add('key1', 'value1').add('key2', 'value2', namespace='alt-ns')

    """  # noqa

    DEFAULT_NAMESPACE_ID = 'default'
    PROVIDER_SPECIFIC_NAMESPACE_ID = 'provider_specific'
    PROVIDER_SPECIFIC_EDITABLE_NAMESPACE_ID = 'provider_specific_editable'
    PROVIDER_METADATA_NAMESPACE_ID = 'provider_metadata'

    def __init__(self, values=None, default_namespace=None):
        if default_namespace is None:
            default_namespace = self.PROVIDER_SPECIFIC_NAMESPACE_ID
        self._default_namespace = default_namespace
        self._data = {}

        if values is not None:
            for value in values:
                if len(value) == 2:
                    self.add(value[0], value[1])
                else:
                    self.add(value[1], value[2], namespace=value[0])

    def add(self, key, value, namespace=None):
        """
            Add metadata

        Args:
            key (str): key
            value (str): value
            namespace (str): Optional namespace. If not included, the ``default_namespace`` is used which defaults to ``provider_specific``.

        Returns:
            :py:class:`nflex_connector_utils.metadata.Metadata`: returns itself, so that ``add`` methods can be chained
        """  # noqa

        if namespace is None:
            namespace = self._default_namespace
        if namespace not in self._data:
            self._data[namespace] = {}
        self._data[namespace][key] = value
        return self

    def serialize(self):
        """Serialize the contents"""

        return self._data
