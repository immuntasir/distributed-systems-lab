import socket
import threading
import time
from threading import Thread
import pickle
HOST = '192.168.43.10'
PORT = 7777

import random

BUFFER = []
printed = 1

IN_HOST = '192.168.43.184'
IN_PORT = 8082

clock = 1

dict_of_addresses = {}
connections = []

def clock_counter(threadName):
    global clock
    random_interval = random.randint(100, 500) / 100
    while 1 == 1:
        time.sleep(random_interval)
        clock = clock+1
        
def update_clock(threadName):
    global clock
    out_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    out_s.bind((IN_HOST, IN_PORT))
    while 1 == 1:
        print('Waiting for connection')
        out_s.listen(5)
        conn2, addr2 = out_s.accept()
        print('Connection established with', addr2)
        input_data = conn2.recv(1024)
        data = input_data.decode("utf8").rstrip()
        print('Got clock time:', int(data))
        print('Old Clock Time:', clock)
        clock = max(clock, int(data)) + 1
        print('New clock time:' , clock)
        
def send_clock(threadName):
    global clock
    random_interval = random.randint(100, 500) / 100
    while 1 == 1:
        time.sleep(random_interval)
        print('Total number of connections:', len(connections))
        for connection_worker in connections:
            if connection_worker[0] == IN_HOST and IN_PORT == int(connection_worker[1]):
                continue;
            print('Connecting with', connection_worker)
            try:
                new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_conn.connect((connection_worker[0], int(connection_worker[1])))
                new_conn.send(str(clock).encode('utf8'))
                new_conn.close()
            except:
                print('Exception')
def active_process_list(threadName, connection):
    global connections
    while 1 == 1:
        client_input = connection.recv(5120)
        data = pickle.loads(client_input)
        print(data)
        connections = data            

print('Enter port address:')
IN_PORT = int(input())
print('Enter clock:')
clock = int(input())

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
Thread(target=clock_counter, args=('J.A.R.V.I.S.', )).start()
Thread(target=update_clock, args=('J.O.C.O.S.T.A', )).start()
conn.send(str(IN_PORT).encode('utf8'))



Thread(target=active_process_list, args=('F.R.I.D.A.Y.', conn)).start()
Thread(target=send_clock, args=('V.I.S.I.O.N', )).start()









