cmake_minimum_required(VERSION 3.26)
project(leovm)

set(CMAKE_CXX_STANDARD 17)

add_executable(src/main.cpp
        src/vm.h
        src/vm.cpp
        src/commands.h
        src/types.h
        src/float.h
        src/float.cpp
        src/bool.h
        src/bool.cpp
        src/int.h
        src/int.cpp
        src/reader.cpp
        src/reader.h
        src/errors.h
)
