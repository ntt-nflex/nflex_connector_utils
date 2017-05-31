class IpAddress(object):
    """
        A representation of an IP address

        Args:
            ip_address (str): IPv4 or IPv6 address
            network_id (str): Optional network id. This isn't used yet, but may be used in the future to associate an IP address with a network.
            network_name (str): Optional network name. This isn't used yet.

    """  # noqa

    def __init__(self, ip_address=None, network_id=None, network_name=None):
        self._ip_address = ip_address
        self._network_id = network_id
        self._network_name = network_name

    def serialize(self):
        """Serialize the contents"""

        results = {}
        if self._ip_address is not None:
            results['ip_address'] = self._ip_address

        if self._network_id is not None and self._network_name is not None:
            results['network'] = {
                'id': self._network_id,
                'name': self._network_name,
            }

        return results
