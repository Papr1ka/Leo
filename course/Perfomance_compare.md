# Сравнение производительности

## Условие задачи

Обозначим единую задачу - поиск первых n простых чисел, начиная с единицы, путём перебора чисел и выявления тех, у кого
количество делителей ровно 2, то есть простых чисел

### Реализация на Leo

```lua
{
    /*
    Поиск первых primeNumberCount простых чисел
    */
    int primeNumberCount, number, j;

    primeNumberCount := 1000;
    number := 0;

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

```

### Реализация на python

```python
def primes():
    primeNumberCount = 1000
    number = 1
    while primeNumberCount > 0:
        number += 1
        j = 0
        for i in range(1, number + 1):
            if number % i == 0:
                j += 1

        if j == 2:
            primeNumberCount -= 1
            print(number)
```

### Программа, реализующая сравнение

```
from src.python_translator.translator import translate
from src.lexer import Lexer
from src.parser.parser import Parser
from src.text_driver import setup_source
from time import time


def primes():
    primeNumberCount = 1000
    number = 1
    while primeNumberCount > 0:
        number += 1
        j = 0
        for i in range(1, number + 1):
            if number % i == 0:
                j += 1

        if j == 2:
            primeNumberCount = primeNumberCount - 1
            print(number)


if __name__ == '__main__':
    setup_source("./examples/ex1.leo")
    lexer = Lexer()

    parser = Parser(lexer)
    ast = parser.parse()
    q_0 = time()
    python = translate(ast)
    print(time() - q_0)
    exit(0)

    r1 = []
    r2 = []

    for i in range(10):
        t_1_0 = time()
        exec(python)
        t_1_1 = time()
        t_2_0 = time()
        primes()
        t_2_1 = time()
        t_1 = t_1_1 - t_1_0
        t_2 = t_2_1 - t_2_0
        r1.append(t_1)
        r2.append(t_2)

    avg1 = sum(r1) / len(r1)
    avg2 = sum(r2) / len(r2)
    print(f"Leo: {avg1} ms, Python: {avg2} ms")
    print(f"Leo уступает в {avg1 / avg2} раз")
```

# Результаты

| Количество простых чисел | Leo, секунд | Python, секунд | Leo/Python |
|:------------------------:|:-----------:|:--------------:|:----------:|
|           1000           |   1.3727    |     1.3594     |   1.0098   |
|           500            |   0.2616    |     0.2598     |   1.0070   |
|           100            |   0.0059    |     0.0050     |   1.1650   |
|            10            |   0.00015   |    0.00004     |   3.5294   |

Заметно, что при n = 10, наш язык уступает довольно сильно, это связано с тем, что код приходится вызывать при помощи
метода exec

Проведём ряд тестов, вставив сгенерированный код в файл

Код, сгенерированный Leo для последнего случая выглядит следующим образом

```python
def main():
    primeNumberCount: int
    number: int
    j: int

    primeNumberCount = 10
    number = 1

    while (primeNumberCount > 0):
        number = (number + 1)
        j = 0

        for i in range(1, (number + 1), 1):

            if ((number % i) == 0):
                j = (j + 1)

        if (j == 2):
            primeNumberCount = (primeNumberCount - 1)
            print(number)
```

> Интересно заметить, что изначально в языке условие if выглядело следующим образом
>
> `if (number / i * i == number)`
>
> это связано с тем, что язык не поддерживает оператор % (mod), поэтому используем целочисленное деление, реализованное
> для типа int
>
> Но вопрос в том, как получился код
>
> `if ((number % i) == 0):`
>
> Ответ: это оптимизация на уровне дерева разбора

Сравнение без `exec()`
| Количество простых чисел | Leo, секунд | Python, секунд | Leo/Python |
|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
| 1000 | 1.3858 | 1.3785 | 1.0097 |
| 500 | 0.2741 | 0.2715 | 1.0070 |
| 100 | 0.0050 | 0.0050 | 1.0010 |
| 10 | 0.00004 | 0.00004 | 1.0254 |

Теперь никаких неожиданностей, отличие на уровне погрешности

Резюмируя сравнение Leo vs Python

![Итог Leo vs Python](./leo_vs_python.jpg)
