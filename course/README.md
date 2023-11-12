![Leo](./Leo.jpeg)

# Язык Leo

Язык Leo - это учебный транслируемый язык программирования, который может быть использован для несложных линейных
программ с числовыми и логическим типом данных

Язык поддерживает трансляцию в **python** и **c++**

Целевой случай - это трансляция в python и непосредственное исполнение, всё это делается под капотом

## Спецификация

[Спецификация](./SPEC.md)

## Сравнение производительности

![Perfomance](./Leo_perfomance.jpg)

[Leo vs Python](./Perfomance_compare.md)

## Зависимости

- Python3

## Запуск

интерпретатор/транслятор - `leo.py`

Запуск скрипта source.leo

`python leo.py source.leo`

Трансляция скрипта source.leo на язык python в файл out.py

`python leo.py source.leo -t py -o out.py`

Трансляция скрипта source.leo на язык c++ в файл out.cpp

`python leo.py source.leo -t cpp -o out.cpp`

Дополнительную информацию можно получить через команду `help`

`python leo.py -h`