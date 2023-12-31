import json
import pygame as pg

from enemy import Enemy
from menu import ImageButton
from world import World
from turret import Turret
from turret_data import TURRET_COST
from constants import *

# инициализация pygame
pg.init()

# создание clock
clock = pg.time.Clock()

# ставим разрешение окна игры
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Epic Tower Defense")

# загружаем шрифт для отображения текста
text_font = pg.font.SysFont("Consolas", 30, bold=True)
large_font = pg.font.SysFont("Consolas", 36)

# открытие сохранения
stars_save = open("savedata/stars.txt")
LEVELS_STARS = list(map(int, stars_save.readline().split()))
stars_save.close()


# Сцена Главного меню
def main_menu():
    # Создание кнопок
    levels_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Выбор уровня",
                                'assets/textures/gui/buttons/rect/default@2x.png',
                                'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    quit_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Выход",
                              'assets/textures/gui/buttons/rect/default@2x.png',
                              'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    menu_background = pg.image.load("assets/textures/menu.png")

    main_menu_run = True
    while main_menu_run:
        screen.blit(menu_background, (0, 0))

        # Название игры
        font = pg.font.SysFont(None, 72)
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
    buttons_list = [level1_button, level2_button, level3_button, back_button]

    menu_background = pg.image.load("assets/textures/menu.png")

    stars = []
    for level_id in range(1, 3 + 1):
        stars.append(
            pg.image.load(f'assets/textures/gui/level/star/Group/{LEVELS_STARS[level_id - 1]}-3@1x.png'))

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
                running_level = 1
                level(running_level)

            if event.type == pg.USEREVENT and event.button == level2_button:
                levels_menu_run = False
                running_level = 2
                level(running_level)

            if event.type == pg.USEREVENT and event.button == level3_button:
                levels_menu_run = False
                running_level = 3
                level(running_level)

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        screen.blit(stars[0], ((SCREEN_WIDTH / 3) - 200 + 46, SCREEN_HEIGHT / 2 + 1))
        screen.blit(stars[1], ((SCREEN_WIDTH / 3) + 127, SCREEN_HEIGHT / 2 + 1))
        screen.blit(stars[2], ((SCREEN_WIDTH / 3) + 408, SCREEN_HEIGHT / 2 + 1))

        pg.display.flip()


