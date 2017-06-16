from . import Resource

class SaasUser(Resource):
    """
        A representation of an Saas User

        Args:
            user_id (str): Id of the Saas User
            name (str): Name of the user
            avatar_url (str): Avatal URL of the user
            phone (str): Phone number of the user
            address (str): Address of the Saas User
            language (str): Preferred language of the user
            metadata (str): Metadata of the user
            is_active (Boolean): To check if the user is active or not
            disk_quota_b (str): The Storage allocated to the user
            disk_used_b (str): The Storage used by the user
            

    """  # noqa

    def __init__(self, user_id=None, name=None, avatar_url=None, phone=None, address=None, language=None,
                 metadata=None, is_active=None, disk_quota_b=None, disk_used_b=None):
        self._user_id = user_id
        self._name = name
        self._avatar_url = avatar_url
        self._phone = phone
        self._address = address
        self._language = language
        self._metadata = metadata
        self._is_active = is_active
        self._disk_quota_b = disk_quota_b
        self._disk_used_b = disk_used_b

    def serialize(self):
        """Serialize the contents"""

        data = super(SaasUser, self).serialize()

        data['details'] = {
            self.type: {
                "user_id": self._user_id,
                "name": self._name,
                "avatar_url": self._avatar_url,
                "phone": self._phone,
                "address": self._address,
                "metadata": self._metadata,
                "is_active": self._is_active,
                "disk_quota_b": self._disk_quota_b,
                "disk_used_b": self._disk_used_b,
            }
        }

        return data
