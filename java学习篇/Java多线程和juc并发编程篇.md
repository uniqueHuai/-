# 线程的基本概念

线程是程序执行的最小单元，是进程中的一个独立执行路径。

与进程的区别：

- 进程是操作系统资源分配的基本单位
- 线程是CPU调度的基本单位
- 同一进程的多个线程共享进程的资源

---

# 创建线程的方式

## 1 继承Thread类

```
class MyThread extends Thread {
    @Override
    public void run() {
        // 线程执行的代码
    }
}
// 使用
MyThread thread = new MyThread();
thread.start();
```

## 2 实现Runnable接口

```
class MyRunnable implements Runnable {
    @Override
    public void run() {
        // 线程执行的代码
    }
}
// 使用
Thread thread = new Thread(new MyRunnable());
thread.start();
```

## 3 实现Callable接口（带返回值）

```
class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        // 线程执行的代码
        return "结果";
    }
}
// 使用
FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
Thread thread = new Thread(futureTask);
thread.start();
String result = futureTask.get(); // 获取返回值
```

2.4 使用线程池（推荐）

```
ExecutorService executor = Executors.newFixedThreadPool(5);
executor.execute(new Runnable() {
    @Override
    public void run() {
        // 线程执行的代码
    }
});
// 或者
Future<String> future = executor.submit(new Callable<String>() {
    @Override
    public String call() throws Exception {
        // 线程执行的代码
        return "结果";
    }
});
```

---

# 线程的生命周期

新建(New)：线程对象被创建但尚未启动

就绪(Runnable)：调用start()后，等待CPU调度

运行(Running)：获得CPU资源，执行run()方法

阻塞(Blocked)：线程暂时停止执行

等待阻塞：wait()

同步阻塞：获取同步锁失败

其他阻塞：sleep()或join()

死亡(Dead)：run()执行完成或异常退出

---

# 线程的基本控制方法

start()：启动线程

run()：线程执行体

wait（）：object类方法，释放锁，需要notify()/notifyAll()唤醒或超时

sleep(long millis)：线程休眠，不释放锁

yield()：让出CPU，进入就绪状态

join()：等待该线程终止

interrupt()：中断线程

isAlive()：判断线程是否存活

---

# 线程同步与锁

## 1 synchronized关键字（传统）（可重入锁）

- 非公平锁
- 内置锁
- 隐式获取锁和释放锁
- 锁不可中断和查询状态

同步方法：

```
public synchronized void method() {
    // 同步代码
}
```

同步代码块：

```
synchronized(锁对象) {
    // 同步代码
}
```

## 2 Lock接口（JUC方式）（可重入锁）

- 默认非公平锁，可设置公平锁
- 显示调用lock()和unlock（）
- 可查询锁的状态

```
Lock lock = new ReentrantLock();
lock.lock();
try {
    // 同步代码
} finally {
    lock.unlock();
}
```

## 3 ReadWriteLock接口（读写锁）

- 读锁（共享锁）
- 写锁（排他锁）

```
 private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private int sharedData = 0;

    // 读操作
    public int readData() {
        rwLock.readLock().lock();
        try {
            System.out.println(Thread.currentThread().getName() + " 读取数据: " + sharedData);
            return sharedData;
        } finally {
            rwLock.readLock().unlock();
        }
    }

    // 写操作
    public void writeData(int newValue) {
        rwLock.writeLock().lock();
        try {
            System.out.println(Thread.currentThread().getName() + " 写入数据: " + newValue);
            sharedData = newValue;
        } finally {
            rwLock.writeLock().unlock();
        }
    }
```

3 volatile关键字(无锁，只是多线程同步时只能修饰变量，轻量级同步机制)

保证变量的可见性，但不保证原子性，禁止指令重排

```
private volatile boolean flag = false;
```

4 原子类（这个可以保证原子性）

java.util.concurrent.atomic包下的原子类，如：

- AtomicInteger
- AtomicLong
- AtomicBoolean
- AtomicReference

---

# 线程间通信

wait()/notify()/notifyAll() （不能精确唤醒线程）

必须在同步代码块中使用：

```
synchronized(obj) {
    obj.wait(); // 释放锁并等待
    obj.notify(); // 唤醒一个等待线程
    obj.notifyAll(); // 唤醒所有等待线程
}
```

Condition（能精确的唤醒线程）

与Lock配合使用：

```
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();

lock.lock();
try {
    condition.await(); // 类似wait()
    condition.signal(); // 类似notify()
    condition.signalAll(); // 类似notifyAll()
} finally {
    lock.unlock();
}
```

注意虚假唤醒，这是JVM的一个特性，用while来条件判断。

---

# 线程安全类

List并发下线程不安全，解决方法有：

```
//方法1
List<String> list1 = new Vector<>();
//方法2
List<String> list2 = Collections.synchronizedList(new ArrayList<>());
//方法3
List<String> list3 = new CopyOnWriteArrayList<>();
```

Set并发下线程不安全，解决方法有：

```
//方法1
Set<String> set2 = Collections.synchronizedSet(new HashSet<>());
//方法2
Set<String> set3 = new CopyOnWriteArraySet<>();
```

Map并发下线程不安全，解决方法有：

```
//方法1
Map<String, String> map1 = Collections.synchronizedMap(new HashMap<>());
//方法2
Map<String, String> map2 = new ConcurrentHashMap<>();
```

---

# 并发集合

- CopyOnWriteArrayList：线程安全的ArrayList
- CopyOnWriteArraySet：线程安全的HashSet
- ConcurrentHashMap：线程安全的HashMap
- BlockingQueue：阻塞队列接口
- ArrayBlockingQueue
- LinkedBlockingQueue
- PriorityBlockingQueue
- SynchronousQueue

