# MySQL 篇

## 一、事务

### 1. 什么是事务

**事务**是一组操作的集合，这些操作**要么全部成功，要么全部失败回滚**。

### 2. ACID 四大特征

| 特征 | 说明 |
|:----:|------|
| **原子性（Atomicity）** | 事务不可分割，要么全成功要么全回滚——由 **undo log** 保证 |
| **一致性（Consistency）** | 事务前后，数据库从一个一致状态到另一个一致状态 |
| **隔离性（Isolation）** | 并发事务之间互不干扰——由 **MVCC** 和 **锁** 保证 |
| **持久性（Durability）** | 一旦提交，修改永久保存——由 **redo log** 保证 |

### 3. 事务操作

```sql
-- 方式一：设置自动提交
SET @@autocommit = 0;   -- 关闭自动提交
COMMIT;                 -- 提交
ROLLBACK;               -- 回滚

-- 方式二：显式事务
START TRANSACTION;
-- SQL 操作...
COMMIT;   -- 或 ROLLBACK;
```

### 4. 并发事务问题

| 问题 | 描述 |
|:----:|------|
| **脏读** | 一个事务读取了**另一个未提交事务**修改过的数据 |
| **不可重复读** | 同一事务内，多次读取**同一数据**结果不同（其他事务修改并提交） |
| **幻读** | 同一事务内，多次执行**相同查询**，结果集行数不同（其他事务插入/删除） |

### 5. 事务隔离级别

```sql
-- 查看当前隔离级别
SELECT @@transaction_isolation;

-- 设置隔离级别
SET [SESSION | GLOBAL] TRANSACTION ISOLATION LEVEL
    {READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE};
```

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|:--------:|:---:|:---------:|:---:|
| **READ UNCOMMITTED** | ❌ 可能 | ❌ 可能 | ❌ 可能 |
| **READ COMMITTED** | ✅ 避免 | ❌ 可能 | ❌ 可能 |
| **REPEATABLE READ**（MySQL 默认） | ✅ 避免 | ✅ 避免 | ❌ 可能（InnoDB 通过 MVCC + 间隙锁避免了） |
| **SERIALIZABLE** | ✅ 避免 | ✅ 避免 | ✅ 避免 |

> [!info] MySQL InnoDB 默认隔离级别是 **REPEATABLE READ**，并通过 **MVCC**（快照读）+ **间隙锁**（当前读）解决了幻读问题。

---

## 二、数据类型与字段设计

### 1. 数值类型

```sql
-- 整数类型（从最小到最大）
TINYINT      -- 1字节  -128~127（有符号） / 0~255（无符号）
SMALLINT     -- 2字节  -32768~32767
MEDIUMINT    -- 3字节  -8388608~8388607
INT          -- 4字节  -21亿~21亿
BIGINT       -- 8字节  -2^63~2^63-1

-- 无符号示例
CREATE TABLE t (
    age TINYINT UNSIGNED,   -- 年龄不会为负，用 UNSIGNED
    status TINYINT          -- 状态可用有符号
);

-- 小数类型
FLOAT(7,4)      -- 4字节，精度低，不推荐用于精确计算
DECIMAL(10,2)   -- ⭐ 精确小数，用于金额（DECIMAL 是字符串存储，无精度损失）

-- ⭐ 金额字段设计
salary DECIMAL(10, 2)   -- 总长10位，小数2位：99999999.99
price DECIMAL(8, 2)     -- 总长8位，小数2位：999999.99
```

### 2. 字符串类型

```sql
-- ⭐ char vs varchar 选择原则
CHAR(n)         -- 定长，n≤255，速度更快，适合固定长度（手机号、身份证号）
VARCHAR(n)      -- 变长，n≤65535，省空间，适合变长字段（姓名、地址）

-- 实际区别
CHAR(10) 'abc'  → 实际存储 'abc       '（定长，空格补齐）
VARCHAR(10) 'abc' → 实际存储 'abc' + 1字节长度前缀（变长）

-- 建议
CHAR:   手机号(11)、身份证(18)、固定编码、MD5值(32)
VARCHAR: 用户名(50)、邮箱(100)、地址(200)

-- 其他字符串
TINYTEXT     -- ≤255字节
TEXT         -- ≤65535字节（2^16-1），适合文章正文
MEDIUMTEXT   -- ≤16MB（2^24-1）
LONGTEXT     -- ≤4GB（2^32-1）

-- ⭐ TEXT 与 VARCHAR 的选择
-- VARCHAR：会存入内存在排序时，适合短文本
-- TEXT：单独存储，需额外 IO，无法设默认值
-- ⚠️ 大字段不要和频繁查询的列放在同一张表（垂直拆分思路）
```

### 3. 日期时间类型

```sql
-- ⭐ 四种日期时间类型对比
DATE        -- '2026-05-17'，3字节，范围 1000-01-01 ~ 9999-12-31
TIME        -- '14:30:00'，3字节
DATETIME    -- '2026-05-17 14:30:00'，8字节，不受时区影响 ⭐ 推荐
TIMESTAMP   -- '2026-05-17 14:30:00'，4字节，受时区影响（自动转换 UTC）
YEAR        -- '2026'，1字节

-- 时间字段设计建议
CREATE TABLE t (
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,   -- 创建时间
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP     -- 更新时间
    ON UPDATE CURRENT_TIMESTAMP,
    -- ⚠️ TIMESTAMP 2038 年问题：最大到 2038-01-19，新系统用 DATETIME
);

-- 常用时间函数
NOW()        -- 当前日期时间
CURDATE()    -- 当前日期
CURTIME()    -- 当前时间
DATE(t)      -- 提取日期部分
TIME(t)      -- 提取时间部分
YEAR(t)      -- 提取年份
DATEDIFF(a, b)  -- 日期差
DATE_ADD(t, INTERVAL 1 DAY)  -- 日期计算
```

### 4. 布尔与枚举

```sql
-- MySQL 没有真正的 BOOL，用 TINYINT(1) 替代
is_active TINYINT(1) DEFAULT 1   -- 0=false, 1=true

-- 枚举类型（不建议频繁使用，修改枚举值需要 ALTER TABLE）
status ENUM('pending', 'active', 'disabled') DEFAULT 'pending'

-- 推荐用 TINYINT 替代 ENUM（扩展更方便）
status TINYINT DEFAULT 0   -- 0=pending, 1=active, 2=disabled
```

### 字段设计最佳实践

```text
✅ 推荐做法
├── 字段用 NOT NULL（NULL 会使索引、比较、统计更复杂）
├── 用明确 DEFAULT 值（避免 NULL 带来的不确定性）
├── 金额用 DECIMAL，不用 FLOAT/DOUBLE
├── 时间用 DATETIME，不用 TIMESTAMP（防 2038）
├── 大文本用 TEXT 并单独拆表
└── IP 地址用 INT UNSIGNED（INET_ATON() / INET_NTOA() 转换）

❌ 避免做法
├── 不要用 LONGTEXT 存大 JSON（考虑 MongoDB/ES）
├── 不要用 VARCHAR 存手机号（应该用 CHAR(11)）
├── 不要用 FLOAT 存金额（精度丢失）
└── 不要用 0/1 表示多状态（用 TINYINT + 常量枚举）
```

