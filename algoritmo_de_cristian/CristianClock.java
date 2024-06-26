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

  public static void main(String[] args) {
    List<Thread> threads = new ArrayList<>();
    CristianClock clock = new CristianClock(TimeUnit.MILLISECONDS.toSeconds(System.currentTimeMillis()));

    for (int i = 0; i < 5; i++) {
      Thread thread = new Thread(new Runnable() {
	@Override
	public void run() {
	  System.out.println("Thread " + Thread.currentThread().getId() + " tiempo local antes de sincronizar: " + clock.getTime() + " segundos");
	  clock.synchronize();
	  System.out.println("Thread " + Thread.currentThread().getId() + " tiempo local después de sincronizar: " + clock.getTime() + " segundos");
	}
      });
      threads.add(thread);
      thread.start();
    }

    for (Thread thread : threads) {
      try {
	thread.join();
      } catch (InterruptedException e) {
	e.printStackTrace();
      }
    }

    System.out.println("Tiempo final sincronizado: " + clock.getTime() + " segundos");
  }

}
