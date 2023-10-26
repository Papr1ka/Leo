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
    DELIM = 50

    #Состояния завершения разбора лексемы
    NUMBER_BIN_END = -1
    NUMBER_OCT_END = -2
    NUMBER_DEC_END = -3
    NUMBER_HEX_END = -4
    NUMBER_ORDER_END = -5
    SEPARATOR_LEFT_BRACKET_END = -6
    SEPARATOR_RIGHT_BRACKET_END = -7
    SEPARATOR_PLUS_END = -8
    SEPARATOR_MINUS_END = -9
    SEPARATOR_MULTIPLICATION_END = -10
    SEPARATOR_DIVISION_END = -11
    SEPARATOR_LEFT_FIGURE_BRACKET_END = -12
    SEPARATOR_RIGHT_FIGURE_BRACKET_END = -13
    SEPARATOR_SEMICOLON_END = -14
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
