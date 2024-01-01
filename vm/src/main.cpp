#include <iostream>
#include "vm.h"
#include "chrono"

#define VERSION "0.0.1"

#define HELP \
"Использование: leovm [-v] [-h] [-S] файл.leo.bin\n\n\
Виртуальная машина языка Leo (.leo) Удачи! \n\n\
Позиционные аргументы:\n\t\
файл.leo            Имя файла с байткодом программы (.leo.bin)\n\n\
Опции:\n\t\
-v, --version       Выводит версию программы \n\t\
-h, --help          Выводит это сообщение \n\t\
-S                  Дизассемблирование, без выполнения \n\t\
-t, --timeit        Выводит время выполнения программы"

int main(int argc, const char* argv[]) {
    std::string filename;
    bool dis_flag = false;
    bool timeit_flag = false;

    for (int i = 1; i < argc; i++)
    {
        std::string a = argv[i];
        if (a.compare("--help") == 0 || a.compare("-h") == 0)
        {
            std::cout << HELP << std::endl;
            return 0;
        }
        else if (a.compare("--version") == 0 || a.compare("-v") == 0)
        {
            std::cout << VERSION << std::endl;
            return 0;
        }
        else if (a.compare("--timeit") == 0 || a.compare("-t") == 0)
        {
            if (timeit_flag || dis_flag)
            {
                std::cout << "Ошибка, повторное указание флага или флаги несовместимы" << std::endl;
                return -3;
            }
            timeit_flag = true;
        }
        else if (a.compare("-S") == 0)
        {
            if (dis_flag || timeit_flag)
            {
                std::cout << "Ошибка, повторное указание флага или флаги несовместимы" << std::endl;
                return -3;
            }
            dis_flag = true;
        }
        else
        {
            if (!filename.empty())
            {
                std::cout << "Ошибка, виртуальная машина может работать только с одним файлом" << std::endl;
                return -1;
            }
            filename = a;
        }
    }

    if (filename.empty())
    {
        std::cout << "Ошибка, не указан файл" << std::endl;
        return -2;
    }

    if (dis_flag)
    {
        dis(filename);
    }
    else
    {
        Vm_init();
        int r = Vm_read(filename);

        if (r == 0)
        {
            if (timeit_flag)
            {
                auto t0 = std::chrono::steady_clock::now();
                run();
                auto t1 = std::chrono::steady_clock::now();
                auto t = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0);
                std::cout << t.count() << " миллисекунд" << std::endl;
            }
            else
            {
                run();
            }
            Vm_dealloc();
        }
    }

    return 0;
}
