from nflex_connector_utils.parser import load_metric_mapping
from unittest import TestCase


class TestParseMappings(TestCase):

    def test_conversion_expr(self):
        mapping = load_metric_mapping(
            file_path="nflex_connector_utils/tests/test_mapping.yaml"
        )

        params = {
            "value": 10,
        }

        self.assertEqual(
            mapping['metric1'].value(**params),
            100,
        )

        self.assertEqual(
            mapping['metric1'].convert(**params),
            100,
        )

        self.assertEqual(
            mapping['metric1'].unit(),
            '%',
        )

        self.assertEqual(
            mapping['metric2'].value(**params),
            1,
        )

        self.assertEqual(
            mapping['metric2'].convert(**params),
            1,
        )

        self.assertEqual(
            mapping['metric3'].value(**params),
            20,
        )

        self.assertEqual(
            mapping['metric3'].convert(**params),
            20,
        )

        self.assertEqual(mapping['metric3'].counter(), False)

        self.assertEqual(
            mapping['metric4'].value(**params),
            0,
        )

        self.assertEqual(
            mapping['metric4'].convert(**params),
            0,
        )

        self.assertEqual(mapping['metric4'].counter(), False)

        self.assertEqual(
            mapping['metric5'].name(),
            'metric5',
        )

        self.assertEqual(mapping['metric5'].counter(), True)
