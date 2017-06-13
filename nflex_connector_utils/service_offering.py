from . import Resource


class ServiceOffering(Resource):
    """
        A representation of a service offering

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            type_id: Type of service offering. Free text.

    """  # noqa

    def __init__(self, type_id=None, **kwargs):
        super(ServiceOffering, self).__init__(type='service_offering',
                                              **kwargs)
        self._type_id = type_id

    def serialize(self):
        """Serialize the contents"""

        data = super(ServiceOffering, self).serialize()

        data['details'] = {
            self.type: {
                "type_id": self._type_id,
            }
        }

        return data
