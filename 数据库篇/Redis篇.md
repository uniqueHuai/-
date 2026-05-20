# Redis 篇

## 一、基本概念

> [!info] Redis = **内存数据库** + **键值存储** + **高性能**

### Redis 快的原因

| 原因             | 说明              |
| -------------- | --------------- |
| 🚀 **内存操作**    | 避开磁盘瓶颈，数据读写都在内存 |
| 🔒 **单线程模型**   | 避免锁竞争和上下文切换开销   |
| 📊 **高效数据结构**  | 根据场景选择最优数据结构    |
| 🔄 **IO 多路复用** | 单线程同时处理多个客户端连接  |

---

## 二、基本命令

### 1. 全局通用命令

| 命令 | 描述 | 示例 |
|:----:|------|------|
| `KEYS pattern` | 查找匹配的 key（**生产环境慎用，会阻塞！**） | `KEYS user:*` |
| `EXISTS key` | 检查 key 是否存在 | `EXISTS name` |
| `DEL key [key ...]` | 删除 key | `DEL name age` |
| `TYPE key` | 返回值的类型 | `TYPE mylist` → `list` |
| `EXPIRE key seconds` | 设置过期时间（秒） | `EXPIRE temp 60` |
| `TTL key` | 查看剩余过期时间（`-1` 永久，`-2` 已过期） | `TTL temp` |
| `PERSIST key` | 移除过期时间 | `PERSIST temp` |
| `FLUSHALL` | **清空所有数据（危险！）** | — |
| `SELECT index` | 切换数据库（0~15） | `SELECT 1` |

> [!warning] **`KEYS *` 生产环境慎用！** 数据量大时会造成 Redis 阻塞，导致服务不可用。生产环境应使用 `SCAN` 替代。

---

### 2. String（字符串）

最简单的键值类型，value 可以是字符串或数字。

| 命令 | 描述 |
|:----:|------|
| `SET key value [EX] [PX] [NX] [XX]` | 设置键值对（支持过期时间、NX/XX 条件） |
| `GET key` | 获取值 |
| `MSET / MGET` | 批量设置/获取 |
| `INCR / DECR / INCRBY / DECRBY` | 递增/递减操作 |
| `STRLEN key` | 获取字符串长度 |
| `APPEND key value` | 追加到末尾 |
| `GETSET key value` | 设置新值并返回旧值 |

> [!tip] **String 应用场景**：缓存、计数器、分布式锁、Session 存储

---

### 3. Hash（哈希）

键值对集合，适合存储**对象**。

| 命令 | 描述 |
|:----:|------|
| `HSET key field value` | 设置字段值 |
| `HGET key field` | 获取字段值 |
| `HGETALL key` | **获取所有字段和值**（大对象慎用） |
| `HKEYS / HVALS` | 获取所有字段名 / 字段值 |
| `HDEL key field` | 删除字段 |
| `HEXISTS key field` | 判断字段是否存在 |
| `HINCRBY key field increment` | 字段值递增 |
| `HLEN key` | 获取字段数量 |

> [!tip] **Hash 应用场景**：用户信息、商品信息、配置信息等对象数据

---

### 4. List（列表）

按插入顺序排序的**双向链表**。

| 命令 | 描述 |
|:----:|------|
| `LPUSH / RPUSH` | 从左侧/右侧插入 |
| `LPOP / RPOP` | 从左侧/右侧弹出 |
| `LRANGE key start stop` | 获取列表片段 |
| `LLEN key` | 获取长度 |
| `LINDEX key index` | 通过索引获取元素 |
| `LREM key count value` | 移除指定元素 |
| `BLPOP / BRPOP` | **阻塞式**弹出（没有元素时等待） |

> [!tip] **List 应用场景**：消息队列、最新文章列表、朋友圈时间线

---

### 5. Set（集合）

**无序、去重**的 String 集合。

| 命令 | 描述 |
|:----:|------|
| `SADD key member` | 添加成员 |
| `SMEMBERS key` | 获取所有成员 |
| `SISMEMBER key member` | 判断是否为成员 |
| `SREM key member` | 移除成员 |
| `SCARD key` | 获取成员数 |
| `SINTER / SUNION / SDIFF` | **交集 / 并集 / 差集** |
| `SPOP / SRANDMEMBER` | 随机弹出 / 随机返回（不弹出） |

