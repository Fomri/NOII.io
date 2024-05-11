import pygame
import math
import json

class player:
    def __init__(self, x, y, color, conn, mass = 10, name = ""):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(mass) * 6
        self.speed = 2 * (mass ** -0.5)
        self.name = name
        self.conn = conn

    def move(self, angle, mapSize):
        velX = math.cos(angle) * self.speed
        self.x += velX
        if self.x + self.size > mapSize[0]:
            self.x = mapSize[0] - self.size
        if self.x - self.size < 0:
            self.x = self.size
        
        velY = math.sin(angle) * self.speed
        self.y += velY
        if self.y + self.size > mapSize[1]:
            self.y = mapSize[1] - self.size
        if self.y - self.size < 0:
            self.y = self.size

        pygame.time.delay(5)

    def draw(self, middle, window, ratio):
        size = window.get_size()
        pos = (middle[0] - self.x + size[0] / 2, middle[1] - self.y + size[1] / 2)
        pygame.draw.circle(window, self.color, pos , self.size / ratio)
        font = pygame.font.Font(None, int(18 / ratio))
        text_surface = font.render(self.name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center = pos)
        window.blit(text_surface, text_rect)
        pygame.display.update()

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
    
    def update(self):
        self.size = 4 + math.sqrt(self.mass) * 6
        self.speed = 2 * (self.mass ** -0.5)

    def to_json(self):
        data = [self.x, self.y, self.color, '', self.mass, self.name]
        return json.dumps(data)
    
def from_json(data):
    data = json.loads(data)
    new = player(data[0], data[1], data[2], data[3], data[4], data[5])
    return new