---

## 三、DDL 深入

### 1. 建表完整语法

```sql
CREATE TABLE [IF NOT EXISTS] users (
    id BIGINT UNSIGNED AUTO_INCREMENT COMMENT '主键',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    phone CHAR(11) COMMENT '手机号',
    age TINYINT UNSIGNED DEFAULT 0 COMMENT '年龄',
    salary DECIMAL(10,2) COMMENT '薪资',
    status TINYINT DEFAULT 0 COMMENT '状态：0=正常 1=冻结',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 约束
    PRIMARY KEY (id),                          -- 主键
    UNIQUE KEY uk_email (email),               -- 唯一约束
    INDEX idx_username (username),             -- 索引
    INDEX idx_age_status (age, status),        -- 联合索引
    CONSTRAINT chk_age CHECK (age >= 0 AND age < 150),  -- 检查约束 ⭐ 8.0+
    FOREIGN KEY (dept_id) REFERENCES dept(id)  -- 外键（InnoDB）
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

### 2. 修改表（ALTER TABLE）

```sql
-- 添加列
ALTER TABLE users ADD COLUMN nick_name VARCHAR(50) AFTER username;
ALTER TABLE users ADD COLUMN info JSON;  -- 8.0+ JSON 类型

-- 修改列类型
ALTER TABLE users MODIFY COLUMN username VARCHAR(100) NOT NULL;

-- 重名列
ALTER TABLE users CHANGE COLUMN nick_name nickname VARCHAR(50);

-- 删除列
ALTER TABLE users DROP COLUMN info;

-- 添加索引
ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE users ADD UNIQUE INDEX uk_phone (phone);

-- 删除索引
ALTER TABLE users DROP INDEX idx_email;

-- 重命名表
ALTER TABLE users RENAME TO members;
```

### 3. TRUNCATE vs DELETE vs DROP

```sql
-- ⭐ 三者区别（面试高频）
TRUNCATE TABLE users;  -- 清空表，DDL，不能回滚，重置自增ID，速度快
DELETE FROM users;     -- 删除所有行，DML，可回滚，不重置自增ID，速度慢
DROP TABLE users;      -- 删除表结构+数据，DDL，不能回滚

-- 带条件的 DELETE
DELETE FROM users WHERE status = 2;
```

---

## 四、DML 深入

### 1. 插入高级用法

```sql
-- 基本插入
INSERT INTO users (name, email) VALUES ('张三', 'zhangsan@test.com');

-- 批量插入（⭐ 推荐，比逐条快 N 倍）
INSERT INTO users (name, email) VALUES
    ('张三', 'z@test.com'),
    ('李四', 'l@test.com'),
    ('王五', 'w@test.com');

-- INSERT IGNORE —— 忽略重复键错误
INSERT IGNORE INTO users (id, name) VALUES (1, '张三'), (1, '李四');
-- 如果 id=1 已存在，不会报错，跳过重复行

-- ⭐ REPLACE INTO —— 有则替换，无则插入
REPLACE INTO users (id, name, email) VALUES (1, '张三', 'new@test.com');
-- 等价于：DELETE + INSERT（如果主键/唯一键冲突）

-- ⭐ INSERT ... ON DUPLICATE KEY UPDATE —— 有则更新，无则插入
INSERT INTO users (id, name, email) VALUES (1, '张三', 'new@test.com')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),      -- 如果 id 冲突，更新 name
    email = VALUES(email);    -- 更新 email

-- 业务场景：每日统计 upsert
INSERT INTO daily_stats (date, pv, uv) VALUES (CURDATE(), 1, 1)
ON DUPLICATE KEY UPDATE
    pv = pv + 1,
    uv = uv + (VALUES(uv));  -- UV 用 VALUES 取本次插入的值
```

### 2. 多表更新与删除

```sql
-- ⭐ 多表 UPDATE（基于关联条件更新）
UPDATE orders o
    JOIN users u ON o.user_id = u.id
SET o.status = 2
WHERE u.level = 'vip';

-- 多表 DELETE（删除关联数据）
DELETE u, o
FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = -1;  -- 删除已注销用户及其订单
```

---

## 五、MySQL 三大日志（高频重点）

MySQL 有三大核心日志：**redo log**、**undo log**、**binlog**，分别服务于不同的目的。

### 1. redo log（重做日志）

| 属性 | 说明 |
|:----:|------|
| **所属引擎** | InnoDB 特有 |
| **存储内容** | 数据页的**物理修改**（如"将页号 10 的偏移量 100 处的值改为 xxx"） |
| **作用** | 保证事务的**持久性**（Durability） |
| **写入时机** | 事务提交时写入（**WAL 机制**：先写日志，后写磁盘） |
| **文件** | `ib_logfile0`、`ib_logfile1`（循环写，固定大小） |

> [!tip] **WAL（Write-Ahead Logging）**：修改数据页之前，先把 redo log 写入磁盘。这样即使宕机，重启后可以通过 redo log **重放**恢复数据。

### 2. undo log（回滚日志）

| 属性 | 说明 |
|:----:|------|
| **所属引擎** | InnoDB 特有 |
| **存储内容** | 数据**修改前的值**（逻辑日志，记录逆操作） |
| **作用** | 保证事务的**原子性**（回滚）+ 实现 **MVCC** |
| **写入时机** | 事务执行过程中，每修改一行就生成一条 undo log |
| **清理** | 事务提交后，undo log 不再用于回滚，但 MVCC 可能需要旧版本，由 **purge 线程** 清理 |

### 3. binlog（二进制日志）⭐

| 属性 | 说明 |
|:----:|------|
| **所属引擎** | **MySQL Server 层**（所有引擎共享） |
| **存储内容** | SQL 语句或行变更的逻辑日志 |
| **作用** | ① **主从复制** ② **数据恢复**（全量+增量） ③ 审计 |
| **写入时机** | 事务**提交时**写入，一次事务一个完整记录 |
| **文件** | `mysql-bin.000001`、`mysql-bin.000002`……（可配置自动滚动） |

#### binlog 三种格式

| 格式 | 说明 | 优点 | 缺点 |
|:----:|------|:----:|:----:|
| **STATEMENT** | 记录原始 **SQL 语句** | 日志量小 | 非确定性函数（NOW()）可能导致主从不一致 |
| **ROW**（**5.7+ 默认**） | 记录每一行**具体变更** | 最精确，主从一致 | 日志量大 |
| **MIXED** | MySQL 自动判断混合使用 | 兼顾两者 | 复杂场景仍可能异常 |

```sql
-- 查看 binlog 格式
SHOW VARIABLES LIKE 'binlog_format';
```

#### binlog 常用操作

```sql
-- 查看 binlog 是否开启
SHOW VARIABLES LIKE 'log_bin';

-- 查看当前写入的 binlog 文件
SHOW MASTER STATUS;

-- 查看 binlog 列表
SHOW BINARY LOGS;

