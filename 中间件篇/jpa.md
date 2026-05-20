# JPA

## 一、JPA 概述

### 什么是 JPA

**JPA**（Java Persistence API）是 Java 官方的 **ORM 规范**，定义了对象与关系数据库的映射标准。Hibernate 是 JPA 最主流的实现。

```
    JPA（规范）
        │
        ├── Hibernate（最主流实现）
        ├── EclipseLink
        └── OpenJPA

    Spring Data JPA
        │
        └── 对 JPA 的更高层抽象（Spring 生态）
```

### 核心注解速览

| 注解 | 用途 |
|:----|:-----|
| `@Entity` | 标记实体类 |
| `@Table` | 指定映射的表名 |
| `@Id` | 主键 |
| `@GeneratedValue` | 主键生成策略 |
| `@Column` | 列映射 |
| `@Transient` | 非持久化字段 |
| `@Enumerated` | 枚举映射 |
| `@Temporal` | 日期类型映射 |
| `@Lob` | 大字段（CLOB/BLOB） |

### Spring Boot 整合

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>
```

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: update          # ⭐ 自动建表/更新表结构
    show-sql: true              # 控制台显示 SQL
    properties:
      hibernate:
        format_sql: true        # 格式化 SQL
        highlight_sql: true     # 高亮 SQL
        use_sql_comments: true  # 显示 SQL 注释
    open-in-view: false         # 关闭 OSIV（生产推荐）
```

> [!warning] **ddl-auto 选项**
> | 值 | 行为 | 适用场景 |
> |:--:|:----|:--------|
> | `none` | 不做任何操作 | 生产环境 |
> | `validate` | 验证实体与表结构是否一致 | 生产环境 |
> | `update` | 自动更新表结构 | 开发环境 |
> | `create` | 每次启动删表重建 | 测试/开发 |
> | `create-drop` | 启动创建，关闭删除 | 集成测试 |

---

## 二、实体映射 ⭐

### 基本实体

```java
@Entity                                         // 标记为 JPA 实体
@Table(name = "sys_user")                        // 指定表名（省略则类名）
@Data                                           // Lombok
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id                                         // ⭐ 主键
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // 自增主键
    private Long id;

    @Column(name = "user_name", nullable = false, length = 50)
    private String name;

    @Column(unique = true)                       // 唯一约束
    private String email;

    @Column(nullable = false)
    private Integer age;

    @Column(updatable = false)                   // 创建后不可修改
    private LocalDateTime createTime;

    @Transient                                   // ⭐ 不持久化到数据库
    private String tempField;
}
```

### @Column 详解

```java
@Column(
    name = "user_name",       // 列名（默认 = 属性名）
    nullable = false,         // 是否允许 null
    unique = false,           // 是否唯一
    length = 100,             // 字符串长度（默认 255）
    precision = 10,           // decimal 精度
    scale = 2,                // decimal 小数位数
    updatable = true,         // 是否可更新
    insertable = true,        // 是否可插入
    columnDefinition = "VARCHAR(100) COMMENT '用户名'"  // 自定义 DDL
)
private String name;
```

### 主键生成策略

```java
// ⭐ 四种主键策略
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)   // 自增（MySQL 推荐）
// @GeneratedValue(strategy = GenerationType.SEQUENCE) // 序列（Oracle 推荐）
// @GeneratedValue(strategy = GenerationType.TABLE)    // 表模拟序列（不推荐）
// @GeneratedValue(strategy = GenerationType.AUTO)     // JPA 自动选择（默认）

// ⭐ UUID 主键
@Id
@GeneratedValue(generator = "uuid2")
@GenericGenerator(name = "uuid2", strategy = "uuid2")
@Column(length = 36)
private String id;

// ⭐ 雪花算法 ID
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
// 或使用自定义 ID 生成器（如雪花算法）
```

### 日期映射

```java
// ⭐ Java 8 时间类型——JPA 2.2+ 自动支持
private LocalDate date;          // 日期：2024-01-15
private LocalTime time;          // 时间：14:30:00
private LocalDateTime dateTime;  // 日期时间：2024-01-15T14:30:00

// ⭐ 旧版 Date 需要 @Temporal
@Temporal(TemporalType.DATE)           // java.sql.Date
@Temporal(TemporalType.TIME)           // java.sql.Time
@Temporal(TemporalType.TIMESTAMP)      // java.sql.Timestamp
private Date createdAt;
```

### 枚举映射

```java
public enum UserStatus {
    ACTIVE, INACTIVE, BANNED
}

public enum UserRole {
    ADMIN("管理员"),
    USER("普通用户"),
    GUEST("访客");

    private final String desc;
    UserRole(String desc) { this.desc = desc; }
}
```

