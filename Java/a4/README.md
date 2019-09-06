First, run the rmiregistry on port 1099.
To kill an already existing port, execute the following command: sudo kill `sudo lsof -t -i:1099`

Then, (compile and) run the codes for Server.
1. cd Server
2. javac Interface.java Server.java 
3. java Server

Finally, (compile and) run the codes for Client.
1. cd ../Client
2. javac Interface.java Client.java 
3. java Client
