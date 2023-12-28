"""
Модуль синтезации программы на c++ из абстрактного дерева
"""
from src.lang import TYPE_TO_TYPE_TABLE
from src.leovm.vm import CMD
from src.tree import *

result = []
count = 0
table = {}
reverse_table = {}


def compile_vm(ast: ASTNode):
    global result, count
    while ast is not None:
        translate_operator(ast)
        ast = ast.next_node
    result.append(CMD.STOP)
    return result.copy(), count, reverse_table.copy()


def translate_expression(ast: ASTTyped):
    if ast.a_type == ASTType.CONST:
        ast: ASTConst
        result.append(CMD.LOAD_CONST)
        result.append(ast.value.value)
    elif ast.a_type == ASTType.VAR:
        ast: ASTVar
        result.append(CMD.LOAD)
        result.append(table[ast.name])

    elif ast.a_type == ASTType.U_OP:
        ast: ASTUOperation
        translate_expression(ast.operand)
        result.append(CMD.NOT)

    elif ast.a_type == ASTType.BIN_OP:
        ast: ASTBinOperation
        translate_expression(ast.left)
        translate_expression(ast.right)
        if ast.operation == BinOperations.sum:
            result.append(CMD.ADD)
        elif ast.operation == BinOperations.diff:
            result.append(CMD.DIFF)
        elif ast.operation == BinOperations.mul:
            result.append(CMD.MUL)
        elif ast.operation == BinOperations.div:
            if ast.t_type == Types.int:
                result.append(CMD.IDIV)
            else:
                result.append(CMD.DIV)
        elif ast.operation == BinOperations.alt:
            result.append(CMD.OR)
        elif ast.operation == BinOperations.con:
            result.append(CMD.AND)
        elif ast.operation == BinOperations.lt:
            result.append(CMD.LT)
        elif ast.operation == BinOperations.lte:
            result.append(CMD.LTE)
        elif ast.operation == BinOperations.gt:
            result.append(CMD.GT)
        elif ast.operation == BinOperations.gte:
            result.append(CMD.GTE)
        elif ast.operation == BinOperations.eq:
            result.append(CMD.EQ)
        elif ast.operation == BinOperations.neq:
            result.append(CMD.NEQ)
        elif ast.operation == BinOperations.mod:
            result.append(CMD.MOD)
        else:
            raise ValueError("Неопределённая операция")


def alloc_var(name: str):
    global count, table
    table[name] = count
    reverse_table[count] = name
    count += 1



def translate_operator(ast: ASTNode):
    if ast.a_type == ASTType.DECL:
        ast: ASTDeclaration
        node = ast.variables
        alloc_var(node.name)
        node = node.next_node
        while node is not None:
            alloc_var(node.name)
            node = node.next_node

    elif ast.a_type == ASTType.ASSIGNMENT:
        ast: ASTAssignment
        translate_expression(ast.value)
        result.append(CMD.STORE)
        result.append(table[ast.var.name])
        # r = "\t" * tabs + ast.var.name + " = " + translate_expression(ast.value)

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        condition = translate_expression(ast.condition)
        result.append(CMD.JIF)
        cmd_else_addr = len(result)  # адрес будущего адреса (номера) команды, с которой начинается else
        result.append(None)  # заглушка, тут будет адрес перехода, если условие ложно
        node = ast.branch
        while node is not None:
            translate_operator(node)
            node = node.next_node

        result.append(CMD.GOTO)
        cmd_if_end_addr = len(result)  # адрес будущего адреса (номера) команды, следующей за концом оператора ветвления
        result.append(None)  # заглушка, тут должен быть адрес перехода на конец условия

        result[cmd_else_addr] = len(result)  # адрес перехода на ветку else или конец условия,
        # если условие в if было ложным

        if ast.else_branch is not None:
            node = ast.else_branch
            while node is not None:
                translate_operator(node)
                node = node.next_node
        result[cmd_if_end_addr] = len(result) # оптимизировать (если нет else, бесполезный переход)

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        cmd_condition_addr = len(result)
        translate_expression(ast.condition)
        result.append(CMD.JIF)
        cmd_while_end_addr = len(result)  # адрес заглушки, где будет адрес конца цикла
        result.append(None)  # заглушка
        node = ast.body
        while node is not None:
            translate_operator(node)
            node = node.next_node
        result.append(CMD.GOTO)
        result.append(cmd_condition_addr)
        result[cmd_while_end_addr] = len(result)

    elif ast.a_type == ASTType.ForLoop:
        ast: ASTForLoop
        alloc_var(ast.assignment.var.name)
        translate_expression(ast.assignment.value)
        result.append(CMD.STORE)  # хорошо бы в будущем добавить команду Double,
        # чтобы удвоить дублировать элемент на вершине стека
        result.append(table[ast.assignment.var.name])

        # assignment = type_enum_to_type_str_table.get(
        #     Types.int) + " " + ast.assignment.var.name + " = " + translate_expression(ast.assignment.value)
        cmd_condition_addr = len(result)  # адрес начала условия
        translate_expression(ast.condition)
        result.append(CMD.JIF)
        cmd_for_end_addr = len(result)  # адрес заглушки, где будет адрес конца цикла for
        result.append(None)  # заглушка

        # step = translate_expression(ast.step) потом
        node = ast.body
        while node is not None:
            translate_operator(node)
            node = node.next_node

        translate_expression(ast.step)
        result.append(CMD.LOAD)
        result.append(table[ast.assignment.var.name])
        result.append(CMD.ADD)
        result.append(CMD.STORE)  # оптимизировать
        result.append(table[ast.assignment.var.name])
        result.append(CMD.GOTO)
        result.append(cmd_condition_addr)

        result[cmd_for_end_addr] = len(result)

    elif ast.a_type == ASTType.IN:
        ast: ASTIn
        node = ast.variables
        while node is not None:
            result.append(CMD.INPUT)
            result.append(node.t_type.value)
            result.append(CMD.STORE)
            result.append(table[node.name])
            node = node.next_node

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        node = ast.expressions
        while node is not None:
            translate_expression(node)
            result.append(CMD.OUTPUT)
            node = node.next_node
    else:
        raise ValueError("Оператор не определён")
