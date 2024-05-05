import pygame
import math
import player
from settings import *
import socket

screen = pygame.display.set_mode(VIEW_SIZE)
screen.fill((255, 255, 255))
pygame.display.update()
pygame.init()

blockSize = 40

def drawGrid(window, player, block_size, size):
    shiftX = player.x - player.size - block_size * int((player.x - player.size) / block_size)
    shiftY = player.y - player.size - block_size * int((player.y - player.size) / block_size)
    
    i = 0
    while i < size[0]:
        pygame.draw.line(window, (128,128,128), (shiftX + i, 0), (shiftX + i, size[1]))
        i += block_size
    
    i = 0
    while i < size[1]:
        pygame.draw.line(window, (128,128,128), (0, shiftY + i), (size[0], shiftY + i))
        i += block_size

def findMiddle(player):
    middleScreen = [0, 0]
    for blob in player:
        middleScreen[0] += blob.x
        middleScreen[1] += blob.y
    middleScreen[0] /= len(player)
    middleScreen[1] /= len(player)
    return middleScreen

def findRatio(player):
    minX = player.x - player.size
    minY = player.y - player.size
    maxX = player.x + player.size
    maxY = player.y + player.size
    
    ratio = 1
    maxDiff = max(maxX - minX, maxY - minY)
    if maxDiff > 300:
        ratio = maxDiff / 300
    
    return ratio

p = player.player(MAP_SIZE[0] / 2, MAP_SIZE[1] / 2, (0, 255, 255), 20)

while True:
    ratio = findRatio(p)
    drawGrid(screen, p[0], blockSize / ratio, VIEW_SIZE)
    p.draw(findMiddle(p), screen, ratio)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    
    pos = pygame.mouse.get_pos()
    angle = math.atan2(VIEW_SIZE[1] / 2 - pos[1], VIEW_SIZE[0] / 2 - pos[0])
    p[0].move(angle, MAP_SIZE)
    pygame.display.update()
    screen.fill((255, 255, 255))
