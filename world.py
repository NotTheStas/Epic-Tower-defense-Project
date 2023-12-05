import pygame as pg
from enemy import *
import random


class World():

    def __init__(self, data, map_image):
        self.wave = 1
        self.tile_map = []
        self.waypoints = []
        self.health = 20
        self.money = 600
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0


    def process_data(self):
        #заходим в файл уровня, чтобы достать нужную инфу
        for layer in self.level_data["layers"]:
            if layer["name"] == "\u0421\u043b\u043e\u0439 \u0442\u0430\u0439\u043b\u043e\u0432 1":
                self.tile_map = layer["data"]

            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    x = obj["x"]
                    self.process_waypoints(waypoint_data, x)

    def process_waypoints(self, data, x):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x+x, temp_y))

    def process_enemies(self):
        enemies = LEVEL1_WAVE_DATA[self.wave - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def check_wave_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_wave(self):
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface):
        surface.blit(self.image, (0, 0))