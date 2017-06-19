from nflex_connector_utils import SaasUser


class TestSaasuser(object):


    def test_saas_user(self):
        data = SaasUser(id='id', name='name').serialize()
        assert 'saas_user' in data['details']
        assert data['details']['saas_user']['avatar_url'] is None
        assert data['details']['saas_user']['address'] is None
        assert data['details']['saas_user']['disk_quota_b'] is None
        assert data['details']['saas_user']['disk_used_b'] is None

        data = SaasUser(id='id', name='name', avatar_url='www.testurl.com'
                        ).serialize()
        assert data['details']['saas_user']['address'] is None
        assert data['details']['saas_user']['avatar_url'] is 'www.testurl.com'
        assert data['details']['saas_user']['disk_quota_b'] is None
        assert data['details']['saas_user']['disk_used_b'] is None
        assert data['details']['saas_user']['phone'] is None

        data = SaasUser(id='id', name='name', avatar_url='www.testurl.com',
                        phone='+4412345678', address='Hollywood'
                        ).serialize()
        assert data['details']['saas_user']['avatar_url'] is 'www.testurl.com'
        assert data['details']['saas_user']['address'] is 'Hollywood'
        assert data['details']['saas_user']['phone'] is '+4412345678'
        assert data['details']['saas_user']['disk_used_b'] is None

        data = SaasUser(id='id', name='name', avatar_url='www.testurl.com',
                        phone='+4412345678', address='USA',
                        disk_quota_b='3663', disk_used_b='1287').serialize()
        assert data['details']['saas_user']['avatar_url'] is 'www.testurl.com'
        assert data['details']['saas_user']['address'] is 'USA'
        assert data['details']['saas_user']['phone'] is '+4412345678'
        assert data['details']['saas_user']['disk_quota_b'] is '3663'
        assert data['details']['saas_user']['disk_used_b'] is '1287'







    # def test_volume_details(self):
    #     data = Volume(id='id', name='name').serialize()
    #     assert 'volume' in data['details']
    #     assert data['details']['volume']['iops'] is None
    #     assert data['details']['volume']['encrypted'] is None
    #     assert data['details']['volume']['size_b'] is None
    #     assert 'zone_name' not in data['details']['volume']
    #
    #     # iops should be None or an int
    #     data = Volume(id='id', name='name', iops=None).serialize()
    #     assert data['details']['volume']['iops'] is None
    #     data = Volume(id='id', name='name', iops=1).serialize()
    #     assert data['details']['volume']['iops'] == 1
    #     data = Volume(id='id', name='name', iops=1.5).serialize()
    #     assert data['details']['volume']['iops'] == 1
    #     data = Volume(id='id', name='name', iops="5").serialize()
    #     assert data['details']['volume']['iops'] == 5
    #
    #     data = Volume(id='id', name='name', encrypted=True,
    #                   size_b=10, zone_name='foo').serialize()
    #     assert data['details']['volume']['encrypted'] is True
    #     assert data['details']['volume']['size_b'] == 10
    #     assert data['details']['volume']['zone_name'] == 'foo'
    #




# AssertionError: assert 'saas_users' in {'saas_user': {'address': None, 'avatar_url': None, 'disk_quota_b': None, '': None, ...}}
