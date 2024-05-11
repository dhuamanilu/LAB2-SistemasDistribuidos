import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class CristianClock {
  private long clock;
  private static final long SERVER_TIME = TimeUnit.MILLISECONDS.toSeconds(System.currentTimeMillis());

  public CristianClock(long initialTime) {
    this.clock = initialTime;
  }

  public synchronized void synchronize() {
    long sendTime = TimeUnit.MILLISECONDS.toSeconds(System.currentTimeMillis());
    long roundTripTime = simulateNetworkDelay();
    long receivedServerTime = SERVER_TIME + (roundTripTime / 2);
    long offset = receivedServerTime - sendTime;
    this.clock += offset;
  }

  private long simulateNetworkDelay() {
    Random random = new Random();
    long delay = random.nextInt(1000);
    try {
      Thread.sleep(delay);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    return TimeUnit.MILLISECONDS.toSeconds(delay);
  }

  public long getTime() {
    return this.clock;
  }

}
