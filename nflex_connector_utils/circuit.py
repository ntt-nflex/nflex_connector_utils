from . import Resource


class Circuit(Resource):
    """
        A representation of a circuit.

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            type_id (str): Type ID (optional)
            carrier (str): Carrier (optional)
            reference(str): Circuit reference (optional)
            endpoint_a (str): One endpoint for the circuit (optional)
            endpoint_b (str): The other endpoint for the circuit (optional)
    """  # noqa

    def __init__(self, type_id=None, carrier=None, reference=None,
                 endpoint_a=None, endpoint_b=None, **kwargs):
        super(Circuit, self).__init__(type='circuit', **kwargs)
        self._type_id = type_id
        self._carrier = carrier
        self._reference = reference
        self._endpoint_a = endpoint_a
        self._endpoint_b = endpoint_b

    def serialize(self):
        """Serialize the contents"""

        data = super(Circuit, self).serialize()
        data['details'] = {
            self.type: {
                "type_id": self._type_id,
                "carrier": self._carrier,
                "reference": self._reference,
                "endpoint_a": self._endpoint_a,
                "endpoint_b": self._endpoint_b,
            }
        }
        return data
