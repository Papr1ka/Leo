from typing import List
from struct import pack

from src.lang import Types
from src.codegen import CMD


def write_program(filename: str, var_count: int, consts: List, commands: List):
    with open(filename, mode="wb") as file:
        file.write(pack("=L", var_count)) # unsigned Long, кол-во переменных
        file.write(pack("=L", len(consts))) # unsigned Long, кол-во констант
        file.write(pack("=L", len(commands))) # unsigned Long, кол-во команд
        for const_type, const, in consts:
            file.write(pack("=B", const_type)) # Unsigned char, тип константы
            if const_type == Types.int.value:
                file.write(pack("=q", const)) # long
            elif const_type == Types.float.value:
                file.write(pack("=d", const)) # double
            elif const_type == Types.bool.value:
                file.write(pack("=?", const)) # bool
            else:
                raise ValueError("Неопределённый тип константы")
        for command in commands:
            if isinstance(command, CMD):
                command = command.value
            file.write(pack("=H", command)) # Unsigned short, команда
