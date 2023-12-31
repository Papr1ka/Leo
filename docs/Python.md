# Особенности трансляции на язык Python

## Имена переменных

Имена переменных 'input' и 'print' зарезервированны, так как необходимы для операций ввода и вывода.

## Типы данных

Тип int языка Leo представлен типом int.

Тип float языка Leo представлен типом float.

Тип bool языка Leo представлен типом bool.

Переполнение типов int и float языка Leo невозможно, так как Python реализует длинную арифметику.

## Цикл for

В python цикл for реализуется с использованием range.

Конструкция будет иметь следующий вид:

```
for счётчик in range(выражение1, выражение2, выражение3):
    код...
```

## Оптимизация

Конструкция вида

```
i / j * j == i
```

Будет заменена на конструкцию

```
i % j == 0
```

При условии, что i и j объявлены как переменные типа int.
