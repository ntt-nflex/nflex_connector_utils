class Connections(object):
    def __init__(self):
        self.data = {}

    def _add_type(self, type_, connections):
        if connections is None or len(connections) == 0:
            return

        if type_ not in self.data:
            self.data[type_] = []

        type_data = self.data[type_]
        for id_ in connections:
            type_data.append({'id': id_})

    def add(self, type=None, connections=None, appliances=None, servers=None,
            networks=None, volumes=None):
        if type is not None and connections is not None:
            self._add_type(type, connections)

        self._add_type('appliance', appliances)
        self._add_type('server', servers)
        self._add_type('network', networks)
        self._add_type('volume', volumes)

        return self

    def serialize(self):
        return self.data
