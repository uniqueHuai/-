# Python基础与进阶篇

## 一、Python 概述

### 解释型与动态类型

Python 是一种 **解释型、动态类型** 的高级编程语言，以其简洁的语法和强大的生态著称。

```
源代码（.py）
   │ Python 解释器（CPython）
   ▼
字节码（.pyc）
   │ PVM（Python 虚拟机）
   ▼
机器码执行
```

| 特性 | 说明 |
|:----:|------|
| **解释型** | 源代码无需编译，由解释器逐行执行，开发效率高 |
| **动态类型** | 变量不需要声明类型，运行时确定 |
| **胶水语言** | 可以轻松调用 C/C++/Java 等语言编写的库 |
| **自动内存管理** | 引用计数 + 垃圾回收（GC），无需手动释放内存 |

### CPython 运行机制

> [!info] **CPython** 是 Python 的官方和默认实现，其工作流程为：
> 1. 源代码（`.py`）被编译成**字节码**（`.pyc`）
> 2. 字节码由 **PVM（Python 虚拟机）** 逐条执行
> 3. 整个过程对开发者透明

### Python 2 vs Python 3

| 对比 | Python 2（已停止维护） | Python 3（当前标准） |
|:----:|:----------------------:|:--------------------:|
| **维护状态** | ❌ 2020 年 1 月 1 日停止维护 | ✅ 活跃开发与维护 |
| **print** | `print "hello"`（语句） | `print("hello")`（函数） |
| **整数除法** | `3 / 2 = 1`（整数除法） | `3 / 2 = 1.5`（真除法） |
| **字符串编码** | 默认 ASCII | 默认 **UTF-8** |
| **range** | `range()` 返回列表，`xrange()` 返回迭代器 | `range()` 返回迭代器（`xrange` 已移除） |
| **异常语法** | `except Exception, e` | `except Exception as e` |
| **input** | `input()` 等价于 `eval(raw_input())` | `input()` 返回字符串 |

> [!tip] **当前选择**：所有新项目应使用 **Python 3.8+**，推荐 **3.11+**（性能大幅提升）。

### 常用应用领域

| 领域 | 典型框架/库 | 说明 |
|:----:|-------------|------|
| **Web 开发** | Django、Flask、FastAPI | 全栈或 API 服务 |
| **数据科学** | NumPy、Pandas、Matplotlib | 数据处理与可视化 |
| **机器学习/AI** | PyTorch、TensorFlow、scikit-learn | 深度学习与模型训练 |
| **自动化脚本** | 无额外依赖 | 文件处理、系统管理、爬虫 |
| **后端服务** | FastAPI、Celery | 高性能 API + 异步任务队列 |
| **游戏开发** | Pygame | 2D 游戏开发 |
| **DevOps** | Ansible、SaltStack | 配置管理与自动化运维 |

> [!info] Python 在 **TIOBE 和 Stack Overflow 调查**中长期稳居前 3，且是 AI/ML 领域的绝对主流语言。

---

## 二、基本数据类型

### 内置类型概览

Python 中的一切皆是对象——`int`、`float`、甚至 `NoneType` 都是类。

| 类型 | 关键字 | 示例 | 不可变 |
|:----:|:------:|:----:|:------:|
| **整型** | `int` | `42`、`-1`、`0` | ✅ |
| **浮点型** | `float` | `3.14`、`1e5`、`float('inf')` | ✅ |
| **复数** | `complex` | `1+2j`、`complex(1, 2)` | ✅ |
| **布尔型** | `bool` | `True`、`False` | ✅ |
| **空值** | `NoneType` | `None` | ✅ |

### 数字运算

```python
# 基本运算
a, b = 10, 3
print(a + b)    # 13  加法
print(a - b)    # 7   减法
print(a * b)    # 30  乘法
print(a / b)    # 3.333...  真除法（返回 float）
print(a // b)   # 3   整除（向下取整）
print(a % b)    # 1   取模
print(a ** b)   # 1000 幂运算

# 注意：// 是向下取整（floor），不是向零取整
print(-10 // 3)  # -4 （-3.33 向下取整为 -4）
print(10 // -3)  # -4

# 内置数学函数
print(abs(-5))      # 5
print(divmod(10, 3))  # (3, 1)
print(pow(2, 10))   # 1024
print(round(3.1415, 2))  # 3.14
```

### 类型转换

```python
# 显式类型转换
int("42")         # 42     str → int
float("3.14")     # 3.14   str → float
str(100)          # "100"  int → str
bool(0)           # False  int → bool
bool("")          # False 空字符串 → False
bool("hello")     # True  非空字符串 → True

# 数值进制转换
bin(42)           # '0b101010'  二进制
oct(42)           # '0o52'      八进制
hex(42)           # '0x2a'      十六进制
int("101010", 2)  # 42          二进制字符串 → 十进制
```

### `is` vs `==`

> [!warning] **核心区别**
> - `==` 比较的是**值**（调用 `__eq__()` 方法）
> - `is` 比较的是**内存地址**（是否同一个对象）

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  （值相等）
print(a is b)   # False （不同对象）
print(a is c)   # True  （同一对象）

# 小整数缓存（-5 ~ 256）
x = 256
y = 256
print(x is y)   # True  （小整数被缓存）

x = 257
y = 257
print(x is y)   # False （超出缓存范围）
```

> [!tip] **判空推荐**：Python 中判空常用隐式布尔转换，而非 `is None` 或 `== None`：
> ```python
> if not some_list:     # ✅ 推荐
> if len(some_list) == 0:  # ❌ 不推荐
> if some_list is None:    # 仅用于判断 None，不用于判断空
> ```

---

## 三、字符串（String）

### 创建与转义

```python
# 三种引号
s1 = '单引号'
s2 = "双引号"
s3 = '''三引号
支持多行'''
s4 = """也是三引号"""

# 转义字符
s = "hello\nworld"     # 换行
s = "tab\there"        # 制表符
s = "他说：\"你好\""    # 引号转义

# 原始字符串（r 前缀）— 不处理转义
path = r"C:\Users\name"   # 等价于 "C:\\Users\\name"
regex = r"\d+\.\d+"       # 正则表达式中极常用
```

### 切片语法 ⭐

切片是 Python 最强大的特性之一，格式为 `[start:stop:step]`：

```python
s = "Python编程"

# 基本切片
print(s[0])      # 'P'          正索引，从 0 开始
print(s[-1])     # '程'         负索引，-1 是最后一个
print(s[2:5])    # 'tho'        从索引 2 到 4（左闭右开）
print(s[:3])     # 'Pyt'        从头到索引 2
print(s[3:])     # 'hon编程'      从索引 3 到末尾
print(s[:])      # 'Python编程'  复制整个字符串

# 步长
print(s[::2])    # 'Pto编'       每隔一个取一个
print(s[::-1])   # '程编nohtyP'  反转字符串（经典用法）
print(s[1:5:2])  # 'yo'         从索引 1 到 4，步长 2
```

```python
# 切片边界示意图
# ┌───┬───┬───┬───┬───┬───┬───┬───┐
# │ P │ y │ t │ h │ o │ n │ 编│ 程│
# ├───┼───┼───┼───┼───┼───┼───┼───┤
# │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │  正索引
# │-8 │-7 │-6 │-5 │-4 │-3 │-2 │-1 │  负索引
# └───┴───┴───┴───┴───┴───┴───┴───┘
```

### 常用方法

```python
text = "  Hello, Python World!  "

# 大小写
text.lower()              # "  hello, python world!  "
text.upper()              # "  HELLO, PYTHON WORLD!  "
text.title()              # "  Hello, Python World!  "
text.swapcase()           # "  hELLO, pYTHON wORLD!  "

# 查找判断
text.find("Python")       # 9   找不到返回 -1
text.index("Python")      # 9   找不到抛 ValueError
text.startswith("Hello")  # False（前面有空格）
text.endswith("!")        # True
text.count("o")           # 3

# 判断
"abc123".isalnum()        # True  字母或数字
"abc".isalpha()           # True  纯字母
"123".isdigit()           # True  纯数字
"hello".isascii()         # True  ASCII 字符
"Hello".istitle()         # True  首字母大写

# 替换与分割 — ⭐ 高频
text.strip()              # "Hello, Python World!"  去除两端空白
text.lstrip()             # "Hello, Python World!  " 去除左侧空白
text.rstrip()             # "  Hello, Python World!" 去除右侧空白
"a,b,c".split(",")        # ['a', 'b', 'c']
"a\nb\nc".splitlines()    # ['a', 'b', 'c']
"-".join(["a", "b", "c"]) # "a-b-c"          ⭐ join 是 split 的逆操作
text.replace("Python", "Java")  # "  Hello, Java World!  "

# 填充对齐
"42".zfill(5)             # "00042"
"hello".center(11, "*")   # "***hello***"
"hello".ljust(10, "-")    # "hello-----"
```

### 格式化 ⭐

```python
name, age = "Alice", 25

# ⭐ f-string（Python 3.6+）— 最推荐
print(f"我叫{name}，今年{age}岁")                    # 基本
print(f"圆周率 ≈ {3.1415926:.2f}")                  # 保留 2 位小数
print(f"十六进制：{255:#x}")                         # 0xff
print(f"百分比：{0.856:.1%}")                        # 85.6%
print(f"右对齐：{name:>10}")                         # "     Alice"
print(f"左对齐：{name:<10}")                         # "Alice     "
print(f"补零：{42:05d}")                             # "00042"
print(f"千分位：{1234567:,}")                        # "1,234,567"

# format() 方法
"我叫{}，今年{}岁".format(name, age)                 # 位置参数
"我叫{name}，今年{age}岁".format(name=name, age=age)  # 关键字参数
"{:.2f}".format(3.14159)                              # "3.14"

# % 格式化（旧式，了解即可）
"我叫%s，今年%d岁" % (name, age)
```

> [!tip] **f-string 是 Python 3.6+ 最推荐的格式化方式**，性能高、可读性强、支持表达式。**避免**在日常代码中使用 `%` 格式化。

---

## 四、容器类型

### 4.1 列表（List）

列表是 **有序、可变、可重复** 的序列，使用 `[]` 创建。

```python
# 创建
lst = [1, 2, 3, "hello", True]   # 可包含不同类型
lst2 = list(range(5))             # [0, 1, 2, 3, 4]
empty = []

# 索引与切片（同字符串语法）
print(lst[0])       # 1
print(lst[-1])      # True
print(lst[1:3])     # [2, 3]

