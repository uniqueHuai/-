# ☕ Java 全栈开发 · 面试知识点

> 配合 [[八股文面试篇/SSM篇]]（Spring 核心八股）一起复习效果更佳
> 已有参考笔记：[[java学习篇/Java基础与进阶篇]] · [[java学习篇/JVM篇]] · [[java学习篇/SpringBoot篇]] · [[java学习篇/SpringCloud篇]] · [[java学习篇/登录认证篇]]

---

# 第一部分：Java 核心基础

---

## 1. 面向对象三大特性是什么？怎么理解？

### 封装
将对象的属性和方法包装在类内部，对外隐藏实现细节，只暴露公开接口。

```java
public class User {
    private String password;  // 私有，外部不可直接访问

    public void setPassword(String password) {
        this.password = encrypt(password); // 内部加密逻辑
    }
}
```

> **好处**：降低耦合、提高安全性、便于修改内部实现

### 继承
子类继承父类的属性和方法，形成类之间的层次关系。

- 子类拥有父类非 `private` 的属性和方法
- 子类可以覆盖（Override）父类的方法
- Java 只支持**单继承**（一个类只能有一个直接父类）

### 多态 ⭐
同一个行为在不同对象上有不同的表现形式。实现条件：
1. **继承**（或接口实现）
2. **重写**（Override）
3. **父类引用指向子类对象**

```java
Animal a = new Dog();
a.sound();  // 实际调用 Dog 的 sound()
```

多态的底层是**虚方法表（vtable）**——JVM 在类加载时构建方法表，运行时根据实际类型动态分派。

> [!tip] **多态 vs 重载**
> - **重载（Overload）**：编译时多态（静态分派），根据参数类型决定调用哪个方法
> - **重写（Override）**：运行时多态（动态分派），根据实际对象类型决定调用哪个方法

---

## 2. 抽象类和接口有什么区别？（JDK 8+）

| 对比维度 | 抽象类 | 接口 |
|---------|--------|------|
| 设计思想 | **"是什么"**（is-a）关系 | **"能做什么"**（can-do）能力 |
| 构造方法 | 可以有 | 不能有 |
| 成员变量 | 任意类型 | `public static final` 常量 |
| 方法实现 | 可以有抽象和非抽象方法 | default/static 方法（JDK 8+） |
| 多继承 | 单继承 | 接口可以多实现 |
| 访问修饰符 | 任意 | Java 9+ 支持 private 方法 |

> [!info] **JDK 版本演进**
> - **JDK 7**：接口只能有抽象方法 + 常量
> - **JDK 8**：接口新增 `default` 方法和 `static` 方法
> - **JDK 9**：接口新增 `private` 方法（辅助 default 方法复用）

---

## 3. ArrayList 和 LinkedList 的区别？

| 对比项 | ArrayList | LinkedList |
|--------|-----------|------------|
| 底层结构 | Object[] 动态数组 | 双向链表（Node 节点） |
| 随机访问 | **O(1)**，实现 RandomAccess 接口 | **O(n)**，需遍历 |
| 尾部插入 | **O(1)** 均摊（扩容偶尔 O(n)） | **O(1)** |
| 指定位置插入/删除 | **O(n)**（数组拷贝） | **O(n)**（需先遍历到位置，但本身操作 O(1)） |
| 内存占用 | 更紧凑（只存数据） | 更大（每个节点存 prev/next 指针） |
| 适用场景 | 频繁随机读取、尾部追加 | 频繁头部插入/删除、不确定大小 |

### ArrayList 扩容机制 ⭐

```java
// JDK 8 源码：grow() 方法
int newCapacity = oldCapacity + (oldCapacity >> 1); // 1.5 倍扩容
```

- 初始容量：默认 10（懒加载，第一次 add 时初始化）
- 扩容倍数：**1.5 倍**（位运算优化）
- 核心操作：`Arrays.copyOf()` 将原数组拷贝到新数组（**O(n)**）
- 如果预知数据量：`new ArrayList<>(initialCapacity)` 指定初始容量避免频繁扩容

---

## 4. HashMap 的实现原理？⭐（JDK 7 vs 8）

### 数据结构
- **JDK 7**：数组 + 链表（Entry 数组）
- **JDK 8**：数组 + 链表 + **红黑树**（Node 数组）

### Put 流程（JDK 8）⭐

```
① 计算 key.hashCode() → 二次扰动 (h ^ (h >>> 16))
② (n - 1) & hash → 计算桶下标
③ 如果桶为空 → 直接插入
④ 如果桶不为空 → 遍历链表/红黑树
   ├── 存在相同 key → 覆盖 value（返回旧值）
   └── 不存在相同 key → 尾插法插入
⑤ 插入后检查 size > threshold → 扩容（resize）
```

### JDK 8 优化的关键点

| 优化项 | JDK 7 | JDK 8 |
|-------|-------|-------|
| 数据结构 | 数组 + 链表 | 数组 + 链表 + **红黑树** |
| 插入方式 | **头插法**（死循环风险） | **尾插法**（解决多线程死循环） |
| 哈希算法 | 复杂扰动（4次位运算+5次异或） | 简化 `h ^ (h >>> 16)` |
| 树化条件 | 无 | 链表长度 ≥ 8 且数组长度 ≥ 64 |

### 红黑树化条件
- 链表长度 **≥ 8** 且数组长度 **≥ 64** → 链表转为红黑树
- 红黑树节点 **≤ 6** → 退化为链表
- 为什么是 8？——泊松分布，链表长度到 8 的概率极低（0.00000006），即**良好的 hash 分布下几乎不会触发树化**

### 扩容机制
- 默认容量：**16**
- 负载因子：**0.75**
- 扩容阈值：`capacity * loadFactor`（16 × 0.75 = 12）
- 扩容为原来的 **2 倍**
- 扩容后元素位置：要么在原位置，要么在 **原位置 + 旧容量**（得益于容量是 2 的幂次）

### 线程安全问题
> [!danger] HashMap **不是线程安全的**
> - JDK 7：多线程扩容时头插法可能导致**环形链表死循环**
> - JDK 8：尾插法解决死循环，但仍有数据覆盖问题
> - ✅ 线程安全方案：`ConcurrentHashMap` / `Collections.synchronizedMap()` / `Hashtable`

---

## 5. ConcurrentHashMap 的原理？⭐

### JDK 7：分段锁（Segment）
```java
ConcurrentHashMap 内含 Segment[]（继承 ReentrantLock）
每个 Segment 管理一部分 HashEntry
写入时只锁对应 Segment，其他 Segment 不受影响
```
- 默认 16 个 Segment → 支持 16 个线程并发写入
- 定位元素需要两次 hash（先定位 Segment，再定位 HashEntry）

### JDK 8：synchronized + CAS
| 机制 | 说明 |
|------|------|
| **CAS** | 插入空桶时，用 `casTabAt()` 无锁插入 |
| **synchronized** | 桶非空时，锁住链表/红黑树的头节点 |
| **红黑树** | 与 HashMap 一样，链表 > 8 转红黑树 |

