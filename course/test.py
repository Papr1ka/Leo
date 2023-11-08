from src.lexer import Lexer

l = Lexer("123\n")

print(next(iter(l.get_lex())))
