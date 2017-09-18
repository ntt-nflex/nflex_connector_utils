from __future__ import division
from pyparsing import (  # noqa
    CaselessKeyword,
    CaselessLiteral,
    Forward,
    OneOrMore,
    Optional,
    ParseException,
    ParserElement,
    Regex,
    StringEnd,
    Word,
    alphanums,
    alphas,
    infixNotation,
    oneOf,
    opAssoc,
)

import logging
import operator
import os
import yaml

_CONVERSION_KEY = 'conversion_expr'

_DEFAULT_FILE_NAME = 'mapping.yaml'


def load_metric_mapping(file_path=_DEFAULT_FILE_NAME):
    """
    Loads a selection of metric definition mappings
    using SimpleExpressionParser.
    It does so by mapping values per metric key to ParsedEntry value which
    looks for conversion_expr in each metric definition and runs
    the logic on that field per evaluate mechanism.

    :return: mapping: mapping of metric with conversion expression ready to be evaluated.
    :rtype: dict of str: :class:`.ParsedEntry`

    Args:
        file_path (str): path to file (optional)

    Examples:
        read mappings from mappings.yaml from current directory (or absolute path)::

            metric1:
                name: metric1
                unit: "%"
                conversion_expr: value * 10

        Get original value::

            value = 10

        Load mapping::

            # can specify custom path by passing argument file_path
            # example file_path='my_project/definition.yaml'
            mapping = load_metric_mapping()

        Evaluate metric based on initial value:

            See :class:`.ParsedEntry`

    """  # noqa

    mapping = os.path.abspath(file_path)

    with open(mapping) as f:
        mapping = yaml.safe_load(f)

    parser = SimpleExpressionParser()

    parsed_mapping = dict()

    for key, val in mapping.iteritems():
        conversion = None
        if _CONVERSION_KEY in val:
            conversion = parser.parse(
                val[_CONVERSION_KEY]
            )

        parsed_mapping[key] = ParsedEntry(
            name=val.get('name', ''),
            unit=val.get('unit', ''),
            counter=val.get('counter', False),
            conversion=conversion,
        )

    return parsed_mapping


class ParsedEntry(object):
    """Represents a parsed mapping entry"""

    def __init__(self, name, unit, counter, conversion=None):
        self._name = name
        self._unit = unit
        self._counter = counter
        self._conversion = conversion

    def convert(self, **kwargs):
        """
        Different syntax for :func:`value`

        Evaluate metric based on initial value::

                metric = mapping['metric1']
                try:
                    # 10 * 10 = 100
                    value = metric.convert(
                        value=10,
                    )
                except VariableLookupError as e:
                    raise e

                name = metric.name()
                unit = metric.unit()
                counter = metric.counter()
        """
        return self.value(**kwargs)

    def value(self, **kwargs):
        """
        Evaluates conversion expression if it has one based on kwargs input.
        :raises VariableLookupError: failed to evaluate expression based on variables given.

        :return: value: evaluated value or original value if definition has no conversion expression

        Args:
            **kwargs(dict) - variables to evaluate on conversion_exr property of specified definition. The original value should be expressed as kwargs['value']

        Examples:

            See :func:`.load_metric_mapping` for load example

            Evaluate metric based on initial value::

                metric = mapping['metric1']
                try:
                    # 10 * 10 = 100
                    value = metric.value(
                        value=10,
                    )
                except VariableLookupError as e:
                    raise e

                name = metric.name()
                unit = metric.unit()
                counter = metric.counter()
        """  # noqa

        if not self._conversion:
            try:
                return kwargs['value']
            except KeyError as e:
                raise VariableLookupError(e)

        return self._conversion.evaluate(kwargs)

    def unit(self):
        """Retrieves metric's unit"""
        return self._unit

    def name(self):
        """Retrieves metric's name"""
        return self._name

    def counter(self):
        """Retrieves metric's counter"""
        return self._counter


class ExpressionParser(object):
    """Takes care of parsing simple math expressions with variables"""
    def __init__(self):
        # a class-level static method to enable a memoizing performance
        # enhancement, known as "packrat parsing".
        ParserElement.enablePackrat()

        NUMBER = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").setParseAction(
            Immediate
        )
        IDENT = Word(alphas, alphanums + '_').setParseAction(Variable)
        self.OPERAND = (NUMBER | IDENT)
        self.MATH_OPERATORS = [
            (oneOf('+ -'), 1, opAssoc.RIGHT, SignTerm),
            ('^', 2, opAssoc.RIGHT, MathTerm),
            (oneOf('* /'), 2, opAssoc.LEFT, MathTerm),
            (oneOf('+ -'), 2, opAssoc.LEFT, MathTerm)
        ]
        self.ARITH_EXPR = infixNotation(self.OPERAND, self.MATH_OPERATORS)
        self.pattern = self.ARITH_EXPR + StringEnd()

    def parse(self, expression):
        try:
            return self.pattern.parseString(expression)[0]

        except ParseException as e:
            logging.warn('Failed to parse "%s": %s' % (expression, e))

        return None


class TernaryExpressionParser(ExpressionParser):
    """Takes care of parsing Python ternary statements with variables"""
    def __init__(self):
        super(TernaryExpressionParser, self).__init__()
        IF = CaselessKeyword('if').suppress()
        ELSE = CaselessKeyword('else').suppress()
        RELATIONAL_OPERATOR = oneOf(">= <= != > < = ==")
        CONDITION = (self.ARITH_EXPR +
                     RELATIONAL_OPERATOR +
                     self.ARITH_EXPR).setParseAction(Condition)
        self.TERNARY_EXPR = (
            self.ARITH_EXPR.setResultsName('if_expr') +
            IF +
            CONDITION.setResultsName('condition') +
            ELSE +
            self.ARITH_EXPR.setResultsName('else_expr')
        ).setParseAction(TernaryExpression)
        self.pattern = self.TERNARY_EXPR + StringEnd()


