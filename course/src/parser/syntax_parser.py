from typing import Generator

from src.constants import Lex, Lexeme
from src.errors import expected, expected_msg
from src.lexer import Lexer
from src.tree import Tree


class SyntaxParser:
    lexer: Generator
    lexeme: Lexeme
    tree: Tree

    def __init__(self, lexer: Lexer):
        self.lexer = iter(lexer.get_lex())
        self.lexeme = self.new_lex()
        self.tree = Tree(None)

    def new_lex(self):
        try:
            self.lexeme = next(self.lexer)
        except StopIteration:
            pass
        else:
            return self.lexeme

    def skip(self):
        pass

    def get_lex(self):
        return self.lexeme

    def skip_lex(self, lex: Lex):
        if self.lexeme.lex == lex:
            self.new_lex()
        else:
            expected(lex, self.lexeme)

    def parse(self):
        self.program_parser()

    def identifier_declaration(self, type: Lex, identifier: Lexeme):
        # лексему берём из self.lexeme
        pass

    def description_parser(self):
        if self.lexeme.lex not in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            expected_msg("Тип", self.lexeme)

        identifier_type = self.lexeme.lex
        self.new_lex()
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        self.identifier_declaration(identifier_type, self.lexeme)
        self.new_lex()

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)

            self.identifier_declaration(identifier_type, self.lexeme)
            self.new_lex()

    def operator_combine_parser(self):
        self.skip_lex(Lex.KEYWORD_BEGIN)
        self.operator_parser()
        while self.lexeme.lex == Lex.SEPARATOR_SEMICOLON:
            self.new_lex()
            self.operator_parser()

        self.skip_lex(Lex.KEYWORD_END)

    def identifier_assignment(self, identifier: Lexeme):
        pass

    def factor_parser(self):
        if self.lexeme.lex in (Lex.IDENTIFIER, Lex.NUMBER_BIN, Lex.NUMBER_OCT,
                               Lex.NUMBER_DEC, Lex.NUMBER_HEX, Lex.NUMBER_FRACTIONAL,
                               Lex.KEYWORD_TRUE, Lex.KEYWORD_FALSE, Lex.SEPARATOR_NOT,
                               Lex.SEPARATOR_LEFT_BRACKET):
            if self.lexeme == Lex.SEPARATOR_NOT:
                self.new_lex()
                if self.lexeme.lex != Lex.IDENTIFIER:
                    expected(Lex.IDENTIFIER, self.lexeme)

                identifier = self.lexeme
                self.new_lex()
            elif self.lexeme.lex == Lex.SEPARATOR_LEFT_BRACKET:
                self.new_lex()
                self.expression_parser()
                self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
            else:
                factor = self.lexeme
                self.new_lex()
        else:
            expected_msg("Множитель", self.lexeme)

    def multiplication_parser(self):
        self.factor_parser()
        while self.lexeme.lex in (Lex.SEPARATOR_MULTIPLICATION, Lex.SEPARATOR_DIVISION, Lex.SEPARATOR_AND):
            operation = self.lexeme.lex
            self.new_lex()
            self.factor_parser()

    def summa_parser(self):
        self.multiplication_parser()
        while self.lexeme.lex in (Lex.SEPARATOR_PLUS, Lex.SEPARATOR_MINUS, Lex.SEPARATOR_OR):
            operation = self.lexeme.lex
            self.new_lex()
            self.multiplication_parser()

    def expression_parser(self):
        self.summa_parser()
        while self.lexeme.lex in (Lex.SEPARATOR_EQUALS, Lex.SEPARATOR_NOT_EQUALS, Lex.SEPARATOR_LT,
                                  Lex.SEPARATOR_LTE, Lex.SEPARATOR_GT, Lex.SEPARATOR_GTE):
            operation = self.lexeme.lex
            self.new_lex()
            self.summa_parser()

    def operator_assignment_parser(self):
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.new_lex()
        self.skip_lex(Lex.SEPARATOR_ASSIGNMENT)
        self.expression_parser()

    def operator_if_parser(self):
        self.skip_lex(Lex.KEYWORD_IF)
        self.skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        self.expression_parser()
        self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        self.operator_parser()
        if self.lexeme == Lex.KEYWORD_ELSE:
            self.new_lex()
            self.operator_parser()

    def operator_for_parser(self):
        self.skip_lex(Lex.KEYWORD_FOR)
        self.operator_assignment_parser()
        self.skip_lex(Lex.KEYWORD_TO)
        self.expression_parser()
        if self.lexeme.lex == Lex.KEYWORD_STEP:
            self.new_lex()
            self.expression_parser()

        self.operator_parser()
        self.skip_lex(Lex.KEYWORD_NEXT)

    def operator_while_parser(self):
        self.skip_lex(Lex.KEYWORD_WHILE)
        self.skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        self.expression_parser()
        self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        self.operator_parser()

    def operator_readln_parser(self):
        self.skip_lex(Lex.KEYWORD_READLN)
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.new_lex()

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)
            identifier = self.lexeme
            self.new_lex()

    def operator_writeln_parser(self):
        self.skip_lex(Lex.KEYWORD_WRITELN)
        self.expression_parser()

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            self.expression_parser()

    def operator_parser(self):
        if self.lexeme.lex == Lex.KEYWORD_BEGIN:
            self.operator_combine_parser()
        elif self.lexeme.lex == Lex.IDENTIFIER:
            self.operator_assignment_parser()
        elif self.lexeme.lex == Lex.KEYWORD_IF:
            self.operator_if_parser()
        elif self.lexeme.lex == Lex.KEYWORD_FOR:
            self.operator_for_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WHILE:
            self.operator_while_parser()
        elif self.lexeme.lex == Lex.KEYWORD_READLN:
            self.operator_readln_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WRITELN:
            self.operator_writeln_parser()
        else:
            expected_msg("Оператор", self.lexeme)

    def description_or_operator_seq(self):
        while self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL,
                                  Lex.KEYWORD_BEGIN, Lex.IDENTIFIER, Lex.KEYWORD_IF,
                                  Lex.KEYWORD_FOR, Lex.KEYWORD_WHILE, Lex.KEYWORD_READLN,
                                  Lex.KEYWORD_WRITELN):
            self.description_or_operator_parser()
            self.skip_lex(Lex.SEPARATOR_SEMICOLON)

    def description_or_operator_parser(self):
        if self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            self.description_parser()
        else:
            self.operator_parser()

    def program_parser(self):
        self.skip_lex(Lex.SEPARATOR_LEFT_FIGURE_BRACKET)

        self.description_or_operator_parser()
        self.skip_lex(Lex.SEPARATOR_SEMICOLON)

        self.description_or_operator_seq()

        self.skip_lex(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)

        print("Синтаксический анализ закончен")
