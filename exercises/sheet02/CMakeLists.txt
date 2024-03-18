cmake_minimum_required(VERSION 3.10)
project(perf_oriented_prog_sheet02)

set_property(GLOBAL PROPERTY C_STANDARD 11)

if(MSVC)
  add_compile_options(/W4 /WX)
else()
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

add_executable(io_loadgen io_loadgen.c)
