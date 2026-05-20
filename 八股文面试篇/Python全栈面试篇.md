# 🐍 Python 全栈开发 · 面试知识点

> 已有参考笔记：[[python学习篇/Python基础与进阶篇]] · [[python学习篇/FastAPI篇]] · [[python学习篇/爬虫基础与进阶篇]]
> 通用底盘（数据库/运维/前端）参考 [[八股文面试篇/README]] · [[八股文面试篇/Java全栈面试篇]]（数据库、设计模式等通用内容可交叉复习）

---

# 第一部分：Python 核心基础 ⭐

---

## 1. Python 语言特性？解释型 vs 编译型？

### Python 执行过程
```
源代码 (.py) → 编译 → 字节码 (.pyc) → 解释执行 → PVM (Python 虚拟机)
```

- **Python 是"先编译后解释"**：先将源代码编译为字节码（.pyc），再由 PVM 逐行解释执行
- **跨平台**：.pyc 字节码可在任何安装了 PVM 的平台上运行

### 解释型 vs 编译型
| 对比 | 解释型（Python） | 编译型（Java/C++） |
|------|----------------|------------------|
| 执行方式 | 逐行翻译执行 | 一次性编译成机器码 |
| 速度 | 较慢 | 较快 |
| 开发效率 | 高，无需编译步骤 | 相对低 |
| 跨平台 | 源码/字节码跨平台 | 需针对各平台编译 |

---

## 2. GIL 全局解释器锁是什么？⭐

**GIL（Global Interpreter Lock）**：CPython 解释器中的一个互斥锁，保证同一时刻**只有一个线程**在执行 Python 字节码。

### 为什么要有 GIL？
1. **内存管理安全**：Python 的引用计数在多线程环境下需要保护，GIL 避免了细粒度锁的复杂度和死锁风险
2. **历史原因**：早期 Python 的简单设计选择，简化了 C 扩展的编写

### GIL 对并发的影响 ⭐
```python
# CPU 密集型任务 — GIL 导致多线程反而更慢
def cpu_intensive():
    count = 0
    for i in range(10**8):
        count += 1  # 多线程下 GIL 切换带来额外开销

# IO 密集型任务 — 多线程有效
def io_intensive():
    time.sleep(1)  # IO 操作释放 GIL，其他线程可以执行
    requests.get("https://example.com")  # 网络 IO 同样释放 GIL
```

| 任务类型 | 多线程 | 多进程 | 协程 |
|---------|:-----:|:-----:|:----:|
| **CPU 密集型** | ❌ 受 GIL 限制 | ✅ 每个进程独立 GIL | ❌ 仍是单线程 |
| **IO 密集型** | ✅ GIL 在 IO 时释放 | ✅ 但进程间通信开销大 | ⭐ **最佳选择** |

> [!info] **GIL 释放时机**
> - IO 操作（网络、文件读写）自动释放 GIL
> - 每执行 **100 个字节码指令** 或达到 `sys.getcheckinterval()` 阈值时释放
> - C 扩展可以在耗时操作前手动释放 GIL

---

## 3. Python 可变与不可变类型？

| 类别 | 类型 | 说明 |
|------|------|------|
| **不可变** | `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` | 修改会**创建新对象** |
| **可变** | `list`, `dict`, `set`, 自定义类实例 | 修改**不改变内存地址** |

```python
# 不可变类型的"修改"实际上是创建新对象
a = [1, 2, 3]
b = a
b.append(4)       # ✅ 修改原对象
print(a is b)      # True — 同一对象

x = "hello"
y = x
y += " world"     # 创建新字符串对象
print(x is y)      # False — y 指向新对象
```

> [!tip] **面试常见陷阱**
> ```python
> def add_item(item, lst=[]):  # ❌ 默认参数是可变对象！
>     lst.append(item)
>     return lst
> print(add_item(1))  # [1]
> print(add_item(2))  # [1, 2] — 默认列表被复用！
> # ✅ 正确写法：lst=None，内部新建 []
> ```

---

## 4. dict 底层原理？

