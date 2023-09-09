from typing import Iterator, List


class ReversePolish:
    #приоритеты арифметических операций, чем больше, тем выше
    _PRIORITIES: dict = {
        **{symbol: 3 for symbol in ["*", "/"]},
        **{symbol: 2 for symbol in ["+", "-"]},
        **{symbol: 1 for symbol in ["(", ")"]},
    }
    #список токенов арифметических операций
    _OPERATIONS: list = list(_PRIORITIES.keys())

class ReversePolishConverter(ReversePolish):
    """
    Конвертер арифметических выражений в обратную польскую запись
    """
    def stringToTokens(self, expression: str) -> Iterator:
        """
        Возвращает итератор, в котором каждый элемент - это токен переданного арифметического выражения вида "1+2*(8-3)"
        Токенами Являются: Знаки операций, числа и буквенные идентификаторы (x, y, ...)
        """
        last = ""
        for letter in expression:
            if letter in self._OPERATIONS:
                if last != "":
                    yield last
                    last = ""
                yield letter
            elif letter != " ":
                last += letter
        if last != "":
            yield last
    
    def convert(self, expression: str) -> List[str]:
        """
        Преобразует строковое арифметическое выражение в обратную польскую запись, возвращает список токенов
        """
        #выходной список токенов
        result = []
        #стэк для токенов
        buffer = []
        for token in self.stringToTokens(expression):
            if token not in self._OPERATIONS:
                result.append(token)
            else:
                if token == "(":
                    buffer.append(token)
                elif token == ")":
                    while buffer[-1] != "(":
                        result.append(buffer[-1])
                        buffer.pop(-1)
                    buffer.pop(-1)
                else:
                    while buffer and self._PRIORITIES[token] <= self._PRIORITIES[buffer[-1]]:
                        result.append(buffer[-1])
                        buffer.pop(-1)
                    buffer.append(token)
        result += buffer[::-1]
        return result

class ReversePolishCounter(ReversePolish):
    def calculate(self, listOfToneks: List[str]) -> int:
        buffer = []
        for token in listOfToneks:
            if token not in self._OPERATIONS:
                buffer.append(token)
            else:
                buffer[-2] = eval(f"{buffer[-2]} {token} {buffer[-1]}")
                buffer.pop(-1)
        return buffer[0]

if __name__ == "__main__":
    converter = ReversePolishConverter()
    counter = ReversePolishCounter()

    expression = input("Выражение: ")

    r = converter.convert(expression)
    print("Вид в обратной польской записи:", " ".join(r))
    print("Значение: ", counter.calculate(r))
