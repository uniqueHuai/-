# Java基础与进阶篇

## 一、Java 概述

### JVM / JDK / JRE 关系

```
JDK（Java Development Kit）
  └── JRE（Java Runtime Environment）
        └── JVM（Java Virtual Machine）
        └── 核心类库
  └── 开发工具（javac、jar、javadoc 等）
```

| 组件 | 说明 |
|:----:|------|
| **JVM** | Java 虚拟机，运行字节码，实现跨平台 |
| **JRE** | 运行时环境，JVM + 核心类库 |
| **JDK** | 开发工具包，JRE + 开发工具 |

### 编译执行流程

```
.java 源文件
   │ javac 编译
   ▼
.class 字节码文件（跨平台的关键）
   │ JVM 加载执行
   ▼
机器码（操作系统相关）
```

> [!NOTE]
> `.class` 字节码是 Java 跨平台的关键，JVM 屏蔽了底层操作系统差异，一份字节码可在任何安装了 JVM 的平台上运行。

### Java 版本简史

| 版本 | 亮点 | 状态 |
|:----:|------|:----:|
| **Java 8**（2014） | Lambda、Stream、Optional、新时间 API | ⭐ **LTS，仍广泛使用** |
| Java 11（2018） | HTTP Client、模块化、ZGC | LTS |
| **Java 17**（2021） | 密封类、Pattern Matching、**LTS** | ⭐ **最新 LTS** |
| Java 21（2023） | 虚拟线程、Record Pattern | LTS |

> [!TIP]
> 生产环境推荐使用 **Java 17 LTS**，Java 21 的虚拟线程（Virtual Threads）值得关注，可大幅降低高并发场景的开发复杂度。

---

## 二、基本数据类型

### 8 种基本类型

| 类型 | 大小 | 默认值 | 取值范围 | 包装类 |
|:----:|:----:|:------:|:---------|:------:|
| `byte` | 1 字节 | 0 | -128 ~ 127 | `Byte` |
| `short` | 2 字节 | 0 | -2^15 ~ 2^15-1 | `Short` |
| `int` | 4 字节 | 0 | -2^31 ~ 2^31-1 | `Integer` |
| `long` | 8 字节 | 0L | -2^63 ~ 2^63-1 | `Long` |
| `float` | 4 字节 | 0.0f | ±3.4E-38 ~ ±3.4E+38 | `Float` |
| `double` | 8 字节 | 0.0d | ±4.9E-324 ~ ±1.7E+308 | `Double` |
| `char` | 2 字节 | '\0' | 0 ~ 65535 | `Character` |
| `boolean` | 未明确定义 | false | true / false | `Boolean` |

### 自动装箱与拆箱

```java
Integer a = 100;          // 自动装箱：int → Integer（编译器调用了 Integer.valueOf(100)）
int b = a;                // 自动拆箱：Integer → int（编译器调用了 a.intValue()）
```

> [!WARNING]
> WARNING
> - `Integer` 默认缓存了 **-128 ~ 127** 之间的值
> - `Long`、`Short`、`Byte`、`Character` 也有类似缓存
> - 缓存范围内的值用 `==` 比较相等，范围外会创建新对象
> ```java
> Integer a = 100, b = 100;     // a == b → true（缓存）
> Integer c = 200, d = 200;     // c == d → false（新对象）
> ```

---

## 三、面向对象

### 三大特性

| 特性 | 说明 | 实现手段 |
|:----:|------|:--------:|
| **封装** | 隐藏内部实现，暴露有限接口 | `private` + getter/setter |
| **继承** | 子类复用父类成员，拓展新功能 | `extends` 关键字 |
| **多态** | 同一方法在不同对象上有不同表现 | 重写 + 父类引用指向子类对象 |

### abstract class vs interface

| 对比 | `abstract class` | `interface` |
|:----:|:----------------:|:-----------:|
| **继承方式** | 单继承（`extends`） | 多实现（`implements`） |
| **构造方法** | ✅ 可以有 | ❌ 不能有 |
| **成员变量** | 任意 | `public static final`（常量） |
| **方法** | 抽象方法 + 普通方法 | 抽象方法 + `default`/`static` 方法（Java 8+） |
| **用途** | **is-a** 关系，模板方法 | **can-do** 关系，行为约定 |

### 重载（Overload）vs 重写（Override）

