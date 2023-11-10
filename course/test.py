from src.cpp_translator.translator import *

from src.lexer import Lexer
from src.parser.parser import Parser
from src.text_driver import setup_source

if __name__ == '__main__':
    setup_source("./examples/ex1.leo")
    lexer = Lexer()

    parser = Parser(lexer)
    ast = parser.parse()
    r = translate(ast)
    with open("./out.cpp", "w") as file:
        file.writelines(r)
    print("Completed")