> [!info] **JDK 8 比 JDK 7 的改进**
> 1. 锁粒度更细：锁头节点而非整个 Segment
> 2. 内存占用更少：去掉了 Segment 数组
> 3. 查询不需加锁：volatile 保证可见性
> 4. 扩容支持多线程协助（ForwardingNode、helpTransfer）

---

## 6. Java 异常体系？

```
Throwable
├── Error（不可处理，程序不应捕获）
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── NoClassDefFoundError
└── Exception
    ├── Checked Exception（必须处理，编译时检查）
    │   ├── IOException
    │   ├── SQLException
    │   └── ClassNotFoundException
    └── Unchecked Exception (RuntimeException，可不处理)
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── IndexOutOfBoundsException
        └── ConcurrentModificationException
```

### try-catch-finally 执行顺序 ⭐
```java
try {
    return 1;      // 注册返回值，但不立即返回
} catch (Exception e) {
    return 2;
} finally {
    return 3;      // ⚠ 会覆盖 try/catch 中的 return！
}
// 最终返回：3
```

> [!warning] **finally 中 return 的坑**
> - finally 块中的 return 会**覆盖** try/catch 中的 return
> - 阿里巴巴规范：**禁止在 finally 中使用 return**

### try-with-resources（JDK 7+）
```java
// 自动关闭资源（需实现 AutoCloseable）
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // 使用 fis
} // 自动调用 fis.close()
```

---

## 7. 反射的三种获取 Class 对象方式？

```java
// 方式一：类名.class（最安全，编译时检查）
Class<User> clazz1 = User.class;

// 方式二：对象.getClass()
Class<?> clazz2 = user.getClass();

// 方式三：Class.forName()（最灵活，可指定类名）
Class<?> clazz3 = Class.forName("com.example.User");
```

### 反射的性能问题及优化
- **性能开销大**：每次调用 `Method.invoke()` 都会做安全检查
- **优化方案**：
  1. `method.setAccessible(true)` — 跳过 Java 权限检查
  2. 缓存 Method/Field 对象（避免反复获取）
  3. 使用 `MethodHandles.lookup()`（JDK 7+，比反射更高效）

> [!info] **反射在框架中的典型应用**
> - Spring IoC：通过反射 + 工厂模式创建和管理 Bean
> - MyBatis Mapper：动态代理生成接口实现类
> - 注解解析：`getAnnotation()` 获取自定义注解

---

## 8. BIO、NIO、AIO 的区别？

| 模型 | 全称 | 特点 | 适用场景 |
|------|------|------|---------|
| **BIO** | Blocking IO | 同步阻塞，一个连接一个线程 | 连接少、低并发（传统 Socket） |
| **NIO** | Non-blocking IO | 同步非阻塞，多路复用 | 连接多、短连接（Netty、Tomcat） |
| **AIO** | Async IO | 异步非阻塞，回调机制 | 连接多、长连接（文件操作） |

### NIO 三大核心 ⭐

```
Channel（通道）     — 双向读写，类似水管的通道
   ↓
Buffer（缓冲区）    — 数据载体，所有读写通过 Buffer
   ↓
Selector（选择器）  — 单线程管理多个 Channel 的事件
```

- **NIO 是 IO 多路复用**：一个 Selector 管理数千个 Channel，有事件就处理，无事件就阻塞
- **零拷贝**：`FileChannel.transferTo()` 直接将数据从文件发送到网络，无需经过用户态

---

## 9. Java 8+ 主要新特性？

### Lambda 表达式
```java
// 传统 vs Lambda
list.sort(new Comparator<User>() {
    public int compare(User a, User b) { return a.age - b.age; }
});
list.sort((a, b) -> a.age - b.age);  // Lambda
```

### Stream API ⭐
```java
// 中间操作（lazy）+ 终端操作（触发执行）
list.stream()
    .filter(u -> u.age > 18)           // 中间：过滤
    .map(User::getName)                 // 中间：映射
    .sorted()                           // 中间：排序
    .collect(Collectors.toList());      // 终端：收集
```

### Optional
```java
Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("未知");
```

### CompletableFuture（异步编排）
```java
CompletableFuture.supplyAsync(() -> getPrice(id))
    .thenApply(price -> price * 0.9)
    .thenAccept(System.out::println);
```

---

# 第二部分：JVM ⭐

---

## 10. JVM 运行时内存结构？

```
┌────────────────────────────────────────┐
│             方法区（元空间）              │ ← 类信息、常量、静态变量
├────────────────────────────────────────┤
│                  堆                    │ ← 几乎所有对象实例
│  ┌───────┬──────┬───────┬────────┐    │
│  │ Eden │ S0  │ S1  │ Old   │    │
│  └───────┴──────┴───────┴────────┘    │
├────────────────────────────────────────┤
│         虚拟机栈（线程私有）              │ ← 栈帧：局部变量表、操作数栈
├────────────────────────────────────────┤
│         本地方法栈（线程私有）             │ ← native 方法调用
├────────────────────────────────────────┤
│          程序计数器（线程私有）            │ ← 当前线程执行的字节码行号
└────────────────────────────────────────┘
```

> [!info] **JDK 8 重大变化：元空间取代永久代**
> - 永久代（PermGen）→ 元空间（Metaspace）
> - 元空间使用**本地内存**（而非 JVM 堆内存）
> - 解决了永久代 OOM 问题和字符串常量池溢出问题

---

## 11. 对象在内存中的布局？

一个对象在堆内存中由三部分组成：

```
┌──────────────────────┐
│    对象头 (Header)    │ ← Mark Word + 类指针（+ 数组长度）
├──────────────────────┤
│    实例数据 (Data)    │ ← 成员变量值
├──────────────────────┤
│    对齐填充 (Padding) │ ← 8 字节对齐
└──────────────────────┘
```

### Mark Word（关键，与锁相关）
| 状态 | 标记位 | 存储内容 |
|------|:-----:|---------|
| 无锁 | 01 | 对象的 hashCode、分代年龄、偏向锁标志（0） |
| 偏向锁 | 01 | 偏向线程 ID、偏向时间戳、分代年龄、偏向锁标志（1） |
| 轻量级锁 | 00 | 指向栈中锁记录的指针 |
| 重量级锁 | 10 | 指向互斥量（Monitor）的指针 |
| GC 标记 | 11 | 空（不存储任何信息） |

### 对象的创建过程 ⭐

```
① 类加载检查：检查 new 指令的参数能否在常量池定位到类的符号引用
② 分配内存：从堆中划出一块内存（指针碰撞 / 空闲列表）
③ 内存初始化零值：将分配到的内存全部设为 0
④ 设置对象头：Mark Word + 类指针
⑤ 执行 <init> 方法：即构造函数
```

---

## 12. 如何判断对象可回收？

### 引用计数法（主流语言不用）
- 每个对象维护一个引用计数器
- ❌ 无法解决**循环引用**问题

### 可达性分析（Java 使用）⭐
- 从 **GC Roots** 对象出发向下搜索，不可达的对象即为可回收
- **GC Roots** 包括：
  - 虚拟机栈（栈帧中的局部变量表）中引用的对象
  - 方法区中静态属性引用的对象
  - 方法区中常量引用的对象
  - 本地方法栈中 JNI（native 方法）引用的对象