---

# 阻塞队列

![](https://cdn.nlark.com/yuque/0/2025/jpeg/52814014/1755488290184-33eb7d3e-0519-4e95-a511-cdd4683ee0ae.jpeg)

## 四组api

```
ArrayBlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);  //容量为10的队列
```

|   |   |   |   |   |
|---|---|---|---|---|
|方式|抛出异常|有返回值，不抛出异常|阻塞等待|等待超时|
|添加|add()|offer()|put()|offer(,,)|
|移除|remove()|poll()|take()|poll(,,)|
|检测队首元素|element()|peek()|--|--|

## SynchronizedQueue同步队列

队列容量为一，使用put（）和take（），放一个拿一个。

---

# 线程池

作用

减少线程创建/销毁开销：线程的创建和销毁是昂贵的操作，线程池通过复用已创建的线程，避免了频繁创建销毁的开销

控制内存占用：无限制创建线程可能导致内存耗尽，线程池限制最大线程数量

1 创建线程池

```
//推荐使用 new ThreadPoolExecutor创建线程

ExecutorService singlepool = Executors.newSingleThreadExecutor();//单个线程
ExecutorService threadPool = Executors.newFixedThreadPool(5); // 固定大小
ExecutorService cachedPool = Executors.newCachedThreadPool(); // 可伸缩线程池，可缓存
//执行线程
.execute();      //在（）内执行任务
.shutdown();     //关闭线程池

ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(3); // 定时
scheduledPool.schedule()   // 单次延迟任务
scheduledPool.scheduleAtFixedRate()    // 固定频率任务（严格间隔）
scheduledPool.scheduleWithFixedDelay()   // 固定延迟任务（保证间隔）
```

2 ThreadPoolExecutor（7个参数）

```
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    corePoolSize, // 核心线程数
    maximumPoolSize, // 最大线程数
    keepAliveTime, // 空闲线程存活时间
    TimeUnit.MILLISECONDS, // 时间单位
    new LinkedBlockingQueue<Runnable>() // 工作队列
    //后面两个参数是可以创建野可以使用默认的，就是可以5个就创建了
    Executors.defaultThreadFactory(),  //默认线程工厂
    new ThreadPoolExecutor.AbortPolicy()  //拒绝策略，就是抛出异常还是不处理这些
);
```

3 线程池参数

- corePoolSize：核心线程数，通过io密集型获取主要io线程数（调优）
- maximumPoolSize：最大线程数，通过cpu密集型获取计算机的线程数（调优）

Runtime.getRuntime().availableProcessors();

- keepAliveTime：空闲线程存活时间
- workQueue：任务队列
- threadFactory：线程工厂
- handler：拒绝策略，有四个拒绝策略

---

# 其他高级特性

1 CountDownLatch(减法计数器)

等待多个线程完成：

```
CountDownLatch latch = new CountDownLatch(3); //设置3个计数器

latch.countDown(); //减去一个计数器

latch.await();	//计数器要为零才能继续执行
```

2 CyclicBarrier（加法计数器）

线程到达屏障时被阻塞：

```
CyclicBarrier barrier = new CyclicBarrier(3,Runnable);
// 在多个线程中,执行了三次这个才能执行上面Runnable里面的东西
barrier.await();
```

3 Semaphore（限流用）

控制同时访问的线程数量：

```
Semaphore semaphore = new Semaphore(5);
semaphore.acquire();  //获得资源等到被释放为止，-1
semaphore.release();  //释放资源，+1
```

4 Future和FutureTask(异步回调)

获取异步计算结果：

```
FutureTask<String> futureTask = new FutureTask<>(callable);
new Thread(futureTask).start();
String result = futureTask.get();
```

5 Fork/Join框架

```
class MyTask extends RecursiveTask<Integer> {
    @Override
    protected Integer compute() {
        // 任务逻辑
    }
}

ForkJoinPool pool = new ForkJoinPool();
MyTask task = new MyTask();
pool.invoke(task);
int result = task.get();
```

---

# 四大函数式接口

1. Consumer (消费者) 作用：消费数据，无返回值

方法：void accept(T t)

示例：list.forEach(x -> System.out.println(x))

2. Supplier (供应者) 作用：提供数据，无参数

方法：T get()

示例：() -> "默认值"

3. Function<T,R> (转换器)  
    作用：数据转换，T→R

方法：R apply(T t)

示例：s -> s.length()

4. Predicate (判断器) 作用：条件判断

方法：boolean test(T t)

示例：n -> n > 0

---

# JMM

java内存模型，不存在的东西，概念！

## 同步约定

1、线程解锁前，必须把共享变量立刻刷回主存。

2、加锁前，读取主存最新值到工作内存中。

3、加锁和解锁是同一把锁。

线程 **工作内存、主内存**

---

# CAS

CAS（Compare-And-Swap）是一种无锁的原子操作

CAS工作原理

1. 读取内存值V
2. 比较V与预期值A
3. 如果相等，则写入新值B
4. 返回操作是否成功

乐观锁（典型CAS，无锁操作）

悲观锁（典型synchronized和lock）

```
AtomicInteger atomicInt = new AtomicInteger(0);

// CAS操作示例
boolean success = atomicInt.compareAndSet(0, 1); // 如果当前值为0，则设置为1
```

## ABA问题

ABA问题描述的是这样一种情况：

线程1读取内存位置V的值为A

线程1被挂起

线程2修改V的值为B，然后又修改回A

线程1恢复执行，进行CAS操作，发现V的值仍然是A，于是操作成功