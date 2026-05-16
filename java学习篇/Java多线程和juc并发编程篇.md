# Java多线程和JUC并发编程篇

## 一、线程的基本概念

**线程**是程序执行的最小单元，是进程中的一个独立执行路径。

| 对比维度 | 进程 | 线程 |
|----------|:----:|:----:|
| 资源分配 | 操作系统**资源分配**的基本单位 | 所属进程内共享资源 |
| CPU 调度 | ❌ | ✅ **CPU 调度**的基本单位 |
| 资源开销 | 独立内存空间，开销大 | 共享进程资源，开销小 |

---

## 二、创建线程的方式

### 1. 继承 Thread 类

```java
class MyThread extends Thread {
    @Override
    public void run() {
        // 线程执行的代码
    }
}
// 使用
new MyThread().start();
```

### 2. 实现 Runnable 接口（推荐）

```java
class MyRunnable implements Runnable {
    @Override
    public void run() {
        // 线程执行的代码
    }
}
// 使用
new Thread(new MyRunnable()).start();
```

### 3. 实现 Callable 接口（带返回值）

```java
class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "结果";
    }
}
// 使用
FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
new Thread(futureTask).start();
String result = futureTask.get(); // 获取返回值（会阻塞）
```

### 4. 使用线程池（推荐）

```java
ExecutorService executor = Executors.newFixedThreadPool(5);
executor.execute(() -> System.out.println("执行任务"));

Future<String> future = executor.submit(() -> "结果");
```

> [!tip] **三种方式对比**
>
| 方式 | 优点 | 缺点 |
|------|------|------|
| 继承 Thread | 简单直接 | 不能继承其他类 |
| 实现 Runnable | 可继承其他类 | 无返回值 |
| 实现 Callable | 有返回值，可抛异常 | 略复杂 |
| **线程池** | **复用线程，控制并发，推荐** | — |

---

## 三、线程的生命周期

```
新建(NEW) ──start()──▶ 就绪(RUNNABLE) ──CPU调度──▶ 运行(RUNNING)
                                                        │
                        ┌────────────────────────────────┤
                        ▼                                ▼
                    阻塞(BLOCKED)                     死亡(TERMINATED)
                        │
                    ┌───┴───┐
                    ▼       ▼
                等待阻塞    同步阻塞
                wait()    锁竞争失败
                其他阻塞
                sleep/join
```

| 状态 | 说明 |
|------|------|
| **NEW** | 线程对象已创建，未调用 `start()` |
| **RUNNABLE** | 调用了 `start()`，等待 CPU 调度 |
| **RUNNING** | 获得 CPU 资源，正在执行 `run()` |
| **BLOCKED** | `wait()` / 锁竞争失败 / `sleep()` / `join()` |
| **TERMINATED** | `run()` 执行完成或异常退出 |

---

## 四、线程的基本控制方法

| 方法 | 属于 | 说明 |
|------|:----:|------|
| `start()` | Thread | **启动**线程 |
| `run()` | Thread | 线程**执行体** |
| `wait()` | **Object** | **释放锁**，等待 `notify()`/`notifyAll()` 唤醒 |
| `sleep()` | Thread | 线程**休眠**，**不释放锁** |
| `yield()` | Thread | **让出** CPU，进入就绪状态 |
| `join()` | Thread | **等待**该线程终止 |
| `interrupt()` | Thread | 中断线程（设置中断标志位） |
| `isAlive()` | Thread | 判断线程是否存活 |

> [!warning] **`wait()` vs `sleep()` 关键区别**
> - `wait()` 是 Object 方法，**会释放锁**，需要被唤醒
> - `sleep()` 是 Thread 方法，**不会释放锁**，到期自动唤醒

---

## 五、线程同步与锁

### 1. synchronized 关键字（内置锁）

- 可重入锁
- 默认**非公平锁**
- 隐式获取 / 释放锁
- 锁不可中断、不可查询状态

```java
// 同步方法
public synchronized void method() { }

// 同步代码块
synchronized(锁对象) { }
```

