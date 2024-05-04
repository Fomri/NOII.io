import pygame
import math
import json

class player:
    def __init__(self, x, y, color, addr, mass = 20, name = ""):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(mass) * 6
        self.speed = 2 * (mass ** -0.5)
        self.name = name
        self.addr = addr[0]

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

    def update(self):
        self.size = 4 + math.sqrt(self.mass) * 6
        self.speed = 2 * (self.mass ** -0.5)

    def to_json(self):
        data = [self.x, self.y, self.color, self.mass, self.size, self.speed, self.name]
        return json.dumps(data)
