from abc import ABC, abstractmethod

from identifiers import add_identifier, get_identifier, Identifier
from lang_base_types import BaseType


class BaseOperator(ABC):
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
