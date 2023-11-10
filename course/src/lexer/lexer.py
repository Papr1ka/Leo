from src.constants import BASE_SEPARATORS, KEYWORDS, Lex, Lexeme, States
from src.errors import lex_error
from src.lexer.handlers import HandlerFactory
from src.text_driver import get_source

"""
Приблизительная оценка:

Обработчики разделителей работают по следующему принципу
каждый такой обработчик кушает свой первый символ и следующий символ
[ - start handler
 ] - identifier handler -> lex 'a'
 [ - start handler
   ] - not_equals handler -> lex '!='
   [ - start handler
    ] - identifier handler -> lex 'b'
a!=b\n

[ - start handler
 ] - identifier handler -> lex 'a'
 [ - start handler
  ] - not equals handler -> lex '!'
  [ - start handler
   ] - identifier handler -> lex 'b'
a!b\n

на месте \n должен быть любой разделитель из SEPARATORS

Каждый раз, когда распознаётся лексема, вызывается метод unget (в методе give_lex), так как обработчик получает символ,
не подходящий под выражение лексемы, например идентификатор получил символ '!', тогда он выдаёт лексему идентификатора, 
переходное состояние START, мы в методе get_lex понимаем, что '!' уже не относится к идентификатору, поэтому и вызывается unget
чтобы новое состояние START разбирала '!', а не пропускала его

Также Start обрабатывает одиночные разделители по такому же принципу, неважно, что мы точно знаем, что после '(', ')', ';' и тд.
точно не будет ничего дельного и можно сразу отдавать лексему, в данной программе важен общий случай алгоритма для простоты кода
таким образом после '(' распознается r'.' - любой символ и мы только тогда отдадим лексему, потом произойдёт unget и так по кругу.
"""


class Lexer():
    # строка для разбора
    __source: str

    # текущий номер символа
    __index: int

    # текущее состояние
    __state: States

    # класс, возвращающий нам обёртку нужного генератора в зависимости от состояния,
    # следит за тем, чтобы после состояний START и ER генератор был пересоздан
    __factory: HandlerFactory

    # буфер для лексемы
    __buffer: str

    # номер разбираемой строки
    __line: int

    # номер начального символа разбираемой лексемы
    __symbol: int

    # сообщение об ошибке последней нераспознанной лексемы
    __error_message: str

    def __init__(self):
        self.__source = get_source()
        self.__index = 0
        self.__state = States.START
        self.__factory = HandlerFactory()
        self.__buffer = ""
        self.__line = 1
        self.__symbol = 1
        self.__error_message = ""

    def __get_char(self):
        """
        Метод возвращает следующий символ строки
        Если символов не осталось, выбрасывается StopIteration
        """
        if self.__index >= len(self.__source):
            raise StopIteration
        char = self.__source[self.__index]
        self.__index += 1
        return char

    def __unget_char(self):
        """
        Метод декрементирует указатель на символ строки
        """
        if self.__index > 0:
            self.__index -= 1

    def __give_lex(self, lex: Lex):
        """
        Метод возвращает кортеж из всех известных параметрах о лексеме
        Все возвращаемые анализатором лексемы проходят через эту функцию
        """
        self.__unget_char()
        if lex == Lex.UNRESOLVED:
            lex_error(Lexeme(lex, self.__buffer, self.__line, self.__symbol, self.__error_message))
        return Lexeme(lex, self.__buffer, self.__line, self.__symbol, "")

    def get_lex(self):
        """
        Генератор
        Возвращает очередную лексему через вызов give_lex
        """

        while True:
            try:
                char = self.__get_char()
            except StopIteration:
                if self.__state == States.SEPARATOR_COMMENT:
                    self.__error_message = "Комментарий должен быть закрыт"
                    yield self.__give_lex(Lex.UNRESOLVED)
                self.__buffer = ""
                yield self.__give_lex(Lex.EOF)
                return

            lex: Lex = None
            # генератор, который будет заниматься разбором следующего символа, выбирается в зависимости от состояния
            handler = self.__factory.get_handler(self.__state)

            # новое состояние, в которое нам следует перейти
            new_state = handler.send(char)

            # если получили лексему и новое состояние
            if isinstance(new_state, tuple):
                lex, new_state = new_state

            # если получили сообщение об ошибке и состояние ошибки
            if isinstance(new_state, list):
                self.__error_message, new_state = new_state

            # если закончился комментарий
            if new_state == States.STATE_NULL:
                new_state = States.START
                self.__buffer = ""

            # выдаём распознанную лексему
            elif lex is not None:
                if lex == Lex.IDENTIFIER:
                    keyword = KEYWORDS.get(self.__buffer)
                    if keyword is None:
                        yield self.__give_lex(lex)
                    else:
                        yield self.__give_lex(keyword)
                else:
                    yield self.__give_lex(lex)

            # накопление буфера (в случае если lex не None накопление не нужно, так лексема уже была выдана во вне)
            # если lex не None, в буфер попадёт `мусор`, который собьёт счётчик символа в строке (symbol)
            if char not in BASE_SEPARATORS and lex is None:
                self.__buffer += char

            if lex is not None:
                # если была распознана лексема

                self.__symbol += len(self.__buffer)
                self.__buffer = ""

            self.__state = new_state

            # подсчёт номера линии и символа в строке
            if char in BASE_SEPARATORS:
                if lex is None:
                    if char == "\n":
                        self.__line += 1
                        self.__symbol = 1
                    else:
                        self.__symbol += 1

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
                    self.__symbol += len(self.__buffer)
                    yield self.__give_lex(Lex.UNRESOLVED)
                    self.__buffer = ""
                    self.__state = States.START
