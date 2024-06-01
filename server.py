import socket
import _thread
import json
import math
import generate
import random
import player
import pygame
from settings import *

End = 'END_OF_TRANSMITION'
def recvall(the_socket, bufferSize, data):
    if End in data:
        value =  json.loads(data[:data.find(End)])
        data = data[data.find(End) + 18:]
        return (value, data)

    while True:
            prev = data
            data = data + the_socket.recv(bufferSize).decode('utf8')
            if(data == prev):
                raise Exception("connection killed")
            if End in data:
                value =  json.loads(data[:data.find(End)])
                data = data[data.find(End) + 18:]
                return (value, data)

def checkInter(conn, player, clientToPlayer, entety, pelletsList, playersList, playerType = False):
    if entety.eaten(player):
        if playerType:
            try:
                conn2 = entety.conn
                clientToPlayer.pop(conn2, None)
                conn2.close()
                playersList.remove(entety)
            except Exception as e:
                print(e)
                return True
        else:
            pelletsList.remove(entety)
        return True
    return False

def broadcast(message, conn):
    message = bytes(message + End, encoding='utf8')
    conn.sendall(message)

def handleError(conn, addr, clientToPlayer, playersList, listOfClients):
    print (addr[0] + " disconnected")
    try:
        player = clientToPlayer[conn]
        clientToPlayer.pop(conn, None)
        listOfClients.remove(conn)
        playersList.remove(player)
        conn.close()
    except:
        return
        

def clientThread(conn, addr, listOfClients, pelletsList, clientToPlayer, playersList):
    try:
        clock = pygame.time.Clock()
        name, data= recvall(conn, 4096, '')
        newPlayer(conn, playersList, clientToPlayer, name)
        while True:
            data = move(conn, clientToPlayer, playersList, data)
            sendDataAndInter(conn, pelletsList, clientToPlayer, playersList)
            clock.tick(30)
    except:
        handleError(conn, addr, clientToPlayer, playersList, listOfClients)
        return -1


def move(conn, clientToPlayer, playersList, data):
    pos, remaine = recvall(conn, 4096, data)

    player = clientToPlayer[conn]
    angle = math.atan2(VIEW_SIZE[1] / 2 - pos[1], VIEW_SIZE[0] / 2 - pos[0])
    clientToPlayer.pop(conn, player)
    playersList.remove(player)
    if (pos[0] - VIEW_SIZE[0] / 2) ** 2 + (pos[1] - VIEW_SIZE[1] / 2) ** 2 > player.size ** 2:
        player.move(angle, MAP_SIZE)
    clientToPlayer[conn] = player
    playersList.append(player)
    return remaine

def sendDataAndInter(conn, entetyList, clientToPlayer, playersList):
    sendingPellets = []
    sendingPlayers = []
    player = clientToPlayer[conn]
    ratio = findRatio(player)
    middle = (player.x, player.y)
    for entety in entetyList:
        if not entety.inScreen(middle, ratio, VIEW_SIZE):
            continue
        if not checkInter(conn, player, clientToPlayer, entety, entetyList, playersList):
            sendingPellets.append(entety.to_json())
    
    for entety in playersList:
        if not entety.inScreen(middle, ratio, VIEW_SIZE):
            continue
        if not checkInter(conn, player, clientToPlayer, entety, entetyList, playersList, True):
            sendingPlayers.append(entety.to_json())
    message = json.dumps((player.to_json(), sendingPellets, sendingPlayers))
    broadcast(message, conn)

def findRatio(player):    
    ratio = 1
    maxDiff = 2*player.size
    if maxDiff > 300:
        ratio = maxDiff / 300
    
    return ratio

def newPlayer(conn, playersList, clientToPlayer, name):
    size = 4 + math.sqrt(10) * 6
    x = random.randint(int(size), int(MAP_SIZE[0] - size))
    y = random.randint(int(size), int(MAP_SIZE[1] - size))
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    new = player.player(x, y, (r, g, b), conn, name)
    playersList.append(new)
    clientToPlayer[conn] = new

def keepPelletsNum(pelletsList):
    while True:
        generate.generatePellets(pelletsList)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((IP_ADDRESS, PORT))
    server.listen(10)
    listOfClients = []

    pelletsList = []
    clientToPlayer = {}
    playersList = []
  
    _thread.start_new_thread(keepPelletsNum, (pelletsList,))
    while True:
        conn, addr = server.accept()
        listOfClients.append(conn)
        print (addr[0] + " connected")
        _thread.start_new_thread(clientThread, (conn, addr, listOfClients, pelletsList, clientToPlayer, playersList))
    
    for conn in list_of_clients:
        conn.close()

    server.close()

main()