# 常用方法 — ⭐ 必须掌握
lst = [3, 1, 4, 1, 5]
lst.append(9)             # [3, 1, 4, 1, 5, 9]   末尾追加
lst.insert(0, 0)          # [0, 3, 1, 4, 1, 5, 9] 指定位置插入
lst.extend([10, 11])      # [0, 3, 1, 4, 1, 5, 9, 10, 11] 合并列表
lst.pop()                 # 11 末尾弹出
lst.pop(1)                # 3  弹出索引 1 的元素
lst.remove(1)             # 删除第一个值为 1 的元素
lst.sort()                # [0, 1, 4, 5, 9, 10]   原地排序
lst.sort(reverse=True)    # [10, 9, 5, 4, 1, 0]
sorted(lst)               # 返回新排序列表（不修改原列表）
lst.reverse()             # 反转
len(lst)                  # 长度
lst.index(5)              # 5 的索引
lst.count(1)              # 1 出现的次数
```

#### 列表推导式 ⭐

```python
# 基本：每个元素平方
squares = [x**2 for x in range(10)]       # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件：筛选偶数
evens = [x for x in range(20) if x % 2 == 0]

# 嵌套循环：矩阵扁平化
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]  # [1, 2, 3, 4, 5, 6]

# 带 else 的条件（for 前面写三目）
result = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

---

### 4.2 元组（Tuple）

元组是 **有序、不可变、可重复** 的序列，使用 `()` 创建。

```python
# 创建
t = (1, 2, 3)
single = (1,)         # 注意：单个元素必须加逗号
not_tuple = (1)       # 这是 int！
tuple_from_list = tuple([1, 2, 3])

# 元组不可变
t[0] = 10             # ❌ TypeError

# 解包（unpacking）— Python 的特色
a, b, c = (1, 2, 3)   # a=1, b=2, c=3
head, *rest = [1, 2, 3, 4]  # head=1, rest=[2, 3, 4]
first, *mid, last = range(10)  # first=0, mid=[1..8], last=9

# 交换变量（经典用法）
a, b = b, a  # ✅ Pythonic 交换，无需临时变量
```

#### namedtuple

```python
from collections import namedtuple

# 定义
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

# 访问
print(p.x)         # 10  （属性风格）
print(p[0])        # 10  （索引风格）
x, y = p           # 解包

# namedtuple 本质是 tuple，仍不可变
p.x = 100          # ❌ AttributeError
```

> [!tip] **何时用元组？**
> - 函数返回多个值时（本质是元组自动解包）
> - 需要**不可变**的数据（作为字典的 key）
> - 比列表更省内存

---

### 4.3 字典（Dict）

字典是 **键值对（key-value）** 的无序集合，Python 3.7+ 保持插入顺序。

```python
# 创建
d = {"name": "Alice", "age": 25, "city": "Beijing"}
d2 = dict(name="Bob", age=30)
d3 = dict(zip(["a", "b"], [1, 2]))   # {'a': 1, 'b': 2}

# 增删改查 ⭐
d["email"] = "alice@example.com"      # 新增/修改
d.update({"phone": "123", "age": 26}) # 批量更新

d.get("name")              # "Alice"   存在则返回值
d.get("salary", 0)         # 0         不存在返回默认值
d["name"]                  # "Alice"   不存在抛 KeyError

d.pop("phone")             # 删除并返回值
d.pop("not_exist", None)   # 不存在的 key 返回默认值
del d["city"]              # 删除
d.clear()                  # 清空

# 遍历
for key in d:                    # 遍历 key
for key, val in d.items():       # 同时遍历 key 和 value ⭐
for val in d.values():           # 遍历 value
for key in d.keys():             # 遍历 key（显式）

# ⭐ setdefault — 不存在时设置默认值并返回
d.setdefault("count", 0)         # 如果 "count" 不存在，设为 0 并返回 0
d.setdefault("count", 100)       # 已存在，返回原值（不覆盖）
```

#### get / setdefault / defaultdict

```python
# 场景：统计字符出现次数

# ❌ 繁琐写法
counts = {}
for c in "hello world":
    if c in counts:
        counts[c] += 1
    else:
        counts[c] = 1

# ✅ get 简化
counts = {}
for c in "hello world":
    counts[c] = counts.get(c, 0) + 1

# ✅ setdefault 简化
counts = {}
for c in "hello world":
    counts.setdefault(c, 0)
    counts[c] += 1

# ⭐ defaultdict 最简洁
from collections import defaultdict
counts = defaultdict(int)       # 默认值为 0
for c in "hello world":
    counts[c] += 1

# defaultdict 的其他默认值
dd = defaultdict(list)          # 默认空列表
dd["key"].append(1)             # 无需先初始化
dd2 = defaultdict(set)          # 默认空集合
```

#### Counter

```python
from collections import Counter

# 自动统计
counter = Counter("hello world")
print(counter)        # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

# 常用操作
counter.most_common(2)    # [('l', 3), ('o', 2)]  出现最多的 2 个
counter["z"]              # 0   不存在的 key 返回 0（不会抛 KeyError）
list(counter.elements())  # 展开为列表（按出现次数重复）

# Counter 支持运算
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)   # Counter({'a': 4, 'b': 3})
print(c1 - c2)   # Counter({'a': 2})  只保留正数
```

#### 字典推导式

```python
# 键值互换
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}   # {1: 'a', 2: 'b', 3: 'c'}

# 过滤
squared = {x: x**2 for x in range(10) if x % 2 == 0}  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 两个列表转字典
keys = ["a", "b", "c"]
vals = [1, 2, 3]
d = {k: v for k, v in zip(keys, vals)}   # {'a': 1, 'b': 2, 'c': 3}
```

---

### 4.4 集合（Set / Frozenset）

集合是 **无序、可变、不重复** 的元素集合，使用 `{}` 创建（空集合用 `set()`）。

```python
# 创建
s = {1, 2, 3, 1, 2}       # {1, 2, 3}  自动去重
s2 = set([1, 2, 2, 3])    # 从列表创建
empty_set = set()          # 空集合（{} 是空字典！）

# 增删
s.add(4)                  # {1, 2, 3, 4}
s.remove(2)               # {1, 3, 4}  不存在抛 KeyError
s.discard(10)             # 不存在也不抛异常
s.pop()                   # 随机弹出一个元素

# ⭐ 集合运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)    # {1, 2, 3, 4, 5, 6}  并集
print(a & b)    # {3, 4}              交集
print(a - b)    # {1, 2}              差集（在 a 不在 b）
print(a ^ b)    # {1, 2, 5, 6}        对称差集
print(a <= b)   # False               子集判断
print(a >= b)   # False               超集判断

# 集合推导式
squares = {x**2 for x in range(10)}   # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}
```

#### Frozenset（不可变集合）

```python
fs = frozenset([1, 2, 3])   # 不可变，可作为字典 key
fs.add(4)                   # ❌ AttributeError

# 应用：去重但需要 hashable 的场景
data = [{1, 2}, {1, 2}, {3, 4}]    # 列表套集合（set 不可 hash）
unique = set(frozenset(s) for s in data)  # {frozenset({1, 2}), frozenset({3, 4})}
```

> [!info] **使用场景总结**
> - **去重**：将列表转集合再转回列表
> - **快速成员检测**：`x in set` 是 O(1)，`x in list` 是 O(n)
> - **集合运算**：共同好友、权限交集/差集、标签过滤

---

## 五、运算符

### 运算符一览

| 类型 | 运算符 | 示例 |
|:----:|:------:|:----:|
| **算术** | `+` `-` `*` `/` `//` `%` `**` | `3 ** 2 = 9` |
| **比较** | `==` `!=` `>` `<` `>=` `<=` | `5 > 3 → True` |
| **赋值** | `=` `+=` `-=` `*=` `/=` `//=` `%=` `**=` | `x += 1` |
| **逻辑** | `and` `or` `not` | `x > 0 and x < 10` |
| **位运算** | `&` `|` `^` `~` `<<` `>>` | `x << 1`（左移 1 位） |
| **身份** | `is` `is not` | `a is None` |
| **成员** | `in` `not in` | `"hello" in text` |

### 身份运算符（is, is not）

```python
# is：比较对象的内存地址（是否是同一个对象）
# ==：比较对象的值

a = [1, 2, 3]
b = a.copy()
print(a == b)   # True  值相同
print(a is b)   # False 不同对象

# is 的典型用法
if x is None:       # ✅ 推荐（判断 None）
if x is True:       # ✅ 推荐（判断单例）
```

### 成员运算符（in, not in）

```python
# in 对序列、字典、集合均适用
print(1 in [1, 2, 3])          # True
print("key" in {"key": 1})     # True  （字典判断的是 key）
print("a" in "hello world")    # False
```

### 逻辑运算符的短路特性

```python
# Python 的 and/or 返回的是决定结果的那个值（并非 True/False）
print(0 and 10)     # 0     0 为假，短路，返回 0
print(3 and 10)     # 10    3 为真，继续算 10，返回 10
print(0 or 10)      # 10    0 为假，继续算 10，返回 10
print(3 or 10)      # 3     3 为真，短路，返回 3

# 经典应用：默认值
name = input_name or "default"   # 如果 input_name 为空，用 "default"
```

> [!warning] **Python 没有 `++` 和 `--` 运算符**。`++i` 在 Python 中不会被解析为自增，而是 `+(+i)`（正号运算）。

---

## 六、流程控制

### if / elif / else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

# ⭐ 三元表达式（条件表达式）
grade = "A" if score >= 90 else "B"
age_status = "成年" if age >= 18 else "未成年"
```

### for 循环与 for-else

```python
# 基础遍历
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i, val in enumerate(lst):    # 同时获取索引和值 ⭐
    print(i, val)

for k, v in d.items():           # 遍历字典 ⭐
    print(k, v)

