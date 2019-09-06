# kill $(lsof -t -i:7777)
import socket
import threading
import time
from threading import Thread

HOST = 'localhost'                 
PORTS = [11110, 11111, 11112]

MAX_BUFFER_LENGTH = 10
DELAY = 1

threadLock = threading.Lock()


class worker:
    def __init__(self, port):
        print('Initiating connection with port: ', port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, port))
        self.BUFFER = []
        Thread(target=self.connect_with_server, args=('Server_connector_'+str(port), self.s, port)).start()
  
    
    def take_input (self, threadName, conn ):
        global threadLock
        while 1==1:
            data = conn.recv(1024)     
            print('Input data:', data)
            data = data.decode("utf8").rstrip()
            threadLock.acquire(blocking = 1)
            integers = data.split('$')
            for integer_input in integers:
                try:
                    a = int(integer_input)
                    time.sleep(.5)
                    if len(self.BUFFER) == MAX_BUFFER_LENGTH:
                         conn.send('BUFFER OVERFLOW.'.encode("utf8"))
                    else:
                        self.BUFFER.append(integer_input)
                        if len(self.BUFFER) == MAX_BUFFER_LENGTH:
                            conn.send('BUFFER LIMIT REACHED.'.encode("utf8"))
                        else:
                            conn.send('BUFFER ALRIGHT.'.encode("utf8"))
                    time.sleep(.5)
                except:
                    pass
            threadLock.release()
    
    def send_output (self, threadName, conn ):
        global threadLock
        while 1==1:
            time.sleep(DELAY)
            threadLock.acquire(blocking = 1)
            print(threadName, ': send_output: Length of buffer:', len(self.BUFFER))
            flag = 0
            if len(self.BUFFER) != 0:
                print('Buffer, ', self.BUFFER[0])
                
                try:
                    data = str(self.BUFFER[0]) + '^2 = ' + str(int(self.BUFFER[0]) ** 2)
                    del self.BUFFER[0]
                    flag = 1
                    
                except:
                    del self.BUFFER[0]
            if flag == 1:
                print(threadName, ': send_output: Sending data: ', data)    
                time.sleep(.5)   
                conn.send('BUFFER ALRIGHT.'.encode("utf8"))
                
                conn.send(('$' + str(data) + '$').encode("utf8"))
                
            threadLock.release()

    def connect_with_server (self, threadName, soc, id ):
        while 7 == 7:
            try:
                soc.listen(1)
                conn, addr = soc.accept()
                print('Connected with ', addr)
                threadLock.acquire(blocking = 1)
                Thread(target=self.take_input, args=('take_input'+str(id),conn,)).start()
                Thread(target=self.send_output, args=('send_output'+str(id),conn,)).start()    
                threadLock.release()
            except:
                print('Exception')
                soc.close()    

for port in PORTS:
    new_worker = worker(port)  
while 1==1:
    pass