```java
@Entity
public class User {
    // ⭐ 枚举映射方式

    @Enumerated(EnumType.ORDINAL)     // 存序号：0, 1, 2（不推荐——增删枚举会乱序）
    private UserStatus status;

    @Enumerated(EnumType.STRING)      // ⭐ 存字符串：ACTIVE, INACTIVE（推荐）
    private UserRole role;
}
```

---

## 三、关联关系映射 ⭐

### @OneToOne（一对一）

```java
// ⭐ 用户 → 身份证（一对一）
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL,
              fetch = FetchType.LAZY)
    private IDCard idCard;
}

@Entity
public class IDCard {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String cardNumber;

    @OneToOne
    @JoinColumn(name = "user_id")     // 外键在 IDCard 表
    private User user;
}
```

### @OneToMany / @ManyToOne（一对多 / 多对一）⭐

```java
// ⭐ 用户 → 订单（一对多）
@Entity
public class User {
    @Id
    private Long id;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL,
               fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();
}

// ⭐ 订单 → 用户（多对一）
@Entity
@Table(name = "orders")
public class Order {
    @Id
    private Long id;

    private BigDecimal total;

    @ManyToOne(fetch = FetchType.LAZY)   // ⭐ 多对一默认 EAGER，建议改为 LAZY
    @JoinColumn(name = "user_id")         // 外键在 Order 表
    private User user;
}
```

### @ManyToMany（多对多）

```java
// ⭐ 用户 → 角色（多对多）
@Entity
public class User {
    @Id
    private Long id;

    @ManyToMany
    @JoinTable(
        name = "user_role",                 // 中间表名
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<Role> roles = new HashSet<>();
}

@Entity
public class Role {
    @Id
    private Long id;

    private String name;

    @ManyToMany(mappedBy = "roles")
    private Set<User> users = new HashSet<>();
}
```

### Cascade 与 Fetch ⭐

```java
// ⭐ CascadeType——级联操作
@OneToMany(cascade = {
    CascadeType.PERSIST,   // 级联保存
    CascadeType.MERGE,     // 级联更新
    CascadeType.REMOVE,    // 级联删除
    CascadeType.REFRESH,   // 级联刷新
    CascadeType.DETACH,    // 级联分离
    CascadeType.ALL        // 全部（谨慎使用）
})

// ⭐ FetchType——加载策略
FetchType.LAZY    // 延迟加载（推荐：用到时才查数据库）
FetchType.EAGER   // 立即加载（联表查询，可能影响性能）
```

> [!tip] **关联关系最佳实践**
> - **FetchType**：`@ManyToOne` 和 `@OneToOne` 默认 EAGER，建议手动改为 LAZY
> - **Cascade**：`CascadeType.ALL` 谨慎使用，尤其不要从父级 cascade REMOVE
> - **双向关联**：`mappedBy` 只在"被拥有方"使用
> - **集合初始化**：`= new ArrayList<>()` 防止 NPE

---

## 四、Spring Data JPA ⭐

### 核心接口

```java
// ⭐ 继承 JpaRepository——获得 CRUD、分页、排序等能力
public interface UserRepository extends JpaRepository<User, Long> {

    // 继承的方法：
    // save(entity)         — 保存/更新
    // findById(id)         — 按 ID 查询
    // findAll()            — 查询全部
    // findAll(Sort)        — 排序查询
    // findAll(Pageable)    — 分页查询
    // count()              — 计数
    // deleteById(id)       — 按 ID 删除
    // existsById(id)       — 是否存在
}
```

### 方法命名查询 ⭐

```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ⭐ 方法命名规则——Spring Data JPA 最强大的特性
    Optional<User> findByEmail(String email);

    List<User> findByName(String name);

    List<User> findByNameAndEmail(String name, String email);

    List<User> findByNameOrEmail(String name, String email);

    List<User> findByNameLike(String namePattern);

    List<User> findByNameStartingWith(String prefix);

    List<User> findByNameEndingWith(String suffix);

    List<User> findByNameContaining(String keyword);

    List<User> findByAgeBetween(Integer min, Integer max);

    List<User> findByAgeLessThan(Integer age);

    List<User> findByAgeGreaterThanEqual(Integer age);

    List<User> findByCreateTimeAfter(LocalDateTime date);

    List<User> findByStatusIn(List<UserStatus> statuses);

    List<User> findByNameIgnoreCase(String name);       // 忽略大小写

    List<User> findByEmailNotNull();                    // IS NOT NULL

    List<User> findTop10ByOrderByCreateTimeDesc();      // 前 10 条

    boolean existsByEmail(String email);

    long countByStatus(UserStatus status);

    void deleteByEmail(String email);                   // 删除操作需 @Transactional

    // ⭐ 排序
    List<User> findByName(String name, Sort sort);

    // ⭐ 分页
    Page<User> findByName(String name, Pageable pageable);
}
```

