from lang_base_types import BaseType

identifiers = {}


class Identifier:
    name: str
    initialized: bool
    type_class: BaseType
    type_object: BaseType

    def __init__(self, name: str, type_class: BaseType):
        self.name = name
        self.initialized = False
        self.type_class = type_class
        self.type_object = None

    def initialize(self, type_object: BaseType):
        self.initialized = True
        self.type_object = type_object


def add_identifier(name: str, type_class: BaseType):
    if identifiers.get(name) is not None:
        raise NameError(f"Identifier with name {name} already defined")

    identifiers[name] = Identifier(name, type_class)


def get_identifier(name: str):
    if identifiers.get(name) is None:
        raise NameError(f"Identifier with name {name} is not defined")

    return identifiers[name]