### 引用类型对比 ⭐

| 引用类型 | 回收时机 | 典型用途 |
|---------|---------|---------|
| **强引用** | `new Object()`，永不回收 | 常规对象 |
| **软引用** | 内存不足时回收 | 缓存（图片缓存） |
| **弱引用** | 下一次 GC 即回收 | ThreadLocal、WeakHashMap |
| **虚引用** | 随时，get 永远返回 null | 管理直接内存（NIO） |

```java
// 软引用 — OOM 前会被回收
SoftReference<byte[]> cache = new SoftReference<>(new byte[1024]);

// 弱引用 — 下次 GC 就被回收
WeakReference<Object> ref = new WeakReference<>(new Object());
```

---

## 13. 垃圾回收算法？

| 算法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| **标记-清除** | 标记存活对象→清除未标记对象 | 基础算法实现简单 | 内存碎片、效率不高 |
| **标记-复制** | 将内存分为两块，存活对象复制到另一块 | 无碎片、分配高效 | 可用内存减半 |
| **标记-整理** | 标记存活对象→向一端移动→清理边界外 | 无碎片、内存利用率高 | 移动对象开销大 |
| **分代收集** | 新生代=复制，老年代=标记-清除/整理 | 结合各算法优势 | 需要分代设计 |

### 分代收集策略（实际使用）⭐
```
新生代（Minor GC）
  Eden + S0 + S1 = 8:1:1
  采用标记-复制算法
  存活对象从 Eden → S0/S1 → 晋升老年代

老年代（Major GC / Full GC）
  采用标记-清除（CMS）或标记-整理（G1）
```

---

## 14. 常见的垃圾收集器？⭐

### Serial / ParNew
- **Serial**：单线程，-XX:+UseSerialGC，适合客户端、单核场景
- **ParNew**：Serial 的多线程版本，用于新生代，配合 CMS 使用

### CMS（Concurrent Mark Sweep）⭐
```
① 初始标记（STW）      — 标记 GC Roots 直接关联的对象
② 并发标记              — 从 GC Roots 开始遍历对象图（与用户线程并发）
③ 重新标记（STW）      — 修正并发标记期间变动的对象
④ 并发清除              — 清除不可达对象（与用户线程并发）
```
- **优点**：并发收集、停顿短
- **缺点**：**浮动垃圾**（并发标记期间产生的垃圾无法当次清理）、内存碎片、无法处理"并发失败"

### G1（Garbage First）⭐⭐
```
核心思想：将堆划分为 2048 个 Region，每个 Region 可以是 Eden/Survivor/Old
优先回收垃圾最多的 Region（Garbage First 的由来）
```
- **停顿可控**：-XX:MaxGCPauseMillis 指定目标停顿时间（默认 200ms）
- **Mixed GC**：同时回收新生代 + 部分老年代 Region
- **JDK 9+** 默认收集器
- **Remembered Set**：记录跨 Region 引用，避免全堆扫描

### ZGC（JDK 11+，低延迟标杆）
- 核心：**染色指针** + **读屏障** + **并发映射**
- 停顿时间 < **10ms**，与堆大小无关
- 支持 TB 级堆
- **JDK 21+** 已支持分代 ZGC

> [!tip] **选型建议**
> - JDK 8 默认：Parallel（吞吐优先）
> - 响应优先：JDK 8 + CMS / JDK 11+ G1
> - 极致低延迟：JDK 17+ ZGC / Shenandoah

---

## 15. 类加载机制？双亲委派模型？

### 类加载的 7 个阶段
```
加载(Load) → 验证(Verify) → 准备(Prepare) → 解析(Resolve) → 初始化(Init) → 使用(Use) → 卸载(Unload)
```
- 解析阶段：将常量池中的符号引用替换为直接引用
- 初始化阶段：执行 `<clinit>()` 方法（收集所有 static 赋值 + static 代码块）

### 双亲委派模型 ⭐
```
┌──────────┐
│ Bootstrap│ ← C++ 实现，加载 rt.jar
│ ClassLoader│
└────┬─────┘
     ↓
┌──────────┐
│ Extension│ ← 加载 jre/lib/ext/*.jar
│ ClassLoader│
└────┬─────┘
     ↓
┌──────────┐
│  Application│ ← 加载 classpath 下的类
│  ClassLoader│
└──────────┘
```

**工作流程**：当一个类加载器收到加载请求，它不会自己加载，而是**委托给父加载器**，父加载器再向上委托，直到 Bootstrap ClassLoader。如果父加载器无法加载（找不到该类），才由子加载器自己尝试加载。

> [!question] **为什么要双亲委派？**
> 1. **安全性**：防止核心 API 被篡改（如自己写 `java.lang.Object` 不会被加载）
> 2. **唯一性**：保证同一个类只被加载一次

### 打破双亲委派
- **Tomcat**：为每个 Web App 提供独立的 ClassLoader，优先加载 Web 应用目录下的类
- **SPI（Service Provider Interface）**：JDBC 驱动加载，启动类加载器无法加载 SPI 实现类，用 `Thread.currentThread().getContextClassLoader()` 获取线程上下文加载器
- **热部署**：每次重启创建新的 ClassLoader 实例

---

## 16. JVM 调优命令和 OOM 排查？

### 常用命令 ⭐
| 命令 | 用途 |
|------|------|
| `jps -l` | 查看 Java 进程 PID |
| `jstat -gcutil pid 1000` | 每秒查看 GC 情况（YGC/YGCT/FGC/FGCT） |
| `jmap -dump:format=b,file=heap.hprof pid` | 导出堆转储快照 |
| `jstack pid` | 查看线程栈（排查死锁、CPU 高） |
| `jinfo -flags pid` | 查看 JVM 参数 |
| `jcmd pid VM.flags` | 更全面的 JVM 参数查看 |

### CPU 100% 排查流程 ⭐
```
① top -Hp pid  → 找到 CPU 最高的线程 tid
② printf "%x\n" tid  → 转为 16 进制 nid
③ jstack pid | grep nid  → 查看该线程的堆栈
```

### OOM 场景
| 类型 | 原因 | 参数 | 排查 |
|------|------|------|------|
| 堆溢出 | 对象无法回收 / 创建过多 | -Xmx | MAT 分析大对象 |
| 栈溢出 | 递归太深 | -Xss | 看栈深度 |
| 元空间溢出 | 类加载过多 / CGLIB | -XX:MaxMetaspaceSize | 检查类加载器 |

> [!tip] **Arthas 推荐**
> 阿里开源的 Java 诊断神器，`trace` / `watch` / `dashboard` 命令比传统 jdk 工具更方便

---

# 第三部分：并发编程 ⭐⭐

---

## 17. 线程的 6 种状态及转换？

```
NEW ──→ RUNNABLE ──→ TERMINATED
              ↕        ↕
           BLOCKED    WAITING
              ↕        ↕
           TIMED_WAITING
```

