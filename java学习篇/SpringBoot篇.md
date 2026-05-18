# SpringBoot 篇

## 一、Spring Boot 概述

### 什么是 Spring Boot？

Spring Boot 是一个基于 Spring 框架的**快速开发框架**，它通过**自动配置**和**起步依赖**大幅简化了 Spring 应用的搭建和开发。

### 解决了什么问题？

| 痛点 | Spring Boot 解决方案 |
|:----|:----|
| 复杂的 XML 配置 | **自动配置**，零 XML |
| 依赖版本冲突 | **Starter** 整合依赖版本 |
| 内嵌容器部署麻烦 | **内嵌 Tomcat/Jetty/Undertow**，jar 直接运行 |
| 生产监控缺失 | **Actuator** 提供开箱即用的监控端点 |

### Spring vs Spring MVC vs Spring Boot

```
Spring Framework（IoC/AOP/DI — 基础容器）
    └── Spring MVC（Web 层框架）
            └── Spring Boot（自动配置 + 起步依赖 + 内嵌容器 — 快速开发）
```

| 对比 | Spring | Spring MVC | Spring Boot |
|:----:|:------:|:----------:|:-----------:|
| **核心** | IoC 容器、AOP | Web MVC 框架 | 自动配置、快速开发 |
| **配置** | XML / Java Config | XML / Java Config | **自动配置 + application.yml** |
| **部署** | 需外置 Tomcat | 需外置 Tomcat | **jar 包独立运行** |
| **监控** | 需自行集成 | 需自行集成 | **内置 Actuator** |

> [!info] 三者关系：**Spring Boot 包含 Spring 和 Spring MVC**，在其基础上做了开箱即用的封装。

### 核心优势

1. ✅ **自动配置**：根据 classpath 依赖自动配置 Bean
2. ✅ **起步依赖**：`spring-boot-starter-xxx` 一站式引入
3. ✅ **内嵌容器**：jar 包直接运行，无需外置 Web 服务器
4. ✅ **生产就绪**：Actuator、Metrics、Health Check
5. ✅ **生态完善**：与 Cloud、Data、Security 无缝集成

---

## 二、核心注解详解

### 1. @SpringBootApplication 组合解剖

```java
@SpringBootApplication = 
    @SpringBootConfiguration    // 标识为配置类（本质是 @Configuration）
  + @EnableAutoConfiguration    // ⭐ 开启自动配置（核心）
  + @ComponentScan              // 包扫描（默认扫描当前包及其子包）
```

> [!tip] 启动类一般放在**根包**下，确保 `@ComponentScan` 能扫描到所有子包。

### 2. @Conditional 条件装配家族

条件注解是自动配置的**核心支撑**，用于判断是否加载某个配置类：

| 注解 | 判断条件 |
|:----:|----------|
| `@ConditionalOnClass` | classpath 中存在指定类 |
| `@ConditionalOnMissingClass` | classpath 中不存在指定类 |
| `@ConditionalOnBean` | 容器中已有指定 Bean |
| `@ConditionalOnMissingBean` | 容器中**没有**指定 Bean（**自定义覆盖**时用） |
| `@ConditionalOnProperty` | 配置文件中存在指定属性 |
| `@ConditionalOnResource` | 资源文件存在 |
| `@ConditionalOnWebApplication` | 当前是 Web 应用 |
| `@ConditionalOnExpression` | SpEL 表达式为 true |

```java
// 示例：只有 classpath 中有 DataSource 且容器中没有自定义 DataSource 时才加载
@Configuration
@ConditionalOnClass(DataSource.class)
@ConditionalOnMissingBean(DataSource.class)
public class DataSourceAutoConfiguration { ... }
```

### 3. @ConfigurationProperties 配置绑定

```java
// 1. 定义配置属性类
@ConfigurationProperties(prefix = "app.datasource")
@Data
public class DataSourceProperties {
    private String url = "jdbc:mysql://localhost:3306/test";  // 默认值
    private String username = "root";
    private String password;
}

// 2. 启用绑定（方式一：在配置类上添加）
@EnableConfigurationProperties(DataSourceProperties.class)
public class DataSourceConfig { ... }

// 或（方式二：直接在类上添加 @Component 自动生效）
@Component
@ConfigurationProperties(prefix = "app.datasource")
public class DataSourceProperties { ... }
```

```yaml
# application.yml
app:
  datasource:
    url: jdbc:mysql://prod:3306/db
    username: admin
    password: ${DB_PASSWORD}  # 支持环境变量
```

> [!tip] **松散绑定**：`@ConfigurationProperties` 支持松散命名规则
> `app.datasource.user-name` = `userName` = `username`

---

