//receiver_____________________________________
import java.io.*;
import java.net.*;
public class Main extends Thread {

    protected MulticastSocket socket =null;
    protected byte [] buf= new byte[1024];
    protected String name;

    public Main(String n){
        name=n;
    }

    public void run() {
        try {
            socket=new MulticastSocket(1234);
            InetAddress group=InetAddress.getByName("230.0.0.0");
            socket.joinGroup(group);
            while (true){
                DatagramPacket packet=new DatagramPacket(buf,buf.length);
                socket.receive(packet);
                String receive=new String(packet.getData(),0,packet.getLength());
                System.out.println(name+" : "+receive);
                if("end".equals(receive)){
                    break;
                }
            }
            socket.leaveGroup(group);
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println(e);
        }

    }

    public static void main(String[] args) {
        Thread T1= new Thread(new Main("T1"));
        Thread T2= new Thread(new Main("T2"));
        Thread T3= new Thread(new Main("T3"));
        Thread T4= new Thread(new Main("T4"));

        T1.start();
        T2.start();
        T3.start();
        T4.start();

    }
}
