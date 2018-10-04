from unittest import TestCase

from nflex_connector_utils.parser import (
    ExpressionParser,
    CaseExpressionParser,
    VariableLookupError,
)


class TestExpressionParser(TestCase):

    def setUp(self):
        self.parser = ExpressionParser()

    def test_evaluate_number_integer(self):
        number = '1'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.00)

    def test_evaluate_number_float(self):
        number = '1.00'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.00)

    def test_evaluate_number_with_parenthesis(self):
        number = '(1)'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.00)

    def test_evaluate_number_scientific_notation_big(self):
        number = '1e5'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({})

        self.assertEqual(result, 100000.00)

    def test_evaluate_number_scientific_notation_small(self):
        number = '1e-3'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({})

        self.assertEqual(result, .001)

    def test_evaluate_identifier_one_letter(self):
        number = 'e'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({'e': 1})

        self.assertEqual(result, 1.0)

    def test_evaluate_identifier_alphanum(self):
        number = 'variable1'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({'variable1': 1})

        self.assertEqual(result, 1.0)

    def test_evaluate_identifier_alphanum_with_underscore(self):
        number = 'variable_1'
        parsed = self.parser.parse(number)

        result = parsed.evaluate({'variable_1': 1})

        self.assertEqual(result, 1.0)

    def test_evaluate_identifier_no_variables_passed(self):
        number = 'cpu_used'
        parsed = self.parser.parse(number)

        with self.assertRaises(VariableLookupError):
            parsed.evaluate({})

    def test_evaluate_expression_signed_number_big(self):
        expression = '-1e6'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, -1000000.0)

    def test_evaluate_expression_signed_number_small(self):
        expression = '-1e-6'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, -.000001)

    def test_evaluate_expression_signed_variable(self):
        expression = '-cpu_used'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({'cpu_used': 1})

        self.assertEqual(result, -1.0)

    def test_evaluate_expression_signed_literal_with_whitespace(self):
        expression = '+ 1'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.0)

    def test_evaluate_expression_signed_literal_with_parenthesis(self):
        expression = '+(1)'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.0)

    def test_evaluate_expression_division_by_zero(self):
        expression = '1 / 0'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, .0)

    def test_evaluate_expression_same_precedence_no_parenthesis(self):
        expression = '1 + 2 + 3 - 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.0)

    def test_evaluate_expression_same_precedence_with_parenthesis(self):
        expression = '1 + (2 + 3) - 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 1.0 + 5.0 - 5.0)

    def test_evaluate_expression_different_precedence_no_parenthesis(self):
        expression = '1 + 2 + 3 * 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 3.0 + 15.0)

    def test_evaluate_expression_different_precedence_with_parenthesis(self):
        expression = '(1 + 2 + 3) * 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 6.0 * 5.0)

    def test_evaluate_expression_exp_func_precedence_no_parenthesis(self):
        expression = '1*5 + 2^2^2 + 3/4 * 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 5.0 + 16.0 + 3.75)

    def test_evaluate_expression_exp_func_precedence_with_parenthesis(self):
        expression = '(1*5 + 2^2)^2 + 3/4 * 5'
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({})

        self.assertEqual(result, 81.0 + 3.75)

    def test_parse_invalid_identifiers(self):
        self.assertExpressionInvalid('1a')
        self.assertExpressionInvalid('1_')
        self.assertExpressionInvalid('1_a')
        self.assertExpressionInvalid('_a')
        self.assertExpressionInvalid('_1')
        self.assertExpressionInvalid('_a1')
        self.assertExpressionInvalid('__')

    def test_parse_invalid_math_expression(self):
        self.assertExpressionInvalid('1 +')
        self.assertExpressionInvalid('1 */ 1')
        self.assertExpressionInvalid('0 // 1')
        self.assertExpressionInvalid('0 ^^^ 1')
        self.assertExpressionInvalid('+')
        self.assertExpressionInvalid('-2*')
        self.assertExpressionInvalid('(')
        self.assertExpressionInvalid(')')
        self.assertExpressionInvalid('()')
        self.assertExpressionInvalid('()+()')
        self.assertExpressionInvalid('(a +)b')
        self.assertExpressionInvalid('(a +()b')
        self.assertExpressionInvalid('a +()b')

    def assertExpressionInvalid(self, expr):
        self.assertIsNone(self.parser.parse(expr))


