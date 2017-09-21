from unittest import TestCase

from nflex_connector_utils import errors


class TestErrors(TestCase):
    def test_raise_errors(self):
        exceptions = [
            errors.InsufficientPermission,
            errors.InvalidCredentials,
            errors.NoBillingReport,
            errors.SpendError
        ]
        for exp in exceptions:
            with self.assertRaises(exp):
                raise exp()
