from typing import Any, Dict

from src.constants import Lexeme
from src.errors import ctx_error
from src.lang.lang_base_types import Types


class TableItem:
    name: str
    t_type: Types
    value: Any
    is_assigned: bool

    def __init__(self, name: str, t_type: Types, value: Any):
        self.name = name
        self.t_type = t_type
        self.value = value
        self.is_assigned = False


table: Dict[str, TableItem] = {}


def add_name(item: TableItem):
    # без проверок
    table[item.name] = item


def find_name(key: str) -> TableItem:
    return table.get(key)


def new_name(t_type: Types, identifier: Lexeme):
    exist = table.get(identifier.value)
    if exist is not None:
        ctx_error("Повторное определение имени", identifier)

    add_name(TableItem(
        identifier.value,
        t_type,
        None
    ))
