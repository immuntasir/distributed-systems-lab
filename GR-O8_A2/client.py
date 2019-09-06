import socket
import sys
from tkinter import *

import threading

class App(threading.Thread):

    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 8888 
        self.isActive = 1      
        
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()
    def Enter_pressed(self, event):
        self.input_get = self.input_field.get()
        if self.input_get == 'Y' or self.input_get == 'y':
            self.soc.sendall('Y'.encode("utf8"))  
        else:
            self.soc.sendall(self.input_get.encode("utf8"))        
        self.messages.insert(INSERT, 'Client: %s\n' % self.input_get)
        self.input_user.set('')
          
        if self.input_get == 'N' or self.input_get == 'n':
          #self.root.quit()
          #self.root.destroy()
          #self.isActive = 0
          #sys.exit()
          pass
        return "break"
    def run(self):
        
        try:
            self.soc.connect((self.host, self.port))
            self.root = Tk()
            self.messages = Text(self.root)
            self.messages.pack()
            self.messages.insert(INSERT, 'Welcome to the carnival of jokes.\n')
            self.messages.insert(INSERT, '__________________________________\n')
            self.soc.sendall('Y'.encode("utf8"))
            
        except:
            print("Connection error")
            sys.exit()
        
        
        
        self.input_user = StringVar()
        self.input_field = Entry(self.root, text=self.input_user)
        self.input_field.pack(side=BOTTOM, fill=X)
     
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.frame = Frame(self.root)  # , width=300, height=300)
        self.input_field.bind("<Return>", self.Enter_pressed)
        self.frame.pack() 
        
        self.root.mainloop()


    def message_from_server(self, message):
        self.messages.insert(INSERT, 'Server: %s\n' % message)
        if message == 'quit':
            #self.root.quit()
            #self.isActive = 0
            pass
        else:
            self.root.update()
        pass    




def main():
    app = App()
    while app.isActive  == 1 :
        server_input = app.soc.recv(5120)        
        server_input_size = sys.getsizeof(server_input)
        if server_input_size != 0:
            decoded_input = server_input.decode("utf8").rstrip()  # decode and strip end of line
            if decoded_input == 'quit':
                print('should quit')
                print(decoded_input)
                app.root.quit()
                sys.exit()
            print('here ', decoded_input)   
            app.message_from_server(decoded_input) 

    
    
    #app.soc.send(b'--quit--')
    
if __name__ == "__main__":
    main()
