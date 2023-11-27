import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        #определение целевой точки
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
        #расчитать расстояние до цели
        dist = self.movement.length()
        #превышает ли оставшееся расстояние скорость противника
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
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