-- 查看 binlog 内容（ROW 格式需用 mysqlbinlog 工具）
SHOW BINLOG EVENTS IN 'mysql-bin.000001' LIMIT 10;
```

### 4. redo log vs binlog 对比

> [!info] **面试高频题：redo log 和 binlog 的区别？**

| 对比维度 | redo log | binlog |
|:--------:|:---------:|:------:|
| **所属层级** | **InnoDB 引擎层** | **MySQL Server 层** |
| **日志类型** | **物理日志**（数据页修改） | **逻辑日志**（SQL / 行变更） |
| **写入方式** | 循环写，固定大小 | 追加写，滚动增长 |
| **用途** | 崩溃恢复、保证持久性 | 主从复制、数据恢复 |
| **写入时机** | 事务执行过程中就写入 | 事务提交时才写入 |
| **记录内容** | "数据页变成什么样" | "执行了什么操作" |

---

## 六、两阶段提交（2PC — 保证 redo log 与 binlog 一致）

> [!info] **为什么需要两阶段提交？**
> redo log 和 binlog 是两个独立的日志。如果写完 redo log 后、写 binlog 前宕机，主从复制就会不一致。**两阶段提交（2PC）** 保证了它们的**逻辑一致性**。

### 执行流程

```
事务提交
   │
   ├── ① Prepare 阶段
   │      └── 写入 redo log，状态设为 prepare
   │
   ├── ② Commit 阶段
   │      ├── 写入 binlog
   │      └── 将 redo log 状态设为 commit（真正提交）
   │
   ▼
事务完成
```

**异常场景分析**：

| 宕机时刻 | redo log | binlog | 恢复后行为 |
|:---------:|:--------:|:------:|:-----------|
| ① 之前 | 未写 | 未写 | 事务丢失，正常 |
| ①→② 之间 | prepare | 未写 | **回滚事务**（binlog 未写，从库会丢数据） |
| ② 之后 | commit | 已写 | **提交事务**（两者一致） |

> [!tip] **一句话总结**：两阶段提交保证了 **redo log 和 binlog 状态一致**，无论何时宕机，恢复后两者都能对上。

---

## 七、存储引擎

### 1. 常见存储引擎对比

| 引擎 | 事务 | 锁级别 | 外键 | 特点 |
|:----:|:----:|:------:|:----:|------|
| **InnoDB**（默认） | ✅ | 行锁 | ✅ | 支持事务、高并发 |
| **MyISAM** | ❌ | 表锁 | ❌ | 读密集型，性能好 |
| **Memory** | ❌ | 表锁 | ❌ | 内存表，速度快，重启数据丢失 |
| **Archive** | ❌ | 行锁 | ❌ | 高压缩比，只支持 INSERT 和 SELECT |

### 2. InnoDB vs MyISAM 适用场景

| 场景 | 推荐引擎 |
|:----|:---------|
| 需要事务、高并发写入 | **InnoDB** |
| 大量 SELECT、读多写少 | MyISAM（或 InnoDB） |
| 需要外键约束 | **InnoDB** |
| 日志/归档数据 | Archive |

---

## 八、索引

### 1. 概念

**索引**是一种高效获取数据的**数据结构**（有序），能极大提高查询效率。

### 2. 优点与缺点

| 优点 | 缺点 |
|:----|:----|
| ✅ 提高查询速度 | ❌ 占用额外存储空间 |
| ✅ 提高排序效率 | ❌ 增删改操作性能降低 |

### 3. 索引结构

| 结构 | 支持的引擎 | 说明 |
|:----:|:----------:|------|
| **B+Tree**（主流） | InnoDB、MyISAM 等 | 内部节点存键值+指针，**叶子节点存数据 + 链表连接** |
| **Hash** | Memory | 精确匹配快，不支持范围查询 |
| **R-Tree** | MyISAM | 空间索引 |
| **Full-text** | MyISAM、InnoDB | 全文索引 |

> [!info] **B+Tree 特点**
> - 非叶子节点只存储键值和指针（不存数据），树更矮更宽
> - 叶子节点通过**链表**相连，支持范围查询
> - 查询稳定（每次都要到叶子节点，I/O 次数固定）

### 4. 索引分类

| 类型 | 说明 |
|:----:|------|
| **聚集索引（Clustered）** | 叶子节点存放**整行数据**，一张表**只有一个**（主键 / 唯一 / 默认） |
| **二级索引（Secondary）** | 叶子节点存放**主键值**，找到主键后**回表**查询数据 |

> [!info] **回表**：通过二级索引找到主键值，再通过聚集索引找到整行数据的过程。

### 5. 索引语法

```sql
-- 创建索引
CREATE [UNIQUE | FULLTEXT] INDEX index_name ON table_name (col1, col2, ...);

-- 查看索引
SHOW INDEX FROM table_name;

-- 删除索引
DROP INDEX index_name ON table_name;
```

### 6. 性能分析工具

```sql
-- ① 查看 SQL 执行频率（增删改查）
SHOW GLOBAL STATUS LIKE 'Com_______';

-- ② 慢查询日志（记录超过指定时间的 SQL）
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;   -- 超过 1 秒

-- ③ Profile 详情
SELECT @@profiling;               -- 查看 profile 开关
SET profiling = 1;                -- 开启
SHOW PROFILES;                    -- 查看每条 SQL 耗时
SHOW PROFILE FOR QUERY query_id;  -- 查看阶段耗时

-- ④ Explain 执行计划（⭐ 基础用法）
EXPLAIN SELECT * FROM user WHERE id = 1;
```

#### Explain 详解

| 字段 | 说明 | 重点关注值 |
|:----:|------|:----------:|
| **`type`** | 访问类型（性能从好到差） | `const` > `eq_ref` > `ref` > `range` > `index` > **`ALL`（全表扫描 ❌）** |
| **`key`** | 实际使用的索引 | 为 NULL 则未使用索引 |
| **`rows`** | 预估扫描行数 | **越小越好** |
| **`Extra`** | 额外信息 | `Using index`（✅ 覆盖索引）、`Using filesort`（❌ 需优化）、`Using temporary`（❌ 需优化）、`Using index condition`（ICP 优化） |

```sql
-- 示例：查看是否有 Using filesort
EXPLAIN SELECT * FROM user WHERE age > 18 ORDER BY name;
-- Extra: Using where; Using filesort  ← 需要优化！
```

### 7. 索引使用原则（索引失效场景）

| 原则 / 场景 | 说明 |
|:-----------:|------|
| **最左前缀法则** | 联合索引最左边列必须存在 |
| **范围索引** | `>` / `<` 右边列索引失效，尽量用 `>=` / `<=` |
| **索引列运算** | 对索引列做运算 → 失效 |
| **字符串不加引号** | 类型转换 → 失效 |
| **头部模糊查询** | `LIKE '%xxx'` → 失效；`LIKE 'xxx%'` → 有效 |
| **OR 条件** | 有一个列没索引 → 索引全失效 |
| **MySQL 评估** | 优化器认为全表更快 → 不走索引 |

### 8. SQL 提示

```sql
SELECT * FROM table USE INDEX(idx_name) WHERE ...;      -- 建议使用
SELECT * FROM table FORCE INDEX(idx_name) WHERE ...;     -- 强制使用
SELECT * FROM table IGNORE INDEX(idx_name) WHERE ...;    -- 忽略
```

### 9. 覆盖索引

> [!info] **覆盖索引**：查询所需的**所有字段都在索引中**，无需回表查询行数据。
> 表现：`Extra` 字段出现 `Using index`。

```sql
-- 假设有联合索引 (name, age)
-- ✅ 覆盖索引：Extra 为 Using index
SELECT name, age FROM user WHERE name = 'Alice';

