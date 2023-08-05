cmake_minimum_required(VERSION 3.0)

set(NAME SillyCrossbow)

if(MINGW)
else()
    add_definitions(-fPIC)
endif()

add_library(${NAME}
    SillyCrossbow.cpp
)

find_package(SWIG)
include(${SWIG_USE_FILE})

find_package(PythonLibs 2.7 REQUIRED)
include_directories(
    ${PYTHON_INCLUDE_PATH} 
    .
)

set(CMAKE_SWIG_FLAGS "-c++")

set(INTERFACE_NAME "${NAME}.i")

set_source_files_properties(${INTERFACE_NAME} PROPERTIES CPLUSPLUS ON)
set_source_files_properties(${INTERFACE_NAME} PROPERTIES SWIG_FLAGS "")

SWIG_ADD_MODULE(${NAME} python ${INTERFACE_NAME})
SWIG_LINK_LIBRARIES(${NAME} ${NAME} ${PYTHON_LIBRARIES})
