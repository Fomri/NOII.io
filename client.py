import pygame
import math
from player import *

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.update()
pygame.init()

mapSize = 2000
blockSize = 40

def drawGrid(window, player, block_size, size):
    shiftX = player.x - block_size * int(player.x / block_size)
    shiftY = player.y - (block_size * int(player.y / block_size))
    
    for i in range(0, size[0], block_size):
        pygame.draw.line(window, (128,128,128), (shiftX + i, 0), (shiftX + i, size[1]))
    
    for i in range(0, size[1], block_size):
        pygame.draw.line(window, (128,128,128), (0, shiftY + i), (size[0], shiftY + i))


p = player(mapSize / 2, mapSize / 2, (0, 255, 255), 20)

while True:
    drawGrid(screen, p, blockSize, size)
    p.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[1] - size[1] / 2, pos[0] - size[0] / 2)
    if (pos[0] - 250) ** 2 + (pos[1] - 250) ** 2 > p.size ** 2:
        p.move(angle, mapSize)

    pygame.display.update()
    screen.fill((255, 255, 255))