| 对比 | 重载 | 重写 |
|:----:|:----:|:----:|
| **发生位置** | **同一个类**中 | **子类与父类**之间 |
| **方法名** | 相同 | 相同 |
| **参数列表** | **必须不同** | **必须相同** |
| **返回值** | 可以不同 | **必须相同**（或协变返回类型） |
| **权限** | 无限制 | **不能低于**父类方法的权限 |
| **编译/运行** | **编译时**多态 | **运行时**多态 |

> [!TIP]
> 重载是**编译时多态**（静态绑定），重写是**运行时多态**（动态绑定）。开发中优先使用重写实现多态，接口设计中善用重载提高 API 易用性。

---

## 四、String 体系

### 1. String 不可变性

> [!NOTE]
> String 是被 `final` 修饰的类，其字符数组也是 `final` 的，任何"修改"都会创建新对象，原对象不受影响。

```java
String s = "hello";
s = s + " world";  // 并非修改原对象，而是创建了新对象
```

**为什么设计成不可变？**
- ✅ **线程安全**：不可变对象天然线程安全
- ✅ **字符串常量池复用**：相同字面量共享同一对象
- ✅ **Hash 缓存**：String 的 `hashCode()` 只计算一次并缓存
- ✅ **安全性**：Class 加载、网络连接等场景需要不可变参数

### 2. String vs StringBuilder vs StringBuffer

| 对比 | String | StringBuilder | StringBuffer |
|:----:|:------:|:-------------:|:------------:|
| **可变性** | ❌ 不可变 | ✅ 可变 | ✅ 可变 |
| **线程安全** | ✅ 天然安全 | ❌ 不安全 | ✅ `synchronized` |
| **性能** | 拼接时性能差 | **最快** | 比 StringBuilder 慢 |
| **推荐场景** | 字符串常量 | **单线程**字符串拼接 | 多线程字符串操作 |

```java
// 字符串拼接性能对比
String s = "";                     // ❌ 每次拼接都创建新对象
StringBuilder sb = new StringBuilder();  // ✅ 单线程推荐
sb.append("a").append("b");
StringBuffer sbf = new StringBuffer();   // ✅ 多线程推荐
```

### 3. 字符串常量池

```
String s1 = "hello";
String s2 = "hello";
String s3 = new String("hello");

s1 == s2      → true （常量池中同一对象）
s1 == s3      → false（s3 是堆上新对象）
s1.equals(s3) → true （equals 比较内容）
```

> [!TIP]
> TIP
> ```java
> String s3 = new String("hello").intern();
> s1 == s3  → true
> ```

---

## 五、集合框架

### 1. Collection 体系概览

```
Iterable
  └── Collection
        ├── List（有序、可重复）
        │     ├── ArrayList     ← 数组实现，查询快
        │     ├── LinkedList    ← 双向链表，增删快
        │     └── Vector        ← 线程安全（古老）
        │           └── Stack
        ├── Set（不可重复）
        │     ├── HashSet       ← 基于 HashMap
        │     │     └── LinkedHashSet  ← 维护插入顺序
        │     └── TreeSet       ← 红黑树，可排序
        └── Queue（队列）
              ├── LinkedList    ← 双端队列
              ├── PriorityQueue ← 优先级队列
              └── BlockingQueue ← 阻塞队列（并发包）
```

```
Map（键值对）
  ├── HashMap          ← 数组+链表+红黑树，⭐ 最常用
  │     └── LinkedHashMap  ← 维护插入/访问顺序
  ├── TreeMap          ← 红黑树，key 可排序
  ├── Hashtable        ← 线程安全（古老）
  └── ConcurrentHashMap ← 线程安全（JUC）
```

### 2. ArrayList vs LinkedList

| 对比 | ArrayList | LinkedList |
|:----:|:---------:|:----------:|
| **底层结构** | 动态数组 | 双向链表 |
| **随机访问** | ✅ O(1) | ❌ O(n) |
| **头部插入** | ❌ O(n) | ✅ O(1) |
| **尾部插入** | ✅ O(1)（扩容时 O(n)） | ✅ O(1) |
| **内存占用** | 小 | 大（存前后指针） |
| **适用场景** | **查询多、尾部插入** | **频繁头尾增删** |

### 3. HashMap 原理 ⭐（高频重点）

#### 数据结构

