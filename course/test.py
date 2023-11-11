from src.cpp_translator.translator import translate as cpp_translate
from src.lexer import Lexer
from src.parser.parser import Parser
from src.python_translator.translator import translate as python_translate
from src.text_driver import setup_source

if __name__ == '__main__':
    setup_source("./examples/debug.leo")
    lexer = Lexer()

    parser = Parser(lexer)
    ast = parser.parse()
    r = cpp_translate(ast)
    with open("./out.cpp", "w") as file:
        file.writelines(r)
    print("Completed")

    r = python_translate(ast)
    with open("./out.py", "w") as file:
        file.writelines(r)
    print("Completed")
