class Metadata(object):
    DEFAULT_NAMESPACE_ID = 'default'
    PROVIDER_SPECIFIC_NAMESPACE_ID = 'provider_specific'
    PROVIDER_SPECIFIC_EDITABLE_NAMESPACE_ID = 'provider_specific_editable'
    PROVIDER_METADATA_NAMESPACE_ID = 'provider_metadata'

    def __init__(self, values=None, default_namespace=None):
        if default_namespace is None:
            default_namespace = self.PROVIDER_SPECIFIC_NAMESPACE_ID
        self.default_namespace = default_namespace
        self.data = {}

        if values is not None:
            for value in values:
                if len(value) == 2:
                    self.add(value[0], value[1])
                else:
                    self.add(value[1], value[2], namespace=value[0])

    def add(self, key, value, namespace=None):
        if namespace is None:
            namespace = self.default_namespace
        if namespace not in self.data:
            self.data[namespace] = {}
        self.data[namespace][key] = value
        return self

    def serialize(self):
        return self.data