### 命名查询关键字

| 关键字 | SQL 片段 |
|:------|:---------|
| `And` | `AND` |
| `Or` | `OR` |
| `Is`, `Equals` | `=` |
| `Between` | `BETWEEN ... AND ...` |
| `LessThan` | `<` |
| `GreaterThan` | `>` |
| `LessThanEqual` | `<=` |
| `GreaterThanEqual` | `>=` |
| `After` | `>`（日期） |
| `Before` | `<`（日期） |
| `IsNull`, `Null` | `IS NULL` |
| `IsNotNull`, `NotNull` | `IS NOT NULL` |
| `Like` | `LIKE` |
| `NotLike` | `NOT LIKE` |
| `StartingWith` | `LIKE 'prefix%'` |
| `EndingWith` | `LIKE '%suffix'` |
| `Containing` | `LIKE '%keyword%'` |
| `OrderBy` | `ORDER BY` |
| `Not` | `<>` |
| `In` | `IN (...)` |
| `NotIn` | `NOT IN (...)` |
| `True` | `= TRUE` |
| `False` | `= FALSE` |
| `IgnoreCase` | 忽略大小写 |

### @Query 自定义 JPQL ⭐

```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ⭐ JPQL——面向对象的查询语言
    @Query("SELECT u FROM User u WHERE u.email = ?1")
    Optional<User> findByEmailCustom(String email);

    @Query("SELECT u FROM User u WHERE u.name LIKE %?1%")
    List<User> searchByName(String keyword);

    // ⭐ 命名参数（推荐）
    @Query("SELECT u FROM User u WHERE u.name = :name AND u.age > :minAge")
    List<User> findByNameAndMinAge(@Param("name") String name,
                                   @Param("minAge") Integer minAge);

    // ⭐ 更新操作
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") UserStatus status);

    // ⭐ 删除操作
    @Modifying
    @Transactional
    @Query("DELETE FROM User u WHERE u.email = :email")
    int deleteByEmail(@Param("email") String email);
}
```

### 原生 SQL 查询

```java
// ⭐ nativeQuery = true —— 写原生 SQL
@Query(value = "SELECT * FROM user WHERE MATCH(name) AGAINST(?1 IN BOOLEAN MODE)",
       nativeQuery = true)
List<User> fullTextSearch(String keyword);

@Query(value = "SELECT * FROM user ORDER BY create_time DESC LIMIT 10",
       nativeQuery = true)
List<User> findRecentUsers();
```

### DTO 投影

```java
// ⭐ 接口投影——只查询部分字段
public interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}

// 或使用类投影
public record UserDto(Long id, String name, String email) {}
```

```java
@Query("SELECT new com.demo.dto.UserDto(u.id, u.name, u.email) FROM User u")
List<UserDto> findUserSummaries();

// 接口投影——Spring Data 自动代理
@Query("SELECT u.id AS id, u.name AS name, u.email AS email FROM User u")
List<UserSummary> findUserSummaries();
```

---

## 五、分页与排序 ⭐

### 分页查询

```java
// ⭐ Pageable 分页
Pageable pageable = PageRequest.of(0, 10);  // 第1页，每页10条

Page<User> page = userRepository.findAll(pageable);

page.getTotalElements();    // 总记录数
page.getTotalPages();       // 总页数
page.getNumber();           // 当前页码（0-based）
page.getSize();             // 每页大小
page.getContent();          // 当前页数据
page.hasPrevious();         // 是否有上一页
page.hasNext();             // 是否有下一页
page.isFirst();             // 是否是第一页
page.isLast();              // 是否是最后一页
```

### 排序

```java
// ⭐ Sort 排序
Sort sort = Sort.by(Sort.Direction.DESC, "createTime");
List<User> users = userRepository.findAll(sort);

// 多字段排序
Sort sort = Sort.by(
    Sort.Order.desc("createTime"),
    Sort.Order.asc("name")
);

// ⭐ 分页 + 排序
Pageable pageable = PageRequest.of(0, 10,
    Sort.by(Sort.Direction.DESC, "createTime"));
Page<User> page = userRepository.findAll(pageable);
```

### Specification 动态查询 ⭐

