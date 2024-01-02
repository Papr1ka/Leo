/*
	Программа для нахождения минимума, максимума и среднего арифметического введённой последовательности
	Ввод: длина последовательности, последовательноть чисел
	Вывод: -1, если длина последовательности 0 или меньше, иначе минимум, максимум, среднее арифметическое
	Примечание: среднее арифметическое будет вычислено как целая часть частного суммы последовательности и её длины
*/
{
	int min
	int max
	int sum
	
	int n
	int curNumber

	min := 7fffffffffffffffh
	max := 0
	sum := 0
	
	readln n

	if (n > 0)
	{
        for i := 0 to n
        {
            readln curNumber
            if (curNumber > max)
                max := curNumber
            if (curNumber < min)
                min := curNumber
            sum := sum + curNumber
		}
        writeln min, max, sum / n
	}
	else
	    writeln 0-1
}