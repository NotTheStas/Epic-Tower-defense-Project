import pygame as pg
import math
from pygame.math import Vector2
from enemy_data import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.type = enemy_type
        self.health = ENEMY_DATA.get(self.type)["health"]
        self.speed = ENEMY_DATA.get(self.type)["speed"]
        self.angle = 0
        self.original_image = images.get(self.type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        #определение целевой точки
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.missed_enemies += 1
            world.health -= 1
            pg.mixer.Sound("assets/sound/health damage.wav").play()

        #расчитать расстояние до цели
        dist = self.movement.length()
        #превышает ли оставшееся расстояние скорость противника
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        #рассчитать расстояние до следующей точки
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #поворачиваем изображение
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += ENEMY_DATA.get(self.type)["money"]
            self.kill()