```java
// ⭐ JPA 的复杂动态查询——Specification
public interface UserRepository extends JpaRepository<User, Long>,
                                        JpaSpecificationExecutor<User> {
}

// ⭐ 动态条件组合
public class UserSpecs {

    public static Specification<User> nameLike(String name) {
        return (root, query, cb) ->
            name == null ? null :
                cb.like(root.get("name"), "%" + name + "%");
    }

    public static Specification<User> ageBetween(Integer min, Integer max) {
        return (root, query, cb) -> {
            if (min == null && max == null) return null;
            if (min == null) return cb.lessThan(root.get("age"), max);
            if (max == null) return cb.greaterThan(root.get("age"), min);
            return cb.between(root.get("age"), min, max);
        };
    }

    public static Specification<User> statusIn(List<UserStatus> statuses) {
        return (root, query, cb) ->
            statuses == null || statuses.isEmpty() ? null :
                root.get("status").in(statuses);
    }
}
```

```java
// 组合使用
Specification<User> spec = Specification
    .where(UserSpecs.nameLike("张"))
    .and(UserSpecs.ageBetween(18, 60))
    .and(UserSpecs.statusIn(List.of(UserStatus.ACTIVE)));

Page<User> page = userRepository.findAll(spec, pageable);
```

---

## 六、事务管理

### 事务

```java
// ⭐ Spring 声明式事务
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Transactional(rollbackFor = Exception.class)  // 所有异常回滚
    public User createUser(User user) {
        User saved = userRepository.save(user);

        // ⭐ 发送邮件——如果失败则回滚用户创建
        emailService.sendWelcomeEmail(user.getEmail());

        return saved;
    }
}
```

### 事务传播行为

```java
@Transactional(propagation = Propagation.REQUIRED)       // 默认：支持当前事务，没有则新建
@Transactional(propagation = Propagation.REQUIRES_NEW)   // 新建事务，挂起当前事务
@Transactional(propagation = Propagation.NESTED)         // 嵌套事务（使用 savepoint）
@Transactional(propagation = Propagation.SUPPORTS)       // 支持当前事务，没有就不使用
@Transactional(propagation = Propagation.NOT_SUPPORTED)  // 非事务方式执行
@Transactional(propagation = Propagation.MANDATORY)      // 必须在事务中，否则抛异常
@Transactional(propagation = Propagation.NEVER)          // 必须不在事务中，否则抛异常
```

### 事务隔离级别

```java
@Transactional(isolation = Isolation.READ_COMMITTED)   // ⭐ 常用（防脏读）
@Transactional(isolation = Isolation.REPEATABLE_READ)  // MySQL 默认
@Transactional(isolation = Isolation.SERIALIZABLE)      // 性能低，极少用
@Transactional(isolation = Isolation.READ_UNCOMMITTED)  // 脏读，基本不用
```

---

## 七、审计（Auditing）⭐

```java
// ⭐ 1. 实体类添加审计字段
@Entity
@EntityListeners(AuditingEntityListener.class)   // 启用审计
public class User {

    @CreatedDate                                    // 创建时间
    @Column(updatable = false)
    private LocalDateTime createTime;

    @LastModifiedDate                               // 最后修改时间
    private LocalDateTime updateTime;

    @CreatedBy                                      // 创建人
    @Column(updatable = false)
    private String createBy;

    @LastModifiedBy                                 // 最后修改人
    private String updateBy;
}
```

```java
// ⭐ 2. 配置审计
@Configuration
@EnableJpaAuditing  // ⭐ 启用 JPA 审计
public class JpaConfig {

    @Bean
    public AuditorAware<String> auditorAware() {
        // 从 SecurityContext 中获取当前用户
        return () -> Optional.ofNullable(SecurityContextHolder.getContext())
                .map(ctx -> ctx.getAuthentication())
                .map(auth -> auth.getName())
                .or(() -> Optional.of("system"));
    }
}
```

---

## 八、锁机制

### 乐观锁 ⭐

```java
// ⭐ @Version——JPA 乐观锁（推荐）
@Entity
public class Product {
    @Id
    private Long id;

    private String name;

    @Version
    private Integer version;  // 每次更新自动 +1
}

// UPDATE product SET name = ?, version = version + 1
// WHERE id = ? AND version = oldVersion
// 如果 version 不匹配，抛出 OptimisticLockException
```

### 悲观锁

