import thread
import random
import time
import socket


host = 'localhost'
port = 26007

syncSocket = socket.socket()
syncSocket 

syncSocket.listen(10)

socketList = str()

while True:
    workerSocket, address = syncSocket.accept()
    adr = workerSocket.recv(1024)
    socketList+=adr[0]+'|'+adr[1]+','
    print(socketList)