### Python 3.7+ 的 dict 实现
- **哈希表**实现，key 必须是可哈希对象（实现了 `__hash__()` 和 `__eq__()`）
- **有序**（Python 3.7+）：维护插入顺序，底层用**紧凑哈希表**（combined table）
- **扩容**：当填充率达到 **2/3** 时扩容（哈希冲突增多影响性能）

### 与 list 的查询对比
```python
# list 查询 O(n)
users = [{"id": 1, "name": "Alice"}, ...]
target = next(u for u in users if u["id"] == 100)  # 遍历

# dict 查询 O(1)
user_map = {1: {"name": "Alice"}, ...}
target = user_map[100]  # 直接哈希查找
```

---

## 5. 深浅拷贝的区别？

```python
import copy

original = [[1, 2], [3, 4]]

# ① 赋值（=）— 只是引用别名
ref = original
ref[0][0] = 99
print(original[0][0])  # 99 — 原对象被修改

# ② 浅拷贝（copy.copy）— 新对象，但子对象仍是引用
shallow = copy.copy(original)
shallow[0][0] = 88
print(original[0][0])  # 88 — 子对象共享！

# ③ 深拷贝（copy.deepcopy）— 完全独立的新对象
deep = copy.deepcopy(original)
deep[0][0] = 77
print(original[0][0])  # 88 — 不受影响
```

| 操作 | 顶层对象 | 子对象 | 使用场景 |
|------|:-------:|:-----:|---------|
| `=` 赋值 | ❌ | ❌ | 只想用别名 |
| `copy.copy()` | ✅ | ❌ | 只有一层结构 |
| `copy.deepcopy()` | ✅ | ✅ | 嵌套结构完全独立 |

---

## 6. 装饰器原理和应用？⭐

### 装饰器本质
**语法糖**：`@decorator` 等价于 `func = decorator(func)`

```python
# 最简单的装饰器
def timer(func):
    @functools.wraps(func)  # 保留原函数的元信息（name, doc等）
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

### 带参数装饰器
```python
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_attempts - 1:
                        raise
                    time.sleep(1)
            return wrapper
    return decorator

@retry(max_attempts=5)
def unstable_api():
    ...
```

### 类装饰器
```python
class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance

@Singleton
class Database:
    pass

# db1 和 db2 是同一个实例
```

> [!info] **装饰器典型应用场景**
> - **日志记录**：`@log` 自动记录方法入参和返回
> - **权限校验**：`@require_auth` 检查用户登录态
> - **缓存**：`@lru_cache` 缓存函数结果
> - **重试**：`@retry` 失败自动重试
> - **限流**：`@rate_limit` 控制调用频率

---

## 7. 生成器 vs 迭代器？`yield` 原理？

### 迭代器
实现了 `__iter__()` 和 `__next__()` 的对象，支持 `for` 循环遍历。

### 生成器 ⭐
用 `yield` 关键字的函数，**惰性求值**，每次调用 `next()` 才继续执行。

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a          # 暂停在此，返回 a
        a, b = b, a + b  # next() 后从这里继续

fib = fibonacci()
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1
print(next(fib))  # 2
```

### yield 工作原理 ⭐
```
调用 gen_func() → 返回生成器对象
     ↓
第一次 next() → 执行到第一个 yield → 暂停 → 返回值
     ↓
第二次 next() → 从暂停处继续 → 执行到下一个 yield → 暂停 → 返回值
     ↓
遇到 return 或函数结束 → 抛出 StopIteration
```

### 生成器 vs 列表
| 对比 | 列表 | 生成器 |
|------|:---:|:-----:|
| 所有元素都在内存 | ✅ | ❌ |
| 惰性求值 | ❌ | ✅ |
| 可重复迭代 | ✅ | ❌ |
| 适用场景 | 数据量小、需多次遍历 | **数据量大、只需一次遍历** |

### send / throw / close
```python
def echo():
    while True:
        received = yield
        print(f"Received: {received}")

gen = echo()
next(gen)         # 启动生成器（走到 yield）
gen.send("hello")  # 发送值给 yield 表达式 → "Received: hello"
gen.close()       # 关闭生成器
```

---

## 8. MRO 方法解析顺序（C3 线性化）？

Python 使用 **C3 线性化算法** 确定多继承时方法的查找顺序。

