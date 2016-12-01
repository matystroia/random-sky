"""
Please learn to use Git already
Also find a better way of making random slopes
"""

from collections import namedtuple
import random
from PIL import Image
import stripes

__author__ = 'Stroia Matei'

WIDTH = 250
HEIGHT = 250

Point = namedtuple('Point', ['x', 'y'])


class Hill:
    def __init__(self, points, color):
        self.points = points
        self.color = color
        self.coefficients = self.calculate_coefficients()

    def calculate_coefficients(self):
        coefficients = {}
        for p0, p1, p2, p3 in zip([self.points[0]] + self.points,
                                  self.points,
                                  self.points[1:],
                                  self.points[2:] + [self.points[-1]]):
            coefficients[(p1.x, p2.x)] = (-1 / 2 * p0.y + 3 / 2 * p1.y - 3 / 2 * p2.y + 1 / 2 * p3.y,
                                          p0.y - 5 / 2 * p1.y + 2 * p2.y - 1 / 2 * p3.y,
                                          -1 / 2 * p0.y + 1 / 2 * p2.y,
                                          p1.y)
        return coefficients

    def get_height(self, p1, p2, t):
        c = self.coefficients[(p1, p2)]
        return c[0]*(t**3) + c[1]*(t**2) + c[2]*t + c[3]

    def get_color(self, x, y):
        return self.color


class RandomSky:
    def __init__(self, pixels, hills, sky_color):
        self.pixels = pixels
        self.hills = hills
        self.sky_color = sky_color

    def make_image(self):
        last_heights = [HEIGHT] * WIDTH
        for hill in self.hills:
            x_values = [point.x for point in hill.points]
            for p1, p2 in zip(x_values, x_values[1:]):
                for col in range(int(p1), int(p2)):
                    t = (col - p1) / (p2 - p1)
                    h = hill.get_height(p1, p2, t)
                    try:
                        if h < last_heights[col]:
                            for row in range(int(h), int(last_heights[col])):
                                # pixels[col, row] = hill.get_color(col, row) if t != 0.0 else (0, 255, 0)
                                self.pixels[col, row] = hill.get_color(col, row)
                            last_heights[col] = h
                    except Exception as e:
                        pass

        for col in range(0, WIDTH):
            for row in range(0, int(last_heights[col])):
                self.pixels[col, row] = self.sky_color
                # pixels[col, row] = sky_colors[(col + row) // ((WIDTH + HEIGHT) // 10)]


if __name__ == '__main__':
    image = Image.new('RGB', (WIDTH, HEIGHT))
    pixels_ = image.load()

    # land_colors = [stripes.gen_color_palette(26, range(55, 205), (55, 205), (55, 205)) for _ in range(3)]
    # land_colors = [(55 + k*55, 55, 55) for k in range(3)]
    land_colors = [(18, 18, 42), (32, 36, 71), (31, 52, 107), (41, 80, 159), (37, 83, 160), (46, 94, 179),
                   (51, 108, 180), (72, 127, 210), (111, 166, 231), (196, 219, 235), (205, 224, 238)]
    sky_colors = stripes.gen_color_palette(10, (55,), (55,), range(55, 125))
    sky_color = (221, 231, 241)

    rng = random.Random()

    hill_lst = []
    for k in range(11):
        points_ = []
        # color_ = (75 + k*35, 55, 55)
        color_ = land_colors[k]
        start_height = HEIGHT - 25 - k*10
        variance = 10 + k * 2
        points_.append(Point(0, start_height + rng.randint(0, variance)))
        for _ in range(20 - k*2):
            x = int(WIDTH/(20-k*2) + _ * (WIDTH/(20-k*2)))
            # x = rng.randint(0, WIDTH)
            y = start_height + rng.randint(0, variance)
            points_.append(Point(x, y))
        points_.append(Point(WIDTH, start_height + rng.randint(0, variance)))
        hill_lst.append(Hill(sorted(points_, key=lambda p: p.x), color_))

    randomSky = RandomSky(pixels_, hill_lst)
    randomSky.make_image()

    '''
    for col in range(WIDTH):

        if col % dist == 0:
            i += 1
            h = heights[i]




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
                pixels[col, row] = land_colors[i]
    '''
    image.save('sky.png')
