from nflex_connector_utils import SaasUser


class TestSaasuser(object):
    def test_saas_user(self):
        assert SaasUser().serialize() == {}

        assert SaasUser(avatar_url='www.testurl.com').serialize() == {
            'avatar_url': 'www.testurl.com'
        }

        assert SaasUser(phone='+4412345678', address='Hollywood'
                        ).serialize() == {
            'phone': '+4412345678',
            'address': 'Hollywood'
        }

        assert SaasUser(disk_quota_b='2048').serialize() == {
            'disk_quota_b': '2048'
        }

        assert SaasUser(avatar_url='www.anotherurl.com', phone='+4412345678',
                        address='USA', disk_quota_b='3663', disk_used_b='1287'
                        ).serialize() == {
            'avatar_url': 'www.anotherurl.com',
            'phone': '+4412345678',
            'address': 'USA',
            'disk_quota_b': '3663',
            'disk_used_b': '1287'
        }
