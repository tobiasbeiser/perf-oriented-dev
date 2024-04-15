cmake_minimum_required(VERSION 3.11)
project(perf_prog_npb_bt)

set_property(GLOBAL PROPERTY C_STANDARD 11)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 11)

add_compile_options(-DTRACY_ENABLE=1 -DTRACY_NO_EXIT=1)

include_directories(tracy)
set(tracy_src tracy/TracyClient.cpp)


if(MSVC)
  add_compile_options(/W4)
else()
  add_compile_options(-Wall -Wextra -Wno-unknown-pragmas -Wno-unused-parameter)
endif()

file(GLOB_RECURSE SOURCE_FILES CONFIGURE_DEPENDS src/*.c src/*.h)

include_directories(${TRACY_INCLUDE_DIR})

link_libraries(m)



add_executable(npb_bt_w ${SOURCE_FILES})
target_include_directories(npb_bt_w PRIVATE src/w)

add_executable(npb_bt_s ${SOURCE_FILES})
target_include_directories(npb_bt_s PRIVATE src/s)

add_executable(npb_bt_a ${SOURCE_FILES})
target_include_directories(npb_bt_a PRIVATE src/a)

add_executable(npb_bt_b ${SOURCE_FILES})
target_include_directories(npb_bt_b PRIVATE src/b)

add_executable(npb_bt_c ${SOURCE_FILES})
target_include_directories(npb_bt_c PRIVATE src/c)
