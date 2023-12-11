/*
    Поиск первых n простых чисел
    Ввод: n
    Вывод: Последовательность из n простых чисел, начиная с единицы
*/
{
    int primeNumberCount, number, j;

    readln primeNumberCount;
    number := 1;

    while (primeNumberCount > 0)
    begin
        number := number + 1;
        j := 0;
        for i := 1 to number + 1 step 1
        begin
            if (number / i * i == number)
                j := j + 1
        end
        next;

        if (j == 2)
        begin
            primeNumberCount := primeNumberCount - 1;
            writeln number
        end
    end;
}
