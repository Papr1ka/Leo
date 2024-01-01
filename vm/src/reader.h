//
// Created by joe on 31.12.23.
//

#ifndef LEOVM_READER_H
#define LEOVM_READER_H

#include "fstream"
#include "string"
#include "vm.h"

int read_file(const std::string &filename, command*& command_memory, LeoObjectBase**& const_memory, LeoObjectBase**& var_memory,
               unsigned long &const_count, unsigned long &command_count, unsigned long &var_count);

void dis(const std::string& filename);

#endif //LEOVM_READER_H
