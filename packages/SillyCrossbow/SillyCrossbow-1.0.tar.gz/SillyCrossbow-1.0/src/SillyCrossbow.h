#ifndef SILLY_CROSSBOW_H_
#define SILLY_CROSSBOW_H_

#include <string>
#include <vector>

std::string SillyCrossbow();

struct CropRect {
    int x, y, width, height;
};

class CropTransparent {
public:
    CropTransparent();
    CropTransparent(int width, int height, int threshold, const std::vector<char>& buffer);
    CropTransparent(int width, int height, int threshold, const char* data);
    CropTransparent(int width, int height, int threshold, void* data);
    virtual ~CropTransparent();

    int getCroppedHeight() const;
    int getCroppedWidth() const;
    int getCroppedOffsetX() const;
    int getCroppedOffsetY() const;
    CropRect getRect() const;

private:
    void cropTransparent(int width, int height, int threshold, const std::vector<char>& buffer);

    CropRect _rect;
};

#endif
