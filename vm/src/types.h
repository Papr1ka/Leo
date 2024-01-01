//
// Created by joe on 30.12.23.
//

#ifndef LEOVM_TYPES_H
#define LEOVM_TYPES_H

#define LeoObject_Head LeoObjectBase base; // заголовок объекта, должен присутствовать во всех объектах

typedef struct object_base LeoObjectBase; // базовый тип объекта


// декремент количества ссылок на объект, объект должен существовать, если ссылок нет, то объект удаляется
#define Leo_DECREF(object) \
{                          \
    object->ref_count--; \
    if (object->ref_count == 0) \
    {\
        object->type_obj->dealloc(object); \
    }                      \
}

// инкремент количества ссылок на объект
#define Leo_INCREF(object) \
{                          \
    object->ref_count++;    \
}

// как Leo_DECREF, только допустимо, что объект равен nullptr
#define Leo_XDECREF(object) \
{                           \
    if (object != nullptr)  \
    { \
       object->ref_count--; \
        if (object->ref_count == 0) \
        {\
            object->type_obj->dealloc(object); \
        }  \
    }\
}

#include "stdint.h"
#include "iostream"

typedef LeoObjectBase* (*binaryfunc) (LeoObjectBase*, LeoObjectBase*);

typedef LeoObjectBase* (*unaryfunc) (LeoObjectBase*);

typedef LeoObjectBase* (*procedure) ();

typedef void (*voidfunc) (LeoObjectBase*);

typedef voidfunc destructor;


// протокол взаимодействия с объектом для арифметических и логических операциях
typedef struct {
    // арифметические
    binaryfunc add; // сложение
    binaryfunc sub; // вычитание
    binaryfunc mul; // умножение
    binaryfunc div; // деление
    binaryfunc idiv; // целочисленное деление
    binaryfunc mod; // остаток от деления

    // логические
    binaryfunc _or; // или
    binaryfunc _and; // и
    unaryfunc _not; // не
    binaryfunc lt; // <
    binaryfunc lte; // <=
    binaryfunc gt; // >
    binaryfunc gte; // >=
    binaryfunc eq; // ==
    binaryfunc neq; // !=
} LeoNumberMethods;

// протокол взаимодействия с объектом для операций ввода и вывода
typedef struct {
    // арифметические
    procedure input; // ввод объекта
    voidfunc output; // вывод объекта
} LeoIOMethods;

// объект типа языка Leo
typedef struct typeobject {
    destructor dealloc; // метод удаления объекта
    LeoNumberMethods* as_number; // протокол взаимодействия арифметических и логических операций
    LeoIOMethods* as_io; // протокол взаимодействия ввода и вывода
} LeoTypeObject;

struct object_base
{
    int32_t ref_count; // количество ссылок на объект, если 0, то он удаляется
    LeoTypeObject* type_obj; // указатель на объект типа, указателей на объект типа много, сам объект типа один
};

static inline void SetLeoObjectType(LeoObjectBase* object, LeoTypeObject* type)
{
    // установить поле объекта типа
    object->type_obj = type;
}

#endif //LEOVM_TYPES_H
