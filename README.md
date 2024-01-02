![Leo](./docs/Leo.jpeg)

# Язык Leo

[![latest
release](https://img.shields.io/github/v/release/Papr1ka/Leo.svg?label=current+release)](https://github.com/Papr1ka/Leo/releases)

Язык Leo - это учебный язык программирования, который может быть использован для несложных линейных
программ с числовыми и логическим типом данных

Язык нацелен на компиляцию в байткод для **виртуальной машины** (LEO/vm), также поддерживает трансляцию в **python** и **c++**.

> Обновление
>
> удалены токены ';' и 'next'
>
> теперь писать программы существенно проще

## Спецификация

[Спецификация](./docs/SPEC.md)

## Зависимости

- Python3 >= 3.8

- Перед использованием виртуальной машины требуется сначала её собрать (Makefile имеется).

## Виртуальная машина

[Про виртуальную машину можно прочитать тут](./vm/Readme.md).

## Запуск

компилятор/транслятор - `leoc.py`

Компиляция скрипта source.leo

`python leoc.py source.leo`

Трансляция скрипта source.leo на язык python в файл out.py

`python leoc.py source.leo -t py -o out.py`

Трансляция скрипта source.leo на язык c++ в файл out.cpp

`python leoc.py source.leo -t cpp -o out.cpp`

Компиляция скрипта source.leo в файл out.leo.bin

`python leoc.py source.leo -o out.leo.bin`

> Если не указывать имя выходного файла, оно будет сформировано на основе входного.

Получение справки

`python leoc.py -h`

Получение версии

`python leoc.py --v`

## Подсветка синтаксиса для vscode

Расширение для vscode находится в [Расширение для vscode](./vscode_lang_extension/)

Для установки необходимо просто перенести папку `leo-lang` в папку `.vscode/extensions` и оно сразу начнёт использоваться и асоциирует с собой файлы с расширением `*.leo`