import pygame
import math

class virus:
    def __init__(self, x, y, color = (0, 255, 0), mass = 100):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(self.mass) * 6

    def draw(self, middle, window, ratio):
        size = window.get_size()
        if self.x < middle[0] + size[0] / 2 and self.x > middle[0] - size[0] / 2:
            if self.y < middle[1] + size[1] / 2 and self.y < middle[1] - size[1] / 2:
                virusImage = pygame.image.load("pictures/virus.png")
                virusImage = pygame.transform.scale(virusImage, (self.size, self.size))
                window.blit(virusImage, (middle[0] - self.x + size[0], middle[1] - self.y + size[1]))

    def eaten(self, player):
        if virus.mass <= 0.8 * player.mass:
            distance = (player.x - self.x) ** 2 + (player.y - self.y) ** 2
            if distance <= (player.size - self.size) ** 2:
                player.mass += self.mass
                player.update()
                return True
        
        return False
