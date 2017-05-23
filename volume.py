from . import Resource


class Volume(Resource):
    def __init__(self, size_b=None, encrypted=None, iops=None, zone_name=None,
                 **kwargs):
        super(Volume, self).__init__(type='volume', **kwargs)
        self.size_b = size_b
        self.encrypted = encrypted
        self.iops = iops
        self.zone_name = zone_name

    def serialize(self):
        data = super(Volume, self).serialize()

        iops = None
        if self.iops is not None:
            iops = int(self.iops)

        data['details'] = {
            self.type: {
                "encrypted": self.encrypted,
                "iops": iops,
                "size_b": self.size_b,
                "zone_name": self.zone_name,
            }
        }
        return data
