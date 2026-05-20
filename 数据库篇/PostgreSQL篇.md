# PostgreSQL 篇

## 一、PostgreSQL 概述

**PostgreSQL** 是一个**对象关系型数据库管理系统**（ORDBMS），以 SQL 标准兼容性、扩展性和丰富的特性著称。

### PostgreSQL vs MySQL

| 对比维度 | PostgreSQL | MySQL |
|:--------:|:-----------|:------|
| **类型** | 对象关系型（支持继承、自定义类型） | 关系型 |
| **SQL 标准兼容性** | ✅ **高度兼容**（最接近标准 SQL） | ⚠️ 部分兼容 |
| **JSON 支持** | **JSONB** — 二进制 JSON，可索引 | JSON — 仅文本存储 |
| **索引类型** | **8 种**（B-Tree, Hash, GiST, GIN, SP-GiST, BRIN, 部分, 表达式） | B+Tree, Hash, Full-text |
| **全文搜索** | ✅ **内建**（tsvector/tsquery） | ❌ 需外部引擎 |
| **窗口函数** | ✅ 完整支持 | ✅ 8.0+ 支持 |
| **CTE 递归** | ✅ `WITH RECURSIVE` | ⚠️ 8.0+ 支持 |
| **复制** | **流复制**（同步/异步）+ **逻辑复制** | 异步主从 / Group Replication |
| **MVCC 实现** | **元组版本链**（无 undo log） | undo log 实现 |
| **扩展性** | ✅ **Extensions**（PostGIS 等） | ⚠️ 有限 |

> [!tip] **选型建议**
> - 需要**复杂查询、数据分析、JSON、GIS** → PostgreSQL
> - 需要**简单的读写分离、生态成熟** → MySQL
> - **Oracle 迁移** → PostgreSQL（语法兼容性更好）

---

## 二、数据类型与扩展字段

PostgreSQL 提供了远超常规关系数据库的丰富数据类型。

### 1. JSONB（二进制 JSON）

> [!info] **JSON vs JSONB**
> - `JSON`：文本存储，保留完整格式（包括空格、重复键）
> - `JSONB`：**二进制**存储，自动去重键，**支持 GIN 索引**，处理更快

```sql
-- 创建 JSONB 字段
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    info JSONB
);

-- 插入数据
INSERT INTO orders (info) VALUES
    ('{"customer": "Alice", "items": [{"product": "A", "qty": 2}], "total": 100}'),
    ('{"customer": "Bob", "items": [{"product": "B", "qty": 1}], "total": 50}');

-- JSONB 高级查询
SELECT info->>'customer' AS customer,
       info->'items'->0->>'product' AS first_product
FROM orders;

-- 条件查询
SELECT * FROM orders WHERE info @> '{"customer": "Alice"}';

-- 创建 GIN 索引加速 JSONB 查询
CREATE INDEX idx_orders_info ON orders USING GIN (info);
```

### 2. 数组类型

```sql
-- 定义数组字段
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name TEXT,
    tags TEXT[],               -- 字符串数组
    scores INTEGER[]           -- 整数数组
);

-- 插入数组
INSERT INTO students (name, tags, scores)
VALUES ('Alice', '{"优秀","进步"}', '{95, 88, 92}');

-- 数组查询
SELECT * FROM students WHERE '优秀' = ANY(tags);      -- 包含某个元素
SELECT * FROM students WHERE tags @> '{"进步"}';      -- 包含数组（使用 GIN 索引）
SELECT name, scores[1] AS first_score FROM students;   -- 按索引访问
SELECT unnest(scores) FROM students;                   -- 数组展开为行
```

### 3. 网络类型

> PostgreSQL 内建支持 IP 地址的存储、比较和范围查询。

```sql
CREATE TABLE access_log (
    id SERIAL PRIMARY KEY,
    ip INET,                   -- IPv4 或 IPv6 地址
    mac MACADDR,               -- MAC 地址
    subnet CIDR                -- CIDR 网段
);

INSERT INTO access_log (ip, mac, subnet)
VALUES ('192.168.1.100', '08:00:2b:01:02:03', '192.168.1.0/24');

SELECT * FROM access_log WHERE ip << '192.168.1.0/24';  -- IP 在子网内
```

### 4. UUID

```sql
-- 启用 uuid 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT
);

INSERT INTO users (name) VALUES ('Alice');
SELECT * FROM users;
```

### 5. 范围类型

