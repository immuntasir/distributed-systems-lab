# kill $(lsof -t -i:7777)


import socket

HOST = 'localhost'                 
PORT = 12378            

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


while 1:
  try:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected with ', addr)
    while 1:
      data = conn.recv(1024)
      if not data: 
        break
      elif str(data) == 'BEGIN':
        print(addr, ': ', str(data))
        conn.send('Connection established.')
        pass
      elif str(data) == 'END':
        print(addr, ': ', str(data))
        conn.send('Connection is now being terminated.')
        conn.close()
        break
      else:
        print(addr, ': ', str(data))
        conn.send(data)
  except:
    s.close()
    break
