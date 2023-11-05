from abc import ABC, abstractmethod

from src.lang.identifiers import add_identifier, get_identifier, Identifier
from src.lang.lang_base_types import BaseType


class BaseOperator(ABC):
    args = []
    kwargs = {}

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self(*self.args, **self.kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class DefineOperator(BaseOperator):
    def __call__(self, type_class: BaseType, names: list):
        for name in names:
            add_identifier(name, type_class)


class AssignmentOperator(BaseOperator):
    def __call__(self, name: str, literal: str):
        identifier: Identifier = get_identifier(name)
        # По идее, ошибки быть не может, так как синтаксически тип будет верным
        identifier.initialize(identifier.type_class.from_string(literal))


class BranchOperator(BaseOperator):
    def __call__(self, expression: BaseType):
        pass
