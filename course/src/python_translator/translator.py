from src.errors import translation_error
from src.tree import *

type_enum_to_type_str_table = {
    Types.int: "int",
    Types.float: "float",
    Types.bool: "bool"
}


def translate(ast: ASTNode):
    r = "\n\n"
    r += "def main():\n"
    while ast is not None:
        r += translate_operator(ast)
        ast = ast.next_node
    r += "\n\n"
    r += "if __name__ == '__main__':\n\tmain()\n"
    return r


def translate_expression(ast: ASTTyped) -> str:
    mod_check_operation = division_to_mod_check(ast)
    if mod_check_operation is not None:
        return translate_expression(mod_check_operation)

    if ast.a_type == ASTType.CONST:
        ast: ASTConst
        return str(ast.value)
    elif ast.a_type == ASTType.VAR:
        ast: ASTVar
        name = str(ast.name)
        if name in ("input", "print"):
            translation_error(f"{name} зарезервировано языком Python")
        return str(ast.name)

    elif ast.a_type == ASTType.U_OP:
        ast: ASTUOperation
        return "(not " + translate_expression(ast.operand) + ")"
    elif ast.a_type == ASTType.BIN_OP:
        ast: ASTBinOperation
        if ast.operation == BinOperations.sum:
            return "(" + translate_expression(ast.left) + " + " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.diff:
            return "(" + translate_expression(ast.left) + " - " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.mul:
            return "(" + translate_expression(ast.left) + " * " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.div:
            if ast.t_type == Types.int:
                return "(" + translate_expression(ast.left) + " // " + translate_expression(ast.right) + ")"
            else:
                return "(" + translate_expression(ast.left) + " / " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.alt:
            return "(" + translate_expression(ast.left) + " or " + translate_expression(ast.right) + ")"
        elif ast.operation == BinOperations.con:
            return "(" + translate_expression(ast.left) + " and " + translate_expression(ast.right) + ")"
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
        node = ast.variables
        r = ""
        while node is not None:
            r += "\t" * tabs + node.name
            r += ": " + type_enum_to_type_str_table.get(ast.t_type) + "\n"
            node = node.next_node

    elif ast.a_type == ASTType.ASSIGNMENT:
        ast: ASTAssignment
        r = "\t" * tabs + ast.var.name + " = " + translate_expression(ast.value)
        r += "\n"

    elif ast.a_type == ASTType.IF:
        ast: ASTIf
        condition = translate_expression(ast.condition)
        r = "\n" + "\t" * tabs + "if " + condition + ":" + "\n"
        node = ast.branch
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node
        if ast.else_branch is not None:
            r += "\t" * tabs + "else:\n"
            node = ast.else_branch
            while node is not None:
                r += translate_operator(node, tabs + 1)
                node = node.next_node

    elif ast.a_type == ASTType.Loop:
        ast: ASTLoop
        condition = translate_expression(ast.condition)
        r = "\n" + "\t" * tabs + "while " + condition + ":" + "\n"
        node = ast.body
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node

    elif ast.a_type == ASTType.ForLoop:
        ast: ASTForLoop
        step = translate_expression(ast.step)

        start = translate_expression(ast.assignment.value)
        end = translate_expression(ast.condition.right)

        r = ("\n" + "\t" * tabs + "for " + ast.assignment.var.name +
             " in range(" + start + ", " + end + ", " + step + "):\n")
        node = ast.body
        while node is not None:
            r += translate_operator(node, tabs + 1)
            node = node.next_node

    elif ast.a_type == ASTType.IN:
        ast: ASTIn
        node = ast.variables
        r = ""
        while node is not None:
            r += "\t" * tabs + node.name + " = "
            if node.t_type == Types.int:
                r += "int("
            elif node.t_type == Types.float:
                r += "float("
            else:
                r += "bool("
            r += "input())\n"
            node = node.next_node

    elif ast.a_type == ASTType.OUT:
        ast: ASTOut
        node = ast.expressions
        r = ""
        while node is not None:
            r += "\t" * tabs + "print(" + translate_expression(node) + ")\n"
            node = node.next_node
    else:
        raise ValueError("Оператор не определён")

    return r
