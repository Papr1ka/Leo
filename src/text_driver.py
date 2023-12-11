import os
import pathlib
from typing import Union

_source = ""
_lines = []
_is_set = False
_filename = "Интерактивный"


def read_file(filename: pathlib.Path) -> str:
    global _lines
    with open(os.path.abspath(os.path.relpath(filename))) as file:
        _lines = file.readlines()
    if not _lines:
        _lines = [""]
    stream = "".join(_lines) + " "
    stream = stream.replace("\t", "    ")  # замена табов на 4 пробела
    return stream


def highlight(line: int, symbol: int):
    if len(_lines) > line - 1:
        content: str = _lines[line - 1]
        if content.endswith("\n"):
            print(content, end="")
        else:
            print(content)
        for i in range(symbol - 1):
            print(" ", end="")
        print("^")


def setup_source(filename: Union[pathlib.Path, str]):
    global _source, _is_set, _filename
    if isinstance(filename, str):
        filename = pathlib.Path(filename)

    if filename.name.endswith(".leo"):
        _source = read_file(filename)
        _filename = filename.name
    else:
        raise ValueError("Имя файла должно иметь расширение .leo")
    _is_set = True


def get_source() -> str:
    if not _is_set:
        raise NotImplementedError("Не вызван setup_source")
    return _source


def get_filename() -> str:
    return _filename