# ⭐ for-else：当循环**正常结束**（未被 break）时执行 else
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} = {x} * {n//x}")
            break
    else:
        print(f"{n} 是质数")    # 内层循环未被 break 时执行

# 等价于 flag 写法，但更优雅
```

### while 循环

```python
count = 0
while count < 5:
    print(count)
    count += 1

# 无限循环（需配合 break）
while True:
    line = input("输入（q 退出）: ")
    if line == "q":
        break
    print(line)
```

### break / continue / pass

| 关键字 | 作用 | 说明 |
|:------:|:----:|------|
| `break` | 跳出循环 | 终止整个循环 |
| `continue` | 跳过本次迭代 | 进入下一次循环 |
| `pass` | 空操作（占位） | 什么也不做，语法需要 |

```python
for i in range(10):
    if i == 3:
        pass       # 占位，后续再实现
    if i == 5:
        continue   # 跳过 5
    if i == 8:
        break      # 终止循环
    print(i)       # 0, 1, 2, 4, 6, 7
```

### match / case（Python 3.10+）

类似于其他语言的 `switch`，但功能更强（支持模式匹配）：

```python
def process_status(code):
    match code:
        case 200:
            return "OK"
        case 201 | 204:              # 多条件匹配
            return "Success"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case _:                      # 默认匹配（类似 default）
            return "Unknown"

# 解构匹配
def process_point(point):
    match point:
        case (0, 0):
            return "原点"
        case (x, 0):
            return f"X 轴上的点 x={x}"
        case (0, y):
            return f"Y 轴上的点 y={y}"
        case (x, y):
            return f"点 ({x}, {y})"
        case _:
            return "不是二维点"
```

> [!info] **match/case 是 Python 3.10 的新特性**，比传统的 `if/elif` 更适合结构化模式匹配的场景（如解析 AST、处理 API 响应）。

---

## 七、函数

### 定义与参数

```python
def greet(name, greeting="Hello"):   # 必传参数在前，默认参数在后
    return f"{greeting}, {name}!"

# 调用方式
greet("Alice")                         # 位置参数
greet(name="Bob", greeting="Hi")       # 关键字参数
greet("Charlie", greeting="Hey")       # 混合：位置 + 关键字
```

### 参数类型详解 ⭐

```python
# 1. 位置参数
def func(a, b, c): pass
func(1, 2, 3)

# 2. 默认参数（默认值只在定义时计算一次）
def func(a, b=[]):          # ⚠️ 可变对象作为默认值有坑！
    b.append(a)
    return b
print(func(1))   # [1]
print(func(2))   # [1, 2]   ← 共享了同一个列表！

# ✅ 正确做法
def func(a, b=None):
    if b is None:
        b = []
    b.append(a)
    return b

# 3. *args（任意位置参数 → 元组）
def sum_all(*args):
    return sum(args)
print(sum_all(1, 2, 3, 4))   # 10

# 4. **kwargs（任意关键字参数 → 字典）
def print_kwargs(**kwargs):
    for k, v in kwargs.items():
        print(f"{k} = {v}")
print_kwargs(name="Alice", age=25)

# 5. 仅限关键字参数（* 后面的参数必须用关键字传参）⭐
def func(a, b, *, c, d):     # c, d 只能用关键字传入
    pass
func(1, 2, c=3, d=4)         # ✅
func(1, 2, 3, 4)             # ❌ TypeError

# 6. 仅限位置参数（Python 3.8+）/ 前面的参数只能用位置传入
def func(a, b, /, c, d):     # a, b 只能用位置传入
    pass
func(1, 2, c=3, d=4)         # ✅
func(a=1, b=2, c=3, d=4)     # ❌ TypeError
```

### 返回值

```python
# 返回多个值（本质是返回元组，自动解包）
def min_max(lst):
    return min(lst), max(lst)

low, high = min_max([3, 1, 4, 1, 5])   # low=1, high=5
```

### Lambda 表达式

```python
# 匿名函数，适合简单操作
square = lambda x: x ** 2
print(square(5))               # 25

# 典型应用：排序 key 参数
students = [("Alice", 22), ("Bob", 19), ("Charlie", 21)]
students.sort(key=lambda s: s[1])   # 按年龄排序

# map/filter 中的使用
list(map(lambda x: x * 2, [1, 2, 3]))   # [2, 4, 6]
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))  # [1, 2]
```

> [!warning] Lambda 只能写单行表达式，不能包含语句（如 `return`、`if/else` 用三目）。

### LEGB 作用域规则

Python 查找变量时按照 **LEGB** 顺序搜索：

```
L — Local（局部作用域，函数内部）
E — Enclosing（外层嵌套函数的作用域）
G — Global（全局作用域，模块级别）
B — Built-in（内置作用域，如 print、len）
```

```python
x = "global"       # G

def outer():
    x = "enclosing"   # E
    def inner():
        x = "local"   # L
        print(x)
    inner()

outer()   # "local"

# global 和 nonlocal 关键字
count = 0
def increment():
    global count        # 声明要修改全局变量
    count += 1

def outer():
    x = 10
    def inner():
        nonlocal x      # 声明要修改外层作用域变量
        x += 1
    inner()
    print(x)            # 11
```

### Docstring 与函数注解

```python
def calculate_area(radius: float) -> float:
    """计算圆的面积。

    Args:
        radius: 圆的半径，必须为正数。

    Returns:
        圆的面积。

    Raises:
        ValueError: 当半径为负数时。
    """
    if radius < 0:
        raise ValueError("半径不能为负数")
    return 3.14159 * radius ** 2

# 函数注解不会强制类型检查（只有提示作用）
print(calculate_area.__annotations__)   # {'radius': <class 'float'>, 'return': <class 'float'>}
```

> [!tip] **函数设计原则**
> - 函数应**只做一件事**
> - 尽量**无副作用**（不修改传入的参数）
> - 使用**类型注解**提高可读性
> - 写 **docstring** 便于调用者理解

---

## 八、文件操作

### open 模式

| 模式 | 说明 | 文件存在 | 文件不存在 |
|:----:|------|:--------:|:----------:|
| `r` | 只读（默认） | ✅ 打开 | ❌ 报错 |
| `w` | 只写（覆盖） | ✅ 清空写入 | ✅ 创建 |
| `a` | 追加 | ✅ 追加写入 | ✅ 创建 |
| `x` | 新建写入 | ❌ 报错 | ✅ 创建 |
| `r+` | 读写 | ✅ 打开 | ❌ 报错 |
| `w+` | 读写（覆盖） | ✅ 清空写入 | ✅ 创建 |
| `a+` | 读写（追加） | ✅ 追加写入 | ✅ 创建 |
| `b` | 二进制模式 | — | — |

### 读/写方法

```python
# 打开文件（推荐使用 with ⭐）
with open("file.txt", "r", encoding="utf-8") as f:
    # 读取方式
    content = f.read()              # 读取全部内容（小文件）
    line = f.readline()             # 读取一行
    lines = f.readlines()           # 读取所有行到列表

# 逐行读取（推荐，内存友好）
with open("large_file.txt", "r", encoding="utf-8") as f:
    for line in f:                  # 逐行迭代，不会一次性加载全部
        print(line.strip())

# 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")      # 写入字符串
    f.writelines(["line1\n", "line2\n"])  # 写入多行

# 二进制文件
with open("image.jpg", "rb") as f:
    data = f.read()
```

### with 上下文管理器

```python
# with 语句自动调用 __enter__ 和 __exit__
# 即使出现异常，文件也会正确关闭

# 等价于：
f = open("file.txt", "r")
try:
    content = f.read()
finally:
    f.close()

# 一行简洁写法
with open("input.txt", "r") as f_in, open("output.txt", "w") as f_out:
    f_out.write(f_in.read().upper())
```

### os.path / pathlib

```python
import os

# os.path 常用函数
os.path.exists("file.txt")        # 文件/目录是否存在
os.path.isfile("file.txt")        # 是否是文件
os.path.isdir("dir")              # 是否是目录
os.path.join("dir", "file.txt")   # 路径拼接（自动处理分隔符）
os.path.basename("/a/b/c.txt")    # 'c.txt'
os.path.dirname("/a/b/c.txt")     # '/a/b'
os.path.splitext("file.txt")      # ('file', '.txt')
os.path.getsize("file.txt")       # 文件大小（字节）
os.listdir(".")                   # 列出目录内容
```

```python
# ⭐ pathlib（Python 3.4+ 推荐，更现代）
from pathlib import Path

p = Path("dir/subdir/file.txt")

p.exists()              # 是否存在
p.is_file()             # 是否是文件
p.is_dir()              # 是否是目录
p.name                  # 'file.txt'
p.stem                  # 'file'
p.suffix                # '.txt'
p.parent                # Path('dir/subdir')
p.parents               # 所有父目录（生成器）

# 文件操作
p.read_text(encoding="utf-8")     # 读取文本
p.write_text("hello", encoding="utf-8")  # 写入文本
p.read_bytes()                    # 读取二进制

# 目录遍历
for f in Path(".").glob("*.py"):        # 匹配当前目录
    print(f.name)
for f in Path(".").rglob("*.py"):       # 递归匹配子目录
    print(f.name)

# 路径拼接（使用 / 运算符！）
data_dir = Path("data")
file_path = data_dir / "subdir" / "file.txt"   # ✅ Pythonic
```

> [!tip] **新代码推荐使用 `pathlib` 而非 `os.path`**，`pathlib` 的 API 更一致、更面向对象。

---

## 九、异常处理

### try/except/else/finally

```python
try:
    num = int(input("请输入数字: "))
    result = 10 / num
except ValueError:
    print("输入不是有效数字")
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:           # 捕获其他所有异常
    print(f"未知错误: {e}")
else:
    print(f"结果是: {result}")   # 没有异常时执行
finally:
    print("总是执行")            # 无论是否异常都执行
