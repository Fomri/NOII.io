import socket
import _thread
import json
import math
import generate
import random
import player
from settings import *

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
        message = bytes(message + End, encoding='utf8')
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
        

def clientThread(conn, addr, listOfClients, pelletsList, clientToPlayer, playersList):
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
    pos = recvall(conn, 4096)

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
    return broadcast(message, conn)

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
        name = recvall(conn, 4096)
        newPlayer(conn, playersList, clientToPlayer, name)
        _thread.start_new_thread(clientThread, (conn, addr, listOfClients, pelletsList, clientToPlayer, playersList))
    
    for conn in list_of_clients:
        conn.close()

    server.close()

main()
