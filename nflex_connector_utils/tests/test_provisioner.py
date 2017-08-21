from nflex_connector_utils.mapping import Provisioner
from unittest import TestCase

_PROVIDER = 'test'


class TestProvisioner(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provisioner = Provisioner(
            provider=_PROVIDER,
            mappings={
                _PROVIDER: {
                    'metric1': {
                        'name': 'metric1',
                        'conversion_expr': 'value * 10'
                    },
                    'metric2': {
                        'name': 'metric2',
                        'conversion_expr': 'value / 10'
                    },
                    'metric3': {
                        'name': 'metric3',
                        'conversion_expr': 'value + 10'
                    },
                    'metric4': {
                        'name': 'metric4',
                        'conversion_expr': 'value - 10'
                    },
                    'metric5': {
                        'name': 'metric5',
                    },
                }
            }
        )

    def _evaluate_value(self, mapping, value):
        return mapping.evaluate({'value': value})

    def test_conversion_expr(self):
        mappings = self.provisioner.parse()

        self.assertEqual(
            self._evaluate_value(
                mappings['metric1']['conversion_expr'], 10
            ),
            100,
        )

        self.assertEqual(
            self._evaluate_value(
                mappings['metric2']['conversion_expr'], 10
            ),
            1,
        )

        self.assertEqual(
            self._evaluate_value(
                mappings['metric3']['conversion_expr'], 10
            ),
            20,
        )

        self.assertEqual(
            self._evaluate_value(
                mappings['metric4']['conversion_expr'], 10
            ),
            0,
        )

        self.assertEqual(
            mappings['metric5']['name'],
            'metric5',
        )