```

### 常见异常类型

| 异常 | 触发场景 |
|:----:|----------|
| `TypeError` | 类型不匹配，如 `"1" + 1` |
| `ValueError` | 值不合法，如 `int("abc")` |
| `KeyError` | 字典 key 不存在 |
| `IndexError` | 列表索引越界 |
| `AttributeError` | 访问不存在的属性 |
| `ZeroDivisionError` | 除以零 |
| `FileNotFoundError` | 文件不存在 |
| `StopIteration` | 迭代器没有更多元素 |
| `ImportError` / `ModuleNotFoundError` | 导入模块失败 |
| `AssertionError` | `assert` 语句失败 |

### 自定义异常

```python
class BusinessError(Exception):
    """业务异常基类"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(BusinessError):
    def __init__(self, message="资源不存在"):
        super().__init__(message, 404)

class PermissionDeniedError(BusinessError):
    def __init__(self, message="权限不足"):
        super().__init__(message, 403)

# 使用
def get_user(user_id):
    if user_id != 1:
        raise NotFoundError(f"用户 {user_id} 不存在")
```

### raise 与 assert

```python
# raise — 主动抛出异常
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# assert — 条件断言（主要用于调试和测试）
def calculate_discount(price, rate):
    assert 0 <= rate <= 1, "折扣率必须在 0 和 1 之间"  # 条件为 False 时抛 AssertionError
    return price * rate

# ⚠️ assert 可以通过 -O 参数关闭
```

### 异常链

```python
# 保留原始异常上下文
try:
    1 / 0
except ZeroDivisionError as e:
    raise RuntimeError("计算失败") from e   # 保留原始 traceback

# 不保留
try:
    1 / 0
except ZeroDivisionError:
    raise RuntimeError("计算失败")           # 丢失原始异常

# 抑制异常链
try:
    1 / 0
except ZeroDivisionError:
    raise RuntimeError("计算失败") from None  # 不显示原始异常
```

> [!tip] **异常处理最佳实践**
> - 捕获异常**要具体**（尽量不捕获 `Exception` 基类）
> - 异常用于**异常情况**，不要用于控制流程
> - 资源操作使用 `with` 语句自动管理
> - 自定义异常继承 `Exception`（不是 `BaseException`）

---

## 十、模块和包

### import 机制

```python
# 导入方式
import math                          # 导入整个模块
from math import sqrt, pi            # 导入特定成员
from math import *                   # 导入所有（不推荐，可能污染命名空间）
import math as m                     # 起别名
from math import sqrt as square_root # 成员起别名

# 包内导入
from package.module import ClassName
from . import sibling_module          # 相对导入（同一包内）
from ..parent import parent_module   # 相对导入（父包）
```

### `if __name__ == '__main__'`

```python
# 每个 Python 文件都有 __name__ 属性
# 作为脚本直接执行时，__name__ = '__main__'
# 被导入时，__name__ = 模块名

def main():
    """程序入口"""
    print("程序启动...")
    # 主逻辑

if __name__ == "__main__":
    main()
```

> [!info] 这是一种**保护性检查**，确保代码只在作为脚本执行时运行，在被 import 时不会自动执行。

### `__init__.py`

```
mypackage/
  ├── __init__.py       # 包的初始化文件（可以为空）
  ├── module_a.py
  └── subpackage/
        ├── __init__.py
        └── module_b.py
```

```python
# __init__.py 中控制包的对外暴露接口
from .module_a import useful_function
from .subpackage.module_b import HelperClass

__all__ = ["useful_function", "HelperClass"]   # 限定 from xxx import * 的内容
```

### 相对导入 vs 绝对导入

```python
# 绝对导入（推荐）
from mypackage.module_a import func
from mypackage.subpackage.module_b import Helper

# 相对导入（仅限包内使用）
from .module_a import func           # 当前包的同级模块
from ..subpackage import helper      # 父包的子包
```

> [!warning] 相对导入只适用于**包内模块**，顶层脚本（`if __name__ == '__main__'`）不支持相对导入。

### pip 与虚拟环境

```bash
# 安装包
pip install requests                          # 最新版本
pip install requests==2.28.0                  # 指定版本
pip install "requests>=2.0,<3.0"              # 版本范围

# 使用国内镜像
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 管理包
pip list                                      # 列出已安装的包
pip show requests                             # 查看包详情
pip freeze > requirements.txt                 # 导出依赖
pip install -r requirements.txt               # 安装依赖

# 卸载包
pip uninstall requests

# ⭐ 虚拟环境（项目隔离）
python -m venv venv                           # 创建虚拟环境
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
deactivate                                    # 退出虚拟环境
```

---

## 十一、面向对象编程

### 类与实例

```python
class Dog:
    # 类变量（所有实例共享）
    species = "Canis familiaris"

    # __init__：构造方法（实例化时自动调用）
    def __init__(self, name: str, age: int):
        # 实例变量（每个实例独有）
        self.name = name
        self.age = age

    # 实例方法（第一个参数必须是 self）
    def bark(self) -> str:
        return f"{self.name} 叫了一声: 汪汪！"

    # 实例方法
    def info(self) -> str:
        return f"{self.name}，{self.age}岁"

# 实例化
dog1 = Dog("旺财", 3)
dog2 = Dog("小白", 1)

print(dog1.bark())      # "旺财 叫了一声: 汪汪！"
print(dog2.info())      # "小白，1岁"
print(dog1.species)     # "Canis familiaris"

# 实例属性的字典
print(dog1.__dict__)    # {'name': '旺财', 'age': 3}
```

### `self` 与 `__init__`

- `self` 指向**当前实例**，Python 自动传入
- `__init__` 是构造方法，在 `__new__` 之后自动调用
- 类中所有实例方法的第一个参数必须是 `self`（名称可改，但约定为 `self`）

### 魔术方法 ⭐

魔术方法（`__xxx__`）让类可以与 Python 的内置操作兼容：

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    # 字符串表示
    def __str__(self) -> str:           # print() 和 str() 调用
        return f"《{self.title}》- {self.author}"

    def __repr__(self) -> str:          # 调试表示（repr()，交互式环境）
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    # 长度
    def __len__(self) -> int:
        return self.pages

    # 比较
    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.author == other.author

    def __lt__(self, other) -> bool:
        return self.pages < other.pages

    # 可调用
    def __call__(self) -> str:
        return f"正在阅读《{self.title}》..."

    # 容器方法
    def __getitem__(self, key):
        # 支持 book["title"] 的访问方式
        return getattr(self, key)

    def __contains__(self, item):
        return item in self.title or item in self.author

# 使用
book = Book("Python编程", "Alice", 300)
print(str(book))            # 《Python编程》- Alice
print(repr(book))           # Book('Python编程', 'Alice', 300)
print(len(book))            # 300
print(book())               # "正在阅读《Python编程》..."
print(book["title"])        # "Python编程"
print("Alice" in book)      # True
```

| 魔术方法 | 说明 | 触发时机 |
|:--------:|------|:--------:|
| `__init__` | 构造方法 | 实例化时 |
| `__str__` | 用户友好字符串 | `print(obj)`、`str(obj)` |
| `__repr__` | 开发者字符串 | `repr(obj)`、交互式 |
| `__len__` | 长度 | `len(obj)` |
| `__eq__` | 相等比较 | `obj == other` |
| `__lt__` / `__gt__` | 小于 / 大于 | `obj < other` |
| `__getitem__` | 索引访问 | `obj[key]` |
| `__setitem__` | 索引赋值 | `obj[key] = val` |
| `__contains__` | 成员检测 | `x in obj` |
| `__call__` | 可调用对象 | `obj(args)` |
| `__enter__` / `__exit__` | 上下文管理器 | `with obj:` |
| `__iter__` / `__next__` | 迭代器 | `for x in obj:` |

### 继承与 MRO

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self) -> str:
        return "..."

class Cat(Animal):                  # 继承 Animal
    def speak(self) -> str:         # 重写父类方法
        return "喵喵～"

class Robot:
    def __init__(self, id):
        self.id = id

    def charge(self) -> str:
        return f"{self.id} 正在充电"

class RoboCat(Cat, Robot):          # ⭐ 多继承
    def __init__(self, name, id):
        Cat.__init__(self, name)    # 手动调用父类构造
        Robot.__init__(self, id)

rc = RoboCat("机器猫", "R-001")
print(rc.speak())         # "喵喵～"  （继承自 Cat）
print(rc.charge())        # "R-001 正在充电"  （继承自 Robot）

# MRO（方法解析顺序）— C3 线性化算法 ⭐
print(RoboCat.__mro__)
# (<class 'RoboCat'>, <class 'Cat'>, <class 'Animal'>, <class 'Robot'>, <class 'object'>)
```

> [!info] **MRO（Method Resolution Order）**
> Python 使用 **C3 线性化算法** 决定多继承下的方法搜索顺序。`类.__mro__` 可查看完整顺序。遵循"深度优先、从左到右"的原则，且保证所有父类在子类之后、`object` 在最后。

### 封装（`_` 和 `__`）

```python
class Person:
    def __init__(self, name, age, password):
        self.name = name              # 公开属性
        self._age = age               # _单下划线：约定为"受保护"（不强制）
        self.__password = password    # __双下划线：名称改写（name mangling）

    def get_password(self) -> str:    # 公开接口
        return self.__password

p = Person("Alice", 30, "secret123")

print(p.name)           # ✅ "Alice"
print(p._age)           # ⚠️ 可以访问，但约定为内部使用

# print(p.__password)   # ❌ AttributeError（名称被改写为 _Person__password）
print(p._Person__password)  # ✅ "secret123"（但强烈不推荐这样访问）
```

> [!tip] **Python 没有真正的 private**
> - `_x`：约定为"内部使用"（请尊重约定）
> - `__x`：名称改写为 `_ClassName__x`，防止子类意外覆盖
> - 真正的封装靠**约定**，而非编译器强制

### `@staticmethod` / `@classmethod` / `@property`

```python
class Date:
    def __init__(self, year, month, day):
        self._year = year
        self._month = month
        self._day = day

    # @property：将方法当作属性访问 ⭐
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value < 0:
            raise ValueError("年份不能为负")
        self._year = value

    # 只读属性（没有 setter）
    @property
    def is_leap_year(self) -> bool:
        return (self._year % 4 == 0 and self._year % 100 != 0) or (self._year % 400 == 0)

    # @classmethod：操作类本身（第一个参数是 cls）
    @classmethod
    def from_string(cls, date_str: str) -> "Date":
        """从 '2024-01-15' 格式的字符串创建 Date 实例"""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

    # @staticmethod：与类相关但不需要访问实例或类
    @staticmethod
    def is_valid_format(date_str: str) -> bool:
        parts = date_str.split("-")
        return len(parts) == 3 and all(p.isdigit() for p in parts)

# 使用
d = Date(2024, 6, 15)
print(d.year)               # 2024（像属性一样访问，不是方法）
d.year = 2025               # 通过 setter 赋值
print(d.is_leap_year)       # False

d2 = Date.from_string("2024-01-15")       # 类方法创建实例
print(Date.is_valid_format("2024-01-15"))  # True（静态方法）
```

### 抽象类（abc 模块）

```python
from abc import ABC, abstractmethod

class Shape(ABC):                # 继承 ABC（Abstract Base Class）
    @abstractmethod
    def area(self) -> float:     # 抽象方法：子类必须实现
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def description(self) -> str:   # 可以包含普通方法
        return "这是一个形状"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self) -> float:        # 必须实现
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:   # 必须实现
        return 2 * 3.14159 * self.radius

# s = Shape()      # ❌ TypeError: Can't instantiate abstract class
c = Circle(5)
print(c.area())          # 78.53975
print(c.description())   # "这是一个形状"
```

### Mixin（混入）

Mixin 是一种通过**多继承**提供可复用功能的模式，类名通常以 `Mixin` 结尾：

```python
class JSONMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)

class LoggerMixin:
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")

class User(JSONMixin, LoggerMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 25)
print(user.to_json())     # {"name": "Alice", "age": 25}
user.log("用户创建成功")  # [User] 用户创建成功
```

### `@dataclass`

Python 3.7+ 引入，自动生成 `__init__`、`__repr__`、`__eq__` 等模板代码：

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Student:
    name: str
    age: int = 18                               # 默认值
    grades: list = field(default_factory=list)   # 可变对象要用 default_factory
    active: bool = True

# 自动生成以下方法：
# __init__: Student("Alice", 20, [90, 85], True)
# __repr__: Student(name='Alice', age=20, grades=[90, 85], active=True)
# __eq__  : student1 == student2（按字段值比较）

s1 = Student("Alice", 20)
s2 = Student("Bob", 19, [88])
print(s1)                   # Student(name='Alice', age=20, grades=[], active=True)
print(s1 == Student("Alice", 20))  # True
```

> [!tip] **@dataclass 简化对比**
> - 传统写法需要手动写 `__init__`、`__repr__`、`__eq__`
> - `@dataclass` **一行注解**自动生成，且有 `frozen=True`（不可变）、`order=True`（排序）等选项

---

## 十二、列表/字典/集合推导式

### 列表推导式 ⭐

```python
# 基本
[x**2 for x in range(10)]           # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带 if 过滤
[x for x in range(20) if x % 2 == 0]  # [0, 2, 4, ..., 18]

# 带 if-else（注意三目位置）
["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']

# 嵌套循环（先外层后内层）
[(x, y) for x in range(3) for y in range(2)]
# [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

# 矩阵转置
matrix = [[1, 2, 3], [4, 5, 6]]
[[row[i] for row in matrix] for i in range(3)]
# [[1, 4], [2, 5], [3, 6]]

# 扁平化
nested = [[1, 2], [3, 4], [5, 6]]
[num for sublist in nested for num in sublist]
# [1, 2, 3, 4, 5, 6]
```

### 字典推导式

```python
# 键值互换
{val: key for key, val in {"a": 1, "b": 2}.items()}  # {1: 'a', 2: 'b'}

# 过滤
{x: x**2 for x in range(10) if x % 2 == 0}  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 数据转换
words = ["hello", "world", "python"]
{word: len(word) for word in words}   # {'hello': 5, 'world': 5, 'python': 6}
```

### 集合推导式

```python
{x**2 for x in range(10)}              # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}
{x % 3 for x in range(10)}            # {0, 1, 2}

# 去重的同时做转换
{len(w) for w in ["apple", "banana", "cherry", "avocado"]}  # {5, 6}
```

### 生成器表达式

```python
# 生成器表达式用圆括号，惰性求值（不一次性生成所有元素）
gen = (x**2 for x in range(1000000))   # 几乎不占内存
print(next(gen))   # 0
print(next(gen))   # 1

# 传给函数时，圆括号可省略
sum(x**2 for x in range(100))    # 328350
any(x > 10 for x in range(5))    # False
```

### 推导式性能对比

```python
import time

n = 10_000_000

# 列表推导式 — 生成所有元素，占用大量内存
start = time.time()
squares_list = [x**2 for x in range(n)]
print(f"列表推导式: {time.time() - start:.2f}s")   # 较快但内存占用大

# 生成器表达式 — 惰性求值，几乎不占内存
start = time.time()
squares_gen = (x**2 for x in range(n))
total = sum(squares_gen)   # 实际计算在这里
print(f"生成器表达式: {time.time() - start:.2f}s") # 总体相当，但内存友好
```

> [!tip] **选型建议**
> - 需要**全部元素多次访问** → 列表推导式
> - 只需要**逐个处理**或**一次聚合**（`sum`/`all`/`any`） → 生成器表达式
> - 数据量**非常大**（百万级以上） → 生成器表达式

---

## 十三、迭代器与生成器

### 可迭代对象 vs 迭代器 vs 生成器

| 概念 | 定义 | 示例 |
|:----:|------|:----:|
| **可迭代对象（Iterable）** | 实现了 `__iter__()` 的对象 | 列表、元组、字典、字符串、文件 |
| **迭代器（Iterator）** | 实现了 `__iter__()` + `__next__()` 的对象 | `iter([1,2,3])` |
| **生成器（Generator）** | 用 `yield` 创建的迭代器 | 生成器函数、生成器表达式 |

```python
# 关系
# Iterable → __iter__() → Iterator → __next__() → StopIteration

lst = [1, 2, 3]
it = iter(lst)           # 将可迭代对象转为迭代器

print(next(it))          # 1
print(next(it))          # 2
print(next(it))          # 3
print(next(it))          # StopIteration 异常
```

### `__iter__` / `__next__` 协议

```python
class CountDown:
    """倒计时迭代器"""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self  # 迭代器对象本身是可迭代的

    def __next__(self):
        if self.current <= 0:
            raise StopIteration  # 终止迭代
        val = self.current
        self.current -= 1
        return val

for i in CountDown(5):
    print(i, end=" ")   # 5 4 3 2 1
```

### yield 与 yield from ⭐

```python
# 生成器函数 — 包含 yield 关键字的函数
def fibonacci(n):
    """生成斐波那契数列的前 n 项"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a                # 每次 yield 都会"暂停"并返回值
        a, b = b, a + b
        count += 1