### 2. Lock 接口（JUC）

- 默认非公平锁，可设置为**公平锁**
- **显式**调用 `lock()` 和 `unlock()`
- 可查询锁状态

```java
Lock lock = new ReentrantLock(true); // fair = true 为公平锁
lock.lock();
try {
    // 同步代码
} finally {
    lock.unlock(); // ⚠️ 必须在 finally 中释放
}
```

### 3. ReadWriteLock（读写锁）

| 锁类型 | 名称 | 说明 |
|:------:|------|------|
| **读锁** | 共享锁 | 多个线程可同时读 |
| **写锁** | 排他锁 | 只能一个线程写，读也阻塞 |

```java
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
private int data = 0;

// 读操作（共享）
public int read() {
    rwLock.readLock().lock();
    try { return data; } 
    finally { rwLock.readLock().unlock(); }
}

// 写操作（排他）
public void write(int value) {
    rwLock.writeLock().lock();
    try { data = value; } 
    finally { rwLock.writeLock().unlock(); }
}
```

### 4. volatile 关键字（轻量级同步）

**特性**：
- ✅ 保证变量的**可见性**（修改后立即刷新到主存）
- ❌ **不保证原子性**
- ✅ **禁止指令重排**

```java
private volatile boolean flag = false;
```

> [!tip] **volatile vs synchronized**
> - `volatile` 只能修饰变量，适用于**一个线程写、多个线程读**的场景
> - `synchronized` 可以修饰方法/代码块，保证**可见性 + 原子性**

### 5. 原子类（保证原子性）

`java.util.concurrent.atomic` 包下，基于 **CAS** 实现：

| 原子类 | 说明 |
|--------|------|
| `AtomicInteger` | 原子整型 |
| `AtomicLong` | 原子长整型 |
| `AtomicBoolean` | 原子布尔 |
| `AtomicReference<V>` | 原子引用类型 |

---

## 六、线程间通信

### 方式一：wait / notify（传统）

> [!warning] 必须在 `synchronized` 同步块中使用，否则抛 `IllegalMonitorStateException`

```java
synchronized(obj) {
    obj.wait();      // 释放锁并等待（不能精确唤醒指定线程）
    obj.notify();    // 随机唤醒一个等待线程
    obj.notifyAll(); // 唤醒所有等待线程
}
```

### 方式二：Condition（精确唤醒）

与 Lock 配合使用，可以精确唤醒**指定**线程：

```java
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();

lock.lock();
try {
    condition.await();    // 类似 wait()
    condition.signal();   // 类似 notify() — 精确唤醒
    condition.signalAll();
} finally {
    lock.unlock();
}
```

> [!danger] **虚假唤醒（Spurious Wakeup）**
> 线程可能在未被 `notify()`/`signal()` 的情况下被唤醒。**必须用 `while` 循环判断条件**，而不是 `if`：
> ```java
> while (条件不满足) { // ⚠️ 用 while 不是 if
>     condition.await();
> }
> ```

---

## 七、线程安全类

### 线程安全的 List

```java
// 方法1：Vector（古老，不推荐）
List<String> list1 = new Vector<>();

// 方法2：同步包装类
List<String> list2 = Collections.synchronizedList(new ArrayList<>());

// 方法3：CopyOnWriteArrayList ✅ 推荐（读多写少场景）
List<String> list3 = new CopyOnWriteArrayList<>();
```

### 线程安全的 Set

```java
Set<String> set1 = Collections.synchronizedSet(new HashSet<>());
Set<String> set2 = new CopyOnWriteArraySet<>();
```

### 线程安全的 Map

```java
Map<String, String> map1 = Collections.synchronizedMap(new HashMap<>());
Map<String, String> map2 = new ConcurrentHashMap<>(); // ✅ 推荐
```

---

## 八、并发集合