| 状态 | 说明 |
|------|------|
| **NEW** | 创建后未启动 `new Thread()` |
| **RUNNABLE** | 调用了 `start()`，正在运行或等待 CPU 时间片 |
| **BLOCKED** | 等待进入 synchronized 代码块/方法（锁竞争失败） |
| **WAITING** | `Object.wait()` / `Thread.join()` / `LockSupport.park()` |
| **TIMED_WAITING** | `Thread.sleep(ms)` / `wait(timeout)` / `join(ms)` |
| **TERMINATED** | 执行完毕 |

> [!info] **`wait()` vs `sleep()` vs `yield()` vs `join()`**
> - **`wait()`**：释放锁，进入 WAITING，需要 notify 唤醒
> - **`sleep()`**：不释放锁，TIMED_WAITING，时间到自动唤醒
> - **`yield()`**：让出 CPU 时间片，但仍处于 RUNNABLE（可能再次被调度）
> - **`join()`**：等待目标线程执行完毕

---

## 18. synchronized 底层原理？⭐

### 三种应用方式
| 方式 | 锁对象 | 作用范围 |
|------|--------|---------|
| 实例方法 | `this`（当前实例） | 整个方法 |
| 静态方法 | `类.class` | 整个静态方法 |
| 代码块 | 指定的对象 | 指定代码块 |

### 锁升级过程（JDK 6 优化）⭐
```
无锁 → 偏向锁 → 轻量级锁 → 重量级锁（不可逆）
```

| 锁状态 | 原理 | 开销 | 适用场景 |
|--------|------|:----:|---------|
| **偏向锁** | Mark Word 记录线程 ID，同线程再次进入无需 CAS | 极低 | 单线程反复获取同一把锁 |
| **轻量级锁** | CAS 自旋尝试获取锁，不阻塞线程 | 低 | 少量线程竞争，短时间执行 |
| **重量级锁** | 获取不到就阻塞挂起线程（操作系统互斥量） | 高 | 多线程竞争激烈，执行时间长 |

### Monitor 机制
- synchronized 底层依赖操作系统的 **Monitor**（监视器锁）
- 每个对象都有一个 Monitor 与之关联
- 重量级锁通过 Monitor 实现线程的阻塞和唤醒（用户态 → 内核态切换）

---

## 19. AQS 原理是什么？⭐

> **AQS**（AbstractQueuedSynchronizer）是 Java 并发包的基石，ReentrantLock、CountDownLatch、Semaphore 等都基于 AQS 实现。

### 核心组成
```
state（volatile int 同步状态）
    ↓
CLH 双向队列（等待队列）
    ├── head → Node {thread, waitStatus, prev, next}
    ├── ...
    └── tail
```

### 核心方法（模板方法模式）
| 独占模式 | 共享模式 |
|---------|---------|
| `acquire(arg)` | `acquireShared(arg)` |
| `release(arg)` | `releaseShared(arg)` |
| `tryAcquire(arg)` | `tryAcquireShared(arg)` |
| `tryRelease(arg)` | `tryReleaseShared(arg)` |

### 以 ReentrantLock 为例
```java
// 非公平锁加锁流程
① compareAndSetState(0, 1)  → 尝试 CAS 修改 state
   ├── 成功 → 当前线程获得锁（设置 exclusiveOwnerThread）
   └── 失败 → acquire(1) → tryAcquire → 再次尝试 CAS
              → 失败 → addWaiter 加入 CLH 队列 → acquireQueued 阻塞
```

> [!info] **ReentrantLock 的公平 vs 非公平**
> - **非公平锁**（默认）：加锁时直接 CAS 抢锁，抢不到才排队。**吞吐量更高**，但可能"插队"导致线程饥饿
> - **公平锁**：严格按照 FIFO 顺序获取锁。先检查队列是否有前驱节点 `hasQueuedPredecessors()`

---

## 20. volatile 关键字的作用？⭐

### 两大语义
| 语义 | 说明 |
|------|------|
| **可见性** | 一个线程修改 volatile 变量，其他线程立即可见 |
| **禁止指令重排序** | 在 volatile 变量读写前后插入内存屏障 |

### 实现原理
- **可见性**：volatile 变量在写时会强制将缓存行刷新到主存，并触发其他 CPU 的缓存行失效（**MESI 缓存一致性协议**）
- **内存屏障**：
  ```
  StoreStore屏障
  volatile 写操作
  StoreLoad屏障    ← 保证 volatile 写之前的普通变量不会重排序到写之后
  -------------------------
  LoadLoad屏障
  volatile 读操作
  LoadStore屏障    ← 保证 volatile 读之后的普通变量不会重排序到读之前
  ```

### 为什么 volatile 不保证原子性？
```java
volatile int count = 0;
count++;  // 不是原子操作：读-改-写三步，中间可能被中断
```
- ✅ **保证**：读到的值是最新的
- ❌ **不保证**：多个线程同时 `count++` 的安全

### volatile vs synchronized
| volatile | synchronized |
|----------|-------------|
| 轻量级，无锁 | 重量级，有锁 |
| 只能修饰变量 | 修饰方法/代码块 |
| 保证可见性，不保证原子性 | 既保证可见性，又保证原子性 |
| 不会阻塞线程 | 可能阻塞线程 |

---

## 21. 线程池核心参数和执行流程？⭐⭐

### 七大核心参数
```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    corePoolSize,          // 核心线程数
    maximumPoolSize,       // 最大线程数
    keepAliveTime,         // 空闲线程存活时间
    TimeUnit.SECONDS,      // 时间单位
    new ArrayBlockingQueue<>(queueSize), // 阻塞队列
    Executors.defaultThreadFactory(),    // 线程工厂
    new AbortPolicy()      // 拒绝策略
);
```

### 执行流程 ⭐
```
① 提交任务 → 检查线程数 < corePoolSize
   ├── 是 → 创建新核心线程执行任务
   └── 否 → ② 尝试放入阻塞队列
            ├── 队列未满 → 入队等待
            └── 队列已满 → ③ 检查线程数 < maximumPoolSize
                          ├── 是 → 创建新非核心线程执行任务
                          └── 否 → ④ 执行拒绝策略
```

### 四种拒绝策略 ⭐
| 策略 | 行为 |
|------|------|
| **AbortPolicy**（默认） | 直接抛出 RejectedExecutionException |
| **CallerRunsPolicy** | 由提交任务的线程自己执行（压回调用者） |
| **DiscardPolicy** | 直接丢弃任务，不抛异常 |
| **DiscardOldestPolicy** | 丢弃队列中最旧的任务，重试提交 |

### 常见线程池的问题
```java
// ⚠ 这些是 Executors 提供的快捷方式，都有坑！
Executors.newFixedThreadPool(10);     // → LinkedBlockingQueue 无界队列，OOM 风险
Executors.newCachedThreadPool();      // → SynchronousQueue，最大线程无限，OOM 风险
Executors.newSingleThreadExecutor();  // → 无界队列，OOM 风险
```
> [!danger] **阿里巴巴规约**：禁止使用 Executors 创建线程池，必须用 ThreadPoolExecutor 手动指定参数

