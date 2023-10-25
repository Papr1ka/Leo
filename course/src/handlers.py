# from src.states import States
from typing import TypeVar
from src.states import States

state_handler = TypeVar("state_handler")

SEPARATORS = (
    " ",
    "\n",
    "\t"
)

def state_start_handler():
    while True:
        char: str = yield

        if char.isalpha():
            yield States.IDENTIFICATOR
        elif char in ("0", "1"):
            yield States.NUMBERBIN
        elif char in ("2", "3", "4", "5", "6", "7"):
            yield States.NUMBEROCT
        elif char in ("8", "9"):
            yield States.NUMBERDEC
        elif char == ".":
            yield States.FRACTIONAL
        elif char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

def state_identificator_handler():
    while True:
        char: str = yield

        if char.isalpha() or char.isdigit():
            yield States.IDENTIFICATOR
        elif char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

def state_number_bin_handler():
    while True:
        char: str = yield

        if char in ("0", "1"):
            yield States.NUMBERBIN
        elif char in ("2", "3", "4", "5", "6", "7"):
            yield States.NUMBEROCT
        elif char in ("8", "9"):
            yield States.NUMBERDEC
        elif char in ("e", "E"):
            yield States.LETTERE
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("b", "B"):
            yield States.LETTERB
        elif char in ("o", "O"):
            yield States.NUMBEROCTEND
        elif char in ("d", "D"):
            yield States.LETTERD
        elif char in SEPARATORS:
            yield States.NUMBERDECEND
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        elif char in ("h", "H"):
            yield States.NUMBERHEXEND
        else:
            yield States.ER

def state_letter_b_handler():
    while True:
        char: str = yield

        if char in SEPARATORS:
            yield States.NUMBERBINEND
        elif char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        elif char in ("h", "H"):
            yield States.NUMBERHEXEND
        else:
            yield States.ER

def state_letter_d_hander():
    while True:
        char: str = yield

        if char in SEPARATORS:
            yield States.NUMBERDECEND
        elif char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        elif char in ("h", "H"):
            yield States.NUMBERHEXEND
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
                yield States.LETTERE
                state = 2
            elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
                yield States.NUMBERHEX
            elif char in ("h", "H"):
                yield States.NUMBERHEXEND
            elif char.isdigit():
                yield States.LETTERE
                state = 1
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.LETTERE
            elif char in ("h", "H"):
                yield States.NUMBERHEXEND
            elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
                yield States.NUMBERHEX
            elif char in SEPARATORS:
                yield States.NUMBERORDEREND
            else:
                yield States.ER
        elif state == 2:
            if char.isdigit():
                yield States.LETTERE
            elif char in SEPARATORS:
                yield States.NUMBERORDEREND

def state_number_oct_handler():
    while True:
        char: str = yield

        if char in ("0", "1", "2", "3", "4", "5", "6", "7"):
            yield States.NUMBEROCT
        elif char in ("8", "9"):
            yield States.NUMBERDEC
        elif char in ("e", "E"):
            yield States.LETTERE
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("o", "O"):
            yield States.START
        elif char in ("d", "D"):
            yield States.LETTERD
        elif char in SEPARATORS:
            yield States.NUMBERDECEND
        elif char in ("h", "H"):
            yield States.NUMBERHEXEND
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        else:
            yield States.ER

def state_number_dec_handler():
    while True:
        char: str = yield

        if char.isdigit():
            yield States.NUMBERDEC
        elif char in ("e", "E"):
            yield States.LETTERE
        elif char == ".":
            yield States.FRACTIONAL
        elif char in ("d", "D"):
            yield States.LETTERD
        elif char in ("h", "H"):
            yield States.NUMBERHEXEND
        elif char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        elif char in SEPARATORS:
            yield States.START
        else:
            yield States.ER

def state_number_hex_handler():
    while True:
        char: str = yield

        if char.isdigit() or char in ("a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"):
            yield States.NUMBERHEX
        elif char in ("h", "H"):
            yield States.START
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
                yield States.NUMBERORDER
            elif char in SEPARATORS:
                yield States.START
            else:
                yield States.ER

def state_number_order_handler():
    state = 0
    while True:
        char: str = yield
        if state == 0:
            if char in ("+", "-"):
                yield States.NUMBERORDER
                state = 1
            elif char.isdigit():
                yield States.NUMBERORDER
                state = 2
            else:
                yield States.ER
        elif state == 1:
            if char.isdigit():
                yield States.NUMBERORDER
                state = 2
            else:
                yield States.ER
        elif state == 2:
            if char.isdigit():
                yield States.NUMBERORDER
            elif char in SEPARATORS:
                yield States.START
            else:
                yield States.ER


def state_er_handler():
    while True:
        char: str = yield
        if char in SEPARATORS:
            yield States.START
        else:
            yield States.ER



HANDLERS = {
    States.START: state_start_handler,
    States.IDENTIFICATOR: state_identificator_handler,
    States.NUMBERBIN: state_number_bin_handler,
    States.NUMBEROCT: state_number_oct_handler,
    States.NUMBERDEC: state_number_dec_handler,
    States.NUMBERHEX: state_number_hex_handler,
    States.FRACTIONAL: state_fractional_handler,
    States.NUMBERORDER: state_number_order_handler,
    States.LETTERB: state_letter_b_handler,
    States.LETTERD: state_letter_d_hander,
    States.LETTERE: state_letter_e_hander,
    States.ER: state_er_handler,
}


class HandlerFactory:
    cache: dict

    def __init__(self):
        self.cache = {}

    def get_handler(self, state: States):
        from_cache = self.cache.get(state, None)
        if (from_cache is not None):
            return from_cache
        handler = self.init_handler(state)
        self.cache[state] = handler
        return handler

    def init_handler(self, state):
        global HANDLERS
        handler = HANDLERS.get(state)()
        handler.send(None)
        handler = self.renewable(state, handler)
        handler.send(None)
        return handler

    def renewable(self, state: States, activated_generator: state_handler):
        def wrapper(*args, **kwargs):
            new_state = None
            while True:
                data = yield new_state
                new_state = activated_generator.send(data)
                if new_state == States.START or new_state == States.ER or new_state.value < 0:
                    self.cache[state] = self.init_handler(state)
                next(activated_generator)

        return wrapper()
