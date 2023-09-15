from polish import ReversePolishCounter, ReversePolishConverter
import argparse

if __name__ == "__main__":
    counter = ReversePolishCounter()
    converter = ReversePolishConverter()

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--expression', dest="expression", help="arithmetic expression to be converted")
    parser.add_argument('-r', '--reverse', dest="count", action="store_true", help="is expression in reverse polish?")

    args = parser.parse_args()

    expression = input() if not args.expression else args.expression

    if (args.count is True):
        print(counter.calculate(expression))
    else:
        expression = converter.convert(expression)
        print(" ".join(expression))
