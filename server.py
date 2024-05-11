import socket
import _thread
import json
import math
import generate
import random
import player
from settings import *


def checkInter(conn, player, clientToPlayer, entety, pelletsList, playersList, playerType = False):
    playersList.remove(player)
    clientToPlayer.pop(conn)
    if entety.eaten(player):
        playersList.append(player)
        clientToPlayer[conn] = player
        if playerType:
            try:
                conn2 = entety.conn
                clientToPlayer.pop(conn2, None)
                conn2.close()
                playersList.remove(entety)
            except:
                return True
        else:
            pelletsList.remove(entety)
        return True
    playersList.append(player)
    clientToPlayer[conn] = player
    return False

def broadcast(message, conn):
    try:
        message = message + b'END_OF_TRANSMITION'
        conn.sendall(message)
        return 0
    except Exception as e:
        print(e)
        return -1

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
        

def  clientThread(conn, addr, listOfClients, pelletsList, clientToPlayer, playersList):
    while True:
        try:
            move(conn, clientToPlayer, playersList)
        except:
            handleError(conn, addr, clientToPlayer, playersList, listOfClients)
            return -1
        
        if sendDataAndInter(conn, pelletsList, clientToPlayer, playersList) == -1:
            handleError(conn, addr, clientToPlayer, playersList, listOfClients)
            return -1

def move(conn, clientToPlayer, playersList):
    pos = json.loads(conn.recv(4096).decode('utf8'))

    player = clientToPlayer[conn]
    angle = math.atan2(VIEW_SIZE[1] / 2 - pos[1], VIEW_SIZE[0] / 2 - pos[0])
    clientToPlayer.pop(conn, player)
    playersList.remove(player)
    if (pos[0] - VIEW_SIZE[0] / 2) ** 2 + (pos[1] - VIEW_SIZE[1] / 2) ** 2 > player.size ** 2:
        player.move(angle, MAP_SIZE)
    clientToPlayer[conn] = player
    playersList.append(player)

def sendDataAndInter(conn, entetyList, clientToPlayer, playersList):
    sendingPellets = []
    sendingPlayers = []
    player = clientToPlayer[conn]
    for entety in entetyList:
        if not checkInter(conn, player, clientToPlayer, entety, entetyList, playersList):
            sendingPellets.append(entety.to_json())
    
    for blob in playersList:
        if not checkInter(conn, player, clientToPlayer, blob, entetyList, playersList, True):
            sendingPlayers.append(blob.to_json())
    
    message = json.dumps((player.to_json(), sendingPellets, sendingPlayers))
    return broadcast(bytes(message, encoding='utf8'), conn)

def newPlayer(conn, playersList, clientToPlayer):
    size = 4 + math.sqrt(10) * 6
    x = random.randint(int(size), int(MAP_SIZE[0] - size))
    y = random.randint(int(size), int(MAP_SIZE[1] - size))
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    new = player.player(x, y, (r, g, b), conn)
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
        newPlayer(conn, playersList, clientToPlayer)
        _thread.start_new_thread(clientThread, (conn, addr, listOfClients, pelletsList, clientToPlayer, playersList))
    
    for conn in list_of_clients:
        conn.close()

    server.close()

main()
