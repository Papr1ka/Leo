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
        self.assertEqual(next(g)[0:2], (Lex.IDENTIFIER, "end"))

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





if __name__ == "__main__":
    TestLexer().run()