### 如何合理设置线程池？⭐
```
CPU 密集型：corePoolSize = CPU 核数 + 1
IO 密集型：corePoolSize = CPU 核数 × 2（or 更多）
```
更精确的公式：
```
线程数 = CPU核数 × (1 + 等待时间 / 计算时间)
```

---

## 22. ThreadLocal 原理和内存泄漏问题？

### 原理
```java
ThreadLocal<String> tl = new ThreadLocal<>();
tl.set("value");
```
```
每个 Thread 内部有一个 ThreadLocalMap（键值对）
  └── key = ThreadLocal 对象（弱引用）
  └── value = 线程局部变量（强引用）
```

### 内存泄漏问题 ⭐
> [!danger] **核心问题**
> ```
> ThreadLocal → key 是弱引用（WeakReference）
> GC 后 key 被回收 → key = null
> value 是强引用（仍被 ThreadLocalMap 中的 Entry 引用）
> ↳ value 永远无法被访问，也无法被回收 → 内存泄漏！
> ```

### 正确的使用方式
```java
ThreadLocal<String> tl = new ThreadLocal<>();
try {
    tl.set("value");
    // ... 使用
} finally {
    tl.remove();  // ✅ 使用完必须 remove
}
```

### 应用场景
- **线程上下文传递**（Request 上下文、用户信息）
- **数据库连接管理**（每个线程持有一个 Connection）
- **SimpleDateFormat** 线程不安全，用 ThreadLocal 包装
- **Spring 事务**：`TransactionSynchronizationManager` 使用 ThreadLocal 持有连接资源

---

# 第四部分：Spring 全家桶

---

## 23. Spring Boot 自动配置原理是什么？⭐

### 核心注解 `@SpringBootApplication`
```java
@SpringBootApplication = @SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan
```

### `@EnableAutoConfiguration` 原理 ⭐
```
① @Import(AutoConfigurationImportSelector.class)
② AutoConfigurationImportSelector 扫描 META-INF/spring.factories
③ 获取 EnableAutoConfiguration 对应的所有配置类全限定名列表
④ 通过 @Conditional 条件注解判断是否要加载该配置
⑤ 条件满足 → 将配置类中的 Bean 注入容器
```

### 条件注解家族
| 注解 | 作用 |
|------|------|
| `@ConditionalOnClass` | classpath 存在指定类时加载 |
| `@ConditionalOnMissingBean` | 容器中不存在指定 Bean 时加载 |
| `@ConditionalOnProperty` | 配置文件中存在指定属性时加载 |
| `@ConditionalOnWebApplication` | 当前是 Web 应用时加载 |
| `@ConditionalOnExpression` | SpEL 表达式为 true 时加载 |

### 自定义 Starter
```java
// 1. 自动配置类
@Configuration
@ConditionalOnClass(MyService.class)
public class MyAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public MyService myService() {
        return new MyService();
    }
}

// 2. spring.factories
// org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
//   com.example.MyAutoConfiguration

// 3. 配置属性绑定
@ConfigurationProperties(prefix = "my.config")
public class MyProperties { ... }
```

---

## 24. Spring Cloud 核心组件有哪些？⭐

### 组件对比总览
| 功能 | Spring Cloud | Spring Cloud Alibaba |
|------|-------------|---------------------|
| 注册中心 | Eureka（已停更） | **Nacos** |
| 配置中心 | Config | **Nacos** |
| 网关 | Gateway / Zuul | **Gateway** |
| 熔断降级 | Hystrix（已停更） | **Sentinel** |
| 负载均衡 | Ribbon（已停更）→ **LoadBalancer** | **LoadBalancer** |
| 远程调用 | Feign → **OpenFeign** | **OpenFeign** |
| 分布式事务 | — | **Seata** |
| 链路追踪 | Sleuth + Zipkin | **Skywalking** |

### Nacos（注册中心 + 配置中心）⭐
```yaml
# 注册中心
spring.cloud.nacos.discovery.server-addr=127.0.0.1:8848

# 配置中心（动态刷新）
spring.cloud.nacos.config.server-addr=127.0.0.1:8848
spring.cloud.nacos.config.refresh-enabled=true
```

**AP/CP 模式切换**：
- **AP**（默认）：可用性优先，适合服务注册发现
- **CP**：一致性优先，适合配置管理

**Nacos 与 Eureka 对比**：
| 特性 | Nacos | Eureka |
|------|-------|--------|
| CAP | AP/CP 可切换 | AP |
| 配置中心 | ✅ 自带 | ❌ 需 Config |
| 健康检查 | 心跳 + 主动探活 | 心跳 |
| 控制台 | 功能丰富 | 简陋 |

### Gateway ⭐
```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("order_route", r -> r.path("/order/**")
            .filters(f -> f
                .addRequestHeader("X-Request-Source", "gateway")
                .circuitBreaker(c -> c.setName("orderCB").setFallbackUri("/fallback")))
            .uri("lb://order-service"))
        .build();
}
```

**Gateway 核心概念**：
- **Route**：路由规则（ID + 目标 URI + 断言集合 + 过滤器集合）
- **Predicate**：匹配条件（Path、Header、Method、Cookie、Query 等）
- **Filter**：请求/响应拦截（Pre/Post 过滤器链）

### Sentinel（流量控制）⭐
```java
// 资源定义
@SentinelResource(value = "getOrder", fallback = "fallbackHandler")

// 配置规则（支持动态 Push 到 Nacos）
- 流量控制：QPS 阈值、并发线程数
- 熔断降级：慢调用比例、异常比例、异常数
- 热点参数：对特定参数值限流
- 系统规则：Load、CPU、RT 自适应
```

### Seata（分布式事务）
| 模式 | 原理 | 适用场景 |
|------|------|---------|
| **AT** | 自动补偿，基于本地事务 + 全局锁 | 简单 SQL，高性能 |
| **TCC** | Try-Confirm-Cancel 手动编码 | 复杂业务逻辑 |
| **Saga** | 长事务模式，业务补偿 | 跨服务长时间事务 |

---

## 25. JWT 和 OAuth 2.0 原理？⭐

### JWT（JSON Web Token）

**结构**：`Header.Payload.Signature`
```
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"sub": "userId", "exp": 1700000000, "iat": 1690000000}
Signature: HMACSHA256(base64(Header) + "." + base64(Payload), secret)
```

**JWT 认证流程**：
```
① 用户登录 → 服务端验证身份 → 签发 JWT Token
② 客户端存储 Token（localStorage / 内存）
③ 后续请求在 Authorization Header 携带 Token
④ 服务端验证 Token 签名和有效期 → 提取用户信息
```

> [!warning] **JWT 痛点**
> - **无法主动失效**：签发后无法在服务端主动踢下线
> - **续期方案**：Refresh Token 双 Token 机制（access_token 短时效 + refresh_token 长时效）
> - **注销**：维护黑名单（Redis），每次请求校验

