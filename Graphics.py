import math
import numpy as np
from PIL import Image, ImageColor

def draw_circle(arr, y, x, r, colour):
    acc = 70
    accR = 8

    angles = np.arange(acc) * (2 * math.pi / acc)
    distances = np.arange(accR * r) / accR

    points = [np.tile(distances, len(angles)), np.repeat(angles, len(distances))]
    d = points[0]
    a = points[1]
    sin = np.sin(a)
    cos = np.cos(a)

    indY = np.floor(y + d * sin).astype(int)
    indX = np.floor(x + d * cos).astype(int)

    arr[indY, indX] = colour