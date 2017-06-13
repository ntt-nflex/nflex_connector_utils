from nflex_connector_utils import Connections


class TestConnections(object):
    def test_connections(self):
        # Test empty constructor
        data = Connections().serialize()
        assert data == {}

        # Test constructor with type/connections
        data = Connections(type='type', connections=['1', '2']).serialize()
        assert data == {'type': [{'id': '1'}, {'id': '2'}]}

        # Test constructor with type any
        data = Connections(type='any', connections=['1', '2']).serialize()
        assert data == {'any': ['1', '2']}

        # Test constructor with named types
        named_types = {
            'appliances': ['a1', 'a2'],
            'networks': ['n1', 'n2'],
            'servers': ['s1', 's2'],
            'volumes': ['v1', 'v2'],
        }
        named_types_result = {
            'appliance': [{'id': 'a1'}, {'id': 'a2'}],
            'network': [{'id': 'n1'}, {'id': 'n2'}],
            'server': [{'id': 's1'}, {'id': 's2'}],
            'volume': [{'id': 'v1'}, {'id': 'v2'}],
        }

        data = Connections(**named_types).serialize()
        assert data == named_types_result

        # Test add() with type/connections
        data = Connections().add(type='type',
                                 connections=['1', '2']).serialize()
        assert data == {'type': [{'id': '1'}, {'id': '2'}]}
        data = Connections().add(**named_types).serialize()
        assert data == named_types_result
