import socket
import threading
import time
from threading import Thread
HOST = 'localhost'
PORT = 7770


BUFFER = []
printed = 1
def print_output(threadName, connection):
    global printed
    while 1 == 1:
        client_input = connection.recv(5120)
        data = client_input.decode("utf8").rstrip()
        if 'BUFFER OVERFLOW' in data:
            print(data)
        else:
            print(str(printed) + '. ' + data)
            printed += 1
            del BUFFER[0]

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
Thread(target=print_output, args=('F.R.I.D.A.Y.', conn)).start()


for i in range(50):
    conn.send(str(i).encode('utf8'))
    conn.send('$'.encode('utf8'))
    BUFFER.append(str(i))
    time.sleep(.25)

while 7 == 7:
    input_string = input()
    conn.send(input_string.encode('utf8'))
    conn.send('$'.encode('utf8'))
    BUFFER.append(input_string)
