from src.interpretor.interpretor import run
from src.lexer import Lexer
from src.parser.syntax_parser import Parser

if __name__ == '__main__':
    source = """123 321 number i e"""

    test = """
можно написать тестовую программу здесь
"""

    # или считать из файла
    with open("./examples/ex2") as file:
        file_contents = "".join(file.readlines())

    # передать в лексический анализатор
    lexer = Lexer(file_contents)

    parser = Parser(lexer)
    ast = parser.parse()
    run(ast)
