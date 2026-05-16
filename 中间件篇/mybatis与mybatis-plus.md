# MyBatis 与 MyBatis-Plus

## 一、MyBatis 概述

### 什么是 MyBatis

**MyBatis** 是一个半自动 ORM（Object Relational Mapping）框架，通过 XML 或注解将 Java 对象与 SQL 语句映射起来。

```
┌──────────────┐      SQL 映射      ┌──────────────┐
│   Java 对象   │  ◄───────────────  │   数据库      │
│  (POJO/DTO)  │                   │  (MySQL/PG)  │
└──────────────┘                   └──────────────┘
         │                               ▲
         │  MyBatis 框架                  │
         ▼                               │
    SqlSession ———→ Mapper XML/注解 ——————┘
```

### 核心组件

| 组件 | 作用 |
|:----:|:----|
| **SqlSessionFactory** | 全局唯一工厂，负责创建 SqlSession |
| **SqlSession** | 会话对象，执行 SQL、管理事务 |
| **Mapper** | 映射接口，定义数据库操作方法 |
| **Mapper XML** | SQL 映射文件，写 SQL 和结果映射 |
| **Configuration** | 核心配置（数据源、别名、插件等） |

### 第一个项目

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.16</version>
</dependency>
```

```xml
<!-- mybatis-config.xml -->
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
    PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
    "https://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/demo"/>
                <property name="username" value="root"/>
                <property name="password" value="root"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="mapper/UserMapper.xml"/>
    </mappers>
</configuration>
```

```java
// 传统方式
String resource = "mybatis-config.xml";
InputStream inputStream = Resources.getResourceAsStream(resource);
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

try (SqlSession session = sqlSessionFactory.openSession()) {
    UserMapper mapper = session.getMapper(UserMapper.class);
    User user = mapper.findById(1L);
}
```

### Spring Boot 整合

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>
```

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: root

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.demo.entity
  configuration:
    map-underscore-to-camel-case: true  # 下划线→驼峰
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

---

## 二、XML 映射

### 基本映射

```xml
<mapper namespace="com.demo.mapper.UserMapper">

    <!-- ⭐ 简单查询 -->
    <select id="findById" resultType="User">
        SELECT * FROM user WHERE id = #{id}
    </select>

    <!-- ⭐ 参数传递 -->
    <select id="findByNameAndEmail" resultType="User">
        SELECT * FROM user
        WHERE name = #{name} AND email = #{email}
    </select>

    <!-- ⭐ 插入并返回自增主键 -->
    <insert id="insert" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO user(name, email, age)
        VALUES(#{name}, #{email}, #{age})
    </insert>

    <!-- ⭐ 更新 -->
    <update id="update">
        UPDATE user SET name = #{name}, email = #{email}
        WHERE id = #{id}
    </update>

    <!-- ⭐ 删除 -->
    <delete id="deleteById">
        DELETE FROM user WHERE id = #{id}
    </delete>

</mapper>
```

### 结果映射（resultMap）⭐

```xml
<!-- ⭐ 当数据库字段名和 Java 属性名不一致时用 resultMap -->
<resultMap id="userResultMap" type="User">
    <id property="id" column="user_id"/>
    <result property="name" column="user_name"/>
    <result property="email" column="email_address"/>
    <result property="createTime" column="create_time"/>
</resultMap>

<select id="findById" resultMap="userResultMap">
    SELECT * FROM user WHERE user_id = #{id}
</select>
```

### 复杂结果映射

```xml
<!-- ⭐ 一对一关联 -->
<resultMap id="orderWithUserMap" type="Order">
    <id property="id" column="id"/>
    <result property="total" column="total"/>

    <association property="user" javaType="User">
        <id property="id" column="user_id"/>
        <result property="name" column="user_name"/>
    </association>
</resultMap>

<!-- ⭐ 一对多关联 -->
<resultMap id="userWithOrdersMap" type="User">
    <id property="id" column="id"/>
    <result property="name" column="name"/>

    <collection property="orders" ofType="Order">
        <id property="id" column="order_id"/>
        <result property="total" column="total"/>
    </collection>
</resultMap>

<!-- ⭐ 延迟加载 -->
<resultMap id="userLazyMap" type="User">
    <id property="id" column="id"/>
    <result property="name" column="name"/>
    <!-- 设置 fetchType="lazy"，访问 orders 时才查数据库 -->
    <collection property="orders" ofType="Order"
                select="com.demo.mapper.OrderMapper.findByUserId"
                column="id" fetchType="lazy"/>
</resultMap>
```

