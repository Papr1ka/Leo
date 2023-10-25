from src.lexer import Lexer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source = """123 321 number i e"""

    NUMBERTEST = """
0110b
0110B
0110c

2352270o
2352270O
2352270c
123
123d
123D
213h
1fabbDH
1fabbD
123e10
123e+10
123e-10
123E10
123E+10
123E-10
1123ee10
123ee+10
213Ee-10
123Ee
123e
..123e
123..123e
123.e
123.e.
123.e.10
123+e10
123-e10

123.123
.123
123.123e10
123.123e+10
123.123e-10
123.123E10
123.123E+10
123.123E-10

.123e10
.123e+10
.123e-10
.123E10
.123E+10
.123E-10
123E-10
ident
0110c
123
10.3e
10
10.3e 10
10.3e10
10.3e ident
"""

    # lexer = Lexer(source)
    # for i in lexer.getLex():
    #     print(i)

    lexer = Lexer(NUMBERTEST)
    for i in lexer.get_lex():
        print(i)

    print("Completed")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
