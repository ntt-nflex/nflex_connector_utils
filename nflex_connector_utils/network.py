from . import Resource


class Network(Resource):
    """
        A representation of a network

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
    """  # noqa

    def __init__(self, **kwargs):
        super(Network, self).__init__(type='network', **kwargs)

    def serialize(self):
        """Serialize the contents"""

        data = super(Network, self).serialize()
        data['details'] = {'network': {}}
        return data
