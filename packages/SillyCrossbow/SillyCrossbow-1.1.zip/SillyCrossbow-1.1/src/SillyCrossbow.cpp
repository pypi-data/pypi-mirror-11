#include "../src/SillyCrossbow.h"

#include <limits>
#include <iostream>

using namespace std;

Image::Image(int width, int height) :
    _width(width), _height(height)/*, _buffer() */{
    _buffer.resize(_width * _height);
}

Image::~Image() {
}

int Image::getWidth() {
    return _width;
}

int Image::getHeight() {
    return _height;
}

const char* Image::getData() {
    return reinterpret_cast<const char*>(_buffer.data());
}

void* Image::getDataVoid() {
    return static_cast<void*>(_buffer.data());
}

std::string SillyCrossbow() {
    return R"(Silly Crossbow is Cpp + SWIG + distutils + crop transparent image borders library for Python.
The goal to make library for the crop rectangle clear edges in the image, 
and learn how to create a library on the C++/CMake/SWIG and use python.

SillCrossbow - это C++/SWIG/Python библиотека для нахождения прямоугольника обрезки
прозрачных краёв на изображении)";
}

CropTransparent::CropTransparent() {
}

CropTransparent::CropTransparent(int width, int height, int threshold, const std::vector<char>& buffer, bool createCropImage) {
    size_t x1 = numeric_limits<size_t>::max();
    size_t y1 = numeric_limits<size_t>::max();

    size_t x2 = numeric_limits<size_t>::min();
    size_t y2 = numeric_limits<size_t>::min();

    RGBA* p = reinterpret_cast<RGBA*>(const_cast<char*>(buffer.data()));

    for (size_t y = 0; y < height; ++y)
        for (size_t x = 0; x < width; ++x, ++p) {
            if (p->a > threshold && x1 > x)
                x1 = x;

            if (p->a > threshold && y1 > y)
                y1 = y;

            if (p->a > threshold && x > x2)
                x2 = x;

            if (p->a > threshold && y > y2)
                y2 = y;

            if (!p->r)
                p->r = 1;
            if (!p->g)
                p->g = 1;
            if (!p->b)
                p->b = 1;
            if (!p->a)
                p->a = 1;
        }

    _rect.x = x1;
    _rect.y = y1;

    _rect.width = (x2 + 1) - x1;
    _rect.height = (y2 + 1) - y1;

    if (createCropImage) {
        _croppedImage = Image { _rect.width, _rect.height };

        RGBA* dst = reinterpret_cast<RGBA*>(const_cast<char*>(_croppedImage.getData()));
        RGBA* src = reinterpret_cast<RGBA*>(const_cast<char*>(buffer.data()));

        auto test =  static_cast<RGBA*>(_croppedImage.getDataVoid());

/*
        for (size_t i = 0; i < _croppedImage.getWidth() * _croppedImage.getHeight(); ++i, ++test, ++src) {
//            *test = {src->r ? src->r : 1, src->g ? src->g : 1, src->b ? src->b : 1, src->a ? src->a : 1};
            *test = {100, 100, 100, 200};
        }
*/
        for (size_t i = 0; i < 100; ++i, ++test) {
//            *test = {src->r ? src->r : 1, src->g ? src->g : 1, src->b ? src->b : 1, src->a ? src->a : 1};
            *test = {100, 200, 100, 200};
        }
        for (size_t i = 100; i < 200; ++i, ++test) {
//            *test = {src->r ? src->r : 1, src->g ? src->g : 1, src->b ? src->b : 1, src->a ? src->a : 1};
            *test = {200, 100, 100, 200};
        }

//        for (size_t y = y1; y < y2; ++y) {
//            for (size_t x = x1; x < x2; ++x, ++dst) {
//
//                RGBA p = src[y * width + x];
//
//                dst->r = 100; // p.r ? p.r : 1;
//                dst->g = 200; // p.g ? p.g : 1;
//                dst->b = 100; // p.b ? p.b : 1;
//                dst->a = 200; // p.a ? p.a : 1;
//            }
//        }
    }
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

Image CropTransparent::getCroppedImage() const {
    return _croppedImage;
}

void CropTransparent::fillWithImage(unsigned long data) {
    cout << sizeof(data) << endl;

    RGBA* dst = reinterpret_cast<RGBA*>(data);
    RGBA* src = reinterpret_cast<RGBA*>(const_cast<char*>(_croppedImage.getData()));

    for (size_t i = 0; i < _croppedImage.getWidth() * _croppedImage.getHeight(); ++i, ++dst, ++src) {
//            *test = {src->r ? src->r : 1, src->g ? src->g : 1, src->b ? src->b : 1, src->a ? src->a : 1};
//        *test = {100, 100, 100, 200};
        *dst = *src;
    }
}