### OAuth 2.0 四种授权模式 ⭐
| 模式 | 适用场景 | 安全等级 |
|------|---------|:-------:|
| **授权码模式** | 第三方应用接入（最常用） | ⭐⭐⭐ |
| 密码模式 | 自家应用（不推荐） | ⭐⭐ |
| 客户端模式 | 服务端到服务端（无用户参与） | ⭐⭐ |
| 隐式模式 | 纯前端应用（已淘汰） | ⭐ |

**授权码流程（核心）**：
```
① 用户点击"微信登录" → 跳转微信授权页面
② 用户确认授权 → 微信回调第三方应用（携带 code）
③ 第三方服务端用 code 向微信换取 access_token
④ 用 access_token 获取用户信息
```

---

# 第五部分：数据库

---

## 26. MySQL 索引原理（B+ 树）？⭐

### 为什么用 B+ 树？
| 数据结构 | 磁盘 IO 次数 | 范围查询 | 说明 |
|---------|:-----------:|:--------:|------|
| 二叉搜索树 | O(log n) | ❌ 差 | 数据量大时树太高，磁盘 IO 多 |
| 红黑树 | O(log n) | ❌ 差 | 同样树高问题 |
| B 树 | O(log_m n) | ❌ 中序 | 节点同时存数据+指针，IO 少但范围差 |
| **B+ 树** ✅ | **O(log_m n)** | ✅ **极优** | 非叶子节点不存数据，叶子节点链表连接 |

### B+ 树的核心优势
- **非叶子节点只存索引**：一个节点可存更多 key，树更矮，磁盘 IO 更少
- **叶子节点形成有序链表**：范围查询只需遍历链表，无需回溯
- **所有数据都在叶子节点**：查询效率稳定

### 聚簇索引 vs 二级索引 ⭐
```
聚簇索引（InnoDB 主键索引）
  └── 叶子节点存储整行数据
  └── 一张表只有一个聚簇索引

二级索引（普通索引）
  └── 叶子节点存储主键值
  └── 查询需要"回表"：二级索引 → 主键 → 聚簇索引查数据
```

> [!info] **覆盖索引优化**
> 查询的列全部在索引中，无需回表：
> ```sql
> -- idx_name_age(name, age) 联合索引
> SELECT name, age FROM user WHERE name = '张三';  -- 覆盖索引，不回表
> ```

### 联合索引的最左前缀原则
```sql
-- 联合索引 (a, b, c)
-- ✅ 命中索引：WHERE a=1 / WHERE a=1 AND b=2 / WHERE a=1 AND b=2 AND c=3
-- ✅ 部分命中：WHERE a=1 AND c=3（仅 a 走索引，c 条件需回表过滤）
-- ❌ 不走索引：WHERE b=2 / WHERE c=3 / WHERE b=2 AND c=3
```

### 索引下推（ICP，JDK 5.6+）
```sql
-- 联合索引 (name, age)
SELECT * FROM user WHERE name LIKE '张%' AND age = 18;
-- 没有 ICP：存储引擎根据 name 模糊匹配查到主键 → 回表 → MySQL 过滤 age
-- 有 ICP ⭐：存储引擎在索引层面同时过滤 age → 减少回表次数
```

---

## 27. MySQL 事务隔离级别和 MVCC 原理？⭐⭐

### 事务的 ACID
| 特性 | 含义 | 实现 |
|------|------|------|
| **A** 原子性 | 事务要么全成功，要么全回滚 | undo log |
| **C** 一致性 | 事务前后数据一致 | 应用层 + 数据库约束 |
| **I** 隔离性 | 并发事务互不干扰 | 锁 + MVCC |
| **D** 持久性 | 提交后数据永久保存 | redo log |

### 隔离级别（加粗为默认）
| 级别 | 脏读 | 不可重复读 | 幻读 |
|------|:---:|:---------:|:---:|
| READ-UNCOMMITTED | ✅可能 | ✅可能 | ✅可能 |
| **READ-COMMITTED**（RC，大多数默认） | ❌ | ✅可能 | ✅可能 |
| **REPEATABLE-READ**（RR，MySQL 默认） | ❌ | ❌ | ✅部分解决 |
| SERIALIZABLE | ❌ | ❌ | ❌ |

### MVCC（多版本并发控制）⭐
> **核心思想**：同一条记录在数据库中维护多个版本（undo log 链），每个事务看到的是某个时间点的快照

**三个关键组件**：
```
隐藏字段：
  DB_TRX_ID — 记录最后修改该行的事务 ID
  DB_ROLL_PTR — 指向 undo log 回滚指针

undo log 链：
  版本链：v1 ← v2 ← v3（每个版本记录修改前的数据）

ReadView（读视图）：
  事务启动时生成，包含：
  - m_ids：活跃事务 ID 集合
  - min_trx_id：最小活跃事务 ID
  - max_trx_id：最大事务 ID + 1
  - creator_trx_id：当前事务 ID
```

**可见性判断规则**：
```
① DB_TRX_ID == creator_trx_id → ✅ 可见（自己修改的）
② DB_TRX_ID < min_trx_id → ✅ 可见（已提交的事务）
③ DB_TRX_ID >= max_trx_id → ❌ 不可见（未来事务）
④ min_trx_id <= DB_TRX_ID < max_trx_id：
   在 m_ids 中 → ❌ 不可见
   不在 m_ids 中 → ✅ 可见
```

### RC vs RR 的区别
| 对比 | RC | RR |
|------|:--:|:--:|
| ReadView 生成时机 | **每次查询**都生成 | **事务第一次查询**时生成 |
| 幻读 | ✅ 可能 | ❌ MVCC + Gap Lock 解决 |
| 性能 | 更高 | 略低（Gap Lock 开销） |

---

## 28. MySQL 锁机制？

### 锁分类
```
按粒度：行锁、间隙锁、临键锁、表锁、意向锁
按模式：共享锁(S)、排他锁(X)、意向共享锁(IS)、意向排他锁(IX)
按算法：Record Lock、Gap Lock、Next-Key Lock
```

### 三种行锁算法 ⭐
```sql
-- 注意：锁的都是"索引项"，不是行记录！

-- ① Record Lock（记录锁）：锁住索引记录
SELECT * FROM user WHERE id = 1 FOR UPDATE;  -- id=1 的记录

-- ② Gap Lock（间隙锁）：锁住索引之间的间隙，防止幻读
SELECT * FROM user WHERE id BETWEEN 10 AND 20 FOR UPDATE;
-- 锁住 (10, 20) 的间隙，不让插入 id=15 的记录

-- ③ Next-Key Lock（临键锁）= Record Lock + Gap Lock
-- InnoDB RR 级别默认使用，通过 Gap Lock 解决幻读
```

> [!info] **加锁规则（林晓斌"丁奇"总结）**
> 1. 加锁的基本单位是 **Next-Key Lock**（前开后闭）
> 2. 等值查询时，最后一个不等的索引项退化为 **Record Lock**
> 3. 唯一索引等值查询时，退化为 **Record Lock**（行锁）
> 4. 索引上的范围查询会锁到第一个不满足条件的值

---

## 29. Redis 数据类型的底层实现？⭐

