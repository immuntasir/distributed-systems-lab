import socket
import threading
import time
from threading import Thread
import pickle
HOST = 'localhost'
PORT = 7777

import random

BUFFER = []
printed = 1

IN_HOST = '127.0.0.1'
IN_PORT = 8082

clock = 1

dict_of_addresses = {}

def clock_counter(threadName):
    global clock
    random_interval = random.randint(50, 100) / 100
    while 1 == 1:
        time.sleep(random_interval)
        clock = clock+1

def send_clock_time (threadName, connection):
    global clock
    random_interval = random.randint(70, 100)/100
    print('sleep time', random_interval)
    try:
        while 1 == 1:
            time.sleep(random_interval)
            print('Sending clock time', clock)
            connection.send(str(clock).encode('utf8'))
    except:
        pass
def get_clock_time(threadName, connection):
    global clock
    try:
        while 1 == 1:
            input_data = connection.recv(1024)
            data = input_data.decode("utf8").rstrip()
            print('Clock time at', connection, ': ', data)
            clock = int(data) + 1
            print('Clock time updated to', clock)
    except:
        pass
def active_process_list(threadName, connection):
    while 1 == 1:
        client_input = connection.recv(5120)
        data = pickle.loads(client_input)
        print(data)
        for conn in data:
            print(conn[0], conn[1], IN_HOST, IN_PORT)
            if conn[0] != IN_HOST or int(conn[1]) != IN_PORT:
                print('Connecting with a new worker')
                try:
                    host = conn[0]
                    port = int(conn[1])
                    new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_conn.connect((HOST, PORT))
                    Thread(target=send_clock_time, args=('I am Iron Man', new_conn)).start()                
                    dict_of_addresses[conn[0]] = 1
                except: 
                    pass            
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
conn.send(str(IN_PORT).encode('utf8'))
Thread(target=active_process_list, args=('F.R.I.D.A.Y.', conn)).start()
Thread(target=clock_counter, args=('J.A.R.V.I.S.', )).start()


out_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_s.bind((IN_HOST, IN_PORT))
while 1==1:
    print('Waiting for connection')
    out_s.listen(5)
    conn2, addr2 = out_s.accept()
    print('Connection established with', addr)
    Thread(target=get_clock_time, args=('I am Groot', conn2)).start()