| JDK 版本  |        结构         | 说明                          |
| :-----: | :---------------: | --------------------------- |
| **1.7** |    **数组 + 链表**    | 头插法，扩容时可能死锁                 |
| **1.8** | **数组 + 链表 + 红黑树** | **尾插法**，链表 ≥8 && 数组 ≥64 时树化 |

```
JDK 1.8 HashMap 结构：
┌────┬────┬────┬────┬────┬────┬────┐
│  0 │  1 │  2 │ …  │ …  │  15│    │  ← 数组（bucket）
└────┴─│──┴────┴────┴────┴────┴────┘
       ▼
    ┌─────┐    ┌─────┐
    │Node │ →  │Node │ →  null    ← 链表（<8）或红黑树（≥8）
    └─────┘    └─────┘
```

#### 核心参数

|          参数           | 说明                           |   默认值    |
| :-------------------: | ---------------------------- | :------: |
|      `capacity`       | 数组容量                         |  **16**  |
|     `loadFactor`      | 负载因子                         | **0.75** |
|      `threshold`      | 扩容阈值 = capacity × loadFactor |    12    |
|  `TREEIFY_THRESHOLD`  | 链表树化阈值                       |  **8**   |
| `UNTREEIFY_THRESHOLD` | 红黑树退化链表阈值                    |  **6**   |

#### 扩容机制

```
put(key, value)
  → 计算 hash → (n - 1) & hash 确定槽位
  → 发生冲突时链入链表/红黑树
  → 当 size > threshold（capacity × 0.75）
  → **扩容为原来的 2 倍**，rehash 重新分布
```

> [!NOTE]
> NOTE
> | 对比 | JDK 1.7 | JDK 1.8 |
> |:----:|:--------:|:--------:|
> | **插入方式** | **头插法**（扩容可能死锁） | **尾插法** |
> | **数据结构** | 数组 + 链表 | 数组 + 链表 + **红黑树** |
> | **Hash 计算** | 4 次位运算 | 1 次位运算 |
> | **扩容 rehash** | 重新计算 hash | 通过 `(hash & oldCap) == 0` 优化 |

### 4. ConcurrentHashMap 原理

| 版本 | 线程安全实现 |
|:----:|-------------|
| **1.7** | **分段锁（Segment）**，每段一个锁，默认 16 段 |
| **1.8** | **CAS + `synchronized`**（只锁链表/红黑树头节点），粒度更细 |

> [!TIP]
> TIP
> - `HashMap`：线程不安全，性能最高
> - `Hashtable`：线程安全，但**全表加锁**，性能差
> - `ConcurrentHashMap`：线程安全，**分段/细粒度锁**，推荐

### 5. HashSet vs TreeSet vs LinkedHashSet

| 对比 | HashSet | TreeSet | LinkedHashSet |
|:----:|:-------:|:-------:|:-------------:|
| **底层** | HashMap | TreeMap（红黑树） | LinkedHashMap |
| **顺序** | 无序 | **自然排序 / Comparator** | **插入顺序** |
| **性能** | O(1) | O(log n) | O(1) |
| **是否允许 null** | ✅ 允许 | ❌ 不允许 | ✅ 允许 |

---

## 六、泛型

### 类型擦除

> [!NOTE]
> 类型擦除意味着泛型信息只在**编译期**有效，运行时所有泛型类型都会被替换为原始类型（`Object` 或上限类型），因此无法在运行时获取泛型参数的具体类型。

```java
List<String> list1 = new ArrayList<>();
List<Integer> list2 = new ArrayList<>();
list1.getClass() == list2.getClass()  // → true（运行时都是 ArrayList）
```

### 通配符与 PECS 原则

```java
// ? extends T：生产者（Producer）— 只读，不可写
List<? extends Number> list = new ArrayList<Integer>();
Number n = list.get(0);   // ✅ 读
list.add(1);              // ❌ 编译错误

// ? super T：消费者（Consumer）— 可写，读只能读到 Object
List<? super Integer> list = new ArrayList<Number>();
list.add(1);              // ✅ 写
Object obj = list.get(0); // ✅ 只能读到 Object
```

> [!TIP]
> TIP
> - **读取**数据用 `? extends T`（生产者）
> - **写入**数据用 `? super T`（消费者）
> - `?` 无界通配符：既不能读也不能写（只能读 Object）

---

## 七、异常体系

### 异常结构