class TestCaseExpressionParser(TestCase):

    def setUp(self):
        self.parser = CaseExpressionParser()

    def test_evaluate_one_when_then_pair(self):
        expression = ('CASE WHEN disk_avail = 0 THEN NULL '
                      'ELSE (disk_used / disk_avail) END')
        parsed = self.parser.parse(expression)

        # test then clause
        result = parsed.evaluate({'disk_avail': 0.0, 'disk_used': 10.0})
        self.assertEqual(result, None)

        # test else clause
        result = parsed.evaluate({'disk_avail': 100.0, 'disk_used': 10.0})
        self.assertEqual(result, .1)

    def test_evaluate_relational_operators(self):
        eq = self.parser.parse('CASE WHEN a = 1 THEN 1 ELSE 0 END')
        ne = self.parser.parse('CASE WHEN a != 1 THEN 1 ELSE 0 END')
        ge = self.parser.parse('CASE WHEN a >= 1 THEN 1 ELSE 0 END')
        gt = self.parser.parse('CASE WHEN a > 1 THEN 1 ELSE 0 END')
        le = self.parser.parse('CASE WHEN a <= 1 THEN 1 ELSE 0 END')
        lt = self.parser.parse('CASE WHEN a < 1 THEN 1 ELSE 0 END')

        # test equal
        result = eq.evaluate({'a': 1})
        self.assertEqual(result, 1)

        result = eq.evaluate({'a': 0})
        self.assertEqual(result, 0)

        # test not equal
        result = ne.evaluate({'a': 0})
        self.assertEqual(result, 1)

        result = ne.evaluate({'a': 1})
        self.assertEqual(result, 0)

        # test less than
        result = lt.evaluate({'a': 0})
        self.assertEqual(result, 1)

        result = lt.evaluate({'a': 1})
        self.assertEqual(result, 0)

        # test less than or equal
        result = le.evaluate({'a': 1})
        self.assertEqual(result, 1)

        result = le.evaluate({'a': 2})
        self.assertEqual(result, 0)

        # test greater than
        result = gt.evaluate({'a': 2})
        self.assertEqual(result, 1)

        result = gt.evaluate({'a': 1})
        self.assertEqual(result, 0)

        # test greater than or equal
        result = ge.evaluate({'a': 1})
        self.assertEqual(result, 1)

        result = ge.evaluate({'a': 0})
        self.assertEqual(result, 0)

    def test_evaluate_multiple_when_then_pairs(self):
        expression = ('CASE WHEN (a = 0 and b = 0) THEN 0 '
                      'WHEN a = 0 and b = 1 or b = 2 THEN 1 '
                      'WHEN (a = 1 and b = 1) or (a = 1 and b = 0) THEN 2 '
                      'WHEN b >= a THEN 60 + a * 3 + b * 1e2 * 2'
                      'ELSE (a + b) * 2 + 1e2 / 2 END')
        parsed = self.parser.parse(expression)

        # test first when
        result = parsed.evaluate({'a': 0.0, 'b': 0.0})
        self.assertEqual(result, .0)

        # test second when
        result = parsed.evaluate({'a': 0.0, 'b': 1.0})
        self.assertEqual(result, 1.00)

        result = parsed.evaluate({'a': 0.0, 'b': 2.0})
        self.assertEqual(result, 1.00)

        # test third when
        result = parsed.evaluate({'a': 1.0, 'b': 1.0})
        self.assertEqual(result, 2.00)

        result = parsed.evaluate({'a': 1.0, 'b': 0.0})
        self.assertEqual(result, 2.00)

        # test forth when
        result = parsed.evaluate({'a': 2.0, 'b': 3.0})
        self.assertEqual(result, 666.0)

        # test else
        result = parsed.evaluate({'a': 4.0, 'b': 1.0})
        self.assertEqual(result, 60.0)

    def test_evaluate_nested_case_statement(self):
        expression = ('CASE WHEN a = 0 THEN 0 '
                      'ELSE CASE WHEN (a = b) THEN a + b END * 8 END')
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({'a': 1, 'b': 1})

        self.assertEqual(result, 16.0)

    def test_evaluate_nested_case_statement_with_parenthesis(self):
        expression = ('CASE WHEN a = 0 THEN 0 '
                      'ELSE (CASE WHEN (a = b) THEN a + b END) * 8 END')
        parsed = self.parser.parse(expression)

        result = parsed.evaluate({'a': 1, 'b': 1})

        self.assertEqual(result, 16.0)

    def test_evalute_invalid_case_statement(self):
        self.assertExpressionInvalid('WHEN a = 1 THEN a END')
        self.assertExpressionInvalid('CASE')
        self.assertExpressionInvalid('CASE END')
        self.assertExpressionInvalid('CASE WHEN')
        self.assertExpressionInvalid('CASE THEN')
        self.assertExpressionInvalid('CASE ELSE')
        self.assertExpressionInvalid('CASE ELSE 1')
        self.assertExpressionInvalid('CASE ELSE 1 END')
        self.assertExpressionInvalid('CASE THEN 1 ELSE 2')
        self.assertExpressionInvalid('CASE THEN 1 ELSE 2 END')
        self.assertExpressionInvalid('CASE WHEN THEN 1 END')
        self.assertExpressionInvalid('CASE WHEN () THEN 1 END')
        self.assertExpressionInvalid('CASE WHEN a THEN 1 END')
        self.assertExpressionInvalid('CASE WHEN a = 1 THEN 1')
        self.assertExpressionInvalid('CASE WHEN a = THEN 1 END')
        self.assertExpressionInvalid('CASE WHEN a = 1 THEN 1 ELSE END')
        self.assertExpressionInvalid('CASE WHEN a = 1 THEN 1 ELSE () END')
        self.assertExpressionInvalid('CASE WHEN THEN ELSE END')
        self.assertExpressionInvalid('CASE WHEN a = 1 THEN '
                                     '(CASE WHEN b = 2 THEN 1 ELSE 2 * 1 END)')
        self.assertExpressionInvalid('CASE CASE WHEN a = 1 THEN 1 END')
        self.assertExpressionInvalid('CASE WHEN a = 1 THEN 1 END END')

    def assertExpressionInvalid(self, expr):
        self.assertIsNone(self.parser.parse(expr))
