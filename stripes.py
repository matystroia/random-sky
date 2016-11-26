import random
from PIL import Image

image = Image.new('RGB', (1920, 1080))
pixels = image.load()


def gen_color_palette(n, r_range, g_range, b_range):
    return [(random.choice(r_range), random.choice(g_range), random.choice(b_range)) for _ in range(n)]

# color_palette = [(random.randint(55, 255), 55, 55) for _ in range(100)]
# color_palette.sort(key=lambda x: x[0])
# print(color_palette)

'''
for i in range(1920):
    for j in range(1080):
        pixels[i, j] = color_palette[(i+j)//((1920+1080)//100)]
'''


def gen_stripes(color_palette):
    color_palette.sort(key=lambda x: x[0] / (x[0]+x[1]+x[2]))
    for i in range(1920):
        for j in range(1080):
            pixels[i, j] = color_palette[((i+j)//((1920+1080)//len(color_palette))) % len(color_palette)]


def gen_repeating_stripes(stripes, color_palette):
    for i in range(1920):
        for j in range(1080):
            pixels[i, j] = color_palette[((i-j)//((1920+1080)//stripes)) % len(color_palette)]

if __name__ == '__main__':  
    gen_repeating_stripes(50, [(243, 0, 0), (243, 226, 27), (15, 15, 243)])
    image.save('test.png', 'PNG')
