from typing import Generator, Tuple

from src.constants import Lex, Lexeme
from src.errors import ctx_error, expected, expected_msg
from src.lang import get_type_number_from_lex, Types
from src.lang.lang_base_types import Boolean, Float, get_bin_operation_from_lex, Integer
from src.lexer import Lexer
from src.parser.name_table import close_scope, find_name, new_name, open_scope
from src.tree import ASTAssignment, ASTBinOperation, ASTConst, ASTDeclaration, ASTForLoop, ASTIf, ASTIn, ASTLoop, \
    ASTNode, ASTOut, \
    ASTTyped, ASTUOperation, ASTVar, optimize_tree


class Parser:
    lexer: Generator
    lexeme: Lexeme

    def __init__(self, lexer: Lexer):
        self.lexer = iter(lexer.get_lex())
        self.lexeme = self.__new_lex()

    def __new_lex(self):
        try:
            self.lexeme = next(self.lexer)
        except StopIteration:
            pass
        else:
            return self.lexeme

    def __get_lex(self):
        return self.lexeme

    def __skip_lex(self, lex: Lex):
        if self.lexeme.lex == lex:
            self.__new_lex()
        else:
            expected(lex, self.lexeme)

    def parse(self) -> ASTNode:
        open_scope()
        ast = self.__program_parser()
        close_scope()
        optimize_tree(ast)
        return ast

    def __identifier_declaration(self, t_type: Types, identifier: Lexeme, readonly=False):
        new_name(t_type, identifier, readonly=readonly)

    def __description_parser(self) -> ASTNode:
        if self.lexeme.lex not in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            expected_msg("Тип", self.lexeme)

        identifier_type = get_type_number_from_lex(self.lexeme.lex)
        self.__new_lex()
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.__identifier_declaration(identifier_type, identifier)
        self.__new_lex()

        head = ASTVar(identifier_type, identifier.value)
        tail = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.__new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)

            self.__identifier_declaration(identifier_type, self.lexeme)
            tail.next_node = ASTVar(identifier_type, self.lexeme.value)
            tail = tail.next_node
            self.__new_lex()

        return ASTDeclaration(head)

    def __operator_combine_parser(self) -> Tuple[ASTNode, ASTNode]:
        self.__skip_lex(Lex.SEPARATOR_LEFT_FIGURE_BRACKET)
        h_head, h_tail = self.__operator_parser()
        tail = h_tail
        while self.lexeme.lex != Lex.SEPARATOR_RIGHT_FIGURE_BRACKET:
            t_head, t_tail = self.__operator_parser()
            tail.next_node = t_head

            tail = t_tail

        self.__skip_lex(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)
        return h_head, tail

    def __identifier_assignment(self, identifier: Lexeme):
        find_name(identifier.value).is_assigned = True

    def __factor_parser(self) -> ASTTyped:
        if self.lexeme.lex in (Lex.IDENTIFIER, Lex.NUMBER_BIN, Lex.NUMBER_OCT,
                               Lex.NUMBER_DEC, Lex.NUMBER_HEX, Lex.NUMBER_FRACTIONAL,
                               Lex.KEYWORD_TRUE, Lex.KEYWORD_FALSE, Lex.SEPARATOR_NOT,
                               Lex.SEPARATOR_LEFT_BRACKET):
            if self.lexeme.lex == Lex.SEPARATOR_NOT:
                self.__new_lex()
                lex_exp_start = self.lexeme
                node = self.__factor_parser()
                if node.t_type != Types.bool:
                    ctx_error("Унарная операция поддерживается только для типа bool", lex_exp_start)

                node = ASTUOperation(node)

                return node

            elif self.lexeme.lex == Lex.SEPARATOR_LEFT_BRACKET:
                self.__new_lex()
                node = self.__expression_parser()
                self.__skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
                return node
            else:
                factor = self.lexeme
                self.__new_lex()
                if factor.lex in (Lex.KEYWORD_TRUE, Lex.KEYWORD_FALSE):
                    return ASTConst(Types.bool, Boolean.from_string(factor.value))
                elif factor.lex == Lex.NUMBER_FRACTIONAL:
                    return ASTConst(Types.float, Float.from_string(factor.value))
                elif factor.lex == Lex.IDENTIFIER:
                    t_item = find_name(factor.value)
                    if t_item is None:
                        ctx_error("Переменная не объявлена в этой области видимости", factor)
                    elif not t_item.is_assigned:
                        ctx_error("Переменная не инициализированна", factor)

                    return ASTVar(t_item.t_type, factor.value)
                return ASTConst(Types.int, Integer.from_string(factor.value))
        else:
            expected_msg("Выражение", self.lexeme)

    def __multiplication_parser(self) -> ASTTyped:
        left_node = self.__factor_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_MULTIPLICATION, Lex.SEPARATOR_DIVISION, Lex.SEPARATOR_AND):
            operation = self.lexeme
            self.__new_lex()
            right_node = self.__factor_parser()
            if ((left_node.t_type == Types.bool or right_node.t_type == Types.bool) and
                    operation.lex != Lex.SEPARATOR_AND):
                ctx_error("Неподдерживаемая операция для типа bool, возможно вы имели ввиду '&&'", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)
            elif left_node.t_type in (Types.int, Types.float) and operation.lex == Lex.SEPARATOR_AND:
                ctx_error("Неподдерживаемая операция для числового типа", operation)

            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def __summa_parser(self) -> ASTTyped:
        left_node = self.__multiplication_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_PLUS, Lex.SEPARATOR_MINUS, Lex.SEPARATOR_OR):
            operation = self.lexeme
            self.__new_lex()
            right_node = self.__multiplication_parser()
            if ((left_node.t_type == Types.bool or right_node.t_type == Types.bool) and
                    operation.lex != Lex.SEPARATOR_OR):
                ctx_error("Неподдерживаемая операция для типа bool, возможно вы имели ввиду '||'", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)
            elif left_node.t_type in (Types.int, Types.float) and operation.lex == Lex.SEPARATOR_OR:
                ctx_error("Неподдерживаемая операция для числового типа", operation)
            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def __expression_parser(self) -> ASTTyped:
        left_node = self.__summa_parser()
        node = left_node
        while self.lexeme.lex in (Lex.SEPARATOR_EQUALS, Lex.SEPARATOR_NOT_EQUALS, Lex.SEPARATOR_LT,
                                  Lex.SEPARATOR_LTE, Lex.SEPARATOR_GT, Lex.SEPARATOR_GTE):
            operation = self.lexeme
            self.__new_lex()
            right_node = self.__summa_parser()
            if (left_node.t_type == Types.bool or right_node.t_type == Types.bool) and operation.lex not in (
                    Lex.SEPARATOR_EQUALS, Lex.SEPARATOR_NOT_EQUALS):
                ctx_error("Неподдерживаемая операция для типа bool", operation)
            elif left_node.t_type != right_node.t_type:
                ctx_error("Типы операндов не совпадают", operation)
            node = ASTBinOperation(node, right_node, get_bin_operation_from_lex(operation.lex))
        return node

    def __operator_assignment_parser(self) -> ASTAssignment:
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        self.__new_lex()
        self.__skip_lex(Lex.SEPARATOR_ASSIGNMENT)
        exp_start_lex = self.lexeme
        node_expression = self.__expression_parser()
        identifier_type = find_name(identifier.value)
        if identifier_type is None:
            ctx_error("Переменная не объявлена", identifier)
        elif identifier_type.readonly:
            ctx_error(f"Переменная доступна только для чтения", identifier)
        elif identifier_type.t_type != node_expression.t_type:
            ctx_error(f"Присваиваемое выражение имеет отличный тип от типа переменной, \
ожидается {identifier_type.t_type.name}", exp_start_lex)
        var = ASTVar(identifier_type.t_type, identifier_type.name)
        self.__identifier_assignment(identifier)

        return ASTAssignment(var, node_expression)

    def __operator_if_parser(self) -> ASTIf:
        self.__skip_lex(Lex.KEYWORD_IF)
        self.__skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        lex_condition_start = self.lexeme
        node_condition = self.__expression_parser()
        if node_condition.t_type != Types.bool:
            ctx_error("Условие должно быть типа bool", lex_condition_start)
        self.__skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        node_branch, _ = self.__operator_parser()

        if self.lexeme.lex == Lex.KEYWORD_ELSE:
            self.__new_lex()
            node_else_branch, _ = self.__operator_parser()

            return ASTIf(node_condition, node_branch, else_branch=node_else_branch)

        return ASTIf(node_condition, node_branch)

    def __operator_for_parser(self) -> ASTForLoop:
        self.__skip_lex(Lex.KEYWORD_FOR)
        lex_assignment_start = self.lexeme

        open_scope()
        identifier_type = Types.int
        self.__identifier_declaration(identifier_type, lex_assignment_start)

        node_assignment = self.__operator_assignment_parser()
        if node_assignment.var.t_type != Types.int:
            ctx_error("Переменная цикла for должна быть типа int, иначе используйте while", lex_assignment_start)

        identifier = find_name(lex_assignment_start.value)
        identifier.readonly = True

        self.__skip_lex(Lex.KEYWORD_TO)
        lex_expression_start = self.lexeme
        node_expression = self.__expression_parser()
        if node_expression.t_type != Types.int:
            ctx_error("Условие цикла for должно быть типа int", lex_expression_start)

        if self.lexeme.lex == Lex.KEYWORD_STEP:
            self.__new_lex()
            lex_expression_start = self.lexeme
            node_step = self.__expression_parser()

            if node_step.t_type != Types.int:
                ctx_error(f"Несоответствие типов, выражение в step должно быть типа int \
({node_assignment.var.t_type.name})", lex_expression_start)
        else:
            node_step = ASTConst(Types.int, Integer(1))

        node_body_start, _ = self.__operator_parser()

        node_loop = ASTForLoop(node_assignment, node_expression, node_body_start, node_step)
        close_scope()
        return node_loop

    def __operator_while_parser(self) -> ASTLoop:
        self.__skip_lex(Lex.KEYWORD_WHILE)
        self.__skip_lex(Lex.SEPARATOR_LEFT_BRACKET)
        lex_condition_start = self.lexeme
        node_condition = self.__expression_parser()
        if node_condition.t_type != Types.bool:
            ctx_error("Условие должно быть типа bool", lex_condition_start)
        self.__skip_lex(Lex.SEPARATOR_RIGHT_BRACKET)
        node_body, _ = self.__operator_parser()
        return ASTLoop(node_condition, node_body)

    def __operator_readln_parser(self) -> ASTIn:
        self.__skip_lex(Lex.KEYWORD_READLN)
        if self.lexeme.lex != Lex.IDENTIFIER:
            expected(Lex.IDENTIFIER, self.lexeme)

        identifier = self.lexeme
        var = find_name(identifier.value)
        if var is None:
            ctx_error("Переменная не объявлена", identifier)
        elif var.readonly:
            ctx_error(f"Переменная доступна только для чтения", identifier)
        self.__identifier_assignment(identifier)
        self.__new_lex()

        head = ASTVar(var.t_type, var.name)
        node = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.__new_lex()
            if self.lexeme.lex != Lex.IDENTIFIER:
                expected(Lex.IDENTIFIER, self.lexeme)
            identifier = self.lexeme
            var = find_name(identifier.value)
            if var is None:
                ctx_error("Переменная не объявлена", identifier)
            self.__identifier_assignment(identifier)
            node.next_node = ASTVar(var.t_type, var.name)
            node = node.next_node
            self.__new_lex()

        return ASTIn(head)

    def __operator_writeln_parser(self) -> ASTOut:
        self.__skip_lex(Lex.KEYWORD_WRITELN)
        head = self.__expression_parser()
        node = head

        while self.lexeme.lex == Lex.SEPARATOR_COMMA:
            self.__new_lex()
            node.next_node = self.__expression_parser()
            node = node.next_node
        return ASTOut(head)

    def __operator_parser(self) -> Tuple[ASTNode, ASTNode]:
        node = None
        if self.lexeme.lex == Lex.SEPARATOR_LEFT_FIGURE_BRACKET:
            return self.__operator_combine_parser()
        elif self.lexeme.lex == Lex.IDENTIFIER:
            node = self.__operator_assignment_parser()
        elif self.lexeme.lex == Lex.KEYWORD_IF:
            node = self.__operator_if_parser()
        elif self.lexeme.lex == Lex.KEYWORD_FOR:
            node = self.__operator_for_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WHILE:
            node = self.__operator_while_parser()
        elif self.lexeme.lex == Lex.KEYWORD_READLN:
            node = self.__operator_readln_parser()
        elif self.lexeme.lex == Lex.KEYWORD_WRITELN:
            node = self.__operator_writeln_parser()
        else:
            expected_msg("Оператор", self.lexeme)
        return node, node

    def __description_or_operator_seq_parser(self) -> Tuple[ASTNode, ASTNode]:
        head = None
        tail = None
        while self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL,
                                  Lex.SEPARATOR_LEFT_FIGURE_BRACKET, Lex.IDENTIFIER, Lex.KEYWORD_IF,
                                  Lex.KEYWORD_FOR, Lex.KEYWORD_WHILE, Lex.KEYWORD_READLN,
                                  Lex.KEYWORD_WRITELN):
            h_head, h_tail = self.__description_or_operator_parser()
            if head is None:
                head = h_head
                tail = h_tail
            else:
                tail.next_node = h_head
                tail = h_tail
        return head, tail

    def __description_or_operator_parser(self) -> Tuple[ASTNode, ASTNode]:
        if self.lexeme.lex in (Lex.KEYWORD_INT, Lex.KEYWORD_FLOAT, Lex.KEYWORD_BOOL):
            node = self.__description_parser()
            return node, node
        else:
            return self.__operator_parser()

    def __program_parser(self) -> ASTNode:
        self.__skip_lex(Lex.SEPARATOR_LEFT_FIGURE_BRACKET)

        h_head, h_tail = self.__description_or_operator_parser()

        t_head, t_tail = self.__description_or_operator_seq_parser()
        if t_head is not None:
            h_tail.next_node = t_head

        self.__skip_lex(Lex.SEPARATOR_RIGHT_FIGURE_BRACKET)
        self.__skip_lex(Lex.EOF)

        return h_head
