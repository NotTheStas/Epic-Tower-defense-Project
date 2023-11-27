import pygame as pg
import pygame.image
import sys
from enemy import Enemy
from menu import *

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#constants
SCREEN_WIDTH = 1365
SCREEN_HEIGHT = 768
FPS = 60

#set game window resolution
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Epic Tower Defense")

#create groups
enemy_group = pg.sprite.Group()

#load images
enemy_image = pg.image.load('assets/textures/enemies/soldier.png').convert_alpha()

waypoints = [
    (200, 200),
    (250, 320),
    (600, 600),

]

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

def main_menu():

    #Создание кнопок
    levels_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 200, 252, 74, "Level Select", 'assets/textures/gui/buttons/rect/default@2x.png', 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')
    quit_button = ImageButton(SCREEN_WIDTH / 2 - (252 / 2), 300, 252, 74, "Quit", 'assets/textures/gui/buttons/rect/default@2x.png', 'assets/textures/gui/buttons/rect/hover@2x.png', 'assets/sound/button.wav')

    menu_background = pg.image.load("assets/textures/tiles/map1.png")

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

            for buttons in [levels_button, quit_button]:
                buttons.handle_event(event)

        for buttons in [levels_button, quit_button]:
            buttons.check_hover(pg.mouse.get_pos())
            buttons.draw(screen)

        pg.display.flip()
main_menu()

#Основной игровой цикл
game_run = True
while game_run:

    clock.tick(FPS)
    screen.fill("grey100")
    #enemy_group.update()
    #draw enemy path
    #pg.draw.lines(screen, "grey0", False, waypoints)
    #draw groups
    #enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False
    pg.display.flip()
#pg.quit()