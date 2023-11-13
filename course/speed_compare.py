from time import time

from src.lexer import Lexer
from src.parser.parser import Parser
from src.python_translator.translator import translate
from src.text_driver import setup_source


def primes():
    primeNumberCount = 500
    number = 1
    while primeNumberCount > 0:
        number += 1
        j = 0
        for i in range(1, number + 1):
            if number % i == 0:
                j += 1

        if j == 2:
            primeNumberCount = primeNumberCount - 1
            print(number)


def main():
    primeNumberCount: int
    number: int
    j: int

    primeNumberCount = 500
    number = 1

    while (primeNumberCount > 0):
        number = (number + 1)
        j = 0

        for i in range(1, (number + 1), 1):

            if ((number % i) == 0):
                j = (j + 1)

        if (j == 2):
            primeNumberCount = (primeNumberCount - 1)
            print(number)


def test_for():
    j = 0
    for i in range(0, 1000000, 1):
        j += 1

    print(j)


def test_while():
    j = 0
    i = 0
    while i < 1000000:
        j += 1
        i += 1

    print(j)

if __name__ == '__main__':
    setup_source("examples/primes.leo")
    lexer = Lexer()

    parser = Parser(lexer)
    ast = parser.parse()
    q_0 = time()
    python = translate(ast)
    print(time() - q_0)

    r1 = []
    r2 = []

    for i in range(10):
        t_1_0 = time()
        # main()
        test_for()
        t_1_1 = time()
        t_2_0 = time()
        # primes()
        test_while()
        t_2_1 = time()
        t_1 = t_1_1 - t_1_0
        t_2 = t_2_1 - t_2_0
        r1.append(t_1)
        r2.append(t_2)

    avg1 = sum(r1) / len(r1)
    avg2 = sum(r2) / len(r2)
    print(f"Leo: {avg1} ms, Python: {avg2} ms")
    print(f"Leo/Python {avg1 / avg2}")
