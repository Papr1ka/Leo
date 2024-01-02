{
    int primeNumberCount, number, i, j

    primeNumberCount := 10
    number := 0

    while (primeNumberCount > 0)
    {
    number := number + 1
    j := 0

    for i := 1 to number step 1
    {

    if (number / i * i == number) j := j + 1

    }


    if (j == 2) primeNumberCount := primeNumberCount - 1

    }

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

    writeln number
}
