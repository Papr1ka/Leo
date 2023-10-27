from src.lexer import Lexer


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source = """123 321 number i e"""

    NUMBERTEST = """I{0})({101 ({{ident}})}
123)
.123e10
IDENT)
IDENT{0}
(
"""
    NUMBERTEST = """a<b<<
(0110b)+-
(a!b)
(a!=b)
b==a
b<=a
b<a
b>=a
b>a
>>>=>
a||b
|||a
/*всякая ересь*/
a&&b
&&&b
a:=b
:=:b
/*asd*/
"""
    # lexer = Lexer(source)
    # for i in lexer.getLex():
    #     print(i)

    NUMBERTEST = """
1
/*abcd*/
2
/***/
3
/*/*/
4
/******
*
/
*
* /
5
*/
"""

    file_contents = ""

    with open("./src/tests/test_separators.txt") as file:
        file_contents = "\n".join(file.readlines())

    lexer = Lexer(NUMBERTEST)
    pattern = "{:<35} {:<20} {:<8} {:<8}"

    print(pattern.format("Lex type", "Lex", "Line", "Symbol"))
    print("{:-<75}".format(""))
    guard = 0
    for i in lexer.get_lex():
        print(pattern.format(*i))
        # print(next(lexer.get_lex()))
        guard += 1
        if guard >= 300:
            print("Error: Force stoped by guard")
            break
    print("Completed")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
