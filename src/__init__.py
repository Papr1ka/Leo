__version__ = "0.1.0"


from src.cpp_translator import translate as cpp_translate
from src.interpreter import run as old_run
from src.lexer import Lexer
from src.parser import Parser
from src.python_translator import translate as py_translate
from src.text_driver import get_filename, setup_source
from src.tree import optimize_tree
from src.codegen import compile_vm
from src.writer import write_program
