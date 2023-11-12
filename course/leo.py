import argparse
import pathlib

import src

if __name__ == "__main__":
    DESCRIPTION = """Интерпретатор и транслятор языка Leo (.leo) Удачи!"""

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("target", type=pathlib.Path, help="Имя файла с расширением .leo", metavar="target")
    parser.add_argument("-t", "--translate", type=str, choices=['py', 'cpp'], default="py",
                        help="Целевой язык для трансляции, py | cpp")
    parser.add_argument("-o", "--output", type=str, help="Название выходного файла", metavar="filename")
    namespace = parser.parse_args()

    src.setup_source(namespace.target)
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

        with open(namespace.output, "w") as file:
            file.writelines(result)

    print("Leo: Успешно")
