from pprint import pprint
from pprint import pprint
from typing import Any, List, Tuple

from src.constants import Lexeme
from src.lang import *

analyzer = None


def callback(callback_func=None):
    if callback_func is None:
        raise ValueError("Пустой callback")

    def inner(method):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            callback_func(method, result)
            return result

        return wrapper

    return inner


def simple_callback(method, lexemes):
    if lexemes[0]:
        print()
        print(method, lexemes[0])
        pprint([i.value for i in lexemes[1:][0]])


def init(instance):
    global analyzer
    analyzer = instance


class BaseParser(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Union[Tuple[bool, List[Lexeme], bool], Any]:
        pass

    def __and__(self, other):
        return Concat(self, other)

    def __or__(self, other):
        return Or(self, other)

    def opt(self):
        return Optional(self)

    def many(self):
        return Many(self)

    def at_least_once(self):
        return AtLeastOnce(self)


class Concat(BaseParser):
    def __init__(self, left_parser, right_parser):
        self.left = left_parser
        self.right = right_parser

    def __call__(self):
        left_success, left_result, already_get = self.left()
        if left_success:
            if not already_get:
                analyzer.new_lex()
            right_success, right_result, already_get = self.right()
            if right_success:
                if not already_get:
                    analyzer.new_lex()
                return True, [*left_result, *right_result], True
        return False, [], True


class Or(BaseParser):
    def __init__(self, left_parser, right_parser):
        self.left = left_parser
        self.right = right_parser

    def __call__(self):
        left_success, left_result, already_get = self.left()
        if left_success:
            if not already_get:
                analyzer.new_lex()
            return True, left_result, True

        right_success, right_result, already_get = self.right()
        if right_success:
            if not already_get:
                analyzer.new_lex()
            return True, right_result, True
        return False, [], already_get


class Optional(BaseParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self):
        success, result, already_get = self.parser()
        if success:
            if not already_get:
                analyzer.new_lex()
            return True, result, True
        return True, [], True


class Many(BaseParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self):
        results = []
        while True:
            success, result, already_get = self.parser()
            if success:
                if not already_get:
                    analyzer.new_lex()
                results.extend(result)
            else:
                break

        return True, results, True


class AtLeastOnce(BaseParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self):
        results = []
        first_success = False
        while True:
            success, result, already_get = self.parser()
            if success:
                first_success = True
                results.extend(result)
                if not already_get:
                    analyzer.new_lex()
            else:
                if first_success:
                    return True, result, True
                else:
                    return False, result, True


class LexParser(BaseParser):
    lex: Lex

    def __init__(self, lex: Lex):
        self.lex = lex

    def __call__(self):
        lexeme = analyzer.get_lex()
        if lexeme.lex == self.lex:
            return True, [lexeme], False
        return False, [], False


class TypeParser(BaseParser):

    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_INT) |
                LexParser(Lex.KEYWORD_FLOAT) |
                LexParser(Lex.KEYWORD_BOOL)
        )()


class DefineOperatorParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                TypeParser() &
                LexParser(Lex.IDENTIFIER) &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        LexParser(Lex.IDENTIFIER)
                ).many()
        )()


class OperatorParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                CombineOperatorParser() |
                AssignmentOperatorParser() |
                BranchOperatorParser() |
                ForLoopOperatorParser() |
                WhileLoopOperatorParser() |
                InputOperatorParser() |
                OutputOperatorParser()
        )()


class CombineOperatorParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_BEGIN) &
                OperatorParser() &
                (
                        LexParser(Lex.SEPARATOR_SEMICOLON) &
                        OperatorParser()
                ).many() &
                LexParser(Lex.KEYWORD_END)
        )()


class OperationSumGroupParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.SEPARATOR_PLUS) | LexParser(Lex.SEPARATOR_MINUS) | LexParser(Lex.SEPARATOR_OR)
        )()


class OperationMulGroupParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.SEPARATOR_MULTIPLICATION) |
                LexParser(Lex.SEPARATOR_DIVISION) |
                LexParser(Lex.SEPARATOR_AND)
        )()


class OperationRelationGroupParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.SEPARATOR_NOT_EQUALS) |
                LexParser(Lex.SEPARATOR_EQUALS) |
                LexParser(Lex.SEPARATOR_LT) |
                LexParser(Lex.SEPARATOR_LTE) |
                LexParser(Lex.SEPARATOR_GT) |
                LexParser(Lex.SEPARATOR_GTE)
        )()


class SumParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                MulParser() &
                (
                        OperationSumGroupParser() &
                        MulParser()
                ).many()
        )()


class NumberParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.NUMBER_BIN) |
                LexParser(Lex.NUMBER_OCT) |
                LexParser(Lex.NUMBER_HEX) |
                LexParser(Lex.NUMBER_DEC) |
                LexParser(Lex.NUMBER_FRACTIONAL)
        )()


class BoolConstantParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_TRUE) |
                LexParser(Lex.KEYWORD_FALSE)
        )()


class MulParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                FactorParser() &
                (
                        OperationMulGroupParser() &
                        FactorParser()
                ).many()
        )()


class FactorParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.IDENTIFIER) |
                NumberParser() |
                BoolConstantParser() |
                (LexParser(Lex.SEPARATOR_NOT) & FactorParser()) |
                (
                        LexParser(Lex.SEPARATOR_LEFT_BRACKET) &
                        ExpressionParser() &
                        LexParser(Lex.SEPARATOR_RIGHT_BRACKET)
                )
        )()


class ExpressionParser(BaseParser):
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                SumParser() &
                (
                        OperationRelationGroupParser() &
                        SumParser()
                ).many()
        )()


class AssignmentOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.IDENTIFIER) &
                LexParser(Lex.SEPARATOR_ASSIGNMENT) &
                ExpressionParser()
        )()


class BranchOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_IF) &
                LexParser(Lex.SEPARATOR_LEFT_BRACKET) &
                ExpressionParser() &
                LexParser(Lex.SEPARATOR_RIGHT_BRACKET) &
                OperatorParser() &
                (
                        LexParser(Lex.KEYWORD_ELSE) & OperatorParser
                ).opt()
        )()


class ForLoopOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_FOR) &
                AssignmentOperatorParser() &
                LexParser(Lex.KEYWORD_TO) &
                ExpressionParser() &
                (
                        LexParser(Lex.KEYWORD_STEP) &
                        ExpressionParser()
                ).opt() &
                OperatorParser() &
                LexParser(Lex.KEYWORD_NEXT)
        )()


class WhileLoopOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_WHILE) &
                LexParser(Lex.SEPARATOR_LEFT_BRACKET) &
                ExpressionParser() &
                LexParser(Lex.SEPARATOR_RIGHT_BRACKET) &
                OperatorParser()
        )()


class InputOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_READLN) &
                LexParser(Lex.IDENTIFIER) &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        LexParser(Lex.IDENTIFIER)
                ).many()
        )()


class OutputOperatorParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.KEYWORD_WRITELN) &
                ExpressionParser() &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        ExpressionParser()
                ).many()
        )()


class ProgramParser:
    @callback(callback_func=simple_callback)
    def __call__(self):
        return (
                LexParser(Lex.SEPARATOR_LEFT_FIGURE_BRACKET) &
                (
                        (
                                DefineOperatorParser() |
                                OperatorParser()
                        ) &
                        LexParser(Lex.SEPARATOR_SEMICOLON)
                ).at_least_once() &
                LexParser(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)
        )()
