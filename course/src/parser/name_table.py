from typing import Any, Dict, List

from src.constants import Lexeme
from src.errors import ctx_error
from src.lang.lang_base_types import Types


class TableItem:
    name: str
    t_type: Types
    value: Any
    is_assigned: bool
    readonly: bool

    def __init__(self, name: str, t_type: Types, value: Any, readonly=False):
        self.name = name
        self.t_type = t_type
        self.value = value
        self.is_assigned = False
        self.readonly = readonly


tables: List[Dict[str, TableItem]] = []


def add_name(item: TableItem):
    # без проверок
    tables[-1][item.name] = item


def find_name(key: str) -> TableItem:
    for table in tables[::-1]:
        r = table.get(key)
        if r is not None:
            return r
    return None


def new_name(t_type: Types, identifier: Lexeme, readonly=False):
    exist = find_name(identifier.value)
    if exist is not None:
        ctx_error("Повторное определение имени", identifier)

    add_name(TableItem(
        identifier.value,
        t_type,
        None,
        readonly=readonly
    ))


def open_scope():
    tables.append({})


def close_scope():
    tables.pop(-1)
