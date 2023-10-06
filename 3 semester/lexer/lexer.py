from enum import Enum
from re import fullmatch
from typing import List, Union

regex_number = r"[-+]?[0-9]*e?\.?[0-9]*"

KEYWORDS = (
    "for",
    "do"
)

separators = (
    '(',
    ')',
    ' ',
    '\t',
    ';',
    ':'
)

def is_number(number: str):
    return (fullmatch(regex_number, number) is not None) and (number.count('E') + number.count('e') <= 1)

class State(Enum):
    h = 1
    id = 2
    nm = 3
    asgn = 4
    dlm = 5
    err = 6

class Lex(Enum):
    keyword = 1
    delimiter = 2
    operation = 3
    identificator = 4
    number = 5

class Token:
    type: Lex
    content: str
    line: int
    position: int
    linePosition: int

    def __init__(self, type: Lex, content: str, line: int, position: int, linePosition: int):
        self.type = type
        self.content = content
        self.line = line
        self.position = position
        self.linePosition = linePosition
    def __str__(self):
        return f"Token {self.content}, type {self.type}, line {self.line}, symbol {self.linePosition}"
    def __repr__(self):
        return self.__str__()

class Lexer():
    def __init__(self):
        self.__state = State.h
        self.__lineNumber = 1
        self.__tokens = []
        self.__position = 1
        self.__linePosition = 0
        self.__buffer = ""
        self.__lexStartPosition = 0

    def addToken(self, tokenType: Lex):
        token = Token(
            tokenType,
            self.__buffer,
            self.__lineNumber,
            self.__position,
            self.__lexStartPosition,
        )
        self.__tokens.append(token)
        self.__position += 1
        self.__buffer = ""

    def parseLine(self, line: str) -> Union[Token, None]:
        line += " "
        def ungetSymbol():
            self.__linePosition -= 1
            return line[self.__linePosition]
        def getSymbol():
            symbol = line[self.__linePosition]
            self.__linePosition += 1
            return symbol

        while self.__linePosition < len(line):
            if self.__state == State.err:
                print("Error in token:", self.__tokens[-1])
                self.__state = State.h

            symbol = getSymbol()

            if self.__state == State.h:
                if symbol in (' ', '\t'):
                    continue

                self.__buffer += symbol
                self.__lexStartPosition = self.__linePosition

                if symbol.isalpha() or symbol == '_':
                    self.__state = State.id
                elif symbol.isdigit() or symbol in ('.', '+', '-'):
                    self.__state = State.nm
                elif symbol == ':':
                    self.__state = State.asgn
                else:
                    self.__state = State.dlm
                    ungetSymbol()

            elif self.__state == State.asgn:
                if symbol == '=':
                    self.__buffer += symbol
                    self.addToken(Lex.operation)
                    self.__state = State.h
                else:
                    self.__state = State.err

            elif self.__state == State.dlm:
                if symbol in ('(', ')', ';', '<', '>', '='):
                    self.addToken(Lex.delimiter)
                    self.__state = State.h
                else:
                    self.addToken(Lex.delimiter)
                    self.__state = State.err

            elif self.__state == State.id:
                if not (symbol.isalpha() or symbol.isdigit() or symbol == '_'):
                    self.addToken(Lex.identificator)
                    self.__state = State.h
                    ungetSymbol()
                else:
                    self.__buffer += symbol

            elif self.__state == State.nm:
                if not (symbol.isdigit() or symbol in ('+', '-', 'e', 'E', '.')):
                    number = self.__buffer
                    self.addToken(Lex.number)
                    if symbol in separators:
                        if is_number(number):
                            self.__state = State.h
                            ungetSymbol()
                        else:
                            self.__state = State.err
                    else:
                        self.__state = State.err
                    self.__buffer = ""
                else:
                    self.__buffer += symbol

        self.__linePosition = 0
        self.__buffer = ""

    def parse(self, document: List[str]):
        for i in range(len(document)):
            self.__lineNumber = i + 1
            err = self.parseLine(document[i])
            if err is not None:
                print(document[i])
                print(f"{'' * (err.linePosition - 2)}^")

        return self.__tokens
