from . import Resource


class Network(Resource):
    def __init__(self, **kwargs):
        super(Network, self).__init__(type='network', **kwargs)

    def serialize(self):
        data = super(Network, self).serialize()
        data['details'] = {'network': {}}
        return data
