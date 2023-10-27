from typing import TypeVar
from src.states import States, SEPARATORS, BASE_SEPARATORS

state_handler = TypeVar("state_handler")

"""
Далее описаны генераторы, обрабатывающие отдельные состояния
state_{состояние}_handler

состояние может быть простым, например identificator, start и тд.,
так и сложным - state_letter_e_handler, имеющим свои подсостояния
беспокоиться за это не нужно, внутренние состояния меняются самостоятельно

Правила:
    если обработчик вернул States.START, значит закончен разбор соответствующей лексемы
    (если обработчик состояния IDENTIFICATOR, то лексема IDENTIFICATOR)
    
    если обработчик вернул состояние {STATE}END, значит закончен разбор лексемы {STATE}
    
    иначе обработчик возвращает новое состояние, которое может быть и таким же
    
    
    состояния используются через оболочку renewable класса HandlerFactory,
    метод get_handler которого сам оборачивает в renewable обработчик
    этот обработчик позволяет каждый раз, когда генератор заканчивает свою работу
    (возвращает состояние, отличное от того, которое он обрабатывает) подменять его на новый,
    чтобы состояние сложных генераторов всегда было начальным
    
    Отдельно см. класс HandlerFactory
"""

def state_start_handler():
    state = 0
    while True:
        char: str = yield

        if state == 0:
            if char.isalpha():
                yield States.IDENTIFIER
            elif char in ("0", "1"):
                yield States.NUMBER_BIN
            elif char in ("2", "3", "4", "5", "6", "7"):
                yield States.NUMBER_OCT
            elif char in ("8", "9"):
                yield States.NUMBER_DEC
            elif char == ".":
                yield States.FRACTIONAL
            elif char in BASE_SEPARATORS:
                yield States.START
            elif char in ("(", ")", "+", "-", "*", "/", "{", "}", ";"):
                if char == "(":
                    state = States.SEPARATOR_LEFT_BRACKET, States.START
                elif char == ")":
                    state = States.SEPARATOR_RIGHT_BRACKET, States.START
                elif char == "+":
                    state = States.SEPARATOR_PLUS, States.START
                elif char == "-":
                    state = States.SEPARATOR_MINUS, States.START
                elif char == "*":
                    state = States.SEPARATOR_MULTIPLICATION, States.START
                elif char == "/":
                    state = States.SEPARATOR_DIVISION, States.START
                elif char == "{":
                    state = States.SEPARATOR_LEFT_FIGURE_BRACKET, States.START
                elif char == "}":
                    state = States.SEPARATOR_RIGHT_FIGURE_BRACKET, States.START
                elif char == ";":
                    state = States.SEPARATOR_SEMICOLON, States.START
                yield States.START
            elif char == "!":
                yield States.SEPARATOR_NOT
            else:
                yield States.ER
        else:
            yield state

def state_identificator_handler():
    while True:
        char: str = yield

        if char.isalpha() or char.isdigit():
            yield States.IDENTIFIER
        elif char in SEPARATORS:
            yield States.IDENTIFIER, States.START
        else:
            yield States.ER

def state_delim_handler():
    """
    Разделители
    в первый такт мы уже знаем, что следующий разделитель разделитель, и устанавливаем, что это за разделитель
    во второй такт, мы отдаём его
    """
    state = States.START
    while True:
        char: str = yield
        if state == States.START:
            if char == "(":
                state = States.SEPARATOR_LEFT_BRACKET, States.START
            elif char == ")":
                state = States.SEPARATOR_RIGHT_BRACKET, States.START
            elif char == "+":
                state = States.SEPARATOR_PLUS, States.START
            elif char == "-":
                state = States.SEPARATOR_MINUS, States.START
            elif char == "*":
                state = States.SEPARATOR_MULTIPLICATION, States.START
            elif char == "/":
                state = States.SEPARATOR_DIVISION, States.START
            elif char == "{":
                state = States.SEPARATOR_LEFT_FIGURE_BRACKET, States.START
            elif char == "}":
                state = States.SEPARATOR_RIGHT_FIGURE_BRACKET, States.START
            elif char == ";":
                state = States.SEPARATOR_SEMICOLON, States.START
            yield States.DELIM
        else:
            yield state