## 三、自动配置原理（深化篇）

### 1. 从 spring.factories 到 AutoConfiguration.imports

| Spring Boot 版本 | 加载机制 | 配置文件 |
|:----------------:|:--------:|:---------:|
| **2.7 之前** | `SpringFactoriesLoader` | `META-INF/spring.factories` |
| **2.7+** | `ImportCandidates` | `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` |

> [!warning] Spring Boot 3.0+ 不再读取 `spring.factories` 中的自动配置类，必须使用新的 `.imports` 文件格式。

### 2. Debug 查看自动配置报告

```yaml
# application.yml
debug: true
```

启动后控制台会打印 **Positive matches**（已生效）和 **Negative matches**（未生效）报告：

```
============================
CONDITIONS EVALUATION REPORT
============================

Positive matches:
-----------------
   DataSourceAutoConfiguration:
      - @ConditionalOnClass found required class 'javax.sql.DataSource' (OnClassCondition)

Negative matches:
-----------------
   QuartzAutoConfiguration:
      - @ConditionalOnClass did not find required class 'org.quartz.Scheduler'
```

> [!tip] 或者通过 Actuator 端点：`GET /actuator/conditions`

### 3. 自动配置的执行流程

```
① @EnableAutoConfiguration → @Import(AutoConfigurationImportSelector.class)
   ↓
② 读取 AutoConfiguration.imports 中的自动配置类全限定名列表
   ↓
③ 逐一对每个配置类评估 @Conditional 条件
   ↓
④ 条件满足 → 加载配置类，注入 Bean 到容器
   ↓
⑤ 条件不满足 → 跳过该配置类
```

### 4. 自定义自动配置

```java
// 1. 编写自动配置类
@Configuration
@ConditionalOnClass(MyService.class)
@ConditionalOnProperty(prefix = "my", name = "enabled", havingValue = "true")
public class MyAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public MyService myService() {
        return new MyService();
    }
}

// 2. 注册到 META-INF/spring/
//    org.springframework.boot.autoconfigure.AutoConfiguration.imports
//    ── 内容：
//    com.example.autoconfigure.MyAutoConfiguration
```

---

## 四、自定义 Starter

### 命名规范

| 类型 | 命名格式 | 示例 |
|:----:|:--------:|------|
| **官方** | `spring-boot-starter-xxx` | `spring-boot-starter-web` |
| **自定义** | `xxx-spring-boot-starter` | `mybatis-spring-boot-starter` |

### 核心四要素

```
xxx-spring-boot-starter
  ├── ① 自动配置类  — @Configuration + @ConditionalXxx
  ├── ② 配置属性类  — @ConfigurationProperties
  ├── ③ spring.factories / .imports  — 注册自动配置类
  └── ④ pom.xml  — 引入项目的核心依赖
```

```java
// 一个简单的邮件发送 Starter 示例

// 配置属性类
@ConfigurationProperties(prefix = "mail")
@Data
public class MailProperties {
    private String host = "localhost";
    private int port = 25;
    private String username;
    private String password;
}

// 自动配置类
@Configuration
@ConditionalOnClass(MailSender.class)
@EnableConfigurationProperties(MailProperties.class)
public class MailAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public MailSender mailSender(MailProperties props) {
        MailSender sender = new MailSender();
        sender.setHost(props.getHost());
        sender.setPort(props.getPort());
        return sender;
    }
}
```

---

## 五、配置文件体系

### 1. 多环境配置

```yaml
# application.yml（主配置）
spring:
  profiles:
    active: dev          # 激活 dev 环境
---
# application-dev.yml（开发环境）
server:
  port: 8080
---
# application-prod.yml（生产环境）
server:
  port: 80
```

> [!info] 激活方式优先级（从高到低）：
> 1. 启动参数 `--spring.profiles.active=prod`
> 2. 环境变量 `SPRING_PROFILES_ACTIVE=prod`
> 3. `application.yml` 中的配置

### 2. 配置加载优先级

**从高到低（高优先级覆盖低优先级）**：

| 优先级 | 配置来源 |
|:------:|:---------|
| **最高** | 命令行参数 `--key=value` |
| ↓ | JNDI 属性 |
| ↓ | JVM 系统属性 `-Dkey=value` |
| ↓ | 操作系统环境变量 |
| ↓ | `application-{profile}.yml`（当前 Profile） |
| ↓ | `application.yml`（主配置） |
| **最低** | `@PropertySource` 注解 |

> [!tip] **记住**：命令行参数 > 环境变量 > application.yml，可用于临时覆盖配置。

### 3. 随机数与占位符

