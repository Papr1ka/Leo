# from src.states import States

from enum import Enum
from inspect import getgeneratorstate as ggs
from inspect import getgeneratorlocals as ggl
from src.handlers import HandlerFactory, States


# class States(Enum):
#     START = 0
#     NUMBER = 1
#     IDENT = 2
#     NUMBERORDER = 3
#     ER = -1

"""
simple grammar

IDENT:== LETTER{LETTER | DIGIT}

NUMBER:== {/DIGIT/}
"""

SEPARATORS = (
    " ",
    "\n",
    "\t"
)

def initialize(func):
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper

@initialize
def stateStart():
    while True:
        char: str = yield
        if char.isdigit():
            yield States.NUMBER
        elif char in ("e", "E"):
            yield States.NUMBER_ORDER
        elif char.isalpha():
            yield States.IDENT
        else:
            yield States.ER

@initialize
def stateIdent():
    while True:
        char: str = yield
        if char.isdigit() or char.isalnum():
            yield States.IDENT
        elif char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

@initialize
def stateNumber():
    while True:
        char: str = yield
        if char.isdigit():
            yield States.NUMBER
        elif char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

@initialize
def stateEr():
    while True:
        char: str = yield
        if char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

@initialize
def stateNumberOrder():
    state = 0
    while True:
        char: str = yield
        if state == 0:
            if char in ("+", "-"):
                yield States.NUMBER_ORDER
                state = 1
            elif char.isdigit():
                yield States.NUMBER_ORDER
                state = 2
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.NUMBER_ORDER
                state = 2
            else:
                yield States.ER
        elif state == 2:
            if char.isdigit():
                yield States.NUMBER_ORDER
            elif char in SEPARATORS:
                yield States.START
            else:
                yield States.ER

string_index = 0

states = {
    States.START: stateStart(),
    States.IDENT: stateIdent(),
    States.NUMBER: stateNumber(),
    States.ER: stateEr(),
    States.NUMBER_ORDER: stateNumberOrder(),
}

def getLex():
    string = "number 100 1qwe 100q lex 213211232 e-10 e+10 E10 e+123 E+e10\n"

    def getChar():
        global string_index
        if string_index >= len(string):
            raise StopIteration
        char = string[string_index]
        string_index += 1
        return char

    def ungetChar():
        global string_index
        if string_index > 0:
            string_index -= 1

    def handle(handler, char: str):
        ns = handler.send(char)
        return ns


    state = States.START
    buffer = ""

    factory = HandlerFactory()

    while True:

        try:
            char = getChar()
        except StopIteration:
            return

        if char not in SEPARATORS:
            buffer += char

        handler = factory.get_handler(state)

        if state == States.START:
            state = handle(handler, char)

        elif state == States.IDENT:
            state = handle(handler, char)

            if state == States.START:
                yield States.IDENT, buffer
                buffer = ""

        elif state == States.NUMBER:
            state = handle(handler, char)

            if state == States.START:
                yield States.NUMBER, buffer
                buffer = ""

        elif state == States.NUMBER_ORDER:
            state = handle(handler, char)

            if state == States.START:
                yield States.NUMBER_ORDER, buffer
                buffer = ""

        elif state == States.ER:
            state = handle(handler, char)
            if state == States.START:
                yield States.ER, buffer
                buffer = ""


def main():
    for lex in getLex():
        print(lex)

main()