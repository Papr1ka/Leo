from typing import Iterator, List, Union
from sstack import Stack

#приоритеты арифметических операций, чем больше, тем выше
PRIORITIES = {
    **{symbol: 3 for symbol in ["*", "/"]},
    **{symbol: 2 for symbol in ["+", "-"]},
    **{symbol: 1 for symbol in ["(", ")"]},
}
#список токенов арифметических операций
OPERATIONS = list(PRIORITIES.keys())

def stringToTokens(expression: str) -> Iterator[str]:
    """
    Возвращает итератор, в котором каждый элемент - это токен переданного арифметического выражения вида "1+2*(8-3)"
    Токенами Являются: Знаки операций, числа и буквенные идентификаторы (x, y, ...)
    """
    last = ""
    for letter in expression:
        if letter in OPERATIONS:
            if last != "":
                yield last
                last = ""
            yield letter
        elif letter != " ":
            last += letter
    if last != "":
        yield last

class ReversePolishConverter():
    """
    Конвертер арифметических выражений в обратную польскую запись.
    Работает только с заведомо правильными выражениями!
    """

    def convert(self, expression: str) -> List[str]:
        """
        Преобразует строковое арифметическое выражение в обратную польскую запись, возвращает список токенов
        """
        #выходной список токенов
        result = []
        #стек для токенов
        buffer = Stack()

        for token in stringToTokens(expression):
            if token not in OPERATIONS:
                result.append(token)
            else:
                if token == "(":
                    buffer.push(token)
                elif token == ")":
                    while buffer[-1] != "(":
                        result.append(buffer.peek())
                        buffer.pop()
                    buffer.pop()
                else:
                    while buffer and PRIORITIES[token] <= PRIORITIES[buffer.peek()]:
                        result.append(buffer.peek())
                        buffer.pop()
                    buffer.push(token)

        buff = []
        while (len(buffer) > 0):
            buff.append(buffer.pop())
        
        result += buff[::-1]
        return result

class ReversePolishCounter():
    """
    Вычислитель выражений в обратной польской записи.
    Работает только с заведомо правильными выражениями!
    """

    def calculate(self, reverseExpression: Union[List[str], str]) -> int:
        if isinstance(reverseExpression, str):
            reverseExpression = reverseExpression.split(" ")
        buffer = Stack()
        for token in reverseExpression:
            if token not in OPERATIONS:
                buffer.push(token)
            else:
                last1 = buffer.pop()
                last2 = buffer.pop()
                buffer.push(eval(f"{last2} {token} {last1}"))
        return buffer.pop()


if __name__ == "__main__":
    converter = ReversePolishConverter()
    counter = ReversePolishCounter()

    expression = input("Выражение: ")
    r = converter.convert(expression)

    print("Вид в обратной польской записи:", " ".join(r))
    print("Значение: ", counter.calculate(r))

    print("Тест:", counter.calculate("6 9 + 5 - 8 1 2 * + / 7 +"))
