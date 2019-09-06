import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Server implements Interface {

    public Server() {}

    public String sayHello() {
        return "Hello, world!";
    }
    

    public String keyed_caesar(String key) {
        return "This should decipher using keyed caesar cipher.";
    }

    public String vigenere(String key) {
        return "This should decipher using vigenere cipher.";
    }    
    
    public static void main(String args[]) {
        try {
            Server obj = new Server();
            Interface stub = (Interface) UnicastRemoteObject.exportObject(obj, 0);

            // Bind the remote object's stub in the registry
            Registry registry = LocateRegistry.getRegistry();
            registry.bind("Hello", stub);

            System.err.println("Server ready");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
