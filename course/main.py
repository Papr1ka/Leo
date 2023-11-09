from src.lexer import Lexer
from src.text_driver import setup_source

if __name__ == '__main__':
    # передать в лексический анализатор
    setup_source("./examples/ex1.leo")
    lexer = Lexer()

    # шаблон вывода лексем
    pattern = "{:<35} {:<20} {:<8} {:<8} {:<40}"

    print(pattern.format("Lex type", "Lex", "Line", "Symbol", "Error message"))
    print("{:-<115}".format(""))

    DEBUG = 1

    guard = 0
    for i in lexer.get_lex():
        if DEBUG:
            print(pattern.format(i.lex, i.value, i.line, i.symbol, i.error, ""))
        else:
            print(i)

        guard += 1
        if guard >= 1000:
            print("Error: Force stoped by guard")
            break

    print("Completed")
