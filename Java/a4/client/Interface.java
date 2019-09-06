import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Interface extends Remote {
    String sayHello() throws RemoteException;
    String keyed_caesar(String key) throws RemoteException;
    String vigenere(String key) throws RemoteException;
}
