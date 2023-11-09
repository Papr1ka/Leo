from enum import Enum
from typing import Any, Union

from src.lang import BinOperations, Types, operator_relation


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


class ASTNode:
    """
    Базовый узел, имеет тип узла, ссылку на следующий узел
    """
    a_type: ASTType
    next_node: Any  # ASTNode

    def __init__(self, a_type: ASTType):
        self.a_type = a_type
        self.next_node = None


class ASTTyped(ASTNode):
    """
    Типизированный узел, может быть переменной, выражением, константой
    """
    t_type: Types

    def __init__(self, t_type: Types, a_type: ASTType):
        super().__init__(a_type)
        self.t_type = t_type


class ASTConst(ASTTyped):
    """
    Константа
    """
    value: Any

    def __init__(self, t_type: Types, value: Any):
        super().__init__(t_type, ASTType.CONST)
        self.value = value


class ASTVar(ASTTyped):
    """
    Переменная
    """
    name: str

    def __init__(self, t_type: Types, name: str):
        super().__init__(t_type, ASTType.VAR)
        self.name = name


class ASTAssignment(ASTNode):
    """
    Оператор присваивания
    """
    var: ASTVar
    value: ASTTyped

    def __init__(self, var: ASTVar, value: ASTTyped):
        super().__init__(ASTType.ASSIGNMENT)
        self.var = var
        self.value = value


class ASTIf(ASTNode):
    """
    Условный оператор
    """
    condition: ASTTyped
    branch: ASTNode  # Список
    else_branch: Union[ASTNode, None]  # Список

    def __init__(self, condition: ASTTyped, branch: ASTNode, else_branch: ASTNode = None):
        super().__init__(ASTType.IF)
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

    def __init__(self, left: ASTTyped, right: ASTTyped, operation: BinOperations):
        if operation in operator_relation:
            super().__init__(Types.bool, ASTType.BIN_OP)
        else:
            super().__init__(left.t_type, ASTType.BIN_OP)
        self.left = left
        self.right = right
        self.operation = operation


class ASTUOperation(ASTTyped):
    """
    Унарная операция (только '!' - отрицание)
    """
    operand = ASTTyped

    def __init__(self, operand: ASTTyped, parent=None):
        super().__init__(operand.t_type, ASTType.U_OP)
        self.operand = operand


class ASTLoop(ASTNode):
    """
    Цикл
    """
    condition: ASTTyped
    body: ASTNode

    def __init__(self, condition: ASTTyped, body: ASTNode):
        super().__init__(ASTType.Loop)
        self.condition = condition
        self.body = body


class ASTDeclaration(ASTTyped):
    """
    Оператор определения переменных
    """
    variables: ASTVar  # список

    def __init__(self, variables: ASTVar, parent=None):
        super().__init__(variables.t_type, ASTType.DECL)
        self.variables = variables


class ASTIn(ASTNode):
    """
    Оператор ввода
    """
    variables: ASTVar  # список

    def __init__(self, variables: ASTVar):
        super().__init__(ASTType.IN)
        self.variables = variables


class ASTOut(ASTNode):
    """
    Оператор вывода
    """
    expressions: ASTTyped  # список

    def __init__(self, expressions: ASTTyped):
        super().__init__(ASTType.OUT)
        self.expressions = expressions