```
Throwable（可抛出的）
  ├── Exception（异常，需要处理）
  │     ├── RuntimeException（运行时异常，非受检）
  │     │     ├── NullPointerException
  │     │     ├── IllegalArgumentException
  │     │     ├── IndexOutOfBoundsException
  │     │     └── ConcurrentModificationException
  │     └── 非 RuntimeException（受检异常，必须处理）
  │           ├── IOException
  │           ├── SQLException
  │           └── ClassNotFoundException
  └── Error（错误，无法处理）
        ├── OutOfMemoryError
        ├── StackOverflowError
        └── NoClassDefFoundError
```

| 异常类型 | 编译检查 | 是否必须处理 | 常见例子 |
|:--------:|:--------:|:------------:|----------|
| **受检异常**（Checked） | ✅ 是 | 必须 try-catch 或 throws | `IOException`、`SQLException` |
| **非受检异常**（Unchecked） | ❌ 否 | 可以选择性处理 | `NullPointerException`、`ArrayIndexOutOfBoundsException` |

### try-with-resources（Java 7+）

```java
// 自动关闭实现了 AutoCloseable 的资源，无需 finally
try (FileInputStream fis = new FileInputStream("file.txt");
     BufferedReader br = new BufferedReader(new InputStreamReader(fis))) {
    String line = br.readLine();
} catch (IOException e) {
    log.error("读取文件失败", e);
}
// 资源自动关闭，无需 finally
```

### 异常处理最佳实践

- ✅ 捕获异常后**记录日志**（`log.error`）而不是 `e.printStackTrace()`
- ✅ 不要捕获 `Exception` 或 `Throwable`（太宽泛）
- ✅ 不要用异常控制业务流程
- ✅ 资源操作使用 try-with-resources
- ✅ 自定义异常继承 `RuntimeException`（非受检，更灵活）

---

## 八、反射

### 获取 Class 对象的三种方式

```java
// 方式一：类名.class（编译时确定）
Class<User> clazz1 = User.class;

// 方式二：对象.getClass()（运行时）
Class<?> clazz2 = user.getClass();

// 方式三：Class.forName()（最常用，可动态加载）
Class<?> clazz3 = Class.forName("com.example.User");
```

### 常见反射操作

```java
// 获取所有公共字段
Field[] fields = clazz.getFields();

// 获取所有字段（含私有）
Field[] declaredFields = clazz.getDeclaredFields();

// 调用私有方法
Method method = clazz.getDeclaredMethod("privateMethod", String.class);
method.setAccessible(true);           // 跳过权限检查
method.invoke(newInstance, "hello");  // 执行

// 创建实例
Object obj = clazz.getDeclaredConstructor().newInstance();
```

### 动态代理

| 代理方式 | 要求 | 原理 |
|:--------:|:----:|------|
| **JDK 动态代理** | 目标类**必须实现接口** | 通过 `Proxy.newProxyInstance()` 生成接口的代理对象 |
| **CGLIB 动态代理** | 无需接口 | 通过**生成子类**（继承）实现代理，不能代理 `final` 类 |

```java
// JDK 动态代理示例
interface UserService {
    void addUser(String name);
}

UserService proxy = (UserService) Proxy.newProxyInstance(
    UserService.class.getClassLoader(),
    new Class[]{UserService.class},
    (proxyObj, method, args) -> {
        System.out.println("前置处理");
        Object result = method.invoke(target, args);
        System.out.println("后置处理");
        return result;
    }
);
```

> [!TIP]
> Spring 的事务管理和 AOP 底层大量使用了动态代理。若目标类没有实现接口，Spring 会切换为 CGLIB 代理（Spring Boot 2.x+ 默认已启用此模式）。

---

## 九、注解（Annotation）

### 元注解

| 注解 | 说明 |
|:----:|------|
| `@Retention` | 注解的生命周期：`SOURCE` / `CLASS`（默认） / `RUNTIME` |
| `@Target` | 注解可修饰的目标：`TYPE` / `METHOD` / `FIELD` / `PARAMETER` 等 |
| `@Documented` | 是否包含在 Javadoc 中 |
| `@Inherited` | 注解是否可以被子类继承 |
| `@Repeatable` | 注解是否可以重复标注（Java 8+） |

```java
// 自定义运行时注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Log {
    String value() default "";
    boolean enable() default true;
}
```

### 运行时 vs 编译时注解