```sql
CREATE TABLE reservations (
    room_id INT,
    period TSRANGE,            -- 时间戳范围
    price_range INT4RANGE      -- 整数价格范围
);

-- 查询范围重叠
SELECT * FROM reservations
WHERE period && '[2025-01-01 14:00, 2025-01-01 16:00)'::tsrange;
```

---

## 三、索引（PostgreSQL 独有优势）

### 索引类型全景

| 索引类型 | 适用场景 | 示例 |
|:--------:|----------|:----:|
| **B-Tree**（默认） | 通用，等值/范围/排序 | `CREATE INDEX ... ON ...` |
| **Hash** | 等值查询（=） |  |
| **GiST** | 几何/全文搜索/范围重叠 |  |
| **GIN** | **JSONB / 数组 / 全文搜索** | `USING GIN` |
| **SP-GiST** | 空间分区/聚类数据 |  |
| **BRIN** | **超大表**、顺序数据 | `USING BRIN` |
| **部分索引** | 只索引部分数据 | `WHERE ...` |
| **表达式索引** | 对函数结果索引 | `ON lower(email)` |

### GIN 索引（重点）

适合**复合值类型**的索引：JSONB、数组、全文搜索

```sql
-- JSONB 索引
CREATE INDEX idx_orders_info ON orders USING GIN (info);

-- 数组索引
CREATE INDEX idx_students_tags ON students USING GIN (tags);
```

### BRIN 索引（超大表优化）

> [!tip] BRIN 适用于**时序数据、日志表**等按顺序插入的超大表，占用的空间极小。

```sql
-- 对时间序列数据使用 BRIN 索引
CREATE INDEX idx_log_created ON access_log USING BRIN (created_at)
WITH (pages_per_range = 32);
```

| 对比 | B-Tree | BRIN |
|:----:|:------:|:----:|
| **占用空间** | 大（索引整个表） | **极小**（索引数据块） |
| **适合场景** | 频繁查询的任意字段 | **时序/日志/顺序数据** |
| **查询速度** | 快 | 稍慢（但远快于全表扫描） |

### 部分索引

```sql
-- 只索引活跃用户（节省空间）
CREATE INDEX idx_active_users ON users (email) WHERE status = 'ACTIVE';
```

### 表达式索引

```sql
-- 忽略大小写的唯一约束
CREATE UNIQUE INDEX idx_lower_email ON users (lower(email));
```

### 覆盖索引（Index-Only Scan）

```sql
-- 创建包含额外字段的索引，避免回表
CREATE INDEX idx_users_email_cover ON users (email) INCLUDE (name, avatar);
```

---

## 四、高级查询特性

### 1. CTE 与递归 CTE

```sql
-- 普通 CTE
WITH dept_avg AS (
    SELECT department_id, AVG(salary) AS avg_sal
    FROM employees GROUP BY department_id
)
SELECT * FROM employees e JOIN dept_avg d
ON e.department_id = d.department_id
WHERE e.salary > d.avg_sal;
```

```sql
-- ⭐ 递归 CTE：查询组织树（面试高频！）
WITH RECURSIVE org_tree AS (
    -- 基例：从根节点开始
    SELECT id, name, parent_id, 1 AS level
    FROM departments WHERE parent_id IS NULL

    UNION ALL

    -- 递归：查找子节点
    SELECT d.id, d.name, d.parent_id, ot.level + 1
    FROM departments d
    JOIN org_tree ot ON d.parent_id = ot.id
)
SELECT * FROM org_tree ORDER BY level, id;
```

### 2. 窗口函数

```sql
-- ROW_NUMBER：每组内编号
SELECT name, department_id, salary,
       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank
FROM employees;

-- LAG/LEAD：访问前一行/后一行数据
SELECT created_at, amount,
       LAG(amount) OVER (ORDER BY created_at) AS prev_amount,
       amount - LAG(amount) OVER (ORDER BY created_at) AS diff
FROM daily_sales;

-- 移动平均
SELECT created_at, amount,
       AVG(amount) OVER (ORDER BY created_at ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily_sales;
```

### 3. RETURNING 子句

```sql
-- 插入后直接返回数据（无需二次查询）
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com')
RETURNING id, created_at;

-- 更新后返回
UPDATE users SET status = 'ACTIVE'
WHERE id = 100
RETURNING *;

-- 删除后返回
DELETE FROM users WHERE last_login < '2023-01-01'
RETURNING id, email;
```

> [!tip] `RETURNING` 是 PG 非常实用的特性，**免去了 INSERT/UPDATE/DELETE 后再次 SELECT**。

