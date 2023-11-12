"""
Модуль синтезации программы на c++ из абстрактного дерева
"""

from src.tree import *

type_enum_to_type_str_table = {
    Types.int: "long long",
    Types.float: "double",
    Types.bool: "bool"
}


def translate(ast: ASTNode):
    r = "#include <iostream>\n\n"
    r += "int main()\n{\n"
    while ast is not None:
        r += translate_operator(ast)
        ast = ast.next_node
    r += "\treturn 0;\n}\n"
    return r


def translate_expression(ast: ASTTyped) -> str:
    if ast.a_type == ASTType.CONST:
        ast: ASTConst
        return str(ast.value)
    elif ast.a_type == ASTType.VAR:
        ast: ASTVar
        return str(ast.name)

    elif ast.a_type == ASTType.U_OP:
        ast: ASTUOperation
        return "(!" + translate_expression(ast.operand) + ")"
    elif ast.a_type == ASTType.BIN_OP:
        ast: ASTBinOperation
        if ast.operation == BinOperations.sum:
            return "(" + translate_expression(ast.left) + " + " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.diff:
            return "(" + translate_expression(ast.left) + " - " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.mul:
            return "(" + translate_expression(ast.left) + " * " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.div:
            return "(" + translate_expression(ast.left) + " / " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.alt:
            return "(" + translate_expression(ast.left) + " || " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.con:
            return "(" + translate_expression(ast.left) + " && " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.lt:
            return "(" + translate_expression(ast.left) + " < " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.lte:
            return "(" + translate_expression(ast.left) + " <= " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.gt:
            return "(" + translate_expression(ast.left) + " > " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.gte:
            return "(" + translate_expression(ast.left) + " >= " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.eq:
            return "(" + translate_expression(ast.left) + " == " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.neq:
            return "(" + translate_expression(ast.left) + " != " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.mod:
            return "(" + translate_expression(ast.left) + " % " + translate_expression(ast.right) + ")"
        else:
            raise ValueError("Неопределённая операция")


def translate_operator(ast: ASTNode, tabs: int = 1):
    if ast.a_type == ASTType.DECL:
        ast: ASTDeclaration
        r = "\t" * tabs + type_enum_to_type_str_table.get(ast.t_type)
        node = ast.variables
        r += " " + node.name
        node = node.next_node
        while node is not None:
            r += ", " + node.name
            node = node.next_node
        r += ";\n"
        return r

    elif ast.a_type == ASTType.ASSIGNMENT:
        ast: ASTAssignment
        r = "\t" * tabs + ast.var.name + " = " + translate_expression(ast.value)
        r += ";\n"
        return r

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        condition = translate_expression(ast.condition)
        r = "\t" * tabs + "if (" + condition + ")" + "\n" + "\t" * tabs + "{\n"
        node = ast.branch
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node
        r += "\t" * tabs + "}\n"
        if ast.else_branch is not None:
            r += "\t" * tabs + "else\n" + "\t" * tabs + "{\n"
            node = ast.else_branch
            while node is not None:
                r += translate_operator(node, tabs + 1)
                node = node.next_node
            r += "\t" * tabs + "}\n"
        return r

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        condition = translate_expression(ast.condition)
        r = "\t" * tabs + "while (" + condition + ")" + "\n" + "\t" * tabs + "{\n"
        node = ast.body
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node
        r += "\t" * tabs + "}\n"
        return r

    elif ast.a_type == ASTType.ForLoop:
        ast: ASTForLoop
        assignment = type_enum_to_type_str_table.get(
            Types.int) + " " + ast.assignment.var.name + " = " + translate_expression(ast.assignment.value)
        condition = translate_expression(ast.condition)
        step = translate_expression(ast.step)
        r = ("\t" * tabs + "for (" + assignment + "; " + condition + "; " + ast.assignment.var.name +
             " += " + step + ")" + "\n" + "\t" * tabs + "{\n")
        node = ast.body
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node

        r += "\t" * tabs + "}\n"
        return r

    elif ast.a_type == ASTType.IN:
        ast: ASTIn
        node = ast.variables
        r = ""
        while node is not None:
            r += "\t" * tabs + "std::cin >> " + node.name + ";\n"
            node = node.next_node
        return r

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        node = ast.expressions
        r = ""
        while node is not None:
            r += "\t" * tabs + "std::cout << " + translate_expression(node) + " << std::endl;\n"
            node = node.next_node
        return r
    else:
        raise ValueError("Оператор не определён")
