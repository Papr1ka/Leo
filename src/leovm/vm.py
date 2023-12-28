from enum import Enum
from typing import List, Union

from src.lang.lang_base_types import Types


class CMD(Enum):
    # Арифметические операции
    ADD = 2  # сложение
    DIFF = 3  # вычитание
    MUL = 4  # умножение
    DIV = 5  # деление
    IDIV = 6  # целочисленное деление
    MOD = 15  # остаток от деления

    # Логические операции
    NOT = 1  # отрицание
    OR = 7  # или
    AND = 8  # и
    LT = 9  # меньше
    LTE = 10  # меньше или равно
    GT = 11  # больше
    GTE = 12  # больше или равно
    EQ = 13  # равно
    NEQ = 14  # не равно

    JIT = 16  # переход, если истина
    JIF = 23  # переход, если ложь
    GOTO = 17  # безусловный переход

    INPUT = 18  # ввод
    OUTPUT = 19  # вывод

    LOAD = 20  # загрузка в стэк
    LOAD_CONST = 24  # загрузка константы
    STORE = 21  # выгрузка из стека

    STOP = 22  # остановка машины


STACK_MEM = []


def run(commands: List, var_count: int):
    COMMAND_MEM = commands
    VAR_MEM = list(range(var_count))
    STACK_MEM = []
    PC = 0
    while True:
        IR = COMMAND_MEM[PC]
        if IR == CMD.ADD:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() + tmp)
        elif IR == CMD.DIFF:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() - tmp)
        elif IR == CMD.MUL:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() * tmp)
        elif IR == CMD.DIV:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() / tmp)
        elif IR == CMD.IDIV:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() // tmp)
        elif IR == CMD.MOD:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() % tmp)
        elif IR == CMD.NOT:
            STACK_MEM.append(not STACK_MEM.pop())
        elif IR == CMD.OR:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() or tmp)
        elif IR == CMD.AND:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() and tmp)
        elif IR == CMD.LT:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() < tmp)
        elif IR == CMD.LTE:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() <= tmp)
        elif IR == CMD.GT:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() > tmp)
        elif IR == CMD.GTE:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() >= tmp)
        elif IR == CMD.EQ:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() == tmp)
        elif IR == CMD.NEQ:
            tmp = STACK_MEM.pop()
            STACK_MEM.append(STACK_MEM.pop() != tmp)
        elif IR == CMD.JIT:
            PC += 1
            addr = COMMAND_MEM[PC]
            if not STACK_MEM.pop():
                PC = addr
                continue
        elif IR == CMD.JIF:
            PC += 1
            addr = COMMAND_MEM[PC]
            if not STACK_MEM.pop():
                PC = addr
                continue
        elif IR == CMD.GOTO:
            PC += 1
            addr = COMMAND_MEM[PC]
            PC = addr
            continue
        elif IR == CMD.INPUT:
            PC += 1
            dtype = COMMAND_MEM[PC]
            value = input("Ожидается ввод: ")
            if dtype == Types.int.value:
                value = int(value)
            elif dtype == Types.float.value:
                value = float(value)
            elif dtype == Types.bool.value:
                value = bool(value)
            STACK_MEM.append(value)
        elif IR == CMD.OUTPUT:
            print(STACK_MEM.pop())
        elif IR == CMD.LOAD:
            PC += 1
            addr = COMMAND_MEM[PC]
            STACK_MEM.append(VAR_MEM[addr])
        elif IR == CMD.STORE:
            PC += 1
            addr = COMMAND_MEM[PC]
            VAR_MEM[addr] = STACK_MEM.pop()
        elif IR == CMD.LOAD_CONST:
            PC += 1
            STACK_MEM.append(COMMAND_MEM[PC])
        elif IR == CMD.STOP:
            print("Программа завершена")
            break
        else:
            print("Ошибка, команда не определена")
        PC += 1


if __name__ == "__main__":
    COMMAND_MEM = [
        CMD.INPUT,
        0,
        CMD.STORE,
        0,
        CMD.LOAD,
        0,
        CMD.LOAD_CONST,
        5,
        CMD.GT,
        CMD.JIF,
        21 - 1,
        CMD.LOAD,
        0,
        CMD.LOAD_CONST,
        2,
        CMD.DIFF,
        CMD.STORE,
        0,
        CMD.GOTO,
        5 - 1,
        CMD.LOAD,
        0,
        CMD.OUTPUT,
        CMD.STOP
    ]

    VAR_MEM = list(range(1))

    run()
