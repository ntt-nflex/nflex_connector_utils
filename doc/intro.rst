Introduction
============
This python package provides a suite of tools to produce data structures when implementing NTT CMP resources connector nflex modules.

An object oriented interface is provided with ``serialize`` methods to convert the data into the format required by the NTT nflex connector resources API.

For example::

    from nflex_connector_utils import Server, serialize_list


    def get(event, context):
        return serialize_list([
            Server(id='server-1', name='Server 1'),
            Server(id='server-2', name='Server 2'),
        ])

See the :ref:`examples` and :ref:`api` documentation for more details.