```yaml
app:
  id: ${random.uuid}           # 随机 UUID
  secret: ${random.long}       # 随机 Long
  value: ${random.int(100,999)} # 随机整数
  description: "当前环境：${spring.profiles.active:default}"  # 占位符，带默认值
```

---

## 六、内嵌容器

### 1. 默认容器与切换

| 容器 | 依赖 | 说明 |
|:----:|:----|------|
| **Tomcat**（默认） | `spring-boot-starter-web` | 稳定、广泛使用 |
| **Jetty** | 排除 Tomcat + 引入 Jetty Starter | 适合长连接场景 |
| **Undertow** | 排除 Tomcat + 引入 Undertow Starter | 高并发、低内存 |

```xml
<!-- 切换为 Undertow -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

### 2. 自定义容器配置

```yaml
server:
  port: 8080
  servlet:
    context-path: /api           # 上下文路径
  ssl:
    enabled: true
    key-store: classpath:keystore.p12
    key-store-password: secret
  compression:
    enabled: true                 # 启用压缩
    mime-types: text/html,text/css,application/json
```

---

## 七、日志框架

Spring Boot 默认使用 **SLF4J（门面） + Logback（实现）**。

### 日志级别

```yaml
# application.yml
logging:
  level:
    root: info                   # 全局日志级别
    com.example: debug           # 指定包级别
    org.springframework: warn    # Spring 框架级别
  file:
    name: logs/app.log           # 输出到文件
    max-size: 10MB               # 单个文件大小
    max-history: 7               # 保留天数
```

### 多环境日志配置

```xml
<!-- logback-spring.xml（推荐命名，支持 Profile） -->
<configuration>
    <!-- 开发环境：控制台彩色输出 -->
    <springProfile name="dev">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
    </springProfile>

    <!-- 生产环境：文件输出 -->
    <springProfile name="prod">
        <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
            <file>logs/app.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>logs/app.%d{yyyy-MM-dd}.log</fileNamePattern>
                <maxHistory>30</maxHistory>
            </rollingPolicy>
        </appender>
    </springProfile>
</configuration>
```

> [!tip] 推荐使用 `logback-spring.xml`（带 `-spring` 后缀），支持 `<springProfile>` 标签实现多环境配置。

---

## 八、异常处理与全局响应

### 1. 统一响应体

```java
@Data
public class Result<T> {
    private int code;
    private String message;
    private T data;
    private long timestamp = System.currentTimeMillis();

    public static <T> Result<T> success(T data) {
        Result<T> r = new Result<>();
        r.code = 200;
        r.message = "success";
        r.data = data;
        return r;
    }

    public static <T> Result<T> error(int code, String message) {
        Result<T> r = new Result<>();
        r.code = code;
        r.message = message;
        return r;
    }
}
```

### 2. 全局异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 处理业务异常
    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusiness(BusinessException e) {
        return Result.error(e.getCode(), e.getMessage());
    }

    // 处理参数校验异常
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Void> handleValidation(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
            .map(f -> f.getField() + ": " + f.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return Result.error(400, msg);
    }

    // 兜底异常（未知异常）
    @ExceptionHandler(Exception.class)
    public Result<Void> handleException(Exception e) {
        log.error("未知异常", e);
        return Result.error(500, "服务器内部错误");
    }
}
```

### 3. 参数校验

```java
@PostMapping("/user")
public Result<User> createUser(@Valid @RequestBody UserCreateRequest request) {
    // 校验通过后执行业务逻辑
    return Result.success(userService.create(request));
}

@Data
public class UserCreateRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 20, message = "用户名长度2-20")
    private String username;

    @NotNull(message = "年龄不能为空")
    @Min(value = 0, message = "年龄不能为负")
    @Max(value = 150, message = "年龄不能超过150")
    private Integer age;

    @Email(message = "邮箱格式不正确")
    private String email;
}
```

> [!tip] 常用校验注解：`@NotBlank`、`@NotNull`、`@Size`、`@Min`、`@Max`、`@Email`、`@Pattern`（正则）

---

## 九、生产监控（Actuator）

### 1. 引入与配置

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,conditions   # 暴露的端点
      # exclude: ...
  endpoint:
    health:
      show-details: always          # 显示详细健康信息