| 集合 | 说明 |
|------|------|
| `CopyOnWriteArrayList` | 线程安全的 ArrayList，**写时复制** |
| `CopyOnWriteArraySet` | 线程安全的 HashSet |
| `ConcurrentHashMap` | 线程安全的 HashMap，**分段锁/CAS** |
| `BlockingQueue` | 阻塞队列接口 |
| `ArrayBlockingQueue` | 有界阻塞队列 |
| `LinkedBlockingQueue` | 可选有界阻塞队列（链表） |
| `PriorityBlockingQueue` | 支持优先级排序 |
| `SynchronousQueue` | 容量为 0，**必须生产者消费者同时到达** |

---

## 九、阻塞队列

### 四组 API

| 方式 | 抛出异常 | 返回特殊值 | 阻塞等待 | 超时等待 |
|:----:|:--------:|:----------:|:--------:|:--------:|
| **添加** | `add()` | `offer()` | `put()` | `offer(time, unit)` |
| **移除** | `remove()` | `poll()` | `take()` | `poll(time, unit)` |
| **检测队首** | `element()` | `peek()` | — | — |

```java
ArrayBlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);
```

> [!info] **`SynchronousQueue`**
> 容量为 1 的同步队列，一个 `put()` 必须等待一个 `take()`，**放一个拿一个**。

---

## 十、线程池

### 作用

- ✅ **减少线程创建/销毁开销**：复用已创建的线程
- ✅ **控制内存占用**：限制最大线程数量，防止资源耗尽
- ✅ **统一管理**：任务队列、拒绝策略等

### 创建线程池

```java
// ⚠️ 推荐使用 new ThreadPoolExecutor() 创建，明确参数
// 不推荐 Executors 工具类（可能隐藏问题）

ExecutorService fixedPool = Executors.newFixedThreadPool(5);     // 固定大小
ExecutorService cachedPool = Executors.newCachedThreadPool();     // 可伸缩
ExecutorService singlePool = Executors.newSingleThreadExecutor(); // 单线程
ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(3);

scheduledPool.schedule(task, 10, TimeUnit.SECONDS);              // 单次延迟
scheduledPool.scheduleAtFixedRate(task, 0, 5, TimeUnit.SECONDS); // 固定频率
scheduledPool.scheduleWithFixedDelay(task, 0, 5, TimeUnit.SECONDS); // 固定延迟
```

### ThreadPoolExecutor（7 个参数）

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    corePoolSize,                                    // ① 核心线程数
    maximumPoolSize,                                 // ② 最大线程数
    keepAliveTime,                                   // ③ 空闲线程存活时间
    TimeUnit.MILLISECONDS,                           // ④ 时间单位
    new LinkedBlockingQueue<>(100),                  // ⑤ 工作队列
    Executors.defaultThreadFactory(),                // ⑥ 线程工厂
    new ThreadPoolExecutor.AbortPolicy()             // ⑦ 拒绝策略
);
```

### 参数调优建议

| 类型 | 公式 | 说明 |
|:----:|------|------|
| **CPU 密集型** | `N + 1` | `Runtime.getRuntime().availableProcessors() + 1` |
| **IO 密集型** | `2N` | 大部分线程在等待 IO，可设置更多线程 |

### 四种拒绝策略

| 策略 | 行为 |
|------|------|
| `AbortPolicy`（默认） | 抛出 `RejectedExecutionException` |
| `CallerRunsPolicy` | 调用者线程自己执行任务 |
| `DiscardPolicy` | 丢弃任务，不抛异常 |
| `DiscardOldestPolicy` | 丢弃队列中最旧的任务，然后重试 |

---

## 十一、JUC 高级工具

### 1. CountDownLatch（减法计数器）

**场景**：等待多个线程完成后再继续执行。

```java
CountDownLatch latch = new CountDownLatch(3);

// 每个线程完成后调用
latch.countDown();  // 计数器减 1

// 主线程等待
latch.await();      // 阻塞，直到计数器归零
```

### 2. CyclicBarrier（加法计数器）

**场景**：多个线程互相等待，都到达屏障后再一起继续。

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("所有线程到达屏障，开始执行");
});

// 每个线程中
barrier.await();  // 等待，直到 3 个线程都到达
```

