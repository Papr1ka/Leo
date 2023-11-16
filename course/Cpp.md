# Особенности трансляции на язык c++

## Типы данных

Тип int языка Leo представлен типом long long.

Тип float языка Leo представлен типом double.

Тип bool языка Leo представлен типом bool.

Переполнение типов int и float языка Leo возможно и определяется поведением языка c++.

## Цикл for

Конструкция будет иметь следующий вид:

```
for (long long счётчик = выражение_1; счётчик < выражение_2, счётчик += выражение_3)
{
    ...
}
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