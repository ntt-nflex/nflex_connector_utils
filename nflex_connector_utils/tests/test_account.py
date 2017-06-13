import pytest

from nflex_connector_utils import Account, Metadata


class TestAccount(object):
    def test_account(self):
        assert Account().serialize() == {}

        assert Account(id='ACCOUNT_ID').serialize() == {
            'id': 'ACCOUNT_ID'
        }

        metadata = Metadata([('regions', ['region1', 'region2'])])
        assert Account(metadata=metadata).serialize() == {
            'metadata': {
                'provider_specific': {
                    'regions': ['region1', 'region2'],
                }
            }
        }

        assert Account(id='ACCOUNT_ID', metadata=metadata).serialize() == {
            'id': 'ACCOUNT_ID',
            'metadata': {
                'provider_specific': {
                    'regions': ['region1', 'region2'],
                }
            }
        }

    def test_update(self, mocker):
        account = Account()
        assert account.update(api=None, account_id=None) is None

        mocked_api = mocker.Mock()
        mocked_api.patch.return_value = mocker.Mock()

        mocked_api.patch.return_value.status_code = 200
        mocked_api.patch.return_value.content = 'OK'
        assert account.update(api=mocked_api, account_id='ACCOUNT_ID') is None

        mocked_api.patch.return_value.status_code = 500
        mocked_api.patch.return_value.content = 'NOT OK'
        with pytest.raises(Exception):
            assert account.update(api=mocked_api,
                                  account_id='ACCOUNT_ID') is None
