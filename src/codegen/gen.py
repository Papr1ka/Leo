"""
Модуль синтезации программы на c++ из абстрактного дерева
"""
from .commands import CMD
from src.tree import *

_program = []
_var_count = 0
_var_table = {}
_consts = []
_const_count = 0


def compile_vm(ast: ASTNode):
    global _program, _var_count, _var_table, _consts, _const_count
    _program.clear()
    _var_count = 0
    _var_table.clear()
    _consts.clear()
    _const_count = 0
    while ast is not None:
        translate_operator(ast)
        ast = ast.next_node
    _program.append(CMD.STOP)
    return _program.copy(), _var_count, _consts.copy()


def translate_expression(ast: ASTTyped):
    if ast.a_type == ASTType.CONST:
        ast: ASTConst
        alloc_const(ast.t_type, ast.value.value)
        _program.append(CMD.LOAD_CONST)
        _program.append(_const_count - 1)
    elif ast.a_type == ASTType.VAR:
        ast: ASTVar
        _program.append(CMD.LOAD)
        _program.append(_var_table[ast.name])

    elif ast.a_type == ASTType.U_OP:
        ast: ASTUOperation
        translate_expression(ast.operand)
        _program.append(CMD.NOT)

    elif ast.a_type == ASTType.BIN_OP:
        ast: ASTBinOperation
        translate_expression(ast.left)
        translate_expression(ast.right)
        if ast.operation == BinOperations.sum:
            _program.append(CMD.ADD)
        elif ast.operation == BinOperations.diff:
            _program.append(CMD.SUB)
        elif ast.operation == BinOperations.mul:
            _program.append(CMD.MUL)
        elif ast.operation == BinOperations.div:
            if ast.t_type == Types.int:
                _program.append(CMD.IDIV)
            else:
                _program.append(CMD.DIV)
        elif ast.operation == BinOperations.alt:
            _program.append(CMD.OR)
        elif ast.operation == BinOperations.con:
            _program.append(CMD.AND)
        elif ast.operation == BinOperations.lt:
            _program.append(CMD.LT)
        elif ast.operation == BinOperations.lte:
            _program.append(CMD.LTE)
        elif ast.operation == BinOperations.gt:
            _program.append(CMD.GT)
        elif ast.operation == BinOperations.gte:
            _program.append(CMD.GTE)
        elif ast.operation == BinOperations.eq:
            _program.append(CMD.EQ)
        elif ast.operation == BinOperations.neq:
            _program.append(CMD.NEQ)
        elif ast.operation == BinOperations.mod:
            _program.append(CMD.MOD)
        else:
            raise ValueError("Неопределённая операция")


def alloc_var(name: str):
    global _var_count, _var_table
    _var_table[name] = _var_count
    _var_count += 1


def alloc_const(type: Types, value: Any):
    global _const_count, _consts
    _consts.append((type.value, value))
    _const_count += 1


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
        _program.append(CMD.STORE)
        _program.append(_var_table[ast.var.name])

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        translate_expression(ast.condition)
        _program.append(CMD.JIF)
        cmd_else_addr = len(_program)  # адрес будущего адреса (номера) команды, с которой начинается else
        _program.append(None)  # заглушка, тут будет адрес перехода, если условие ложно
        node = ast.branch
        while node is not None:
            translate_operator(node)
            node = node.next_node

        if ast.else_branch is not None:
            _program.append(CMD.GOTO)
            cmd_if_end_addr = len(_program)  # адрес будущего адреса (номера) команды, следующей за концом оператора ветвления
            _program.append(None)  # заглушка, тут должен быть адрес перехода на конец условия

        _program[cmd_else_addr] = len(_program)  # адрес перехода на ветку else или конец условия,
        # если условие в if было ложным

        if ast.else_branch is not None:
            node = ast.else_branch
            while node is not None:
                translate_operator(node)
                node = node.next_node
            _program[cmd_if_end_addr] = len(_program)

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        cmd_condition_addr = len(_program)
        translate_expression(ast.condition)
        _program.append(CMD.JIF)
        cmd_while_end_addr = len(_program)  # адрес заглушки, где будет адрес конца цикла
        _program.append(None)  # заглушка
        node = ast.body
        while node is not None:
            translate_operator(node)
            node = node.next_node
        _program.append(CMD.GOTO)
        _program.append(cmd_condition_addr)
        _program[cmd_while_end_addr] = len(_program)

    elif ast.a_type == ASTType.ForLoop:
        ast: ASTForLoop
        alloc_var(ast.assignment.var.name)
        translate_expression(ast.assignment.value)
        _program.append(CMD.STORE)  # хорошо бы в будущем добавить команду Double,
        # чтобы удвоить дублировать элемент на вершине стека
        _program.append(_var_table[ast.assignment.var.name])

        # assignment = type_enum_to_type_str_table.get(
        #     Types.int) + " " + ast.assignment.var.name + " = " + translate_expression(ast.assignment.value)
        cmd_condition_addr = len(_program)  # адрес начала условия
        translate_expression(ast.condition)
        _program.append(CMD.JIF)
        cmd_for_end_addr = len(_program)  # адрес заглушки, где будет адрес конца цикла for
        _program.append(None)  # заглушка

        # step = translate_expression(ast.step) потом
        node = ast.body
        while node is not None:
            translate_operator(node)
            node = node.next_node

        translate_expression(ast.step)
        _program.append(CMD.LOAD)
        _program.append(_var_table[ast.assignment.var.name])
        _program.append(CMD.ADD)
        _program.append(CMD.STORE)  # оптимизировать
        _program.append(_var_table[ast.assignment.var.name])
        _program.append(CMD.GOTO)
        _program.append(cmd_condition_addr)

        _program[cmd_for_end_addr] = len(_program)

    elif ast.a_type == ASTType.IN:
        ast: ASTIn
        node = ast.variables
        while node is not None:
            _program.append(CMD.INPUT)
            _program.append(node.t_type.value)
            _program.append(CMD.STORE)
            _program.append(_var_table[node.name])
            node = node.next_node

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        node = ast.expressions
        while node is not None:
            translate_expression(node)
            _program.append(CMD.OUTPUT)
            node = node.next_node
    else:
        raise ValueError("Оператор не определён")
