import pytest

from nflex_connector_utils import ImageDetail, ImageDetailMap


class TestImageDetail(object):
    ALL_NONES = {
        'architecture': None,
        'distribution': None,
        'id': 'foo',
        'name': None,
        'type': None,
        'version': None
    }

    def test_image_detail(self):
        data = ImageDetail(id='foo').serialize()
        assert data == self.ALL_NONES

        # Test exception for missing id
        with pytest.raises(ValueError):
            data = ImageDetail()

        # Test values
        kwargs = {
            'architecture': 'arch',
            'distribution': 'dist',
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'version': 'version'
        }
        data = ImageDetail(**kwargs).serialize()
        assert data == kwargs

    def test_image_detail_map(self):
        m = ImageDetailMap({
            #       name, type, dist, version, arch
            'id1': ('n1', 't1', 'd1', 'v1', 'a1'),
            'nothing': (None, None, None, None, None)
        })

        # No match
        assert m.get('foo').serialize() == self.ALL_NONES

        # No match with default
        assert m.get('foo', name='alt-name').serialize() == {
            'id': 'foo',
            'architecture': None,
            'distribution': None,
            'name': 'alt-name',
            'type': None,
            'version': None
        }

        # Match
        assert m.get('id1').serialize() == {
            'id': 'id1',
            'name': 'n1',
            'version': 'v1',
            'architecture': 'a1',
            'distribution': 'd1',
            'type': 't1',
        }

        # Match image with id='nothing'
        assert m.get('nothing').serialize() == {
            'id': 'nothing',
            'name': None,
            'version': None,
            'architecture': None,
            'distribution': None,
            'type': None,
        }

        for key in ('name', 'version', 'architecture', 'distribution', 'type'):
            kwargs = {key: 'value'}
            data = m.get('nothing', **kwargs).serialize()
            assert data[key] == 'value'
