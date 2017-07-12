from . import Resource


class SaasUser(Resource):
    """
        A representation of an Saas User

        Args:
            base (base): See :py:class:`nflex_connector_utils.resource.Resource` for common resource args.
            user_id (str): Id of the Saas User
            avatar_url (str): Avatal URL of the user
            phone (str): Phone number of the user
            address (str): Address of the Saas User
            language (str): Preferred language of the user
            is_active (Boolean): To check if the user is active or not
            disk_quota_b (str): The Storage allocated to the user
            disk_used_b (str): The Storage used by the user


    """  # noqa

    def __init__(self, avatar_url=None, phone=None, address=None,
                 language=None, is_active=None, disk_quota_b=None,
                 disk_used_b=None, email=None, country=None, **kwargs):

        super(SaasUser, self).__init__(type='saas_user', **kwargs)

        self._avatar_url = avatar_url
        self._phone = phone
        self._address = address
        self._language = language
        self._is_active = is_active
        self._disk_quota_b = disk_quota_b
        self._disk_used_b = disk_used_b
        self._email = email
        self._country = country

    def serialize(self):
        """Serialize the contents"""

        data = super(SaasUser, self).serialize()

        data['details'] = {
            self.type: {
                "avatar_url": self._avatar_url,
                "phone": self._phone,
                "address": self._address,
                "is_active": self._is_active,
                "disk_quota_b": self._disk_quota_b,
                "disk_used_b": self._disk_used_b,
                "email": self._email,
                "country": self._country,
                "language": self._language,
            }
        }

        return data
