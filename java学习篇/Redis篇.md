# 1. 基本概念

定义：内存数据库 + 键值存储 + 高性能

快的原因：内存操作（避开磁盘瓶颈）+ 单线程避免切换（避免锁 & 上下文切换）+ 高效数据结构 + 单线程和IO多路复用

# 2.基本命令

## 一、全局通用命令

这些命令不针对特定数据类型。

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`**KEYS pattern**`|**查找所有符合给定模式** `**pattern**`<br><br>**的 key**。生产环境慎用，会造成阻塞！|`**KEYS ***`<br><br>(查看所有key) `**KEYS user:***`|
|`**EXISTS key**`|检查给定的 `**key**`<br><br>是否存在。|`**EXISTS name**`|
|`**DEL key**`|删除指定的一个或多个 `**key**`<br><br>。|`**DEL name age**`|
|`**TYPE key**`|返回 `**key**`<br><br>所储存的值的类型。|`**TYPE mylist**`<br><br>-> `**list**`|
|`**EXPIRE key seconds**`|为 `**key**`<br><br>设置过期时间，单位为**秒**。|`**EXPIRE temp_data 60**`<br><br>(60秒后过期)|
|`**TTL key**`|查看 `**key**`<br><br>剩余的过期时间（秒）。`**-1**`<br><br>表示永不过期，`**-2**`<br><br>表示已过期/不存在。|`**TTL temp_data**`|
|`**PERSIST key**`|移除 `**key**`<br><br>的过期时间，使其永不过期。|`**PERSIST temp_data**`|
|`**FLUSHALL**`|**清空整个 Redis 服务器的数据**（所有数据库）。**非常危险！**||
|`**SELECT index**`|切换数据库。Redis 默认有 16 个数据库，索引从 0 到 15。|`**SELECT 1**`<br><br>(切换到 1 号数据库)|

---

## 二、核心数据结构命令

### 1. String（字符串）

最简单的键值类型，value 可以是字符串或数字。

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`SET key value [EX seconds] [PX milliseconds] [NXXX]`|设置键值对（可设置过期时间、NX：键不存在时设置、XX：键存在时设置）。|`**SET session:1234 "data" EX 3600 NX**`|
|`**GET key**`|获取指定 key 的值。|`**GET name**`<br><br>-> `**"Alice"**`|
|`**GETSET key value**`|设置新值并返回旧值。|`**GETSET count 10**`|
|`**MSET key value [key value ...]**`|同时设置多个键值对。|`**MSET k1 v1 k2 v2**`|
|`**MGET key [key ...]**`|获取所有给定 key 的值。|`**MGET k1 k2**`<br><br>-> `**1) "v1" 2) "v2"**`|
|`**STRLEN key**`|返回 key 所存储的字符串值的长度。|`**STRLEN name**`<br><br>-> `**5**`|
|`**INCR key**`|将 key 中储存的数字值增一。|`**INCR count**`|
|`**DECR key**`|将 key 中储存的数字值减一。|`**DECR count**`|
|`**INCRBY key increment**`|将 key 所储存的值加上给定的增量值。|`**INCRBY count 5**`|
|`**DECRBY key decrement**`|将 key 所储存的值减去给定的减量值。|`**DECRBY count 3**`|
|`**APPEND key value**`|将 value 追加到原值的末尾。|`**APPEND name " Smith"**`|

**应用场景**：缓存、计数器、分布式锁、Session 存储。

---

### 2. Hash（哈希）

键值对集合，适合存储对象。

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`**HSET key field value [field value ...]**`|设置哈希表 key 中的一个或多个 field-value 对。|`**HSET user:1000 name "Bob" age 30**`|
|`**HGET key field**`|获取哈希表中指定字段的值。|`**HGET user:1000 name**`<br><br>-> `**"Bob"**`|
|`**HGETALL key**`|获取哈希表中指定 key 的所有字段和值。|`**HGETALL user:1000**`<br><br>-> `**1) "name" 2) "Bob" 3) "age" 4) "30"**`|
|`**HDEL key field [field ...]**`|删除哈希表 key 中的一个或多个指定字段。|`**HDEL user:1000 age**`|
|`**HKEYS key**`|获取哈希表 key 中的所有字段名。|`**HKEYS user:1000**`<br><br>-> `**1) "name"**`|
|`**HVALS key**`|获取哈希表 key 中所有字段的值。|`**HVALS user:1000**`<br><br>-> `**1) "Bob"**`|
|`**HEXISTS key field**`|检查哈希表 key 中指定的字段是否存在。|`**HEXISTS user:1000 name**`<br><br>-> `**1**`|
|`**HINCRBY key field increment**`|为哈希表 key 中的指定字段的整数值加上增量。|`**HINCRBY user:1000 score 5**`|
|`**HLEN key**`|获取哈希表 key 中字段的数量。|`**HLEN user:1000**`<br><br>-> `**2**`|

**应用场景**：存储用户信息、商品信息、配置信息等对象数据。

---

### 3. List（列表）

简单的字符串列表，按插入顺序排序，是双向链表。

|                                    |                                              |                                                  |
| ---------------------------------- | -------------------------------------------- | ------------------------------------------------ |
| **命令**                             | **描述（L=Left左, R=Right右）**                    | **示例**                                           |
| `**LPUSH key value [value ...]**`  | 将一个或多个值插入到列表头部（左边）。                          | `**LPUSH mylist A B**`<br><br>-> 列表为 `**B, A**`  |
| `**RPUSH key value [value ...]**`  | 将一个或多个值插入到列表尾部（右边）。                          | `**RPUSH mylist C**`<br><br>-> 列表为 `**B, A, C**` |
| `**LPOP key**`                     | 移除并返回列表的第一个元素（左边）。                           | `**LPOP mylist**`<br><br>-> `**"B"**`            |
| `**RPOP key**`                     | 移除并返回列表的最后一个元素（右边）。                          | `**RPOP mylist**`<br><br>-> `**"C"**`            |
| `**LRANGE key start stop**`        | 获取列表指定范围内的元素（0 第一个，-1 最后一个）。                 | `**LRANGE mylist 0 -1**`<br><br>-> `**1) "A"**`  |
| `**LLEN key**`                     | 获取列表长度。                                      | `**LLEN mylist**`<br><br>-> `**1**`              |
| `**LINDEX key index**`             | 通过索引获取列表中的元素。                                | `**LINDEX mylist 0**`<br><br>-> `**"A"**`        |
| `**LREM key count value**`         | 根据参数 count 的值，移除列表中与参数 value 相等的元素。          | `**LREM mylist 1 "A"**`                          |
| `**RPOPLPUSH source destination**` | 从 source 列表尾部弹出元素并推入 destination 列表头部（原子操作）。 | `**RPOPLPUSH list1 list2**`                      |
| `**BLPOP key [key ...] timeout**`  | 移出并获取列表的第一个元素，如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。 | `**BLPOP task_queue 30**`                        |