# 使用
for num in fibonacci(10):
    print(num, end=" ")        # 0 1 1 2 3 5 8 13 21 34

# 生成器可以手动驱动
gen = fibonacci(3)
print(next(gen))     # 0
print(next(gen))     # 1
print(next(gen))     # 1

# ⭐ yield from — 委托给另一个生成器（Python 3.3+）
def chain(*iterables):
    for iterable in iterables:
        yield from iterable   # 等价于 for item in iterable: yield item

print(list(chain("ABC", [1, 2, 3])))  # ['A', 'B', 'C', 1, 2, 3]
```

### 生成器性能优势

```python
# 内存对比
import sys

# 列表保存所有值
list_squares = [x**2 for x in range(1000000)]
print(sys.getsizeof(list_squares))   # ~8MB

# 生成器不保存所有值
gen_squares = (x**2 for x in range(1000000))
print(sys.getsizeof(gen_squares))    # ~200B

# 用生成器读取大文件
def read_large_file(file_path):
    """逐行读取大文件，内存友好"""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 使用
for line in read_large_file("huge_file.txt"):
    process(line)
```

> [!tip] **生成器 vs 普通函数**
> - 普通函数：`return` 一次返回所有结果，函数结束
> - 生成器：`yield` 多次返回值，每次暂停，next() 时继续
> - 生成器可以表示**无限序列**（如自然数）
> - 生成器**只能遍历一次**

---

## 十四、装饰器

### 函数装饰器（基础）

```python
# 装饰器本质：接收函数作为参数，返回新函数的"高阶函数"

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("函数执行前")
        result = func(*args, **kwargs)
        print("函数执行后")
        return result
    return wrapper

# 使用 @ 语法
@my_decorator
def say_hello(name):
    print(f"你好，{name}！")

say_hello("Alice")
# 输出：
# 函数执行前
# 你好，Alice！
# 函数执行后
```

### `functools.wraps` ⭐

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)          # 保留原函数的元信息（__name__, __doc__ 等）
    def wrapper(*args, **kwargs):
        """这是包装函数"""
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    """打招呼函数"""
    print(f"你好，{name}！")

print(say_hello.__name__)    # "say_hello"（没有 @wraps 会输出 "wrapper"）
print(say_hello.__doc__)     # "打招呼函数"（没有 @wraps 会输出 "这是包装函数"）
```

### 带参数装饰器

```python
def repeat(times: int):
    """带参数的装饰器：重复执行函数多次"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)          # 等价于 repeat(3)(greet)
def greet(name):
    print(f"你好，{name}")

greet("Alice")
# 你好，Alice
# 你好，Alice
# 你好，Alice

# 结构拆解：
# @repeat(3) → 先执行 repeat(3) 返回 decorator
#           → 再用 @decorator 修饰 greet
```

### 类装饰器

```python
class CountCalls:
    """记录函数被调用了多少次"""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 已被调用 {self.count} 次")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("Hello!")

hello()  # hello 已被调用 1 次
hello()  # hello 已被调用 2 次
```

### 多个装饰器执行顺序（洋葱模型）

```python
def decorator_a(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("A 前置")
        result = func(*args, **kwargs)
        print("A 后置")
        return result
    return wrapper

def decorator_b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("B 前置")
        result = func(*args, **kwargs)
        print("B 后置")
        return result
    return wrapper

@decorator_a
@decorator_b
def greet(name):
    print(f"你好，{name}")

greet("Alice")
# 输出顺序：
# A 前置
# B 前置
# 你好，Alice
# B 后置
# A 后置

# 等价于：decorator_a(decorator_b(greet))
# 执行：外层 decorator_a 的前置 → ...
# 从内到外执行，像洋葱一样一层层包裹
```

### 常见装饰器应用

```python
from functools import wraps
import time

# 1. 计时器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper

# 2. 缓存（LRU 缓存）
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 3. 重试
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"第 {attempt + 1} 次失败，重试中...")
                    time.sleep(delay)
        return wrapper
    return decorator
```

> [!tip] **装饰器执行时机**
> - 装饰器在**函数定义时**执行（模块加载时），不是在函数调用时
> - 被 `@wraps(func)` 修饰的 wrapper 函数会保留原函数的 `__name__`、`__doc__` 等属性

---

## 十五、闭包

### 闭包定义

**闭包**是一个函数，它记住了其创建时所在作用域中的变量，即使该作用域已经不存在：

```python
def outer(x):
    def inner(y):
        return x + y      # inner 使用了 outer 的局部变量 x
    return inner           # 返回 inner 函数（尚未执行）

add5 = outer(5)           # add5 是一个闭包，记住了 x=5
print(add5(10))           # 15（5 + 10）
print(add5(3))            # 8（5 + 3）

add10 = outer(10)         # 每个闭包实例独立记住自己的 x
print(add10(10))          # 20
print(add10(3))           # 13
```

### nonlocal 关键字

```python
def counter():
    count = 0
    def increment():
        nonlocal count     # ⚠️ 声明引用的是外层变量（不是局部变量）
        count += 1
        return count
    return increment

c1 = counter()
print(c1())   # 1
print(c1())   # 2
print(c1())   # 3

c2 = counter()   # 每个计数器独立
print(c2())   # 1
```

> [!warning] 在内部函数中**修改**外层变量必须使用 `nonlocal`。如果只读取外层变量（不修改），则不需要。

### 闭包 vs 类

```python
# 闭包方案 — 轻量，适合简单场景
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

# 类方案 — 功能更强，适合复杂场景
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
        return self.count

# 两者行为等价，闭包更简洁轻量
```

### 典型应用场景

