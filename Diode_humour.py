from PIL import Image, ImageDraw
import math

w = 300 // 1
h = 200 // 1
size = w * h

img = Image.new('RGB', (w * 1, h * 1), "white")

pixels = img.load()
W = img.size[0]
H = img.size[1]
print('size: (%d, %d)' % (W, H))

draw = ImageDraw.Draw(img)
#draw.ellipse(((10, 10), (W - 10, H - 10)), outline='gray')
#draw.line((0, 0,   100, 0,     100, 100,    0, 100,   0, 0), fill='gray', width=2)

draw.line((100, 50,    200, 100,    100, 150,   100, 50 ), fill='green', width=3)

draw.line((0, H // 2,  W, H // 2), fill='green', width=3)
draw.line((200, 50,  200, 150), fill='green', width=3)

xp = 0
yp = H // 2

for i in range(W):
    x = 30 * i / W * math.pi
    a = (H - i) // 2
    if i > 200: 
        a = 0
    if i < 100: 
        a = 50
    y = H // 2 + a  * math.sin(x)
    draw.line((xp, yp,  i, y), fill='red')
    xp = i
    yp = y
img.save("How_diode_works_%d_%d.png" % (w, h))