-- ❌ 需要回表：Extra 为 NULL 或 Using index condition
SELECT name, age, phone FROM user WHERE name = 'Alice';
```

### 10. 前缀索引

对字符串字段的**前 N 个字符**建立索引，节省空间：

```sql
CREATE INDEX idx_email_prefix ON user(email(10));
```

### 11. 索引设计原则

1. ⭐ 数据量大 + 查询频繁的表建立索引
2. ⭐ 常用作 `WHERE` / `ORDER BY` / `GROUP BY` 的字段建立索引
3. 尽量选择**区分度高**的列（唯一索引优先）
4. 长字符串用**前缀索引**
5. 尽量使用**联合索引**（覆盖索引，避免回表）
6. **控制索引数量**，索引越多，增删改越慢
7. 索引列用 `NOT NULL` 约束，优化器决策更准确

---

## 九、SQL 优化

### 1. 批量插入

```sql
-- 批量插入（一条语句）
INSERT INTO tb VALUES (1,'a'), (2,'b'), (3,'c');

-- 手动开启事务
START TRANSACTION;
INSERT INTO tb VALUES ...;
INSERT INTO tb VALUES ...;
COMMIT;

-- 主键顺序插入（效率高于乱序插入）
```

> [!tip] **百万级数据插入**：使用 MySQL 的 `LOAD DATA LOCAL INFILE` 命令

### 2. 主键优化

| 原则 | 说明 |
|:----:|------|
| **降低长度** | 主键越短越好 |
| **顺序插入** | 使用 `AUTO_INCREMENT` 自增主键 |
| **避免 UUID** | UUID 是随机长字符串，会频繁触发**页分裂** |
| **避免修改** | 主键尽量不要 `UPDATE` |

> [!info] **页分裂与页合并**
> B+Tree 数据页满时 → 页分裂（插入新页，影响性能）；数据页空闲过多 → 页合并

### 3. GROUP BY 优化

- 对分组字段建立索引
- 满足**最左前缀法则**

### 4. LIMIT 优化

大数据分页时，越往后越慢。优化思路：**覆盖索引 + 子查询**

```sql
-- 优化前：LIMIT 1000000, 10 跳过大量行
-- 优化后：通过覆盖索引先获取主键
SELECT * FROM tb t
JOIN (SELECT id FROM tb ORDER BY id LIMIT 1000000, 10) tmp
ON t.id = tmp.id;
```

### 5. COUNT 优化

```sql
-- 效率排序（从慢到快）
COUNT(字段) < COUNT(主键 id) < COUNT(1) ≈ COUNT(*)  -- 尽量用 COUNT(*)
```

### 6. UPDATE 优化

> [!warning] **InnoDB 行锁是针对索引加的锁！**
> 如果 UPDATE 的 `WHERE` 条件没有走索引，**行锁会升级为表锁**，严重影响并发性能。

```sql
-- ✅ 走索引：行锁
UPDATE user SET name = 'Alice' WHERE id = 1;

-- ❌ 不走索引：表锁（全表扫描，锁全表）
UPDATE user SET name = 'Alice' WHERE name = 'Bob';
```

---

## 十、窗口函数 ⭐

### 1. 什么是窗口函数

**窗口函数（Window Function）** 是 MySQL 8.0+ 引入的**重量级特性**，能在不减少行数的情况下对结果集进行分组计算。普通 `GROUP BY` 会折叠行，窗口函数**不会**。

```sql
-- ⭐ GROUP BY vs 窗口函数的区别
-- GROUP BY：每部门返回一行
SELECT department, AVG(salary) FROM emp GROUP BY department;

-- 窗口函数：每行都保留，额外返回部门平均薪资
SELECT name, salary, department,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM emp;
```

### 2. 基本语法

```sql
函数() OVER (
    PARTITION BY 分组列    -- 分组（可选）
    ORDER BY 排序列        -- 排序（可选）
    ROWS/RANGE 窗口范围     -- 窗口范围（可选）
)

-- 如果不写 PARTITION BY，整个结果集作为一个窗口
-- 如果不写 ORDER BY，窗口内所有行在同一等级
```

### 3. 排名函数

```sql
-- ⭐ 三种排名函数对比（面试高频）
SELECT name, salary, department,
    ROW_NUMBER() OVER (        -- 1, 2, 3, 4（唯一且连续，无并列）
        PARTITION BY department
        ORDER BY salary DESC
    ) AS row_num,
    RANK() OVER (              -- 1, 1, 3, 4（并列跳跃）
        PARTITION BY department
        ORDER BY salary DESC
    ) AS rk,
    DENSE_RANK() OVER (        -- 1, 1, 2, 3（并列不跳跃）
        PARTITION BY department
        ORDER BY salary DESC
    ) AS dense_rk
FROM emp;

-- 示例结果：
-- name    salary  dept   row_num  rank  dense_rank
-- 张三    50000   IT      1       1       1
-- 李四    50000   IT      2       1       1   ← ROW_NUMBER 区分并列
-- 王五    45000   IT      3       3       2   ← RANK 跳过2
-- 赵六    40000   IT      4       4       3

-- ⭐ 常用场景：分组取 Top N
SELECT * FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS rn
    FROM emp
) t WHERE t.rn <= 3;  -- 每个部门薪资前三
```

### 4. 聚合窗口函数

```sql
-- ⭐ 累积求和 —— 常用于财务报表
SELECT date, amount,
    SUM(amount) OVER (ORDER BY date) AS cumulative_sum
FROM sales;

-- 移动平均 —— 常用于趋势分析
SELECT date, amount,
    AVG(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
FROM sales;

-- 分组内占比
SELECT name, department, salary,
    ROUND(salary / SUM(salary) OVER (PARTITION BY department) * 100, 1) AS pct
FROM emp;
```

### 5. 偏移函数

```sql
-- ⭐ LAG / LEAD —— 获取前/后行的值（同比环比、前后对比）
SELECT date, amount,
    LAG(amount, 1) OVER (ORDER BY date) AS prev_day,      -- 前一天
    LAG(amount, 7) OVER (ORDER BY date) AS prev_week,     -- 前7天
    LEAD(amount, 1) OVER (ORDER BY date) AS next_day,     -- 后一天
    -- 环比增长率
    ROUND((amount - LAG(amount, 1) OVER (ORDER BY date))
        / LAG(amount, 1) OVER (ORDER BY date) * 100, 2) AS growth_rate
FROM sales;

-- FIRST_VALUE / LAST_VALUE —— 窗口内首尾值
SELECT name, department, salary,
    FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_paid,
    LAST_VALUE(name) OVER (
        PARTITION BY department ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_paid       -- ⚠️ LAST_VALUE 需要指定窗口范围
FROM emp;

-- NTILE —— 分桶函数（常用于四分位、九宫格）
SELECT name, salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile  -- 按薪资分4档
FROM emp;
```

### 6. 窗口函数实战场景

```sql
-- ⭐ 场景1：用户连续签到天数（经典面试题）
WITH user_logins AS (
    SELECT user_id, login_date,
        ROW_NUMBER() OVER (
            PARTITION BY user_id ORDER BY login_date
        ) AS rn,
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (
            PARTITION BY user_id ORDER BY login_date
        ) DAY) AS group_id
    FROM login_records
)
SELECT user_id, group_id,
    MIN(login_date) AS start_date,
    MAX(login_date) AS end_date,
    COUNT(*) AS consecutive_days
FROM user_logins
GROUP BY user_id, group_id
HAVING COUNT(*) >= 3;  -- 连续签到3天以上

-- ⭐ 场景2：查询每个用户的最近一次登录
SELECT user_id, login_date
FROM (
    SELECT user_id, login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date DESC) AS rn
    FROM login_records
) t WHERE rn = 1;
```

---

## 十一、子查询与 CTE

### 1. 子查询类型

```sql
-- 标量子查询（返回单行单列）
SELECT name, salary,
    (SELECT AVG(salary) FROM emp) AS avg_salary
