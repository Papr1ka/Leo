from typing import Union

from src.lang import BinOperations, Boolean, Float, Integer, Types
from src.lexer import Lexer
from src.tree import ASTAssignment, ASTBinOperation, ASTConst, ASTIf, ASTIn, ASTLoop, ASTNode, ASTOut, ASTType, \
    ASTTyped, ASTUOperation, \
    ASTVar
from .runtime_memory import load, store
from ..text_driver import setup_source


def run(ast: ASTNode):
    while ast is not None:
        exec_operator(ast)
        ast = ast.next_node

    print("Выполнение завершено")


def exec_expression(ast: ASTTyped) -> Union[Integer, Float, Boolean]:
    if ast.a_type == ASTType.CONST:
        ast: ASTConst
        return ast.value
    elif ast.a_type == ASTType.VAR:
        ast: ASTVar
        return load(ast.name)
    elif ast.a_type == ASTType.U_OP:
        ast: ASTUOperation
        return exec_expression(ast.operand).not_()
    elif ast.a_type == ASTType.BIN_OP:
        ast: ASTBinOperation
        if ast.operation == BinOperations.sum:
            return exec_expression(ast.left).add(exec_expression(ast.right))
        elif ast.operation == BinOperations.diff:
            return exec_expression(ast.left).sub(exec_expression(ast.right))
        elif ast.operation == BinOperations.mul:
            return exec_expression(ast.left).mul(exec_expression(ast.right))
        elif ast.operation == BinOperations.div:
            return exec_expression(ast.left).div(exec_expression(ast.right))
        elif ast.operation == BinOperations.alt:
            return exec_expression(ast.left).or_(exec_expression(ast.right))
        elif ast.operation == BinOperations.con:
            return exec_expression(ast.left).and_(exec_expression(ast.right))
        elif ast.operation == BinOperations.lt:
            return exec_expression(ast.left).lt(exec_expression(ast.right))
        elif ast.operation == BinOperations.lte:
            return exec_expression(ast.left).lte(exec_expression(ast.right))
        elif ast.operation == BinOperations.gt:
            return exec_expression(ast.left).gt(exec_expression(ast.right))
        elif ast.operation == BinOperations.gte:
            return exec_expression(ast.left).gte(exec_expression(ast.right))
        elif ast.operation == BinOperations.eq:
            return exec_expression(ast.left).eq(exec_expression(ast.right))
        elif ast.operation == BinOperations.neq:
            return exec_expression(ast.left).neq(exec_expression(ast.right))
        else:
            raise ValueError("Неопределённая операция")


def exec_operator(ast: ASTNode):
    if ast.a_type == ASTType.DECL:
        return None

    elif ast.a_type == ASTType.ASSIGNMENT:
        ast: ASTAssignment
        store(ast.var.name, exec_expression(ast.value))

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        condition: Boolean = exec_expression(ast.condition)
        if condition.value:
            node = ast.branch
            while node is not None:
                exec_operator(node)
                node = node.next_node
        else:
            if ast.else_branch is not None:
                node = ast.else_branch
                while node is not None:
                    exec_operator(node)
                    node = node.next_node

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        condition: Boolean = exec_expression(ast.condition)
        while condition.value:
            node = ast.body
            while node is not None:
                exec_operator(node)
                node = node.next_node
            condition = exec_expression(ast.condition)
    elif ast.a_type == ASTType.IN:
        ast: ASTIn
        node = ast.variables
        while node is not None:
            input_data = input()
            setup_source(input_data)
            lexer = Lexer()

            lexeme = next(iter(lexer.get_lex()))
            if ast.variables.t_type == Types.int:
                value = Integer.from_string(lexeme.value)
            elif ast.variables.t_type == Types.float:
                value = Float.from_string(lexeme.value)
            else:
                value = Boolean.from_string(lexeme.value)
            store(node.name, value)
            node = node.next_node

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        node = ast.expressions
        while node is not None:
            value = exec_expression(node)
            print(value)
            node = node.next_node
    else:
        raise ValueError("Оператор не определён")
