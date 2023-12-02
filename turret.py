import pygame as pg
from turret_data import TURRET_DATA
import math

class Turret(pg.sprite.Sprite):

    def __init__(self, sprite_sheets, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.animation_steps = TURRET_DATA[self.upgrade_level - 1].get("animation_steps")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        #координаты
        self.tile_x = tile_x
        self.tile_y = tile_y
        #расчитываем центральные координаты
        self.x = (self.tile_x + 0.5) * 64
        self.y = (self.tile_y + 0.5) * 64

        #анимация
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #обновление изображения
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #создаём прозрачный круг вокруг турели, чтобы показать дальность
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet):
        #читаем изображения из sprite sheet
        size = sprite_sheet.get_height()
        print(size)
        animation_list = []
        for x in range(self.animation_steps):
            print(self.animation_steps)
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group):
        #если цель выбрана, проигрываем анимацию выстрела
        if self.target:
            self.play_animation()
        else:
            #поиск новой цели
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        #проверяем расстояние до врага, хватает ли дистанции
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))

    def play_animation(self):
        #обновляем изображение покадрово
        self.original_image = self.animation_list[self.frame_index]
        #достаточно ли времени прошло с предыдущего кадра
        if pg.time.get_ticks() - self.update_time > 15:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #проверить, завершена ли анимация
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.animation_steps = TURRET_DATA[self.upgrade_level - 1].get("animation_steps")

        #обновляем изображение турели
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        #обновляем прозрачный круг радиуса
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)


