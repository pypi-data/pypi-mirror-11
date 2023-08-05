#include "../src/SillyCrossbow.h"

#include <limits>
#include <iostream>

using namespace std;

std::string SillyCrossbow() {
    return R"(Silly Crossbow is Cpp + SWIG + distutils + crop transparent image borders library for Python.
The goal to make library for the crop rectangle clear edges in the image, 
and learn how to create a library on the C++/CMake/SWIG and use python.

SillCrossbow - это C++/SWIG/Python библиотека для нахождения прямоугольника обрезки
прозрачных краёв на изображении)";
}

CropTransparent::CropTransparent() {
}

CropTransparent::CropTransparent(int width, int height, int threshold, const std::vector<char>& buffer,
    bool createCropImage) {
    size_t x1 = numeric_limits<size_t>::max();
    size_t y1 = numeric_limits<size_t>::max();

    size_t x2 = numeric_limits<size_t>::min();
    size_t y2 = numeric_limits<size_t>::min();

    RGBA* p = reinterpret_cast<RGBA*>(const_cast<char*>(buffer.data()));

    for (size_t y = 0; y < height; ++y) {
        for (size_t x = 0; x < width; ++x, ++p) {
            if (p->a > threshold && x1 > x)
                x1 = x;

            if (p->a > threshold && y1 > y)
                y1 = y;

            if (p->a > threshold && x > x2)
                x2 = x;

            if (p->a > threshold && y > y2)
                y2 = y;
        }
    }

    _rect.x = x1;
    _rect.y = y1;

    _rect.width = (x2 + 1) - x1;
    _rect.height = (y2 + 1) - y1;
}

CropTransparent::CropTransparent(int width, int height, int threshold, const char* data, bool createCropImage) :
    CropTransparent(width, height, threshold, { data, data + width * height * 4 }, createCropImage) {
}

CropTransparent::CropTransparent(int width, int height, int threshold, void* data, bool createCropImage) :
    CropTransparent(width, height, threshold,
        { static_cast<char*>(data), static_cast<char*>(data) + width * height * 4 }, createCropImage) {
}

CropTransparent::~CropTransparent() {
}

int CropTransparent::getCroppedWidth() const {
    return _rect.width;
}

int CropTransparent::getCroppedHeight() const {
    return _rect.height;
}

int CropTransparent::getCroppedOffsetX() const {
    return _rect.x;
}

int CropTransparent::getCroppedOffsetY() const {
    return _rect.y;
}

CropRect CropTransparent::getRect() const {
    return _rect;
}
