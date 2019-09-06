# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 12378          # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
isConnected = False
while 1 == 1 :
  raw_inputString = input()
  
  if (raw_inputString == 'BEGIN'):
    if isConnected == True:
      print('Already connected!')
    else:
      s.send('BEGIN')
      data = s.recv(1024)
      isConnected = True
      print('Received', repr(data))
    
  elif (raw_inputString == 'END'):
    if isConnected == True:
      s.send('END')      
      data = s.recv(1024)
      s.close()
      print('Received', repr(data))
      break
    else:
      print('Not connected yet.')
      pass
  else:
    print('Is connected: ', isConnected)
    if isConnected == True:
      s.send(raw_inputString)
      data = s.recv(1024)
      print('Received', repr(data))
    else: 
      print('Not connected yet.')
      pass



