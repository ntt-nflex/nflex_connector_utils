import httplib


class Account(object):
    """
        A representation of an Account
    """

    def __init__(self, id=None, metadata=None):
        self.id = id
        self.metadata = metadata

    def serialize(self):
        """Serialize the contents"""

        results = {}
        if self.id:
            results["id"] = self.id

        if self.metadata:
            results["metadata"] = self.metadata.serialize()

        return results

    def update(self, api, account_id):
        """Updates CMP account"""

        if account_id is None:
            '''For testing purposes, if the event doesn't have an account_id,
               don't bother trying to POST to the accounts API.'''
            return

        response = api.patch(
            path='/accounts/%s/resource' % account_id,
            data=self.serialize())
        if response.status_code != httplib.OK:
            raise Exception(
                'Got bad response from account API: %d, %s' % (
                    response.status_code, response.content))
