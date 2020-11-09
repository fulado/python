import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人群
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)

        # 更新飞船
        ship.update()

        # 更新子弹
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)

        # 更新外星人
        gf.update_aliens(ai_settings, aliens)

        # 每次循环重绘屏幕
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


if __name__ == '__main__':
    run_game()


