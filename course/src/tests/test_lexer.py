from unittest import TestCase
from ..lexer import Lexer
from ..constants import Lex

class TestLexer(TestCase):

    def test_lex_numbers(self):

        # import os
        # print(os.path.abspath(os.path.relpath(os.curdir)))

        # Файл с заранее известными числами и заранее известным порядком этих чисел
        with open("./src/tests/test_numbers.txt") as file:
            data = "".join(file.readlines())

        lexer = Lexer(data).get_lex()
        g = iter(lexer)

        # print(next(lexer.get_lex())[0:2])
        # Двоичные числа и их ошибки
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_BIN, '0110b'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_BIN, '0110B'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110c'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0120B'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110BB'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110HB'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110DB'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110HB'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '0110OB'))

        # Восьмиричные числа и их ошибки
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_OCT, '2352270o'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_OCT, '2352270O'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123456BO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123456DO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '2352270c'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '2352280O'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123BO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123DO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123OO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123HO'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123OH'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123O0'))

        # Десятичные числа и их ошибки
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '123'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '123d'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '123D'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '98765'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '01234'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '213AD'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123bd'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123DD'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123dd'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123ED'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '321D0'))

        # Шестнадцатиричные числа и их ошибки (также распознавания как идентификаторов)
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123h'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1B0E0CH'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1FFFH'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '0000H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1000h'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '9E00H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1D0B0H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1B0D0h'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1BH'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '1DH'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123Hh'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123HH'))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, 'FFFFH'))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, 'DE0H'))

        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123e10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123e+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123e-10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123E10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123E+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123E-10'))

        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '1123ee10'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123ee+10'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '213Ee-10'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123Ee'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123e'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '..123e'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123..123e'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123.e'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123.e.'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '123.e.10'))


        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '123'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, 'e10'))

        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, '123'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, 'e10'))

        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123e10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123e+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123e-10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123E10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123E+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123.123E-10'))

        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123e10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123e+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123e-10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123E10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123E+10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '.123E-10'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_FRACTIONAL, '123E-10'))

        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123EB10H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123ED10H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123E10H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123E90H'))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, '123EBBD0H'))

    def test_lex_separators(self):
        with open("./src/tests/test_separators.txt") as file:
            data = "".join(file.readlines())

        lexer = Lexer(data).get_lex()
        g = iter(lexer)

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, '!='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '=!'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, '!'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, '!='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, '!='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '=!'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_EQUALS, '=='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_EQUALS, '=='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, '!='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '=<'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, '!='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GTE, '>='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GTE, '>='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GTE, '>='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GTE, '>='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '=>'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '='))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '=>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LT, '<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LTE, '<='))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_GT, '>'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, '*'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MINUS, '-'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_PLUS, '+'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, '('))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, '/'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ')'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_OR, '||'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '|='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '|'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_OR, '||'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '|'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '|<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_OR, '||'))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_AND, '&&'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '&='))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '&'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_AND, '&&'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '&'))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, '&<'))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_AND, "&&"))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, ":"))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, "::"))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, "="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_EQUALS, "=="))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, ":"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, ":"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, "!="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, "!="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_ASSIGNMENT, ":="))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, ":!"))
        self.assertEqual(next(g)[0:2], (Lex.UNRESOLVED, "="))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_SEMICOLON, ";"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_SEMICOLON, ";"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_SEMICOLON, ";"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_SEMICOLON, ";"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_SEMICOLON, ";"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_MULTIPLICATION, "*"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_DIVISION, "/"))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "abcd"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_END, "end"))

        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "a"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "b"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "a"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "b"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "a"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "b"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT, "!"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_NOT_EQUALS, "!="))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_EQUALS, "=="))

    def test_line_symbols(self):
        with open("./src/tests/test_line_symbols.txt") as file:
            data = "".join(file.readlines())

        lexer = Lexer(data).get_lex()
        g = iter(lexer)
        self.assertEqual(next(g)[2:4], (1, 1))

        self.assertEqual(next(g)[2:4], (2, 5))
        self.assertEqual(next(g)[2:4], (2, 9))
        self.assertEqual(next(g)[2:4], (2, 25))
        self.assertEqual(next(g)[2:4], (2, 27))
        self.assertEqual(next(g)[2:4], (2, 33))
        self.assertEqual(next(g)[2:4], (2, 35))
        self.assertEqual(next(g)[2:4], (2, 36))
        self.assertEqual(next(g)[2:4], (2, 38))
        self.assertEqual(next(g)[2:4], (2, 39))

        self.assertEqual(next(g)[2:4], (4, 5))
        self.assertEqual(next(g)[2:4], (4, 22))
        self.assertEqual(next(g)[2:4], (4, 25))
        self.assertEqual(next(g)[2:4], (4, 27))

        self.assertEqual(next(g)[2:4], (5, 5))
        self.assertEqual(next(g)[2:4], (5, 12))
        self.assertEqual(next(g)[2:4], (5, 15))
        self.assertEqual(next(g)[2:4], (5, 16))

        self.assertEqual(next(g)[2:4], (7, 5))
        self.assertEqual(next(g)[2:4], (7, 11))
        self.assertEqual(next(g)[2:4], (7, 12))
        self.assertEqual(next(g)[2:4], (7, 29))
        self.assertEqual(next(g)[2:4], (7, 31))
        self.assertEqual(next(g)[2:4], (7, 32))

        self.assertEqual(next(g)[2:4], (8, 5))

        self.assertEqual(next(g)[2:4], (9, 5))
        self.assertEqual(next(g)[2:4], (9, 12))
        self.assertEqual(next(g)[2:4], (9, 15))
        self.assertEqual(next(g)[2:4], (9, 22))
        self.assertEqual(next(g)[2:4], (9, 24))
        self.assertEqual(next(g)[2:4], (9, 25))

        self.assertEqual(next(g)[2:4], (10, 5))
        self.assertEqual(next(g)[2:4], (10, 7))
        self.assertEqual(next(g)[2:4], (10, 10))
        self.assertEqual(next(g)[2:4], (10, 11))

        self.assertEqual(next(g)[2:4], (12, 5))
        self.assertEqual(next(g)[2:4], (12, 9))
        self.assertEqual(next(g)[2:4], (12, 11))
        self.assertEqual(next(g)[2:4], (12, 14))
        self.assertEqual(next(g)[2:4], (12, 16))
        self.assertEqual(next(g)[2:4], (12, 19))
        self.assertEqual(next(g)[2:4], (12, 26))
        self.assertEqual(next(g)[2:4], (12, 31))

        self.assertEqual(next(g)[2:4], (13, 5))

        self.assertEqual(next(g)[2:4], (15, 5))
        self.assertEqual(next(g)[2:4], (15, 8))
        self.assertEqual(next(g)[2:4], (15, 9))
        self.assertEqual(next(g)[2:4], (15, 16))
        self.assertEqual(next(g)[2:4], (15, 18))
        self.assertEqual(next(g)[2:4], (15, 20))
        self.assertEqual(next(g)[2:4], (15, 22))
        self.assertEqual(next(g)[2:4], (15, 24))
        self.assertEqual(next(g)[2:4], (15, 27))
        self.assertEqual(next(g)[2:4], (15, 33))
        self.assertEqual(next(g)[2:4], (15, 35))
        self.assertEqual(next(g)[2:4], (15, 37))
        self.assertEqual(next(g)[2:4], (15, 40))
        self.assertEqual(next(g)[2:4], (15, 42))
        self.assertEqual(next(g)[2:4], (15, 44))

        self.assertEqual(next(g)[2:4], (17, 5))

        self.assertEqual(next(g)[2:4], (18, 5))
        self.assertEqual(next(g)[2:4], (18, 9))

        self.assertEqual(next(g)[2:4], (20, 5))
        self.assertEqual(next(g)[2:4], (20, 8))
        self.assertEqual(next(g)[2:4], (20, 9))
        self.assertEqual(next(g)[2:4], (20, 11))
        self.assertEqual(next(g)[2:4], (20, 14))
        self.assertEqual(next(g)[2:4], (20, 15))
        self.assertEqual(next(g)[2:4], (20, 17))
        self.assertEqual(next(g)[2:4], (20, 34))
        self.assertEqual(next(g)[2:4], (20, 37))
        self.assertEqual(next(g)[2:4], (20, 54))
        self.assertEqual(next(g)[2:4], (20, 56))

        self.assertEqual(next(g)[2:4], (22, 5))
        self.assertEqual(next(g)[2:4], (22, 8))

        self.assertEqual(next(g)[2:4], (35, 5))
        self.assertEqual(next(g)[2:4], (35, 13))
        self.assertEqual(next(g)[2:4], (35, 19))

        self.assertEqual(next(g)[2:4], (36, 1))

    def test_lex_identifiers_separators(self):
        with open("./src/tests/test_separators_context.txt") as file:
            data = "".join(file.readlines())

        lexer = Lexer(data).get_lex()
        g = iter(lexer)

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "1"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, "0H"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_HEX, "0H"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))

        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "I"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_FIGURE_BRACKET, "{"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_LEFT_BRACKET, "("))
        self.assertEqual(next(g)[0:2], (Lex.NUMBER_DEC, "0"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_BRACKET, ")"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_RIGHT_FIGURE_BRACKET, "}"))

    def test_lex_keywords(self):
        with open("./src/tests/test_keywords.txt") as file:
            data = "".join(file.readlines())

        lexer = Lexer(data).get_lex()
        g = iter(lexer)

        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_BEGIN, "begin"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_BOOL, "bool"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_ELSE, "else"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_END, "end"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FALSE, "false"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FLOAT, "float"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FOR, "for"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_IF, "if"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_INT, "int"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_NEXT, "next"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_READLN, "readln"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_STEP, "step"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_TO, "to"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_TRUE, "true"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_WHILE, "while"))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_WRITELN, "writeln"))


        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_BEGIN, "begin"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_BOOL, "bool"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_ELSE, "else"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_END, "end"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FALSE, "false"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FLOAT, "float"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_FOR, "for"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_IF, "if"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_INT, "int"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_NEXT, "next"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_READLN, "readln"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_STEP, "step"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_TO, "to"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_TRUE, "true"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_WHILE, "while"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))
        self.assertEqual(next(g)[0:2], (Lex.KEYWORD_WRITELN, "writeln"))
        self.assertEqual(next(g)[0:2], (Lex.SEPARATOR_COMMA, ","))





if __name__ == "__main__":
    TestLexer().run()
