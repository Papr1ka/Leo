from typing import Generator

from src.constants import LangSyntaxException, Lex, Lexeme
from src.lexer import Lexer
from src.parser.parsers import init, ProgramParser
from src.tree import Tree


class SyntaxParser:
    lexer: Generator
    lexeme: Lexeme
    tree: Tree

    def __init__(self, lexer: Lexer):
        self.lexer = iter(lexer.get_lex())
        self.lexeme = None
        self.tree = Tree(None)

    def throw_error(self, message: str):
        raise LangSyntaxException(message, self.lexeme.line, self.lexeme.symbol)

    def new_lex(self):
        try:
            self.lexeme = next(self.lexer)
        except StopIteration:
            if self.lexeme.lex != Lex.SEPARATOR_RIGHT_FIGURE_BRACKET:
                self.throw_error("Программа должна завершаться символом '}'")
        else:
            return self.lexeme

    def get_lex(self):
        return self.lexeme

    def parse(self):
        init(self)
        self.new_lex()
        parser = ProgramParser()
        out = parser()
        print(out)