```python
# 1. 函数工厂
def power_of(exp):
    def power(x):
        return x ** exp
    return power

square = power_of(2)
cube = power_of(3)
print(square(5))   # 25
print(cube(5))     # 125

# 2. 装饰器（装饰器底层就是闭包）
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 3. 延迟计算
def lazy_evaluate(expr):
    def evaluate():
        return eval(expr)
    return evaluate

# 4. 回调函数
def register_handler(event):
    def handler(data):
        print(f"处理事件 {event}: {data}")
    return handler
```

> [!info] **闭包 vs 装饰器**
> 闭包是**概念**（函数+环境），装饰器是闭包的**应用**。所有装饰器都是闭包，但不是所有闭包都是装饰器。

---

## 十六、上下文管理器

### `__enter__` / `__exit__` 协议

```python
class ManagedFile:
    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        """进入 with 块时自动调用"""
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file      # 返回的对象会赋给 as 后的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开 with 块时自动调用（即使有异常）"""
        self.file.close()
        # 返回 False 或 None：异常会继续传播
        # 返回 True：异常被抑制（不推荐）
        if exc_type:
            print(f"发生异常: {exc_val}")
        return False          # 让异常继续传播

# 使用
with ManagedFile("test.txt", "w") as f:
    f.write("Hello, World!")
# 自动关闭文件
```

### `contextlib.contextmanager`

用生成器语法快速创建上下文管理器（不用写类）：

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode="r"):
    """等价于上面的 ManagedFile 类"""
    try:
        file = open(filename, mode, encoding="utf-8")
        yield file                # yield 之前的代码是 __enter__，yield 的值赋给 as 变量
    finally:
        file.close()              # finally 中的代码是 __exit__

# 使用
with managed_file("test.txt", "w") as f:
    f.write("Hello!")

# 更实用的例子：计时器
@contextmanager
def timer(description="操作"):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{description} 耗时: {elapsed:.4f}s")

with timer("数据处理"):
    data = [i**2 for i in range(1000000)]
```

### `contextlib.suppress` / `redirect_stdout`

```python
from contextlib import suppress, redirect_stdout

# suppress：忽略指定异常（比 try/except pass 更干净）
with suppress(FileNotFoundError):
    os.remove("temp_file.txt")   # 文件不存在时不会抛异常

# redirect_stdout：临时重定向标准输出
import io
output = io.StringIO()
with redirect_stdout(output):
    print("这段文字被重定向到 StringIO")
    print("不会在控制台显示")
print(output.getvalue())   # 获取捕获的内容
```

> [!tip] **何时自定义上下文管理器？**
> - 需要**获取/释放资源**（文件、数据库连接、锁）
> - 需要**进入/退出状态**（计时、事务、临时修改全局设置）
> - 简单场景用 `@contextmanager`，复杂场景用类

---

## 十七、深浅拷贝

### 赋值 vs 浅拷贝 vs 深拷贝

```python
import copy

# 原始数据
original = {
    "name": "Alice",
    "scores": [90, 85, 88],
    "address": {"city": "Beijing", "zip": "100000"}
}

# 1. 赋值（=）— 仅仅是引用
assigned = original
assigned["name"] = "Bob"
print(original["name"])   # "Bob"（互相影响！）

# 2. 浅拷贝 — 创建新对象，但嵌套对象是引用
shallow = copy.copy(original)
shallow["name"] = "Charlie"           # 基本类型：独立
shallow["scores"].append(95)          # 嵌套类型：共享引用！
print(original["scores"])             # [90, 85, 88, 95]（被修改了！）
print(original["name"])               # "Bob"（不变）

# 3. 深拷贝 — 完全独立的新对象
deep = copy.deepcopy(original)
deep["scores"].append(100)
deep["address"]["city"] = "Shanghai"
print(original["scores"])             # [90, 85, 88, 95]（不变）
print(original["address"]["city"])    # "Beijing"（不变）
```

### 图解

```
原始对象 ──┬── 赋值（=）────── 同一对象（完全共享）
           │
           ├── 浅拷贝 ──────┬── 基本类型字段：独立（新对象）
           │                └── 引用类型字段：共享
           │
           └── 深拷贝 ──────┬── 基本类型字段：独立
                            └── 引用类型字段：递归独立
```

### 不可变对象的特殊性

```python
# 不可变对象（int、str、tuple）的"浅拷贝"实际上不复制
a = (1, 2, 3)
b = copy.copy(a)    # 返回的是 a 本身（因为不可变，无需复制）
print(a is b)       # True

# 即使是 deepcopy，对不可变对象也返回原引用（优化）
```

### 实现自定义拷贝

```python
from dataclasses import dataclass, field

@dataclass
class Address:
    city: str
    zip_code: str

@dataclass
class Person:
    name: str
    address: Address
    scores: list = field(default_factory=list)

p1 = Person("Alice", Address("Beijing", "100000"), [90, 85])

# 浅拷贝
import copy
p2 = copy.copy(p1)
p2.scores.append(95)
print(p1.scores)   # [90, 85, 95]（共享）

# 深拷贝
p3 = copy.deepcopy(p1)
p3.scores.append(100)
print(p1.scores)   # [90, 85, 95]（独立）
```

> [!tip] **选择指南**
> - **赋值**（`=`）：只需要另一个引用
> - **浅拷贝**：对象只有基本类型字段，或想共享嵌套对象
> - **深拷贝**：需要完全独立的对象副本（注意性能开销）

---

## 十八、类型注解

### 基础注解语法

```python
# 变量注解
name: str = "Alice"
age: int = 25
is_active: bool = True
scores: list = [90, 85, 88]

# 函数注解
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# 容器类型注解（3.9+ 简化写法）
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"math": 90, "english": 85}
coords: set[tuple[int, int]] = {(1, 2), (3, 4)}
maybe_val: int | None = None       # 联合类型（3.10+）
```

### typing 模块 ⭐

```python
from typing import Optional, Union, Any, Callable, TypeVar, Generic, Literal

# Optional：相当于 Union[T, None]
def find_user(user_id: int) -> Optional[str]:
    # 返回 str 或 None
    pass

# Union：联合类型
def process(value: Union[int, str, float]) -> str:
    return str(value)

# Any：任意类型
def log(message: Any) -> None:
    print(message)

# Callable：可调用类型
# Callable[[参数类型], 返回值类型]
def execute_handler(handler: Callable[[str, int], bool]) -> None:
    result = handler("test", 42)

# TypeVar：泛型变量
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

first([1, 2, 3])    # 返回值类型推断为 int
first(["a", "b"])   # 返回值类型推断为 str

# Generic：泛型类
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

stack = Stack[int]()
stack.push(1)
val = stack.pop()   # val 类型被推断为 int

# Literal：字面量类型（限制为特定值）
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass

set_mode("read")    # ✅
set_mode("delete")  # ❌ 类型检查器会报错
```

### 3.10+ 联合类型简化

```python
# Python 3.10+ 推荐写法
def process(value: int | str | None) -> str | None:
    return str(value) if value is not None else None

# 等价于旧写法
from typing import Union, Optional
def process_old(value: Union[int, str, None]) -> Optional[str]:
    return str(value) if value is not None else None
```

> [!note] **类型注解 ≠ 强制类型检查**
> Python 的注解只在 **静态类型检查器**（mypy、pyright）下生效，运行时 Python 不做类型检查。注解的作用是：
> - 提高代码**可读性**
> - 让 IDE 提供更好的**代码补全**和**错误提示**
> - 通过 mypy 等工具进行**静态分析**

---

## 十九、多线程与多进程

### threading.Thread

```python
import threading
import time

def task(name, delay):
    print(f"线程 {name} 开始")
    time.sleep(delay)
    print(f"线程 {name} 结束")

# 创建线程
t1 = threading.Thread(target=task, args=("A", 2))
t2 = threading.Thread(target=task, args=("B", 1))

# 启动
t1.start()
t2.start()

# 等待完成
t1.join()
t2.join()

print("所有线程结束")

# 继承 Thread
class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):                     # 重写 run 方法
        print(f"线程 {self.name} 开始")
        time.sleep(self.delay)
        print(f"线程 {self.name} 结束")

t = MyThread("C", 3)
t.start()
t.join()
```

### 线程同步

```python
import threading

# Lock — 互斥锁
lock = threading.Lock()
shared_counter = 0

def increment():
    global shared_counter
    for _ in range(100000):
        with lock:                # 自动 acquire 和 release
            shared_counter += 1

# RLock — 可重入锁（同一线程可以多次 acquire）
rlock = threading.RLock()

def recursive_lock_test(n):
    with rlock:                   # 同一线程可以重复获取
        if n > 1:
            recursive_lock_test(n - 1)

# Semaphore — 信号量（控制同时访问数量）
semaphore = threading.Semaphore(3)   # 最多 3 个线程同时访问

def limited_access(task_id):
    with semaphore:
        print(f"任务 {task_id} 正在执行")
        time.sleep(1)

# Event — 事件（线程间通知）
event = threading.Event()

def waiter():
    print("等待事件...")
    event.wait()                   # 阻塞等待事件被设置
    print("事件触发！继续执行")

def setter():
    time.sleep(2)
    print("设置事件")
    event.set()                    # 设置事件
```

### ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def heavy_compute(n):
    time.sleep(n)
    return n ** 2

# 方式 1：submit 提交
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(heavy_compute, i) for i in range(10)]

    for future in as_completed(futures):     # 按完成顺序
        print(future.result())

# 方式 2：map 批量提交（按输入顺序返回）
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(heavy_compute, range(10))
    for result in results:
        print(result)                        # 按输入顺序
```

### GIL 详解 ⭐

> [!warning] **GIL（Global Interpreter Lock）** 是 CPython 解释器的一个互斥锁，**同一时刻只允许一个线程执行 Python 字节码**。

```python
# GIL 影响场景
import threading
import time

# CPU 密集型 — GIL 导致多线程无法并行（和单线程差不多）
def cpu_intensive(n):
    count = 0
    for i in range(n):
        count += i ** 2
    return count

# IO 密集型 — GIL 在 IO 等待时释放，多线程有效
def io_intensive():
    time.sleep(1)       # 模拟 IO 等待

# CPU 密集型用多线程：几乎无加速
# CPU 密集型用多进程：多核并行，显著加速
# IO 密集型用多线程：GIL 在 IO 时释放，有效加速
```

| 对比 | IO 密集型 | CPU 密集型 |
|:----:|:---------:|:----------:|
| GIL 是否影响 | **影响小**（IO 时释放 GIL） | **影响大**（无法利用多核） |
| 推荐方案 | **多线程**（threading） | **多进程**（multiprocessing） |
| 备选方案 | asyncio（协程） | 用 C 扩展（numpy 等）绕过 GIL |