| 类型 | `@Retention` | 获取方式 | 用途 |
|:----:|:------------:|:--------:|------|
| **编译时注解** | `SOURCE` / `CLASS` | **APT 处理器**（编译期处理） | Lombok（`@Getter`、`@Setter`）、代码生成 |
| **运行时注解** | `RUNTIME` | **反射**获取 | Spring（`@Service`、`@Autowired`） |

---

## 十、序列化

### Serializable 接口

```java
class User implements Serializable {
    private static final long serialVersionUID = 1L;  // ⭐ 显式声明版本号

    private String name;
    private transient String password;   // ⭐ transient 字段不参与序列化
    private int age;
}
```

> [!WARNING]
> WARNING
> - 用于验证序列化和反序列化的版本一致性
> - **显式声明**：修改类字段后依然能兼容反序列化
> - **不声明**：JVM 自动生成，一旦类结构改变就会抛 `InvalidClassException`

### transient 关键字

- 被 `transient` 修饰的字段**不参与序列化**
- 适合存储敏感信息（密码）或可从其他字段计算出的数据

### 常见的序列化方式

| 方式 | 特点 |
|:----:|------|
| **Java 原生序列化** | 实现 `Serializable`，跨语言差，性能一般 |
| **JSON**（Jackson / Gson） | ⭐ **最常用**，跨语言，可读性好 |
| **Protobuf** | 二进制，性能高，体积小，跨语言 |

---

## 十一、IO 与 NIO

### 字节流 vs 字符流

```
字节流：
  InputStream（读） → FileInputStream / BufferedInputStream
  OutputStream（写）→ FileOutputStream / BufferedOutputStream

字符流：
  Reader（读） → FileReader / BufferedReader
  Writer（写） → Writer → FileWriter / BufferedWriter
```

> [!TIP]
> TIP
> - **字节流**：操作所有文件（图片、视频、文本），按字节读写
> - **字符流**：操作文本文件，按字符读写，需要指定编码（UTF-8）

### BIO / NIO / AIO 对比

| 对比 | BIO（阻塞 IO） | NIO（非阻塞 IO） | AIO（异步 IO） |
|:----:|:--------------:|:----------------:|:--------------:|
| **模型** | 同步阻塞 | 同步非阻塞 | 异步非阻塞 |
| **线程模型** | **一个连接一个线程** | **一个线程轮询多个连接** | 回调/事件驱动 |
| **适用场景** | 连接数少、固定 | 连接数多、短连接 | 连接数多、长连接 |
| **例子** | 传统 Socket | Netty、Tomcat NIO | Windows IOCP |

### NIO 三大核心组件

| 组件 | 说明 |
|:----:|------|
| **Channel（通道）** | 双向，可读可写，比 Stream 更灵活 |
| **Buffer（缓冲区）** | 底层是数组，`flip()` 切换读写模式 |
| **Selector（选择器）** | 单线程管理多个 Channel 的就绪状态（**IO 多路复用**） |

---

## 十二、深拷贝 vs 浅拷贝

### 概念对比

```
浅拷贝：
  原对象 ──→ 副本对象（引用类型字段指向同一对象）
               ↓
           实 例 变 量  ← 共享

深拷贝：
  原对象 ──→ 副本对象（引用类型字段也被复制）
               ↓
           新 实 例  ← 独立
```

### 实现方式

```java
// 浅拷贝（实现 Cloneable，默认 clone 是浅拷贝）
class User implements Cloneable {
    private String name;
    private Address address;  // 引用类型

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();  // address 字段仍指向同一对象
    }
}

// 深拷贝方式一：重写 clone
@Override
protected Object clone() throws CloneNotSupportedException {
    User cloned = (User) super.clone();
    cloned.address = (Address) address.clone();  // 手动复制引用类型
    return cloned;
}

// 深拷贝方式二：序列化（推荐）
public User deepClone() {
    ByteArrayOutputStream bos = new ByteArrayOutputStream();
    new ObjectOutputStream(bos).writeObject(this);
    ByteArrayInputStream bis = new ByteArrayInputStream(bos.toByteArray());
    return (User) new ObjectInputStream(bis).readObject();
}
```

> [!TIP]
> 推荐使用**序列化方式**实现深拷贝，可以完整复制整个对象图，且无需手动处理每个引用字段。商业项目中应优先考虑使用第三方库（如 Apache Commons Lang 的 `SerializationUtils` 或 JSON 序列化）。

---