FROM emp;

-- 行子查询（返回单行多列）
SELECT * FROM emp
WHERE (department, salary) = (
    SELECT department, MAX(salary) FROM emp GROUP BY department LIMIT 1
);

-- 表子查询（返回多行多列）
SELECT * FROM (
    SELECT department, AVG(salary) AS avg_sal
    FROM emp GROUP BY department
) AS dept_stats
WHERE avg_sal > 10000;

-- EXISTS 子查询（⭐ 比 IN 更高效，存在即返回）
SELECT * FROM departments d
WHERE EXISTS (
    SELECT 1 FROM emp e WHERE e.dept_id = d.id
);
```

### 2. EXISTS vs IN 选择

```sql
-- ⭐ 选择原则
-- 外层表大、内层表小 → 用 IN
SELECT * FROM orders WHERE user_id IN (1, 2, 3);

-- 外层表小、内层表大 → 用 EXISTS
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- NOT EXISTS vs NOT IN（⚠️ NOT IN 遇到 NULL 会全表返回空！）
-- ❌ NOT IN 陷阱
SELECT * FROM users WHERE id NOT IN (1, 2, NULL);  -- 结果为空！

-- ✅ 推荐用 NOT EXISTS
SELECT * FROM users u
WHERE NOT EXISTS (SELECT 1 FROM blacklist b WHERE b.user_id = u.id);
```

### 3. CTE（公用表表达式）

```sql
-- ⭐ WITH —— CTE，让复杂查询更清晰
-- 等价于子查询，但可复用、可递归、更易读

-- 基本 CTE
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM emp GROUP BY department
)
SELECT e.name, e.salary, d.avg_sal,
    ROUND(e.salary - d.avg_sal) AS diff
FROM emp e
JOIN dept_avg d ON e.department = d.department;

-- 多个 CTE（用逗号分隔）
WITH
    high_salary AS (
        SELECT * FROM emp WHERE salary > 20000
    ),
    it_dept AS (
        SELECT * FROM emp WHERE department = 'IT'
    )
SELECT * FROM high_salary
UNION
SELECT * FROM it_dept;
```

### 4. 递归 CTE ⭐

```sql
-- ⭐ WITH RECURSIVE —— 树形结构查询（组织架构、评论、分类）
-- 8.0+ 支持，之前版本只能用存储过程+临时表

-- 场景：查询组织树
WITH RECURSIVE org_tree AS (
    SELECT id, name, parent_id, 1 AS level
    FROM organization
    WHERE parent_id IS NULL

    UNION ALL

    SELECT o.id, o.name, o.parent_id, t.level + 1
    FROM organization o
    JOIN org_tree t ON o.parent_id = t.id
)
SELECT * FROM org_tree ORDER BY level, id;

-- 场景：生成连续日期序列（填充报表空缺）
WITH RECURSIVE dates AS (
    SELECT '2026-01-01' AS dt
    UNION ALL
    SELECT DATE_ADD(dt, INTERVAL 1 DAY)
    FROM dates WHERE dt < '2026-12-31'
)
SELECT d.dt, IFNULL(SUM(s.amount), 0) AS daily_sales
FROM dates d
LEFT JOIN sales s ON DATE(s.created_at) = d.dt
GROUP BY d.dt
ORDER BY d.dt;
```

---

## 十二、视图 / 存储过程 / 触发器

### 1. 视图（View）

**虚拟表**，数据不真实存在，使用时动态生成：

```sql
CREATE VIEW view_name AS SELECT ...;
```

**作用**：
- **简单**：封装复杂查询
- **安全**：只暴露部分数据给用户
- **数据独立**：屏蔽底层表结构变化

### 2. 存储过程（Stored Procedure）

SQL 层面的**代码封装与重用**：

```sql
DELIMITER //
CREATE PROCEDURE proc_name(IN param INT, OUT result INT)
BEGIN
    -- 业务逻辑
    SELECT COUNT(*) INTO result FROM tb WHERE col = param;
END //
DELIMITER ;

CALL proc_name(100, @result);
SELECT @result;
```

**变量类型**：

| 类型 | 作用域 | 说明 |
|:----:|:------:|------|
| **系统变量** | 全局/会话 | MySQL 服务器配置 |
| **用户变量** | 当前会话 | `@var` |
| **局部变量** | 当前存储过程 | `DECLARE var INT` |

**关键字**：`IF`、`CASE`、`WHILE`、`REPEAT`、`LOOP`、`CURSOR`（游标）

### 3. 触发器（Trigger）

当某张表执行 INSERT / UPDATE / DELETE 时自动触发：

```sql
CREATE TRIGGER trigger_name
AFTER INSERT ON tb FOR EACH ROW
BEGIN
    -- 插入日志表
END;
```

---

## 十三、字符集与排序规则

### 1. utf8mb4 为什么是必选项

```sql
-- ⭐ 永远用 utf8mb4，不要用 utf8
-- MySQL 的 utf8 是"假 utf8"，最大只支持3字节，存不了 emoji 和生僻字
-- utf8mb4 才是真正的 4 字节 UTF-8

