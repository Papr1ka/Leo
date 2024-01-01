//
// Created by joe on 30.12.23.
//

#include "int.h"
#include "bool.h"

static LeoObjectBase* int_add(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoInt_FromInt(
            IntValue_From_Object(a) + IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_sub(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoInt_FromInt(
            IntValue_From_Object(a) - IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_mul(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoInt_FromInt(
            IntValue_From_Object(a) * IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_idiv(LeoObjectBase* a, LeoObjectBase* b)
{
    INT_VALUE tmp = IntValue_From_Object(b);

    if (tmp == 0)
    {
        Leo_SetError(Err::ZIRO_DIVISION, "Деление на 0")
        return nullptr;
    }
    return LeoInt_FromInt(
            IntValue_From_Object(a) / IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_mod(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoInt_FromInt(
            IntValue_From_Object(a) % IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_lt(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) < IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_lte(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) <= IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_gt(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) > IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_gte(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) >= IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_eq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) == IntValue_From_Object(b)
    );
}

static LeoObjectBase* int_neq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            IntValue_From_Object(a) != IntValue_From_Object(b)
    );
}


static LeoObjectBase* int_unresolved(LeoObjectBase* a, LeoObjectBase* b)
{
    Leo_SetError(Err::UNRESOLVED_OPERATION, "Бинарная операция для int не определена")
    return nullptr;
}

static LeoObjectBase* int_unresolved_unary(LeoObjectBase* a)
{
    Leo_SetError(Err::UNRESOLVED_OPERATION, "Унарная операция для int не определена")
    return nullptr;
}

static LeoNumberMethods int_as_number = {
        int_add,
        int_sub,
        int_mul,
        int_unresolved,
        int_idiv,
        int_mod,
        int_unresolved,
        int_unresolved,
        int_unresolved_unary,
        int_lt,
        int_lte,
        int_gt,
        int_gte,
        int_eq,
        int_neq,
};

LeoObjectBase* int_input()
{
    INT_VALUE value;
    std::cin >> value;
    return LeoInt_FromInt(value);
}

void int_output(LeoObjectBase* object)
{
    std::cout << ((LeoInt*) object)->value << std::endl;
}

LeoIOMethods int_as_io = {
        int_input,
        int_output,
};

static void int_dealloc(LeoObjectBase* object)
{
    delete ((LeoInt*) object);
}

LeoTypeObject LeoIntType = {
        int_dealloc,
        &int_as_number,
        &int_as_io,
};

LeoObjectBase* LeoInt_FromInt(INT_VALUE value)
{
    LeoInt* object = new LeoInt();
    object->value = value;
    SetLeoObjectType((LeoObjectBase* )object, &LeoIntType);
    Leo_INCREF(((LeoObjectBase*) object))
    return (LeoObjectBase*) object;
}
