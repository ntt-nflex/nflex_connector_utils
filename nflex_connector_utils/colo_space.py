from . import Resource


class ColoSpace(Resource):
    """
        A representation of a colo space.

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            power_allocation_w (int): Power Allocation in W (optional)
            type_id (str): Type ID (optional)
            colo_space_location (str): Location (optional)
            customer_name (str): Customer Name (optional)
            customer_label (str): Customer Label (optional)
            customer_description (str): Customer Description (optional)
            combination (str): Combination (optional)
    """  # noqa

    def __init__(self, power_allocation_w=None, type_id=None,
                 colo_space_location=None, customer_name=None,
                 customer_label=None, customer_description=None,
                 combination=None, **kwargs):
        super(ColoSpace, self).__init__(type='colo_space', **kwargs)
        self._power_allocation_w = power_allocation_w
        self._type_id = type_id
        self._colo_space_location = colo_space_location
        self._customer_name = customer_name
        self._customer_label = customer_label
        self._customer_description = customer_description
        self._combination = combination

    def serialize(self):
        """Serialize the contents"""

        data = super(ColoSpace, self).serialize()
        data['details'] = {
            self.type: {
                "power_allocation_w": self._power_allocation_w,
                "type_id": self._type_id,
                "colo_space_location": self._colo_space_location,
                "customer_name": self._customer_name,
                "customer_label": self._customer_label,
                "customer_description": self._customer_description,
                "combination": self._combination
            }
        }
        return data
