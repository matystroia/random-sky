from PIL import Image
import random
import moviepy.editor as mpy
import numpy
from collections import namedtuple

from random_sky import Hill, RandomSky

WIDTH = 250
HEIGHT = 250
Point = namedtuple('Point', ['x', 'y'])


def make_frame(t):
    frame = t * 60
    img = Image.new('RGB', (250, 250))
    pix = img.load()

    new_lst = []
    for i, hill in enumerate(hill_lst):
        new_points = []
        for point in hill.points:
            new_points.append(Point(point.x + frame * (1/(i+1)), point.y))
        new_lst.append(Hill(new_points, hill.color))

    sky = RandomSky(pix, new_lst, sky_color)
    sky.make_image()
    return numpy.array(img)


land_colors = [(18, 18, 42), (32, 36, 71), (31, 52, 107), (41, 80, 159), (37, 83, 160), (46, 94, 179),
               (51, 108, 180), (72, 127, 210), (111, 166, 231), (196, 219, 235), (205, 224, 238)]
sky_color = (221, 231, 241)

if __name__ == '__main__':
    rng = random.Random()

    hill_lst = []
    for k in range(11):
        points_ = []
        color_ = land_colors[k]
        start_height = HEIGHT - 25 - k * 10
        variance = 10 + k * 2
        points_.append(Point(0, start_height + rng.randint(0, variance)))
        for _ in range((12-k) * (20 - k)):
            x = int(WIDTH / (20 - k) + _ * (WIDTH / (20 - k))) - (11-k)*WIDTH
            y = start_height + rng.randint(0, variance)
            points_.append(Point(x, y))
        points_.append(Point(WIDTH, start_height + rng.randint(0, variance)))
        hill_lst.append(Hill(sorted(points_, key=lambda p: p.x), color_))

    clip = mpy.VideoClip(make_frame, duration=(1/60) * WIDTH * 11)
    clip.write_videofile('sky.webm', fps=60)