配置全局延迟加载：
```yaml
mybatis:
  configuration:
    lazy-loading-enabled: true
    aggressive-lazy-loading: false  # 按需加载而非全部加载
```

---

## 三、动态 SQL ⭐

### if

```xml
<select id="findByCondition" resultType="User">
    SELECT * FROM user WHERE 1=1
    <if test="name != null and name != ''">
        AND name LIKE CONCAT('%', #{name}, '%')
    </if>
    <if test="email != null and email != ''">
        AND email = #{email}
    </if>
    <if test="age != null">
        AND age = #{age}
    </if>
</select>
```

### where

```xml
<!-- ⭐ <where> 自动处理 AND/OR 前缀，省去 WHERE 1=1 -->
<select id="findByCondition" resultType="User">
    SELECT * FROM user
    <where>
        <if test="name != null and name != ''">
            AND name LIKE CONCAT('%', #{name}, '%')
        </if>
        <if test="email != null and email != ''">
            AND email = #{email}
        </if>
    </where>
</select>
```

### set

```xml
<!-- ⭐ <set> 自动处理 UPDATE 逗号 -->
<update id="updateSelective">
    UPDATE user
    <set>
        <if test="name != null">name = #{name},</if>
        <if test="email != null">email = #{email},</if>
        <if test="age != null">age = #{age},</if>
    </set>
    WHERE id = #{id}
</update>
```

### foreach

```xml
<!-- ⭐ IN 查询 -->
<select id="findByIds" resultType="User">
    SELECT * FROM user WHERE id IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>

<!-- ⭐ 批量插入 -->
<insert id="batchInsert">
    INSERT INTO user(name, email, age) VALUES
    <foreach collection="list" item="user" separator=",">
        (#{user.name}, #{user.email}, #{user.age})
    </foreach>
</insert>
```

### choose/when/otherwise

```xml
<!-- ⭐ 类似 Java 的 switch-case -->
<select id="findByCondition" resultType="User">
    SELECT * FROM user
    <where>
        <choose>
            <when test="name != null">
                AND name = #{name}
            </when>
            <when test="email != null">
                AND email = #{email}
            </when>
            <otherwise>
                AND status = 'ACTIVE'
            </otherwise>
        </choose>
    </where>
</select>
```

### trim

```xml
<!-- ⭐ trim 自定义前缀/后缀，灵活替代 where/set -->
<select id="findByCondition" resultType="User">
    SELECT * FROM user
    <trim prefix="WHERE" prefixOverrides="AND |OR ">
        <if test="name != null"> AND name = #{name}</if>
        <if test="email != null"> OR email = #{email}</if>
    </trim>
</select>
```

---

## 四、注解方式

### 基本 CRUD

```java
public interface UserMapper {

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(Long id);

    @Select("SELECT * FROM user WHERE name LIKE CONCAT('%', #{name}, '%')")
    List<User> findByName(String name);

    @Insert("INSERT INTO user(name, email, age) VALUES(#{name}, #{email}, #{age})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);

    @Update("UPDATE user SET name = #{name} WHERE id = #{id}")
    int update(User user);

    @Delete("DELETE FROM user WHERE id = #{id}")
    int deleteById(Long id);

}
```

### 注解复杂映射

```java
@Results(id = "userMap", value = {
    @Result(property = "id", column = "id", id = true),
    @Result(property = "name", column = "name"),
    @Result(property = "email", column = "email"),
    @Result(property = "createTime", column = "create_time"),
})
@Select("SELECT * FROM user WHERE id = #{id}")
User findById(Long id);

// 复用 @Results
@ResultMap("userMap")
@Select("SELECT * FROM user WHERE name = #{name}")
User findByName(String name);
```

> [!tip] **XML vs 注解**
> - **简单 SQL**：用注解，代码简洁
> - **复杂 SQL / 动态 SQL / 复杂结果映射**：用 XML
> - **最佳实践**：两者可混用，根据复杂度选择

---

## 五、缓存机制

### 一级缓存（SqlSession 级别）