> [!tip] **Set 应用场景**：标签（Tag）、共同好友、抽奖、唯一计数

---

### 6. Sorted Set（ZSet — 有序集合）

**去重 + 排序**，每个元素关联一个 `score`（分数）。

| 命令 | 描述 |
|:----:|------|
| `ZADD key score member` | 添加成员并指定分数 |
| `ZRANGE key start stop` | 按分数从**低到高**返回 |
| `ZREVRANGE key start stop` | 按分数从**高到低**返回 |
| `ZRANK / ZREVRANK` | 获取排名 |
| `ZSCORE key member` | 获取分数 |
| `ZINCRBY key increment member` | 增加分数 |
| `ZCARD key` | 获取成员数 |
| `ZCOUNT key min max` | 统计指定分数区间内的成员数 |
| `ZINTERSTORE / ZUNIONSTORE` | **交集 / 并集** 并存入新 key |

> [!tip] **ZSet 应用场景**：排行榜、带权重的任务队列、范围查找

---

### 7. Geospatial（地理空间）

底层基于 **Sorted Set** 实现，通过 Geohash 算法将经纬度编码为一维分数。

| 命令 | 描述 |
|:----:|------|
| `GEOADD key lng lat member` | 添加地理位置 |
| `GEOPOS key member` | 获取坐标 |
| `GEODIST key m1 m2 [unit]` | 计算两地距离 |
| `GEOSEARCH` | **Redis 6.2+ 统一搜索**（推荐） |
| `GEORADIUS` | 以给定坐标为中心搜索半径内的元素 |

> [!tip] **应用场景**：附近的人、骑行轨迹记录、距离计算

---

### 8. HyperLogLog（HLL — 基数统计）

**特点**：用约 **12KB** 固定内存，估算 **2^64** 个不重复元素，误差率约 **0.81%**。

| 命令 | 描述 |
|:----:|------|
| `PFADD key element` | 添加元素 |
| `PFCOUNT key` | 估算基数 |
| `PFMERGE dest source` | 合并多个 HLL |

> [!tip] **典型场景：统计 UV（独立访客数）**
> ```bash
> PFADD uv:20231001 "user:1001" "user:1002"
> PFCOUNT uv:20231001  # → 2
> PFMERGE uv:total uv:20231001 uv:20231002
> ```

---

### 9. Bitmap（位图）

本质是 **String**，按**位（bit）** 操作，每个 bit 存 0 或 1。

| 命令 | 描述 |
|:----:|------|
| `SETBIT key offset value` | 设置某一位 |
| `GETBIT key offset` | 获取某一位 |
| `BITCOUNT key` | 统计为 1 的位数 |
| `BITPOS key bit` | 查找第一个为 0/1 的位 |
| `BITOP op dest key` | 位运算（AND / OR / XOR / NOT） |

> [!tip] **典型场景：用户签到统计**
> ```bash
> SETBIT user:sign:1000 5 1     # 第 1000 号用户在第 5 天签到
> GETBIT user:sign:1000 5        # 查询是否签到
> BITCOUNT user:sign:1000        # 统计签到总次数
> ```

---

## 三、事务

> [!warning] **Redis 事务 vs 数据库事务**
> Redis 事务是"命令打包执行"**不是真正的事务回滚**——失败后不取消已执行的命令！

### 事务命令

| 命令 | 描述 |
|:----:|------|
| `MULTI` | 开启事务，后续命令入队不执行 |
| `EXEC` | **执行**队列中的所有命令 |
| `DISCARD` | **取消**事务，清空队列 |
| `WATCH key` | **乐观锁**，监视 key 是否被修改 |
| `UNWATCH` | 取消监视 |

### Redis 事务三大特性

| 特性 | 是否支持 | 说明 |
|:----:|:--------:|------|
| **原子性** | ❌ | **不保证回滚**，某命令失败后继续执行后续命令 |
| **隔离性** | ✅ | 单线程，`EXEC` 执行时不被其他命令打断 |
| **持久性** | ⚠️ | 取决于 RDB/AOF 持久化配置 |

