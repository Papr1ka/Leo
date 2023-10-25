from src.states import States, SEPARATORS
from src.handlers import HandlerFactory
from typing import Dict, Tuple
from collections.abc import Generator


class Lexer():
    # строка для разбора
    source: str
    # текущий номер символа
    index: int
    # текущее состояние
    state: States
    # класс, возвращающий нам обёртку нужного генератора в зависимости от состояния,
    # следит за тем, чтобы после состояний START и ER генератор был пересоздан
    factory: HandlerFactory

    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.state = States.START
        self.factory = HandlerFactory()

    def getChar(self):
        """
        Метод возвращает следующий символ строки
        Если символов не осталось, выбрасывается StopIteration
        """
        if self.index >= len(self.source):
            raise StopIteration
        char = self.source[self.index]
        self.index += 1
        return char

    def ungetChar(self):
        if self.index > 0:
            self.index -= 1

    def getLex(self):
        # буфер для лексемы
        buffer: str = ""

        while True:
            try:
                char = self.getChar()
            except StopIteration:
                return

            if char not in SEPARATORS:
                buffer += char

            handler = self.factory.get_handler(self.state)

            new_state = handler.send(char)

            if self.state == States.START:
                pass

            elif self.state == States.IDENTIFICATOR:
                if new_state == States.START:
                    yield States.IDENTIFICATOR, buffer
                    buffer = ""

            elif self.state == States.NUMBERBIN:
                if new_state == States.START:
                    yield States.NUMBERBIN, buffer
                    buffer = ""
                elif new_state == States.NUMBEROCTEND:
                    yield States.NUMBEROCT, buffer
                    buffer = ""
                elif new_state == States.NUMBERDECEND:
                    yield States.NUMBERDEC, buffer
                    buffer = ""
                elif new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.NUMBEROCT:
                if new_state == States.START:
                    yield States.NUMBEROCT, buffer
                    buffer = ""
                elif new_state == States.NUMBERDECEND:
                    yield States.NUMBERDEC, buffer
                    buffer = ""
                elif new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.NUMBERDEC:
                if new_state == States.START:
                    yield States.NUMBERDEC, buffer
                    buffer = ""
                elif new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.NUMBERHEX:
                if new_state == States.START:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.LETTERB:
                if new_state == States.NUMBERBINEND:
                    yield States.NUMBERBIN, buffer
                    buffer = ""
                elif new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.LETTERD:
                if new_state == States.NUMBERDECEND:
                    yield States.NUMBERDEC, buffer
                    buffer = ""
                elif new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""

            elif self.state == States.LETTERE:
                if new_state == States.NUMBERHEXEND:
                    yield States.NUMBERHEX, buffer
                    buffer = ""
                elif new_state == States.NUMBERORDEREND:
                    yield States.FRACTIONAL, buffer
                    buffer = ""

            elif self.state == States.ER:
                if new_state == States.START:
                    yield States.ER, buffer
                    buffer = ""

            elif self.state == States.FRACTIONAL:
                if new_state == States.START:
                    yield States.FRACTIONAL, buffer
                    buffer = ""

            elif self.state == States.NUMBERORDER:
                if new_state == States.START:
                    yield States.FRACTIONAL, buffer
                    buffer = ""

            if (new_state.value < 0):
                self.state = States.START
            else:
                self.state = new_state