![](https://cdn.nlark.com/yuque/0/2025/png/52814014/1756115584925-5b456d91-979f-45df-9c2f-52cf4874a2da.png)

**应用场景**：消息队列、最新文章列表、朋友圈时间线、发布/订阅模型。

---

### 4. Set（集合）

String 类型的无序集合，集合成员是唯一的。

|                                    |                              |                                              |
| ---------------------------------- | ---------------------------- | -------------------------------------------- |
| **命令**                             | **描述**                       | **示例**                                       |
| `**SADD key member [member ...]**` | 向集合添加一个或多个成员。                | `**SADD tags Redis MongoDB MySQL**`          |
| `**SMEMBERS key**`                 | 返回集合中的所有成员。                  | `**SMEMBERS tags**`<br><br>-> 无序返回           |
| `**SISMEMBER key member**`         | 判断 member 元素是否是集合 key 的成员。   | `**SISMEMBER tags Redis**`<br><br>-> `**1**` |
| `**SREM key member [member ...]**` | 移除集合中一个或多个成员。                | `**SREM tags MySQL**`                        |
| `**SCARD key**`                    | 获取集合的成员数。                    | `**SCARD tags**`<br><br>-> `**2**`           |
| `**SINTER key [key ...]**`         | 返回给定所有集合的交集。                 | `**SINTER set1 set2**`                       |
| `**SUNION key [key ...]**`         | 返回给定所有集合的并集。                 | `**SUNION set1 set2**`                       |
| `**SDIFF key [key ...]**`          | 返回给定所有集合的差集（key1 相对于其他集合的差）。 | `**SDIFF set1 set2**`                        |
| `**SPOP key [count]**`             | 移除并返回集合中的一个或多个随机元素。          | `**SPOP tags 1**`<br><br>-> `**"Redis"**`    |
| `**SRANDMEMBER key [count]**`      | 返回集合中一个或多个随机数，但不移除。          | `**SRANDMEMBER tags 2**`                     |

**应用场景**：标签（Tag）、共同好友、抽奖、唯一计数。

---

### 5. Sorted Set（有序集合 / ZSet）

String 类型元素的集合，不允许重复，但每个元素关联一个分数（score）用于排序。

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`ZADD key [NXXX] [GTLT] [CH] [INCR] score member [score member ...]`|向有序集合添加成员或更新分数（NX：不存在才设置，XX：存在才更新，LT：新分数小于当前分数才更新，GT：大于才更新，CH：返回变化的成员数）。|`**ZADD leaderboard 100 "Alice" 200 "Bob"**`|
|`**ZRANGE key start stop [WITHSCORES]**`|通过索引区间返回有序集合指定区间内的成员（低到高）。|`**ZRANGE leaderboard 0 -1 WITHSCORES**`|
|`**ZREVRANGE key start stop [WITHSCORES]**`|返回有序集中指定区间内的成员，通过索引，分数从高到低。|`**ZREVRANGE leaderboard 0 1 WITHSCORES**`|
|`**ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]**`|通过分数返回有序集合指定区间内的成员（低到高）。|`**ZRANGEBYSCORE leaderboard 50 200 WITHSCORES**`|
|`**ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]**`|通过分数返回有序集合指定区间内的成员（高到低）。|`**ZREVRANGEBYSCORE leaderboard 200 50 WITHSCORES**`|
|`**ZRANK key member**`|返回有序集合中指定成员的排名（从0开始，分数从小到大）。|`**ZRANK leaderboard "Alice"**`<br><br>-> `**0**`|
|`**ZREVRANK key member**`|返回有序集合中指定成员的排名（从0开始，分数从大到小）。|`**ZREVRANK leaderboard "Alice"**`<br><br>-> `**1**`|
|`**ZSCORE key member**`|返回有序集中，成员的分数值。|`**ZSCORE leaderboard "Bob"**`<br><br>-> `**"200"**`|
|`**ZINCRBY key increment member**`|为有序集合 key 的成员 member 的分数加上增量 increment。|`**ZINCRBY leaderboard 50 "Alice"**`<br><br>-> `**"150"**`|
|`**ZCARD key**`|获取有序集合的成员数。|`**ZCARD leaderboard**`<br><br>-> `**2**`|
|`**ZCOUNT key min max**`|计算在有序集合中指定分数区间内的成员数量。|`**ZCOUNT leaderboard 100 300**`<br><br>-> `**2**`|
|`**ZREM key member [member ...]**`|移除有序集合中的一个或多个成员。|`**ZREM leaderboard "Charlie"**`|
|`**ZREMRANGEBYRANK key start stop**`|移除有序集合中给定的排名区间的所有成员。|`**ZREMRANGEBYRANK leaderboard 0 0**`|
|`**ZREMRANGEBYSCORE key min max**`|移除有序集合中给定的分数区间的所有成员。|`**ZREMRANGEBYSCORE leaderboard 0 100**`|
|`**ZINTERSTORE / ZUNIONSTORE**`|计算多个有序集合的交集/并集并将结果存储在新的 key 中。|`**ZINTERSTORE out 2 zset1 zset2 WEIGHTS 2 3**`|

**应用场景**：排行榜、带权重的任务队列、范围查找（如时间线）。

---

### 6.Geospatial（地理空间）

Geospatial 数据类型允许你存储经纬度坐标（经度, 纬度），并基于这些坐标进行高效的地理位置计算，其底层实现是基于 **Sorted Set (ZSet)**。它巧妙地将二维的经纬度通过 **Geohash** 算法编码成一维的分数（score），然后将地点名称作为 member，分数就是这个编码值。

- **Key**: 代表一个地理空间集合（例如 `**cities:location**`, `**bikes:around**`）
- **Member**: 地点的唯一标识符（例如 `**"Beijing"**`, `**"bike:123"**`）
- **Score**: 经过 Geohash 编码后得到的数字，代表其地理位置。

|   |   |   |
|---|---|---|
|**命令**|**描述及参数**|**示例**|
|`**GEOADD key [NX\|XX] [CH] longitude latitude member [longitude latitude member ...]**`|**向集合中添加一个或多个地理空间位置。**  <br>• `**NX**`<br><br>：仅添加新元素，不更新已有元素。  <br>• `**XX**`<br><br>：仅更新已有元素，不添加新元素。  <br>• `**CH**`<br><br>：返回发生变化的元素数量（新增+更新的）。|`**GEOADD cities:location 116.405285 39.904989 "Beijing" 121.472644 31.231706 "Shanghai"**`|
|`**GEOPOS key member [member ...]**`|**返回一个或多个成员的经纬度坐标。**|`**GEOPOS cities:location Beijing**`<br><br>  <br>-> `**1) 1) "116.405285" 2) "39.904989"**`|
|`**GEODIST key member1 member2 [m\|km\|ft\|mi]**`|**返回两个给定位置之间的距离。**  <br>• `**m**`<br><br>：米 (默认)  <br>• `**km**`<br><br>：公里  <br>• `**mi**`<br><br>：英里  <br>• `**ft**`<br><br>：英尺|`**GEODIST cities:location Beijing Shanghai km**`<br><br>  <br>-> `**"1067.5980"**`<br><br>(约1068公里)|
|`**GEORADIUS key longitude latitude radius m\|km\|ft\|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC\|DESC]**`<br><br>  <br>**(Redis 6.2 后建议使用** `**GEOSEARCH**`<br><br>**)**|**以给定的经纬度为中心，找出某一半径内的元素。**  <br>• `**WITHDIST**`<br><br>：同时返回距离。  <br>• `**WITHCOORD**`<br><br>：同时返回坐标。  <br>• `**COUNT n**`<br><br>：限制返回结果数量。  <br>• `**ASC/DESC**`<br><br>：按距离排序。|`**GEORADIUS cities:location 116.4 39.9 100 km WITHDIST**`<br><br>  <br>-> `**1) 1) "Beijing" 2) "5.8315"**`<br><br>(北京距离中心点约5.8公里)|
|`**GEORADIUSBYMEMBER key member radius m\|km\|ft\|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC\|DESC]**`<br><br>  <br>**(Redis 6.2 后建议使用** `**GEOSEARCH**`<br><br>**)**|**功能同** `**GEORADIUS**`<br><br>**，但中心点由指定的成员决定。**|`**GEORADIUSBYMEMBER cities:location Beijing 200 km WITHDIST**`<br><br>  <br>-> 查找北京200公里内的城市。|
|`**GEOSEARCH key [FROMMEMBER member] [FROMLONLAT long lat] [BYRADIUS radius m\|km\|ft\|mi] [BYBOX width height m\|km\|ft\|mi] [ASC\|DESC] [COUNT count] [WITHCOORD] [WITHDIST] [WITHHASH]**`|**Redis 6.2 新增的统一搜索命令，更直观、更强大。**  <br>• `**FROMMEMBER**`<br><br>或 `**FROMLONLAT**`<br><br>：指定中心点。  <br>• `**BYRADIUS**`<br><br>或 `**BYBOX**`<br><br>：指定圆形或矩形搜索区域。|`**GEOSEARCH cities:location FROMMEMBER Beijing BYRADIUS 1000 km ASC COUNT 5 WITHDIST**`<br><br>  <br>-> 查找北京1000公里内最近的5个城市及距离。|
|`**GEOHASH key member [member ...]**`|**返回一个或多个位置元素的 Geohash 表示。**  <br>这是一个由11个字符组成的字符串，是经纬度的编码，可以用于外部地图应用。|`**GEOHASH cities:location Beijing**`<br><br>  <br>-> `**1) "wx4g0f8fv20"**`|

1. **附近的人/地点（Nearby）**：这是最经典的应用。

- **命令**：`**GEORADIUS**` 或 `**GEOSEARCH**`
- **示例**：查找我附近3公里内的所有共享单车、餐厅、朋友。

2. **骑行/跑步轨迹记录**：

- **命令**：`**GEOADD**`
- **示例**：记录一辆共享单车的位置变化（`**GEOADD bikes:locations <lng> <lat> bike:123**`）。

3. **距离计算**：

- **命令**：`**GEODIST**`
- **示例**：在电商中计算用户与商家的距离，用以估算配送费和时间。

4. **地理位置信息存储**：

- **命令**：`**GEOADD**`, `**GEOPOS**`
- **示例**：存储所有门店的经纬度信息，方便查询和展示在地图上。

---

### 7.HyperLogLog (HLL)

- **基数 (Cardinality)**：一个集合中**不重复**元素的个数。

- 例如：集合 `**{1, 2, 3, 2, 1, 5}**` 的基数是 4（不重复元素为 1, 2, 3, 5）。

- **问题**：如何统计一个超大集合的基数？（例如，统计某网页一天的 **UV（独立访客数）**，即有多少个不同的用户 IP 访问）。

- 使用 `**Set**`：如果 IP 有 1 亿个，那么 `**SET**` 需要消耗大量的内存（可能几个 GB）来存储所有 IP，这非常昂贵。
- 使用 `**HyperLogLog**`：**它不需要存储每个元素本身**，而是用一个极小的固定大小的数据结构（约 12 KB）来估算基数，误差率仅为 **0.81%**。

**简单来说，HyperLogLog 用大约 12KB 的内存，就能估算出最高接近 2^64 个不重复元素的基数，并且误差率很小。**

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`**PFADD key element [element ...]**`|**将任意数量的元素添加到 HyperLogLog 结构中。**  <br>• 如果 HyperLogLog 的内部结构被修改了，则返回 1，否则返回 0。|`**PFADD visits:20231001 "192.168.1.1" "10.0.0.2"**`<br><br>  <br>-> `**(integer) 1**`|
|`**PFCOUNT key [key ...]**`|**返回单个 HyperLogLog 的估算基数，或多个 HyperLogLog 的并集的基数。**|`**PFCOUNT visits:20231001**`<br><br>  <br>-> `**(integer) 2**`<br><br>  <br>`**PFCOUNT visits:20231001 visits:20231002**`<br><br>(计算两天的总UV)|
|`**PFMERGE destkey sourcekey [sourcekey ...]**`|**将多个 HyperLogLog 合并（merge）为一个 HyperLogLog，合并后的 HyperLogLog 存储在** `**destkey**`<br><br>**中。**  <br>• 合并后的基数是所有 sourcekey 的**并集**的基数。|`**PFMERGE visits:total visits:20231001 visits:20231002**`<br><br>  <br>(将两天的数据合并，`**visits:total**`<br><br>中存储的是这两天的总UV)|

HyperLogLog **只做一件事，并且做得非常好**：**去重计数**。

**统计网站/应用的每日/每月 UV（独立用户访问量）**：

1. bash

```
# 用户 1001 访问
PFADD uv:20231001 "user:1001"
# 用户 1002 访问
PFADD uv:20231001 "user:1002"
# 用户 1001 再次访问（不会重复计算）
PFADD uv:20231001 "user:1001"

# 查看当日 UV
PFCOUNT uv:20231001
-> (integer) 2

# 合并一周的数据，计算周UV
PFMERGE uv:2023w40 uv:20231001 uv:20231002 ... uv:20231007
PFCOUNT uv:2023w40
```

2. **统计搜索引擎的不同搜索查询词数量**。
3. **统计数据库中某个大型字段的不同值的数量**（无需执行昂贵的 `**DISTINCT COUNT**` SQL 查询）。
4. **统计网络中一天内不同的源 IP 地址数量**（用于监控和分析）。

---

### 8.Bitmap（位图）

Bitmap 的本质是一个 **String** 值，但它被当作一个由 **比特位（bit）** 组成的数组来处理。数组的每个单元只能存储 `**0**` 或 `**1**`。

|   |   |   |
|---|---|---|
|**命令**|**描述**|**示例**|
|`**SETBIT key offset value**`|**对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。**  <br>• `**value**`<br><br>只能是 `**0**`<br><br>或 `**1**`<br><br>。  <br>• 返回**原位置**的旧值。|`**SETBIT user:sign:1000 5 1**`<br><br>  <br>-> `**(integer) 0**`<br><br>(表示第5位原来的值是0)  <br>_含义：用户1000在第5天签到了_|
|`**GETBIT key offset**`|**获取键对应值的指定偏移量上的位(bit)。**  <br>• 如果偏移量超出当前值的长度，返回 `**0**`<br><br>。|`**GETBIT user:sign:1000 5**`<br><br>  <br>-> `**(integer) 1**`<br><br>  <br>_含义：查询用户1000第5天是否签到（是）_|
|`**BITCOUNT key [start end]**`|**计算给定字符串中，被设置为** `**1**`<br><br>**的比特位的数量。**  <br>• `**start**`<br><br>和 `**end**`<br><br>是**字节索引**，不是位索引。`**0 -1**`<br><br>表示所有字节。|`**BITCOUNT user:sign:1000**`<br><br>  <br>-> `**(integer) 3**`<br><br>  <br>_含义：用户1000总共签到了3次_|
|`**BITPOS key bit [start [end]]**`|**返回位图中第一个值为** `**bit**`<br><br>**(0或1) 的二进制位的位置。**  <br>• 同样，`**start**`<br><br>和 `**end**`<br><br>是字节索引。|`**BITPOS user:sign:1000 1**`<br><br>  <br>-> `**(integer) 0**`<br><br>  <br>_含义：用户1000第一次签到是在第0天_|
|`**BITOP operation destkey key [key ...]**`|**对一个或多个保存二进制位的键执行位操作，并将结果保存到** `**destkey**`<br><br>**上。**  <br>• `**operation**`<br><br>可以是 `**AND**`<br><br>(与), `**OR**`<br><br>(或), `**XOR**`<br><br>(异或), `**NOT**`<br><br>(非)。|`**BITOP AND result key1 key2**`<br><br>  <br>_含义：将key1和key2进行按位与操作，结果存到result中_|

常用场景：

1. **用户签到统计 / 活跃度统计**

- 这是最经典的场景。 key 可以设计为 `**user:sign:{userId}**` 或 `**activity:20231001**`。
- **签到**：`**SETBIT user:sign:1000 5 1**` （第1000号用户在今年第5天签到）
- **检查某天是否签到**：`**GETBIT user:sign:1000 5**`
- **统计本月签到次数**：`**BITCOUNT user:sign:1000**`
- **获取本月第一次签到的日期**：`**BITPOS user:sign:1000 1**` (返回的是偏移量，即日期)

2. **用户行为跟踪（是否完成某任务）**

- key: `**task:finished:123**` (任务123的完成情况)
- `**SETBIT task:finished:123 1000 1**` (标记用户1000完成了任务123)

---

# 3.事务

**Redis 事务的主要目的是将一个或多个命令打包，然后按顺序、一次性、排他性地执行。它通过命令** `**MULTI**`**,** `**EXEC**`**,** `**DISCARD**` **和** `**WATCH**` **来实现。**  

### 事务的生命周期与常用命令

|   |   |   |
|---|---|---|
|**阶段**|**命令**|**描述**|
|**1. 开启事务**|`**MULTI**`|标记一个事务块的开始。后续的命令都不会立即执行，而是被放入一个队列中。返回 `**OK**`<br><br>。|
|**2. 命令入队**|`**SET, GET, INCR...**`|在 `**MULTI**`<br><br>后输入的所有命令都会按顺序进入事务队列。Redis 返回 `**QUEUED**`<br><br>表示命令已入队。|
|**3. 执行事务**|`**EXEC**`|执行事务队列中的所有命令。返回一个列表，包含每个命令的执行结果，按入队顺序排列。|
|**（可选）取消事务**|`**DISCARD**`|放弃事务，清空事务队列。连接状态恢复正常。|
|**（高级）乐观锁**|`**WATCH key [key ...]**`|在 `**MULTI**`<br><br>之前执行，监视一个或多个 key。如果在 `**EXEC**`<br><br>执行前这些 key 被其他客户端修改，则整个事务将被放弃（返回 `**nil**`<br><br>）。|
||`**UNWATCH**`|取消 `**WATCH**`<br><br>命令对所有 key 的监视。|

---

### 一个简单的事务示例

bash

```
127.0.0.1:6379> MULTI          # 开启事务
OK
127.0.0.1:6379> SET name Alice # 命令入队
QUEUED
127.0.0.1:6379> INCR counter   # 命令入队
QUEUED
127.0.0.1:6379> GET name       # 命令入队
QUEUED
127.0.0.1:6379> EXEC           # 执行事务
1) OK                         # SET 命令的返回结果
2) (integer) 1                # INCR 命令的返回结果
3) "Alice"                    # GET 命令的返回结果
```

---

### Redis 事务的三大特性（与ACID的对比）

#### 1. 不保证原子性 (Atomicity)

Redis 事务的原子性指的是：`**EXEC**` 命令会触发所有命令一次性执行完毕，期间不会被其他客户端的命令打断。事务中的所有命令要么全部执行，要么全部不执行（例如使用 `**DISCARD**` 或在 `**WATCH**` 失败时）。

**与传统数据库的区别**：**不保证回滚！** 这是最大的不同。如果事务中的某个命令**执行失败**（例如对错误的数据类型执行了 `**INCR**`），**Redis 不会停止事务并回滚已执行的命令，而是会继续执行后续的命令**。

- bash

```
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379> SET a 1
QUEUED
127.0.0.1:6379> INCR b # 假设 b 的值是字符串 "hello"，无法被 INCR
QUEUED
127.0.0.1:6379> SET c 3
QUEUED
127.0.0.1:6379> EXEC
1) OK          # SET a 1 成功
2) (error) ERR value is not an integer or out of range # INCR b 失败
3) OK          # SET c 3 成功！它继续执行了
```

**结论**：Redis 事务不支持回滚，它只在命令**入队时检查语法错误**（这种错误会导致整个 `**EXEC**` 失败），而**运行时错误**不会影响其他命令。

#### 2. 一致性 (Consistency) 和 隔离性 (Isolation)

- **一致性**：**保证！** 无论是在事务执行前、执行后还是执行中，数据库的完整性约束都不会被破坏。单个命令是原子的，事务以原子方式执行，所以一致性得到了保证。
- **隔离性 (Isolation Level)**：**保证！** Redis 事务是**单线程**执行的，因此它天生就具备**隔离性**。`**EXEC**` 命令执行前，所有命令只是排队；`**EXEC**` 命令执行时，Redis 不会中途处理其他客户端的请求。所以事务中的所有命令看起来就像是一个单独的操作，不会被打断。

#### 3. 持久性 (Durability)

- **取决于配置**：事务的持久性与 Redis 本身的持久化配置（RDB 快照或 AOF 日志）有关，和事务本身无关。如果 Redis 配置了持久化，那么事务执行后的结果就可以被持久化到磁盘。

---

### 高级功能：基于 `**WATCH**` 的乐观锁 (Optimistic Locking)

`**WATCH**` 是 Redis 实现 **CAS（Check-And-Set）** 操作的关键，它使得在并发环境下安全地执行事务成为可能。

**场景**：用户 A 和用户 B 同时想修改同一个账户的余额（`**balance:100**`，初始值为 100）。

**没有** `**WATCH**` **的问题：**

1. 用户 A 读取 `**balance:100**` -> 100。
2. 用户 B 读取 `**balance:100**` -> 100。
3. 用户 A 将其减去 20，设置为 80。
4. 用户 B 也将其减去 30，设置为 70。
5. 结果变成了 70，而不是正确的 100 - 20 - 30 = 50。用户 A 的修改被覆盖了！

**使用** `**WATCH**` **的解决方案：**

bash

```
# 客户端 1
127.0.0.1:6379> WATCH balance:100 # 开始监视这个键
OK
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379> DECRBY balance:100 20 # 在事务中执行操作
QUEUED

# 假设在客户端1 EXEC 之前，客户端2修改了 balance:100
# 客户端 2
127.0.0.1:6379> INCRBY balance:100 50 # 其他客户端修改了被监视的键
(integer) 150

# 客户端 1 继续
127.0.0.1:6379> EXEC # 执行事务时，Redis 发现 balance:100 已被修改
(nil)               # 因此事务执行失败，返回 nil
```

此时，客户端 1 的事务因为 `**WATCH**` 的键被修改而执行失败。应用程序可以捕获这个失败，然后**重试整个逻辑**（重新读取余额、重新 `**WATCH**`、重新计算、重新开启事务），直到成功为止。

---

### 总结：Redis 事务的特点

1. **打包执行**：将多个命令打包，一次性、按顺序执行，不会被中断。
2. **无回滚机制**：**最重要的特点**。事务中某个命令失败，不会影响其他命令的执行。开发者需要在入队前确保命令的正确性。
3. **单线程隔离**：天生保证隔离性，所有命令串行执行。
4. **乐观锁支持**：通过 `**WATCH**` 命令可以实现 CAS 操作，解决并发竞争问题。
5. **不满足原子性（ACID意义上）**：因为失败后无法回滚。

**适用场景**：

- 需要一次性执行多个命令，且不希望中途被其他命令打断。
- 对一批数据做连续的操作（例如先 `**GET**` 再 `**SET**`）。
- 配合 `**WATCH**` 实现乐观锁，用于秒杀、抢购等并发控制场景。

---

# 4.Jedis

## 一、 Jedis 是什么？

Jedis 是一个轻量级、高性能的 Java 客户端，用于与 Redis 服务器进行交互。它提供了对 Redis 命令的完整封装，API 设计非常直观，与 Redis 命令名基本保持一致，是 Java 开发者最常用的 Redis 客户端之一。

**核心特征**：

- **全面**：支持几乎所有 Redis 命令。
- **高效**：提供了连接池（`**JedisPool**`）、管道（`**Pipeline**`）、事务等高级特性。
- **同步**：所有操作默认是同步阻塞的（也支持 `**JedisPubSub**` 进行异步订阅）。
- **线程不安全**：一个 `**Jedis**` 实例不应被多个线程共享。

---

## 二、 快速开始

**添加 Maven 依赖**

```
<dependency>
<groupId>redis.clients</groupId>
<artifactId>jedis</artifactId>
<version>5.1.2</version> <!-- 请使用最新版本 -->
</dependency>
```

**基本使用示例**

```
import redis.clients.jedis.Jedis;

public class JedisDemo {
    public static void main(String[] args) {
        // 1. 创建 Jedis 对象，指定服务器地址和端口
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            // 2. 认证（如果 Redis 服务器设置了密码）
            // jedis.auth("yourpassword");

            // 3. 操作 Redis
            jedis.set("key", "Hello Jedis!");
            String value = jedis.get("key");
            System.out.println(value); // 输出: Hello Jedis!

            // 其他操作，如 List, Hash, Set 等
            jedis.lpush("list", "item1", "item2");
            // ...
        } // 4. 使用 try-with-resources 自动关闭连接
    }
}
```

**关键点**：`**Jedis**` 对象实现了 `**Closeable**` 接口，**使用后必须关闭**以释放网络连接资源。推荐使用 **try-with-resources** 语句。

---

## 三、 核心 API 使用

Jedis 的 API 与 Redis 命令几乎一一对应，非常直观。

**String（字符串）**

- java

```
jedis.set("k1", "v1");
String v = jedis.get("k1");
jedis.mset("k1", "v1", "k2", "v2"); // 批量 set
List<String> values = jedis.mget("k1", "k2"); // 批量 get
jedis.incr("counter"); // 自增
```

**Hash（哈希）**

- java

```
jedis.hset("user:1001", "name", "Alice");
jedis.hset("user:1001", "age", "30");
String name = jedis.hget("user:1001", "name");
Map<String, String> userMap = jedis.hgetAll("user:1001"); // 获取整个 Hash
```

**List（列表）**

- java

```
jedis.lpush("list", "a", "b", "c");
jedis.rpush("list", "d");
List<String> elements = jedis.lrange("list", 0, -1); // 获取所有元素
```

**Set（集合）**

- java

```
jedis.sadd("set", "member1", "member2");
Set<String> members = jedis.smembers("set");
```

**ZSet（有序集合）**

- java

```
jedis.zadd("zset", 100, "member1");
jedis.zadd("zset", 90, "member2");
Set<String> topMembers = jedis.zrange("zset", 0, 1); // 获取排名前2的成员
```

---

## 四、 核心特性与高级用法

##### **1. 连接池 (**`**JedisPool**`**)**

直接创建 `**Jedis**` 实例每次都会建立新的 TCP 连接，性能极差。**生产环境必须使用连接池**。

- **为什么用连接池？**

- 避免频繁创建和销毁连接的开销。
- 控制连接数量，防止资源耗尽。

**使用方法**：

- java

```
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class JedisPoolDemo {
    public static void main(String[] args) {
        // 1. 配置连接池
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(128); // 最大连接数
        poolConfig.setMaxIdle(64);   // 最大空闲连接数
        poolConfig.setMinIdle(10);   // 最小空闲连接数
        poolConfig.setTestOnBorrow(true); // 获取连接时进行有效性测试

        // 2. 创建连接池 (服务器地址, 端口, 超时时间, 密码)
        try (JedisPool jedisPool = new JedisPool(poolConfig, "localhost", 6379, 2000, "yourpassword")) {

            // 3. 从池中获取资源
            try (Jedis jedis = jedisPool.getResource()) {
                // 4. 执行操作
                jedis.set("pooledKey", "pooledValue");
                System.out.println(jedis.get("pooledKey"));
            } // 5. try-with-resources 会将 Jedis 连接返还给池，而不是真正关闭
        } // 6. 应用关闭时，关闭连接池
    }
}
```

**最佳实践**：`**JedisPool**` 应该是**全局单例**的，在应用启动时创建，关闭时销毁。

##### **2. 事务 (**`**Transaction**`**)**

Jedis 的事务通过 `**multi()**` 和 `**exec()**` 方法实现。

```
try (Jedis jedis = jedisPool.getResource()) {
    // 开启事务
    Transaction tx = jedis.multi();

    tx.set("a", "1");
    tx.incr("a"); // 注意：此时命令是排队，不会立即执行，所以无法获取返回值
    tx.get("a");

    // 执行事务，返回一个包含每个命令执行结果的 List
    List<Object> results = tx.exec();
    // results.get(0) -> "OK" (set 的结果)
    // results.get(1) -> 2L   (incr 的结果)
    // results.get(2) -> "2"  (get 的结果)
}
```

**注意**：事务中的命令在 `**exec()**` 前不会执行，所以中间无法获取结果。

##### **3. 管道 (**`**Pipeline**`**)**

用于批量执行大量命令，减少网络 RTT（往返时间），极大提升性能。

```
try (Jedis jedis = jedisPool.getResource()) {
    Pipeline pipeline = jedis.pipelined();

    for (int i = 0; i < 10000; i++) {
        pipeline.set("pkey:" + i, "pvalue:" + i);
        // 或者 pipeline.get("pkey:" + i);
    }

    // 同步执行所有命令并关闭管道。此方法返回一个包含所有命令回复的 List
    List<Object> responses = pipeline.syncAndReturnAll();

    // 如果不需要返回值，只关心是否执行成功，可以使用 sync()
    // pipeline.sync();
}
```

**与事务的区别**：Pipeline 只是将命令打包发送，不保证原子性；而事务保证原子性（一起成功或失败）。

##### **4. 发布订阅 (**`**JedisPubSub**`**)**

用于消息的发布和订阅，是异步的。

java

```
// 订阅者
try (Jedis jedis = jedisPool.getResource()) {
    JedisPubSub subscriber = new JedisPubSub() {
        @Override
        public void onMessage(String channel, String message) {
            System.out.println("Received: " + message + " from channel: " + channel);
        }
        // 还可以重写 onSubscribe, onUnsubscribe 等方法
    };
    // subscribe 方法会阻塞当前线程！
    jedis.subscribe(subscriber, "myChannel");
}

// 发布者（在另一个线程或客户端）
try (Jedis jedis = jedisPool.getResource()) {
    jedis.publish("myChannel", "Hello, PubSub!");
}
```

**注意**：`**subscribe**` 方法会阻塞当前线程，通常需要在一个单独的线程中运行。

---

# 5.springboot整合Redis

## 一、 概述

Spring Boot 通过 `**spring-boot-starter-data-redis**` starter 为 Redis 提供了开箱即用的自动化配置。它底层默认使用 **Lettuce** 作为客户端（也可切换为 Jedis），并提供了两个高度封装的抽象工具：

1. `**RedisTemplate**`：用于通用的 Redis 操作。
2. `**StringRedisTemplate**`：专门用于处理字符串类型数据的 `**RedisTemplate**`。

它们封装了底层的连接管理、序列化等复杂细节，让开发者能更专注于业务逻辑。

---

## 二、 项目搭建与基础配置

#### **1. 引入依赖**

在 `**pom.xml**` 中添加依赖。**Spring Boot 2.x 及以上默认使用 Lettuce**。

```
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<!-- 如果需要使用连接池 (Lettuce 默认使用 commons-pool2) -->
<dependency>
<groupId>org.apache.commons</groupId>
<artifactId>commons-pool2</artifactId>
</dependency>

<!-- 如果你坚持要使用 Jedis (不推荐)，排除 Lettuce 并引入 Jedis -->
<!--
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-data-redis</artifactId>
<exclusions>
<exclusion>
<groupId>io.lettuce</groupId>
<artifactId>lettuce-core</artifactId>
</exclusion>
</exclusions>
</dependency>
<dependency>
<groupId>redis.clients</groupId>
<artifactId>jedis</artifactId>
</dependency>
-->
```

#### **2. 基础配置 (**`**application.yml**`**)**

```
spring:
data:
redis:
# Redis 服务器地址
host: localhost
# Redis 服务器端口
port: 6379
# Redis 数据库索引 (默认是 0)
database: 0
# Redis 访问密码 (如果没有，可以省略)
              password: yourpassword
# 连接超时时间
timeout: 3000ms
# Lettuce 连接池配置 (如果你使用了 commons-pool2)
lettuce:
pool:
# 最大连接数 (默认8，负值表示没有限制)
max-active: 16
# 最大阻塞等待时间 (负值表示没有限制)
max-wait: -1ms
# 最大空闲连接数 (默认8)
           max-idle: 8
# 最小空闲连接数 (默认0)
min-idle: 0
# 如果使用 Jedis，配置如下
# jedis:
#   pool:
#     ... (配置同 lettuce.pool)
```

---

## 三、 核心组件：`RedisTemplate` & `StringRedisTemplate`

Spring Data Redis 的核心是这两个模板类。它们通过 **序列化器（Serializer）** 来处理 Java 对象和 Redis 中存储的二进制数据之间的转换。

- `**RedisTemplate**`：默认使用 **JdkSerializationRedisSerializer**。

- **优点**：可以序列化任何实现了 `**Serializable**` 接口的对象。
- **缺点**：序列化后的二进制数据可读性差，且不同 JVM 之间可能不兼容。

- `**StringRedisTemplate**`：是 `**RedisTemplate<String, String>**` 的子类。

- 它的 key 和 value 序列化器都是 **StringRedisSerializer**。
- **优点**：存入 Redis 的数据是人类可读的字符串，与 Redis CLI 和其他客户端兼容性好。
- **使用场景**：**绝大多数情况下推荐使用它**，除非你需要存储复杂的对象。

#### **1. 直接注入使用**

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/redis")
public class TestController {

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @PostMapping("/set")
    public String setValue(@RequestParam String key, @RequestParam String value) {
        ValueOperations<String, String> ops = stringRedisTemplate.opsForValue();
        ops.set(key, value);
        return "OK";
    }

    @GetMapping("/get/{key}")
    public String getValue(@PathVariable String key) {
        ValueOperations<String, String> ops = stringRedisTemplate.opsForValue();
        return ops.get(key);
    }
}
```

#### **2.** `**RedisTemplate**` **的 opsForXxx() 方法**

这些方法提供了对不同数据类型的操作接口。

|   |   |   |
|---|---|---|
|**操作类型**|**方法**|**返回接口**|
|**String（字符串）**|`**opsForValue()**`|`**ValueOperations<K, V>**`|
|**Hash（哈希）**|`**opsForHash()**`|`**HashOperations<K, HK, HV>**`|
|**List（列表）**|`**opsForList()**`|`**ListOperations<K, V>**`|
|**Set（集合）**|`**opsForSet()**`|`**SetOperations<K, V>**`|
|**ZSet（有序集合）**|`**opsForZSet()**`|`**ZSetOperations<K, V>**`|

**示例：操作 Hash**

```
// 注入 RedisTemplate 或 StringRedisTemplate
@Autowired
private StringRedisTemplate redisTemplate;

public void testHash() {
    HashOperations<String, Object, Object> ops = redisTemplate.opsForHash();
    ops.put("user:1001", "name", "Alice");
    ops.put("user:1001", "age", "30");

    String name = (String) ops.get("user:1001", "name");
    Map<Object, Object> userMap = ops.entries("user:1001");
}
```

---

## 四、 自定义配置（序列化策略）

默认的 JDK 序列化方式不理想，我们通常需要自定义 `**RedisTemplate**` 的序列化器，**推荐使用 JSON 格式（如 Jackson2）**。

#### **自定义 RedisTemplate 配置类**

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {

    /**
     * 自定义 RedisTemplate，配置 JSON 序列化
     * @param factory 连接工厂，由 Spring Boot 自动注入
     * @return 配置好的 RedisTemplate
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);

        // 设置 Key 的序列化器为 StringRedisSerializer
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);

        // 设置 Value 的序列化器为 GenericJackson2JsonRedisSerializer
        GenericJackson2JsonRedisSerializer jsonSerializer = new GenericJackson2JsonRedisSerializer();
        template.setValueSerializer(jsonSerializer);
        template.setHashValueSerializer(jsonSerializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

**使用自定义的 Template：**

```
@Autowired
private RedisTemplate<String, Object> myRedisTemplate; // 注入自定义的 Template

public void testJson() {
    User user = new User("Alice", 30);
    // 存储对象，value 会被序列化为 JSON 字符串
    myRedisTemplate.opsForValue().set("user:1001", user);

    // 取回对象，会自动反序列化
    User cachedUser = (User) myRedisTemplate.opsForValue().get("user:1001");
}
```

**存入 Redis 后的效果：**

```
Key: "user:1001"
Value: "{"@class":"com.example.model.User","name":"Alice","age":30}"
```

_注意：_`**_GenericJackson2JsonRedisSerializer_**` _会在 JSON 中添加_ `**_@class_**` _属性，以便反序列化。这会占用额外空间。如果你能确定类型，可以使用_ `**_Jackson2JsonRedisSerializer(User.class)_**`_。_

---

# 6.高级特性

## 1. 事务支持

Spring Data Redis 提供了与 Spring 声明式事务管理无缝集成的事务支持。

```
@Service
public class TransactionService {

    @Autowired
    private StringRedisTemplate redisTemplate;

    // 使用 @Transactional 注解开启事务
    // 注意：需要启用事务管理，在配置类上添加 @EnableTransactionManagement
    @Transactional
    public void transactionalMethod() {
        redisTemplate.opsForValue().set("key1", "value1");
        redisTemplate.opsForValue().increment("counter", 1);
        // 如果这里发生异常，上面的 set 和 increment 操作都会回滚
        // int i = 1 / 0; // 取消注释测试回滚
    }
}
```

**重要**：Redis 事务与数据库事务不同，它是“**命令打包执行**”，并非真正意义上的原子回滚。Spring 只是确保在事务范围内的所有操作在一个连接中顺序执行。

## 2.持久化RDB和AOF

RDB是**快照式持久化**。它会在**特定的时间间隔**内，将内存中的数据集**完整地生成一个二进制快照文件**（默认名为 `dump.rdb`）。

AOF 是**日志式持久化**。它记录服务器执行的**每一个写操作命令**（例如 `SET`, `SADD`, `LPUSH`），并在服务器启动时通过**重新执行这些命令**来重建原始数据集。

**开启持久化：**

在你的 Redis 服务器上，修改 `redis.conf` 文件。

```
# 1. 启用 RDB
# 保持默认的 save 规则或根据需求调整
save 900 1	# 900秒（15分钟）内至少有1个key被改变
save 300 10		# 300秒（5分钟）内至少有10个key被改变
save 60 10000
dbfilename dump.rdb
dir ./  # 指定 RDB 和 AOF 文件保存的目录，确保有写入权限

# 2. 启用 AOF
appendonly yes          # 这是最关键的一步，将 no 改为 yes
appendfilename "appendonly.aof"
appendfsync everysec    # 推荐使用 everysec

# 其他必要配置（如绑定地址、密码等）
bind 0.0.0.0
requirepass your_strong_password_here
daemonize yes
```

## 3. 发布订阅 (Pub/Sub)

```
// 1. 定义消息监听器
import org.springframework.data.redis.connection.Message;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.stereotype.Component;

@Component
public class MyRedisMessageListener implements MessageListener {
    @Override
    public void onMessage(Message message, byte[] pattern) {
        String channel = new String(message.getChannel());
        String body = new String(message.getBody());
        System.out.println("Received message: " + body + " from channel: " + channel);
    }
}

// 2. 配置监听容器
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.listener.ChannelTopic;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import org.springframework.data.redis.listener.adapter.MessageListenerAdapter;

@Configuration
public class RedisPubSubConfig {

    @Bean
    public RedisMessageListenerContainer container(RedisConnectionFactory connectionFactory,
                                                   MessageListenerAdapter listenerAdapter) {
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        // 订阅频道 "myChannel"
        container.addMessageListener(listenerAdapter, new ChannelTopic("myChannel"));
        return container;
    }

    @Bean
    public MessageListenerAdapter listenerAdapter(MyRedisMessageListener receiver) {
        // 将 receiver 的 onMessage 方法适配为监听器
        return new MessageListenerAdapter(receiver, "onMessage");
    }
}

// 3. 发布消息（在 Service 中）
@Service
public class MessageService {
    @Autowired
    private StringRedisTemplate redisTemplate;

    public void sendMessage(String channel, String message) {
        redisTemplate.convertAndSend(channel, message);
    }
}
```

## 4. 缓存抽象 (`@Cacheable`)

Spring Boot 可以轻松地将 Redis 用作分布式缓存提供商。

1. **开启缓存支持**：在主应用类上添加 `**@EnableCaching**`。

**使用注解**：

```
@Service
public class UserService {

    // 执行方法前，先检查缓存中是否有 key=‘user::’+id 的值，有则直接返回，不执行方法。
    @Cacheable(value = "user", key = "#id")
    public User getUserById(Long id) {
        // 模拟从数据库查询
        System.out.println("Getting user from DB: " + id);
        return new User(id, "User " + id);
    }

    // 方法执行后，更新缓存
    @CachePut(value = "user", key = "#user.id")
    public User updateUser(User user) {
        // ... update DB
        return user;
    }

    // 方法执行后，清除缓存
    @CacheEvict(value = "user", key = "#id")
    public void deleteUserById(Long id) {
        // ... delete from DB
    }
}
```

2. **配置缓存管理器**（通常不需要，Spring Boot 会自动配置 `**RedisCacheManager**`）。

## 5.缓存穿透 (Cache Penetration)

### 什么是缓存穿透？

**缓存穿透**是指查询一个**根本不存在的数据**。由于数据不存在，缓存中自然不会命中，于是请求就会直接穿透缓存，每次都去数据库查询。

**举个栗子** **🌰****：**  
你的系统用户ID是从1000开始的，但有人一直请求查询用户ID为 -1、0、999 的数据。这些ID根本不存在，每次请求都会绕过缓存直接访问数据库。

### 会造成什么后果？

- 如果有人恶意攻击，大量请求不存在的数据，会导致数据库压力巨大，甚至宕机。
- 缓存失去了保护数据库的作用。

### 解决方案：

1. **缓存空对象 (Cache Null Object)**

- 即使查询不到数据，也在缓存中存储一个空值（如：`key: user:999, value: null`），并设置一个较短的过期时间（如30秒）。
- **优点**：实现简单。
- **缺点**：可能会缓存大量无用的key，消耗内存。

2. **布隆过滤器 (Bloom Filter)**

- 在缓存之前，设置一个布隆过滤器。
- **布隆过滤器**是一个很长的二进制向量和一系列随机映射函数。它可以**快速判断一个元素是否绝对不存在于某个集合中**。
- **工作流程**：

1. 将所有可能存在的key（例如所有有效的用户ID）预先加载到布隆过滤器中。
2. 请求到来时，先经过布隆过滤器。
3. 如果过滤器说"这个key肯定不存在"，则直接返回空结果，不再查询缓存和数据库。
4. 如果过滤器说"这个key可能存在"，则继续查询缓存和数据库。

- **优点**：内存占用非常小，效率极高。
- **缺点**：实现稍复杂，有一定的误判率（但只会误判为"可能存在"，不会误判为"肯定不存在"，不影响正确性）。

---

## 6.缓存雪崩 (Cache Avalanche)

### 什么是缓存雪崩？

**缓存雪崩**是指**缓存中大量的key在同一时间点或时间段内过期失效**，导致所有请求瞬间都打到了数据库上，引起数据库压力骤增甚至宕机。

**举个栗子** **🌰****：**  
你的系统中有10万个热点数据，为了数据更新，你设置了它们都在凌晨2点同时过期。一到2点，所有请求这些数据的流量瞬间全部涌向数据库，数据库直接被压垮。就像雪山上的积雪突然崩塌一样， hence the name "雪崩"。

### 会造成什么后果？

- 数据库瞬间承受巨大压力，可能直接崩溃。
- 系统响应变慢或完全不可用。

### 解决方案：

1. **设置随机过期时间**

- 不要让大量的key在同一时间过期。为每个key的过期时间加上一个随机值。
- 例如：原本统一设置1小时过期，改为 `基础过期时间（1小时） + 随机时间（0~300秒）`。
- **这是最简单有效的预防措施**。

2. **永不过期 + 后台更新**

- 缓存数据不设置过期时间。
- 由后台线程或定时任务定期更新缓存。
- **优点**：不会出现大量key同时失效。
- **缺点**：数据一致性延迟，架构更复杂。

3. **熔断降级与限流**

- 使用熔断器（如 Hystrix、Sentinel），当检测到数据库访问量过大或失败率过高时，自动熔断，直接返回降级内容（如默认值、友好提示）。
- 使用限流机制，限制打到数据库的请求数量，保护数据库不被冲垮。

4. **构建高可用缓存集群**

- 使用 Redis 集群或哨兵模式，即使单个缓存节点宕机，也不会导致整个缓存层完全失效。

---

## 7.缓存击穿 (Cache Breakdown)

这里再补充一个容易混淆的概念：**缓存击穿**。

### 什么是缓存击穿？

它是指**某一个非常热点的key**（如明星出轨的新闻）在过期瞬间，有大量的并发请求这个key。这些请求发现缓存过期，都会同时去数据库加载数据，导致数据库瞬间压力巨大。

**注意**：缓存击穿是针对**单个热点key**，而雪崩是针对**大量key**。

### 解决方案：

**使用互斥锁 (Mutex Lock)**

- 当第一个发现缓存过期的请求到达时，它先去获取一个分布式锁（如在Redis中执行 `SETNX` 命令）。
- 获取到锁的线程负责去数据库加载数据并回填缓存。
- 其他没获取到锁的线程等待一小段时间，然后重新从缓存中获取数据。
- 这样可以保证只有一个线程去访问数据库。

---

## 8.集群搭建（主从复制）和哨兵模式

我们将搭建：

- **1 个主节点 (Master)**
- **2 个从节点 (Slave)**
- **3 个哨兵节点 (Sentinel)**（推荐至少3个以实现仲裁）

### 第一步：创建 Docker 网络

powershell

docker network create redis-sentinel-net

### 第二步：搭建主从复制

1. 启动主节点

powershell

```
docker run -d --name redis-master `
  --net redis-sentinel-net `
  -p 6379:6379 `
  redis:latest `
  redis-server `
  --requirepass 123456 `          # 主节点密码
  --masterauth 123456 `           # 主从通信密码
  --appendonly yes
```

2. 启动两个从节点

powershell

```
# 从节点1
docker run -d --name redis-slave1 `
  --net redis-sentinel-net `
  -p 6380:6379 `
  redis:latest `
  redis-server `
  --replicaof redis-master 6379 `  # 指定主节点
  --masterauth 123456 `            # 主从通信密码
  --requirepass 123456 `           # 从节点密码（可选，但建议设置）
  --appendonly yes

# 从节点2  
docker run -d --name redis-slave2 `
  --net redis-sentinel-net `
  -p 6381:6379 `
  redis:latest `
  redis-server `
  --replicaof redis-master 6379 `
  --masterauth 123456 `
  --requirepass 123456 `
  --appendonly yes
```

3. 验证主从复制

powershell

```
# 查看主节点复制信息
docker exec -it redis-master redis-cli -a 123456 info replication
# 应该看到 role:master 和 connected_slaves:2

# 查看从节点复制信息  
docker exec -it redis-slave1 redis-cli -a 123456 info replication
# 应该看到 role:slave 和 master_host:redis-master
```

### 第三步：搭建哨兵集群

1. 创建哨兵配置文件

首先创建一个哨兵配置文件 `sentinel.conf`：

conf

```
port 26379
dir /tmp
sentinel monitor mymaster redis-master 6379 2
sentinel auth-pass mymaster 123456
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
sentinel parallel-syncs mymaster 1
```

**关键配置说明：**

- `sentinel monitor mymaster redis-master 6379 2`: 监控名为 `mymaster` 的主节点，需要2个哨兵同意才进行故障转移
- `sentinel auth-pass mymaster 123456`: 主节点密码
- `down-after-milliseconds 5000`: 5秒无响应认为节点下线
- `failover-timeout 10000`: 故障转移超时时间

2. 启动三个哨兵节点

powershell

```
# 哨兵1
docker run -d --name redis-sentinel1 `
  --net redis-sentinel-net `
  -p 26379:26379 `
  -v ${PWD}/sentinel.conf:/etc/redis/sentinel.conf `
  redis:latest `
  redis-sentinel /etc/redis/sentinel.conf

# 哨兵2
docker run -d --name redis-sentinel2 `
  --net redis-sentinel-net `
  -p 26380:26379 `
  -v ${PWD}/sentinel.conf:/etc/redis/sentinel.conf `
  redis:latest `
  redis-sentinel /etc/redis/sentinel.conf

# 哨兵3
docker run -d --name redis-sentinel3 `
  --net redis-sentinel-net `
  -p 26381:26379 `
  -v ${PWD}/sentinel.conf:/etc/redis/sentinel.conf `
  redis:latest `
  redis-sentinel /etc/redis/sentinel.conf
```

---

## 总结与对比

|   |   |   |   |
|---|---|---|---|
|问题类型|**缓存穿透**|**缓存雪崩**|**缓存击穿**|
|**问题本质**|查询**不存在**的数据|**大量key**同时失效|**单个热点key**失效|
|**攻击性**|可能来自恶意攻击|通常是**设计失误**|通常是**高并发场景**|
|**影响范围**|个别不存在的key|全局性、大量key|单个热点key|
|**解决方案**|1. 缓存空值  <br>2. 布隆过滤器|1. **随机过期时间**  <br>2. 永不过期+后台更新  <br>3. 熔断限流|1. **互斥锁**  <br>2. 永不过期|

---

# 7. 最佳实践与总结

1. **首选** `**StringRedisTemplate**`：除非需要存储复杂对象，否则用它，可读性好。
2. **自定义序列化**：生产环境一定要配置 JSON 序列化，替代默认的 JDK 序列化。
3. **使用连接池**：务必在配置中启用 Lettuce 或 Jedis 的连接池。
4. **清晰定义 Key**：使用冒号 `**:**` 来构造有层次的键名（如 `**user:1001:profile**`），这是一种命名约定，便于管理。
5. **注意事务的局限性**：理解 Redis 事务是“批量执行”而非“回滚”。
6. **Pipeline for Batch**：如果需要执行大量操作，可以考虑使用底层的 `**RedisTemplate.executePipelined**` 方法进行管道操作来提升性能。
7. **缓存Null值**：注意 `**@Cacheable**` 可能会缓存空值，可通过 `**unless = "#result == null"**` 条件来避免。

---