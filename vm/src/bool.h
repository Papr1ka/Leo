//
// Created by joe on 30.12.23.
//

#ifndef LEOVM_BOOL_H
#define LEOVM_BOOL_H

#include "types.h"
#include "vm.h"

// Получение значения из объекта для типа Float
#define BoolValue_From_Object(object) ((LeoBool*) object)->value

struct LeoBool
{
    LeoObject_Head
    bool value;
};

// Функция создания объекта из значения
LeoObjectBase* LeoBool_FromBool(bool value);

extern LeoTypeObject LeoBoolType;

#endif //LEOVM_BOOL_H
