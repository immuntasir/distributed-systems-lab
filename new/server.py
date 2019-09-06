import socket
import threading
import time
from threading import Thread
import pickle

SERVER_HOST = 'localhost'
SERVER_PORT = 7777
out_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_s.bind((SERVER_HOST, SERVER_PORT))

clock = 1

connections = []
conn_addresses = []
new_connections = []
new_conn_addresses = []

def send_addresses (threadName = 'Naam chilo na') :
    global connections
    global new_connections
    global conn_addresses
    global new_conn_addresses
    while 1 == 1:
        time.sleep(1)
        new_connections = []
        new_conn_addresses = []
        data=pickle.dumps(conn_addresses)
        for connection_itr in range(len(connections)):
            connection = connections[connection_itr]
            connection_addr = conn_addresses[connection_itr]
            try:
               print(data)
               connection.send(data)
               new_connections.append(connection)
               new_conn_addresses.append(connection_addr) 
            except:
                print(connection, 'removed successfully')
        connections = new_connections
        conn_addresses = new_conn_addresses

Thread(target=send_addresses, args=('I am Groot', )).start()
    
while 1==1:
    out_s.listen(5)
    conn, addr = out_s.accept()
    input_data = conn.recv(1024)
    data = input_data.decode("utf8").rstrip()
    connections.append(conn)
    print([addr[0], data])
    conn_addresses.append((addr[0], data))
    print('Connected with ', conn, addr)
    pass
