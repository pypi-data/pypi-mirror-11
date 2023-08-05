#ifndef SILLY_CROSSBOW_H_
#define SILLY_CROSSBOW_H_

#include <string>
#include <vector>

std::string SillyCrossbow();

struct RGBA {
    uint8_t r, g, b, a;
};

struct CropRect {
    int x, y, width, height;
};

class CropTransparent {
public:
    CropTransparent();
    CropTransparent(int width, int height, int threshold, const std::vector<char>& buffer, bool createCropImage = false);
    CropTransparent(int width, int height, int threshold, const char* data, bool createCropImage = false);
    CropTransparent(int width, int height, int threshold, void* data, bool createCropImage = false);
    virtual ~CropTransparent();

    int getCroppedHeight() const;
    int getCroppedWidth() const;
    int getCroppedOffsetX() const;
    int getCroppedOffsetY() const;

    CropRect getRect() const;

private:
    CropRect _rect;
};

#endif