> [!tip] **CountDownLatch vs CyclicBarrier**
> - `CountDownLatch`：**一个线程等待多个线程**（减计数，**不可重置**）
> - `CyclicBarrier`：**多个线程互相等待**（加计数，**可重置复用**）

### 3. Semaphore（信号量 — 限流）

**场景**：控制同时访问资源的线程数量。

```java
Semaphore semaphore = new Semaphore(5);   // 最多 5 个线程同时访问

semaphore.acquire();   // 获取许可（-1），没有则阻塞等待
semaphore.release();   // 释放许可（+1）
```

### 4. Future / FutureTask（异步回调）

```java
FutureTask<String> futureTask = new FutureTask<>(() -> "异步结果");
new Thread(futureTask).start();
String result = futureTask.get();   // 阻塞获取结果
```

### 5. Fork / Join 框架

**场景**：将大任务拆分为小任务并行执行，再合并结果。

```java
class MyTask extends RecursiveTask<Integer> {
    @Override
    protected Integer compute() {
        // 拆分+合并逻辑
        return result;
    }
}

ForkJoinPool pool = new ForkJoinPool();
Integer result = pool.invoke(new MyTask());
```

---

## 十二、四大函数式接口（Java 8）

| 接口 | 名称 | 方法 | 参数 | 返回值 |
|------|:----:|:----:|:----:|:------:|
| `Consumer<T>` | 消费者 | `void accept(T t)` | ✅ | ❌ |
| `Supplier<T>` | 供应者 | `T get()` | ❌ | ✅ |
| `Function<T,R>` | 转换器 | `R apply(T t)` | ✅ | ✅ |
| `Predicate<T>` | 判断器 | `boolean test(T t)` | ✅ | `boolean` |

```java
// Consumer：消费数据
list.forEach(x -> System.out.println(x));

// Supplier：提供数据
Supplier<String> supplier = () -> "默认值";

// Function：数据转换
Function<String, Integer> func = s -> s.length();

// Predicate：条件判断
Predicate<Integer> pred = n -> n > 0;
```

---

## 十三、JMM（Java 内存模型）

> [!info] JMM 是一种**规范**（抽象概念），定义了多线程之间共享变量的访问规则，保证可见性、有序性、原子性。

### 同步约定

1. **解锁前**：必须将共享变量**立即刷回主存**
2. **加锁前**：必须读取主存**最新值**到工作内存
3. **加锁和解锁必须是同一把锁**

```
          线程 A                         线程 B
     ┌─────────────┐              ┌─────────────┐
     │  工作内存    │              │  工作内存    │
     │  (变量副本)   │              │  (变量副本)   │
     └──────┬──────┘              └──────┬──────┘
            │                            │
            │        ╔══════════╗        │
            └─────── ║  主内存   ║ ←──────┘
                     ╚══════════╝
```

---

## 十四、CAS（Compare-And-Swap）

**CAS 是一种无锁的原子操作**，是乐观锁的实现基础。

### 工作原理

```
① 读取内存值 V
② 比较 V 与预期值 A
③ 如果相等 → 写入新值 B（操作成功）
   如果不相等 → 操作失败，返回 false
```

```java
AtomicInteger atomicInt = new AtomicInteger(0);
// CAS 操作：如果当前值为 0，则设置为 1
boolean success = atomicInt.compareAndSet(0, 1);
```

### 乐观锁 vs 悲观锁

| 类型 | 代表 | 特点 |
|:----:|:----:|------|
| **乐观锁** | CAS、版本号 | 不加锁，冲突后重试，适合读多写少 |
| **悲观锁** | `synchronized`、`Lock` | 加锁，阻塞等待，适合写多 |

### ABA 问题

> [!warning] **ABA 问题描述**
> 线程 1 读取值为 A，被挂起 → 线程 2 将 A 改为 B 又改回 A → 线程 1 恢复执行，CAS 发现还是 A，操作成功——但值实际上已经被修改过。

**解决方案**：使用 `AtomicStampedReference`（带版本号的原子引用），每次修改版本号 +1。