```java
// ⭐ 默认开启，同一个 SqlSession 内共享
try (SqlSession session = factory.openSession()) {
    UserMapper mapper = session.getMapper(UserMapper.class);

    User u1 = mapper.findById(1L);  // 查询数据库
    User u2 = mapper.findById(1L);  // ⭐ 命中缓存，不查库

    System.out.println(u1 == u2);   // true（同一对象）
}
```

一级缓存失效场景：
- 执行了 `commit` / `rollback` / `close`
- 执行了任何 DML（`INSERT`/`UPDATE`/`DELETE`）
- 跨 SqlSession

### 二级缓存（Mapper 级别）

```xml
<!-- mybatis-config.xml -->
<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
    </settings>
</configuration>
```

```xml
<!-- UserMapper.xml — 开启二级缓存 -->
<mapper namespace="com.demo.mapper.UserMapper">
    <cache/>
    <!-- 或者更精细的配置 -->
    <cache
        eviction="LRU"          <!-- 淘汰策略 -->
        flushInterval="60000"   <!-- 刷新间隔（毫秒） -->
        size="512"              <!-- 缓存引用数量 -->
        readOnly="true"/>       <!-- 只读模式 -->
</mapper>
```

```java
// 实体类需要实现 Serializable
public class User implements Serializable {
    private static final long serialVersionUID = 1L;
    // ...
}
```

> [!warning] **二级缓存注意事项**
> - 跨 SqlSession 共享，适用于**查询多、修改少**的场景
> - 查询结果必须实现 `Serializable`
> - 多个 Mapper 关联查询时可能产生脏数据
> - **生产环境常用 Redis 替代 MyBatis 二级缓存**

### 自定义缓存（Redis 整合）

```xml
<cache type="org.mybatis.caches.redis.RedisCache"/>
```

```xml
<dependency>
    <groupId>org.mybatis.caches</groupId>
    <artifactId>mybatis-redis</artifactId>
    <version>1.0.0-beta2</version>
</dependency>
```

---

## 六、插件机制（Interceptor）

### PageHelper 分页 ⭐

```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>2.1.0</version>
</dependency>
```

```java
// ⭐ 分页——在查询前调用 PageHelper.startPage
PageHelper.startPage(pageNum, pageSize);
List<User> list = userMapper.findAll();

// 包装为 PageInfo（包含总页数、总数等）
PageInfo<User> pageInfo = new PageInfo<>(list);

pageInfo.getTotal();       // 总记录数
pageInfo.getPages();       // 总页数
pageInfo.getPageNum();     // 当前页
pageInfo.getList();        // 当前页数据
```

### 自定义插件

```java
// ⭐ MyBatis 插件拦截器（基于 JDK 动态代理）
@Intercepts({
    @Signature(
        type = Executor.class,
        method = "query",
        args = {MappedStatement.class, Object.class,
                RowBounds.class, ResultHandler.class}
    )
})
public class SqlLogPlugin implements Interceptor {

    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = invocation.proceed();
        long elapsed = System.currentTimeMillis() - start;

        MappedStatement ms = (MappedStatement) invocation.getArgs()[0];
        System.out.println("[SQL] " + ms.getId() + " - 耗时: " + elapsed + "ms");
        return result;
    }

    @Override
    public Object plugin(Object target) {
        return Plugin.wrap(target, this);
    }
}
```

```xml
<plugins>
    <plugin interceptor="com.demo.plugin.SqlLogPlugin"/>
</plugins>
```

---

## 七、MyBatis-Plus 概述 ⭐

### 什么是 MyBatis-Plus

**MyBatis-Plus** 是 MyBatis 的增强工具，**只增强不修改**，在 MyBatis 的基础上提供了强大的 CRUD、分页、条件构造器等能力。

```
                        MyBatis 做的事
    ┌─────────────────────────────────────────────┐
    │  写 Mapper XML / 注解 → 手动 CRUD            │
    └─────────────────────────────────────────────┘
                        +
    ┌─────────────────────────────────────────────┐
    │  BaseMapper — 内置通用 CRUD                   │
    │  QueryWrapper/LambdaQueryWrapper — 条件构造  │
    │  Page — 自动分页                             │
    │  ️ 代码生成器 — 一键生成实体/Mapper/Service   │
    └─────────────────────────────────────────────┘
                    MyBatis-Plus 增强的事
```

### 快速开始

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
    <version>3.5.9</version>
