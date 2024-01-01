//
// Created by joe on 30.12.23.
//
#include "vm.h"

uint16_t memory_size = 8192;
command* command_memory;
LeoObjectBase** stack_memory;
LeoObjectBase** const_memory;
LeoObjectBase** var_memory;
unsigned long PC;
unsigned long SP;
command IR;
unsigned long var_count;
unsigned long const_count;
unsigned long command_count;
unsigned char err_code; // код ошибки (если произошла)
std::string err_message; // сообщение об ошибке

void Vm_init()
{
    /*
     * Первичная инициализация виртуальной машины
     * */
    PC = 0;
    SP = 0;
    stack_memory = new LeoObjectBase *[memory_size];
    command_memory = nullptr;
    var_memory = nullptr;
    const_memory = nullptr;
    err_code = Err::SUCCESS;
    err_message = "";
}

int Vm_read(const std::string &filename)
{
    // Чтение программы и вторичная инициализация виртуальной машины
    return read_file(filename, command_memory, const_memory, var_memory,
              const_count, command_count, var_count);
}

void Vm_dealloc()
{
    /*
     * Освобождение памяти виртуальной машины
     * При корректном завершении работы программы,
     * в var_memory и const_memory у всех объектов ref_count должен быть равен единице,
     * следовательно Leo_DECREF приведёт к их удалению
     * */
    for (int i = 0; i < SP; i++)
    {
        if (stack_memory[i] != nullptr)
        {
            Leo_DECREF(stack_memory[i])
        }
    }
    delete [] stack_memory;
    delete [] command_memory;
    for (int i = 0; i < var_count; i++)
    {
        if (var_memory[i] != nullptr)
        {
            Leo_DECREF(var_memory[i])
        }
    }
    delete [] var_memory;
    for (int i = 0; i < const_count; i++)
    {
        if (const_memory[i] != nullptr)
        {
            Leo_DECREF(const_memory[i])
        }
    }
    delete [] const_memory;
}

void run()
{
    /*
     * Выполнение программы на виртуальной машине, предполагается, что Vm_Init и Vm_Read были вызваны ранее
     * */
    LeoObjectBase* left = nullptr; // вспомогательный виртуальный регистр 1
    LeoObjectBase* right = nullptr; // вспомогательный виртуальный регистр 2
    LeoObjectBase* result = nullptr; // вспомогательный виртуальный регистр 3
    command addr = 0; // вспомогательный виртуальный регистр 4
    bool running = true; // флаг остановки выполнения программы
    while (running)
    {
        IR = command_memory[PC]; // Instruction Fetch
        switch (IR)
        {
            // проверки на соответствие типов отсутствуют, так как выполняются компилятором
            case CMD::ADD:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->add(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::SUB:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->sub(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::MUL:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->mul(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::DIV:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->div(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::IDIV:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->idiv(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::MOD:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->mod(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::NOT:
                left = TOP();
                result = left->type_obj->as_number->_not(left);
                SET_TOP(result);
                Leo_DECREF(left)
                break;
            case CMD::OR:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->_or(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::AND:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->_and(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::LT:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->lt(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::LTE:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->lte(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::GT:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->gt(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::GTE:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->gte(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::EQ:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->eq(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::NEQ:
                right = POP();
                left = TOP();
                result = left->type_obj->as_number->neq(left, right);
                SET_TOP(result);
                Leo_DECREF(right)
                Leo_DECREF(left)
                break;
            case CMD::JIT:
                PC++;
                addr = command_memory[PC];
                left = POP();
                if (BoolValue_From_Object(left))
                {
                    PC = addr;
                    Leo_DECREF(left)
                    continue;
                }
                Leo_DECREF(left)
                break;
            case CMD::JIF:
                PC++;
                addr = command_memory[PC];
                left = POP();
                if (not BoolValue_From_Object(left))
                {
                    PC = addr;
                    Leo_DECREF(left)
                    continue;
                }
                Leo_DECREF(left)
                break;
            case CMD::GOTO:
                PC++;
                addr = command_memory[PC];
                PC = addr;
                continue;
            case CMD::INPUT:
                PC++;
                addr = command_memory[PC]; // addr равен типу переменной
                switch (addr)
                {
                    case 0:
                        left = LeoIntType.as_io->input(); // тут уже делается INCREF
                        break;
                    case 1:
                        left = LeoFloatType.as_io->input();
                        break;
                    case 2:
                        left = LeoBoolType.as_io->input();
                        break;
                    default:
                        throw 10;
                }
                PUSH(left);
                break;
            case CMD::OUTPUT:
                left = POP();
                left->type_obj->as_io->output(left);
                Leo_DECREF(left)
                break;
            case CMD::LOAD:
                PC++;
                addr = command_memory[PC];
                left = var_memory[addr];
                Leo_INCREF(left)
                PUSH(left);
                break;
            case CMD::LOAD_CONST:
                PC++;
                addr = command_memory[PC];
                left = const_memory[addr];
                Leo_INCREF(left)
                PUSH(left);
                break;
            case CMD::STORE:
                PC++;
                addr = command_memory[PC];
                left = POP();

                // Уменьшаем количество ссылок на объект, который хранился до этого момента в ячейке памяти переменных
                // Так как объекта там может и не быть, используется Leo_XDECREF
                Leo_XDECREF(var_memory[addr])

                // Удалили из стека, но записали в память переменных => DECREF + INCREF = 0 => не меняем ref_count
                var_memory[addr] = left;
                break;
            case CMD::DUP:
                left = TOP();
                Leo_INCREF(left) // осторожно, дублируется не сам объект, а лишь ссылка на него
                PUSH(left);
                break;
            case CMD::STOP:
                running = false;
                std::cout << "Program stopped" << std::endl;
                break;
            default:
                Leo_SetError(Err::UNRESOLVED_OPCODE, "Неопределённый опкод: " + std::to_string(IR))
        }
        ASSERT_NO_ERROR() // проверка на случай возникновения ошибки
        PC++;
        continue;

error_occured:
        std::cout << "RunTimeError: " + err_message << std::endl;
        std::cout << "Виртуальная машина остановлена" << std::endl;
        return;
    }
}