## 十三、`equals()` vs `hashCode()`

### 对比

| 方法 | 用途 | 默认实现 |
|:----:|:----:|:--------:|
| `equals()` | 判断两个对象**逻辑相等** | `==`（比较引用地址） |
| `hashCode()` | 返回对象的**哈希值** | 根据内存地址生成 |

### 约定规则

> [!WARNING]
> WARNING
> 1. 如果 `equals()` 返回 `true`，`hashCode()` **必须相等**
> 2. 如果 `hashCode()` 相等，`equals()` **不一定**为 `true`（哈希碰撞）
> 3. 因此**重写 `equals()` 必须同时重写 `hashCode()`**

### 为什么要同时重写？

```java
// 错误示范：只重写 equals，不重写 hashCode
Map<User, String> map = new HashMap<>();
map.put(new User("Alice"), "value");
map.get(new User("Alice"));  // → null！

// 原因：put 时用 hashCode() 找槽位，get 时 hashCode() 不同 → 找不到
// 即使 equals 为 true，但 hashCode 不同导致定位到不同 bucket
```

### 重写规范

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    User user = (User) o;
    return age == user.age && Objects.equals(name, user.name);
}

@Override
public int hashCode() {
    return Objects.hash(name, age);  // ⭐ 使用与 equals 相同的字段
}
```

---

## 十四、内部类

### 四种内部类对比

| 类型 | 定义位置 | 能否有 static 成员 | 能否访问外部类成员 |
|:----:|:--------:|:------------------:|:-----------------:|
| **静态内部类** | 类内部，`static` 修饰 | ✅ 可以 | 只能访问外部类 **static** 成员 |
| **成员内部类** | 类内部，无 static | ❌ 不可以 | 可以访问外部类**所有**成员 |
| **局部内部类** | 方法内部 | ❌ 不可以 | 可以访问外部类成员 + `final`/`effectively final` 局部变量 |
| **匿名内部类** | 方法内部，无类名 | ❌ 不可以 | 同局部内部类 |

```java
class Outer {
    private String name = "outer";

    // 静态内部类
    static class StaticInner {}

    // 成员内部类
    class Inner {
        void print() { System.out.println(name); }  // 访问外部类成员
    }

    void method() {
        // 局部内部类
        class LocalInner {}

        // 匿名内部类（Lambda 可简化）
        Runnable r = new Runnable() {
            @Override
            public void run() {}
        };

        // Lambda 简化
        Runnable r2 = () -> {};
    }
}
```

---

## 十五、Lambda 与函数式接口

### @FunctionalInterface

**函数式接口**：有且仅有一个抽象方法的接口，可以用 Lambda 简化。

```java
@FunctionalInterface
public interface Runnable {
    void run();
}
```

### 四大函数式接口

| 接口 | 名称 | 方法 | 参数 | 返回值 |
|:----:|:----:|:----:|:----:|:------:|
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
// 组合
Predicate<Integer> complex = pred.and(n -> n < 100).negate();
```

### 方法引用 `::`

```java
// 静态方法引用
Consumer<String> c = System.out::println;        // (x) → System.out.println(x)

// 实例方法引用
Function<String, Integer> f = String::length;    // (s) → s.length()

// 构造方法引用
Supplier<List<String>> sup = ArrayList::new;     // () → new ArrayList<>()
```

---

## 十六、Stream API

### 创建流

```java
// 从集合创建
list.stream();
list.parallelStream();  // 并行流

// 从数组创建
Arrays.stream(array);

// 工厂方法
Stream.of("a", "b", "c");
Stream.iterate(0, n -> n + 2).limit(10);       // 0, 2, 4, 6...
Stream.generate(Math::random).limit(5);         // 5 个随机数
```

### 中间操作（返回 Stream，延迟执行）

| 操作 | 说明 | 示例 |
|:----:|------|:----:|
| `filter` | **过滤** | `.filter(n -> n > 0)` |
| `map` | **转换** | `.map(String::length)` |
| `flatMap` | **扁平化** | `.flatMap(Collection::stream)` |
| `sorted` | **排序** | `.sorted(Comparator.naturalOrder())` |
| `distinct` | **去重** | `.distinct()` |
| `limit` | **截取** | `.limit(10)` |
| `skip` | **跳过** | `.skip(5)` |

### 终止操作（触发执行）

