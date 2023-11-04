from abc import ABC, abstractmethod
from typing import List

from src.constants import Lex
from syntax_parser import SyntaxParser


class BaseParser(ABC):
    analyzer: SyntaxParser

    def __init__(self, analyzer: SyntaxParser):
        self.analyzer = analyzer

    @abstractmethod
    def parse(self) -> bool:
        pass


class LexParser(BaseParser):
    lex: Lex

    def __init__(self, analyzer: SyntaxParser, lex: Lex):
        super().__init__(analyzer)
        self.lex = lex

    def parse(self) -> bool:
        return self.analyzer.get_lex().lex == self.lex


class ChoiceParser(BaseParser):
    parsers: List[BaseParser]

    def __init__(self, analyzer: SyntaxParser, parsers: List[BaseParser]):
        super().__init__(analyzer)
        self.parsers = parsers

    def parse(self) -> bool:
        for parser in self.parsers:
            if parser.parse():
                return True
        return False


class ManyParser(BaseParser):
    parser: BaseParser

    def __init__(self, analyzer: SyntaxParser, parser: BaseParser):
        super().__init__(analyzer)
        self.parser = parser

    def parse(self) -> bool:
        while self.parser.parse():
            pass
        return True


class TypeParser(BaseParser):

    def parse(self) -> bool:
        pass

        return ChoiceParser(
            self.analyzer,
            [
                LexParser(self.analyzer, Lex.KEYWORD_INT),
                LexParser(self.analyzer, Lex.KEYWORD_FLOAT),
                LexParser(self.analyzer, Lex.KEYWORD_BOOL)
            ]
        ).parse()
