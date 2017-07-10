import pytest

from nflex_connector_utils import (
    Resource, Appliance, Network, Server, ServiceOffering, Volume,
    IpAddress, ImageDetail, Region, Locations, Connections, Metadata,
    ComputePool, ColoSpace, Circuit)


class TestResources(object):
    def test_resource(self):
        data = Resource(id='id', name='name', type='type').serialize()
        assert data['id'] == 'id'
        assert data['type'] == 'type'
        assert data['connections'] == {}
        assert data['metadata'] == {}
        assert data['base']['name'] == 'name'
        assert data['base']['provider_created_at'] is None
        assert data['base']['last_seen_at'] is not None
        assert data['base']['regions'] == []
        assert 'native_portal_link' not in data['base']

        # Test exception raising
        for key in ('id', 'name', 'type'):
            with pytest.raises(ValueError):
                # Check None value
                kwargs = {'id': 'id', 'name': 'name', 'type': 'type'}
                kwargs[key] = None
                data = Resource(**kwargs).serialize()

            with pytest.raises(ValueError):
                kwargs = {'id': 'id', 'name': 'name', 'type': 'type'}
                # Check missing key
                del kwargs[key]
                data = Resource(**kwargs).serialize()

            with pytest.raises(ValueError):
                kwargs = {'id': 'id', 'name': 'name', 'type': 'type'}
                # Check bad type
                kwargs[key] = {}
                data = Resource(**kwargs).serialize()

        kwargs = {'id': 'id', 'name': 'name', 'type': 'type'}

        # Test native_portal_link
        data = Resource(native_portal_link='foo', **kwargs).serialize()
        assert data['base']['native_portal_link'] == 'foo'

        # Ensure complex keys are there. More elaborate tests are elsewhere

        data = Resource(region=Region(id='foo'), **kwargs).serialize()
        assert len(data['base']['regions']) > 0

        data = Resource(locations=Locations([{id: 'foo'}]), **kwargs). \
            serialize()
        assert len(data['base']['locations']) > 0

        data = Resource(connections=Connections(servers=['foo']),
                        **kwargs).serialize()
        assert len(data['connections'].keys()) > 0

        data = Resource(metadata=Metadata([('key', 'value')]),
                        **kwargs).serialize()
        assert len(data['metadata'].keys()) > 0

    def test_appliance_details(self):
        data = Appliance(id='id', name='name').serialize()
        assert data['details']['appliance']['type_id'] is None

        data = Appliance(id='id', name='name', type_id='foo').serialize()
        assert data['details']['appliance']['type_id'] == 'foo'

    def test_compute_pool_details(self):
        data = ComputePool(id='id', name='name').serialize()
        assert data['details']['compute_pool'] == {
            'cpu_hz': None,
            'memory_b': None,
            'storage_b': None,
        }

        data = ComputePool(
            id='id',
            name='name',
            cpu_hz=2000000,
            memory_b=1024,
            storage_b=1024,
            billing_tag='something'
        ).serialize()
        assert data['details']['compute_pool'] == {
            'cpu_hz': 2000000,
            'memory_b': 1024,
            'storage_b': 1024,
            'billing_tag': 'something'
        }

    def test_network_details(self):
        # There isn't much to test here
        data = Network(id='id', name='name').serialize()
        assert 'network' in data['details']

    def test_server_details(self):
        # Check defaults
        data = Server(id='id', name='name').serialize()
        assert data['details']['server'] == {
            'cpu_cores': None,
            'cpu_hz': None,
            'image_detail': None,
            'instance_type': None,
            'ip_addresses': [],
            'provider_state': 'unknown',
            'ram_b': None,
            'state': 'unknown',
            'volumes_b': None,
        }

        data = Server(
            id='id',
            name='name',
            cpu_cores=2,
            cpu_hz=2000000,
            provider_state='foo',
            ram_b=2 * 1024 * 1024 * 1024,
            state='bar',
            volumes_b=1 * 1024 * 1024 * 1024 * 1024,
            is_virtual=False,
            ip_addresses=[IpAddress(ip_address='127.0.0.1')],
            image_detail=ImageDetail(id='foo')
        ).serialize()

        # Ensure complex keys are there. More elaborate tests are elsewhere
        ip_addresses = data['details']['server'].pop('ip_addresses')
        image_detail = data['details']['server'].pop('image_detail')
        assert len(ip_addresses) > 0
        assert len(image_detail.keys()) > 0

        assert data['details']['server'] == {
            'cpu_cores': 2,
            'cpu_hz': 2000000,
            'instance_type': None,
            'provider_state': 'foo',
            'ram_b': 2 * 1024 * 1024 * 1024,
            'state': 'bar',
            'volumes_b': 1 * 1024 * 1024 * 1024 * 1024,
            'is_virtual': False,
        }

    def test_service_offering_details(self):
        data = ServiceOffering(id='id', name='name').serialize()
        assert data['details']['service_offering']['type_id'] is None

        data = ServiceOffering(id='id', name='name', type_id='foo').serialize()
        assert data['details']['service_offering']['type_id'] == 'foo'

    def test_volume_details(self):
        data = Volume(id='id', name='name').serialize()
        assert 'volume' in data['details']
        assert data['details']['volume']['iops'] is None
        assert data['details']['volume']['encrypted'] is None
        assert data['details']['volume']['size_b'] is None
        assert 'zone_name' not in data['details']['volume']

        # iops should be None or an int
        data = Volume(id='id', name='name', iops=None).serialize()
        assert data['details']['volume']['iops'] is None
        data = Volume(id='id', name='name', iops=1).serialize()
        assert data['details']['volume']['iops'] == 1
        data = Volume(id='id', name='name', iops=1.5).serialize()
        assert data['details']['volume']['iops'] == 1
        data = Volume(id='id', name='name', iops="5").serialize()
        assert data['details']['volume']['iops'] == 5

        volume = Volume(id='id', name='name', encrypted=True,
                        size_b=10, zone_name='foo')
        data = volume.serialize()
        assert data['details']['volume']['encrypted'] is True
        assert data['details']['volume']['size_b'] == 10
        assert volume.size_b == 10
        assert data['details']['volume']['zone_name'] == 'foo'

    def test_colo_space_details(self):
        data = ColoSpace(id='id', name='name').serialize()
        assert data['details']['colo_space'] == {
            'power_allocation_w': None,
            'type_id': None,
            'colo_space_location': None,
            'customer_name': None,
            'customer_label': None,
            'customer_description': None,
            'combination': None
        }

        data = ColoSpace(
            id='id',
            name='COLOSPACE',
            power_allocation_w=42,
            type_id='cab',
            colo_space_location='Somewhere over the rainbow',
            customer_name='The Original Colo Space',
            customer_label='Coley McColoface',
            customer_description='Yet another Colo Space',
            combination='Open Sesame'
        ).serialize()
        assert data['details']['colo_space'] == {
            'power_allocation_w': 42,
            'type_id': 'cab',
            'colo_space_location': 'Somewhere over the rainbow',
            'customer_name': 'The Original Colo Space',
            'customer_label': 'Coley McColoface',
            'customer_description': 'Yet another Colo Space',
            'combination': 'Open Sesame'
        }

    def test_circuit_details(self):
        data = Circuit(id='id', name='name').serialize()
        assert data['details']['circuit'] == {
            'type_id': None,
            'carrier': None,
            'reference': None,
            'endpoint_a': None,
            'endpoint_b': None,
        }

        data = Circuit(
            id='id',
            name='circuit',
            type_id='pvc',
            carrier='test',
            reference='test',
            endpoint_a='test_endpoint_a',
            endpoint_b='test_endpoint_b'
        ).serialize()
        assert data['details']['circuit'] == {
            'type_id': 'pvc',
            'carrier': 'test',
            'reference': 'test',
            'endpoint_a': 'test_endpoint_a',
            'endpoint_b': 'test_endpoint_b'
        }