class CaseExpressionParser(TernaryExpressionParser):
    """Takes care of parsing (nested) SQL CASE statements with variables"""
    def __init__(self):
        super(CaseExpressionParser, self).__init__()
        CASE = CaselessKeyword('case').suppress()
        WHEN = CaselessKeyword('when').suppress()
        THEN = CaselessKeyword('then').suppress()
        ELSE = CaselessKeyword('else').suppress()
        END = CaselessKeyword('end').suppress()
        NOT = CaselessLiteral('not')
        AND = CaselessLiteral('and')
        OR = CaselessLiteral('or')

        RELATIONAL_OPERATOR = oneOf(">= <= != > < =")

        self.CASE_EXPR = Forward()
        # Case statements can be operands
        self.OPERAND = self.CASE_EXPR | self.OPERAND
        ARITH_EXPR = infixNotation(self.OPERAND, self.MATH_OPERATORS)

        CONDITION = (ARITH_EXPR +
                     RELATIONAL_OPERATOR +
                     ARITH_EXPR).setParseAction(Condition)

        WHEN_TERM = infixNotation(CONDITION,
                                  [(NOT, 1, opAssoc.RIGHT, NegativeTerm),
                                   (AND, 2, opAssoc.LEFT, AndTerm),
                                   (OR, 2, opAssoc.LEFT, OrTerm)])
        WHEN_EXPR = WHEN + WHEN_TERM.setResultsName('when_expr',
                                                    listAllMatches=True)

        THEN_EXPR = THEN + ARITH_EXPR.setResultsName('then_expr',
                                                     listAllMatches=True)

        ELSE_EXPR = ELSE + ARITH_EXPR.setResultsName('else_expr')

        self.CASE_EXPR << (
            CASE +
            OneOrMore(WHEN_EXPR + THEN_EXPR) + Optional(ELSE_EXPR) +
            END
        ).setParseAction(CaseStatement)
        self.pattern = self.CASE_EXPR + StringEnd()


class SimpleExpressionParser(CaseExpressionParser):
    """Takes care of parsing only python ternary
    expressions and simple math expressions with variables
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.pattern = (self.TERNARY_EXPR |
                        self.ARITH_EXPR) + StringEnd()


class Immediate(object):
    def __init__(self, tokens):
        self.value = tokens[0]

    def evaluate(self, variables):
        return float(self.value)

    def __repr__(self):
        return '<Immediate value=%s>' % self.value


class Variable(object):
    def __init__(self, tokens):
        self.value = tokens[0]

    def evaluate(self, variables):
        if self.value == 'NULL':
            return None
        try:
            return float(variables[self.value])

        except KeyError:
            raise VariableLookupError('Lookup failed for variable %s in %s'
                                      % (self.value, variables))

    def __repr__(self):
        return '<Variable value=%s>' % self.value


class Condition(object):
    opMap = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '=': operator.eq,
        '==': operator.eq,
        '!=': operator.ne,
    }

    def __init__(self, tokens):
        self.left, self.op, self.right = tokens

    def evaluate(self, variables):
        return self.opMap[self.op](self.left.evaluate(variables),
                                   self.right.evaluate(variables))


class CaseStatement(object):
    def __init__(self, tokens):
        self.if_then_pairs = zip(tokens['when_expr'], tokens['then_expr'])
        self.else_value = tokens.get('else_expr')

    def evaluate(self, variables):
        result = 'NULL'
        # go through all WHEN-THEN pairs and try to find a match
        for pair in self.if_then_pairs:
            if pair[0].evaluate(variables):
                result = pair[1].evaluate(variables)
                break

        # if none of the WHEN clauses are matched, use the ELSE clause
        if result == 'NULL':
            result = None
            if self.else_value:
                result = self.else_value.evaluate(variables)

        return result


class TernaryExpression(object):
    def __init__(self, tokens):
        self.condition = tokens['condition']
        self.if_expr = tokens['if_expr']
        self.else_expr = tokens['else_expr']

    def evaluate(self, variables):
        result = None
        if self.condition.evaluate(variables):
            result = self.if_expr.evaluate(variables)

        else:
            result = self.else_expr.evaluate(variables)

        return result


class BoolTerm(object):
    def __init__(self, tokens):
        self.operands = tokens[0][0::2]

    def evaluate(self, variables):
        return self.operator(o.evaluate(variables) for o in self.operands)


class AndTerm(BoolTerm):
    operator = all


class OrTerm(BoolTerm):
    operator = any


class NegativeTerm(object):
    def __init__(self, tokens):
        self.operand = tokens[0][1]

    def evaluate(self, variables):
        return not self.operand.evaluate(variables)


class MathTerm(object):
    opMap = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
    }

    def __init__(self, tokens):
        self.operands = tokens[0][0::2]
        self.operators = tokens[0][1::2]

    def evaluate(self, variables):
        result = self.operands[0].evaluate(variables)
        for i, op in enumerate(self.operators, start=1):
            try:
                result = self.opMap[op](result,
                                        self.operands[i].evaluate(variables))

            except ZeroDivisionError:
                result = 0.0

        return result


class SignTerm(object):
    def __init__(self, tokens):
        self.sign, self.operand = tokens[0]

    def evaluate(self, variables=None):
        if self.sign == '+':
            return self.operand.evaluate(variables)
        else:
            return -self.operand.evaluate(variables)


class VariableLookupError(Exception):
    """ Occurs when a variable lookup fails """