| 数据类型 | 底层编码（REDIS 6/7） | 说明 |
|---------|---------------------|------|
| **String** | int / embstr / raw | int：整数；embstr：短字符串（<44B）；raw：长字符串 |
| **List** | quicklist | 压缩列表 + 双向链表组合（3.2+） |
| **Set** | intset / hashtable | intset：整数集合（全整数且少）；ht：哈希表 |
| **ZSet** | **ziplist / skiplist** | ziplist：少量有序；**skiplist**：大量（跳表+哈希表） |
| **Hash** | ziplist / **hashtable** | ziplist：少量字段；ht：大量字段 |
| **Geo** | zset（skiplist） | 经纬度编码为 score，存入 zset |
| **HyperLogLog** | 固定 12KB | 基数统计，误差 0.81% |
| **Bitmap** | String 的位操作 | SETBIT / GETBIT / BITCOUNT |

### 跳表（skiplist）为什么是 ZSet 的核心？⭐
```
Redis ZSet 使用【跳表 + 哈希表】双结构：
  - 哈希表：O(1) 查 value → score
  - 跳表：O(log n) 范围查询、排序

跳表本质：有序链表 + 多级索引
  层数：1/2 概率上升（最高 32 层）
```

---

## 30. Redis 缓存设计和三大问题？⭐⭐

### 缓存穿透
```
描述：查询一个【不存在】的数据，缓存和数据库都没有
后果：请求直接打到数据库，可能压垮 DB
```
**解决方案**：
- **布隆过滤器**（Bloom Filter）：将所有可能的 key 存入过滤器，请求不存在的 key 直接拦截
- **缓存空值**：查询结果为 null 也缓存（短 TTL）

### 缓存击穿
```
描述：热点 key 在缓存过期的一瞬间，大量请求同时涌入数据库
后果：数据库压力瞬间增大，可能宕机
```
**解决方案**：
- **互斥锁**（SETNX）：第一个请求获取锁查数据库，其他请求等待后读取缓存
- **逻辑过期**：缓存不设置 TTL，而是存一个逻辑过期时间，发现过期后加锁异步更新

### 缓存雪崩
```
描述：大量 key 同时过期，或 Redis 宕机，所有请求直接打到数据库
后果：数据库被打崩
```
**解决方案**：
- **过期时间加随机值**：避免大量 key 同一时间过期
- **Redis 高可用**：主从 + Sentinel / Cluster
- **本地缓存**：Guava Cache / Caffeine 做二级缓存
- **限流降级**：Sentinel 保护服务

### 缓存一致性 ⭐
```java
// ✅ 推荐方案：先更新数据库，再删除缓存
public void updateUser(User user) {
    // 1. 更新数据库
    userDao.update(user);
    // 2. 删除缓存（下次查询再写入）
    redisTemplate.delete("user:" + user.getId());
}
```

**延迟双删**（保证最终一致）：
```java
// 延迟双删：先删缓存 → 更新 DB → 等待 N 毫秒 → 再删缓存
redisTemplate.delete(key);
userDao.update(user);
Thread.sleep(500);               // 等待可能读取旧数据写缓存的线程完成
redisTemplate.delete(key);        // 再次删除
```

---

## 31. Redis 分布式锁？⭐

```java
// 加锁
String uuid = UUID.randomUUID().toString();
Boolean locked = redisTemplate.opsForValue()
    .setIfAbsent("lock:order:" + orderId, uuid, 30, TimeUnit.SECONDS);

// 解锁（必须用 Lua 脚本保证原子性！）
String luaScript = "if redis.call('get', KEYS[1]) == ARGV[1] then " +
                   "return redis.call('del', KEYS[1]) " +
                   "else return 0 end";
redisTemplate.execute(new DefaultRedisScript<>(luaScript, Long.class),
    Arrays.asList("lock:order:" + orderId), uuid);
```

**Redisson 看门狗机制**：
```java
RLock lock = redissonClient.getLock("lock:order:" + orderId);
lock.lock(30, TimeUnit.SECONDS);  // 看门狗自动续期（默认每 10s 续期一次）
```

> [!info] **面试金句：Redisson 分布式锁核心**
> - 加锁：Lua 脚本 `hset lockName threadId 1` + 设置过期时间
> - 看门狗：后台线程每 10s 检查一次，锁还在就续期到 30s
> - 解锁：Lua 脚本校验线程身份 → 删除 key → 发布解锁消息（通知其他线程）

---

# 第六部分：中间件

---

## 32. MyBatis-Plus 核心特性？

| 特性 | 作用 |
|------|------|
| **分页插件** | `PageHelper` / `MyBatisPlusInterceptor` 自动拦截 SQL 拼装 COUNT 和 LIMIT |
| **条件构造器** | `QueryWrapper` / `LambdaQueryWrapper` 链式构造 WHERE 条件 |
| **代码生成器** | `AutoGenerator` 自动生成 Entity/Mapper/Service/Controller |
| **逻辑删除** | `@TableLogic` 注解，删除变更新 |
| **乐观锁插件** | `@Version` 注解，更新时自动检查版本 |
| **自动填充** | `@TableField(fill = FieldFill.INSERT)` 自动填充创建时间 |

---

## 33. 消息队列：RabbitMQ vs Kafka？

| 对比维度 | RabbitMQ | Kafka |
|---------|---------|-------|
| **定位** | 消息中间件（注重可靠性） | 分布式流处理平台（注重吞吐量） |
| **协议** | AMQP（高级消息队列协议） | 自定义 TCP 协议 |
| **消息模型** | Exchange + Queue + Binding | Topic + Partition |
| **吞吐量** | 万级/秒 | **百万级/秒** ⭐ |
| **消息顺序** | 单队列有序 | Partition 内有序（全局需单分区） |
| **消息确认** | 手动 ACK + 重投 | Offset 提交 + 重平衡 |
| **消息回溯** | ❌ 不支持 | ✅ 支持按 Offset/时间戳回溯 |
| **延迟队列** | ✅ 死信队列 + TTL | ❌ 不支持（需插件） |
| **适用场景** | 订单消息、延迟任务、事务消息 | 日志收集、埋点数据、流计算 |

---

## 34. Elasticsearch 倒排索引原理？

### 正排 vs 倒排
```
正排索引（MySQL 方式）：文档ID → 文档内容
倒排索引（ES 方式）：    词条 → 包含该词条的文档ID列表
```

### 倒排索引结构
```
词条（Term） → 倒排列表（Posting List）
  "java"   → [doc1, doc3, doc7]  → 文档频率（DF）
  "elastic" → [doc2, doc5]
  "search" → [doc2, doc3, doc5, doc8]
```

**ES 倒排索引 = Term Dictionary（词项字典）+ Posting List（倒排列表）**
- Term Dictionary 用 **FST（Finite State Transducer）** 存储，内存友好、查询快
- Posting List 用 **FOR（Frame of Reference）** 压缩差值编码

---

# 第七部分：系统设计与架构

---

## 35. 设计模式常见面试题？

