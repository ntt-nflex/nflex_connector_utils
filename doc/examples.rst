.. _examples:

Examples
========
Here is a full example of some nflex resource connector code::

    def get(event, context):
        resources = serialize_list([
            Appliance(id='appliance-1', name='Network 1', type_id='firewall'),
            Network(id='network-1', name='Network 1'),
            Server(id='server-1', name='Server 1'),
            Volume(id='volume-1', name='Volume 1'),

            # A volume with some more details
            Volume(
                id='volume-2',
                name='Volume 2',
                size_b=1024 * 1024 * 1024 * 1024,  # 1 TB disks
                encrypted=False,
                iops=None,
                zone_name='eu-west-1',
            ),

            # A server with some more details
            Server(
                id='server-2',
                name='Server with lots of details',
                provider_created_at=datetime(year=2017, month=2, day=4),

                # Associate the server with the volume and network
                connections=Connections(
                    volumes=['volume-2'],
                    networks=['network-1']),

                # Add some metadata
                metadata=Metadata([('key1', 'value1'), ('key2', 'value2')]),

                # Set a location by matching a region id with locations
                # in the CMP database. This is a legacy procedure which
                # requires data to be added to the CMP database by the CMP
                # development team.
                region=Region('region-1'),

                # An example of a single location association
                locations = Locations([{
                    'country': {'name': 'France'},
                    'city': {'name': 'Paris'},
                    'location': {
                        'name': 'Legendary Paris Place',
                        'latitude': 48.860764,
                        'longitude': 2.393646,
                    }
                }]),

                native_portal_link='http://www.example.com/servers/server-2',
                state='stopped',
                provider_state='powered off',

                image_detail=ImageDetail(id='image-1',
                                         name='ubuntu 16.04',
                                         type='Linux',
                                         distribution='Ubuntu',
                                         version='16.04',
                                         architecture='64'),

                cpu_cores=2,
                cpu_hz=2500000,                       # 2.5 GHz
                ram_b=1024 * 1024 * 32,               # 1 GB RAM
                volumes_b=1024 * 1024 * 1024 * 1024,  # 1 TB disks

                ip_addresses=[IpAddress(
                    ip_address='192.168.0.1',
                    network_id='network-1',
                    network_name='Network 1',
                )]
            ),
        ])

        return resources
