from pprint import pprint
from typing import Any, List, Tuple

from src.constants import Lexeme
from src.lang import *

analyzer = None


def simple_callback(method, lexemes):
    if lexemes[0] and (
            isinstance(method, ExpressionParser) or
            isinstance(method, SumParser) or
            isinstance(method, MulParser) or
            isinstance(method, FactorParser) or
            isinstance(method, ExpressionInBracketsParser)
    ):
        print()
        print(method)
        # pprint(lexemes)
        pprint([i.value for i in lexemes])


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


class CombineParser(BaseParser):
    error_message: str = ""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def starts(self) -> BaseParser:
        pass

    def setup(self) -> BaseParser:
        return None

    def on_success(self, lexemes: List[Lexeme]):
        pass

    def on_error(self):
        analyzer.throw_error(self.error_message)

    def __call__(self):
        start_success, start_lexemes, start_flag = self.starts()()
        if not start_success:
            return start_success, start_lexemes, start_flag

        if not start_flag:
            analyzer.new_lex()

        body = self.setup()

        if body is None:
            self.on_success(start_lexemes)
            return start_success, start_lexemes, start_flag

        body_success, body_lexemes, body_flag = body()

        lexemes = [*start_lexemes, *body_lexemes]

        if body_success:
            if not body_flag:
                analyzer.new_lex()
            self.on_success(lexemes)
            return True, lexemes, True
        else:
            self.on_error()
            return False, lexemes, True


