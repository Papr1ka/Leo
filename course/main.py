from src.lexer import Lexer


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

    # шаблон вывода лексем
    pattern = "{:<35} {:<20} {:<8} {:<8} {:<40}"

    print(pattern.format("Lex type", "Lex", "Line", "Symbol", "Error message"))
    print("{:-<115}".format(""))

    DEBUG = 1

    guard = 0
    for i in lexer.get_lex():
        if DEBUG:
            if len(i) == 4:
                print(pattern.format(*i, ""))
            else:
                print(pattern.format(*i))
        else:
            print(i)

        guard += 1
        if guard >= 1000:
            print("Error: Force stoped by guard")
            break

    print("Completed")
