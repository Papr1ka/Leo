![Leo](./docs/Leo.jpeg)

# Язык Leo

[![latest
release](https://img.shields.io/github/v/release/Papr1ka/Leo.svg?label=current+release)](https://github.com/Papr1ka/Leo/releases)

Язык Leo - это учебный транслируемый язык программирования, который может быть использован для несложных линейных
программ с числовыми и логическим типом данных

Язык поддерживает трансляцию в **python** и **c++**

Целевой случай - это трансляция в python и непосредственное исполнение, всё это делается под капотом

## Спецификация

[Спецификация](./docs/SPEC.md)

## Сравнение производительности

![Perfomance](./docs/Leo_perfomance.jpg)

[Leo vs Python](./docs/Perfomance_compare.md)

## Зависимости

- Python3 >= 3.8

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

## Подсветка синтаксиса для vscode

Расширение для vscode находится в [Расширение для vscode](./vscode_lang_extension/)

Для установки необходимо просто перенести папку `leo-lang` в папку `.vscode/extensions` и оно сразу начнёт использоваться и асоциирует с собой файлы с расширением `*.leo`