# Сцена Паузы
def pause(running_level):
    pause_width = SCREEN_WIDTH / 2
    pause_height = SCREEN_HEIGHT - 100

    # кнопки
    levels_button = ImageButton(pause_width - 126, 400, 252, 74, "Выбор уровня",
                                'assets/textures/gui/buttons/rect/default@2x.png',
                                'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    quit_button = ImageButton(pause_width - 126, 500, 252, 74, "Выход",
                              'assets/textures/gui/buttons/rect/default@2x.png',
                              'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    restart_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Начать заново",
                                 'assets/textures/gui/buttons/rect/default@2x.png',
                                 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    continue_button = ImageButton(pause_width - 126, 200, 252, 74, "Продолжить",
                                  'assets/textures/gui/buttons/rect/default@2x.png',
                                  'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    buttons_list = [levels_button, quit_button, continue_button, restart_button]

    # фон
    p_background = pg.image.load("assets/textures/pause_background.png")

    pause_menu_run = True

    while pause_menu_run:

        screen.blit(p_background, (SCREEN_WIDTH / 4, 50))

        # Надпись Выбор уровня
        font = pg.font.Font(None, 72)
        text_surface = font.render("Пауза", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 135))
        screen.blit(text_surface, text_rect)

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

            if event.type == pg.USEREVENT and event.button == restart_button:
                level(running_level)

            if event.type == pg.USEREVENT and event.button == continue_button:
                pause_menu_run = False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.mixer.Sound("assets/sound/button.wav").play()
                pause_menu_run = False

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()


# Сцена Меню Проигрыша
def game_over_menu1(running_level):
    restart_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Начать заново",
                                 'assets/textures/gui/buttons/rect/default@2x.png',
                                 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    to_main_menu_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Главное меню",
                                      'assets/textures/gui/buttons/rect/default@2x.png',
                                      'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    to_levels_menu_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 400, 252, 74, "Выбор уровня",
                                        'assets/textures/gui/buttons/rect/default@2x.png',
                                        'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    buttons_list = [restart_button, to_main_menu_button, to_levels_menu_button]

    menu_back = pg.image.load("assets/textures/menu.png")

    game_over_run = True
    while game_over_run:
        screen.blit(menu_back, (0, 0))

        font = pg.font.Font(None, 72)
        text_surface = font.render("Ты проиграл", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over_run = False
                pg.quit()

            if event.type == pg.USEREVENT and event.button == restart_button and level == 1:
                game_over_run = False
                level(running_level)

            if event.type == pg.USEREVENT and event.button == to_main_menu_button:
                game_over_run = False
                main_menu()

            if event.type == pg.USEREVENT and event.button == to_levels_menu_button:
                game_over_run = False
                levels_menu()

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()


# Сцена Меню Выигрыша
def game_win_menu(running_level, rest_lifes):
    # создание кнопок
    restart_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Начать заново",
                                 'assets/textures/gui/buttons/rect/default@2x.png',
                                 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    main_menu_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 400, 252, 74, "Главное меню",
                                   'assets/textures/gui/buttons/rect/default@2x.png',
                                   'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    levels_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 500, 252, 74, "Выбор уровня",
                                'assets/textures/gui/buttons/rect/default@2x.png',
                                'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    buttons_list = [restart_button, main_menu_button, levels_button]

    # фон
    background = pg.image.load("assets/textures/menu.png")

    # количество звёзд
    if rest_lifes >= BASE_HEALTH * 0.9:
        stars = pg.image.load('assets/textures/gui/level/star/Group/3-3@2x.png')
        LEVELS_STARS[running_level - 1] = 3
    elif rest_lifes >= BASE_HEALTH * 0.5:
        stars = pg.image.load('assets/textures/gui/level/star/Group/2-3@2x.png')
        if LEVELS_STARS[running_level - 1] < 3: LEVELS_STARS[running_level - 1] = 2
    elif rest_lifes >= BASE_HEALTH * 0.2:
        stars = pg.image.load('assets/textures/gui/level/star/Group/1-3@2x.png')
        if LEVELS_STARS[running_level - 1] < 2: LEVELS_STARS[running_level - 1] = 1
    else:
        stars = pg.image.load('assets/textures/gui/level/star/Group/0-3@2x.png')
        if LEVELS_STARS[running_level - 1] < 1: LEVELS_STARS[running_level - 1] = 0

    print(" ".join(map(str, LEVELS_STARS)))
    # запись сохранения
    stars_save = open("savedata/stars.txt", "w")
    stars_save.write(" ".join(map(str, LEVELS_STARS)))
    stars_save.close()

    game_win_run = True
    while game_win_run:
        screen.blit(background, (0, 0))

        font = pg.font.Font(None, 72)
        text_surface = font.render("Победа!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        screen.blit(stars, (SCREEN_WIDTH / 2 - 77, 150))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_win_run = False
                pg.quit()

            if event.type == pg.USEREVENT and event.button == restart_button:
                game_win_run = False
                level(running_level)

            if event.type == pg.USEREVENT and event.button == main_menu_button:
                game_win_run = False
                main_menu()

            if event.type == pg.USEREVENT and event.button == levels_button:
                game_win_run = False
                levels_menu()

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()


# Сцена Уровня
def level(running_level):
    # загрузка изображений
    enemy_images = {
        "soldier": pg.image.load("assets/textures/enemies/soldier.png").convert_alpha(),
        "heavy_soldier": pg.image.load("assets/textures/enemies/heavy_soldier.png").convert_alpha(),
        "runner": pg.image.load("assets/textures/enemies/runner.png").convert_alpha(),
        "robot": pg.image.load("assets/textures/enemies/robot.png").convert_alpha(),
        "light_robot": pg.image.load("assets/textures/enemies/light_robot.png").convert_alpha(),
        "light_tank": pg.image.load("assets/textures/enemies/light_tank1.png").convert_alpha(),
        "heavy_tank": pg.image.load("assets/textures/enemies/heavy_tank1.png").convert_alpha()
    }

    turrets_spritesheets = [[], []]
    turrets_images = [pg.image.load('assets/textures/towers/cannon/cannon1.png').convert_alpha(),
                      pg.image.load('assets/textures/towers/rocket/rockettower1.png').convert_alpha()]
    turret_sounds = [pg.mixer.Sound("assets/sound/cannon.wav"), pg.mixer.Sound("assets/sound/rocket.wav")]
    for x in range(1, TURRET_LEVELS + 1):
        turret1_sheet = pg.image.load(f'assets/textures/towers/cannon/cannon{x}_sheet.png').convert_alpha()
        turret2_sheet = pg.image.load(f'assets/textures/towers/rocket/rockettower{x}_sheet.png').convert_alpha()
        turrets_spritesheets[0].append(turret1_sheet)
        turrets_spritesheets[1].append(turret2_sheet)
    print(turrets_spritesheets)

    map_image = pg.image.load(f"assets/textures/maps/map{running_level}.png")
    battle_gui = pg.image.load("assets/textures/battle_gui.png")
    coin_icon = pg.image.load("assets/textures/gui/battle/coin.png").convert_alpha()
    heart_icon = pg.image.load("assets/textures/gui/battle/heart.png").convert_alpha()
    wave_icon = pg.image.load("assets/textures/gui/battle/wave.png").convert_alpha()

    # создание кнопок
    turret1_button = ImageButton(768 + 45, 250, 105, 105, "", 'assets/textures/gui/button/icon/cannon1_iconDefault.png',
                                 "assets/textures/gui/button/icon/cannon1_iconHover.png", 'assets/sound/button.wav')
    turret2_button = ImageButton(768 + 170, 250, 105, 105, "",
                                 'assets/textures/gui/button/icon/rocket1_iconDefault.png',
                                 "assets/textures/gui/button/icon/rocket1_iconHover.png", 'assets/sound/button.wav')
    cancel_button = ImageButton(768 + 45, 400, 230, 45, "Отменить",
                                'assets/textures/gui/buttons/rect/cancel_buttonDefault.png',
                                "assets/textures/gui/buttons/rect/cancel_buttonHover.png", 'assets/sound/button.wav')
    upgrade_button = ImageButton(768 + 45, 460, 230, 45, "Улучшить",
                                 'assets/textures/gui/buttons/rect/upgrade_buttonDefault.png',
                                 "assets/textures/gui/buttons/rect/upgrade_buttonHover.png", 'assets/sound/button.wav')
    begin_button = ImageButton(768 + 45, 520, 230, 45, "Начать волну",
                               'assets/textures/gui/buttons/rect/begin_buttonDefault.png',
                               "assets/textures/gui/buttons/rect/begin_buttonHover.png", 'assets/sound/button.wav')
    speedup_button = ImageButton(768 + 107.5, 580, 105, 105, "",
                                 'assets/textures/gui/button/icon/speedup_iconDefault.png',
                                 "assets/textures/gui/button/icon/speedup_iconHover.png", 'assets/sound/button.wav')

    buttons_list = [turret1_button, turret2_button, cancel_button, upgrade_button, begin_button, speedup_button]

    # чтение файла data
    file = open(f'assets/levels/level{running_level}/level{running_level}.tmj')
    world_data = json.load(file)

    # создание мира
    world = World(world_data, map_image, running_level)
    world.process_data()
    world.process_enemies()

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
                turret = Turret(turrets_spritesheets[turret_id - 1], mouse_tile_x, mouse_tile_y, turret_id,
                turret_sounds[turret_id - 1])
                turret_group.add(turret)
                world.money -= TURRET_COST[turret_id - 1]

    def select_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret

    def clear_selection():
        for turret in turret_group:
            turret.selected = False

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # игровые переменные
    game_over = False
    last_enemy_spawn = pg.time.get_ticks()
    turret_placing = False
    selected_turret = None
    wave_started = False
    game_speedup = False
    FPS = 60

    # создание групп
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    level_run = True
    while level_run:

        clock.tick(FPS)

        if game_over == False:
            # проверить, проиграл ли игрок
            if world.health <= 0:
                game_over = True
                pg.mixer.Sound("assets/sound/defeat.wav").play()
                game_over_menu1(running_level)

            # проверить, победил ли игрок ли игрок
            if world.wave > TOTAL_WAVES:
                game_over = True
                pg.mixer.Sound("assets/sound/testing/unknown.wav").play()
                game_win_menu(running_level, world.health)

        # подсветка выбранной турели
        if selected_turret:
            selected_turret.selected = True

        # отрисовка экрана
        world.draw(screen)

        # отрисовка групп
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        # отрисовка хп, денег, волны, интерфейса
        screen.blit(battle_gui, (768, 0))
        draw_text(str(world.health), text_font, "grey100", 786 + 50, 50)
        draw_text(str(world.money), text_font, "grey100", 786 + 50, 85)
        draw_text(str(world.wave) + "/15", text_font, "grey100", 786 + 50, 120)
        screen.blit(heart_icon, (786 + 18, 50 - 3))
        screen.blit(coin_icon, (786 + 18, 85 - 3))
        screen.blit(wave_icon, (786 + 18, 120 - 3))

        # спавн врагов
        if wave_started == True:
            if pg.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()
        else:
            begin_button.draw(screen)

        # обновление групп
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.mixer.Sound("assets/sound/button.wav").play()
                turret1_button.draw(screen)
                turret2_button.draw(screen)
                speedup_button.draw(screen)
                if turret_placing:
                    cancel_button.draw(screen)
                if selected_turret and selected_turret.upgrade_level < TURRET_LEVELS:
                    upgrade_button.draw(screen)
                pause(running_level)

            if (event.type == pg.USEREVENT and event.button == cancel_button) or (
                    event.type == pg.MOUSEBUTTONDOWN and event.button == 3):
                turret_placing = False

            if selected_turret:
                if selected_turret.upgrade_level < TURRET_LEVELS:
                    if event.type == pg.USEREVENT and event.button == upgrade_button:
                        if world.money >= UPGRADE_COST:
                            selected_turret.upgrade()
                            world.money -= UPGRADE_COST

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()

                if mouse_pos[0] < TILE_SIZE * ROWS and mouse_pos[1] < TILE_SIZE * COLS:
                    # убираем выбранные турели
                    selected_turret = None
                    clear_selection()
                    if turret_placing:
                        if world.money >= BUY_COST:
                            create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)

            if event.type == pg.USEREVENT and event.button == turret1_button:
                turret_id = 1
                turret_placing = True

            if event.type == pg.USEREVENT and event.button == turret2_button:
                turret_id = 2
                turret_placing = True

            if event.type == pg.USEREVENT and event.button == speedup_button:
                if game_speedup:
                    game_speedup = False
                    world.game_speed = 1
                else:
                    game_speedup = True
                    world.game_speed = 2

            # проверка, начата ли волна
            if wave_started == False:
                if event.type == pg.USEREVENT and event.button == begin_button:
                    wave_started = True

            for buttons in buttons_list:
                buttons.handle_event(event)

        for buttons in buttons_list:
            buttons.check_hover(pg.mouse.get_pos())
            speedup_button.draw(screen)
            turret1_button.draw(screen)
            turret2_button.draw(screen)
            if turret_placing:
                cursor_rect = turrets_images[turret_id - 1].get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= SCREEN_HEIGHT:
                    screen.blit(turrets_images[turret_id - 1], cursor_rect)
                cancel_button.draw(screen)
            if selected_turret and selected_turret.upgrade_level < TURRET_LEVELS:
                upgrade_button.draw(screen)

        # проверка, закончена ли волна
        if world.check_wave_complete() == True:
            world.money += LEVEL_COMPLETE_REWARD
            world.wave += 1
            wave_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_wave()
            world.process_enemies()

        pg.display.flip()


# Запуск главного меню
main_menu()
