'''
Exceptions predefined here will be handled in spend collector.
'''


class InvalidCredentials(Exception):
    """
        Exception for invalid account credentials

        Args:
            msg (str): customised error msg.

        Returns:
            Raise an exception with either default message or given message
    """

    def __init__(self, msg=None):
        msg = msg or 'Invalid Credentials'
        super(InvalidCredentials, self).__init__(msg)


class InsufficientPermission(Exception):
    """
        Exception for insufficient permission. Raise this if the account does
        not have permission to access billing data

        Args:
            msg (str): customised error msg.

        Returns:
            Raise an exception with either default message or given message
    """
    def __init__(self, msg=None):
        msg = msg or 'Insufficient permission'
        super(InsufficientPermission, self).__init__(msg)


class NoBillingReport(Exception):
    """
        Exception for no billing report file found

        Args:
            msg (str): customised error msg.

        Returns:
            Raise an exception with either default message or given message
    """
    def __init__(self, msg=None):
        msg = msg or 'No billing report found'
        super(NoBillingReport, self).__init__(msg)


class SpendError(Exception):
    """
        Exception for any other kind of spend errors
    """
    pass
