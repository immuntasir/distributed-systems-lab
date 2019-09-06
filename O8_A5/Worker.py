import socket
import sys
import os
from thread import *
import time
from datetime import datetime
import random

host = 'localhost'
port = 26007

workerSocket = socket.socket()
workerSocket.connect((host,port))

myHost = 'localhost'
myPort = 26017

workerSocket.sendall(myHost+'|'+myPort+',')


