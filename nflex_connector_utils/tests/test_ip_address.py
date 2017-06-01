from nflex_connector_utils import IpAddress


class TestIpAddress(object):
    def test_ip_address(self):
        assert IpAddress().serialize() == {}

        assert IpAddress(ip_address='127.0.0.1').serialize() == {
            'ip_address': '127.0.0.1'
        }

        assert IpAddress(network_id='id', network_name='name').serialize() == {
            'network': {
                'id': 'id',
                'name': 'name',
            }
        }

        assert IpAddress(description='Public IP').serialize() == {
            'description': 'Public IP'
        }

        assert IpAddress(ip_address='127.0.0.1', network_id='id',
                         network_name='name', description='Public IP'
                         ).serialize() == {
            'ip_address': '127.0.0.1',
            'network': {
                'id': 'id',
                'name': 'name',
            },
            'description': 'Public IP'
        }
