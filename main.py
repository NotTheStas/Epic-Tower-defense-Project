import json
import pygame as pg

from enemy import Enemy
from menu import ImageButton
from world import World
from turret import Turret

# инициализация pygame
pg.init()

# создание clock
clock = pg.time.Clock()

# переменные
ROWS = 12
COLS = 12
TILE_SIZE = 64
SCREEN_WIDTH = 1088
SCREEN_HEIGHT = 768
FPS = 60
TURRET_LEVELS = 3

# ставим разрешение окна игры
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Epic Tower Defense")


# Сцена Главного меню
def main_menu():
    # Создание кнопок
    levels_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Level Select",
                                'assets/textures/gui/buttons/rect/default@2x.png',
                                'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    quit_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Quit",
                              'assets/textures/gui/buttons/rect/default@2x.png',
                              'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

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

            if event.type == pg.USEREVENT and event.button == quit_button:
                main_menu_run = False
                pg.quit()

            if event.type == pg.USEREVENT and event.button == levels_button:
                levels_menu()

            for buttons in [levels_button, quit_button]:
                buttons.handle_event(event)

        for buttons in [levels_button, quit_button]:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()


# Сцена Меню уровней
def levels_menu():
    # Создание кнопок
    level1_button = ImageButton((SCREEN_WIDTH / 3) - 200, SCREEN_HEIGHT / 3, 200, 200, "1",
                                'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    level2_button = ImageButton((SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT / 3, 200, 200, "2",
                                'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    level3_button = ImageButton(SCREEN_WIDTH - (SCREEN_WIDTH / 3), SCREEN_HEIGHT / 3, 200, 200, "3",
                                'assets/textures/gui/level/button/Unlocked@2x.png', '', 'assets/sound/button.wav')
    back_button = ImageButton(20, 645, 110, 110, "", 'assets/textures/gui/buttons/square/ArrowLeft-Thin/Default@2x.png',
                              'assets/textures/gui/buttons/square/ArrowLeft-Thin/Hover@2x.png',
                              'assets/sound/button.wav')

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

            # Кнопка назад в главное меню и выход через эскейп
            if (event.type == pg.USEREVENT and event.button == back_button) or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
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