```python
class A:
    def method(self): print("A")

class B(A):
    def method(self): print("B")

class C(A):
    def method(self): print("C")

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

**C3 算法原则**：
1. 子类优先于父类
2. 保持基类的相对顺序（如 `D(B, C)` 中 B 在 C 前）
3. 单调性：一个类的 MRO 在子类中保持

> [!tip] **`super()` 的执行顺序按照 MRO**
> ```python
> class D(B, C):
>     def method(self):
>         super().method()  # 实际调用 B.method()，不是 A.method()
> ```

---

## 9. Python 的垃圾回收机制？

### 三种回收机制 ⭐

| 机制 | 原理 | 处理对象 |
|------|------|---------|
| **引用计数** | 每个对象维护 `ob_ref`，为 0 时立即回收 | 大多数对象 |
| **标记清除** | 从 GC Roots 遍历，标记可达对象，清除不可达 | **循环引用** |
| **分代回收** | 0 代（年轻）→ 1 代 → 2 代（年老），代龄越高扫描频率越低 | 长期存活对象 |

### 引用计数的优缺点
```python
import sys
a = []
print(sys.getrefcount(a))  # 2（a 的引用 + getrefcount 参数引用）
b = a
print(sys.getrefcount(a))  # 3
del b
print(sys.getrefcount(a))  # 2
```
- ✅ **优点**：实时回收、延迟低
- ❌ **缺点**：无法处理**循环引用**（a 引用 b，b 引用 a，外部无引用但引用计数不为 0）

### gc 模块
```python
import gc
gc.disable()        # 关闭自动 GC
gc.collect()        # 手动触发完整 GC
gc.set_threshold(700, 10, 10)  # 设置分代回收阈值
gc.get_objects()    # 获取所有被 GC 管理的对象
```

---

## 10. `__new__` vs `__init__`？

```python
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # 创建实例
        return cls._instance
    
    def __init__(self):
        # __new__ 返回同一实例，但 __init__ 每次调用都会被触发
        pass
```

| 方法 | 调用时机 | 作用 | 返回 |
|------|---------|------|------|
| `__new__` | 实例**创建之前**（类方法） | **分配内存**，控制实例创建过程 | 实例对象 |
| `__init__` | 实例**创建之后** | **初始化实例属性** | `None` |

> [!info] **执行顺序**
> `obj = MyClass()` → `__new__(cls)` 创建实例 → `__init__(self)` 初始化

---

## 11. Python 并发编程：多线程 vs 多进程 vs 协程？⭐

### 三者的核心区别

| 对比项 | 多线程 `threading` | 多进程 `multiprocessing` | 协程 `asyncio` |
|--------|:-----------------:|:----------------------:|:--------------:|
| 资源开销 | 轻量（共享同一进程内存） | 重（独立进程、独立内存） | **极轻**（单线程内切换） |
| GIL 影响 | CPU 密集型受限 | ✅ 不受 GIL 影响 | ⚠️ 同一线程内，不受 GIL 影响 |
| 数据共享 | 自动共享（需加锁） | 需 IPC（Queue/Pipe） | 共享同一线程变量 |
| 切换方式 | 操作系统抢占式调度 | 操作系统抢占式调度 | **用户态协作式**（async/await） |
| 适用场景 | IO 密集型 | CPU 密集型 | **高并发 IO 密集型** |

### asyncio 协程 ⭐
```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def main():
    urls = ["https://api.example.com/1", "https://api.example.com/2"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)  # 并发执行！
    return results

asyncio.run(main())
```

**协程的执行流程**：
```
async def → 定义协程函数
     ↓
调用协程函数 → 返回 coroutine 对象（不执行）
     ↓
await coro → 将协程注册到事件循环 → 开始执行
     ↓
遇到 await（IO 操作）→ 挂起当前协程 → 切换到其他协程
     ↓
IO 完成 → 恢复该协程继续执行
```

### 如何选择？
```python
# ✅ IO 密集型 → asyncio 协程（最高效）
async with aiohttp.ClientSession() as session: ...

# ✅ IO 密集型但有阻塞操作 → 多线程
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = pool.map(io_task, items)

# ✅ CPU 密集型 → 多进程
with multiprocessing.Pool(processes=os.cpu_count()) as pool:
    results = pool.map(cpu_task, items)
