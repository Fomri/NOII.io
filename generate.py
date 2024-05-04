import pellet
from settings import *
import random

def generate_pellets(pelletsList){
    while pelletsList.len() < PELLETS_NUM:
        x = random.randint(0, MAP_SIZE)
        y = random.randint(0, MAP_SIZE)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)
        new = pellet(x, y, color)
        pelletsList.append(new)    
}
