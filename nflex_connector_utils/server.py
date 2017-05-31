from . import Resource


class Server(Resource):
    """
        A representation of a server

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            cpu_hz (int): Optional CPU Speed in Hz
            cpu_cores (int): Optional number of CPU cores
            ram_b (int): Optional RAM size in bytes
            volumes_b: Optional  total volume size in bytes
            state: CMP state. Must be one of: ``unknown``, ``pending``, ``running``, ``shutting``, ``terminated``, ``stopping``, ``stopped``,
            provider_state (str): Optional provider description of the state, can be any text.
            instance_type (str): Optional text value describing the instance type
            is_virtual (bool): Optional, set to ``True`` if the server is physical. Defaults to ``False``.
            image_detail (:py:class:`nflex_connector_utils.image_detail.ImageDetail`): An optional :py:class:`nflex_connector_utils.image_detail.ImageDetail` object
            ip_addresses (:py:class:`nflex_connector_utils.ip_address.IpAddress`): An optional :py:class:`nflex_connector_utils.ip_address.IpAddress` object


    """  # noqa

    def __init__(self, cpu_hz=None, cpu_cores=None, ram_b=None, volumes_b=None,
                 state=None, provider_state=None, image_detail=None,
                 instance_type=None, ip_addresses=None,
                 is_virtual=None, **kwargs):
        super(Server, self).__init__(type='server', **kwargs)
        self._cpu_cores = cpu_cores
        self._cpu_hz = cpu_hz
        self._ram_b = ram_b
        self._volumes_b = volumes_b
        self._is_virtual = is_virtual

        if state is None:
            state = 'unknown'
        self._state = state

        if provider_state is None:
            provider_state = 'unknown'
        self._provider_state = provider_state

        self._instance_type = instance_type
        self._image_detail = image_detail

        if ip_addresses is None:
            ip_addresses = []
        self._ip_addresses = ip_addresses

    def serialize(self):
        """Serialize the contents"""

        data = super(Server, self).serialize()

        ip_addresses = [ip.serialize() for ip in self._ip_addresses]

        data['details'] = {
            self.type: {
                "cpu_cores": self._cpu_cores,
                "cpu_hz": self._cpu_hz,
                "ram_b": self._ram_b,
                "volumes_b": self._volumes_b,
                "instance_type": self._instance_type,
                "state": self._state,
                "provider_state": self._provider_state,
                "ip_addresses": ip_addresses,
            }
        }

        type_details = data['details'][self.type]

        if self._image_detail is not None:
            type_details['image_detail'] = self._image_detail.serialize()
        else:
            type_details['image_detail'] = None

        if self._is_virtual is not None:
            type_details['is_virtual'] = self._is_virtual

        return data
