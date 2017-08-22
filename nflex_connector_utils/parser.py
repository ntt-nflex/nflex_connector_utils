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


_CONVERSION_KEY = 'conversion_expr'


def parse_mappings(mappings):
    """
    Parses through a selection of metric definition mappings
    using SimpleExpressionParser.
    Looks for conversion_expr in each metric definition and runs
    the logic on that field per evaluate mechanism.

    Args:
        mappings (dict): metric definition mappings

    Examples:
        Setup mappings::

            mappings = {
                'definition1': {
                    'name': 'definition1',
                    'conversion_expr': 'value * 10'
                }
            }

        Get original value::

            metric_value = 10

        Parse the mappings::

            parsed_mappings = parse_mappings(mappings)

        Evaluate metric definition based on initial value::

            parsed_metric_definition = parsed_mappings['definition1']
            if 'conversion_expr' in parsed_metric_definition:
                # 10 * 10 = 100
                parsed_metric_value = parsed_metric_definition['
                'conversion_expr'].evaluate({
                    "value": metric_value
                })

    """  # noqa
    parser = SimpleExpressionParser()

    for item in mappings.values():
            if _CONVERSION_KEY in item:
                item[_CONVERSION_KEY] = parser.parse(
                    item[_CONVERSION_KEY]
                )

    return mappings


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
