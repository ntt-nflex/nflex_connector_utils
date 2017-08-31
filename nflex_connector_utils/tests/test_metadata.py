from nflex_connector_utils import Metadata


class TestMetadata(object):
    NS_PS = Metadata.PROVIDER_SPECIFIC_NAMESPACE_ID

    def test_metadata(self):
        def test_init(values=None, default_namespace=None,
                      expected_result=None):
            data = Metadata(values=values,
                            default_namespace=default_namespace).serialize()
            assert data == expected_result

        test_init(None, None, {})
        test_init([], None, {})
        test_init([('key', 'value')], None, {self.NS_PS: {'key': 'value'}})
        test_init([('ns', 'key', 'value')], None, {'ns': {'key': 'value'}})
        test_init([('ns',)], None, {})
        test_init({}, None, {})
        test_init('foo', None, {})

        m = Metadata()
        m.add('key1', 'value1')
        m.add('key2', 'value2', namespace='different-ns')
        assert m.serialize() == {
            self.NS_PS: {'key1': 'value1'},
            'different-ns': {'key2': 'value2'},
        }

        m = Metadata(default_namespace='alt-ns')
        m.add('key1', 'value1')
        m.add('key2', 'value2', namespace='different-ns')
        assert m.serialize() == {
            'alt-ns': {'key1': 'value1'},
            'different-ns': {'key2': 'value2'},
        }
