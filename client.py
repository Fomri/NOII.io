import pygame
from settings import *
import socket
import player
import pellet
import json

End = 'END_OF_TRANSMITION'
data = ''
def recvall(the_socket, bufferSize):
    global data
    if End in data:
        value =  json.loads(data[:data.find(End)])
        data = data[data.find(End) + 18:]
        return value

    while True:
            data = data + the_socket.recv(bufferSize).decode('utf8')
            if(data == ''):
                raise Exception("connection closed")
            if End in data:
                value =  json.loads(data[:data.find(End)])
                data = data[data.find(End) + 18:]
                return value


def drawBorders(window, middle):
    upMax = min(middle[1] - MAP_SIZE[1] + VIEW_SIZE[1] / 2, VIEW_SIZE[1])
    downMin = max(middle[1] + VIEW_SIZE[1] / 2, 0)
    leftMax = min(middle[0] - MAP_SIZE[0] + VIEW_SIZE[0] / 2, VIEW_SIZE[0])
    rightMin = max(middle[0] + VIEW_SIZE[0] / 2, 0)
    pygame.draw.line(window, (0, 0, 0), (middle[0] + VIEW_SIZE[0] / 2, downMin), (middle[0] + VIEW_SIZE[0] / 2, upMax))
    pygame.draw.line(window, (0, 0, 0), (rightMin, middle[1] + VIEW_SIZE[1] / 2), (leftMax, middle[1] + VIEW_SIZE[1] / 2))
    pygame.draw.line(window, (0, 0, 0), (middle[0] - MAP_SIZE[0] + VIEW_SIZE[0] / 2, downMin), (middle[0] - MAP_SIZE[0] + VIEW_SIZE[0] / 2, upMax))
    pygame.draw.line(window, (0, 0, 0), (rightMin, middle[1] - MAP_SIZE[1] + VIEW_SIZE[1] / 2), (leftMax, middle[1] - MAP_SIZE[1] + VIEW_SIZE[1] / 2))

def findRatio(player):    
    ratio = 1
    maxDiff = 2*player.size
    if maxDiff > 300:
        ratio = maxDiff / 300
    
    return ratio 

def updateData(server):
    message = recvall(server, 4096)
    p = player.from_json(message[0])
    recieved = message[1]
    pelletsList = []
    for entety in recieved:
        pelletsList.append(pellet.from_json(entety))
    recieved = message[2]
    playersList = []
    for entety in recieved:
        playersList.append(player.from_json(entety))

    playersList = sorted(playersList, key = sortPlayersKey)
    return (p, playersList, pelletsList)

def sortPlayersKey(player):
    return player.size

def main(name):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(VIEW_SIZE)
    pygame.init()

    off_screen_surface = pygame.Surface(VIEW_SIZE)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.connect((IP_ADDRESS, 8088)) 

    server.sendall(bytes(json.dumps(name) + End, encoding = 'utf8'))

    pos = (VIEW_SIZE[0] / 2, VIEW_SIZE[1] / 2)
    server.sendall(bytes(json.dumps(pos) + End, encoding='utf8'))
    pelletsList = []
    running = True
    while running:
        try:
            p, playersList, pelletsList = updateData(server)
            off_screen_surface.fill((255, 255, 255))
            ratio = findRatio(p)
            drawBorders(off_screen_surface, (p.x, p.y))
            middle = (p.x, p.y)
            for entety in pelletsList:
                entety.draw(middle, off_screen_surface, ratio)
            for entety in playersList:
                entety.draw(middle, off_screen_surface, ratio)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    server.close()
                    break
            pos = pygame.mouse.get_pos()
            server.sendall(bytes(json.dumps(pos) + End, encoding='utf8'))
            screen.blit(off_screen_surface, (0, 0))
            pygame.display.update()
            clock.tick(30)

        except Exception as e:
            print(e)
            server.close()
            break
        
    pygame.quit()