### WATCH 乐观锁示例

```bash
WATCH balance:100           # 监视余额
MULTI                       # 开启事务
DECRBY balance:100 20       # 扣减 20
EXEC                        # 如果期间 balance 被修改 → 返回 nil（失败）
```

> [!tip] 应用层检测 `EXEC` 返回 `nil` 后，**重试整个逻辑**即可实现 CAS。

---

## 四、Jedis（Java 客户端）

### 核心特征

- ✅ **全面**：支持几乎所有 Redis 命令
- ✅ **高效**：支持连接池、Pipeline、事务
- ❌ **线程不安全**：一个实例不可被多线程共享

### 快速开始

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>5.1.2</version>
</dependency>
```

```java
try (Jedis jedis = new Jedis("localhost", 6379)) {
    jedis.set("key", "Hello Jedis!");
    String value = jedis.get("key");
}
```

### 连接池（JedisPool）— 生产环境必须使用

```java
JedisPoolConfig poolConfig = new JedisPoolConfig();
poolConfig.setMaxTotal(128);
poolConfig.setMaxIdle(64);
poolConfig.setMinIdle(10);
poolConfig.setTestOnBorrow(true);

try (JedisPool jedisPool = new JedisPool(poolConfig, "localhost", 6379, 2000);
     Jedis jedis = jedisPool.getResource()) {
    jedis.set("pooledKey", "pooledValue");
}
```

> [!tip] **JedisPool 应该是全局单例**，应用启动时创建，关闭时销毁。

### Pipeline（管道） vs 事务

| 特性 | Pipeline | 事务（Transaction） |
|:----:|:--------:|:-------------------:|
| **原子性** | ❌ | ✅ 一次性执行 |
| **目的** | 减少网络 RTT | 命令打包，排他执行 |
| **返回值** | 可获取 | 统一返回 |

---

## 五、Spring Boot 整合 Redis

### 依赖配置

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

### 核心组件

| 组件 | 序列化器 | 说明 |
|:----:|:---------:|------|
| **`RedisTemplate`** | JdkSerializationRedisSerializer（默认） | 可存任何 `Serializable` 对象，但不可读 |
| **`StringRedisTemplate`** | StringRedisSerializer | **推荐**，存入数据人类可读 |

### opsForXxx() 方法

| 操作类型 | 方法 | 返回接口 |
|:--------:|:----:|:--------:|
| String | `opsForValue()` | `ValueOperations` |
| Hash | `opsForHash()` | `HashOperations` |
| List | `opsForList()` | `ListOperations` |
| Set | `opsForSet()` | `SetOperations` |
| ZSet | `opsForZSet()` | `ZSetOperations` |

### 自定义 JSON 序列化

```java
@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

---

## 六、高级特性

### 1. Spring 声明式事务

```java
@Service
public class TransactionService {
    @Autowired
    private StringRedisTemplate redisTemplate;

    @Transactional
    public void transactionalMethod() {
        redisTemplate.opsForValue().set("key1", "value1");
        redisTemplate.opsForValue().increment("counter", 1);
    }
}
```

### 2. 持久化：RDB vs AOF

| 对比 | RDB（快照） | AOF（日志） |
|:----:|:----------:|:----------:|
| **方式** | 定期生成二进制快照 | 记录每个写命令 |
| **文件大小** | 较小 | 较大 |
| **恢复速度** | 快 | 慢 |
| **数据丢失** | 可能丢失较多数据 | 丢失较少（取决于 fsync 策略） |
| **启动优先级** | 低 | **高**（AOF 优先加载） |

```conf
# redis.conf — 推荐同时开启
save 900 1         # 900 秒内至少 1 个 key 变更
save 300 10        # 300 秒内至少 10 个 key 变更
save 60 10000      # 60 秒内至少 10000 个 key 变更
appendonly yes     # 开启 AOF
appendfsync everysec  # 推荐：每秒同步
```

### 3. 发布订阅（Pub/Sub）

