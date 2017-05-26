class IpAddress(object):
    """
        A representation of an IP address

        Args:
            ip_address (str): IPv4 or IPv6 address
            network_id (str): Optional network id. This isn't used yet, but may be used in the future to associate an IP address with a network.
            network_name (str): Optional network name. This isn't used yet.

    """  # noqa

    def __init__(self, ip_address=None, network_id=None, network_name=None):
        self.ip_address = ip_address
        self.network_id = network_id
        self.network_name = network_name

    def serialize(self):
        """Serialize the contents"""

        results = {}
        if self.ip_address is not None:
            results['ip_address'] = self.ip_address

        if self.network_id is not None and self.network_name is not None:
            results['network'] = {
                'id': self.network_id,
                'name': self.network_name,
            }

        return results
