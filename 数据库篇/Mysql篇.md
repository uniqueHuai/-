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

## 二、MySQL 三大日志（高频重点）

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

## 三、两阶段提交（2PC — 保证 redo log 与 binlog 一致）

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

## 四、存储引擎

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

## 五、索引

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

## 六、SQL 优化

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

## 七、视图 / 存储过程 / 触发器

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

## 八、锁

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

## 九、InnoDB 引擎

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

## 十、主从复制 ⭐

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

## 十一、读写分离

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

## 十二、分库分表 ⭐

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

## 十三、MySQL 管理常用命令

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
