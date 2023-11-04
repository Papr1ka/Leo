from typing import Generator

from src.constants import LangSyntaxException, Lex, Lexeme
from src.lang.lang_base_types import Boolean, Float, Integer
from src.lexer import Lexer
from src.tree import Tree


class SyntaxParser:
    lexer: Generator
    lexeme: Lexeme
    tree: Tree

    def __init__(self, lexer: Lexer):
        self.lexer = iter(lexer.get_lex())
        self.lexer.send(None)
        self.tree = Tree(None)

    def throw_error(self, message: str):
        raise LangSyntaxException(message, self.lexeme.line, self.lexeme.symbol)

    def get_lex(self):
        try:
            self.lexeme = next(self.lexer)
        except StopIteration:
            if self.lexeme.lex != Lex.SEPARATOR_RIGHT_FIGURE_BRACKET:
                self.error("Программа должна завершаться символом '}'")
        else:
            return self.lexeme

    def define(self):
        if self.lexeme.lex == Lex.KEYWORD_INT:
            type = Integer
        elif self.lexeme.lex == Lex.KEYWORD_FLOAT:
            type = Float
        elif self.lexeme.lex == Lex.KEYWORD_BOOL:
            type = Boolean
        else:

    def start(self):
        self.get_lex()
        if self.lexeme.lex != Lex.SEPARATOR_LEFT_FIGURE_BRACKET:
            self.error("Программа должна начинаться с символа '{'")
        self.get_lex()

    def parse(self):
        self.program()
