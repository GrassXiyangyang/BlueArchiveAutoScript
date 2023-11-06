import math
import cv2
import numpy as np

from common import ocr
from common.iconst import *


def color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def check_rgb(self, area, rgb):
    """
    根据一个坐标判断rgb
    """
    area = (area[0], area[1], area[0] + 10, area[1] + 10)
    ocr.screenshot_check_text(self, '', area, 0)
    img = cv2.imread(SS_FILE)
    return np.array_equal(img[0][0], np.array(rgb))


def check_rgb_similar(self, area=(1090, 683, 1091, 684), rgb=(75, 238, 249)):
    """
    判断颜色是否相近，用来判断按钮是否可以点击
    """
    ocr.screenshot_check_text(self, '', area, 0)
    img = cv2.imread(SS_FILE)
    dist = color_distance(img[0][0], rgb)
    return dist <= 20
