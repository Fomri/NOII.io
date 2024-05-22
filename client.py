import pygame
from settings import *
import socket
import player
import pellet
import json
import _thread

End = 'END_OF_TRANSMITION'
data = ''
def recvall(the_socket, bufferSize):
    total_data=[]
    global data
    if End in data:
        total_data.append(data[:data.find(End)])
        data = data[data.find(End) + 18:]
        return json.loads(''.join(total_data))

    while True:
            data = data + the_socket.recv(bufferSize).decode('utf8')
            if End in data:
                total_data.append(data[:data.find(End)])
                data = data[data.find(End) + 18:]
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
    return json.loads(''.join(total_data))


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
    screen = pygame.display.set_mode(VIEW_SIZE)
    screen.fill((255, 255, 255))
    pygame.display.update()
    pygame.init()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.connect((IP_ADDRESS, PORT)) 

    server.sendall(bytes(json.dumps(name) + End, encoding = 'utf8'))

    pos = (VIEW_SIZE[0] / 2, VIEW_SIZE[1] / 2)
    server.sendall(bytes(json.dumps(pos) + End, encoding='utf8'))
    pelletsList = []
    while True:
        try:
            p, playersList, pelletsList = updateData(server)
            ratio = findRatio(p)
            drawBorders(screen, (p.x, p.y))
            middle = (p.x, p.y)
            for entety in pelletsList:
                entety.draw(middle, screen, ratio)
            for entety in playersList:
                entety.draw(middle, screen, ratio)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            pos = pygame.mouse.get_pos()
            server.sendall(bytes(json.dumps(pos) + End, encoding='utf8'))
            pygame.display.update()
            screen.fill((255, 255, 255))

        except Exception as e:
            print(e)
            break

