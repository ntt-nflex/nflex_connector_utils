from . import Resource


class Appliance(Resource):
    """
        A representation of an appliance.

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            type_id (str): one of ``firewall``, ``load_balancer``, ``router``, ``switch``, ``storage``, ``kvm``, ``unknown``
    """  # noqa

    def __init__(self, size_b=None, type_id=None, **kwargs):
        super(Appliance, self).__init__(type='appliance', **kwargs)
        self._type_id = type_id

    def serialize(self):
        """Serialize the contents"""

        data = super(Appliance, self).serialize()
        data['details'] = {
            self.type: {
                "type_id": self._type_id
            }
        }
        return data
