from enum import Enum

class States(Enum):
    #Рабочие состояния
    START = 1
    IDENTIFIER = 2
    NUMBER_BIN = 3
    NUMBER_OCT = 4
    NUMBER_DEC = 5
    NUMBER_HEX = 6
    NUMBER_ORDER = 7
    FRACTIONAL = 10
    ER = 0
    LETTER_B = 11
    LETTER_D = 12
    LETTER_E = 13
    LETTER_H = 14
    LETTER_O = 15

    SEPARATOR_NOT_EQUALS = 16
    SEPARATOR_NOT = 32
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
    SEPARATOR_LT = 33
    SEPARATOR_GT = 34
    SEPARATOR_COMMENT = 35
    DELIM = 50

    STATE_NULL = -1 # вспомогательное состояние, когда буфер накопился, но это не лексема (комментарий)
    STATE_LEX_END_HELPER = -100
# Границы лексем, список пока простой (не полный)
BASE_SEPARATORS = (
    " ",
    "\n",
    "\t"
)

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
)

SEPARATORS_STATES = (
    States.DELIM,
    States.SEPARATOR_NOT
)
