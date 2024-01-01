//
// Created by joe on 31.12.23.
//

#include "reader.h"

#define DEBUG

#ifdef DEBUG

#include "iomanip"

#define PRINT(value) std::cout << std::left << std::setw(5) << i << std::setw(15) << value << std::endl
#define PRIN(value) std::cout << std::left << std::setw(5) << i << std::setw(15) << value << std::setw(15)
#define OUTL(value) std::cout << value << std::endl
#define NEXT() \
stream.read((char*) &cmd, 2); \
i++;

#endif

void dis(const std::string& filename)
{
    // Дизассемблер
    std::fstream stream;
    stream.open(filename);
    if (!stream.is_open() || !stream.good())
    {
        std::cout << "Ошибка, файл не может быть открыт" << std::endl;
        return;
    }
    INT_VALUE buffer_int;
    double buffer_double;
    bool buffer_bool;

    stream.read((char*) &var_count, 4);
    stream.read((char*) &const_count, 4);
    stream.read((char*) &command_count, 4);

    std::cout << "Var count: " << var_count << std::endl;
    std::cout << "Const count: " << const_count << std::endl;
    std::cout << "Command count: " << command_count << std::endl;

    const_memory = new LeoObjectBase *[const_count];

    std::cout << "Consts" << std::endl;

    for (int i = 0; i < const_count; i++)
    {
        unsigned char const_type;
        stream.read((char*) &const_type, 1);

        switch (const_type)
        {
            case 0:
                stream.read((char*) &buffer_int, sizeof(INT_VALUE));
                std::cout << "Int " << buffer_int << std::endl;
                const_memory[i] = LeoInt_FromInt(buffer_int);
                break;
            case 1:
                stream.read((char*) &buffer_double, 8);
                std::cout << "Float " << buffer_double << std::endl;
                const_memory[i] = LeoFloat_FromDouble(buffer_double);
                break;
            case 2:
                stream.read((char*) &buffer_bool, 1);
                std::cout << "Bool " << buffer_bool << std::endl;
                const_memory[i] = LeoBool_FromBool(buffer_bool);
                break;
            default:
                std::cout << "Ошибка, неопределённый тип константы" << std::endl;
                delete [] const_memory;
                return;
        }
    }

    for (int i = 0; i < command_count; i++)
    {
        command cmd;
        stream.read((char*) &cmd, 2);

#ifdef DEBUG
        switch (cmd) {
            case 1:
                PRINT("ADD");
                break;
            case 2:
                PRINT("SUB");
                break;
            case 3:
                PRINT("MUL");
                break;
            case 4:
                PRINT("DIV");
                break;
            case 5:
                PRINT("IDIV");
                break;
            case 6:
                PRINT("MOD");
                break;
            case 7:
                PRINT("NOT");
                break;
            case 8:
                PRINT("OR");
                break;
            case 9:
                PRINT("AND");
                break;
            case 10:
                PRINT("LT");
                break;
            case 11:
                PRINT("LTE");
                break;
            case 12:
                PRINT("GT");
                break;
            case 13:
                PRINT("GTE");
                break;
            case 14:
                PRINT("EQ");
                break;
            case 15:
                PRINT("NEQ");
                break;
            case 16:
                PRIN("JIT");
                NEXT()
                OUTL(cmd);
                break;
            case 17:
                PRIN("JIF");
                NEXT()
                OUTL(cmd);
                break;
            case 18:
                PRIN("GOTO");
                NEXT()
                OUTL(cmd);
                break;
            case 19:
                PRIN("INPUT");
                NEXT()
                OUTL(cmd);
                break;
            case 20:
                PRINT("OUTPUT");
                break;
            case 21:
                PRIN("LOAD");
                NEXT()
                OUTL("Var " + std::to_string(cmd));
                break;
            case 22:
                PRIN("LOAD_CONST");
                NEXT()
                const_memory[cmd]->type_obj->as_io->output(const_memory[cmd]);
                break;
            case 23:
                PRIN("STORE");
                NEXT()
                OUTL("Var " + std::to_string(cmd));
                break;
            case 24:
                PRINT("DUP");
                break;
            case 25:
                PRINT("STOP");
                break;
        }
#endif
    }
    stream.close();
    return;
}

int read_file(const std::string &filename, command*& command_memory, LeoObjectBase**& const_memory, LeoObjectBase**& var_memory,
               unsigned long &const_count, unsigned long &command_count, unsigned long &var_count)
{
    /*
     * Функция чтения программы
     * */
    std::fstream stream;
    stream.open(filename);
    if (!stream.is_open())
    {
        std::cout << "File could not be opened" << std::endl;
        return 1;
    }
    INT_VALUE buffer_int;
    double buffer_double;
    bool buffer_bool;

    stream.read((char*) &var_count, 4);
    stream.read((char*) &const_count, 4);
    stream.read((char*) &command_count, 4);

    const_memory = new LeoObjectBase *[const_count];
    command_memory = new command[command_count];
    var_memory = new LeoObjectBase *[var_count];

    for (int i = 0; i < var_count; i++)
    {
        var_memory[i] = nullptr; // инициализация для корректной работы Leo_XDECREF
    }

    for (int i = 0; i < const_count; i++)
    {
        unsigned char const_type;
        stream.read((char*) &const_type, 1);

        switch (const_type)
        {
            case 0:
                stream.read((char*) &buffer_int, sizeof(INT_VALUE));
                const_memory[i] = LeoInt_FromInt(buffer_int);
                break;
            case 1:
                stream.read((char*) &buffer_double, 8);
                const_memory[i] = LeoFloat_FromDouble(buffer_double);
                break;
            case 2:
                stream.read((char*) &buffer_bool, 1);
                const_memory[i] = LeoBool_FromBool(buffer_bool);
                break;
            default:
                i--;
                for (int j = 0; j < i; j++)
                {
                    delete const_memory[j];
                }
                delete [] const_memory;
                delete [] var_memory;
                delete [] command_memory;
                return 2;
        }
    }

    for (int i = 0; i < command_count; i++)
    {
        command cmd;
        stream.read((char*) &cmd, 2);
        command_memory[i] = cmd;
    }
    stream.close();
    return 0;
}