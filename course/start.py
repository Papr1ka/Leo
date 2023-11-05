from src.lexer import Lexer
from src.parser.syntax_parser import SyntaxParser

if __name__ == '__main__':
    source = """123 321 number i e"""

    test = """
можно написать тестовую программу здесь
"""

    # или считать из файла
    with open("./examples/ex1") as file:
        file_contents = "".join(file.readlines())

    # передать в лексический анализатор
    lexer = Lexer(file_contents)

    parser = SyntaxParser(lexer)
    parser.parse()