def state_separator_not_handler():
    state = 0
    """
    state = 0 - получаем символ ! (нам перенаправил его START)
    state = 1 - либо = (!=), либо другой символ (!)
    state = 2 - точно другой символ, отправляем (!=)
    """
    while True:
        char: str = yield
        if state == 0:
            if char == "=":
                state = 1
                yield States.SEPARATOR_NOT
            else:
                yield States.SEPARATOR_NOT, States.START
        else:
            yield States.SEPARATOR_NOT_EQUALS, States.START



def state_number_bin_handler():
    while True:
        char: str = yield

        if char in ("0", "1"):
            yield States.NUMBER_BIN
        elif char in ("2", "3", "4", "5", "6", "7"):
            yield States.NUMBER_OCT
        elif char in ("8", "9"):
            yield States.NUMBER_DEC
        elif char in ("e", "E"):
            yield States.LETTER_E
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("b", "B"):
            yield States.LETTER_B
        elif char in ("o", "O"):
            yield States.LETTER_O
        elif char in ("d", "D"):
            yield States.LETTER_D
        elif char in SEPARATORS:
            yield States.NUMBER_DEC, States.START
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        elif char in ("h", "H"):
            yield States.LETTER_H
        else:
            yield States.ER

def state_letter_b_handler():
    while True:
        char: str = yield

        if char in SEPARATORS:
            yield States.NUMBER_BIN, States.START
        elif char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        elif char in ("h", "H"):
            yield States.LETTER_H
        else:
            yield States.ER

def state_letter_d_hander():
    while True:
        char: str = yield

        if char in SEPARATORS:
            yield States.NUMBER_DEC, States.START
        elif char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        elif char in ("h", "H"):
            yield States.LETTER_H
        else:
            yield States.ER

def state_letter_e_hander():
    #10E0H
    #10E10
    #10E+10
    #10EH
    """
    state = 0 - не можем определить, что будет в итоге
    state = 1 - формируется либо 16-ричное число, либо порядок числа
    state = 2 - порядок числа
    """

    state = 0

    while True:
        char: str = yield

        if state == 0:
            if char in ("+", "-"):
                yield States.LETTER_E
                state = 2
            elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
                yield States.NUMBER_HEX
            elif char in ("h", "H"):
                yield States.LETTER_H
            elif char.isdigit():
                yield States.LETTER_E
                state = 1
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.LETTER_E
            elif char in ("h", "H"):
                yield States.LETTER_H
            elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
                yield States.NUMBER_HEX
            elif char in SEPARATORS:
                # check this
                yield States.FRACTIONAL, States.START
            else:
                yield States.ER
        elif state == 2:
            if char.isdigit():
                yield States.LETTER_E
            elif char in SEPARATORS:
                # and this
                yield States.FRACTIONAL, States.START

def state_letter_h_handler():
    while True:
        char: str = yield
        if char in SEPARATORS:
            yield States.NUMBER_HEX, States.START
        else:
            yield States.ER

def state_letter_o_handler():
    while True:
        char: str = yield
        if char in SEPARATORS:
            yield States.NUMBER_OCT, States.START
        else:
            yield States.ER

def state_number_oct_handler():
    while True:
        char: str = yield

        if char in ("0", "1", "2", "3", "4", "5", "6", "7"):
            yield States.NUMBER_OCT
        elif char in ("8", "9"):
            yield States.NUMBER_DEC
        elif char in ("e", "E"):
            yield States.LETTER_E
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("o", "O"):
            yield States.LETTER_O
        elif char in ("d", "D"):
            yield States.LETTER_D
        elif char in SEPARATORS:
            yield States.NUMBER_DEC, States.START
        elif char in ("h", "H"):
            yield States.LETTER_H
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        else:
            yield States.ER