### 单例模式（饿汉 vs 懒汉 vs 枚举 vs 静态内部类）⭐
```java
// ✅ 推荐：静态内部类（线程安全 + 懒加载）
public class Singleton {
    private Singleton() {}
    private static class Holder {
        private static final Singleton INSTANCE = new Singleton();
    }
    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}

// ✅ 最推荐的实现：枚举
public enum Singleton {
    INSTANCE;
    public void doSomething() { ... }
}
```

### 代理模式（Spring AOP 的基石）
| 类型 | JDK 动态代理 | CGLIB 动态代理 |
|------|-------------|---------------|
| 原理 | 实现接口 → 生成 Proxy 对象 | **继承**目标类 → 生成子类 |
| 要求 | 目标类必须有接口 | 目标类不能是 final |
| 性能 | JDK 8+ 性能已接近 CGLIB | 初始化慢，方法调用快 |
| Spring 选择 | 目标实现接口 → JDK | 未实现接口 → CGLIB |

---

## 36. CAP 理论和 BASE 理论？

### CAP ⭐
| 属性 | 含义 |
|------|------|
| **C**（Consistency）一致性 | 所有节点同一时间看到的数据一致 |
| **A**（Availability）可用性 | 任何请求都能获得非错误的响应 |
| **P**（Partition Tolerance）分区容错性 | 系统允许网络分区（节点间通信中断） |

> **CAP 只能三选二**（实际只能 CP 或 AP，P 是分布式系统的必选项）

### BASE
| 要素 | 含义 |
|------|------|
| **BA**（Basically Available）基本可用 | 允许降级，比如响应变慢、部分功能关闭 |
| **S**（Soft State）软状态 | 允许中间状态，数据副本的同步有延迟 |
| **E**（Eventually Consistent）最终一致性 | 经过一段时间后，所有副本数据最终一致 |

> BASE 是对 CAP 中 AP 方案的延伸，**放弃强一致性，追求最终一致性**

### Raft 协议（理解即可）
```
① Leader 选举：节点获得多数派投票成为 Leader
② 日志复制：Leader 将日志复制到 Follower，多数派写入后提交
③ 安全性保证：Leader 拥有所有已提交日志，日志单向流动
```

---

## 37. 经典面试场景题？

### 设计秒杀系统 ⭐
```
核心目标：高并发下单 + 库存防超卖 + 用户体验
分层架构：
  ┌────────┐
  │ CDN + Nginx │ ← 静态页面、限流
  ├────────┤
  │ Gateway + Sentinel │ ← 流量过滤、限流熔断
  ├────────┤
  │ Redis │ ← 预扣库存（原子操作 DECR）
  ├────────┤
  │ MQ │ ← 削峰填谷，异步下单
  ├────────┤
  │ DB │ ← 最终库存扣减
  └────────┘
```
**关键设计**：
- Redis 预扣库存：`lua` 脚本保证原子性
- MQ 异步下单：请求先入队列，Worker 消费后返回结果
- 库存放在 Redis，用 Lua 脚本保证原子扣减
- 前端限流：按钮置灰 + 随机限流

### 分布式 ID 方案
| 方案 | 优点 | 缺点 |
|------|------|------|
| UUID | 本地生成，无网络开销 | 无序、太长、影响索引性能 |
| **雪花算法** ⭐ | 有序、高性能、自增 | 依赖机器时钟（时钟回拨问题） |
| Redis INCR | 简单 | 网络开销、单点 |
| Leaf（美团） | 号段模式预取，性能高 | 需要依赖 DB/zk |

### 雪花算法（Snowflake）
```
1bit(符号位) | 41bit(时间戳) | 10bit(机器ID) | 12bit(序列号)
→ 总共 64 位 long 类型
→ 同一毫秒最多生成 4096 个 ID
```

---

# 第八部分：数据结构与算法

---

## 38. 高频算法题推荐清单

### 必须能手写的排序
| 算法 | 时间复杂度 | 空间复杂度 | 稳定性 |
|------|:---------:|:---------:|:-----:|
| 快速排序 | O(n log n) | O(log n) | ❌ |
| 归并排序 | O(n log n) | O(n) | ✅ |
| 堆排序 | O(n log n) | O(1) | ❌ |

### LeetCode 分类重点
| 类型 | 经典题目 |
|------|---------|
| **链表** | 反转链表、环形链表、合并有序链表、删除倒数第 N 个节点 |
| **二叉树** | 前/中/后序遍历（递归+迭代）、层序遍历、最近公共祖先 |
| **动态规划** | 爬楼梯、最大子数组和、最长回文子串、背包问题 |
| **哈希表** | 两数之和、三数之和、最长无重复子串 |
| **栈/队列** | 最小栈、有效括号、单调栈 |
| **双指针** | 盛最多水的容器、三数之和、删除有序数组重复项 |
| **二分查找** | 旋转数组、搜索插入位置 |

---

# 第九部分：简历项目准备

---

## 39. 项目面试灵魂三问 ⭐

### 1. "项目用了什么技术栈？为什么选它？"
> 不要只列名词，要讲**选型考量**：
> - 为什么用 Nacos 而不是 Eureka？（Nacos 支持配置中心 + 注册中心合二为一，CAP 模式可切换）
> - 为什么用 Redis 缓存？（业务读多写少，缓存 QPS 从 500 提升到 5000+）
> - 为什么用 RabbitMQ 而不是 Kafka？（业务需要延迟队列、死信队列，对吞吐量要求不高）

### 2. "你负责什么？最大难点是什么？" ⭐
> 准备 **1-2 个技术亮点**，用 **STAR 法则**：
> - **Situation**：百万 QPS 秒杀场景，库存只有 100 件
> - **Task**：保证不超卖 + 系统不崩
> - **Action**：Redis Lua 预扣库存 + MQ 削峰 + Sentinel 限流
> - **Result**：系统平稳扛过 10 万并发，0 超卖

### 3. "如果重新做，会怎么改进？"
> 展示你的**技术视野和反思能力**：
> - "我会引入分库分表，当前单库性能瓶颈明显"
> - "缓存一致性现在用的是延迟双删，可以改用 Canal 监听 binlog 同步"
> - "加入全链路压测，提前发现系统瓶颈"

---

## 40. 项目亮点提炼方向建议

| 方向 | 具体措施 | 数据佐证 |
|------|---------|---------|
| **性能优化** | 引入缓存、SQL 索引优化、异步化改造 | QPS 从 300 → 3000，接口耗时从 2s → 50ms |
| **稳定性** | 限流熔断、降级兜底、灰度发布 | 系统可用性 99.9% → 99.99% |
| **架构升级** | 单体 → 微服务，引入消息队列解耦 | 部署频率从周级 → 天级 |
| **工具提效** | 代码生成器、CI/CD 流水线、自动化测试 | 开发效率提升 40% |
| **质量意识** | 单元测试覆盖率达 80%、Code Review 制度 | 线上 Bug 减少 60% |

---

> [!tip] **最后的话**
> - 面试是 **"引导面试官到你准备好的领域"**，不要被动挨打
> - 每个回答最后加一句 **"总之，核心在于..."** 展示你的总结能力
> - 说"不知道"不可怕，可怕的是答非所问、强行解释
> - 祝面试顺利！☕
