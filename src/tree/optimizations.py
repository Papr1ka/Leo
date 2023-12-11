from src.lang import Integer
from src.tree.tree import *


def division_to_mod_check(ast: ASTTyped) -> Union[ASTBinOperation | None]:
    if ast.a_type == ASTType.BIN_OP and ast.operation == BinOperations.eq:
        if (ast.right.t_type == Types.int and
                ast.left.t_type == Types.int and
                ast.right.a_type == ASTType.VAR and
                ast.left.a_type == ASTType.BIN_OP and
                ast.left.operation == BinOperations.mul):
            node: ASTBinOperation = ast.left
            first_var_name = ast.right.name
            if (
                    node.right.a_type == ASTType.VAR and node.left.a_type == ASTType.BIN_OP and node.left.operation == BinOperations.div):
                second_var_name = node.right.name
                node: ASTBinOperation = node.left
                if (node.left.a_type == ASTType.VAR and node.right.a_type == ASTType.VAR):
                    if node.left.name == first_var_name and node.right.name == second_var_name:
                        return ASTBinOperation(ASTBinOperation(ast.right, ast.left.right, BinOperations.mod),
                                               ASTConst(Types.int, Integer(0)), BinOperations.eq)


def optimize_tree(ast: ASTNode):
    while ast is not None:
        optimize_one(ast)
        ast = ast.next_node


def optimize_expression(ast: ASTTyped) -> Union[ASTNode | None]:
    mod_check_operation = division_to_mod_check(ast)
    if mod_check_operation is not None:
        return mod_check_operation


def optimize_one(ast: ASTNode):
    if ast.a_type == ASTType.ASSIGNMENT:
        ast: ASTAssignment
        r = optimize_expression(ast.value)
        if r is not None:
            ast.value = r

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        r = optimize_expression(ast.condition)
        if r is not None:
            ast.condition = r
        node = ast.branch
        while node is not None:
            optimize_one(node)
            node = node.next_node
        if ast.else_branch is not None:
            node = ast.else_branch
            while node is not None:
                optimize_one(node)
                node = node.next_node

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        r = optimize_expression(ast.condition)
        if r is not None:
            ast.condition = r

        node = ast.body
        while node is not None:
            optimize_one(node)
            node = node.next_node

    elif ast.a_type == ASTType.ForLoop:
        ast: ASTForLoop
        r = optimize_expression(ast.step)
        if r is not None:
            ast.step = r

        r = optimize_expression(ast.assignment.value)
        if r is not None:
            ast.assignment.value = r

        r = optimize_expression(ast.condition.right)
        if r is not None:
            ast.condition.right = r

        node = ast.body
        while node is not None:
            optimize_one(node)
            node = node.next_node

    elif ast.a_type == ASTType.IN:
        pass

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        r = optimize_expression(ast.expressions)
        if r is not None:
            ast.expressions = r

        prev = ast.expressions
        node = ast.expressions.next_node

        while node is not None:
            r = optimize_expression(node)
            if r is not None:
                prev.next_node = r

            prev = node
            node = node.next_node
