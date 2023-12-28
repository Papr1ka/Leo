from time import time

import src
from src.lang import Types
from src.leovm.vm import CMD
import datetime
import openpyxl
import os

DIR = os.path.abspath(os.path.relpath("./codegen_outputs"))

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

def main(filename: str):
    try:
        src.setup_source(filename)
    except ValueError as E:
        print(E.args[0])
        exit(4)
    except FileNotFoundError:
        print("Файл не найден")
        exit(5)

    lexer = src.Lexer()
    parser = src.Parser(lexer)
    ast = parser.parse()


    result = src.py_translate(ast)

    pattern = "{:<5} {:<20} {:<20}"

    commands, var_count, table = src.compile_vm(ast)
    i = 0

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    if not os.path.exists(os.path.join(DIR, src.__vm_version__)):
        os.mkdir(os.path.join(DIR, src.__vm_version__))

    with open(os.path.join(DIR, f"{src.__vm_version__}/{filename.split('/')[2]}.leo.txt"), mode="w") as file:

        while i < len(commands):
            j = i
            cmd = CMD(commands[i])
            arg = ""
            if cmd in (CMD.STORE, CMD.LOAD, CMD.JIF, CMD.JIT, CMD.GOTO, CMD.LOAD_CONST, CMD.INPUT):
                i += 1
                if cmd == CMD.INPUT:
                    arg = Types(commands[i]).name
                elif cmd in (CMD.LOAD, CMD.STORE):
                    arg = table[commands[i]]
                else:
                    arg = commands[i]
            if arg is None:
                print("Ошибка, arg == None")
            print(pattern.format(j, cmd.name, arg))
            file.write(pattern.format(j, cmd.name, arg) + "\n")
            i += 1

    t_vm = timeit(src.run, 10)(commands, var_count)

    t_python = timeit(exec, 10)(result)

    t_old_executer = timeit(src.old_run, 10)(ast)



    wb = openpyxl.load_workbook("speed_tests.xlsx")
    ws = wb.active

    ws.append([filename, t_python, t_old_executer, t_vm, datetime.datetime.now(), src.__vm_version__])

    wb.save("speed_tests.xlsx")



    print(f"VM / Python {t_vm / t_python}, Executer / VM {t_old_executer / t_vm}, Виртуалка {t_vm} с. Питончик {t_python} с. Старый исполнитель {t_old_executer}")

    print("Leo: Успешно")


if __name__ == "__main__":
    main("./examples/sin_test.leo")
    main("./examples/primes_test.leo")
    main("./examples/fib_test.leo")
