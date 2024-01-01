//
// Created by joe on 30.12.23.
//

#include "float.h"
#include "bool.h"

static LeoObjectBase* float_add(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoFloat_FromDouble(
            FloatValue_From_Object(a) + FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_sub(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoFloat_FromDouble(
            FloatValue_From_Object(a) - FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_mul(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoFloat_FromDouble(
            FloatValue_From_Object(a) * FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_div(LeoObjectBase* a, LeoObjectBase* b)
{
    double tmp = FloatValue_From_Object(b);

    if (tmp == 0)
    {
        Leo_SetError(Err::ZIRO_DIVISION, "Деление на 0")
        return nullptr;
    }

    return LeoFloat_FromDouble(
            FloatValue_From_Object(a) / FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_lt(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) < FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_lte(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) <= FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_gt(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) > FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_gte(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) >= FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_eq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) == FloatValue_From_Object(b)
    );
}

static LeoObjectBase* float_neq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            FloatValue_From_Object(a) != FloatValue_From_Object(b)
    );
}


static LeoObjectBase* float_unresolved(LeoObjectBase* a, LeoObjectBase* b)
{
    Leo_SetError(Err::UNRESOLVED_OPERATION, "Бинарная операция для float не определена")
    return nullptr;
}

static LeoObjectBase* float_unresolved_unary(LeoObjectBase* a)
{
    Leo_SetError(Err::UNRESOLVED_OPERATION, "Унарная операция для float не определена")
    return nullptr;
}

static LeoNumberMethods float_as_number = {
    float_add,
    float_sub,
    float_mul,
    float_div,
    float_unresolved,
    float_unresolved,
    float_unresolved,
    float_unresolved,
    float_unresolved_unary,
    float_lt,
    float_lte,
    float_gt,
    float_gte,
    float_eq,
    float_neq,
};

static LeoObjectBase* float_input()
{
    double value;
    std::cin >> value;
    return LeoFloat_FromDouble(value);
}

static void float_output(LeoObjectBase* object)
{
    std::cout << ((LeoFloat*) object)->value << std::endl;
}

static LeoIOMethods float_as_io = {
    float_input,
    float_output,
};

static void float_dealloc(LeoObjectBase* object)
{
    delete ((LeoFloat*) object);
}

LeoTypeObject LeoFloatType = {
    float_dealloc,
    &float_as_number,
    &float_as_io,
};

LeoObjectBase* LeoFloat_FromDouble(double value)
{
    LeoFloat* object = new LeoFloat();
    object->value = value;
    SetLeoObjectType((LeoObjectBase* )object, &LeoFloatType);
    Leo_INCREF(((LeoObjectBase*) object))
    return (LeoObjectBase*) object;
}