| 操作 | 说明 | 示例 |
|:----:|------|:----:|
| `collect` | **收集到集合** | `.collect(Collectors.toList())` |
| `forEach` | **遍历** | `.forEach(System.out::println)` |
| `reduce` | **归约** | `.reduce(0, Integer::sum)` |
| `count` | **计数** | `.count()` |
| `anyMatch/allMatch/noneMatch` | **匹配判断** | `.anyMatch(x -> x > 0)` |
| `findFirst` / `findAny` | **查找** | `.findFirst()` |

```java
// 综合示例：获取所有年龄大于18的用户名，按名字排序
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .sorted()
    .collect(Collectors.toList());
```

> [!TIP]
> Stream 操作是**惰性求值**的 — 中间操作不会立即执行，只有遇到终止操作（如 `collect`、`forEach`）才会触发整个流水线。合理利用并行流（`parallelStream()`）可发挥多核优势，但需注意线程安全。

---

## 十七、Optional

**用途**：优雅地处理 null，防止 `NullPointerException`。

### 创建 Optional

```java
// 值不能为 null，否则抛 NPE
Optional<String> opt = Optional.of("hello");

// 值可以为 null
Optional<String> opt2 = Optional.ofNullable(nullableValue);

// 空 Optional
Optional<String> empty = Optional.empty();
```

### 常用方法

```java
// 判读是否存在
if (opt.isPresent()) { ... }

// 存在则执行（Java 8）
opt.ifPresent(val -> System.out.println(val));

// 存在则执行，否则执行其他（Java 9）
opt.ifPresentOrElse(val -> {}, () -> {});

// 转换
Optional<Integer> len = opt.map(String::length);        // 返回 Optional
Optional<String> upper = opt.flatMap(v -> Optional.of(v.toUpperCase()));

// 兜底值
String result = opt.orElse("default");          // 始终计算默认值
String result2 = opt.orElseGet(() -> fetch());   // 延迟计算（推荐）
String result3 = opt.orElseThrow(() -> new IllegalArgumentException("值不存在"));
// Java 9+
opt.or(() -> Optional.of("fallback"));           // Optional 兜底
```

> [!TIP]
> TIP
> - `orElse(T)`：**无论 Optional 是否为空**，都会计算默认值
> - `orElseGet(Supplier)`：**只有为空时**才调用 Supplier，更高效

---

## 十八、新时间日期 API（Java 8+）

### 核心类

| 类 | 说明 | 示例 |
|:---:|------|:----:|
| `LocalDate` | **日期**（年月日） | `2025-01-15` |
| `LocalTime` | **时间**（时分秒纳秒） | `14:30:00` |
| `LocalDateTime` | **日期+时间** | `2025-01-15T14:30:00` |
| `Instant` | **时间戳**（从 1970-01-01 开始） | 适合机器处理 |
| `Duration` | **时间间隔**（秒/纳秒） | `between(t1, t2)` |
| `Period` | **日期间隔**（年月日） | `between(date1, date2)` |

### 基本使用

```java
// 获取当前时间
LocalDate today = LocalDate.now();
LocalTime now = LocalTime.now();
LocalDateTime dateTime = LocalDateTime.now();

// 指定时间
LocalDate date = LocalDate.of(2025, Month.JANUARY, 15);

// 日期运算
LocalDate tomorrow = today.plusDays(1);
LocalDate lastMonth = today.minusMonths(1);
LocalDate nextWeek = today.with(TemporalAdjusters.next(DayOfWeek.MONDAY));

// 比较
boolean after = date1.isAfter(date2);
boolean before = date1.isBefore(date2);
```

### 格式化

```java
// 格式化
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = dateTime.format(formatter);      // "2025-01-15 14:30:00"

// 解析
LocalDateTime parsed = LocalDateTime.parse("2025-01-15 14:30:00", formatter);
```

### 与传统 Date/Calendar 对比

| 对比 | `Date` / `Calendar` | `java.time` 包 |
|:----:|:-------------------:|:--------------:|
| **可变性** | ❌ 可变（线程不安全） | ✅ **不可变**（线程安全） |
| **设计** | 设计混乱，方法命名不直观 | 清晰，职责分明 |
| **月份** | `Calendar.JANUARY = 0` | `Month.JANUARY`（正常 1-12） |
| **操作** | 需要 `Calendar` 辅助 | 直接 `.plusDays()` / `.minusMonths()` |
| **线程安全** | ❌ | ✅ |

