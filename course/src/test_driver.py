_source = ""
_lines = []
_is_set = False


def read_file(filename: str) -> str:
    global _lines
    with open(filename) as file:
        _lines = file.readlines()
    stream = "".join(_lines) + "\n"
    return stream


def read_string(string: str):
    global _lines
    _lines = string.split("\n")
    return string + "\n"


def highlight(line: int, symbol: int):
    print(_lines[line - 1], end="")
    for i in range(symbol - 1):
        print(" ", end="")
    print("^")


def setup_source(filename_or_source: str):
    global _source, _is_set
    if filename_or_source.endswith(".leo"):
        _source = read_file(filename_or_source)
    else:
        _source = read_string(filename_or_source)
    _is_set = True


def get_source() -> str:
    if not _is_set:
        raise NotImplementedError("Не вызван setup_source")
    return _source