### multiprocessing.Process

```python
import multiprocessing
import time

def cpu_task(n):
    """CPU 密集型任务"""
    total = sum(i ** 2 for i in range(n))
    print(f"进程 {multiprocessing.current_process().name}: 结果 = {total}")

if __name__ == "__main__":      # ⭐ Windows 必须要有
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=cpu_task, args=(10_000_000,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
```

### ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def heavy_cpu(n):
    return sum(i ** 2 for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(heavy_cpu, 10_000_000) for _ in range(8)]
        results = [f.result() for f in futures]
    print(results)
```

### 进程间通信

```python
from multiprocessing import Queue, Pipe, Process

# Queue — 进程安全队列
def worker(q):
    q.put("来自子进程的数据")

if __name__ == "__main__":
    q = Queue()
    p = Process(target=worker, args=(q,))
    p.start()
    print(q.get())     # "来自子进程的数据"
    p.join()

# Pipe — 双向管道
def send(conn):
    conn.send("hello")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=send, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # "hello"
    p.join()
```

> [!tip] **选型总结**
>
> | 任务类型 | 推荐方案 | 原因 |
> |:--------:|:--------:|:------|
> | **IO 密集型** | `ThreadPoolExecutor` | 轻量，共享内存方便 |
> | **CPU 密集型** | `ProcessPoolExecutor` | 绕过 GIL，多核并行 |
> | **高并发 IO** | `asyncio` | 更轻量（单线程协程） |

---

## 二十、异步编程

### async / await 语法

```python
import asyncio

# 定义协程函数
async def greet(name: str, delay: float) -> str:
    await asyncio.sleep(delay)         # 模拟异步 IO 操作
    return f"你好，{name}！"

# 运行协程
async def main():
    # 方式 1：await 逐个执行
    result1 = await greet("Alice", 1)
    print(result1)

    # 方式 2：并发执行 ⭐
    results = await asyncio.gather(
        greet("Bob", 2),
        greet("Charlie", 1),
        greet("David", 3),
    )
    print(results)

# 入口
asyncio.run(main())
```

### 事件循环

```python
import asyncio

async def task(name, delay):
    print(f"{name} 开始")
    await asyncio.sleep(delay)
    print(f"{name} 结束")
    return f"{name} 的结果"

async def main():
    # 获取当前事件循环
    loop = asyncio.get_event_loop()

    # 创建 Task（自动调度）
    task1 = asyncio.create_task(task("A", 3))
    task2 = asyncio.create_task(task("B", 1))
    task3 = asyncio.create_task(task("C", 2))

    # 等待所有 Task 完成
    done, pending = await asyncio.wait(
        [task1, task2, task3],
        timeout=5.0,           # 最长等待 5 秒
        return_when=asyncio.FIRST_COMPLETED  # 或 ALL_COMPLETED
    )

    for t in done:
        print(t.result())

asyncio.run(main())
```

### aiohttp 示例

```python
import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

async def fetch_all():
    urls = [
        "https://api.github.com/users/python",
        "https://api.github.com/users/microsoft",
        "https://api.github.com/users/google",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

results = asyncio.run(fetch_all())
for r in results:
    print(r["login"], r["id"])
```

### 同步 vs 异步 vs 多线程对比

```python
import asyncio
import threading
import time
import requests

# 1. 同步 — 串行，最慢
def sync_way(urls):
    for url in urls:
        requests.get(url)

# 2. 多线程 — 并发（IO 密集型有效）
def threads_way(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(requests.get, urls)

# 3. 异步 — 单线程协程（最高并发，IO 密集型首选）
async def async_way(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        await asyncio.gather(*tasks)

# 性能对比（100 个请求）
# 同步:    ~30s
# 多线程:  ~3s
# 异步:    ~1s
```

| 对比 | 同步 | 多线程 | 异步 |
|:----:|:----:|:------:|:----:|
| **并发方式** | 串行等待 | 系统线程切换 | 协程切换（用户态） |
| **并发数** | 1 | 几百（受线程限制） | 成千上万 |
| **内存开销** | 小 | 大（每个线程 ~8MB） | 极小 |
| **适用** | 简单脚本 | IO 密集型，中等并发 | 高并发 IO |
| **代码复杂度** | 低 | 中 | 较高（需要 async 生态） |

> [!tip] **异步编程使用场景**
> - Web 服务器处理大量并发请求（FastAPI、aiohttp）
> - 爬虫抓取大量 URL
> - WebSocket 长连接
> - API 网关（大量上游调用）
> - **不适用**：CPU 密集型任务

---

## 二十一、常用内置模块深入

### os / sys

```python
import os
import sys

# os — 操作系统接口
os.getcwd()                    # 当前工作目录
os.chdir("/path")              # 改变工作目录
os.listdir(".")                # 列出目录内容
os.mkdir("new_dir")            # 创建目录
os.makedirs("a/b/c", exist_ok=True)  # 递归创建目录
os.remove("file.txt")          # 删除文件
os.rename("old", "new")        # 重命名
os.environ                     # 环境变量字典
os.environ.get("PATH")         # 获取环境变量
os.cpu_count()                 # CPU 核心数

# sys — Python 解释器相关
sys.argv                       # 命令行参数列表
sys.path                       # 模块搜索路径
sys.platform                   # 操作系统平台
sys.version                    # Python 版本
sys.exit(0)                    # 退出程序
sys.getrecursionlimit()        # 递归深度限制
sys.setrecursionlimit(3000)    # 设置递归深度
```

### json

```python
import json

data = {"name": "Alice", "age": 25, "scores": [90, 85], "active": True}

# 序列化
json_str = json.dumps(data, ensure_ascii=False, indent=2)
# {
#   "name": "Alice",
#   "age": 25,
#   "scores": [90, 85],
#   "active": true
# }

# 反序列化
parsed = json.loads(json_str)
print(parsed["name"])          # "Alice"

# 文件操作
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 自定义 JSON 序列化
from datetime import datetime

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"无法序列化 {type(obj)}")

json.dumps(datetime.now(), default=custom_serializer)
# "2025-01-15T14:30:00"
```

### datetime / time

```python
from datetime import datetime, date, time, timedelta, timezone
import time as time_module

# ⭐ datetime — 当前时间
now = datetime.now()
utc_now = datetime.now(timezone.utc)

# 构造
dt = datetime(2025, 1, 15, 14, 30, 0)
d = date(2025, 1, 15)
t = time(14, 30, 0)

# 格式化（⭐ 高频）
dt.strftime("%Y-%m-%d %H:%M:%S")       # "2025-01-15 14:30:00"
dt.strftime("%Y年%m月%d日 %A")          # "2025年01月15日 Wednesday"

# 解析
datetime.strptime("2025-01-15", "%Y-%m-%d")

# 时间运算 ⭐
tomorrow = dt + timedelta(days=1)
last_week = dt - timedelta(weeks=1)
diff = dt - datetime(2024, 1, 1)       # timedelta 对象
print(diff.days)                       # 天数差

# time 模块（Unix 时间戳）
time_module.time()                     # 当前时间戳（秒）
time_module.sleep(1)                   # 睡眠 1 秒
```

### re（正则表达式）

```python
import re

# re.match — 从开头匹配（匹配成功返回 Match 对象，否则 None）
m = re.match(r"\d+", "123abc")
print(m.group()) if m else None        # "123"

# re.search — 搜索整个字符串（返回第一个匹配）
m = re.search(r"\d+", "abc123def456")
print(m.group())                       # "123"

# re.findall — 找到所有匹配
re.findall(r"\d+", "abc123def456")     # ['123', '456']

# re.sub — 替换
re.sub(r"\d+", "NUM", "abc123def456")  # "abcNUMdefNUM"

# re.split — 分割
re.split(r"[,;.\s]+", "a,b;c d.e")    # ['a', 'b', 'c', 'd', 'e']

# 常用正则模式
# \d — 数字        \w — 字母/数字/下划线
# \s — 空白符      .  — 任意字符（除换行）
# *  — 0 次或多次  +  — 1 次或多次
# ?  — 0 次或 1 次 {n,m} — n 到 m 次

# 分组提取 ⭐
m = re.match(r"(\d{4})-(\d{2})-(\d{2})", "2025-01-15")
print(m.group(0))    # "2025-01-15"（完整匹配）
print(m.group(1))    # "2025"（年）
print(m.group(2))    # "01"（月）
print(m.group(3))    # "15"（日）

# 编译正则（多次使用建议预编译）⭐
pattern = re.compile(r"\b\w+\b")
text = "Hello, World! Python 3.12"
print(pattern.findall(text))     # ['Hello', 'World', 'Python', '3', '12']

# flag 标志
re.findall(r"^hello", "Hello\nworld", re.MULTILINE | re.IGNORECASE)
```

### collections

```python
from collections import deque, Counter, defaultdict, namedtuple

# deque — 双端队列 ⭐
d = deque([1, 2, 3])
d.append(4)               # 右侧添加
d.appendleft(0)           # 左侧添加
d.pop()                   # 右侧弹出
d.popleft()               # 左侧弹出（O(1)，比 list 快）
d.rotate(1)               # 循环右移一位

# Counter — 计数 ⭐
Counter("hello")           # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# defaultdict — 默认值字典
dd = defaultdict(list)     # 访问不存在的 key 时返回空列表
dd["key"].append(1)        # 无需先初始化

# namedtuple — 命名元组
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
```

### itertools

```python
from itertools import chain, cycle, count, groupby, permutations, combinations

# chain — 串联多个可迭代对象
list(chain([1, 2], [3, 4], "AB"))     # [1, 2, 3, 4, 'A', 'B']

# cycle — 无限循环
# for x in cycle("ABC"): print(x)  → A B C A B C ...

# count — 计数器（无限递增）
# for i in count(10, 2): print(i)  → 10 12 14 ...

# groupby — 分组（需要先排序）⭐
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))   # A [(A,1),(A,2)]  B [(B,3),(B,4)]

# permutations — 排列
list(permutations("ABC", 2))   # [('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')]

# combinations — 组合
list(combinations("ABC", 2))   # [('A','B'),('A','C'),('B','C')]
```

### functools

```python
from functools import partial, lru_cache, reduce

# partial — 偏函数（冻结部分参数）⭐
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)    # 冻结 exponent 参数
cube = partial(power, exponent=3)
print(square(5))           # 25
print(cube(5))             # 125

# lru_cache — 函数结果缓存（LRU 策略）⭐
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 查看缓存信息
print(fibonacci.cache_info())   # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)