```

---

## 12. 魔法方法面试常考点？

```python
class MyClass:
    # 字符串表示
    def __str__(self):   # str() / print() 调用
        return "User-friendly string"
    def __repr__(self):  # 调试/交互式解释器
        return "MyClass()"
    
    # 容器方法
    def __len__(self):     # len()
        return 0
    def __getitem__(self, key):  # obj[key]
        ...
    def __iter__(self):    # for 循环
        ...
    
    # 属性访问
    def __getattr__(self, name):  # 属性不存在时调用
        return None
    def __setattr__(self, name, value):  # 设置属性
        ...
    
    # 可调用对象
    def __call__(self, *args):  # obj()
        return sum(args)
```

---

## 13. `__slots__` 原理与用途？

```python
# 没有 __slots__
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 25)
user.email = "alice@example.com"  # ✅ 动态添加属性（使用 __dict__）

# 有 __slots__
class UserSlotted:
    __slots__ = ("name", "age")  # 只允许这两个属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = UserSlotted("Alice", 25)
# user.email = "alice@example.com"  # ❌ AttributeError!
```

| 对比 | 普通类 | `__slots__` 类 |
|------|:-----:|:-------------:|
| 属性存储 | `__dict__`（哈希表） | **固定数组**（类似 C 结构体） |
| 内存占用 | 大（哈希表 + 键字符串） | **小**（节省 50-60% 内存） |
| 属性访问速度 | 哈希查找 | **直接索引访问**（快 10-30%） |
| 动态添加属性 | ✅ | ❌ |

> [!info] **适用场景**：大量实例的场景（如 ORM 模型、数据类），显式声明 `__slots__` 可大幅降低内存

---

# 第二部分：Python Web 框架 ⭐⭐

---

## 14. FastAPI 核心原理？⭐

### 技术栈
```
FastAPI = Starlette（ASGI 框架）+ Pydantic（数据校验）+ OpenAPI（自动文档）
```

| 组件 | 作用 |
|------|------|
| **Starlette** | ASGI 底层框架，处理路由、中间件、WebSocket |
| **Pydantic v2** | 基于 Rust 的数据校验引擎，定义请求/响应模型 |
| **OpenAPI / JSON Schema** | 自动生成 API 文档（`/docs` Swagger + `/redoc`） |

### 依赖注入（Depends）⭐
```python
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# 定义依赖
async def get_db():
    async with async_session() as session:
        yield session  # yield 表示请求结束后清理

# 注入依赖
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # db 自动从依赖中获取
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one()
```

**依赖注入的层级**（面试亮点）：
```
路径操作函数 → Depends(get_db)
    ↕
路径装饰器 → dependencies=[Depends(verify_token)]
    ↕
全局 → app.dependency_overrides[get_db] = test_get_db  # 测试时替换
```

### async def vs def ⭐
```python
@app.get("/async")      # async def → 协程，ASGI 事件循环调度
async def async_endpoint():
    async with aiohttp.ClientSession() as session:
        ...

@app.get("/sync")       # def → 在线程池中运行，不阻塞事件循环
def sync_endpoint():
    time.sleep(1)       # 阻塞操作不会阻塞事件循环
    return {"message": "running in thread pool"}
```

> [!tip] **面试核心**
> - FastAPI 自动区分 async/def 和 def：def 在**线程池**运行，不阻塞事件循环
> - 如果你用 `time.sleep()` 在 async 函数中，它会**阻塞整个事件循环**，改用 `asyncio.sleep()`

### Pydantic v2 核心
```python
from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)
    email: str | None = None
    
    @field_validator("name")
    @classmethod
    def name_must_not_contain_numbers(cls, v):
        if any(c.isdigit() for c in v):
            raise ValueError("name must not contain numbers")
        return v

