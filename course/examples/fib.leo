/*
	Программа для нахождения первых n чисел Фибоначчи.
	Ввод: n
	Вывод: числа последовательности или -1, если n <= 0
*/
{
	int n;
	
    int fib1;
	int fib2;
	int tmp;
	
	fib1 := 0;
	fib2 := 1;
	readln n;
	
	if (n > 0)
		for i := 0 to n
		begin
			writeln fib1;
			
			tmp := fib2;
			fib2 := fib2 + fib1;
			fib1 := tmp
		end
		next
	else
		writeln 0 -1;
}