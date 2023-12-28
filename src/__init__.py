__version__ = "0.0.1"


from src.cpp_translator import translate as cpp_translate
from src.interpreter import run as old_run
from src.lexer import Lexer
from src.parser import Parser
from src.python_translator import translate as py_translate
from src.text_driver import get_filename, setup_source
from src.tree import optimize_tree
from src.codegen import compile_vm
from src.leovm import run, __vm_version__
