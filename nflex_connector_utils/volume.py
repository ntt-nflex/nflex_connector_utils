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
    """  # noqa

    def __init__(self, size_b=None, encrypted=None, iops=None, zone_name=None,
                 **kwargs):
        super(Volume, self).__init__(type='volume', **kwargs)
        self._size_b = size_b
        self._encrypted = encrypted
        self._iops = iops
        self._zone_name = zone_name

    def serialize(self):
        """Serialize the contents"""

        data = super(Volume, self).serialize()

        iops = None
        if self._iops is not None:
            iops = int(self._iops)

        data['details'] = {
            self.type: {
                "encrypted": self._encrypted,
                "iops": iops,
                "size_b": self._size_b,
            }
        }

        if self._zone_name is not None:
            data['details']['volume']['zone_name'] = self._zone_name

        return data
