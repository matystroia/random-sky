import random
from PIL import Image
import stripes


WIDTH = 1920
HEIGHT = 1080

image = Image.new('RGB', (WIDTH, HEIGHT))
pixels = image.load()
height = random.randrange(HEIGHT//2)
land_colors = [stripes.gen_color_palette(26, range(55, 205), (55, 205), (55, 205)) for _ in range(3)]
sky_colors = stripes.gen_color_palette(10, (55,), (55,), range(55, 125))
resolution = 1 / 60
heights = []

for k in range(3):
    heights.append([])
    for __ in range(int(WIDTH * resolution) + 1):
        heights[k].append(height)
        height += random.randint(-50, 50)

dist = int(1/resolution)
i = -1

coefficients = []
for k in range(3):
    coefficients.append({})
    for p0, p1, p2, p3 in zip([heights[k][0]] + heights[k], heights[k], heights[k][1:], heights[k][2:] + [heights[k][-1]]):
        coefficients[k][(p1, p2)] = (-1/2*p0+3/2*p1-3/2*p2+1/2*p3,
                                     p0-5/2*p1+2*p2-1/2*p3,
                                     -1/2*p0+1/2*p2,
                                     p1)

for col in range(WIDTH):
    '''
    if col % dist == 0:
        i += 1
        h = heights[i]
    '''
    i = col // dist
    t = (col % dist) / (dist - 1)
    # h = t * heights[i+1] + (1-t) * heights[i]

    co = [coefficients[k][(heights[k][i], heights[k][i+1])] for k in range(3)]
    h = [c[0]*(t**3) + c[1]*(t**2) + c[2]*t + c[3] for c in co]

    # h = int(heights[i] + (col % dist) * ((heights[i+1] - heights[i]) / dist))
    h = [max(0, min(int(_h), HEIGHT)) for _h in h]

    for row in range(0, h[0]):
        pixels[col, row] = sky_colors[(col + row) // ((WIDTH + HEIGHT) // 10)]

    for i, (a, b) in enumerate(zip(h, h[1:] + [HEIGHT])):
        for row in range(a, b):
            pixels[col, row] = land_colors[i][(row)//((HEIGHT)//25)]

image.save('sky.png')
