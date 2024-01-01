//
// Created by joe on 30.12.23.
//

#include "bool.h"

LeoObjectBase* bool_or(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            BoolValue_From_Object(a) + BoolValue_From_Object(b)
    );
}

LeoObjectBase* bool_and(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            BoolValue_From_Object(a) + BoolValue_From_Object(b)
    );
}

LeoObjectBase* bool_not(LeoObjectBase* a)
{
    return LeoBool_FromBool(
            not BoolValue_From_Object(a)
    );
}

LeoObjectBase* bool_eq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            BoolValue_From_Object(a) == BoolValue_From_Object(b)
    );
}

LeoObjectBase* bool_neq(LeoObjectBase* a, LeoObjectBase* b)
{
    return LeoBool_FromBool(
            BoolValue_From_Object(a) != BoolValue_From_Object(b)
    );
}

LeoObjectBase* bool_unresolved(LeoObjectBase* object, LeoObjectBase*)
{
    Leo_SetError(Err::UNRESOLVED_OPERATION, "Бинарная операция для bool не определена")
    return nullptr;
}

static LeoNumberMethods bool_as_number = {
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_or,
        bool_and,
        bool_not,
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_unresolved,
        bool_eq,
        bool_neq,
};

LeoObjectBase* bool_input()
{
    bool value;
    std::cin >> value;
    return LeoBool_FromBool(value);
}

void bool_output(LeoObjectBase* object)
{
    std::cout << ((LeoBool*) object)->value << std::endl;
}

LeoIOMethods bool_as_io = {
        bool_input,
        bool_output,
};

static void bool_dealloc(LeoObjectBase* object)
{
    delete ((LeoBool*) object);
}

LeoTypeObject LeoBoolType = {
        bool_dealloc,
        &bool_as_number,
        &bool_as_io,
};

LeoObjectBase* LeoBool_FromBool(bool value)
{
    LeoBool* object = new LeoBool();
    object->value = value;
    SetLeoObjectType((LeoObjectBase* )object, &LeoBoolType);
    Leo_INCREF(((LeoObjectBase*) object))
    return (LeoObjectBase*) object;
}
