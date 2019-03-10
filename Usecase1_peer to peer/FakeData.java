import java.io.IOException;
import java.util.*;

public class FakeData extends Thread {
    private Puplisher p=new Puplisher();


    public String  RandomWord() {

        int leftLimit = 97; // letter 'a'
        int rightLimit = 122; // letter 'z'
        int targetStringLength = 10;
        Random random = new Random();
        StringBuilder buffer = new StringBuilder(targetStringLength);
        for (int i = 0; i < targetStringLength; i++) {
            int randomLimitedInt = leftLimit + (int)
                    (random.nextFloat() * (rightLimit - leftLimit + 1));
            buffer.append((char) randomLimitedInt);
        }
        String generatedString = buffer.toString();
       // System.out.println(generatedString);
        p.queue.addElement(generatedString);

        return generatedString;
    }

    public void run(){
        try{

            Random x=new Random();
            //System.out.println(x.nextInt(5000));
            while (true){

                p.multicast(RandomWord());
                Thread.sleep(x.nextInt(5000));
            }
        }catch (IOException e)
        {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    public static void main(String [] args) throws IOException {

        System.out.println("sending!!!!");
        Thread f =new Thread(new FakeData());

        f.start();

    }

}
