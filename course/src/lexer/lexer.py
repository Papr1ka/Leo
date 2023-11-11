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
    _source: str

    # текущий номер символа
    _index: int

    # текущее состояние
    _state: States

    # класс, возвращающий нам обёртку нужного генератора в зависимости от состояния,
    # следит за тем, чтобы после состояний START и ER генератор был пересоздан
    _factory: HandlerFactory

    # буфер для лексемы
    _buffer: str

    # номер разбираемой строки
    _line: int

    # номер начального символа разбираемой лексемы
    _symbol: int

    # сообщение об ошибке последней нераспознанной лексемы
    _error_message: str

    def __init__(self):
        self._source = get_source()
        self._index = 0
        self._state = States.START
        self._factory = HandlerFactory()
        self._buffer = ""
        self._line = 1
        self._symbol = 1
        self._error_message = ""

    def _get_char(self):
        """
        Метод возвращает следующий символ строки
        Если символов не осталось, выбрасывается StopIteration
        """
        if self._index >= len(self._source):
            raise StopIteration
        char = self._source[self._index]
        self._index += 1
        return char

    def _unget_char(self):
        """
        Метод декрементирует указатель на символ строки
        """
        if self._index > 0:
            self._index -= 1

    def _give_lex(self, lex: Lex):
        """
        Метод возвращает кортеж из всех известных параметрах о лексеме
        Все возвращаемые анализатором лексемы проходят через эту функцию
        """
        self._unget_char()
        if lex == Lex.UNRESOLVED:
            lex_error(Lexeme(lex, self._buffer, self._line, self._symbol, self._error_message))
        return Lexeme(lex, self._buffer, self._line, self._symbol, "")

    def get_lex(self):
        """
        Генератор
        Возвращает очередную лексему через вызов give_lex
        """

        while True:
            try:
                char = self._get_char()
            except StopIteration:
                if self._state == States.SEPARATOR_COMMENT:
                    self._error_message = "Комментарий должен быть закрыт"
                    yield self._give_lex(Lex.UNRESOLVED)
                self._buffer = ""
                yield self._give_lex(Lex.EOF)
                return

            lex: Lex = None
            # генератор, который будет заниматься разбором следующего символа, выбирается в зависимости от состояния
            handler = self._factory.get_handler(self._state)

            # новое состояние, в которое нам следует перейти
            new_state = handler.send(char)

            # если получили лексему и новое состояние
            if isinstance(new_state, tuple):
                lex, new_state = new_state

            # если получили сообщение об ошибке и состояние ошибки
            if isinstance(new_state, list):
                self._error_message, new_state = new_state

            # если закончился комментарий
            if new_state == States.STATE_NULL:
                new_state = States.START
                self._buffer = ""

            # выдаём распознанную лексему
            elif lex is not None:
                if lex == Lex.IDENTIFIER:
                    keyword = KEYWORDS.get(self._buffer)
                    if keyword is None:
                        yield self._give_lex(lex)
                    else:
                        yield self._give_lex(keyword)
                else:
                    yield self._give_lex(lex)

            # накопление буфера (в случае если lex не None накопление не нужно, так лексема уже была выдана во вне)
            # если lex не None, в буфер попадёт `мусор`, который собьёт счётчик символа в строке (symbol)
            if char not in BASE_SEPARATORS and lex is None:
                self._buffer += char

            if lex is not None:
                # если была распознана лексема

                self._symbol += len(self._buffer)
                self._buffer = ""

            self._state = new_state

            # подсчёт номера линии и символа в строке
            if char in BASE_SEPARATORS:
                if lex is None:
                    if char == "\n":
                        self._line += 1
                        self._symbol = 1
                    else:
                        self._symbol += 1

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
                    self._symbol += len(self._buffer)
                    yield self._give_lex(Lex.UNRESOLVED)
                    self._buffer = ""
                    self._state = States.START


class DebugLexer(Lexer):
    """
    Нужен исключительно для тестов
    Вместо лексемы выдаёт кортеж
    Вместо вызова ошибки отдаёт неопределённую лексему
    """

    def _give_lex(self, lex: Lex):
        """
        Метод возвращает кортеж из всех известных параметрах о лексеме
        Все возвращаемые анализатором лексемы проходят через эту функцию
        """
        self._unget_char()
        if lex == Lex.UNRESOLVED:
            return lex, self._buffer, self._line, self._symbol, self._error_message
        return lex, self._buffer, self._line, self._symbol, ""