```java
// 订阅者
@Slf4j
@Component
public class MyRedisMessageListener implements MessageListener {
    @Override
    public void onMessage(Message message, byte[] pattern) {
        log.info("收到消息: {} 来自频道: {}", message.getBody(), message.getChannel());
    }
}

// 发布者
redisTemplate.convertAndSend("myChannel", "Hello, PubSub!");
```

### 4. 缓存抽象 @Cacheable

```java
@EnableCaching  // 启动类上开启

@Service
public class UserService {
    @Cacheable(value = "user", key = "#id")      // 查询缓存
    public User getUserById(Long id) { ... }

    @CachePut(value = "user", key = "#user.id")  // 更新缓存
    public User updateUser(User user) { ... }

    @CacheEvict(value = "user", key = "#id")      // 清除缓存
    public void deleteUserById(Long id) { ... }
}
```

---

## 七、缓存三大问题

### 1. 缓存穿透（Cache Penetration）

**问题**：查询**不存在的数据**，请求直接穿透缓存打到数据库。

| 解决方案 | 优点 | 缺点 |
|----------|:----:|:----:|
| **缓存空对象** | 实现简单 | 占用内存 |
| **布隆过滤器** | 内存极小、效率极高 | 有误判率 |

> [!tip] 布隆过滤器原理：将所有可能的 key 加载到二进制向量中，能**快速判断 key 绝对不存在**，但不能完全确定 key 存在。

### 2. 缓存雪崩（Cache Avalanche）

**问题**：**大量 key 同时过期**，请求瞬间涌向数据库。

| 解决方案 | 说明 |
|:--------:|------|
| ⭐ **随机过期时间** | 基础过期时间 + 随机值（最简单有效） |
| **永不过期 + 后台更新** | 定时任务异步刷新缓存 |
| **熔断降级限流** | Sentinel / Hystrix 保护数据库 |
| **高可用集群** | Redis 主从 / 哨兵 / 集群 |

### 3. 缓存击穿（Cache Breakdown）

**问题**：**单个热点 key** 过期瞬间，大量并发请求同时访问数据库。

> [!tip] **解决方案：互斥锁**
> 第一个发现缓存过期的线程获取锁 → 查数据库回填缓存 → 其他线程等待后直接读缓存

### 三大问题对比

| 对比项 | **缓存穿透** | **缓存雪崩** | **缓存击穿** |
|:------:|:-----------:|:-----------:|:-----------:|
| **问题本质** | 查询不存在的数据 | 大量 key 同时失效 | 单个热点 key 失效 |
| **影响范围** | 个别不存在的 key | 全局性、大量 key | 单个热点 key |
| **解决方案** | 缓存空值 / 布隆过滤器 | **随机过期时间** / 熔断限流 | **互斥锁** |

---

## 八、集群搭建

### 主从复制 + 哨兵模式

```bash
# 1. 创建 Docker 网络
docker network create redis-sentinel-net

# 2. 启动主节点
docker run -d --name redis-master --net redis-sentinel-net \
  -p 6379:6379 redis:latest redis-server --requirepass 123456 --appendonly yes

# 3. 启动从节点
docker run -d --name redis-slave1 --net redis-sentinel-net \
  -p 6380:6379 redis:latest redis-server --replicaof redis-master 6379 \
  --masterauth 123456 --appendonly yes
```

```conf
# sentinel.conf
sentinel monitor mymaster redis-master 6379 2   # 2 个哨兵同意才故障转移
sentinel auth-pass mymaster 123456
sentinel down-after-milliseconds mymaster 5000
```

> [!info] **哨兵模式做了啥？**
> 监控主节点状态 → 主节点宕机 → **自动故障转移**（选新主节点）→ 通知客户端更新

---

## 九、最佳实践

> [!tip] **Redis 使用要点**
> 1. ✅ 首选 `StringRedisTemplate`，可读性好
> 2. ✅ 生产环境配置 JSON 序列化
> 3. ✅ **必须使用连接池**
> 4. ✅ Key 命名使用冒号分层：`user:1001:profile`
> 5. ✅ 批量操作使用 Pipeline
> 6. ⚠️ 理解 Redis 事务是"批量执行"而非"回滚"
> 7. ⚠️ `@Cacheable` 缓存空对象可能爆内存，用 `unless = "#result == null"` 避免
