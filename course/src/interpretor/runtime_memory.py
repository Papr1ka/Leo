from typing import Union

from src.lang.lang_base_types import Boolean, Float, Integer

table = {

}


def store(name: str, value: Union[Integer, Float, Boolean]):
    table[name] = value


def load(name: str):
    return table[name]
