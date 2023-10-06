import lexer
from pprint import pprint

s = """for (i := 0; i := _ < 3; i := i = 3)
do
i := 2
sad)
110
1e+10
0.0012313
123123.123
+1e-10
-1e+10
+0.0012313
-123123.123
2e+10
123.e123

for
do
asd
sad3424f"""

a = s.split("\n")

# while True:
#     try:
#         i = input()
#     except EOFError:
#         break
#     else:
#         a.append(i)

l = lexer.Lexer()
tokens = l.parse(a)
pprint(tokens)