# 自动 JSON Schema
print(UserCreate.model_json_schema())
```

---

## 15. FastAPI vs Flask vs Django 对比？

| 对比维度 | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| **定位** | 高性能异步 API 框架 | 轻量级微框架 | 全栈大而全 |
| **异步支持** | ✅ 原生 ASGI | ❌ WSGI（Flask 2.0 支持有限） | ✅ 3.0+ 支持 ASGI |
| **性能** | ⭐ 最高（媲美 Node.js/Go） | 中等 | 中等 |
| **数据校验** | ✅ Pydantic（自动） | ❌ 需手动 / Marshmallow | ✅ DRF Serializer |
| **自动文档** | ✅ Swagger + ReDoc 自动生成 | ❌ Flask-RESTX 等插件 | ✅ DRF-YASG 等插件 |
| **ORM** | SQLAlchemy（可选） | SQLAlchemy（可选） | ⭐ Django ORM 内置 |
| **生态丰富度** | 成长中 | 很丰富（插件多） | ⭐ 最丰富（自带管理后台、Auth、Admin） |
| **学习曲线** | 平缓 | **最平缓** | 较陡 |
| **最适合** | **API 服务、微服务、AI 应用** | 简单应用、原型 | 内容站点、CMS、企业内部系统 |

---

## 16. Django ORM 优化（N+1 问题）？

### N+1 查询问题 ⭐
```python
# ❌ N+1 问题
books = Book.objects.all()           # 1 次查询
for book in books:
    print(book.author.name)          # N 次查询 → 总共 N+1 次

# ✅ select_related 解决（JOIN 查询，适用于 ForeignKey）
books = Book.objects.select_related('author').all()  # 1 次 JOIN 查询
for book in books:
    print(book.author.name)          # 不再产生额外查询

# ✅ prefetch_related 解决（适用于 ManyToMany/反向关联）
authors = Author.objects.prefetch_related('books').all()  # 2 次查询
for author in authors:
    print([book.title for book in author.books.all()])     # 不再产生额外查询
```

### select_related vs prefetch_related
| | select_related | prefetch_related |
|--|--------------|-----------------|
| **查询方式** | SQL **JOIN**（连表查询） | **分两次查询**，Python 中关联 |
| **适用字段** | ForeignKey、OneToOneField | ManyToManyField、反向 ForeignKey |
| **查询次数** | 1 次 | 2 次（主表 + 关联表） |
| **大数据量** | JOIN 可能导致大结果集 | 分次查询更可控 |

---

# 第三部分：Python 数据库操作

---

## 17. SQLAlchemy 2.0 核心？⭐

### 声明式映射
```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(unique=True)
    age: Mapped[int] = mapped_column(default=0)
    
    # 关系
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
```

### 异步引擎（与 FastAPI 搭配）
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async def get_user(user_id: int):
    async with AsyncSession(engine) as session:
        # SQLAlchemy 2.0 风格查询
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

### Session 管理
```python
# 每个请求创建新的 Session 实例
async def get_db():
    async with AsyncSession(engine) as session:
        yield session          # FastAPI 依赖注入使用

# 事务管理
async def create_user(db: AsyncSession, name: str):
    user = User(name=name)
    db.add(user)
    await db.commit()          # 提交事务
    await db.refresh(user)     # 刷新获取数据库生成的值
    return user
```

---

## 18. Redis 在 Python 中的使用？

```python
import redis.asyncio as aioredis

# 连接池管理
redis_client = aioredis.from_url(
    "redis://localhost:6379/0",
    max_connections=10,
    decode_responses=True
)

# Pipeline 批量操作
async def batch_operation():
    async with redis_client.pipeline(transaction=True) as pipe:
        await pipe.set("key1", "value1")
        await pipe.set("key2", "value2")
        await pipe.get("key1")
        results = await pipe.execute()  # 一次网络往返

# Lua 脚本（实现分布式锁）
lock_script = """
if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'PX', ARGV[2]) then
    return 1
end
return 0
"""
locked = await redis_client.eval(lock_script, 1, "lock:key", "owner", 30000)
```

---

# 第四部分：爬虫 & 自动化

---

## 19. Scrapy 框架核心组件？

```
Spider（爬虫）→ Requests → Scheduler（调度器）→ Downloader（下载器）→ Responses
    ↕                                              ↕