</dependency>
```

```java
// ⭐ 实体类
@Data
@TableName("user")  // 指定表名，默认类名下划线转表名
public class User {
    @TableId(type = IdType.AUTO)  // 自增主键
    private Long id;

    private String name;
    private String email;
    private Integer age;

    @TableField(fill = FieldFill.INSERT)  // 自动填充
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    @TableLogic  // 逻辑删除
    private Integer deleted;
}

// ⭐ Mapper——只需继承 BaseMapper
@Mapper
public interface UserMapper extends BaseMapper<User> {
    // 无需写任何方法，BaseMapper 提供了 20+ CRUD 方法
}

// ⭐ Service
public interface UserService extends IService<User> { }

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User>
        implements UserService { }
```

### 基础 CRUD

```java
@Autowired
private UserMapper userMapper;

// ⭐ BaseMapper 内置方法
User user = userMapper.selectById(1L);
List<User> list = userMapper.selectList(null);
List<User> list = userMapper.selectBatchIds(Arrays.asList(1L, 2L, 3L));
int count = userMapper.selectCount(null);

User user = new User();
user.setName("张三");
user.setEmail("zhangsan@example.com");
userMapper.insert(user);  // ⭐ 自动回填 id

user.setName("李四");
userMapper.updateById(user);

userMapper.deleteById(1L);
userMapper.deleteBatchIds(Arrays.asList(1L, 2L));
```

### Service CRUD

```java
@Autowired
private UserService userService;

// ⭐ IService 内置方法
User user = userService.getById(1L);
List<User> list = userService.list();
boolean saved = userService.save(user);
boolean updated = userService.updateById(user);
boolean removed = userService.removeById(1L);
boolean savedBatch = userService.saveBatch(userList);
```

---

## 八、条件构造器（Wrapper）⭐

### QueryWrapper

```java
// ⭐ QueryWrapper——最常用条件构造器
QueryWrapper<User> wrapper = new QueryWrapper<>();

// 等值查询
wrapper.eq("name", "张三");

// 模糊查询
wrapper.like("email", "example");

// 范围查询
wrapper.between("age", 18, 60);
wrapper.ge("age", 18);   // >=
wrapper.le("age", 60);   // <=

// 排序
wrapper.orderByDesc("create_time");

// 分组
wrapper.groupBy("status");
wrapper.having("count(*) > 1");

// 子查询
wrapper.inSql("id", "SELECT user_id FROM order WHERE total > 100");

// 链式调用
List<User> list = userMapper.selectList(
    new QueryWrapper<User>()
        .eq("name", "张三")
        .like("email", "example")
        .orderByDesc("id")
);

// 只查询特定列
QueryWrapper<User> wrapper = new QueryWrapper<>();
wrapper.select("id", "name", "email");
```

### LambdaQueryWrapper ⭐

```java
// ⭐ LambdaQueryWrapper——避免硬编码列名（推荐）
LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();

wrapper.eq(User::getName, "张三");
wrapper.like(User::getEmail, "example");
wrapper.between(User::getAge, 18, 60);
wrapper.orderByDesc(User::getCreateTime);

List<User> list = userMapper.selectList(wrapper);
```

### UpdateWrapper

```java
// ⭐ UpdateWrapper —— 带条件的更新
UpdateWrapper<User> wrapper = new UpdateWrapper<>();
wrapper.set("email", "new@example.com")
       .set("age", 25)
       .eq("name", "张三");

userMapper.update(null, wrapper);

// 或 Lambda 方式
LambdaUpdateWrapper<User> wrapper = new LambdaUpdateWrapper<>();
wrapper.set(User::getEmail, "new@example.com")
       .eq(User::getName, "张三");
userMapper.update(null, wrapper);
```

### 复杂条件组合

```java
// ⭐ and / or 嵌套
LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(User::getStatus, "ACTIVE")
       .and(w -> w.like(User::getName, "张")
                   .or()
                   .like(User::getName, "李"))
       .or()
       .eq(User::getAge, 18);

// SQL: WHERE status = 'ACTIVE'
//      AND (name LIKE '%张%' OR name LIKE '%李%')
//      OR age = 18
```

### 分页查询

```java
// ⭐ 配置分页插件
@Configuration
public class MyBatisPlusConfig {
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(
            new PaginationInnerInterceptor(DbType.MYSQL)
        );
        return interceptor;
    }
}

