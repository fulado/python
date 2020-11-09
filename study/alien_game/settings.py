"""
存储游戏设置
"""


class Settings():
    """游戏设置"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船速度因子
        self.ship_speed_factor = 2.5

        # 子弹
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10  # 外星人群下降数据
        self.fleet_direction = 1  # 外星人移动方向, 1-右, -1-左


