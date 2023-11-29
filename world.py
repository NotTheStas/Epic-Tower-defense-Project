import pygame as pg

class World():

    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image

    def process_data(self):
        #заходим в файл уровня, чтобы достать нужную инфу
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
                print(self.tile_map)
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    x = obj["x"]
                    self.process_waypoints(waypoint_data, x)

    def process_waypoints(self, data, x):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x+x, temp_y))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))