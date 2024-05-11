import pygame
import math
import json

class pellet:
    def __init__(self, x, y, color, mass = 1):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(self.mass) * 6

    def draw(self, middle, window, ratio):
        size = window.get_size()
        if self.x < middle[0] + size[0] / (2 * ratio) and self.x > middle[0] - size[0] / (2 * ratio):
            if self.y < middle[1] + size[1] / (2 * ratio) and self.y > middle[1] - size[1] / (2 * ratio):
                pygame.draw.circle(window, self.color, (middle[0] - self.x + size[0] / 2, middle[1] - self.y + size[1] / 2), self.size / ratio)

    def eaten(self, player):
        if self.mass <= 0.8 * player.mass:
            x1 = player.x
            x2 = self.x
            y1 = player.y
            y2 = self.y
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (player.size - self.size) ** 2:
                player.mass += self.mass
                player.update()
                return True
            
        return False

    def to_json(self):
        data = [self.x, self.y, self.color, self.mass]
        return json.dumps(data)
    
def from_json(data):
    data = json.loads(data)
    new = pellet(data[0], data[1], data[2], data[3])
    return new