```

### 2. 常用端点

| 端点 | 路径 | 作用 |
|:----:|:----:|------|
| **`health`** | `/actuator/health` | 应用健康状态 ✅ |
| **`info`** | `/actuator/info` | 应用基本信息 |
| **`metrics`** | `/actuator/metrics` | 性能指标 |
| **`conditions`** | `/actuator/conditions` | 自动配置条件评估报告 |
| **`env`** | `/actuator/env` | 环境属性 |
| **`loggers`** | `/actuator/loggers` | 日志配置（支持**动态修改级别**） |
| **`mappings`** | `/actuator/mappings` | 请求映射信息 |
| **`beans`** | `/actuator/beans` | 所有 Bean |

> [!tip] **动态修改日志级别**：
> ```bash
> POST /actuator/loggers/com.example
> {"configuredLevel": "debug"}
> ```

### 3. 自定义健康检查

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            return Health.up()
                .withDetail("database", "MySQL")
                .withDetail("status", "connected")
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

---

## 十、Spring Boot 测试

### 1. @SpringBootTest 集成测试

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserServiceTest {

    @Autowired
    private UserService userService;

    @Test
    void testFindById() {
        User user = userService.findById(1L);
        assertThat(user).isNotNull();
        assertThat(user.getName()).isEqualTo("Alice");
    }
}
```

### 2. 测试切片（Test Slice）

| 注解 | 测试范围 |
|:----:|:---------|
| `@WebMvcTest` | **Controller 层**，仅加载 Web 组件 |
| `@DataJpaTest` | **JPA 层**，仅加载 Repository |
| `@MybatisTest` | **MyBatis 层**，仅加载 Mapper |
| `@RestClientTest` | REST 客户端 |
| `@JsonTest` | JSON 序列化/反序列化 |

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void testGetUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new User(1L, "Alice"));

        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.data.name").value("Alice"));
    }
}
```

> [!tip] 测试切片只加载需要的组件，**速度更快**，是单元测试的最佳选择。

---

## 十一、高频面试题精选

### Q1：Spring Boot 的启动流程是怎样的？

```
① 启动类调用 SpringApplication.run()
   ↓
② 创建 SpringApplication 实例
   （推断应用类型、加载初始化器、加载监听器）
   ↓
③ 调用 run() 方法
   ↓
④ 加载 SpringApplicationRunListeners（事件监听）
   ↓
⑤ 准备 Environment（加载 application.yml 等配置文件）
   ↓
⑥ 创建 ApplicationContext（AnnotationConfigServletWebServerApplicationContext）
   ↓
⑦ 刷新容器前准备（设置 Environment 等）
   ↓
⑧ 执行 refreshContext()（⭐ 核心步骤：自动配置在此生效）
   ↓
⑨ 刷新后回调（afterRefresh）
   ↓
⑩ 启动完成 → 调用 Runner（CommandLineRunner / ApplicationRunner）
```

> [!info] **run() 方法一句话版本**：**准备环境 → 创建容器 → 刷新容器（自动配置在此步生效）→ 启动 Web 服务器 → 运行 Runner**

### Q2：Spring Boot 是如何加载配置文件的？

按优先级从高到低：

1. 当前目录 `/config/` 下的配置文件
2. 当前目录下的配置文件
3. classpath `/config/` 下的配置文件
4. classpath 根目录下的配置文件

```
file:./config/   （最高）
file:./
classpath:/config/
classpath:/      （最低）

高优先级属性会覆盖低优先级
```

### Q3：如何实现配置的**动态刷新**？

```java
// 方式一：@RefreshScope（Spring Cloud 原生，需结合配置中心）
@RestController
@RefreshScope
public class ConfigController {

    @Value("${app.version}")
    private String version;
}

// 方式二：Actuator 的 /actuator/refresh 端点
// 触发后，@RefreshScope 修饰的 Bean 会重新创建
```

> [!tip] 生产环境常用的方案：**Nacos 配置中心 + @RefreshScope**

### Q4：内嵌容器是如何启动的？

```
① refreshContext() 触发
   ↓
② 自动配置 ServletWebServerFactory（如 TomcatServletWebServerFactory）
   ↓
③ getWebServer() 创建内嵌容器实例
   ↓
④ 容器启动 → 监听指定端口 → 接受 HTTP 请求
```

### Q5：Spring Boot 性能优化建议？

| 优化项 | 做法 |
|:------|:------|
| **扫描范围** | 使用 `@ComponentScan` 指定扫包范围，避免全量扫描 |
| **延迟初始化** | `spring.main.lazy-initialization=true`（减少启动耗时） |
| **内嵌容器** | 切换为 Undertow（内存更低） |
| **自动配置** | 排除不需要的自动配置 `@SpringBootApplication(exclude = {...})` |
| **日志** | 生产环境关闭 DEBUG 日志 |
| **连接池** | 合理配置 HikariCP 参数 |
| **JVM 参数** | 根据吞吐量调优堆内存和 GC 策略 |

---

> **📖 学习路线**：[[README]] | **上一篇**：[[JVM篇]] | **下一篇**：选择 [[登录认证篇]] 或 [[SpringCloud篇]]