Item Pipeline（数据处理）                     Middleware（中间件）
```

| 组件 | 作用 |
|------|------|
| **Spider** | 定义爬取逻辑、解析规则、提取 Item |
| **Engine** | 控制数据流在组件之间流转 |
| **Scheduler** | 接收请求并排队去重（集成 Redis 实现分布式） |
| **Downloader** | 下载页面，支持中间件（代理、UA、Cookie） |
| **Item Pipeline** | 清洗、验证、存储数据 |
| **Middleware** | 修改请求/响应（Downloader/Spider 中间件） |

### 分布式爬虫（Scrapy-Redis）
```python
# 核心变化：用 Redis 替换 Scheduler 的去重队列
# settings.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = "redis://localhost:6379"

# 多个爬虫实例共享同一 Redis 队列，自动分配 URL
```

---

## 20. 反爬与反反爬策略？⭐

| 反爬手段 | 反反爬策略 |
|---------|-----------|
| **IP 限流** | IP 代理池（付费代理 + 自建代理 IP） |
| **User-Agent 检测** | 随机 UA 池（`fake-useragent` 库） |
| **Cookie 校验** | Session 保持 + 模拟登录 |
| **验证码** | OCR + 打码平台 + 深度学习（CNN） |
| **签名/加密参数** | 逆向 JS（AST 还原 + 补环境） |
| **WebDriver 检测** | stealth.min.js 隐藏特征 / Playwright |
| **行为分析** | 随机延时 + 鼠标轨迹模拟 + 浏览器指纹 |

### 请求频率控制策略
```python
import time
import random

class RateLimiter:
    def __init__(self, min_delay=1.0, max_delay=3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
    
    def wait(self):
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)  # 随机延时，避免固定间隔

# 更高级的自适应策略
class AdaptiveRateLimiter:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.delay = 1.0
    
    def on_success(self):
        self.success_count += 1
        if self.success_count > 10:
            self.delay = max(0.5, self.delay * 0.9)  # 成功多了加快速度
    
    def on_fail(self):
        self.fail_count += 1
        self.delay = min(10, self.delay * 2)  # 失败马上放慢
        time.sleep(self.delay * 2)
```

---

# 第五部分：数据分析基础

---

## 21. NumPy 核心概念？

### ndarray vs list
```python
import numpy as np

# ndarray：同质、连续内存、支持向量化
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)       # [2, 4, 6, 8, 10] — 向量化操作
print(arr.shape)     # (5,)
print(arr.dtype)     # int64
```

| 对比 | Python list | NumPy ndarray |
|------|:----------:|:-------------:|
| 元素类型 | 任意（对象引用） | **同质**（单一 dtype） |
| 内存布局 | 不连续（指针数组） | **连续内存块** |
| 运算方式 | 循环遍历 | **向量化**（C 语言实现） |
| 性能 | 慢 | ⭐ **快 10-100 倍** |

### 广播机制 ⭐
```python
# 广播：不同形状的数组自动扩展为相同形状
a = np.array([[1, 2, 3], [4, 5, 6]])  # (2,3)
b = np.array([10, 20, 30])            # (3,) → 广播为 (2,3)
print(a + b)
# [[11 22 33]
#  [14 25 36]]
```

---

## 22. Pandas 常用操作？

```python
import pandas as pd

# 创建 DataFrame
df = pd.read_csv("data.csv")

# 常用操作
df.head()                    # 前 5 行
df.info()                    # 列类型、非空计数
df.describe()                # 统计摘要
df.isnull().sum()            # 每列空值数

# 数据清洗
df.dropna()                  # 删除空值行
df.fillna(df.mean())         # 用均值填充
df.drop_duplicates()         # 去重

# 分组聚合
df.groupby("category")["price"].agg(["count", "mean", "sum"])

# 多表关联
pd.merge(df1, df2, on="user_id", how="left")

# 时间序列
df["date"] = pd.to_datetime(df["date"])
df.set_index("date").resample("M")["revenue"].sum()  # 按月聚合
```

---

# 第六部分：DevOps & 部署

---

## 23. WSGI vs ASGI？Gunicorn vs Uvicorn？⭐

| 协议 | 全称 | 特点 | 对应服务器 |
|------|------|------|-----------|
| **WSGI** | Web Server Gateway Interface | 同步、阻塞 | Gunicorn、uWSGI |
| **ASGI** | Asynchronous Server Gateway Interface | 异步、支持 WebSocket | **Uvicorn**、Daphne |

### 部署方案对比
```python
# ① 开发环境 — 直接 Uvicorn
uvicorn main:app --reload --port 8000

