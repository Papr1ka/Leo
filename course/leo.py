import src
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Ошибка, необходимо указать имя файла")
        exit(4)

    src.setup_source(sys.argv[1])
    print("Файл", src.get_filename())
    lexer = src.Lexer()
    parser = src.Parser(lexer)
    ast = parser.parse()
    src.run(ast)