### 4. ON CONFLICT（UPSERT）

```sql
-- 插入，如果唯一键冲突则更新
INSERT INTO users (id, name, email)
VALUES (1, 'Alice', 'alice@new.com')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    updated_at = NOW();

-- 冲突时什么都不做
INSERT INTO users (id, name)
VALUES (100, 'Bob')
ON CONFLICT (id) DO NOTHING;
```

### 5. DISTINCT ON

```sql
-- 每组取第一条（比子查询更简洁）
SELECT DISTINCT ON (department_id) *
FROM employees
ORDER BY department_id, salary DESC;
```

---

## 五、事务与 MVCC（PG 实现篇）

### PG 的 MVCC 原理

> [!info] PostgreSQL 的 MVCC 通过**元组版本链**实现，**没有 undo log**，每个元组（行）上有 `xmin`（创建事务 ID）和 `xmax`（删除事务 ID）两个隐藏字段。

```
元组版本示例
═══════════════════════════════════
  (Alice, 100)     ← 最新版本（可见）
   ↑
  (Alice, 80)      ← 旧版本（对并发事务可能可见）
   ↑
  (Alice, 50)      ← 更旧版本
═══════════════════════════════════
```

| 隐藏列 | 含义 |
|:------:|------|
| `xmin` | 创建这个元组的**事务 ID** |
| `xmax` | 删除/更新这个元组的**事务 ID**（为空则仍可见） |
| `cmin` / `cmax` | 命令 ID（同一事务内多个命令） |

### PG vs MySQL MVCC 对比

| 对比项 | PostgreSQL | MySQL (InnoDB) |
|:------:|:-----------|:---------------|
| **实现方式** | 元组版本链（数据本身多版本） | undo log 记录变更 |
| **清理机制** | **Autovacuum** | purge 线程 |
| **回滚方式** | 标记 xmax 为回滚事务 | 读取 undo log 回滚 |
| **REPEATABLE READ 幻读** | ✅ **不会产生幻读**（快照隔离） | ❌ 可能产生（需间隙锁） |

### 查看当前事务与锁

```sql
-- 查看当前活跃事务
SELECT pid, state, query_start, wait_event_type, query
FROM pg_stat_activity
WHERE state != 'idle';

-- 查看锁等待
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_locks blocked
JOIN pg_locks blocking ON ...
```

---

## 六、全文搜索（Full-Text Search）

PostgreSQL 内置全文搜索，无需外部搜索引擎。

### 基础概念

| 概念 | 说明 |
|:----:|------|
| **tsvector** | 文档的**词素**表示（分词 + 位置） |
| **tsquery** | 搜索**查询**表示（条件词 + 逻辑运算） |
| **GIN 索引** | 加速全文搜索的索引 |

```sql
-- 创建全文搜索字段
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    body TEXT,
    tsv TSVECTOR                     -- 预计算分词结果
);

-- 生成 tsvector
UPDATE articles SET tsv =
    to_tsvector('english', title || ' ' || body);

-- 搜索
SELECT id, title
FROM articles
WHERE tsv @@ to_tsquery('english', 'database & performance');

-- 相关性排序
SELECT id, title,
       ts_rank(tsv, to_tsquery('english', 'database')) AS rank
FROM articles
WHERE tsv @@ to_tsquery('english', 'database')
ORDER BY rank DESC;

-- 创建 GIN 索引
CREATE INDEX idx_articles_tsv ON articles USING GIN (tsv);
```

> [!warning] 中文全文搜索需要额外分词插件：
> - `zhparser`（SCWS 分词）
> - `jieba` 分词扩展
> - 或使用 `pg_bigm`（2-gram 方式）

---

## 七、分区表

PostgreSQL **10+** 支持**声明式分区**。

### 分区类型

