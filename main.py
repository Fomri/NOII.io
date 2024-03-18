import pygame
import math

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.update()
pygame.init()

mapSize = 10000

class player:
    def __init__(self, x, y, color, mass, name = ""):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.size = 4 + math.sqrt(mass) * 6
        self.speed = 2.2 * (mass ** (-0.439))
        self.name = name
    
    def move(self, angle):
        velX = math.sin(angle) * self.speed
        if angle < 180:
            velX = -velX
        self.x += velX
        
        velY = math.cos(angle) * self.speed
        if angle < 180:
            velY = -velY
        self.y += velY

        pygame.time.delay(5)

    def draw(self, window, size):
        pygame.draw.circle(window, self.color, (size[0] / 2, size[1] / 2), self.size)

def drawGrid(window, x, y, blockSize, size):
    shiftX = x - (blockSize * int(int(x) / blockSize))
    shiftY = y - (blockSize * int(int(y) / blockSize))

    for i in range(0, size[0], blockSize):
        pygame.draw.line(window, (0, 0, 0), (shiftX + i, 0), (shiftX + i, size[1]))
    
    for i in range(0, size[1], blockSize):
        pygame.draw.line(window, (0, 0, 0), (0, shiftY + i), (size[0], shiftY + i))


p = player(mapSize / 2, mapSize / 2, (0, 255, 255), 20)

run = True
while run:
    drawGrid(screen, p.x, p.y, 20, size)
    p.draw(screen, size)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[0] - size[0] / 2, pos[1] - size[1] / 2)
    if (pos[0] - 250) ** 2 + (pos[1] - 250) ** 2 > p.size ** 2:
        p.move(angle)

    pygame.display.update()
    screen.fill((255, 255, 255))
