import pygame as pg
import pygame.image
import sys
import json
from enemy import *
from menu import *
from world import *

#инициализация pygame
pg.init()

#создание clock
clock = pg.time.Clock()

#переменные
ROWS = 12
COLS = 12
TILE_SIZE = 64
SCREEN_WIDTH = 1088
SCREEN_HEIGHT = 768
FPS = 60

#ставим разрешение окна игры
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Epic Tower Defense")

#Сцена Главного меню
def main_menu():

    #Создание кнопок
    levels_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Level Select", 'assets/textures/gui/buttons/rect/default@2x.png', 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    quit_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Quit", 'assets/textures/gui/buttons/rect/default@2x.png', 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    menu_background = pg.image.load("assets/textures/menu.png")

    main_menu_run = True
    while main_menu_run:
        screen.blit(menu_background, (0, 0))


        # Название игры
        font = pg.font.Font(None, 72)
        text_surface = font.render("Epic Tower Defense", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_menu_run = False
                pg.quit()
                sys.exit()
                quit()

            if event.type == pg.USEREVENT and event.button == quit_button:
                main_menu_run = False
                pg.quit()
                sys.exit()
                quit()

            if event.type == pg.USEREVENT and event.button == levels_button:
                levels_menu()

            for buttons in [levels_button, quit_button]:
                buttons.handle_event(event)

        for buttons in [levels_button, quit_button]:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()

#Сцена Меню уровней
def levels_menu():

    #Создание кнопок
    level1_button = ImageButton((SCREEN_WIDTH / 3) - 200, SCREEN_HEIGHT / 3, 200, 200, "1", 'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    level2_button = ImageButton((SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT / 3, 200, 200, "2", 'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    level3_button = ImageButton(SCREEN_WIDTH - (SCREEN_WIDTH / 3), SCREEN_HEIGHT / 3, 200, 200, "3", 'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    back_button = ImageButton(20, 645, 110, 110, "", 'assets/textures/gui/buttons/square/ArrowLeft-Thin/Default@2x.png', 'assets/textures/gui/buttons/square/ArrowLeft-Thin/Hover@2x.png', 'assets/sound/button.wav')

    menu_background = pg.image.load("assets/textures/menu.png")

    levels_menu_run = True
    while levels_menu_run:
        screen.blit(menu_background, (0, 0))

        # Надпись Выбор уровня
        font = pg.font.Font(None, 72)
        text_surface = font.render("Выбор уровня", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                levels_menu_run = False
                pg.quit()
                sys.exit()
                quit()

            #Кнопка назад в главное меню и выход через эскейп
            if (event.type == pg.USEREVENT and event.button == back_button) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                levels_menu_run = False
                main_menu()

            if event.type == pg.USEREVENT and event.button == level1_button:
                levels_menu_run = False
                level1()


            for buttons in [level1_button, level2_button, level3_button, back_button]:
                buttons.handle_event(event)

        for buttons in [level1_button, level2_button, level3_button, back_button]:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()

#Сцена Первого уровня
def level1():

    #загрузка изображений
    enemy_image = pg.image.load('assets/textures/enemies/soldier.png').convert_alpha()
    map_image = pg.image.load("assets/textures/maps/map1.png")

    #чтение файла data
    file = open('assets/levels/level1/level1.tmj')
    world_data = json.load(file)

    #создание мира
    world = World(world_data, map_image)
    world.process_data()

    #создание групп
    enemy_group = pg.sprite.Group()
    enemy = Enemy(world.waypoints, enemy_image)
    enemy_group.add(enemy)

    level1_run = True
    while level1_run:

        clock.tick(FPS)

        world.draw(screen)

        enemy_group.update()

        enemy_group.draw(screen)

        pg.draw.lines(screen, "grey0", False, world.waypoints)
        print(world.waypoints)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                levels_menu_run = False
                pg.quit()
                sys.exit()
                quit()

        pg.display.flip()

#Запуск главного меню
main_menu()