```sql
-- 1. Range 分区（范围）
CREATE TABLE orders (
    id SERIAL,
    created_at DATE NOT NULL,
    total DECIMAL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- 2. List 分区（列表）
CREATE TABLE users PARTITION BY LIST (region);
CREATE TABLE users_north PARTITION OF users FOR VALUES IN ('北京', '天津');
CREATE TABLE users_south PARTITION OF users FOR VALUES IN ('广州', '深圳');

-- 3. Hash 分区（哈希）
CREATE TABLE logs PARTITION BY HASH (id);
CREATE TABLE logs_p0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE logs_p1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

### 分区裁剪

> [!info] 当查询条件包含分区键时，PG 会自动跳过不相关的分区（**Partition Pruning**），显著提升大表查询性能。

```sql
-- 只扫描 orders_2024 分区
EXPLAIN SELECT * FROM orders WHERE created_at = '2024-06-01';
```

---

## 八、锁与并发控制

### 1. 表级锁

| 锁模式 | 兼容性 |
|:------:|--------|
| `ACCESS SHARE` | 与 ACCESS EXCLUSIVE 冲突（SELECT） |
| `ROW SHARE` | 与 EXCLUSIVE 冲突（SELECT FOR UPDATE） |
| `ROW EXCLUSIVE` | 常见 DML（INSERT/UPDATE/DELETE） |
| `SHARE UPDATE EXCLUSIVE` | VACUUM、CREATE INDEX CONCURRENTLY |
| `SHARE` | CREATE INDEX（不阻塞读） |
| `SHARE ROW EXCLUSIVE` |  |
| `EXCLUSIVE` | REFRESH MATERIALIZED VIEW CONCURRENTLY |
| `ACCESS EXCLUSIVE` | DROP TABLE、TRUNCATE、VACUUM FULL |

### 2. 行级锁

```sql
SELECT * FROM users WHERE id = 1 FOR UPDATE;               -- 排他锁（不等待读）
SELECT * FROM users WHERE id = 1 FOR NO KEY UPDATE;         -- 弱化版 UPDATE 锁
SELECT * FROM users WHERE id = 1 FOR SHARE;                 -- 共享锁
SELECT * FROM users WHERE id = 1 FOR KEY SHARE;             -- 仅锁键
```

### 3. 锁监控

```sql
-- 查看当前锁等待
SELECT relation::regclass, mode, granted
FROM pg_locks
WHERE NOT granted;                      -- granted = false 则正在等待
```

---

## 九、备份、恢复与迁移

### 1. 逻辑备份（pg_dump）

```bash
# 备份单个数据库
pg_dump -h localhost -U postgres mydb > mydb.sql

# 备份并压缩
pg_dump -h localhost -U postgres mydb | gzip > mydb.sql.gz

# 仅备份表结构（-s）
pg_dump -s -h localhost -U postgres mydb > schema.sql

# 恢复
psql -h localhost -U postgres mydb < mydb.sql
```

### 2. 物理备份（pg_basebackup）

```bash
pg_basebackup -h localhost -U replicator -D /backup/dir -P -Xs
```

### 3. PITR（时间点恢复）

基于 **WAL 归档**实现任意时间点的恢复：

```
① 配置 WAL 归档（postgresql.conf）
② pg_basebackup 全量备份
③ 应用 WAL 日志到指定时间点
④ 数据库恢复到目标状态
```

### 4. MySQL → PostgreSQL 迁移注意点

| MySQL 概念 | PG 等效 | 注意事项 |
|:----------:|:--------:|----------|
| `AUTO_INCREMENT` | `SERIAL` / `IDENTITY` | PG 标准语法不同 |
| `ENGINE=InnoDB` | 无需指定 | PG 只有一种存储引擎 |
| `SHOW TABLES` | `\dt` / `pg_tables` | PG 用 `\` 元命令 |
| `LIMIT a, b` | `LIMIT b OFFSET a` | PG 不支持 `LIMIT a, b` |
| `` ` `` 反引号 | `"` 双引号 | PG 使用双引号作为标识符 |
| `ON DUPLICATE KEY UPDATE` | `ON CONFLICT ... DO UPDATE` | PG 的 UPSERT 语法 |

---

## 十、配置与调优

### 1. postgresql.conf 核心参数

| 参数 | 说明 | 建议值 | 影响 |
|:----:|------|:------:|:----:|
| `shared_buffers` | 共享缓冲区大小 | 物理内存的 **25%** | 读性能 |
| `work_mem` | 排序/哈希操作内存 | 从 4MB 开始调优 | 排序查询 |
| `maintenance_work_mem` | 维护操作（VACUUM、索引） | 256MB ~ 1GB | 维护速度 |
| `effective_cache_size` | OS 文件缓存估算 | 物理内存的 **50~75%** | 规划器决策 |
| `random_page_cost` | 随机 IO 成本 | HDD=4, SSD=**1.1** | 索引选择 |
| `max_connections` | 最大连接数 | 通常 100~500 | 内存占用 |
| `wal_buffers` | WAL 缓冲区 | 16MB ~ 64MB | 写入性能 |

> [!tip] **快速调优工具**：使用 `pg_config` 查看编译参数，用 `EXPLAIN ANALYZE` 分析慢查询。

