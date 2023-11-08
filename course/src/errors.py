from .constants import Lex, Lexeme, semantic


def lex_error(lex: Lexeme):
    print(f"Лексическая ошибка: '{lex.value}', Строка {lex.line}, Символ {lex.symbol} - {lex.error}")
    exit(1)


def expected(exp: Lex, actual: Lexeme):
    print(
        f"Синтаксическая ошибка: ожидалось - '{semantic.get(exp)}', обнаружено - '{actual.value}' Строка {actual.line}, Символ {actual.symbol}")
    exit(2)


def expected_msg(msg: str, actual: Lexeme):
    print(
        f"Синтаксическая ошибка: ожидалось - {msg}, обнаружено - '{actual.value}' Строка {actual.line}, Символ {actual.symbol}")
    exit(2)
