import socket
import _thread
import json
import math
import generate
from settings import *

def sendDataAndInter(conn, addr, pelletsList, clientToPlayer, playersList):
    sendingData = []
    for entety in pelletsList:
        if not checkInter(addr, clientToPlayer, entety, pelletsList, playersList):
            sendingData.append(entety)
    
    for blob in playersList:
        if not checkInter(addr, clientToPlayer, blob, pelletsList, playersList, True):
            sendingData.append(blob)

    broadcast(json.dumps(sendingData), conn)

def checkInter(addr, clientToPlayer, entety, pelletsList, playersList, playerType = False):
    player = clientToPlayer[addr[0]]
    if entety.eaten(player):
        pelletsList.remove(entety)
        if playerType:
            addr2 = entety.addr
            clientToPlayer.pop(addr2[0], entety)
            playersList.remove(entety)
        else:
            pelletsList.remove(entety)
        clientToPlayer[addr[0]] = player
        return True
    return False

def broadcast(message, conn):
    try:
        conn.send(message.encode())
    except:
        conn.close()
        return -1

def clientthread(conn, addr, listOfClients, pelletsList, clientToPlayer, playersList):
    while True:
        if sendDataAndInter(conn, pelletsList, clientToPlayer, playersList) == -1:
            player = clientToPlayer[addr[0]]
            clientToPlayer.pop(addr[0], player)
            listOfClients.remove(conn)
            playersList.remove(player)
            conn.close()
            return -1

def move(conn, addr, clientToPlayer, playersList):
    pos = json.load(conn.recv(1024).decode())
    middleScreen = (clientToPlayer[addr[0]].x, clientToPlayer[addr[0]].y)

    player = clientToPlayer[addr[0]]
    y = player.y - middleScreen[1]
    x = player.x - middleScreen[0]
    angle = math.atan2(VIEW_SIZE[1] / 2 - pos[1] - y, VIEW_SIZE[0] / 2 - pos[0] - x)
    clientToPlayer.pop(addr[0], player)
    playersList.remove(player)
    if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 > player.size ** 2:
        player.move(angle, MAP_SIZE)
    clientToPlayer[addr[0]] = player

def newPlayer(conn, addr, playersList, clientsToPlayer){
    x = random.randint(0, MAP_SIZE)
    y = random.randint(0, MAP_SIZE)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    new = player.player(x, y, (r, g, b), addr)
    playersList.append(new)
    clientToPlayer[conn] = new
}

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((IP_ADDRESS, PORT))
    server.listen(10)
    list_of_clients = []

    pelletsList = []
    clientToPlayer = {}
    playersList = []

    generate.generatePellets(pelletsList)
    
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print (addr[0] + " connected")
        newPlayer(conn, addr, playersList, clientToPlayers)
        _thread.start_new_thread(clientthread,(conn, pelletsList, clientToPlayer, playersList))
        generate.generatePellets(pelletsList)
    
    for conn in list_of_clients:
        conn.close()

    server.close()

main()
