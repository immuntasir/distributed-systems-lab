# kill $(lsof -t -i:7777)
import socket
import sys
import traceback
from threading import Thread
import random
import numpy as np
import time
names = []
jokes = []
total_number_of_clients = -1

def main():
    global total_number_of_clients
    total_number_of_clients = -1
    start_server()


def start_server():
    global total_number_of_clients
    host = "127.0.0.1"
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    soc.settimeout(5)   
   
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests
    while total_number_of_clients != 0:
        try:
          connection, address = soc.accept()
          ip, port = str(address[0]), str(address[1])
        except TimeoutException:
          pass
        print("Connected with " + ip + ":" + port)
        if total_number_of_clients == -1:
            total_number_of_clients = 1
        else:
            total_number_of_clients += 1
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    global total_number_of_clients
    with open('name.txt') as f:
        names = f.readlines()
    with open('joke.txt') as f:
        jokes = f.readlines()
        
    flag = np.zeros(len(names))
    print(names)
    print(jokes)
    is_active = True
    joke_stage = 0
    expected_message = 'Y'
    selected_joke = -1
    should_terminate = 0
    jokes_served = 0
    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        print(client_input, expected_message)
        if client_input.lower() == expected_message.lower():
            if joke_stage == 0:
                connection.sendall("Knock Knock!".encode("utf8"))
                joke_stage = 1
                expected_message = 'Who\'s there?'
            elif joke_stage == 1:
                finding = 1
                while finding == True:
                  selected_joke = random.randint(0, len(jokes)-1)
                  if flag[selected_joke] == 0:
                     finding = False
                print('Selected', selected_joke)
                should_terminate = 0
                connection.sendall(names[selected_joke].encode("utf8"))
                joke_stage = 2
                expected_message = names[selected_joke].rstrip() + ' who?'
                print('Sent', names[selected_joke])
                print('Expecting', expected_message)
            elif joke_stage == 2:
                connection.sendall(jokes[selected_joke].encode("utf8"))
                flag[selected_joke] = 1
                jokes_served += 1
                if jokes_served == len(jokes):
                    print('No more jokes to serve for this client')
                    connection.sendall('I have no more jokes to tell.'.encode("utf8"))
                    time.sleep(3)
                    connection.sendall("quit".encode("utf8"))
                    connection.close()
                    print("Connection " + ip + ":" + port + " closed")
                    total_number_of_clients -= 1
                    print('Number of active clients: ', total_number_of_clients)
                    is_active = False
                else:
                    connection.sendall('Would you like to listen to another? (Y/N)'.encode("utf8"))
                    joke_stage = 0
                    should_terminate = 1
                    expected_message = 'Y'
                    selected_joke = -1    
                
        elif should_terminate == 1 and (client_input == 'N' or client_input == 'n'):
            print("Client is requesting to quit")
            connection.sendall("quit".encode("utf8"))
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            total_number_of_clients -= 1
            print('Number of active clients: ', total_number_of_clients)
            is_active = False
            
        else:
            print("Processed result: {}".format(client_input))
            send_message = "You are supposed to say \"" + expected_message + "\".Let\'s try again." 
            connection.sendall(send_message.encode("utf8"))
            connection.sendall('Knock Knock!'.encode("utf8"))
            joke_stage = 1
            expected_message = 'Who\'s there?'
def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    print("Processing the input received from client")

    return str(input_str)

if __name__ == "__main__":
    main()
