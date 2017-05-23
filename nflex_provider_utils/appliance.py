from . import Resource


class Appliance(Resource):
    def __init__(self, size_b=None, type_id=None, **kwargs):
        super(Appliance, self).__init__(type='appliance', **kwargs)
        self.type_id = type_id

    def serialize(self):
        data = super(Appliance, self).serialize()
        data['details'] = {
            self.type: {
                "type_id": self.type_id
            }
        }
        return data
