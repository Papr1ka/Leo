from typing import Generator, Tuple

from src.constants import Lex, Lexeme
from src.errors import ctx_error, expected, expected_msg
from src.lang import get_type_number_from_lex, Types
from src.lang.lang_base_types import BinOperations, Boolean, Float, get_bin_operation_from_lex, Integer
from src.lexer import Lexer
from src.parser.name_table import find_name, new_name
from src.tree import ASTAssignment, ASTBinOperation, ASTConst, ASTDeclaration, ASTIf, ASTIn, ASTLoop, ASTNode, ASTOut, \
    ASTTyped, ASTUOperation, ASTVar


class SyntaxParser:
    lexer: Generator
    lexeme: Lexeme

    def __init__(self, lexer: Lexer):
        self.lexer = iter(lexer.get_lex())
        self.lexeme = self.new_lex()

    def new_lex(self):
        try:
            self.lexeme = next(self.lexer)
        except StopIteration:
            pass
        else:
            return self.lexeme

    def skip(self):
        pass

    def get_lex(self):
        return self.lexeme

    def skip_lex(self, lex: Lex):
        if self.lexeme.lex == lex:
            self.new_lex()
        else:
            expected(lex, self.lexeme)

    def parse(self):
        ast = self.program_parser()
        while ast != None:
            self.print(ast)
            ast = ast.next_node

    def print(self, node: ASTNode):
        if isinstance(node, ASTDeclaration):
            print("Start Declaration")
            print(node.t_type)
            i = node.variables
            while i is not None:
                self.print(i)
                i = i.next_node
            print("End declaration", end="\n\n")
        elif isinstance(node, ASTConst):
            print("Const", node.t_type, node.value.value)
        elif isinstance(node, ASTVar):
            print(node.t_type, node.name)
        elif isinstance(node, ASTAssignment):
            print("Start Assignment")
            self.print(node.var)
            self.print(node.value)
            print("End Assignment", end="\n\n")
        elif isinstance(node, ASTUOperation):
            print("Start U Operation")
            print(node.t_type)
            self.print(node.operand)
            print("End U Operation", end="\n\n")
        elif isinstance(node, ASTBinOperation):
            print("Start Bin Operation")
            print(node.t_type, node.operation)
            i = node.left
            while i is not None:
                self.print(i)
                i = i.next_node

            i = node.right
            while i is not None:
                self.print(i)
                i = i.next_node
            print("End bin Operation", end="\n\n")
        elif isinstance(node, ASTLoop):
            print("Start loop")
            print("Start condition")
            self.print(node.condition)
            print("End condition")
            print("Start loop body")
            i = node.body
            while i is not None:
                self.print(i)
                i = i.next_node
            print("End loop body")
            print("End loop", end="\n\n")
        elif isinstance(node, ASTIf):
            print("Start if")
            print("Start condition")
            self.print(node.condition)
            print("End condition")
            print("Start branch")
            i = node.branch
            while i is not None:
                self.print(i)
                i = i.next_node
            print("End branch")
            print("Start else Branch")
            i = node.else_branch
            while i is not None:
                self.print(i)
                i = i.next_node
            print("End else Branch")
            print("End if", end="\n\n")

    def identifier_declaration(self, t_type: Types, identifier: Lexeme):
        new_name(t_type, identifier)

    def description_parser(self) -> ASTNode:
        if self.lexeme.lex not in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            expected_msg("Тип", self.lexeme)

        identifier_type = get_type_number_from_lex(self.lexeme.lex)
        self.new_lex()
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.identifier_declaration(identifier_type, identifier)
        self.new_lex()

        head = ASTVar(identifier_type, identifier.value)
        tail = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)

            self.identifier_declaration(identifier_type, self.lexeme)
            tail.next_node = ASTVar(identifier_type, self.lexeme.value)
            tail = tail.next_node
            self.new_lex()

        return ASTDeclaration(head)

    def operator_combine_parser(self) -> Tuple[ASTNode, ASTNode]:
        self.skip_lex(Lex.KEYWORD_BEGIN)
        h_head, h_tail = self.operator_parser()
        tail = h_tail
        while self.lexeme.lex == Lex.SEPARATOR_SEMICOLON:
            self.new_lex()

            t_head, t_tail = self.operator_parser()
            tail.next_node = t_head

            tail = t_tail

        self.skip_lex(Lex.KEYWORD_END)
        return h_head, tail

    def identifier_assignment(self, identifier: Lexeme):
        pass

    def factor_parser(self) -> ASTTyped:
        if self.lexeme.lex in (Lex.IDENTIFIER, Lex.NUMBER_BIN, Lex.NUMBER_OCT,
                               Lex.NUMBER_DEC, Lex.NUMBER_HEX, Lex.NUMBER_FRACTIONAL,
                               Lex.KEYWORD_TRUE, Lex.KEYWORD_FALSE, Lex.SEPARATOR_NOT,
                               Lex.SEPARATOR_LEFT_BRACKET):
            if self.lexeme == Lex.SEPARATOR_NOT:
                self.new_lex()
                lex_exp_start = self.lexeme
                node = self.factor_parser()
                if node.t_type != Types.bool:
                    ctx_error("Унарная операция поддерживается только для типа bool", lex_exp_start)

                self.new_lex()

                node = ASTUOperation(node)

                return node

            elif self.lexeme.lex == Lex.SEPARATOR_LEFT_BRACKET:
                self.new_lex()
                node = self.expression_parser()
                self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
                return node
            else:
                factor = self.lexeme
                self.new_lex()
                if factor.lex in (Lex.KEYWORD_TRUE, Lex.KEYWORD_FALSE):
                    return ASTConst(Types.bool, Boolean.from_string(factor.value))
                elif factor.lex == Lex.NUMBER_FRACTIONAL:
                    return ASTConst(Types.float, Float.from_string(factor.value))
                elif factor.lex == Lex.IDENTIFIER:
                    t_item = find_name(factor.value)
                    return ASTVar(t_item.t_type, factor.value)
                return ASTConst(Types.int, Integer.from_string(factor.value))
        else:
            expected_msg("Множитель", self.lexeme)

    def multiplication_parser(self) -> ASTTyped:
        left_node = self.factor_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_MULTIPLICATION, Lex.SEPARATOR_DIVISION, Lex.SEPARATOR_AND):
            operation = self.lexeme
            self.new_lex()
            right_node = self.factor_parser()
            if (
                    left_node.t_type == Types.bool or right_node.t_type == Types.bool) and operation.lex != Lex.SEPARATOR_AND:
                ctx_error("Неподдерживаемая операция для типа bool, возможно вы имели ввиду '&&'", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)

            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def summa_parser(self) -> ASTTyped:
        left_node = self.multiplication_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_PLUS, Lex.SEPARATOR_MINUS, Lex.SEPARATOR_OR):
            operation = self.lexeme
            self.new_lex()
            right_node = self.multiplication_parser()
            if (
                    left_node.t_type == Types.bool or right_node.t_type == Types.bool) and operation.lex != Lex.SEPARATOR_OR:
                ctx_error("Неподдерживаемая операция для типа bool, возможно вы имели ввиду '||'", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)
            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def expression_parser(self) -> ASTTyped:
        left_node = self.summa_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_EQUALS, Lex.SEPARATOR_NOT_EQUALS, Lex.SEPARATOR_LT,
                                  Lex.SEPARATOR_LTE, Lex.SEPARATOR_GT, Lex.SEPARATOR_GTE):
            operation = self.lexeme
            self.new_lex()
            right_node = self.summa_parser()
            if (left_node.t_type == Types.bool or right_node.t_type == Types.bool) and operation.lex not in (
                    Lex.SEPARATOR_EQUALS, Lex.SEPARATOR_NOT_EQUALS):
                ctx_error("Неподдерживаемая операция для типа bool", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)
            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def operator_assignment_parser(self) -> ASTAssignment:
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.new_lex()
        self.skip_lex(Lex.SEPARATOR_ASSIGNMENT)
        exp_start_lex = self.lexeme
        node_expression = self.expression_parser()
        identifier_type = find_name(identifier.value)
        if identifier_type is None:
            ctx_error("Переменная не объявлена", identifier)
        elif identifier_type.t_type != node_expression.t_type:
            ctx_error(f"Присваиваемое выражение имеет отличный тип от типа переменной, \
ожидается {identifier_type.t_type.name}", exp_start_lex)
        var = ASTVar(identifier_type.t_type, identifier_type.name)

        return ASTAssignment(var, node_expression)

    def operator_if_parser(self) -> ASTNode:
        self.skip_lex(Lex.KEYWORD_IF)
        self.skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        node_condition = self.expression_parser()
        self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        node_branch, _ = self.operator_parser()

        if self.lexeme == Lex.KEYWORD_ELSE:
            self.new_lex()
            node_else_branch, _ = self.operator_parser()

            return ASTIf(node_condition, node_branch, else_branch=node_else_branch)

        return ASTIf(node_condition, node_branch)

    def operator_for_parser(self) -> Tuple[ASTNode, ASTNode]:
        node_step = None
        self.skip_lex(Lex.KEYWORD_FOR)
        node_assignment = self.operator_assignment_parser()
        self.skip_lex(Lex.KEYWORD_TO)
        node_condition = self.expression_parser()

        if self.lexeme.lex == Lex.KEYWORD_STEP:
            self.new_lex()
            lex_expression_start = self.lexeme
            node_expression = self.expression_parser()

            if node_assignment.var.t_type != node_expression.t_type:
                ctx_error(f"Несоответствие типов, выражение в step должно быть типа \
{node_assignment.var.name} ({node_assignment.var.t_type.name})", lex_expression_start)

            node_step = ASTAssignment(node_assignment.var,
                                      ASTBinOperation(node_assignment.var, node_expression, BinOperations.sum))

        node_body_start, node_body_end = self.operator_parser()
        if node_step is not None:
            node_body_end.next_node = node_step

        self.skip_lex(Lex.KEYWORD_NEXT)

        node_loop = ASTLoop(node_condition, node_body_start)

        node_assignment.next_node = node_loop
        return node_assignment, node_loop

    def operator_while_parser(self) -> ASTNode:
        self.skip_lex(Lex.KEYWORD_WHILE)
        self.skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        node_condition = self.expression_parser()
        self.skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        node_body, _ = self.operator_parser()
        return ASTLoop(node_condition, node_body)

    def operator_readln_parser(self) -> ASTNode:
        self.skip_lex(Lex.KEYWORD_READLN)
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        var = find_name(identifier.value)
        if var is None:
            ctx_error("Переменная не объявлена", identifier)

        self.new_lex()

        head = ASTVar(var.t_type, var.name)
        node = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)
            identifier = self.lexeme
            var = find_name(identifier.value)
            if var is None:
                ctx_error("Переменная не объявлена", identifier)

            node.next_node = ASTVar(var.t_type, var.name)
            node = node.next_node
            self.new_lex()

        return ASTIn(head)

    def operator_writeln_parser(self) -> ASTNode:
        self.skip_lex(Lex.KEYWORD_WRITELN)
        head = self.expression_parser()
        node = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.new_lex()
            node.next_node = self.expression_parser()
            node = node.next_node
        return ASTOut(head)

    def operator_parser(self) -> Tuple[ASTNode, ASTNode]:
        node = None
        if self.lexeme.lex == Lex.KEYWORD_BEGIN:
            return self.operator_combine_parser()
        elif self.lexeme.lex == Lex.IDENTIFIER:
            node = self.operator_assignment_parser()
        elif self.lexeme.lex == Lex.KEYWORD_IF:
            node = self.operator_if_parser()
        elif self.lexeme.lex == Lex.KEYWORD_FOR:
            return self.operator_for_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WHILE:
            node = self.operator_while_parser()
        elif self.lexeme.lex == Lex.KEYWORD_READLN:
            node = self.operator_readln_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WRITELN:
            node = self.operator_writeln_parser()
        else:
            expected_msg("Оператор", self.lexeme)
        return node, node

    def description_or_operator_seq(self) -> Tuple[ASTNode, ASTNode]:
        head = None
        tail = None
        while self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL,
                                  Lex.KEYWORD_BEGIN, Lex.IDENTIFIER, Lex.KEYWORD_IF,
                                  Lex.KEYWORD_FOR, Lex.KEYWORD_WHILE, Lex.KEYWORD_READLN,
                                  Lex.KEYWORD_WRITELN):
            h_head, h_tail = self.description_or_operator_parser()
            if head is None:
                head = h_head
                tail = h_tail
            else:
                tail.next_node = h_head
                tail = h_tail
            self.skip_lex(Lex.SEPARATOR_SEMICOLON)
        return head, tail

    def description_or_operator_parser(self) -> Tuple[ASTNode, ASTNode]:
        if self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            node = self.description_parser()
            return node, node
        else:
            return self.operator_parser()

    def program_parser(self) -> ASTNode:
        self.skip_lex(Lex.SEPARATOR_LEFT_FIGURE_BRACKET)

        h_head, h_tail = self.description_or_operator_parser()
        self.skip_lex(Lex.SEPARATOR_SEMICOLON)

        t_head, t_tail = self.description_or_operator_seq()
        if t_head is not None:
            h_tail.next_node = t_head

        self.skip_lex(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)

        print("Синтаксический и семантический анализ закончен")
        return h_head
