from unittest import TestCase
from ..lexer import Lexer
from ..states import States

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
        self.assertEqual(next(g)[0:2], (States.NUMBERBIN, '0110b'))
        self.assertEqual(next(g)[0:2], (States.NUMBERBIN, '0110B'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110c'))
        self.assertEqual(next(g)[0:2], (States.ER, '0120B'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110BB'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110HB'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110DB'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110HB'))
        self.assertEqual(next(g)[0:2], (States.ER, '0110OB'))

        # Восьмиричные числа и их ошибки
        self.assertEqual(next(g)[0:2], (States.NUMBEROCT, '2352270o'))
        self.assertEqual(next(g)[0:2], (States.NUMBEROCT, '2352270O'))
        self.assertEqual(next(g)[0:2], (States.ER, '123456BO'))
        self.assertEqual(next(g)[0:2], (States.ER, '123456DO'))
        self.assertEqual(next(g)[0:2], (States.ER, '2352270c'))
        self.assertEqual(next(g)[0:2], (States.ER, '2352280O'))
        self.assertEqual(next(g)[0:2], (States.ER, '123BO'))
        self.assertEqual(next(g)[0:2], (States.ER, '123DO'))
        self.assertEqual(next(g)[0:2], (States.ER, '123OO'))
        self.assertEqual(next(g)[0:2], (States.ER, '123HO'))
        self.assertEqual(next(g)[0:2], (States.ER, '123OH'))
        self.assertEqual(next(g)[0:2], (States.ER, '123O0'))

        # Десятичные числа и их ошибки
        self.assertEqual(next(g)[0:2], (States.NUMBERDEC, '123'))
        self.assertEqual(next(g)[0:2], (States.NUMBERDEC, '123d'))
        self.assertEqual(next(g)[0:2], (States.NUMBERDEC, '123D'))
        self.assertEqual(next(g)[0:2], (States.NUMBERDEC, '98765'))
        self.assertEqual(next(g)[0:2], (States.NUMBERDEC, '01234'))
        self.assertEqual(next(g)[0:2], (States.ER, '213AD'))
        self.assertEqual(next(g)[0:2], (States.ER, '123bd'))
        self.assertEqual(next(g)[0:2], (States.ER, '123DD'))
        self.assertEqual(next(g)[0:2], (States.ER, '123dd'))
        self.assertEqual(next(g)[0:2], (States.ER, '123ED'))
        self.assertEqual(next(g)[0:2], (States.ER, '321D0'))

        # Шестнадцатиричные числа и их ошибки (также распознавания как идентификаторов)
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123h'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1B0E0CH'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1FFFH'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '0000H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1000h'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '9E00H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1D0B0H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1B0D0h'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1BH'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '1DH'))
        self.assertEqual(next(g)[0:2], (States.ER, '123Hh'))
        self.assertEqual(next(g)[0:2], (States.ER, '123HH'))
        self.assertEqual(next(g)[0:2], (States.IDENTIFICATOR, 'FFFFH'))
        self.assertEqual(next(g)[0:2], (States.IDENTIFICATOR, 'DE0H'))

        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123e10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123e+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123e-10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123E10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123E+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123E-10'))

        self.assertEqual(next(g)[0:2], (States.ER, '1123ee10'))
        self.assertEqual(next(g)[0:2], (States.ER, '123ee+10'))
        self.assertEqual(next(g)[0:2], (States.ER, '213Ee-10'))
        self.assertEqual(next(g)[0:2], (States.ER, '123Ee'))
        self.assertEqual(next(g)[0:2], (States.ER, '123e'))
        self.assertEqual(next(g)[0:2], (States.ER, '..123e'))
        self.assertEqual(next(g)[0:2], (States.ER, '123..123e'))
        self.assertEqual(next(g)[0:2], (States.ER, '123.e'))
        self.assertEqual(next(g)[0:2], (States.ER, '123.e.'))
        self.assertEqual(next(g)[0:2], (States.ER, '123.e.10'))
        self.assertEqual(next(g)[0:2], (States.ER, '123+e10'))
        self.assertEqual(next(g)[0:2], (States.ER, '123-e10'))

        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123e10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123e+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123e-10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123E10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123E+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123.123E-10'))

        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123e10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123e+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123e-10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123E10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123E+10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '.123E-10'))
        self.assertEqual(next(g)[0:2], (States.FRACTIONAL, '123E-10'))

        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123EB10H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123ED10H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123E10H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123E90H'))
        self.assertEqual(next(g)[0:2], (States.NUMBERHEX, '123EBBD0H'))

if __name__ == "__main__":
    TestLexer().run()
