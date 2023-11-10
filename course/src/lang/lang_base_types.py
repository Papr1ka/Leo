from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from src.constants import Lex


class BaseType(ABC):
    value: Union[int, float, bool]

    @staticmethod
    @abstractmethod
    def from_string(literal: str):
        pass

    def neq(self, other):
        return Boolean(self.value.__ne__(other.value))

    def eq(self, other):
        return Boolean(self.value.__eq__(other.value))

    def lt(self, other):
        tmp = self.value.__lt__(other.value)
        return Boolean(self.value.__lt__(other.value))

    def lte(self, other):
        return Boolean(self.value.__le__(other.value))

    def gt(self, other):
        return Boolean(self.value.__gt__(other.value))

    def gte(self, other):
        return Boolean(self.value.__ge__(other.value))

    def or_(self, other):
        return Boolean(bool(self.value) or bool(other.value))

    def and_(self, other):
        return Boolean(bool(self.value) and bool(other.value))

    def not_(self):
        return Boolean(not bool(self.value))

    def __str__(self):
        return str(self.value)


class Number(BaseType):

    @abstractmethod
    def add(self, other):
        pass

    @abstractmethod
    def sub(self, other):
        pass

    @abstractmethod
    def mul(self, other):
        pass

    @abstractmethod
    def div(self, other):
        pass


class Integer(Number):
    @staticmethod
    def from_string(literal: str):
        if literal.endswith(("b", "B")):
            return Integer(int(literal[:-1], 2))
        elif literal.endswith(("o", "O")):
            return Integer(int(literal[:-1], 8))
        elif literal.endswith(("h", "H")):
            return Integer(int(literal[:-1], 16))
        elif literal.endswith(("d", "D")):
            return Integer(int(literal[:-1]))
        return Integer(int(literal))

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Значение параметра value должно быть типа int")
        self.value = value

    def add(self, other):
        return Integer(self.value + other.value)

    def sub(self, other):
        return Integer(self.value - other.value)

    def mul(self, other):
        return Integer(self.value * other.value)

    def div(self, other):
        return Integer(self.value // other.value)


class Float(Number):
    @staticmethod
    def from_string(literal: str):
        return Float(float(literal))

    def __init__(self, value: float):
        if not isinstance(value, float):
            raise ValueError("Значение параметра value должно быть типа float")
        self.value = value

    def add(self, other):
        return Float(self.value + other.value)

    def sub(self, other):
        return Float(self.value - other.value)

    def mul(self, other):
        return Float(self.value * other.value)

    def div(self, other):
        return Float(self.value / other.value)


class Boolean(BaseType):
    @staticmethod
    def from_string(literal: str):
        if literal == "true":
            return Boolean(True)
        return Boolean(False)

    def __init__(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Значение параметра value должно быть типа bool")
        self.value = value


TYPES = {
    Lex.KEYWORD_INT: Integer,
    Lex.KEYWORD_FLOAT: Float,
    Lex.KEYWORD_BOOL: Boolean
}


class Types(Enum):
    int = 0
    float = 1
    bool = 2


LEX_TO_TYPE_TABLE = {
    Lex.KEYWORD_INT: Types.int,
    Lex.KEYWORD_FLOAT: Types.float,
    Lex.KEYWORD_BOOL: Types.bool
}

TYPE_TO_TYPE_TABLE = {
    Integer: Types.int,
    Float: Types.float,
    Boolean: Types.bool
}


def type_to_type(t_type: Union[Integer, Float, Boolean]):
    r = TYPE_TO_TYPE_TABLE.get(t_type.__class__)
    if r is not None:
        return r
    raise ValueError("Тип не определён")


def get_type_number_from_lex(lex: Lex) -> Types:
    r = LEX_TO_TYPE_TABLE.get(lex)
    if r is not None:
        return r
    raise ValueError("Тип не определён")


class BinOperations(Enum):
    sum = 0  # сумма
    diff = 1  # разность
    mul = 2  # произведение
    div = 3  # частное
    alt = 4  # операция или
    con = 5  # операция и
    eq = 6  # ==
    neq = 7  # !=
    gt = 8  # >
    gte = 9  # >=
    lt = 10  # <
    lte = 11  # <=


RELATION_OPERATORS = [
    BinOperations.lt,
    BinOperations.lte,
    BinOperations.gt,
    BinOperations.gte,
    BinOperations.eq,
    BinOperations.neq
]

LEX_TO_BIN_OP_TABLE = {
    Lex.SEPARATOR_PLUS: BinOperations.sum,
    Lex.SEPARATOR_MINUS: BinOperations.diff,
    Lex.SEPARATOR_MULTIPLICATION: BinOperations.mul,
    Lex.SEPARATOR_DIVISION: BinOperations.div,
    Lex.SEPARATOR_OR: BinOperations.alt,
    Lex.SEPARATOR_AND: BinOperations.con,
    Lex.SEPARATOR_EQUALS: BinOperations.eq,
    Lex.SEPARATOR_NOT_EQUALS: BinOperations.neq,
    Lex.SEPARATOR_GT: BinOperations.gt,
    Lex.SEPARATOR_GTE: BinOperations.gte,
    Lex.SEPARATOR_LT: BinOperations.lt,
    Lex.SEPARATOR_LTE: BinOperations.lte
}


def get_bin_operation_from_lex(lex: Lex) -> BinOperations:
    r = LEX_TO_BIN_OP_TABLE.get(lex)
    if r is not None:
        return r
    raise ValueError("Операция не определён")