# ② 生产环境 — Gunicorn + Uvicorn Workers（推荐）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# ③ 生产环境 — Uvicorn 直接多进程
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker 多阶段构建（Python）
```dockerfile
# 构建阶段
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段（使用 slimmer 基础镜像）
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> [!info] **Nginx 反向代理配置**
> ```nginx
> upstream backend {
>     server 127.0.0.1:8001 weight=3;
>     server 127.0.0.1:8002 weight=3;
> }
> server {
>     listen 443 ssl;
>     location / {
>         proxy_pass http://backend;
>         proxy_set_header Host $host;
>         proxy_set_header X-Real-IP $remote_addr;
>     }
>     location /ws {
>         proxy_pass http://backend;
>         proxy_http_version 1.1;
>         proxy_set_header Upgrade $http_upgrade;
>         proxy_set_header Connection "upgrade";
>     }
> }
> ```

---

## 24. pytest 核心特性？⭐

```python
import pytest

# Fixture（依赖注入）
@pytest.fixture
def db_session():
    """每个测试函数获取独立数据库会话"""
    session = create_test_session()
    yield session
    session.close()  # 测试结束后清理

# 参数化测试
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

# Mock（模拟外部依赖）
def test_get_user(mocker):
    mock_response = {"id": 1, "name": "Alice"}
    mocker.patch("app.api.requests.get", return_value=mock_response)
    result = get_user(1)
    assert result["name"] == "Alice"

# conftest.py 共享 fixture
# 将 db_session 等通用 fixture 放在 tests/conftest.py 中，自动对所有测试可见
```

| pytest 特性 | 作用 |
|------------|------|
| `fixture` | 依赖注入式资源管理，替代 setup/teardown |
| `parametrize` | 一组参数运行多次测试 |
| `mocker` | 替换外部依赖（需 pip install pytest-mock） |
| `conftest.py` | 共享 fixture 和 hooks 的作用域文件 |
| `--cov` | 测试覆盖率报告（需 pip install pytest-cov） |

---

# 第七部分：系统设计（Python 版）

---

## 25. 设计一个异步任务队列（Celery 架构）？

```
Producer（FastAPI/Flask 应用）
    ↓ 发送任务
Redis/RabbitMQ（Broker — 消息中间件）
    ↓ 分发任务
Celery Worker（消费者进程）
    ↓ 存储结果
Redis/DB（Result Backend）
```

```python
# tasks.py
from celery import Celery

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",       # 消息队列
    backend="redis://localhost:6379/1"       # 结果存储
)

@app.task(bind=True, max_retries=3)
def process_order(self, order_id):
    try:
        # 耗时操作：发送邮件、生成 PDF、调用第三方 API
        do_heavy_work(order_id)
    except Exception as e:
        self.retry(countdown=60)  # 60s 后重试

# FastAPI 中调用
@app.post("/orders")
async def create_order(order: OrderCreate):
    # 异步提交任务，立即返回
    task = process_order.delay(order.id)
    return {"task_id": task.id, "status": "processing"}
```

### 面试要点
| 概念 | 说明 |
|------|------|
| **Broker** | 消息中间件（Redis / RabbitMQ / SQS） |
| **Worker** | 执行任务的进程，支持水平扩展 |
| **Result Backend** | 存储任务执行结果 |
| **Task** | 最小执行单元，支持重试、超时、绑定 |
| **Beat** | 定时任务调度器（类似 cron） |
| **Flower** | Celery 监控面板（任务状态、Worker 状态） |

---

## 26. 设计一个实时数据看板？

### 架构
```
数据源（DB / API / MQ）
    ↓ 定时采集
数据处理器（Pandas 聚合）
    ↓ Pub/Sub
Redis（缓存 + 发布订阅）
    ↓
WebSocket Server（FastAPI WebSocket）
    ↓
前端（ECharts + Vue/React）
```

### 后端实现示例
```python
# WebSocket 推送
class DataBoard:
    def __init__(self):
        self.connections: set[WebSocket] = set()
    
    async def broadcast(self, data: dict):
        dead = set()
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except Exception:
                dead.add(ws)
        self.connections -= dead
    
    async def data_generator(self):
        """定时从 Redis 读取最新数据推送给前端"""
        while True:
            data = await redis_client.get("dashboard:realtime")
            if data:
                await self.broadcast(json.loads(data))
            await asyncio.sleep(5)  # 每 5 秒推送一次