> [!TIP]
> 新代码应**完全使用 `java.time` 包**替代 `Date` / `Calendar`。`LocalDate`、`LocalDateTime` 等类都是不可变的，天然线程安全，API 设计也更为直观。

---

## 十九、线程的基本概念

**线程**是程序执行的最小单元，是进程中的一个独立执行路径。

| 对比维度 | 进程 | 线程 |
|----------|:----:|:----:|
| 资源分配 | 操作系统**资源分配**的基本单位 | 所属进程内共享资源 |
| CPU 调度 | ❌ | ✅ **CPU 调度**的基本单位 |
| 资源开销 | 独立内存空间，开销大 | 共享进程资源，开销小 |

---

## 二十、创建线程的方式

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

> [!TIP]
> TIP
>
| 方式 | 优点 | 缺点 |
|------|------|------|
| 继承 Thread | 简单直接 | 不能继承其他类 |
| 实现 Runnable | 可继承其他类 | 无返回值 |
| 实现 Callable | 有返回值，可抛异常 | 略复杂 |
| **线程池** | **复用线程，控制并发，推荐** | — |

---

## 二十一、线程的生命周期

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

## 二十二、线程的基本控制方法

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

> [!WARNING]
> WARNING
> - `wait()` 是 Object 方法，**会释放锁**，需要被唤醒
> - `sleep()` 是 Thread 方法，**不会释放锁**，到期自动唤醒

---

## 二十三、线程同步与锁

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

> [!TIP]
> TIP
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

## 二十四、线程间通信

### 方式一：wait / notify（传统）

> [!WARNING]
> `wait()` / `notify()` 必须在 `synchronized` 块中调用，否则抛出 `IllegalMonitorStateException`。`notify()` 是随机唤醒一个线程，无法精确控制唤醒哪个线程，因此推荐使用 `Condition` 实现精确唤醒。

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

> [!CAUTION]
> CAUTION
> 线程可能在未被 `notify()`/`signal()` 的情况下被唤醒。**必须用 `while` 循环判断条件**，而不是 `if`：
> ```java
> while (条件不满足) { // ⚠️ 用 while 不是 if
>     condition.await();
> }
> ```

---

## 二十五、线程安全类

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

## 二十六、并发集合

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

## 二十七、阻塞队列

### 四组 API

| 方式 | 抛出异常 | 返回特殊值 | 阻塞等待 | 超时等待 |
|:----:|:--------:|:----------:|:--------:|:--------:|
| **添加** | `add()` | `offer()` | `put()` | `offer(time, unit)` |
| **移除** | `remove()` | `poll()` | `take()` | `poll(time, unit)` |
| **检测队首** | `element()` | `peek()` | — | — |

```java
ArrayBlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);
```

> [!NOTE]
> `SynchronousQueue` 容量为 1 的同步队列，一个 `put()` 必须等待一个 `take()`，**放一个拿一个**。

---

## 二十八、线程池

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

## 二十九、JUC 高级工具

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

> [!TIP]
> TIP
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

## 三十、JMM（Java 内存模型）

> [!NOTE]
> JMM（Java Memory Model）定义了多线程读写共享变量的**内存可见性规则**，核心是保证各线程工作内存与主存之间数据的一致性。理解 JMM 是深入掌握并发编程的基础。

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

### happens-before 规则

| 规则 | 说明 |
|:----:|------|
| **程序顺序规则** | 一个线程中的每个操作，happens-before 于该线程中的任意后续操作 |
| **volatile 规则** | 对一个 volatile 域的写，happens-before 于后续对这个域的读 |
| **锁规则** | 对一个锁的解锁，happens-before 于后续对这个锁的加锁 |
| **传递性** | A happens-before B，B happens-before C → A happens-before C |

---

## 三十一、CAS（Compare-And-Swap）

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

> [!WARNING]
> WARNING
> 线程 1 读取值为 A，被挂起 → 线程 2 将 A 改为 B 又改回 A → 线程 1 恢复执行，CAS 发现还是 A，操作成功——但值实际上已经被修改过。

**解决方案**：使用 `AtomicStampedReference`（带版本号的原子引用），每次修改版本号 +1。

---

> **📖 学习路线**：[[README]] | **下一站**：[[JVM篇]] → [[SpringBoot篇]] → [[登录认证篇]] 或 [[SpringCloud篇]]