-- 数据库级别
CREATE DATABASE mydb
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 表级别
CREATE TABLE users (
    name VARCHAR(100)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 查看字符集
SHOW VARIABLES LIKE 'character_set_%';
SHOW VARIABLES LIKE 'collation_%';
```

### 2. 排序规则选择

```sql
-- ⭐ 三种常见 collation 对比
utf8mb4_unicode_ci          -- 基于 Unicode 标准排序，通用推荐
utf8mb4_general_ci          -- 旧版，排序略快但不准确（不推荐）
utf8mb4_0900_ai_ci          -- ⭐ MySQL 8.0+ 默认，基于 UCA 9.0，更准确

-- 区别示例
-- utf8mb4_general_ci：a=A, ß=s（简单）
-- utf8mb4_unicode_ci：a=A, ß=ss（更准确）
-- utf8mb4_0900_ai_ci：a=A, à=â（区分口音）

-- 建议：
-- MySQL 5.7：utf8mb4 + utf8mb4_unicode_ci
-- MySQL 8.0+：utf8mb4 + utf8mb4_0900_ai_ci ⭐

-- 排序规则影响排序结果
SELECT 'a' = 'A' COLLATE utf8mb4_bin;          -- 0（区分大小写）
SELECT 'a' = 'A' COLLATE utf8mb4_unicode_ci;   -- 1（不区分大小写）
```

### 3. 字符集相关陷阱

```sql
-- ⚠️ 连接字符集导致乱码
-- 设置客户端/连接/结果字符集一致
SET NAMES utf8mb4;

-- 查看当前连接字符集
SHOW VARIABLES LIKE 'character_set_client';
SHOW VARIABLES LIKE 'character_set_connection';
SHOW VARIABLES LIKE 'character_set_results';

-- 推荐：在连接池或 ORM 配置中指定
-- JDBC: jdbc:mysql://host/db?useUnicode=true&characterEncoding=utf8mb4
-- Spring: spring.datasource.url=jdbc:mysql://host/db?useUnicode=true&characterEncoding=utf8mb4

-- ⚠️ 修改表字符集注意事项
-- 只改 DEFAULT CHARSET 不影响已有列
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4;  -- 重建所有列
ALTER TABLE users DEFAULT CHARACTER SET utf8mb4;      -- 只改默认，不影响已有列
```

---

## 十四、锁

### 1. 全局锁

```sql
FLUSH TABLES WITH READ LOCK;  -- 加全局锁（只读）
```

> 加了全局锁后，其他所有 DDL / DML 操作阻塞，保证数据备份的一致性。**生产环境推荐使用 `mysqldump --single-transaction`**（InnoDB 可用事务快照，无需加锁）。

### 2. 表级锁

| 类型 | 说明 |
|:----:|------|
| **表锁** | 读锁不阻塞读，阻塞写；写锁既阻塞读也阻塞写 |
| **元数据锁（MDL）** | 防止 DDL 和 DML 冲突（自动管理） |
| **意向锁** | 表级锁和行级锁的**协调机制**，快速判断表中是否有行锁 |

### 3. 行级锁（InnoDB）

| 类型 | 说明 |
|:----:|------|
| **行锁（Record Lock）** | 锁定**单条记录**，防止其他事务 UPDATE / DELETE |
| **间隙锁（Gap Lock）** | 锁定**索引记录之间的间隙**，防止 INSERT 产生幻读 |
| **临键锁（Next-Key Lock）** | **行锁 + 间隙锁**，InnoDB 默认行锁策略，解决幻读 |

> [!warning] **间隙锁只在 REPEATABLE READ 级别生效**。READ COMMITTED 级别下间隙锁会失效，这也是 RC 级别有幻读的原因之一。

---

## 十五、InnoDB 引擎

### 1. 逻辑存储结构

```
表空间（Tablespace） → 段（Segment） → 区（Extent，1MB） → 页（Page，16KB） → 行（Row）
```

### 2. 内存结构

| 组件 | 说明 |
|:----:|------|
| **Buffer Pool** | 缓冲池，缓存数据页和索引页（分为 free / clean / dirty page） |
| **Change Buffer** | 变更缓冲，合并**随机**二级索引写入，减少磁盘 IO |
| **Adaptive Hash Index** | 自适应哈希索引，对热数据自动建立 Hash 索引 |
| **Log Buffer** | 日志缓冲区，保存要写入磁盘的日志 |

### 3. MVCC（多版本并发控制）

> [!info] MVCC 是一种**无锁并发控制**机制，通过保留数据的**多个版本**实现：
> - 读操作**不等待**写操作
> - 写操作**不阻塞**读操作

#### 核心组成

| 组件 | 说明 |
|:----:|------|
| **隐藏字段** | 每行有 `DB_TRX_ID`（最近修改事务 ID）、`DB_ROLL_PTR`（回滚指针指向 undo log） |
| **undo log 版本链** | 通过回滚指针串联旧版本，形成版本链 |
| **ReadView** | 事务执行快照读时生成，决定当前事务能看到哪些版本 |

#### ReadView 可见性规则

```
creator_trx_id：当前事务 ID
m_ids：活跃事务 ID 列表
min_trx_id：m_ids 最小值
max_trx_id：下一个要分配的事务 ID

判断规则：
① 版本 trx_id = creator_trx_id → 自己修改的，可见 ✅
② 版本 trx_id < min_trx_id → 已提交事务，可见 ✅
③ 版本 trx_id ≥ max_trx_id → 未来事务，不可见 ❌
④ min_trx_id ≤ trx_id ≤ max_trx_id → 在 m_ids 中则未提交，不可见 ❌；不在则已提交，可见 ✅
```

> [!tip] **RC  vs  RR 下 ReadView 的区别**
> - **READ COMMITTED**：每执行一次 SELECT **生成一个新的 ReadView**
> - **REPEATABLE READ**：事务中**第一次 SELECT 生成 ReadView**，后续复用（解决了不可重复读）

---

## 十六、主从复制 ⭐

### 1. 复制原理

```
主库（Master）                          从库（Slave）
   │                                       │
   │ ① 写入 binlog                        │
   │─────────────────────────              │
   │                                       │ ② 读取主库 binlog
   │         ┌─────────────────────────────│─── 写入 relay log（中继日志）
   │         │                             │
   │         │                             │ ③ 回放 relay log
   │         │                             │    → 应用到从库
   ▼         ▼                             ▼
```

| 步骤 | 说明 | 线程 |
|:----:|------|:----:|
| **① 主库写入 binlog** | 事务提交时写入 binlog | 主库 |
| **② 从库 I/O 线程拉取** | 从库连接主库，读取 binlog 写入 relay log | 从库 I/O 线程 |
| **③ 从库 SQL 线程回放** | 读取 relay log 并在从库执行 | 从库 SQL 线程 |

```sql
-- 查看从库复制状态
SHOW SLAVE STATUS\G
-- 重点关注：
-- Slave_IO_Running: Yes      → I/O 线程正常
-- Slave_SQL_Running: Yes     → SQL 线程正常
-- Seconds_Behind_Master: 0   → 主从延迟（秒）
```

### 2. 复制模式

| 模式 | 说明 | 数据安全性 | 性能影响 |
|:----:|------|:---------:|:--------:|
| **异步复制**（默认） | 主库提交后立即返回，不等待从库确认 | ❌ 可能丢数据 | 最快 |
| **半同步复制** | 主库等待**至少一个从库**确认收到 binlog 后才提交 | ✅ 较高 | 中等 |
| **全同步复制** | 主库等待所有从库确认后才提交 | ✅ 最高 | 最慢 |

### 3. 主从延迟的原因与解决方案

**原因**：
- 从库 I/O 线程慢（网络延迟）
- **从库 SQL 线程单线程回放**（主库并发写入高时，从库回放跟不上）
- 从库硬件配置低于主库

**解决方案**：
- ⭐ 升级到 MySQL 5.7+ 的**并行复制**（slave_parallel_workers）
- 从库硬件不低于主库
- 避免从库上执行长查询
- 监控 `Seconds_Behind_Master`

---

## 十七、读写分离

### 基本架构

```
应用层
   │
   ├── 写操作 → 主库（Master）
   │               ↓
   │          binlog 同步
   │               ↓
   └── 读操作 → 从库（Slave 1 / Slave 2 / ...）
```

### 实现方式

| 方式 | 说明 |
|:----:|------|
| **Spring ShardingSphere** | 配置读写分离规则，自动路由 |
| **MyCat** | 数据库中间件 |
| **应用层硬编码** | 配置多个数据源，手动切换 |

> [!warning] **读写分离带来的问题**
> - **主从延迟**：刚写入的数据在从库可能读不到
> - **解决方案**：写后强制读主库 / 等待从库同步确认

---

## 十八、分库分表 ⭐

### 1. 为什么要分库分表？

| 问题 | 说明 | 解决方案 |
|:----|:-----|:---------|
| **单表数据量过大** | 千万级→亿级，索引深度增加，查询变慢 | **分表** |
| **单库并发过高** | 连接数不够用，QPS 瓶颈 | **分库** |

### 2. 拆分方式

```
垂直拆分（按业务拆）
   垂直分库：将不同业务表拆分到不同数据库
   垂直分表：将大表的大字段拆到另一张表（冷热分离）

水平拆分（按行拆）
   水平分表：将一张表的数据按规则分散到多张结构相同的表
   水平分库：将数据分散到多个数据库实例
```

### 3. 分片策略

| 策略 | 说明 | 优缺点 |
|:----:|------|:------:|
| **Hash 取模** | `id % N` 路由到对应库/表 | 简单，但**扩容困难** |
| **范围分片** | 按 ID 范围（1~1000万 → 库1，1000万~2000万 → 库2） | 扩容方便，但**热点集中** |
| **一致性 Hash** | Hash 环 + 虚拟节点 | **扩容友好**，迁移数据少 |

### 4. 分库分表带来的问题

| 问题 | 说明 | 解决方案 |
|:----|:-----|:---------|
| **跨库 JOIN** | 数据分散在不同库，无法直接 JOIN | 应用层组装 / 宽表冗余 |
| **分布式事务** | 跨库操作需要一致性 | Seata / TCC / 可靠消息 |
| **全局主键** | 自增 ID 会重复 | **雪花算法（Snowflake）** / Redis 发号器 / UUID |
| **跨库分页排序** | ORDER BY + LIMIT 跨库后结果不准 | 中间件归并排序 |
| **数据迁移** | 扩容时需要重新分布数据 | 一致性 Hash 减少迁移量 |

---

## 十九、用户与权限管理

### 1. 用户管理

```sql
-- 创建用户
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password123';
CREATE USER 'app_user'@'%' IDENTIFIED BY 'password123';  -- 任意主机

-- 删除用户
DROP USER 'app_user'@'localhost';

-- 修改密码
ALTER USER 'app_user'@'localhost' IDENTIFIED BY 'new_password';

-- 查看用户
SELECT user, host, account_locked, password_expired
FROM mysql.user;

-- 锁定/解锁用户
ALTER USER 'app_user'@'localhost' ACCOUNT LOCK;
ALTER USER 'app_user'@'localhost' ACCOUNT UNLOCK;
```

### 2. 权限管理

```sql
-- ⭐ MySQL 权限层级（从宽到窄）
-- 全局权限（*.*），数据库权限（db.*），表权限（db.table），列权限

-- 授予权限
GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'localhost';
GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'localhost';
GRANT SELECT (name, email) ON mydb.users TO 'readonly'@'%';  -- 列级权限

-- 查看权限
SHOW GRANTS FOR 'app_user'@'localhost';
SHOW GRANTS FOR CURRENT_USER();

-- 回收权限
REVOKE DELETE ON mydb.* FROM 'app_user'@'localhost';
REVOKE ALL PRIVILEGES ON mydb.* FROM 'app_user'@'localhost';

-- 刷新权限（使修改立即生效）
FLUSH PRIVILEGES;
```

### 3. 权限最佳实践

```text
✅ 权限设计原则
├── 最小权限原则：只给必要的权限
├── 应用账号区分：读写账号 / 只读账号 / 管理账号
├── 限制登录主机：应用服务器用内网 IP，不用 %
├── 定期审查权限：清理闲置账号和过期权限
└── 不要用 root 连接应用

推荐的应用账号配置
├── 读写账号：SELECT, INSERT, UPDATE, DELETE（业务库）
├── 只读账号：SELECT（报表/查询）
├── 管理账号：ALL PRIVILEGES（DBA 使用）
└── 备份账号：SELECT, RELOAD, LOCK TABLES, REPLICATION CLIENT
```

---

## 二十、SQL_MODE

### 1. 什么是 SQL_MODE

```sql
-- SQL_MODE 定义了 MySQL 的 SQL 语法和行为规则
-- 不同版本的默认值不同，了解它避免"开发环境正常，生产环境报错"

-- 查看当前 SQL_MODE
SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;

-- 设置 SQL_MODE
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
SET SESSION sql_mode = 'STRICT_TRANS_TABLES';
```

### 2. 常用 SQL_MODE 说明

| 模式 | 说明 | 建议 |
|:----|:-----|:----|
| **STRICT_TRANS_TABLES** | ⭐ 事务表启用严格模式，数据溢出/非法值报错而非警告 | ✅ 必开 |
| **NO_ENGINE_SUBSTITUTION** | 指定的存储引擎不可用时报错，不自动替换 | ✅ 必开 |
| **ONLY_FULL_GROUP_BY** | ⭐ GROUP BY 查询中，SELECT 列必须在 GROUP BY 中或聚合函数内 | ✅ 推荐开 |
| **NO_ZERO_DATE** | 不允许 '0000-00-00' 日期 | ✅ 推荐开 |
| **NO_ZERO_IN_DATE** | 不允许日期中有零值（如 '2026-00-01'） | ✅ 推荐开 |
| **PIPES_AS_CONCAT** | 将 `||` 视为字符串连接符而非 OR（像 SQL Server） | ❌ 默认不开 |
| **ANSI_QUOTES** | 将双引号视为标识符引用符而非字符串 | ❌ 看团队规范 |
| **STRICT_ALL_TABLES** | 所有表启用严格模式（包括非事务表） | ✅ 推荐 |

```sql
-- ⚠️ ONLY_FULL_GROUP_BY 陷阱
-- 8.0 默认开启，5.7 默认开启，5.6 默认不开启

-- ❌ 报错（name 不在 GROUP BY 中且非聚合）
SELECT department, name, AVG(salary)
FROM emp GROUP BY department;

-- ✅ 正确写法
SELECT department, AVG(salary)
FROM emp GROUP BY department;

-- ✅ 或用 ANY_VALUE() 绕过（确认值唯一时）
SELECT department, ANY_VALUE(name), AVG(salary)
FROM emp GROUP BY department;
```

### 推荐配置

```ini
# my.cnf 推荐配置（MySQL 8.0+）
[mysqld]
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
```

---

## 二十一、JSON 数据类型

### 1. JSON 类型优势

```sql
-- ⭐ MySQL 8.0+ 原生 JSON 类型
-- 优势：自动校验 JSON 合法性、可索引、高效部分更新

CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200),
    attributes JSON,       -- ⭐ 灵活属性，避免频繁 ALTER TABLE
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 插入 JSON 数据
INSERT INTO products VALUES (
    1,
    '笔记本电脑',
    '{"brand": "Lenovo", "specs": {"cpu": "i7", "ram": "16GB", "disk": "512GB"}, "color": "silver"}'
);
```

### 2. JSON 查询与操作

```sql
-- JSON 查询函数
SELECT
    id,
    name,
    JSON_EXTRACT(attributes, '$.brand') AS brand,        -- "Lenovo"
    attributes->'$.brand' AS brand,                       -- ⭐ 简写
    attributes->>'$.brand' AS brand_str,                  -- ⭐ 去引号
    attributes->'$.specs.cpu' AS cpu,
    JSON_UNQUOTE(JSON_EXTRACT(attributes, '$.color')) AS color
