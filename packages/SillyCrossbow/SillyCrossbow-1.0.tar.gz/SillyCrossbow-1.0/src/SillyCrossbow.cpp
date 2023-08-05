#include "../src/SillyCrossbow.h"

#include <limits>
#include <iostream>

using namespace std;

struct RGBA {
    uint8_t r, g, b, a;
};

std::string SillyCrossbow() {
    return "Silly Crossbow is SWIG + distutils + crop transparent image borders example";
}

CropTransparent::CropTransparent() {
}

CropTransparent::CropTransparent(int width, int height, int threshold, const std::vector<char>& buffer) {
    cropTransparent(width, height, threshold, buffer);
}

CropTransparent::CropTransparent(int width, int height, int threshold, const char* data) {
    cropTransparent(width, height, threshold, { data, data + width * height * 4 });
}

CropTransparent::CropTransparent(int width, int height, int threshold, void* data) {
    cropTransparent(width, height, threshold,
        { static_cast<char*>(data), static_cast<char*>(data) + width * height * 4 });
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

void CropTransparent::cropTransparent(int width, int height, int threshold, const std::vector<char>& buffer) {

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

CropRect CropTransparent::getRect() const {
    return _rect;
}
