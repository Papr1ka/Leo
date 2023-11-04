from lang_base_types import BaseType

identifiers = {}


def add_identifier(name: str, type_instance: BaseType):
    if identifiers.get(name) is not None:
        raise NameError(f"Identifier with name {name} already defined")

    identifiers[name] =