def pause():
    pause_width = SCREEN_WIDTH / 2
    pause_height = SCREEN_HEIGHT - 100

    # кнопки
    levels_button = ImageButton(pause_width - 126, 300, 252, 74, "Level Select",
                                'assets/textures/gui/buttons/rect/default@2x.png',
                                'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    quit_button = ImageButton(pause_width - 126, 400, 252, 74, "Quit",
                              'assets/textures/gui/buttons/rect/default@2x.png',
                              'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    continue_button = ImageButton(pause_width - 126, 200, 252, 74, "Continue",
                                  'assets/textures/gui/buttons/rect/default@2x.png',
                                  'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    # restart_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Restart",'assets/textures/gui/buttons/rect/default@2x.png','assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    buttons_list = [levels_button, quit_button, continue_button]

    # фон
    p_background = pg.image.load("assets/textures/pause_background.png")

    pause_menu_run = True

    while pause_menu_run:

        screen.blit(p_background, (SCREEN_WIDTH / 4, 50))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause_menu_run = False
                pg.quit()

            if event.type == pg.USEREVENT and event.button == quit_button:
                pause_menu_run = False
                pg.quit()

            if event.type == pg.USEREVENT and event.button == levels_button:
                pause_menu_run = False
                levels_menu()

            if event.type == pg.USEREVENT and event.button == continue_button:
                pause_menu_run = False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause_menu_run = False

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()


# Сцена Первого уровня
def level1():
    # загрузка изображений
    enemy_image = pg.image.load('assets/textures/enemies/soldier.png').convert_alpha()
    cannon_image = pg.image.load('assets/textures/towers/cannon/cannon1.png').convert_alpha()
    cannon_sheet = pg.image.load('assets/textures/towers/cannon/cannon1_sheet.png').convert_alpha()
    cannon_spritesheets = []
    for x in range(1, TURRET_LEVELS + 1):
        cannon_sheet = pg.image.load(f'assets/textures/towers/cannon/cannon{x}_sheet.png').convert_alpha()
        cannon_spritesheets.append(cannon_sheet)
    map_image = pg.image.load("assets/textures/maps/map1.png")
    battle_gui = pg.image.load("assets/textures/battle_gui.png")

    # создание кнопок
    turret1_button = ImageButton(768 + 45, 250, 105, 105, "", 'assets/textures/gui/button/icon/cannon1_iconDefault.png',
                                 "assets/textures/gui/button/icon/cannon1_iconHover.png", 'assets/sound/button.wav')
    turret2_button = ImageButton(768 + 170, 250, 105, 105, "",
                                 'assets/textures/gui/button/icon/rocket1_iconDefault.png',
                                 "assets/textures/gui/button/icon/rocket1_iconHover.png", 'assets/sound/button.wav')
    cancel_button = ImageButton(768 + 45, 400, 230, 45, "Cancel",
                                'assets/textures/gui/buttons/rect/cancel_buttonDefault.png',
                                "assets/textures/gui/buttons/rect/cancel_buttonHover.png", 'assets/sound/button.wav')
    upgrade_button = ImageButton(768 + 45, 460, 230, 45, "Upgrade",
                                 'assets/textures/gui/buttons/rect/upgrade_buttonDefault.png',
                                 "assets/textures/gui/buttons/rect/upgrade_buttonHover.png", 'assets/sound/button.wav')

    buttons_list = [turret1_button, turret2_button, cancel_button, upgrade_button]

    # чтение файла data
    file = open('assets/levels/level1/level1.tmj')
    world_data = json.load(file)

    # создание мира
    world = World(world_data, map_image)
    world.process_data()

    # функция создания турелей
    def create_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE

        # вычисляем порядковый номер клетки
        mouse_tile_num = (mouse_tile_y * COLS) + mouse_tile_x

        # проверка, является ли данная клетка травой
        if world.tile_map[mouse_tile_num] == 9:
            # проверка, поставлена ли в клетке турель
            space_is_free = True
            for turret in turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
            if space_is_free == True:
                cannon = Turret(cannon_spritesheets, mouse_tile_x, mouse_tile_y)
                turret_group.add(cannon)

    def select_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret

    def clear_selection():
        for turret in turret_group:
            turret.selected = False

    # переменные турелей
    turret_placing = False
    selected_turret = None

    # создание групп
    enemy_group = pg.sprite.Group()
    enemy = Enemy(world.waypoints, enemy_image)
    enemy_group.add(enemy)
    turret_group = pg.sprite.Group()

    level1_run = True
    while level1_run:

        clock.tick(FPS)

        # обновление групп
        enemy_group.update()
        turret_group.update(enemy_group)

        # подсветка выбранной турели
        if selected_turret:
            selected_turret.selected = True

        # отрисовка экрана
        screen.blit(battle_gui, (768, 0))
        world.draw(screen)

        # отрисовка групп
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                levels_menu_run = False
                pg.quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause()

            if event.type == pg.USEREVENT and event.button == turret1_button and turret_placing == False:
                turret_placing = True

            if (event.type == pg.USEREVENT and event.button == cancel_button) or (
                    event.type == pg.MOUSEBUTTONDOWN and event.button == 3):
                turret_placing = False

            if selected_turret:
                if selected_turret.upgrade_level < TURRET_LEVELS:
                    if event.type == pg.USEREVENT and event.button == upgrade_button:
                        selected_turret.upgrade()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()

                if mouse_pos[0] < TILE_SIZE * ROWS and mouse_pos[1] < TILE_SIZE * COLS:
                    # убираем выбранные турели
                    selected_turret = None
                    clear_selection()
                    if turret_placing:
                        create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            turret1_button.draw(screen)
            turret2_button.draw(screen)
            if turret_placing:
                cursor_rect = cannon_image.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= SCREEN_HEIGHT:
                    screen.blit(cannon_image, cursor_rect)
                cancel_button.draw(screen)
            if selected_turret and selected_turret.upgrade_level < TURRET_LEVELS:
                upgrade_button.draw(screen)

        pg.display.flip()


# Запуск главного меню
main_menu()
