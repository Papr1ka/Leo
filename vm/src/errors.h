//
// Created by joe on 01.01.24.
//

#ifndef LEOVM_ERRORS_H
#define LEOVM_ERRORS_H

enum Err
{
    SUCCESS = 0, // ошибок нет
    ZIRO_DIVISION, // деление на 0
    UNRESOLVED_OPERATION, // реализация опкода не определена типом ({type}_unresolved метод)
    UNRESOLVED_OPCODE, // неопределённый опкод
};

#endif //LEOVM_ERRORS_H
