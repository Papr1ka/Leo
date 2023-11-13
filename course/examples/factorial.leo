/*
    Расчёт факториала числа
    Ввод: число
    Вывод: -1, если ввод не натуральное число, иначе факториал числа
*/
{
    int n;
    int factorial;

    readln n;
    if (n >= 0)
        begin

        factorial := 1;

        while (n > 1)
        begin
            factorial := factorial * n;
            n := n - 1
        end;
        
        writeln factorial
        end
    else
        writeln 0-1;
}