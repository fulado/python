from random import randint


class Die(object):
    """表示一个骰子的类"""

    def __init__(self, num_sides=6):
        """默认骰子为6个面"""
        self.num_sides = num_sides

    def roll(self):
        """返回一个位于1和骰子面数之间的随机数"""
        return randint(1, self.num_sides)












