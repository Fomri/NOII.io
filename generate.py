import pellet
from settings import *
import random

def generatePellets(pelletsList):
    while len(pelletsList) < PELLETS_NUM:
        x = random.randint(15, MAP_SIZE[0] - 15)
        y = random.randint(15, MAP_SIZE[1] - 15)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)
        new = pellet.pellet(x, y, color)
        pelletsList.append(new)  
