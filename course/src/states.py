from enum import Enum

class States(Enum):
    #Рабочие состояния
    START = 1
    IDENTIFICATOR = 2
    NUMBERBIN = 3
    NUMBEROCT = 4
    NUMBERDEC = 5
    NUMBERHEX = 6
    NUMBERORDER = 7
    FRACTIONAL = 10
    ER = 0
    LETTERB = 11
    LETTERD = 12
    LETTERE = 13


    #Состояния завершения разбора лексемы
    NUMBERBINEND = -1
    NUMBEROCTEND = -2
    NUMBERDECEND = -3
    NUMBERHEXEND = -4
    NUMBERORDEREND = -5

# Границы лексем, список пока простой (не полный)
SEPARATORS = (" ", "\n", "\t")
