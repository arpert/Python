from PIL import Image
#import os

w = 256 // 1
h = 256 // 1
size = w * h

img = Image.new('RGB', (w * 3, h * 3), "black")

pixels = img.load()
W = img.size[0]
H = img.size[1]
print('size: (%d, %d)' % (W, H))

for i in range(W // 3):
    for j in range(H // 3):
        r = (i * 256) // w 
        g = (j * 256) // h
        b = ( (256 * i * j) // (w * h) % 256)
        pixels[i            , j] = (r, g, b)
        pixels[2 * w - j - 1, i] = (g, b, r)
        pixels[2 * w + i    , j] = (b, r, g)

        pixels[i            , 2 * h - j - 1] = (r, g, b)
        pixels[2 * w - j - 1, 2 * h - i - 1] = (g, b, r)
        pixels[2 * w + i    , 2 * h - j - 1] = (b, r, g)

        pixels[i            , 2 * h + j] = (r, g, b)
        pixels[2 * w - j - 1, 2 * h + i] = (g, b, r)
        pixels[2 * w + i    , 2 * h + j] = (b, r, g)

img.save("Image_%d_%d.png" % (w, h))