### 2. EXPLAIN ANALYZE 解读

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'alice@example.com';
```

**扫描方式**（性能从好到差）：

| 扫描方式 | 说明 |
|:--------:|------|
| `Index Only Scan` | ⭐ 最优，不回表 |
| `Index Scan` | 回表 |
| `Bitmap Index Scan` | 多个索引组合 |
| `Seq Scan` | ❌ **全表扫描**，需要优化 |

**Join 方式**：

| Join 类型 | 说明 |
|:---------:|------|
| `Nested Loop` | 小表关联大表 |
| `Hash Join` | 等值关联，无索引 |
| `Merge Join` | 已排序数据 |

### 3. pg_stat_statements（慢 SQL 排查）

```sql
-- 启用扩展（需在 postgresql.conf 中配置 shared_preload_libraries）
CREATE EXTENSION pg_stat_statements;

-- 查看最耗时的 SQL
SELECT query, calls, total_exec_time / calls AS avg_time_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### 4. Autovacuum 原理与调优

> [!info] Autovacuum 是 PG **最重要的后台进程**，负责清理 MVCC 产生的死元组，防止事务 ID 回卷。

```sql
-- 查看表的 autovacuum 状态
SELECT relname, n_dead_tup, n_live_tup,
       round(100.0 * n_dead_tup / (n_live_tup + 1)) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY dead_pct DESC;
```

| 参数 | 默认值 | 说明 |
|:----:|:------:|------|
| `autovacuum_vacuum_threshold` | 50 | 触发阈值 |
| `autovacuum_vacuum_scale_factor` | 0.2 | 比例因子（总行数的 20%） |
| `autovacuum_naptime` | 1min | 检查间隔 |

> [!warning] **事务 ID 回卷（Transaction ID Wraparound）** 是 PG 最严重的故障之一，**永远不要禁用 autovacuum**！

---

## 十一、主从复制与高可用

### 1. WAL 架构

PostgreSQL 通过 **WAL（Write-Ahead Log）** 实现数据持久化和复制：

```
事务提交 → 写入 WAL 日志（内存 → 磁盘）
    ↓
WAL 通过流复制发送到从库
    ↓
从库重放 WAL → 数据同步
```

### 2. 流式复制

```conf
# postgresql.conf（主库）
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1024      # MB

# postgresql.conf（从库）
hot_standby = on
primary_conninfo = 'host=master_ip port=5432 user=replicator password=xxx'
```

```bash
# 从库创建（pg_basebackup）
pg_basebackup -h master_ip -D /var/lib/postgresql/data -U replicator -P -Xs
```

### 3. 同步复制 vs 异步复制

| 模式 | 数据安全 | 写入性能 |
|:----:|:--------:|:--------:|
| **异步复制**（默认） | 主库宕机可能丢数据 | 快 |
| **同步复制** | 无损（写入即持久化到至少一个从库） | 慢（需等待从库确认） |

### 4. 逻辑复制（PG 10+）

> 逻辑复制允许**选择性复制**（只复制部分表），支持不同版本间的复制。

```
发布端（Publisher）→ 发布一个表集合 → WAL → 订阅端（Subscriber）
```

---

## 十二、Spring Boot 整合 PostgreSQL

### application.yml 配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: postgres
    password: secret
    driver-class-name: org.postgresql.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      idle-timeout: 300000
      connection-timeout: 20000

  jpa:
    database: postgresql
    hibernate:
      ddl-auto: validate          # ⚠️ PG 推荐 validate，不自动建表
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
```

### MyBatis 集成注意点

```xml
<!-- MyBatis 使用 PG 的 RETURNING 语法获取自增 ID -->
<insert id="insert" useGeneratedKeys="false">
    INSERT INTO users (name, email)
    VALUES (#{name}, #{email})
    <selectKey keyColumn="id" keyProperty="id" resultType="long" order="AFTER">
        SELECT LASTVAL()
    </selectKey>
</insert>
```

### JSONB 字段（MyBatis Plus）

```java
@Data
@TableName(value = "orders", autoResultMap = true)
public class Order {
    private Long id;
    private String customer;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> info;   // JSONB 映射为 Map
}
```

### 连接池推荐

| 连接池 | 说明 |
|:------:|------|
| **HikariCP**（默认） | ⭐ **最推荐**，性能极高 |
| pgagroal | PG 专用连接池 |
| PgBouncer | **轻量级连接池代理**，适合大量短连接场景 |
