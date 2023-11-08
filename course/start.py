from src.interpretor.interpretor import run
from src.lexer import Lexer
from src.parser.syntax_parser import Parser
from src.test_driver import setup_source

if __name__ == '__main__':
    setup_source("./examples/test3.leo")
    lexer = Lexer()

    parser = Parser(lexer)
    ast = parser.parse()
    run(ast)