def state_number_dec_handler():
    while True:
        char: str = yield

        if char.isdigit():
            yield States.NUMBER_DEC
        elif char in ("e", "E"):
            yield States.LETTER_E
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("d", "D"):
            yield States.LETTER_D
        elif char in ("h", "H"):
            yield States.LETTER_H
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        elif char in SEPARATORS:
            yield States.NUMBER_DEC, States.START
        else:
            yield States.ER

def state_number_hex_handler():
    while True:
        char: str = yield

        if char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBER_HEX
        elif char in ("h", "H"):
            yield States.LETTER_H
        else:
            yield States.ER

def state_fractional_handler():
    state = 0
    """
    state = 0 - пока не пуступила ни 1-на цифра
    state = 1 - поступила как минимум 1-на цифра
    """
    while True:
        char: str = yield

        if state == 0:
            if char.isdigit():
                yield States.FRACTIONAL
                state = 1
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.FRACTIONAL
            elif char in ("e", "E"):
                yield States.NUMBER_ORDER
            elif char in SEPARATORS:
                yield States.FRACTIONAL, States.START
            else:
                yield States.ER

def state_number_order_handler():
    state = 0
    while True:
        char: str = yield
        if state == 0:
            if char in ("+", "-"):
                yield States.NUMBER_ORDER
                state = 1
            elif char.isdigit():
                yield States.NUMBER_ORDER
                state = 2
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.NUMBER_ORDER
                state = 2
            else:
                yield States.ER
        elif state == 2:
            if char.isdigit():
                yield States.NUMBER_ORDER
            elif char in SEPARATORS:
                # check this
                yield States.FRACTIONAL, States.START
            else:
                yield States.ER


def state_er_handler():
    while True:
        char: str = yield
        if char in SEPARATORS:
            yield States.ER, States.START
        else:
            yield States.ER



HANDLERS = {
    States.START: state_start_handler,
    States.IDENTIFIER: state_identificator_handler,
    States.NUMBER_BIN: state_number_bin_handler,
    States.NUMBER_OCT: state_number_oct_handler,
    States.NUMBER_DEC: state_number_dec_handler,
    States.NUMBER_HEX: state_number_hex_handler,
    States.FRACTIONAL: state_fractional_handler,
    States.NUMBER_ORDER: state_number_order_handler,
    States.LETTER_B: state_letter_b_handler,
    States.LETTER_D: state_letter_d_hander,
    States.LETTER_E: state_letter_e_hander,
    States.LETTER_H: state_letter_h_handler,
    States.LETTER_O: state_letter_o_handler,
    States.DELIM: state_delim_handler,
    States.SEPARATOR_NOT: state_separator_not_handler,
    States.ER: state_er_handler,
}


class HandlerFactory:
    """
    Класс фабрика,
    позволяет получать нужный обработчик без необходимости его обновления
    """

    # кэшированные генераторы
    cache: dict

    def __init__(self):
        self.cache = {}

    def get_handler(self, state: States):
        """
        Метод возвращает генератор из кэша или возвращает созданный, обернув его в оболочку renewable
        в зависимости от состояния
        """
        from_cache = self.cache.get(state, None)
        if (from_cache is not None):
            return from_cache
        handler = self.init_handler(state)
        self.cache[state] = handler
        return handler

    def init_handler(self, state):
        """
        Метод инициализирует генератор-обработчик состояния, оборачивает его в renewable,
        инициализирует renewable и возвращает его
        """
        global HANDLERS
        handler = HANDLERS.get(state)()
        handler.send(None)
        handler = self.renewable(state, handler)
        handler.send(None)
        return handler

    def renewable(self, state: States, activated_generator: state_handler):
        """
        Генератор-делегатор,
        следит за тем, когда подгенератор activated_generator возвращает состояния, соответствующие концу работы генератора
        и кладёт в кэш новый инициализированный объект генератор, чтобы сбросить внутренние состояния для следующих лексем
        """
        def wrapper(*args, **kwargs):
            new_state = None
            while True:
                data = yield new_state
                new_state = activated_generator.send(data)
                if new_state != state:
                    self.cache[state] = self.init_handler(state)
                next(activated_generator)

        return wrapper()