FROM products;

-- JSON 条件查询
SELECT * FROM products
WHERE attributes->>'$.brand' = 'Lenovo';

-- JSON 数组查询
SELECT * FROM products
WHERE JSON_CONTAINS(attributes->'$.tags', '"新品"');

-- JSON 索引（⭐ 虚拟列 + 索引）
ALTER TABLE products ADD COLUMN brand VARCHAR(50)
    GENERATED ALWAYS AS (attributes->>'$.brand') STORED;

CREATE INDEX idx_brand ON products(brand);

-- 现在可以直接按 brand 查询，走索引
SELECT * FROM products WHERE brand = 'Lenovo';

-- JSON 更新
UPDATE products
SET attributes = JSON_SET(attributes, '$.price', 9999)
WHERE id = 1;

-- JSON 追加
UPDATE products
SET attributes = JSON_ARRAY_APPEND(attributes, '$.tags', '热销')
WHERE id = 1;

-- JSON 删除键
UPDATE products
SET attributes = JSON_REMOVE(attributes, '$.color')
WHERE id = 1;
```

### 3. JSON 使用场景

```text
✅ 适合用 JSON
├── 字段属性不固定（商品属性、配置项）
├── 第三方 API 响应（直接存原始 JSON）
├── 日志/事件数据（schema-on-read）
├── 避免频繁 ALTER TABLE（新属性直接加在 JSON 里）
└── 简单文档存储（不需要 MongoDB 复杂度时）

