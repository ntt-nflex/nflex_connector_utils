from . import Resource


class Volume(Resource):
    """
        A representation of a volume. See

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            size_b (int): Optional size in bytes
            encrypted (bool): Optional, set to true if the volume is encrypted
            iops (int): Optional iops
            zone_name (str): Optional zone name
    """

    def __init__(self, size_b=None, encrypted=None, iops=None, zone_name=None,
                 **kwargs):
        super(Volume, self).__init__(type='volume', **kwargs)
        self.size_b = size_b
        self.encrypted = encrypted
        self.iops = iops
        self.zone_name = zone_name

    def serialize(self):
        """Serialize the contents"""

        data = super(Volume, self).serialize()

        iops = None
        if self.iops is not None:
            iops = int(self.iops)

        data['details'] = {
            self.type: {
                "encrypted": self.encrypted,
                "iops": iops,
                "size_b": self.size_b,
            }
        }

        if self.zone_name is not None:
            data['details']['zone_name'] = self.zone_name

        return data
