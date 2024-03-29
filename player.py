import pygame
import math

class player:
    def __init__(self, x, y, color, mass, name = ""):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(mass) * 6
        self.speed = 2 * (mass ** -0.5)
        self.name = name

    def move(self, angle, mapSize):
        velX = math.cos(angle) * self.speed
        self.x -= velX
        if self.x + 3 * self.size > mapSize:
            self.x = mapSize - 3 * self.size
        if self.x < 0:
            self.x = 0
        
        velY = math.sin(angle) * self.speed
        self.y -= velY
        if self.y + 2 * self.size > mapSize:
            self.y = mapSize - 2 * self.size
        if self.y < 0:
            self.y = 0

        pygame.time.delay(5)

    def draw(self, window):
        size = window.get_size()
        pygame.draw.circle(window, self.color, (size[0] / 2, size[1] / 2), self.size)
        font = pygame.font.Font(None, 18)
        text_surface = font.render(self.name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center = (size[0] / 2, size[1] / 2))
        window.blit(text_surface, text_rect)
        pygame.display.update()

    def update(self):
        self.size = 4 + math.sqrt(self.mass) * 6
        self.speed = 2 * (self.mass ** -0.5)