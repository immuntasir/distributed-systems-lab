# Echo client program
import socket
import threading
import time
from threading import Thread

threadLock = threading.Lock()
threadLock2 = threading.Lock()

HOST = 'localhost'   
PORTS = [11110, 11111, 11112]    
flag = [1] * len(PORTS)   
DELAY = .5
SERVER_HOST = 'localhost'
SERVER_PORT = 7770
out_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_s.bind((SERVER_HOST, SERVER_PORT))

MAX_BUFFER_LENGTH = 150

BUFFER = []
BUFFER_CLIENT = []
BUFFER_RESULTS = []
BUFFER_RESULTS_CLIENT = []
BUFFER_INPUTS = []
dict_of_workers = {}

number_of_workers = 0

def select_worker():
    #print('available workers: ', dict_of_workers)
    workers = sorted(list(dict_of_workers.values()), key = lambda k : k['count'])
    for worker in workers:
        if flag[worker['index']] == 1:
            return worker
    return -1     

def distribute_work(threadName):
    global threadLock
    global threadLock2
    while 1 == 1:
        time.sleep(DELAY)
        print('Size of buffer:', len(BUFFER))
        if len(BUFFER) != 0:
            if threadLock2.acquire(blocking = False):
                threadLock.acquire(blocking = 1)
                print('Lock1 acquired by', threadName)
                data = BUFFER[0]
                client = BUFFER_CLIENT[0]
                
                selected_worker = select_worker()
                if selected_worker == -1:
                    print('Could not avail any worker.')
                    pass
                else:
                    print('Selected worker index:', selected_worker['index'])
                    print('server: Sending data to the selected worker: ', selected_worker)
                    print('pending ', client, 'added to', selected_worker['index'])
                    
                    
                    selected_worker['connection'].send(str(data).encode("utf8"))
                    selected_worker['connection'].send('$'.encode("utf8"))
                    
                    worker_input = selected_worker['connection'].recv(5120)
                    data = worker_input.decode("utf8").rstrip()
                    
                    print('JARVIS:')
                    print('||| RESPONSE FROM WORKER |||')
                    print('index =', selected_worker['index'])
                    print('Data from', selected_worker['connection'], ': ', data)      
                   
                    if 'BUFFER LIMIT REACHED' in data:
                        flag[selected_worker['index']] = 0
                        BUFFER_RESULTS_CLIENT[selected_worker['index']].append(client)
                        BUFFER_INPUTS[selected_worker['index']].append(str(data))
                        selected_worker['count'] += 1
                        del BUFFER[0]
                        del BUFFER_CLIENT[0]
                        
                    elif 'BUFFER ALRIGHT' in data:
                        BUFFER_RESULTS_CLIENT[selected_worker['index']].append(client)
                        BUFFER_INPUTS[selected_worker['index']].append(str(data))
                        flag[selected_worker['index']] = 1
                        selected_worker['count'] += 1
                        del BUFFER[0]
                        del BUFFER_CLIENT[0]
                    elif 'BUFFER OVERFLOW' in data:
                        print('ERROR OVERFLOW')
                    
                    threadLock2.release()
                print('Lock released')
                threadLock.release()
            

def send_responses(threadName):
    global threadLock
    while 1 == 1:
        for i in range(len(BUFFER_RESULTS)):
            if len(BUFFER_RESULTS[i]) != 0:
                threadLock.acquire(blocking = 1)
                print('Lock1 acquired by', threadName)
                print(i, len(BUFFER_RESULTS[i]), len(BUFFER_RESULTS_CLIENT[i]))
                data = BUFFER_RESULTS[i][0]
                client = BUFFER_RESULTS_CLIENT[i][0]
                print('||| RESPONSE ||')
                print('Sending data, ', data)
                del BUFFER_RESULTS[i][0]
                del BUFFER_RESULTS_CLIENT[i][0]
                print(client)
                client.send(str(data).encode("utf8"))
                print('Lock1 released')
                threadLock.release()
                break
                

def accept_clients (threadName, client_connection):
    global threadLock
    while 1 == 1:
        client_input = client_connection.recv(5120)
        data = client_input.decode("utf8").rstrip()
        integers = data.split('$')
        
        threadLock.acquire(blocking = 1)
        print('Lock1 acquired by', threadName)
        for input_integer in integers:
            try:
                a = int(input_integer)
                if len(BUFFER) != MAX_BUFFER_LENGTH:
                    BUFFER.append(input_integer)
                    BUFFER_CLIENT.append(client_connection)
                else:
                    client_connection.send(('[BUFFER OVERFLOW] ' + str(input_integer) + ' can not be processed now. Please try again later.').encode("utf8"))
                    time.sleep(1)
            except:
                pass
        print('Lock1 Released')
        threadLock.release()

def get_responses (threadName, connection, index):
    global threadLock2
    global threadLock
    while 1 == 1:
        time.sleep(.3)
        if threadLock2.acquire(blocking = False):
            print('Lock2 acquired by ', threadName)
            try:
                connection.settimeout(.25)
                worker_input = connection.recv(5120)
                connection.settimeout(None)
                data = worker_input.decode("utf8").rstrip()
                print(threadName, ':')
                print('||| RESPONSE FROM WORKER |||')
                print('index =', index)
                print('Data from', connection, ': ', data)      
                if 'BUFFER LIMIT REACHED' in data:
                    flag[index] = 0
                elif 'BUFFER ALRIGHT' in data:
                    flag[index] = 1
                if '^2 = ' in data:
                    data = data.split('$')[-2]
                    dict_of_workers[index]['count'] -= 1
                    threadLock.acquire(blocking=True)
                    BUFFER_RESULTS[index].append(str(data))
                    del BUFFER_INPUTS[index][0]      
                    threadLock.release() 
            except:
                connection.settimeout(None)    
            print('Lock released')
            threadLock2.release()   
            
    
number_of_workers = 0        
for port in PORTS:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, port))
    
    dict_of_workers[number_of_workers] = {}
    dict_of_workers[number_of_workers]['count'] = 0
    dict_of_workers[number_of_workers]['connection'] = conn
    dict_of_workers[number_of_workers]['index'] = number_of_workers
    
    BUFFER_RESULTS.append([])
    BUFFER_RESULTS_CLIENT.append([])
    BUFFER_INPUTS.append([])
    
    Thread(target=get_responses, args=('I am Groot', conn, number_of_workers)).start()
    print('Worker ', conn, 'added successfully with index =', number_of_workers)
    
    number_of_workers += 1
        
    time.sleep(1)    
      
Thread(target=distribute_work, args=('I am Iron Man',)).start()
Thread(target=send_responses, args=('I am Steve Rogers',)).start()
        

while 1==1:
    out_s.listen(5)
    conn, addr = out_s.accept()
    print('Connected with ', addr)
    
    Thread(target=accept_clients, args=('I am not Groot', conn,)).start()
    pass
