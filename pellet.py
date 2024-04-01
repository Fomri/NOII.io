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

    def draw(self, window , player):
        size = window.get_size()
        if self.x < player.x + size[0] / 2 and self.x > player.x - size[0] / 2:
            if self.y < player.y + size[1] / 2 and self.y > player.y - size[1] / 2:
                pygame.draw.circle(window, self.color, (player.x - self.x + size[0], player.y - self.y + size[1]))

    def eaten(self, player):
        if self.mass <= 0.8 * player.mass:
            x1 = player.x
            x2 = self.x
            y1 = player.y
            y2 = self.y
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= player.size - self.size:
                player.mass += 1
                player.update()
                return True
            
        return False

def to_json(self):
    data = [self.x, self.y, self.mass, self.size]
    return json.dumps(data)
