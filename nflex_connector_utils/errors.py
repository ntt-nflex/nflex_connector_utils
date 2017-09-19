'''
Exceptions predefined here will be handled in our spend collector.
'''


class InvalidCredentials(Exception):
    def __init__(self, msg=None):
        msg = msg or 'Invalid Credentials'
        super(InvalidCredentials, self).__init__(msg)


class InsufficientPermission(Exception):
    def __init__(self, msg=None):
        msg = msg or 'Insufficient permission'
        super(InsufficientPermission, self).__init__(msg)


class NoBillingReport(Exception):
    def __init__(self, msg=None):
        msg = msg or 'No billing report found'
        super(NoBillingReport, self).__init__(msg)


class SpendError(Exception):
    pass
