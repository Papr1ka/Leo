//
// Created by joe on 30.12.23.
//

#ifndef LEOVM_INT_H
#define LEOVM_INT_H

/*
 * Тип Int
 * */

#include "types.h"

// Получение значения из объекта для типа Int
#define IntValue_From_Object(object) ((LeoInt*) object)->value

// размерность типа int
#define INT_VALUE long long

struct LeoInt
{
    LeoObject_Head
    INT_VALUE value;
};

// Функция создания объекта из значения
LeoObjectBase* LeoInt_FromInt(INT_VALUE);

extern LeoTypeObject LeoIntType;

#endif //LEOVM_INT_H
