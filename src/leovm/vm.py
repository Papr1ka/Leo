from enum import Enum
from time import time
from typing import List

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

    DUP = 25 # дублировать вершину стека


# STACK_MEM = []
def timeit(func, n):
    def wrapper(*args, **kwargs):
        times = []
        for i in range(n):
            t0 = time()
            func(*args, **kwargs)
            t1 = time()
            times.append(t1 - t0)
        return sum(times) / len(times)
    return wrapper

def run(commands: List, var_count: int):
    COMMAND_MEM = commands.copy()
    VAR_MEM = list(range(var_count))
    STACK_MEM = [0 for i in range(1000)]

    PC = 0
    SP = 0

    while True:
        IR = COMMAND_MEM[PC]
        if IR == CMD.ADD:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] + STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.DIFF:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] - STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.MUL:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] * STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.DIV:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] / STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.IDIV:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] // STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.MOD:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] % STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.NOT:
            STACK_MEM[SP - 1] = not STACK_MEM[SP - 1]
        elif IR == CMD.OR:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] or STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.AND:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] and STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.LT:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] < STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.LTE:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] <= STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.GT:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] > STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.GTE:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] >= STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.EQ:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] == STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.NEQ:
            STACK_MEM[SP - 2] = STACK_MEM[SP - 2] != STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.JIT:
            PC += 1
            addr = COMMAND_MEM[PC]
            if not STACK_MEM[SP - 1]:
                PC = addr
                SP -= 1
                continue
            SP -= 1
        elif IR == CMD.JIF:
            PC += 1
            addr = COMMAND_MEM[PC]
            if not STACK_MEM[SP - 1]:
                PC = addr
                SP -= 1
                continue
            SP -= 1
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
            STACK_MEM[SP] = value
            SP += 1
        elif IR == CMD.OUTPUT:
            print(STACK_MEM[SP - 1])
            SP -= 1
        elif IR == CMD.LOAD:
            PC += 1
            addr = COMMAND_MEM[PC]
            STACK_MEM[SP] = VAR_MEM[addr]
            SP += 1
        elif IR == CMD.STORE:
            PC += 1
            addr = COMMAND_MEM[PC]
            VAR_MEM[addr] = STACK_MEM[SP - 1]
            SP -= 1
        elif IR == CMD.LOAD_CONST:
            PC += 1
            STACK_MEM[SP] = COMMAND_MEM[PC]
            SP += 1
        elif IR == CMD.DUP:
            STACK_MEM[SP] = STACK_MEM[SP - 1]
            SP += 1
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

    COMMAND_MEM = [
        CMD.LOAD_CONST,
        100000,
        CMD.DUP,
        CMD.DUP,
        CMD.LOAD_CONST,
        0,
        CMD.GT,
        CMD.JIF,
        16 - 1,
        CMD.LOAD_CONST,
        1,
        CMD.DIFF,
        CMD.DUP,
        CMD.GOTO,
        5 - 1,
        CMD.OUTPUT,
        CMD.STOP
    ]

    VAR_MEM = list(range(1))

    t = timeit(run, 10)(COMMAND_MEM, 1)
    print(t, "Секунд") # 1.74079


    def myfunc():
        x = 1000000
        while (x > 0):
            x = x - 1

        print(x)


    t = timeit(myfunc, 10)()
    print(t, "Секунд")  # существенно быстрее)
