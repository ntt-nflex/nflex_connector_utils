from . import Resource


class Server(Resource):
    def __init__(self, cpu_hz=None, cpu_cores=None, ram_b=None, volumes_b=None,
                 state=None, provider_state=None, image_detail=None,
                 instance_type=None, ip_addresses=None,
                 is_virtual=None, **kwargs):
        super(Server, self).__init__(type='server', **kwargs)
        self.cpu_cores = cpu_cores
        self.cpu_hz = cpu_hz
        self.ram_b = ram_b
        self.volumes_b = volumes_b
        self.is_virtual = is_virtual

        if state is None:
            state = 'unknown'
        self.state = state

        if provider_state is None:
            provider_state = 'unknown'
        self.provider_state = provider_state

        self.instance_type = instance_type
        self.image_detail = image_detail

        if ip_addresses is None:
            ip_addresses = []
        self.ip_addresses = ip_addresses

    def serialize(self):
        data = super(Server, self).serialize()

        ip_addresses = [ip.serialize() for ip in self.ip_addresses]

        data['details'] = {
            self.type: {
                "cpu_cores": self.cpu_cores,
                "cpu_hz": self.cpu_hz,
                "ram_b": self.ram_b,
                "volumes_b": self.volumes_b,
                "instance_type": self.instance_type,
                "state": self.state,
                "provider_state": self.provider_state,
                "ip_addresses": ip_addresses,
            }
        }

        type_details = data['details'][self.type]

        if self.image_detail is not None:
            type_details['image_detail'] = self.image_detail.serialize()
        else:
            type_details['image_detail'] = None

        if self.is_virtual is not None:
            type_details['is_virtual'] = self.is_virtual

        return data
