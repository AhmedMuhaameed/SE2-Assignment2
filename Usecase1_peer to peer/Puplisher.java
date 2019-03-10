import java.io.IOException;
import java.net.*;
import java.util.*;

public class Puplisher {
    private DatagramSocket socket =null;
    private InetAddress group=null;
    private byte [] buf;
    public Vector<String>queue=new Vector<>();

    public void multicast(String message)throws IOException {
        socket =new DatagramSocket();
        group=InetAddress.getByName("230.0.0.0");
        buf = message.getBytes();

        DatagramPacket packet =new DatagramPacket(buf,buf.length,group,1234);
        socket.send(packet);
        socket.close();
    }


}
