import weakref
from enum import Enum
from typing import Any, Union

from src.lang import BinOperations, Types


class ASTType(Enum):
    ASSIGNMENT = 0
    IF = 1
    Loop = 2
    IN = 3
    OUT = 4
    DECL = 5
    U_OP = 6
    BIN_OP = 7
    CONST = 8
    VAR = 9
    Branch = 10


class ASTNode:
    """
    Базовый узел, имеет тип узла, ссылку на следующий узел
    """
    a_type: ASTType
    parent: Union[weakref, None]  # Родитель
    next_node: Any  # ASTNode

    def __init__(self, a_type: ASTType, parent=None):
        self.a_type = a_type
        self.parent = parent
        self.next_node = None


class ASTTyped(ASTNode):
    """
    Типизированный узел, может быть переменной, выражением, константой
    """
    t_type: Types

    def __init__(self, t_type: Types, a_type: ASTType, parent=None):
        super().__init__(a_type, parent)
        self.t_type = t_type


#
# class ASTBranch(ASTNode):
#     """
#     Ветка, имеет свой односвязный список, создана для того, чтобы можно было последовательно выполнить несколько операторов
#     например:
#     Имеем программу:
#     if ()
#         begin
#         operator1
#         operator2
#         end
#     else
#         begin
#         operator3
#         operator4
#         end
#     operator5
#     operator1 и operator2 создадут первую ветку
#     operator3 и operator4 создадут четвёртую ветку
#     а когда ветка исчерпается, по указателю на следующий узел самого узла (next_node) (а не узла branch.next_node)
#     перейдём на operator5
#     """
#     branch: ASTNode  # список
#
#     def __init__(self, branch: ASTNode, parent=None):
#         super().__init__(ASTType.Branch, parent)
#         self.branch = branch


class ASTConst(ASTTyped):
    """
    Константа
    """
    value: Any

    def __init__(self, t_type: Types, value: Any, parent=None):
        super().__init__(t_type, ASTType.CONST, parent)
        self.value = value


class ASTVar(ASTTyped):
    """
    Переменная
    """
    name: str

    def __init__(self, t_type: Types, name: str, parent=None):
        super().__init__(t_type, ASTType.VAR, parent)
        self.name = name


class ASTAssignment(ASTNode):
    """
    Оператор присваивания
    """
    var: ASTVar
    value: ASTTyped

    def __init__(self, var: ASTVar, value: ASTTyped, parent=None):
        super().__init__(ASTType.ASSIGNMENT, parent)
        self.var = var
        self.value = value


class ASTIf(ASTNode):
    """
    Условный оператор
    """
    condition: ASTTyped
    branch: ASTNode  # Список
    else_branch: Union[ASTNode, None]  # Список

    def __init__(self, condition: ASTTyped, branch: ASTNode, else_branch: ASTNode = None, parent=None):
        super().__init__(ASTType.IF, parent)
        self.condition = condition
        self.branch = branch
        self.else_branch = else_branch


class ASTBinOperation(ASTTyped):
    """
    Бинарная операция
    """
    left: ASTTyped
    right: ASTTyped
    operation: BinOperations

    def __init__(self, left: ASTTyped, right: ASTTyped, operation: BinOperations, parent=None):
        super().__init__(left.t_type, ASTType.BIN_OP, parent)
        self.left = left
        self.right = right
        self.operation = operation


class ASTUOperation(ASTTyped):
    """
    Унарная операция (только '!' - отрицание)
    """
    operand = ASTTyped

    def __init__(self, operand: ASTTyped, parent=None):
        super().__init__(operand.t_type, ASTType.U_OP, parent)
        self.operand = operand


class ASTLoop(ASTNode):
    """
    Цикл
    """
    condition: ASTTyped
    body: ASTNode

    def __init__(self, condition: ASTTyped, body: ASTNode, parent=None):
        super().__init__(ASTType.Loop, parent)
        self.condition = condition
        self.body = body


class ASTDeclaration(ASTTyped):
    """
    Оператор определения переменных
    """
    variables: ASTVar  # список

    def __init__(self, variables: ASTVar, parent=None):
        super().__init__(variables.t_type, ASTType.DECL, parent)
        self.variables = variables


class ASTIn(ASTNode):
    """
    Оператор ввода
    """
    variables: ASTVar  # список

    def __init__(self, variables: ASTVar, parent=None):
        super().__init__(ASTType.IN, parent)
        self.variables = variables


class ASTOut(ASTNode):
    """
    Оператор вывода
    """
    expressions: ASTTyped  # список

    def __init__(self, expressions: ASTTyped, parent=None):
        super().__init__(ASTType.OUT, parent)
        self.expressions = expressions
