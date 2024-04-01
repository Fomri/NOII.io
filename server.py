import socket
from _thread import *
import json
import math

VIEW_SIZE = (500, 500)
MAP_SIZE = (2000, 2000)

def sendDataAndInter(conn, pelletsList, virusList, spawnersList, playerToClient, clientToPlayers, playersList):
    for pellet in pelletsList:
        if not checkInter(conn, clientToPlayers, playerToClient, pellet, pelletsList):
            if broadcast(pellet.to_json(), conn) == -1:
                return -1

    for virus in virusList:
        if not checkInter(conn, clientToPlayers, playerToClient, virus, virusList):
            if broadcast(virus.to_json(), conn) == -1:
                return -1

    for spawner in spawnersList:
        if not checkInter(conn, clientToPlayers, playerToClient, spawner, spawnersList):
            if broadcast(spawner.to_json(), conn) == -1:
                return -1
    
    for player in playersList:
        if not checkInter(conn, clientToPlayers, playerToClient, player, playersList, True):
           if broadcast(player.to_json(), conn) == -1:
                return -1

def checkInter(conn, clientToPlayers, playerToClient, entety, entetyList, playerType = False):
    for player in clientToPlayers[conn]:
        if entety.eaten(player):
            entetyList.remove(entety)
            if playerType:
                client = playerToClient[entety]
                clientToPlayers[client].remove(entety)
                playerToClient.pop(entety, None)
            return True
    return False

def broadcast(message, conn):
    try:
        conn.send(message.encode())
    except:
        conn.close()
        return -1

def clientthread(conn, pelletsList, virusList, spawnersList, playerToClient, clientToPlayers, playersList):
    while True:
        if sendDataAndInter(conn, pelletsList, virusList, spawnersList, playerToClient, clientToPlayers, playersList) == -1:
            return -1

def move(conn, playerToClient, clientToPlayers, playersList):
    pos = json.load(conn.recv(1024).decode())
    middleScreen = [0, 0]
    for player in clientToPlayers[conn]:
        middleScreen[0] += player.x
        middleScreen[1] += player.y
    middleScreen[0] /= len(clientToPlayers[conn])
    middleScreen[1] /= len(clientToPlayers[conn])
    for blob in clientToPlayers[conn]:
        y = blob.y - middleScreen[1]
        x = blob.x - middleScreen[0]
        angle = math.atan2(pos[1] - VIEW_SIZE[1] / 2 - y, VIEW_SIZE[0] / 2 - pos[0] - x)
        clientToPlayers[conn].remove(blob)
        playerToClient.pop(blob, None)
        playersList.remove(blob)
        blob.move(angle, MAP_SIZE)
        clientToPlayers[conn].append(blob)
        playerToClient[blob] = conn
        playersList.append(blob)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    IP_address = "127.0.0.1"
    Port = 8080

    server.bind((IP_address, Port))
    server.listen(10)
    list_of_clients = []

    pelletsList = []
    virusList = []
    spawnersList = []
    playerToClient = {}
    clientToPlayers = {}
    playersList = []

    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print (addr[0] + " connected")
        start_new_thread(clientthread,(conn, pelletsList, virusList, spawnersList, playerToClient, clientToPlayers, playersList))

    conn.close()
    server.close()

main()