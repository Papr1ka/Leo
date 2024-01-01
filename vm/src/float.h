//
// Created by joe on 30.12.23.
//

#ifndef LEOVM_FLOAT_H
#define LEOVM_FLOAT_H

#include "types.h"

// Получение значения из объекта для типа Float
#define FloatValue_From_Object(object) ((LeoFloat*) object)->value

struct LeoFloat
{
    LeoObject_Head
    double value;
};

// Функция создания объекта из значения
LeoObjectBase* LeoFloat_FromDouble(double value);

extern LeoTypeObject LeoFloatType;

#endif //LEOVM_FLOAT_H
