import argparse
import pathlib

import src


class RussianHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Использование: '
            return super(RussianHelpFormatter, self).add_usage(
                usage, actions, groups, prefix)


def main():
    DESCRIPTION = """Интерпретатор и транслятор языка Leo (.leo) Удачи!"""

    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=RussianHelpFormatter, add_help=False)
    parser._positionals.title = "Позиционные аргументы"
    parser._optionals.title = "Опции"
    parser.add_argument('-v', '--version', action='version',
                        version=f'Leo {src.__version__}', help="Выводит версию программы")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Выводит это сообщение')
    parser.add_argument("target", type=pathlib.Path, help="Имя файла с расширением .leo", metavar="файл.leo")
    parser.add_argument("-t", "--translate", type=str, choices=['py', 'cpp'], default="py",
                        help="Целевой язык для трансляции, 'py' - python, 'cpp' - c++")
    parser.add_argument("-o", "--output", type=str, help="Название выходного файла", metavar="имя_файла")
    namespace = parser.parse_args()

    try:
        src.setup_source(namespace.target)
    except ValueError as E:
        print(E.args[0])
        exit(4)
    except FileNotFoundError:
        print("Файл не найден")
        exit(5)

    lexer = src.Lexer()
    parser = src.Parser(lexer)
    ast = parser.parse()

    if namespace.output is None:
        result = src.py_translate(ast)

        exec(result)
    else:
        if namespace.translate == "py":
            result = src.py_translate(ast)
        else:
            result = src.cpp_translate(ast)

        if namespace.output == "std":
            print(result)
        else:
            with open(namespace.output, "w") as file:
                file.writelines(result)

    print("Leo: Успешно")


if __name__ == "__main__":
    main()
