from enum import Enum


class States(Enum):
    # Рабочие состояния
    ER = 0
    START = 1
    IDENTIFIER = 2
    NUMBER_BIN = 3
    NUMBER_OCT = 4
    NUMBER_DEC = 5
    NUMBER_HEX = 6
    NUMBER_ORDER = 7
    FRACTIONAL = 10
    LETTER_B = 11
    LETTER_D = 12
    LETTER_E = 13
    LETTER_H = 14
    LETTER_O = 15

    # Разделители
    SEPARATOR_NOT_EQUALS = 16
    SEPARATOR_EQUALS = 17
    SEPARATOR_LTE = 18
    SEPARATOR_GTE = 19
    SEPARATOR_OR = 20
    SEPARATOR_AND = 21
    SEPARATOR_ASSIGNMENT = 22
    SEPARATOR_LEFT_BRACKET = 23
    SEPARATOR_RIGHT_BRACKET = 24
    SEPARATOR_PLUS = 25
    SEPARATOR_MINUS = 26
    SEPARATOR_MULTIPLICATION = 27
    SEPARATOR_DIVISION = 28
    SEPARATOR_LEFT_FIGURE_BRACKET = 29
    SEPARATOR_RIGHT_FIGURE_BRACKET = 30
    SEPARATOR_SEMICOLON = 31
    SEPARATOR_NOT = 32
    SEPARATOR_LT = 33
    SEPARATOR_GT = 34
    SEPARATOR_COMMENT = 35
    DELIM = 50

    STATE_NULL = -1  # вспомогательное состояние, когда буфер накопился, но это не лексема (комментарий)


# Границы лексем, не накапливаемые в буфере
BASE_SEPARATORS = (
    " ",
    "\n",
    "\t"
)

# Границы лексем
SEPARATORS = (
    *BASE_SEPARATORS,
    "(",
    ")",
    "!",
    "=",
    "<",
    ">",
    "+",
    "-",
    "|",
    "*",
    "/",
    "&",
    "{",
    "}",
    ":",
    ";",
    ",",
)


class Lex(Enum):
    KEYWORD_BEGIN = 1
    KEYWORD_BOOL = 2
    KEYWORD_ELSE = 3
    KEYWORD_END = 4
    KEYWORD_FALSE = 5
    KEYWORD_FLOAT = 6
    KEYWORD_FOR = 7
    KEYWORD_IF = 8
    KEYWORD_INT = 9
    KEYWORD_NEXT = 10
    KEYWORD_READLN = 11
    KEYWORD_STEP = 12
    KEYWORD_TO = 13
    KEYWORD_TRUE = 14
    KEYWORD_WHILE = 15
    KEYWORD_WRITELN = 16

    IDENTIFIER = 17

    NUMBER_BIN = 18
    NUMBER_OCT = 19
    NUMBER_DEC = 20
    NUMBER_HEX = 21
    NUMBER_FRACTIONAL = 22

    SEPARATOR_AND = 23
    SEPARATOR_ASSIGNMENT = 24
    SEPARATOR_DIVISION = 25
    SEPARATOR_EQUALS = 26
    SEPARATOR_GT = 27
    SEPARATOR_GTE = 28
    SEPARATOR_LEFT_BRACKET = 29
    SEPARATOR_LEFT_FIGURE_BRACKET = 30
    SEPARATOR_LT = 31
    SEPARATOR_LTE = 32
    SEPARATOR_MINUS = 33
    SEPARATOR_MULTIPLICATION = 34
    SEPARATOR_NOT = 35
    SEPARATOR_NOT_EQUALS = 36
    SEPARATOR_OR = 37
    SEPARATOR_PLUS = 38
    SEPARATOR_RIGHT_BRACKET = 39
    SEPARATOR_RIGHT_FIGURE_BRACKET = 40
    SEPARATOR_SEMICOLON = 41
    SEPARATOR_COMMA = 42

    UNRESOLVED = 0


KEYWORDS = {
    'begin': Lex.KEYWORD_BEGIN,
    'bool': Lex.KEYWORD_BOOL,
    'else': Lex.KEYWORD_ELSE,
    'end': Lex.KEYWORD_END,
    'false': Lex.KEYWORD_FALSE,
    'float': Lex.KEYWORD_FLOAT,
    'for': Lex.KEYWORD_FOR,
    'if': Lex.KEYWORD_IF,
    'int': Lex.KEYWORD_INT,
    'next': Lex.KEYWORD_NEXT,
    'readln': Lex.KEYWORD_READLN,
    'step': Lex.KEYWORD_STEP,
    'to': Lex.KEYWORD_TO,
    'true': Lex.KEYWORD_TRUE,
    'while': Lex.KEYWORD_WHILE,
    'writeln': Lex.KEYWORD_WRITELN,
}