class TypeParser(CombineParser):

    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.KEYWORD_INT) |
                LexParser(Lex.KEYWORD_FLOAT) |
                LexParser(Lex.KEYWORD_BOOL)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class DefineOperatorParser(CombineParser):
    error_message = "Ожидалось перечисление идентификаторов для объявления"

    def starts(self) -> BaseParser:
        return TypeParser()

    def setup(self) -> BaseParser:
        return (
                LexParser(Lex.IDENTIFIER) &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        LexParser(Lex.IDENTIFIER)
                ).many()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class OperatorParser(CombineParser):
    error_message = "Ошибка в начале/конце оператора"

    def starts(self) -> BaseParser:
        return (
                CombineOperatorParser() |
                AssignmentOperatorParser() |
                BranchOperatorParser() |
                ForLoopOperatorParser() |
                WhileLoopOperatorParser() |
                InputOperatorParser() |
                OutputOperatorParser()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class CombineOperatorParser(CombineParser):
    error_message = "Неверно задан составной оператор"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_BEGIN)

    def setup(self) -> BaseParser:
        return (
                OperatorParser() &
                (
                        LexParser(Lex.SEPARATOR_SEMICOLON) &
                        OperatorParser()
                ).many() &
                LexParser(Lex.KEYWORD_END)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class OperationSumGroupParser(CombineParser):

    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_PLUS) | LexParser(Lex.SEPARATOR_MINUS) | LexParser(Lex.SEPARATOR_OR)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class OperationMulGroupParser(CombineParser):
    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_MULTIPLICATION) |
                LexParser(Lex.SEPARATOR_DIVISION) |
                LexParser(Lex.SEPARATOR_AND)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class OperationRelationGroupParser(CombineParser):
    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_NOT_EQUALS) |
                LexParser(Lex.SEPARATOR_EQUALS) |
                LexParser(Lex.SEPARATOR_LT) |
                LexParser(Lex.SEPARATOR_LTE) |
                LexParser(Lex.SEPARATOR_GT) |
                LexParser(Lex.SEPARATOR_GTE)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class SumParser(CombineParser):

    def starts(self) -> BaseParser:
        return MulParser()

    def setup(self) -> BaseParser:
        return (
                OperationSumGroupParser() &
                MulParser()
        ).many()

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class NumberParser(CombineParser):
    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.NUMBER_BIN) |
                LexParser(Lex.NUMBER_OCT) |
                LexParser(Lex.NUMBER_HEX) |
                LexParser(Lex.NUMBER_DEC) |
                LexParser(Lex.NUMBER_FRACTIONAL)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class BoolConstantParser(CombineParser):
    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.KEYWORD_TRUE) |
                LexParser(Lex.KEYWORD_FALSE)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class MulParser(CombineParser):
    def starts(self) -> BaseParser:
        return FactorParser()

    def setup(self) -> BaseParser:
        return (
                OperationMulGroupParser() &
                FactorParser()
        ).many()

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class ExpressionInBracketsParser(CombineParser):
    error_message = "В скобках ожидалось выражение"

    def starts(self) -> BaseParser:
        return LexParser(Lex.SEPARATOR_LEFT_BRACKET)

    def setup(self) -> BaseParser:
        return (
                ExpressionParser() &
                LexParser(Lex.SEPARATOR_RIGHT_BRACKET)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class NotOperatorParser(CombineParser):
    error_message = "Ожидался операнд"

    def starts(self) -> BaseParser:
        return LexParser(Lex.SEPARATOR_NOT)

    def setup(self) -> BaseParser:
        return FactorParser()

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class FactorParser(CombineParser):
    def starts(self) -> BaseParser:
        return (
                LexParser(Lex.IDENTIFIER) |
                NumberParser() |
                BoolConstantParser() |
                NotOperatorParser() |
                ExpressionInBracketsParser()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class ExpressionParser(CombineParser):
    def starts(self) -> BaseParser:
        return SumParser()

    def setup(self) -> BaseParser:
        return (
                OperationRelationGroupParser() &
                SumParser()
        ).many()

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class AssignmentOperatorParser(CombineParser):
    error_message = "Ошибка в операторе присваивания"

    def starts(self) -> BaseParser:
        return LexParser(Lex.IDENTIFIER)

    def setup(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_ASSIGNMENT) &
                ExpressionParser()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class BranchOperatorParser(CombineParser):
    error_message = "Неверно задан условный оператор"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_IF)

    def setup(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_LEFT_BRACKET) &
                ExpressionParser() &
                LexParser(Lex.SEPARATOR_RIGHT_BRACKET) &
                OperatorParser() &
                (
                        LexParser(Lex.KEYWORD_ELSE) & OperatorParser()
                ).opt()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class ForLoopOperatorParser(CombineParser):
    error_message = "Неверно задан оператор цикла со счётчиком"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_FOR)

    def setup(self) -> BaseParser:
        return (
                AssignmentOperatorParser() &
                LexParser(Lex.KEYWORD_TO) &
                ExpressionParser() &
                (
                        LexParser(Lex.KEYWORD_STEP) &
                        ExpressionParser()
                ).opt() &
                OperatorParser() &
                LexParser(Lex.KEYWORD_NEXT)
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class WhileLoopOperatorParser(CombineParser):
    error_message = "Неверно задан цикл с предусловием"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_WHILE)

    def setup(self) -> BaseParser:
        return (
                LexParser(Lex.SEPARATOR_LEFT_BRACKET) &
                ExpressionParser() &
                LexParser(Lex.SEPARATOR_RIGHT_BRACKET) &
                OperatorParser()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class InputOperatorParser(CombineParser):
    error_message = "Неверно задан оператор ввода, ожидался идентификатор"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_READLN)

    def setup(self) -> BaseParser:
        return (
                LexParser(Lex.IDENTIFIER) &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        LexParser(Lex.IDENTIFIER)
                ).many()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class OutputOperatorParser(CombineParser):
    error_message = "Неверно задан оператор вывода, ожидалось выражение"

    def starts(self) -> BaseParser:
        return LexParser(Lex.KEYWORD_WRITELN)

    def setup(self) -> BaseParser:
        return (
                ExpressionParser() &
                (
                        LexParser(Lex.SEPARATOR_COMMA) &
                        ExpressionParser()
                ).many()
        )

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)


class ProgramParser(CombineParser):
    error_message = "Операторы должны разделяться символом ';'"

    def starts(self) -> BaseParser:
        return LexParser(Lex.SEPARATOR_LEFT_FIGURE_BRACKET)

    def setup(self):
        return (
                (
                        (
                                DefineOperatorParser() |
                                OperatorParser()
                        ) &
                        LexParser(Lex.SEPARATOR_SEMICOLON)
                ).at_least_once() &
                LexParser(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)
        )

    def __call__(self):
        start_success, start_lexemes, start_flag = self.starts()()
        if not start_success:
            analyzer.throw_error("Программа должна начинаться с символа '{'")
            return start_success, start_lexemes, start_flag

        if not start_flag:
            analyzer.new_lex()

        body = self.setup()

        if body is None:
            self.on_success(start_lexemes)
            return start_success, start_lexemes, start_flag

        body_success, body_lexemes, body_flag = body()

        lexemes = [*start_lexemes, *body_lexemes]

        if body_success:
            if not body_flag:
                analyzer.new_lex()
            self.on_success(lexemes)
            return True, lexemes, True
        else:
            self.on_error()
            return False, lexemes, True

    def on_success(self, lexemes: List[Lexeme]):
        simple_callback(self, lexemes)
