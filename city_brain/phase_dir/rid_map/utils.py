"""
工具
"""

import math


# 根据角度计算线段的终点
def get_pos2(angle):
    rad = math.pi / 180 * angle

    x = math.cos(rad) * 100 + 100
    y = math.sin(rad) * 100 + 100

    return x, y