# reduce — 归约（Python 2 是内置函数，Python 3 移到 functools）
reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])   # 120（阶乘）
```

### hashlib / base64

```python
import hashlib
import base64

# hashlib — 哈希计算 ⭐
text = "hello".encode("utf-8")     # 需要 bytes 类型

hashlib.md5(text).hexdigest()      # "5d41402abc4b2a76b9719d911017c592"
hashlib.sha1(text).hexdigest()     # "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
hashlib.sha256(text).hexdigest()   # "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

# SHA256 常用场景：密码存储（还需加盐）、文件完整性校验
# MD5 已不安全，仅适合校验而非安全场景

# base64 — 编码/解码
data = b"hello world"
encoded = base64.b64encode(data)       # b'aGVsbG8gd29ybGQ='
decoded = base64.b64decode(encoded)    # b'hello world'
```

### logging

```python
import logging

# 基本配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

logger.debug("调试信息")     # 不会输出（level 为 INFO）
logger.info("程序启动")
logger.warning("磁盘空间不足")
logger.error("文件未找到")
logger.critical("系统崩溃")

# 输出到文件
logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# 错误堆栈追踪
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("发生除零错误")   # 自动记录 traceback
```

> [!tip] **logging vs print 选型**
> - 开发调试小脚本：`print()` 即可
> - 生产环境、需要分级/持久化：使用 `logging`
> - 永远不要在生产用 `print()` 来记录日志

---

## 二十二、函数式编程工具

### map / filter / reduce

```python
numbers = [1, 2, 3, 4, 5, 6]

# map — 对每个元素应用函数
squares = list(map(lambda x: x ** 2, numbers))
# [1, 4, 9, 16, 25, 36]
# 等价于列表推导式：[x**2 for x in numbers]

# filter — 过滤元素
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6]
# 等价于列表推导式：[x for x in numbers if x % 2 == 0]

# reduce — 归约（累积计算）
from functools import reduce
total = reduce(lambda a, b: a + b, numbers)    # 21（求和）
product = reduce(lambda a, b: a * b, numbers)  # 720（求积）
max_val = reduce(lambda a, b: a if a > b else b, numbers)  # 6（求最大值）
```

> [!tip] **map/filter vs 推导式**
> 多数情况下**列表推导式**比 `map`/`filter` 更 Pythonic、更可读。`map`/`filter` 适合与已有函数配合：
> ```python
> # map 配合已有函数更简洁
> list(map(str.upper, ["hello", "world"]))   # ["HELLO", "WORLD"]
>
> # filter 配合 None 过滤假值
> list(filter(None, [0, 1, "", "hello", None]))  # [1, "hello"]
> ```

### zip / enumerate / sorted

```python
# zip — 并行迭代多个序列 ⭐
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
grades = ["A", "A", "B"]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip + dict：两个列表转为字典
result = dict(zip(names, scores))   # {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# zip 处理不等长序列（默认以最短为准）
list(zip([1, 2, 3], [10, 20]))       # [(1, 10), (2, 20)]
# Python 3.10+ 支持 strict=True（抛出异常）
# list(zip([1, 2, 3], [10, 20], strict=True))  # ValueError

# zip(*) — 解压缩 ⭐
pairs = [(1, "a"), (2, "b"), (3, "c")]
nums, letters = zip(*pairs)   # nums=(1, 2, 3), letters=('a', 'b', 'c')

# enumerate — 同时获取索引和值 ⭐
for i, name in enumerate(names, start=1):   # 从 1 开始
    print(f"{i}. {name}")

# sorted — 排序（返回新列表）
sorted([3, 1, 4, 1, 5])                              # [1, 1, 3, 4, 5]
sorted([3, 1, 4, 1, 5], reverse=True)                # [5, 4, 3, 1, 1]

# ⭐ sorted 的 key 参数 — 自定义排序规则
students = [("Alice", 22), ("Bob", 19), ("Charlie", 21)]
sorted(students, key=lambda s: s[1])                 # 按年龄排序
sorted(students, key=lambda s: s[0], reverse=True)   # 按名字降序

# 更复杂的排序
words = ["apple", "banana", "cherry", "date"]
sorted(words, key=len)                               # 按长度排序
sorted(words, key=lambda w: w[-1])                   # 按最后一个字母排序

# attrgetter — 按属性排序
from operator import itemgetter, attrgetter
sorted(students, key=itemgetter(1))                  # 等价于 lambda s: s[1]
```

### functools.reduce 的应用

```python
from functools import reduce

# 1. 求和
reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])       # 15

# 2. 求最大值
reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5, 9])  # 9

# 3. 列表扁平化
reduce(lambda a, b: a + b, [[1, 2], [3, 4], [5, 6]])   # [1, 2, 3, 4, 5, 6]

# 4. 构建字典
pairs = [("a", 1), ("b", 2), ("c", 3)]
reduce(lambda d, kv: {**d, kv[0]: kv[1]}, pairs, {})    # {'a': 1, 'b': 2, 'c': 3}
# 更简洁：dict(pairs)

# 5. 阶乘
reduce(lambda a, b: a * b, range(1, 6))    # 120（5!）
```

> [!info] **函数式编程工具选择建议**
> - 简单的转换 → **列表推导式**（最 Pythonic）
> - 与已有函数配合 → **map/filter**
> - 累积计算 → **reduce**
> - 并行迭代 → **zip**
> - 索引遍历 → **enumerate**
> - 自定义排序 → **sorted(key=...)**
> - 对于可读性，列表推导式通常优于 map/filter

---

## 二十三、测试与最佳实践

### unittest vs pytest

```python
# 被测函数
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

```python
# unittest（标准库）
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        """每个测试前执行"""
        pass

    def tearDown(self):
        """每个测试后执行"""
        pass

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

```python
# pytest（第三方，更简洁，推荐 ⭐）
# pip install pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5

import pytest
def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)

# pytest 特性：参数化测试
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

# pytest fixture
@pytest.fixture
def sample_data():
    return {"name": "Alice", "scores": [90, 85]}

def test_fixture(sample_data):
    assert sample_data["name"] == "Alice"
```

### mock

```python
from unittest.mock import Mock, patch
import requests

# Mock 对象
mock_response = Mock()
mock_response.status_code = 200
mock_response.json.return_value = {"id": 1, "name": "Alice"}

# patch — 替换真实对象 ⭐
def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

@patch("requests.get")
def test_get_user_data(mock_get):
    # 配置 mock
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    # 调用被测函数
    result = get_user_data(1)

    # 验证
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### 测试覆盖率

```bash
# 安装 coverage
pip install coverage

# 运行测试并收集覆盖率
coverage run -m pytest test_math.py
coverage run -m pytest tests/          # 运行所有测试

# 查看覆盖率报告
coverage report                         # 终端报告
coverage html                           # HTML 报告（更直观）

# 实战命令
coverage run -m pytest && coverage report -m
```

### PEP8 代码风格 ⭐

| 规则 | 说明 |
|:----:|------|
| **缩进** | 4 个空格（不要用 Tab） |
| **行宽** | 最多 79 字符（文档/注释 72 字符） |
| **空行** | 顶层定义之间 2 空行，类方法之间 1 空行 |
| **导入** | `import` 放文件顶部，按 标准库 → 第三方 → 本地 分组 |
| **空格** | 运算符两侧各 1 空格，`=` 在关键字参数时无空格 |
| **命名** | 变量/函数：`snake_case`，类：`CamelCase`，常量：`UPPER_CASE` |
| **换行** | 长行用括号隐式换行，而不是反斜杠 `\` |

```python
# ✅ 好的风格
import os
import sys
from typing import Optional

import requests
from flask import Flask

from mypackage import helper

def calculate_total(
    prices: list[float],
    discount: float = 0.0,
    tax_rate: float = 0.0,
) -> float:
    """计算总价（含折扣和税费）。

    Args:
        prices: 商品价格列表
        discount: 折扣率，默认 0
        tax_rate: 税率，默认 0
    """
    subtotal = sum(prices)
    after_discount = subtotal * (1 - discount)
    total = after_discount * (1 + tax_rate)
    return round(total, 2)

# ❌ 不好的风格
def calculateTotal(prices, discount=0.0, tax_rate=0.0):  # 驼峰命名
    s=sum(prices)                                            # 缺少空格
    d=s*(1-discount)                                          # 运算符周围无空格
    return round(d*(1+tax_rate),2)
```

### 代码组织最佳实践

```
project/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── main.py            # 程序入口
│   ├── config.py          # 配置
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/          # 业务逻辑
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/             # 工具函数
│       ├── __init__.py
│       └── helpers.py
├── tests/                 # 测试
│   ├── __init__.py
│   ├── conftest.py        # pytest 共享 fixture
│   ├── test_models/
│   └── test_services/
├── requirements.txt       # 依赖
├── pyproject.toml         # 项目配置
├── README.md              # 项目说明
└── .gitignore             # Git 忽略规则
```

```python
# 最佳实践要点

# 1. 使用类型注解
def process_data(data: list[dict]) -> dict[str, list]:
    ...

# 2. 使用异常而非返回错误码
def find_user(user_id: int) -> User:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise NotFoundError(f"用户 {user_id} 不存在")
    return user

# 3. 使用 with 管理资源
with open("file.txt") as f:
    content = f.read()

# 4. 使用 Path 处理路径
from pathlib import Path
config_path = Path("config") / "settings.json"

# 5. 函数只做一件事
# ❌ 不好的：一个函数既验证又处理又写入
# ✅ 好的：分开成 validate() → process() → save()

# 6. 列表推导式优于 map/filter
# ✅ 推导式
results = [x**2 for x in range(10) if x > 5]
# ❌ 不 Pythonic
results = list(map(lambda x: x**2, filter(lambda x: x > 5, range(10))))
```

> [!info] **Python 之禅（Zen of Python）**
> ```python
> import this
> ```
> - 优美胜于丑陋（Beautiful is better than ugly）
> - 明了胜于晦涩（Explicit is better than implicit）
> - 简洁胜于复杂（Simple is better than complex）
> - 扁平胜于嵌套（Flat is better than nested）
> - **可读性计数**（Readability counts）

---

> [!tip] **学习路径建议**
> **第一阶段**：掌握 1~11 章（基础），能够编写日常脚本
> **第二阶段**：掌握 12~18 章（进阶），理解 Python 语言特性
> **第三阶段**：掌握 19~23 章（高级），应对生产级开发
>
> 每学一章后，建议动手编写**小练习**巩固，而非只看不练。
>
> 下一篇：[[python学习篇/面向对象与设计模式篇|面向对象与设计模式篇]] →