❌ 不适合用 JSON
├── 需要 JOIN 关联的数据（JSON 字段不能直接 JOIN）
├── 需要频繁更新单个属性的高频场景（JSON_SET 性能不如普通列）
├── 需要排序、聚合的字段（JSON 提取列排序不如普通列）
└── 数据量极大的场景（JSON 占用空间比普通列大）
```

---

## 二十二、备份与恢复

### 1. mysqldump 逻辑备份

```bash
# ⭐ 常用备份命令

# 备份单库
mysqldump -u root -p mydb > mydb_backup.sql

# 备份多库
mysqldump -u root -p --databases db1 db2 > dbs_backup.sql

# 备份所有库
mysqldump -u root -p --all-databases > all_backup.sql

# ⭐ 只备份表结构（不备份数据）
mysqldump -u root -p --no-data mydb > mydb_schema.sql

# ⭐ 只备份数据（不备份结构）
mysqldump -u root -p --no-create-info mydb > mydb_data.sql

# ⭐ InnoDB 热备份（不锁表）
mysqldump -u root -p --single-transaction mydb > mydb_hot.sql
# --single-transaction：利用 MVCC 快照，不阻塞读写 ⭐ 推荐

# 指定表
mysqldump -u root -p mydb users orders > tables_backup.sql

# 压缩备份
mysqldump -u root -p mydb | gzip > mydb_backup.sql.gz

# 恢复
mysql -u root -p mydb < mydb_backup.sql
# 从压缩包恢复
gunzip -c mydb_backup.sql.gz | mysql -u root -p mydb

# 远程备份
mysqldump -h host -u root -p mydb > remote_backup.sql
```

### 2. 物理备份

```bash
# ⭐ 物理备份 vs 逻辑备份
# 逻辑备份（mysqldump）：SQL 语句，可跨版本，速度慢，体积大
# 物理备份（直接拷贝文件）：速度快，体积小，需同版本

# 使用 XtraBackup（Percona 官方工具，推荐生产环境）
# 全量备份
xtrabackup --backup --target-dir=/backup/mysql/full/

# 增量备份（基于 LSN）
xtrabackup --backup --target-dir=/backup/mysql/inc1/ \
    --incremental-basedir=/backup/mysql/full/

# 准备恢复
xtrabackup --prepare --target-dir=/backup/mysql/full/

# 恢复
xtrabackup --copy-back --target-dir=/backup/mysql/full/
```

### 3. binlog 增量恢复

```bash
# ⭐ 基于 binlog 的时间点恢复

# 查看 binlog 列表
mysql -e "SHOW BINARY LOGS;"

# 将 binlog 转为可读的 SQL
mysqlbinlog mysql-bin.000001 > binlog_001.sql

# 按时间点恢复（比如误删数据后恢复到删除前的状态）
mysqlbinlog --stop-datetime="2026-05-17 14:00:00" \
    mysql-bin.000001 | mysql -u root -p

# 按位置恢复
mysqlbinlog --stop-position=12345 mysql-bin.000001 | mysql -u root -p

# 完整恢复流程：全量备份 + binlog 增量
# 1. 恢复最近的 mysqldump 全量备份
mysql -u root -p mydb < mydb_backup.sql

# 2. 应用 binlog 增量（从备份时间点到故障前）
mysqlbinlog --start-datetime="2026-05-16 03:00:00" \
    --stop-datetime="2026-05-17 13:59:00" \
    mysql-bin.000001 mysql-bin.000002 | mysql -u root -p mydb
```

### 4. 备份策略

```text
企业级备份策略
═══════════════════════════════════════

日常备份
├── 每天凌晨：mysqldump --single-transaction 全量备份
├── 保留最近 7 天全量
└── binlog 实时同步到独立存储

周备份
├── 每周日：XtraBackup 物理全量备份
└── 保留最近 4 周

月备份
├── 每月1日：全量备份归档
└── 保留最近 12 个月

恢复演练
├── 每季度：从备份搭建从库，验证数据完整性
└── 每年：完整容灾演练

3-2-1 原则
├── 至少 3 份副本
├── 至少 2 种不同介质
└── 至少 1 份异地存储
```

---

## 二十三、MySQL 管理常用命令

```sql
-- 查看数据库版本
SELECT VERSION();

-- 查看当前连接
SHOW PROCESSLIST;

-- 查看字符集
SHOW VARIABLES LIKE 'character%';

-- 查看表状态
SHOW TABLE STATUS;

-- 分析表
ANALYZE TABLE table_name;

-- 检查表
CHECK TABLE table_name;

-- 优化表（回收碎片空间）
OPTIMIZE TABLE table_name;

-- 查看正在运行的事务
SELECT * FROM information_schema.INNODB_TRX\G;

-- 查看锁
SELECT * FROM performance_schema.data_locks;
```
