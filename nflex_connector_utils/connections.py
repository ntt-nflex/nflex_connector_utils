class Connections(object):
    """
        A representation of inter-resource associations.

        Args:
            type (str): The type of resource to add connections to, e.g. ``server``
            connections (list): When used together with ``type``, a list of associated resource ids
                                or dicts
            appliances (list): an optional list of appliance ids
            servers (list): an optional list of server ids
            networks (list): an optional list of network ids
            volumes (list): an optional list of volume ids

        Examples:
            Create a bunch of connections to a server::

                Connections(type='server', connections=['server-1', 'server-2'])

            Create a connection to two volumes and a network::

                Connections(networks=['network-1'], volumes=['volume-1', 'volume-2'])

            Incrementally add connections::

                c = Connections()
                c.add(type='appliances', connections='appliance-1').add(servers=['server-1'])
                c.add(networks=['network-1'])

    """  # noqa

    def __init__(self, type=None, connections=None, appliances=None,
                 servers=None, networks=None, volumes=None):
        self._data = {}
        self.add(type=type, connections=connections, appliances=appliances,
                 servers=servers, networks=networks, volumes=volumes)

    def _add_type(self, type_, connections):
        if connections is None or len(connections) == 0:
            return

        if type_ not in self._data:
            self._data[type_] = []

        type_data = self._data[type_]
        for id_ in connections:
            if type_ == 'any':
                type_data.append(id_)
            else:
                type_data.append({'id': id_})

    def add(self, type=None, connections=None, appliances=None, servers=None,
            networks=None, volumes=None):
        """
            Add a connection

            Args:
                type (str): The type of resource to add connections to, e.g. ``server``
                connections (str): When used together with ``type``, a list of associated resource ids
                appliances (str): an optional list of appliance ids
                servers (str): an optional list of server ids
                networks (str): an optional list of network ids
                volumes (str): an optional list of volume ids

            Returns:
                :py:class:`nflex_connector_utils.connections.Connections`: returns itself, so that ``add`` methods can be chained
        """  # noqa

        if type is not None and connections is not None:
            self._add_type(type, connections)

        self._add_type('appliance', appliances)
        self._add_type('server', servers)
        self._add_type('network', networks)
        self._add_type('volume', volumes)

        return self

    def serialize(self):
        """Serialize the contents"""

        return self._data
