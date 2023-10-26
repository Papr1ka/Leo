from src.states import States, SEPARATORS
from src.handlers import HandlerFactory


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

    # буфер для лексемы
    buffer: str

    # номер разбираемой строки
    line: int

    # номер начального символа разбираемой лексемы
    symbol: int

    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.state = States.START
        self.factory = HandlerFactory()
        self.buffer = ""
        self.line = 1
        self.symbol = 0

    def get_char(self):
        """
        Метод возвращает следующий символ строки
        Если символов не осталось, выбрасывается StopIteration
        """
        if self.index >= len(self.source):
            raise StopIteration
        char = self.source[self.index]
        self.index += 1
        return char

    def unget_char(self):
        """
        Метод декрементирует указатель на символ строки
        """
        if self.index > 0:
            self.index -= 1

    def give_lex(self, state: States):
        """
        Метод возвращает кортеж из всех известных параметрах о лексеме
        Все возвращаемые анализатором лексемы проходят через эту функцию
        """
        return state, self.buffer, self.line, self.symbol

    def get_lex(self):
        """
        Генератор
        Возвращает очередную лексему через вызов give_lex
        """
        while True:
            try:
                char = self.get_char()
            except StopIteration:
                return

            if char not in SEPARATORS:
                # аккумуляция символьного значения лексемы
                self.buffer += char

            # генератор, который будет заниматься разбором следующего символа, выбирается в зависимости от состояния
            handler = self.factory.get_handler(self.state)

            # новое состояние, в которое нам следует перейти
            new_state = handler.send(char)

            # отлавливаем успешные распознавания
            if self.state == States.START:
                pass

            elif self.state == States.IDENTIFICATOR:
                if new_state == States.START:
                    yield self.give_lex(States.IDENTIFICATOR)

            elif self.state == States.NUMBERBIN:
                if new_state == States.START:
                    yield self.give_lex(States.NUMBERBIN)
                elif new_state == States.NUMBERDECEND:
                    yield self.give_lex(States.NUMBERDEC)

            elif self.state == States.NUMBEROCT:
                if new_state == States.START:
                    yield self.give_lex(States.NUMBEROCT)
                elif new_state == States.NUMBERDECEND:
                    yield self.give_lex(States.NUMBERDEC)

            elif self.state == States.NUMBERDEC:
                if new_state == States.START:
                    yield self.give_lex(States.NUMBERDEC)

            elif self.state == States.NUMBERHEX:
                if new_state == States.START:
                    yield self.give_lex(States.NUMBERHEX)

            elif self.state == States.LETTERB:
                if new_state == States.NUMBERBINEND:
                    yield self.give_lex(States.NUMBERBIN)

            elif self.state == States.LETTERD:
                if new_state == States.NUMBERDECEND:
                    yield self.give_lex(States.NUMBERDEC)

            elif self.state == States.LETTERE:
                if new_state == States.NUMBERORDEREND:
                    yield self.give_lex(States.FRACTIONAL)

            elif self.state == States.LETTERH:
                if new_state == States.NUMBERHEXEND:
                    yield self.give_lex(States.NUMBERHEX)

            elif self.state == States.LETTERO:
                if new_state == States.NUMBEROCTEND:
                    yield self.give_lex(States.NUMBEROCT)

            elif self.state == States.FRACTIONAL:
                if new_state == States.START:
                    yield self.give_lex(States.FRACTIONAL)

            elif self.state == States.NUMBERORDER:
                if new_state == States.START:
                    yield self.give_lex(States.FRACTIONAL)

            elif self.state == States.ER:
                if new_state == States.START:
                    yield self.give_lex(States.ER)


            if new_state == States.START or new_state.value < 0:
                # Если следующее состояние стартовое, или соответствует завершению определённой лексемы,
                if self.state != States.START:
                    # self.unget_char()
                    pass

                self.symbol += len(self.buffer)

                self.state = States.START
                self.buffer = ""
            else:
                # Если состояние промежуточное (лексема полностью не распознана)
                self.state = new_state

            if char in SEPARATORS:
                if char == "\n":
                    self.line += 1
                    self.symbol = 0
                else:
                    self.symbol += 1

                if new_state == States.ER:
                    """
                    Особый случай, отлавливает собития вида
                    '123c\n' - в конце состояние будет NUMBERHEX, следующее - ER
                    при этом ER не успеет отработать, \n будет проглочено обработчиком NUMBERHEX
                    на месте NUMBERHEX может быть другое состояние
                    поэтому мы явно возвращаем ошибочную лексему и очищаем буфер для разбора новой строки
                    также позволяет разделять лексемы
                    чтобы строка
                    '123e 10\n' была распознана как ошибочная лексема и лексема десятичного числа
                    """
                    self.symbol += len(self.buffer)
                    yield self.give_lex(States.ER)
                    self.buffer = ""
                    self.state = States.START
