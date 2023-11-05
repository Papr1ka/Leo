from abc import ABC, abstractmethod
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
