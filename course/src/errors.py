from .constants import Lex, Lexeme, semantic
from .text_driver import highlight

def lex_error(lex: Lexeme):
    highlight(lex.line, lex.symbol)
    print(f"Лексическая ошибка: '{lex.value}', Строка {lex.line}, Символ {lex.symbol} - {lex.error}")
    exit(1)


def expected(exp: Lex, actual: Lexeme):
    highlight(actual.line, actual.symbol)
    print(
        f"Синтаксическая ошибка: ожидалось - '{semantic.get(exp)}', обнаружено - '{actual.value}' Строка {actual.line}, Символ {actual.symbol}")
    exit(2)


def expected_msg(msg: str, actual: Lexeme):
    highlight(actual.line, actual.symbol)
    print(
        f"Синтаксическая ошибка: ожидалось - {msg}, обнаружено - '{actual.value}' Строка {actual.line}, Символ {actual.symbol}")
    exit(2)


def ctx_error(msg: str, lex: Lexeme):
    highlight(lex.line, lex.symbol)
    print(f"Контекстная ошибка: {msg} ('{lex.value}' Строка {lex.line}, Символ {lex.symbol})")
    exit(3)