```java
// ⭐ 悲观锁——行级锁
@Lock(LockModeType.PESSIMISTIC_WRITE)  // 排他锁（SELECT ... FOR UPDATE）
@Query("SELECT p FROM Product p WHERE p.id = :id")
Optional<Product> findByIdWithLock(@Param("id") Long id);

// ⭐ 其他锁模式
@Lock(LockModeType.PESSIMISTIC_READ)      // 共享锁
@Lock(LockModeType.OPTIMISTIC)            // 乐观锁（检查 version）
@Lock(LockModeType.OPTIMISTIC_FORCE_INCREMENT)  // 乐观锁（强制 increate version）
```

---

## 九、性能优化

### N+1 问题 ⭐

```java
// ⭐ N+1 问题：查 1 次用户，然后 N 次查每个用户的订单
List<User> users = userRepository.findAll();
for (User user : users) {
    System.out.println(user.getOrders().size());  // 每次循环都查数据库！
}
```

#### 解决办法 1：JOIN FETCH

```java
@Query("SELECT DISTINCT u FROM User u LEFT JOIN FETCH u.orders")
List<User> findAllWithOrders();

// 或 @EntityGraph（推荐，更简洁）
@EntityGraph(attributePaths = {"orders"})
@Query("SELECT u FROM User u")
List<User> findAllWithOrders();
```

#### 解决办法 2：@EntityGraph

```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ⭐ 实体图——在查询时指定要加载的关联
    @EntityGraph(attributePaths = {"orders", "roles"})
    @Query("SELECT u FROM User u WHERE u.id = :id")
    Optional<User> findByIdWithAssociations(@Param("id") Long id);

    // 命名实体图
    @EntityGraph("User.orders")
    List<User> findAll();
}

@Entity
@NamedEntityGraph(name = "User.orders",
    attributeNodes = @NamedAttributeNode("orders"))
public class User {
    // ...
}
```

#### 解决办法 3：批量抓取

```yaml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 20  # ⭐ 批量抓取大小
```

### 只读查询优化

```java
// ⭐ 只读事务——优化查询性能
@Transactional(readOnly = true)
public Optional<User> findById(Long id) {
    return userRepository.findById(id);
}
```

### 批量操作

```java
// ⭐ 批量插入优化
@Transactional
public void batchInsert(List<User> users) {
    for (int i = 0; i < users.size(); i++) {
        userRepository.save(users.get(i));
        if (i % 20 == 0) {
            entityManager.flush();    // 批量刷入
            entityManager.clear();    // 清空持久化上下文
        }
    }
}
```

---

## 十、常见面试题

### 1. JPA 和 MyBatis 怎么选？

> JPA 适用于**对象模型复杂、关联多、标准 CRUD 多**的项目，开发效率高，但 SQL 调优困难。MyBatis 适用于**复杂 SQL、需要精细优化、报表类查询**多的场景。**实际项目中可以混用**：Spring Data JPA 做简单 CRUD，MyBatis 做复杂查询。

### 2. N+1 问题是什么？怎么解决？

> 查询主实体后循环访问关联实体导致多次查询。解决方式：**JOIN FETCH** / **@EntityGraph** / **批量抓取（`@BatchSize`）**。

### 3. `@Transactional` 的失效场景？

> - 同一类内的方法自调用（`this.method()`）
> - `private` 方法
> - 非 Spring 管理的对象调用
> - `rollbackFor` 没设置，默认只回滚 `RuntimeException`
> - `propagation` 设置为 `NOT_SUPPORTED` / `NEVER`

### 4. `save()` 方法是保存还是更新？

> JPA 的 `save()` 根据 ID 判断：**ID 为 null → persist（插入）**，**ID 不为 null → merge（更新）**。注意 merge 会先查询数据库再决定。

### 5. 什么是持久化上下文？

> 持久化上下文（Persistence Context）是一级缓存，EntityManager 管理的实体都在其中。`find()` 先查缓存，没有才查数据库。事务提交时，缓存中的脏数据自动同步到数据库。

### 6. JPA 中的懒加载和急加载？

> `FetchType.LAZY`：用到关联时才查数据库（代理对象），**推荐使用**。`FetchType.EAGER`：查主实体时关联对象一起查出，可能导致性能问题和 N+1。最佳实践：全部用 LAZY + @EntityGraph 按需控制。

---

> [!tip] **学习路径建议**
> 1. **入门**：JPA 概念 → @Entity/Table/Column → Spring Data JPA 基本 CRUD
> 2. **进阶**：方法命名查询 → @Query → 关联映射（@OneToMany/@ManyToMany）
> 3. **深入**：分页排序 → Specification 动态查询 → 事务 → 审计
> 4. **高级**：乐观/悲观锁 → N+1 优化 → 批量操作 → EntityGraph
