from src.states import States, SEPARATORS, BASE_SEPARATORS, SEPARATORS_STATES
from src.handlers import HandlerFactory

"""
Приблизительная оценка:

Обработчики разделителей работают по следующему принципу
каждый такой обработчик кушает свой первый символ и следующий символ
[] - identifier handler
 [ ] - not_equals handler
   [ ] - identifier handler
a!=b\n

каждый раз, когда лексема распознаётся (распознаётся символ, не подходящей лексеме
(например number!) - здесь '!' - не подходит под понятие идентификатор, обработчик посмотрел '!' и выдал новое состояние - Start
в этот момент вызвался метод unget, чтобы на следующем проходе в цикле обработчик start работал над тем,
что не забрал прошлый обработчик (identifier_handler). И так каждый раз, когда распознаётся лексема

Для разделителей обработка ещё дольше
Таким образом, символ ! может присутствовать аж 3 такта
i!=2
когда обработчик identifier_handler (i в данном случае) получил '!', это первый такт, он выдал состояние Start
когда обработчик start_handler получил '!', это второй такт, он выдал состояние SEPARATOR_NOT
когда обработчик separator_not_handler получил '!' это третий такт, выдаст состояние SEPARATOR_NOT
далее обработчик separator_not_handler получит символ '=', выдаст
"""

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
        self.unget_char()
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
            lex: States = States.START
            # генератор, который будет заниматься разбором следующего символа, выбирается в зависимости от состояния
            handler = self.factory.get_handler(self.state)

            # новое состояние, в которое нам следует перейти
            new_state = handler.send(char)

            if isinstance(new_state, tuple):
                lex, new_state = new_state

            if lex != States.START:
                yield self.give_lex(lex)

            # if self.state == States.START and char not in BASE_SEPARATORS:
            #     self.unget_char()

            #
            # if char not in BASE_SEPARATORS:
            #     # аккумуляция символьного значения лексемы
            #     # if new_state != States.START and new_state.value >= 0:
            #     if ((char not in SEPARATORS and self.state not in SEPARATORS_STATES) or (
            #         char in SEPARATORS and self.state in SEPARATORS_STATES) or (
            #         self.state in (States.LETTER_E, States.NUMBER_ORDER, States.ER)) or (
            #         new_state == States.ER)):
            #         self.buffer += char

                # if char not in SEPARATORS or self.state in SEPARATORS_STATES:
                #     self.buffer += char
                # if self.state in SEPARATORS_STATES and char not in SEPARATORS:
                #     self.buffer = self.buffer[:-1]

            # отлавливаем успешные распознавания
            # if self.state == States.START:
            #     if new_state in SEPARATORS_STATES:
            #         self.unget_char()
            #         self.buffer = ""
            #
            # elif self.state == States.DELIM:
            #     if new_state == States.SEPARATOR_LEFT_BRACKET_END:
            #         yield self.give_lex(States.SEPARATOR_LEFT_BRACKET)
            #     elif new_state == States.SEPARATOR_RIGHT_BRACKET_END:
            #         yield self.give_lex(States.SEPARATOR_RIGHT_BRACKET)
            #     elif new_state == States.SEPARATOR_PLUS_END:
            #         yield self.give_lex(States.SEPARATOR_PLUS)
            #     elif new_state == States.SEPARATOR_MINUS_END:
            #         yield self.give_lex(States.SEPARATOR_MINUS)
            #     elif new_state == States.SEPARATOR_MULTIPLICATION_END:
            #         yield self.give_lex(States.SEPARATOR_MULTIPLICATION)
            #     elif new_state == States.SEPARATOR_DIVISION_END:
            #         yield self.give_lex(States.SEPARATOR_DIVISION)
            #     elif new_state == States.SEPARATOR_LEFT_FIGURE_BRACKET_END:
            #         yield self.give_lex(States.SEPARATOR_LEFT_FIGURE_BRACKET)
            #     elif new_state == States.SEPARATOR_RIGHT_FIGURE_BRACKET_END:
            #         yield self.give_lex(States.SEPARATOR_RIGHT_FIGURE_BRACKET)
            #     elif new_state == States.SEPARATOR_SEMICOLON_END:
            #         yield States.SEPARATOR_SEMICOLON
            #
            # elif self.state == States.IDENTIFIER:
            #     if new_state == States.START:
            #         yield self.give_lex(States.IDENTIFIER)
            #
            # elif self.state == States.SEPARATOR_NOT:
            #     if new_state == States.START:
            #         yield self.give_lex(States.SEPARATOR_NOT)
            #     elif new_state == States.SEPARATOR_NOT_EQUALS_END:
            #         yield self.give_lex(States.SEPARATOR_NOT_EQUALS)
            #
            # elif self.state == States.NUMBER_BIN:
            #     if new_state == States.START:
            #         yield self.give_lex(States.NUMBER_BIN)
            #     elif new_state == States.NUMBER_DEC_END:
            #         yield self.give_lex(States.NUMBER_DEC)
            #
            # elif self.state == States.NUMBER_OCT:
            #     if new_state == States.START:
            #         yield self.give_lex(States.NUMBER_OCT)
            #     elif new_state == States.NUMBER_DEC_END:
            #         yield self.give_lex(States.NUMBER_DEC)
            #
            # elif self.state == States.NUMBER_DEC:
            #     if new_state == States.START:
            #         yield self.give_lex(States.NUMBER_DEC)
            #
            # elif self.state == States.NUMBER_HEX:
            #     if new_state == States.START:
            #         yield self.give_lex(States.NUMBER_HEX)
            #
            # elif self.state == States.LETTER_B:
            #     if new_state == States.NUMBER_BIN_END:
            #         yield self.give_lex(States.NUMBER_BIN)
            #
            # elif self.state == States.LETTER_D:
            #     if new_state == States.NUMBER_DEC_END:
            #         yield self.give_lex(States.NUMBER_DEC)
            #
            # elif self.state == States.LETTER_E:
            #     if new_state == States.NUMBER_ORDER_END:
            #         yield self.give_lex(States.FRACTIONAL)
            #
            # elif self.state == States.LETTER_H:
            #     if new_state == States.NUMBER_HEX_END:
            #         yield self.give_lex(States.NUMBER_HEX)
            #
            # elif self.state == States.LETTER_O:
            #     if new_state == States.NUMBER_OCT_END:
            #         yield self.give_lex(States.NUMBER_OCT)
            #
            # elif self.state == States.FRACTIONAL:
            #     if new_state == States.START:
            #         yield self.give_lex(States.FRACTIONAL)
            #
            # elif self.state == States.NUMBER_ORDER:
            #     if new_state == States.START:
            #         yield self.give_lex(States.FRACTIONAL)
            #
            # elif self.state == States.ER:
            #     if new_state == States.START:
            #         yield self.give_lex(States.ER)

            if char not in BASE_SEPARATORS:
                self.buffer += char

            if lex != States.START:
                # Если следующее состояние стартовое, или соответствует завершению определённой лексемы,

                self.symbol += len(self.buffer)
                self.buffer = ""

            self.state = new_state

            if char in BASE_SEPARATORS:
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
