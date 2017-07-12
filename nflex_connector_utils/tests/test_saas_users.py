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
                        disk_quota_b='3663', disk_used_b='1287',
                        language='en_GB').serialize()
        assert data['details']['saas_user']['avatar_url'] is 'www.testurl.com'
        assert data['details']['saas_user']['address'] is 'USA'
        assert data['details']['saas_user']['phone'] is '+4412345678'
        assert data['details']['saas_user']['disk_quota_b'] is '3663'
        assert data['details']['saas_user']['disk_used_b'] is '1287'
        assert data['details']['saas_user']['language'] is 'en_GB'