# FastAPI WebSocket 端点
board = DataBoard()

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    board.connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # 保持连接
    except WebSocketDisconnect:
        board.connections.discard(websocket)
```

---

## 27. FastAPI 微服务架构设计？

### 服务拆分原则
```
每个微服务独立：
  - 独立数据库（数据隔离）
  - 独立部署单元（Docker + K8s）
  - 独立 API 版本管理

服务间通信：
  - 同步：HTTP/gRPC（实时查询）
  - 异步：消息队列（事件驱动）
```

### API 网关设计要点
```python
# 统一的 API 网关（用 FastAPI 实现）
app = FastAPI(title="API Gateway")

# 路由转发
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_router(path: str, request: Request):
    """转发到 User Service"""
    async with httpx.AsyncClient() as client:
        url = f"http://user-service:8001/{path}"
        return await forward_request(client, url, request)

# 统一认证
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token or not await verify_token(token):
        return JSONResponse(status_code=401, content={"error": "unauthorized"})
    return await call_next(request)

# 统一限流
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, 60)
    if count > 100:
        return JSONResponse(status_code=429, content={"error": "too many requests"})
    return await call_next(request)
```

---

# 第八部分：简历项目准备

---

## 28. Python 全栈面试必问项目问题？

### "你们的项目用了什么技术栈？为什么选 FastAPI？"
> **回答框架**：
> - 项目需要高并发 WebSocket 推送（在线聊天/实时看板）→ FastAPI 原生支持 ASGI
> - 需要自动生成 API 文档给前端 → FastAPI + Pydantic 零成本 Swagger
> - 性能要求高 → FastAPI 性能是 Flask 的 2-3 倍，接近 Go 的水平

### "Python 项目的性能瓶颈在哪？怎么优化的？"
> ⭐ **常见优化三板斧**：
> 1. **IO 异步化**：用 async/await 替换同步 requests/数据库操作，吞吐量从 200/s → 2000/s
> 2. **缓存策略**：热点数据用 Redis 缓存（Pandas 聚合结果缓存 5 分钟不重复计算）
> 3. **数据库优化**：SQLAlchemy 查询加 `selectinload` / `joinedload` 解决 N+1，慢查询加索引

### "Python 项目的部署方案？"
```yaml
# Docker Compose 多服务编排
services:
  api:
    build: .
    command: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - db
  
  worker:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
  
  db:
    image: postgres:15-alpine
```

---

## 29. Python 面试对比速查表

| 面试问法 | 核心考点 | 一句话回答 |
|---------|---------|-----------|
| "Python 的 GIL 是什么？" | 多线程限制 | 同一时刻只有一个线程执行字节码，CPU 密集用多进程 |
| "装饰器有什么用？" | 切面编程 | 在不修改原函数的前提下增强功能，如日志/鉴权/缓存 |
| "生成器和迭代器区别？" | 惰性求值 | 生成器用 yield 返回，每次 next 才计算，节省内存 |
| "怎么理解 async/await？" | 协程 | 用户态协作式调度，await 挂起当前协程，IO 完成后恢复 |
| "FastAPI 为什么快？" | ASGI + Pydantic v2 | Starlette 异步 + Pydantic v2 Rust 校验引擎 |
| "Django N+1 怎么解决？" | ORM 优化 | select_related（JOIN）和 prefetch_related（分次查询） |
| "Python 内存泄漏怎么排查？" | GC 分析 | objgraph / tracemalloc / gc.get_objects() |

> [!tip] **Python 面试核心策略**
> - **深度优先**：重点准备 FastAPI、async/await、装饰器、GIL 四个高频话题
> - **项目为重**：准备 2 个 Python 项目亮点（一个后端的 + 一个 AI/数据的）
> - **与 Java 差异化**：Python 面试更看重"解决问题的能力"而非"原理背诵"
> - **加分项**：异步编程经验、Pandas 数据处理、爬虫反爬经验、与 AI/LLM 集成经验
