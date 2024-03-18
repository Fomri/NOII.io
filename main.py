import pygame
import math

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.update()
pygame.init()

mapSize = 10000

class player:
    def __init__(self, x, y, color, mass):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.speed = 2.2 * (mass ** (-0.439))
    
    def move(self, angle):
        velX = math.sin(angle) * self.speed
        if angle < 180:
            velX = -velX
        self.x += velX
        
        velY = math.cos(angle) * self.speed
        if angle < 180:
            velY = -velY
        self.y += velY

        pygame.time.delay(2)

    def draw(self, window, size):
        pygame.draw.circle(window, self.color, (size[0] / 2, size[1] / 2), self.mass * 1.5)

def drawGrid(window, x, y, blockSize, size):
    shiftX = x - (blockSize * int(int(x) / blockSize))
    shiftY = y - (blockSize * int(int(y) / blockSize))

    for i in range(0, size[0], blockSize):
        pygame.draw.line(window, (0, 0, 0), (shiftX + i, 0), (shiftX + i, size[1]))
    
    for i in range(0, size[1], blockSize):
        pygame.draw.line(window, (0, 0, 0), (0, shiftY + i), (size[1], shiftY + i))


p = player(mapSize / 2, mapSize / 2, (0, 255, 255), 20)

while True:
    drawGrid(screen, p.x, p.y, 20, size)
    p.draw(screen, size)
    relPosX = p.x - (size[0] * int(int(p.x) / size[0]))
    relPosY = p.y - (size[1] * int(int(p.y) / size[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[0] - size[0] / 2, pos[1] - size[1] / 2)
    if (pos[0] - relPosX) ** 2 + (pos[1] - relPosY) ** 2 > p.mass ** 2:
        p.move(angle)

    pygame.display.update()
    screen.fill((255, 255, 255))