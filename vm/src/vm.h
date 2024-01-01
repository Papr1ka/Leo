//
// Created by joe on 30.12.23.
//

#ifndef LEOVM_VM_H
#define LEOVM_VM_H

#include "commands.h"
#include "types.h"
#include "int.h"
#include "float.h"
#include "bool.h"
#include "errors.h"
#include "cstdint"


/*
 * Тип команды, хранит опкод или аргумент для операции
 * Выделено 2 байта для возможности адресации 2^16 переменных, констант и номера строки для инструкций перехода
 * Если программа будет занимать более 2^16 строк кода, то необходимо будет выделить больше байт
 * */
typedef uint16_t command;

#include "reader.h"

extern uint16_t memory_size; // максимальное количество операндов в стеке
extern command* command_memory; // память команд, здесь хранится программа
extern LeoObjectBase** stack_memory; // стек
extern LeoObjectBase** const_memory; // память констант
extern LeoObjectBase** var_memory; // память переменных
extern unsigned long var_count; // размер массива var_memory
extern unsigned long const_count; // размер массива const_count
extern unsigned long command_count; // размер массива command_memory
extern unsigned long PC; // виртуальный регистр-указатель на адрес инструкции в command_memory


// установка кода и сообщения ошибки
#define Leo_SetError(e_code, e_message) \
{                                           \
    err_code = e_code;                    \
    err_message = e_message;\
}

// true, если произошла RunTime ошибка
#define Leo_ErrorOccured() (err_code != Err::SUCCESS)

// Проверка, произошла ли ошибка, если да, то переход к месту её обработки
#define ASSERT_NO_ERROR() \
if (Leo_ErrorOccured()) \
{ \
    goto error_occured; \
}

extern unsigned char err_code; // код ошибки (если произошла)
extern std::string err_message; // сообщение об ошибке

// виртуальный регистр-указатель стека, указывает на элемент,
// находящийся над вершиной стека (первая свободная ячейка)
extern unsigned long SP;

extern command IR; // виртуальный регистр команды

#define TOP() (stack_memory[SP - 1]) // Верхний элемент стека

// Получение и удаление из стека верхнего элемента
#define POP() (stack_memory[--SP])

// Добавить элемент на вершину стека
#define PUSH(value) (stack_memory[SP++] = value)

// Установить вершину стека
#define SET_TOP(value) (stack_memory[SP - 1] = value)

void Vm_init();

void Vm_dealloc();

int Vm_read(const std::string &filename);

void run();



#endif //LEOVM_VM_H
