/*
    Поиск минимального из 5-ти различных чисел
    Вывод: минимальное из number1 ... number5
*/
{
    int number1, number2, number3, number4, number5
    int min

    number1 := 123
    number2 := 123
    number3 := 52
    number4 := 123
    number5 := 7

    if (number1 < number2)
        min := number1
    else
        min := number2

    if (min > number3)
        min := number3

    if (min > number4)
        min := number4

    if (min > number5)
        min := number5
    
    writeln min
}