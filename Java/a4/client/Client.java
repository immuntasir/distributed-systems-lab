import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {

    private Client() {}

    public static void main(String[] args) {
        System.out.println("Client Started.");
        String host = (args.length < 1) ? null : args[0];
        System.out.println("host " + host);        
        try {
            Registry registry = LocateRegistry.getRegistry(host);
            Interface stub = (Interface) registry.lookup("Interface");
            String response = stub.sayHello();
            System.out.println("response: " + response);
            response = stub.keyed_caesar("GORDIAN");
            System.out.println("response: " + response);
            response = stub.vigenere("GORDIAN");
            System.out.println("response: " + response);
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
