%option noyywrap yylineno
%{
#include <stdio.h>
int state;
void UndefinedTokenPrint();
%}

%s S_START

DIGIT [0-9]
BEGIN_OBJECT \{
END_OBJECT \}
BEGIN_ARRAY \[
END_ARRAY \]
COMMA ,
COLON :
LITERAL (true|false|null)
STRING ([^\"]*)?

BINARY [0-1]+(B|b)
OCTAL [0-7]+(O|o)
DECIMAL {DIGIT}+(D|d)?
HEXADECIMAL ({DIGIT}|[a-fA-F])+(H|h)

INTEGER ({BINARY}|{OCTAL}|{DECIMAL}|{HEXADECIMAL})

NUMORDER (E|e)(\+|-){DIGIT}

REAL ({DIGIT}+{NUMORDER}){DIGIT}+?\.{DIGIT}+{NUMORDER}?

NUMBER ({INTEGER}|{REAL})

DELIM [ \t\n]

QUOTE \"

%%

{QUOTE} {
	if (state == 0)
	{
		state = 1;
		BEGIN(S_START);
	}
	else
	{
		state = 0;
		BEGIN(INITIAL);
	}
}
{DELIM} { ; }
{BEGIN_OBJECT} { printf("(BEGIN_OBJECT, '%s')\n", yytext); }
{END_OBJECT} { printf("(END_OBJECT, '%s')\n", yytext); }
{BEGIN_ARRAY} { printf("(BEGIN_ARRAY, '%s')\n", yytext); }
{END_ARRAY} { printf("(END_ARRAY, '%s')\n", yytext); }
{COMMA} { printf("(COMMA, '%s')\n", yytext); }
{COLON} { printf("(COLON, '%s')\n", yytext); }
{LITERAL} { printf("(LITERAL, '%s')\n", yytext); }
<S_START>{STRING} { printf("(STRING, '%s')\n", yytext); }
{NUMBER} { printf("(NUMBER, '%s')\n", yytext); }
. { UndefinedTokenPrint(); }
%%

int main(int argc, char **argv)
{
	if(argc < 2)
	{
		printf("\nNot enough arguments. Please specify filename.\n");
		return -1;
	}
	if((yyin = fopen(argv[1], "r")) == NULL)
	{
		printf("\nCannot open file %s.\n", argv[1]);
		return -1;
	}
	state = 0;
	yylineno = 1;
	printf("Tokenlist:\n");
	yylex();
	fclose(yyin);
	return 0;
}

void UndefinedTokenPrint()
{
	printf("Error: \"Нераспознанный токен\" in line %d. Token = %s\n", yylineno, yytext);
}