from .constants import Lex, Lexeme, semantic
from .text_driver import highlight, get_filename

first_string = 'Файл "{}", Строка {}, Символ {}'


def error(message: str, line: int, symbol: int, exit_code: int):
    print(first_string.format(get_filename(), line, symbol))
    highlight(line, symbol)
    print(message)
    exit(exit_code)


def lex_error(lex: Lexeme):
    error(f"Лексическая ошибка: '{lex.value}' - {lex.error}", lex.line, lex.symbol, 1)


def expected(exp: Lex, actual: Lexeme):
    error(f"Синтаксическая ошибка: ожидалось - '{semantic.get(exp)}', получено - {semantic.get(actual.lex)}",
          actual.line, actual.symbol, 2)


def expected_msg(msg: str, actual: Lexeme):
    error(f"Синтаксическая ошибка: ожидалось - '{msg}', получено - {semantic.get(actual.lex)}",
          actual.line, actual.symbol, 2)


def ctx_error(msg: str, lex: Lexeme):
    error(f"Контекстная ошибка: '{lex.value}' - {msg}",
          lex.line, lex.symbol, 3)