// ⭐ 分页查询
Page<User> page = new Page<>(1, 10);  // 第1页，每页10条
Page<User> result = userMapper.selectPage(page, null);

result.getTotal();      // 总记录数
result.getPages();      // 总页数
result.getCurrent();    // 当前页
result.getRecords();    // 数据列表
result.hasPrevious();   // 是否有上一页
result.hasNext();       // 是否有下一页

// ⭐ 自定义 SQL 分页（在 Mapper 中）
@Mapper
public interface UserMapper extends BaseMapper<User> {

    IPage<User> selectUserPage(Page<User> page, @Param("name") String name);
}

<!-- UserMapper.xml -->
<select id="selectUserPage" resultType="User">
    SELECT * FROM user
    <where>
        <if test="name != null and name != ''">
            AND name LIKE CONCAT('%', #{name}, '%')
        </if>
    </where>
</select>
```

---

## 九、自动填充与乐观锁

### 自动填充 ⭐

```java
// ⭐ 实体类配置
@Data
public class User {
    // ...

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    @TableField(fill = FieldFill.INSERT)
    private String createBy;
}

// ⭐ 实现 MetaObjectHandler
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {

    @Override
    public void insertFill(MetaObject metaObject) {
        this.strictInsertFill(metaObject, "createTime",
            LocalDateTime.class, LocalDateTime.now());
        this.strictInsertFill(metaObject, "updateTime",
            LocalDateTime.class, LocalDateTime.now());
        this.strictInsertFill(metaObject, "createBy",
            String.class, "system");
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        this.strictUpdateFill(metaObject, "updateTime",
            LocalDateTime.class, LocalDateTime.now());
    }
}
```

### 乐观锁 ⭐

```java
// ⭐ 实体类添加 @Version
@Data
public class User {
    // ...
    @Version
    @TableField(fill = FieldFill.INSERT)
    private Integer version;
}

// ⭐ 更新时 version 自动 +1，CAS 机制防并发覆盖
// UPDATE user SET name = ?, version = version + 1
// WHERE id = ? AND version = oldVersion
```

配置乐观锁插件：
```java
@Bean
public MybatisPlusInterceptor mybatisPlusInterceptor() {
    MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
    interceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
    return interceptor;
}
```

### 逻辑删除

```java
// ⭐ 实体类
@Data
public class User {
    // ...
    @TableLogic  // 逻辑删除标记
    private Integer deleted;  // 0=正常, 1=删除
}

// 配置
mybatis-plus:
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
```

开启后，MyBatis-Plus 会自动：
- **查询时**追加：`WHERE deleted = 0`
- **删除时**执行：`UPDATE user SET deleted = 1 WHERE id = ?`

---

## 十、代码生成器 ⭐

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-generator</artifactId>
    <version>3.5.9</version>
</dependency>
<dependency>
    <groupId>org.apache.velocity</groupId>
    <artifactId>velocity-engine-core</artifactId>
    <version>2.3</version>
</dependency>
```

```java
// ⭐ 一键生成 Entity / Mapper / Service / Controller
FastAutoGenerator.create("jdbc:mysql://localhost:3306/demo",
                         "root", "root")
    .globalConfig(builder -> builder
        .author("开发者")
        .outputDir("src/main/java")
        .enableSwagger()
    )
    .packageConfig(builder -> builder
        .parent("com.demo")
        .entity("entity")
        .mapper("mapper")
        .service("service")
        .controller("controller")
    )
    .strategyConfig(builder -> builder
        .addInclude("user", "order", "product")  // 表名
        .addTablePrefix("t_", "sys_")             // 表前缀过滤
        .entityBuilder()
            .enableLombok()
            .enableTableFieldAnnotation()
        .controllerBuilder()
            .enableRestStyle()  // @RestController
    )
    .execute();
```

> [!tip] 也可使用 MyBatisX 插件（IDEA）图形化生成

---

## 十一、多数据源

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>dynamic-datasource-spring-boot3-starter</artifactId>
    <version>4.3.1</version>
</dependency>
```

```yaml
spring:
  datasource:
    dynamic:
      primary: master  # 默认数据源
      strict: false    # 严格模式
      datasource:
        master:
          url: jdbc:mysql://localhost:3306/db_master
          username: root
          password: root
          driver-class-name: com.mysql.cj.jdbc.Driver
        slave_1:
          url: jdbc:mysql://localhost:3306/db_slave_1
          username: root
          password: root
          driver-class-name: com.mysql.cj.jdbc.Driver
        slave_2:
          url: jdbc:mysql://localhost:3306/db_slave_2
          username: root
          password: root
          driver-class-name: com.mysql.cj.jdbc.Driver
```

```java
// ⭐ 使用 @DS 切换数据源
@Service
@DS("master")  // 默认走主库
public class UserServiceImpl extends ServiceImpl<UserMapper, User>
        implements UserService {

    @Override
    @DS("slave_1")  // 读操作走从库
    public List<User> list() {
        return baseMapper.selectList(null);
    }

    @Override
    @DS("master")   // 写操作走主库
    public boolean save(User user) {
        return baseMapper.insert(user) > 0;
    }
}
```

---

## 十二、MyBatis vs MyBatis-Plus 对比

| 对比维度 | MyBatis | MyBatis-Plus |
|:--------:|:-------:|:------------:|
| **CRUD 方法** | 需手动编写 | BaseMapper 内置 20+ 方法 |
| **条件查询** | 手写 XML 动态 SQL | QueryWrapper / LambdaQueryWrapper |
| **分页** | PageHelper 或手写 | Page 插件，自动拦截 |
| **代码生成** | MyBatis Generator | 更强大的生成器 |
| **自动填充** | 需自定义插件 | @TableField(fill = ...) |
| **乐观锁** | 手写 version 逻辑 | @Version + 插件 |
| **逻辑删除** | 手写 SQL 过滤 | @TableLogic + 自动过滤 |
| **多数据源** | 手动配置多个 SqlSessionFactory | @DS 注解切换 |
| **学习成本** | 较高（需写 XML） | 低（开箱即用） |
| **灵活性** | 完全控制 SQL | 约定大于配置 |

---

## 十三、常见面试题

### 1. #{} 和 ${} 有什么区别？

> `#{}` 使用**预编译**（`PreparedStatement`），会加引号并防 SQL 注入。`${}` 是**字符串替换**，存在注入风险。`ORDER BY` / `表名` 等不能加引号的场景才用 `${}`。

### 2. MyBatis 的一级缓存和二级缓存原理？

> 一级缓存是 **SqlSession 级别**（Map 结构），默认开启。二级缓存是 **Mapper 级别**（namespace 共享），需手动开启，实体需实现 `Serializable`。二级缓存底层也是一个 Map，生产环境建议替换为 **Redis**。

### 3. 什么是 MyBatis 的插件原理？

> MyBatis 插件基于 **JDK 动态代理**，可以拦截 `Executor`、`StatementHandler`、`ParameterHandler`、`ResultSetHandler` 这四个核心对象的创建。分页插件 PageHelper 就使用了此机制。

### 4. MyBatis-Plus 的条件构造器是如何防止 SQL 注入的？

> `QueryWrapper` 里传的**列名是硬编码字符串**（或 Lambda 引用），**值部分始终使用 `#{}` 预编译**，不会拼接到 SQL 中。LambdaQueryWrapper 更进一步，用 Lambda 方法引用替代列名字符串，避免列名拼写错误。

### 5. MyBatis-Plus 和 MyBatis 可以混用吗？

> **可以。** MyBatis-Plus 只增强不修改，`BaseMapper` 提供了通用 CRUD，自定义复杂查询仍然可以写 XML 或用注解。两者在同一个项目中完全兼容。

### 6. 分页插件原理？

> MyBatis-Plus 的 `PaginationInnerInterceptor` 拦截 `Executor.query()`，在执行前自动拼装 `COUNT` 查询和分页参数（`LIMIT`），对业务代码完全无侵入。

---

> [!tip] **学习路径建议**
> 1. **入门**：MyBatis XML 映射 → 基本 CRUD → 整合 Spring Boot
> 2. **进阶**：动态 SQL → resultMap 复杂映射 → 缓存机制
> 3. **升级**：MyBatis-Plus BaseMapper → Wrapper 条件构造器 → 分页插件
> 4. **深入**：自动填充 → 乐观锁 → 逻辑删除 → 多数据源
> 5. **工程化**：代码生成器 → 插件开发 → 性能优化
