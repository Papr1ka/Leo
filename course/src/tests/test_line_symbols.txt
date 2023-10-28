{
    int primeNumberCount, number, i, j;

    primeNumberCount := 10;
    number := 0;

    while (primeNumberCount > 0)
    begin
    number := number + 1;
    j := 0;

    for i := 1 to number step 1
    begin

    if (number / i * i == number) j := j + 1

    end
    next;

    if (j == 2) primeNumberCount := primeNumberCount - 1

    end;

    /*
    Программа ищет простые числа
    и выводит последнее найденное
    где количество чисел для поиска - primeNumberCount
    также стоит отметить, что в комментариях можно свободно пользоваться
    следующими символами
    / * * /
    /* * /
    / *
    */

    writeln number;
}
