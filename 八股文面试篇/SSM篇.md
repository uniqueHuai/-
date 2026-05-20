# SSM篇

## 1. Spring 中的 IoC 和 DI 是什么？

**IoC（控制反转）**：将对象的创建和依赖关系的管理交给 Spring 容器，由容器负责对象的生命周期，而不是由对象自己创建或查找依赖。核心思想是**将控制权从程序代码转移到外部容器**。

**DI（依赖注入）**：IoC 的具体实现方式，容器在创建对象时，自动将其依赖的其他对象注入给它。

**三种注入方式对比**：
| 注入方式 | 说明 | 推荐度 |
| 构造器注入 | 保证不可变性和依赖完整性 | ⭐ **推荐** |
| Setter 注入 | 可选依赖，支持重新注入 | ⭐⭐ 次选 |
| 字段注入（`@Autowired`） | 代码最简洁，但不利于测试 | ❌ 不推荐生产使用 |

> [!quote] **IoC 是设计思想，DI 是具体实现方式。**

---

## 2. Spring 框架中的单例 Bean 是线程安全的吗？

Spring 单例 Bean **默认不是线程安全的**。当 Bean 中包含**可变状态**（成员属性）时，多线程访问就需要考虑**线程同步问题**。

> [!tip] **解决思路**
> 1. `@Scope("prototype")` → 改为**多例**，每次获取创建新实例
> 2. **无状态设计** → 不定义可变成员变量，或使用 `final` 修饰
> 3. **`ThreadLocal`** → 保存线程私有变量，空间换时间
> 4. **加锁** → `synchronized` / `Lock`，但会降低并发性能

---

## 3. 什么是 AOP？

**AOP**（面向切面编程）将公共行为和公共模块复用抽离出来，降低耦合。

Spring AOP 底层基于**动态代理技术**：
- ==JDK 动态代理==：目标类实现了接口时使用
- ==CGLIB 动态代理==：目标类没有实现接口时使用（通过生成子类）

常见应用场景：**权限认证、==日志记录==、==事务管理==、性能监控**

### AOP 核心注解

| 注解 | 类别 | 作用 |
|------|------|------|
| `@Aspect` | 切面声明 | 声明一个类为切面类 |
| `@Pointcut` | 切点定义 | 定义可重用的切点表达式 |
| `@Before` | 前置通知 | 目标方法执行前执行 |
| `@AfterReturning` | 返回通知 | 方法成功返回后执行 |
| `@AfterThrowing` | 异常通知 | 方法抛出异常后执行 |
| `@After` | 后置通知 | 方法执行后执行（finally） |
| `@Around` | **环绕通知** | **最强大**，可控制方法执行全过程 |
| `@EnableAspectJAutoProxy` | 配置 | 启用 AspectJ 自动代理 |

### 通知类型对比

| 通知类型 | 能否阻止方法执行 | 能否修改返回值 | 能否处理异常 |
|----------|:---:|:---:|:---:|
| `@Before` | 可抛出异常阻止 | ❌ | ❌ |
| `@AfterReturning` | ❌ | ✅ **可修改** | ❌ |
| `@AfterThrowing` | ❌ | ❌ | ✅ **可捕获** |
| `@After` | ❌ | ❌ | ❌ |
| `@Around` | ✅ **完全控制** | ✅ **完全修改** | ✅ **完全处理** |

---

## 4. 你们项目中有没有使用到 AOP？

我们在后台管理系统中使用 AOP 来记录**系统操作日志**。

> [!example] **实现思路**
> 1. 自定义 `@Log` 注解标记需要记录日志的方法
> 2. 使用 `@Around` 环绕通知 + 切点表达式匹配
> 3. 通过 `ProceedingJoinPoint` 获取请求参数、类信息、方法信息等
> 4. 将操作日志**异步**保存到数据库

---

## 5. Spring 中的事务是如何实现的？

Spring 事务管理基于 **AOP + 动态代理**：

```
目标方法调用前   →   开启事务
   ↓
目标方法执行     →   (正常 / 异常)
   ↓
正常返回 → 提交事务  |  抛出异常 → 回滚事务
```

> [!info] **声明式事务的两种方式**
> - ✅ 基于 `@Transactional` 注解（推荐）
> - 📋 基于 XML 配置事务增强

---

## 6. Spring 中事务失效的场景有哪些？

> [!danger] **场景一：异常被内部捕获未抛出**
> - 事务方法内 `try-catch` 捕获异常后没有重新抛出
> - Spring 无法感知异常，事务**不会回滚**
> - ✅ **解决**：捕获后重新抛出异常，或手动 `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`

> [!warning] **场景二：抛出检查型异常（Checked Exception）**
> - 默认只对 `RuntimeException` 和 `Error` 回滚
> - `IOException`、`SQLException` 等**不会触发回滚**
> - ✅ **解决**：`@Transactional(rollbackFor = Exception.class)`

> [!warning] **场景三：方法不是 public 修饰**
> - Spring 代理机制限制，只能拦截 public 方法
> - `private`、`protected`、`default` 方法上 `@Transactional` 失效

> [!caution] **场景四：同类中方法内部调用**
> - `this.method()` 直接调用同类中的另一个 `@Transactional` 方法
> - 不走代理对象，事务注解不生效
> - ✅ **解决**：将事务方法拆分到另一个 Service，或自注入调用代理方法

> [!caution] **场景五：数据库引擎不支持事务**
> - 例如 MySQL 的 MyISAM 引擎不支持事务
> - ✅ **解决**：改用 InnoDB 引擎

---

## 7. Spring 的 Bean 生命周期？

> [!info] **完整流程（9 步）**
>
> **① 解析 BeanDefinition** — 读取配置元数据
> **② 实例化** — 通过构造函数创建 Bean 实例
> **③ 依赖注入** — Setter 注入 / `@Autowired` 属性赋值
> **④ Aware 接口回调** — `BeanNameAware`、`BeanFactoryAware`、`ApplicationContextAware`
> **⑤ BeanPostProcessor 前置处理** — `postProcessBeforeInitialization`，初始化前最后的修改机会
> **⑥ 初始化** — `InitializingBean.afterPropertiesSet()` / 自定义 `init-method`
> **⑦ ==BeanPostProcessor 后置处理==** — `postProcessAfterInitialization`，**在此产生代理对象**（AOP、`@Transactional` 都在此完成）
> **⑧ 使用 Bean** — Bean 就绪，供应用程序使用
> **⑨ 销毁** — `DisposableBean.destroy()` / 自定义 `destroy-method`

> [!tip] **记忆要点**
> 关键节点：**实例化 → DI → 初始化前后处理器（AOP 代理在此产生）**

---

## 8. Spring 中的循环引用（循环依赖）？

循环依赖指两个或以上的 Bean 互相持有对方，形成闭环。

Spring 通过**三级缓存**解决（仅适用于 **Setter 注入**）：

| 缓存级别 | 名称 | 说明 |
|:---:|------|------|
| 🥇 一级缓存 | `singletonObjects` | **单例池**，已完成初始化的 Bean |
| 🥈 二级缓存 | `earlySingletonObjects` | **早期对象**，尚未完成生命周期的 Bean |
| 🥉 三级缓存 | `singletonFactories` | **`ObjectFactory`**，用于提前创建代理对象 |

> [!danger] **构造器注入的循环依赖无法解决** — 构造函数在实例化阶段就执行，此时三级缓存尚未生效

---

## 9. 循环依赖的具体解决流程？

以 A 依赖 B、B 依赖 A 为例：

```
① 实例化 A → 将 A 的 ObjectFactory 存入 三级缓存
   ↓
② A 需要注入 B → 开始创建 B
   ↓
③ 实例化 B → 将 B 的 ObjectFactory 存入 三级缓存
   ↓
④ B 需要注入 A
   → 从三级缓存获取 A 的 ObjectFactory
   → 生成 A 的早期对象 → 移入 二级缓存，清除 A 的三级缓存
   ↓
⑤ B 获取到 A → B 创建完成 → 存入 一级缓存，清除 B 的三级缓存
   ↓
⑥ A 恢复初始化 → 此时 B 已在 一级缓存 → 直接注入 B
   ↓
⑦ A 创建完成 → 存入 一级缓存，清除二级缓存中的 A 临时对象
```

---

## 10. 构造方法出现循环依赖怎么解决？

> [!danger] **无法解决**
> 构造函数在 Bean 生命周期中最先执行，三级缓存在此场景下无效

> [!tip] **解决方案**
> 1. **`@Lazy` 注解**：延迟其中一个 Bean 的创建，Spring 为其生成代理对象，使用时才真正创建
> 2. **改为 Setter 注入**：Setter 注入可以通过三级缓存解决
> 3. **重新设计**：拆分职责，彻底消除循环依赖

---

## 11. BeanFactory 和 FactoryBean 的区别？

| | BeanFactory | FactoryBean |
|------|-------------|-------------|
| **本质** | Spring 容器的**顶层接口** | 一个**特殊的 Bean** |
| **作用** | 管理 Bean 的创建、配置、生命周期 | 用于**复杂对象的创建** |
| **获取方式** | `beanName` 获取普通 Bean | `&beanName` 获取 FactoryBean 本身；`beanName` 获取其生产的对象 |

> [!example] **典型应用**
> `MyBatis` 的 `SqlSessionFactoryBean`、`Spring` 的 `ProxyFactoryBean` 都实现了 `FactoryBean`

---

## 12. SpringMVC 的执行流程？

```
用户请求
   ↓
① DispatcherServlet（前端控制器 → 统一调度）
   ↓
② HandlerMapping（处理器映射器 → 根据 URL 查找 Handler）
   ↓
③ 返回处理器执行链（Handler + 拦截器链）
   ↓
④ HandlerAdapter（处理器适配器 → 调用具体 Controller）
   ↓
⑤ Controller 方法执行
   ↓
⑥ 返回 ModelAndView
   ↓
⑦ ViewResolver（视图解析器 → 解析视图）
   ↓
⑧ 渲染视图 → 响应给用户
```

> [!info] **核心组件串记**
> **前端控制器 → 处理器映射器 → 处理器适配器 → Controller → 视图解析器**

---

## 13. SpringBoot 自动配置原理？

`@SpringBootApplication` 封装了三个核心注解：

```
@SpringBootApplication
   ├── @SpringBootConfiguration     // 标识配置类
   ├── @EnableAutoConfiguration     // ⭐ 开启自动配置（核心）
   └── @ComponentScan               // 包扫描
```

> [!info] **`@EnableAutoConfiguration` 核心机制**
>
> 1. `@Import(AutoConfigurationImportSelector.class)` 导入配置选择器
> 2. 读取 `META-INF/spring.factories` 中的自动配置类列表
> 3. 通过 ==`@Conditional` 条件注解== 判断是否加载（如 `@ConditionalOnClass`、`@ConditionalOnMissingBean`）
> 4. 条件满足 → 将配置类中的 Bean 注入容器

> [!tip] **举例：spring-boot-starter-web**
> 依赖传递引入 `spring-boot-autoconfigure` → 读取自动配置类 → 检测 classpath 下是否存在 `Servlet` 类 → 条件满足则注入 `DispatcherServlet` 等 Web 组件

---

## 14. Spring、SpringMVC、SpringBoot 常见注解

### Spring 核心注解

| 类别 | 注解 |
|------|------|
| 声明 Bean | `@Component`、`@Service`、`@Repository`、`@Controller` |
| 依赖注入 | `@Autowired`、`@Qualifier`、`@Resource`（JSR-250） |
| 作用域 | `@Scope`（singleton / prototype / request / session） |
| 配置类 | `@Configuration`、`@ComponentScan`、`@Bean`、`@Import` |
| AOP | `@Aspect`、`@Before`、`@After`、`@Around`、`@Pointcut` |
| 条件装配 | `@Conditional`、`@Profile` |

### SpringMVC 常见注解

| 注解 | 作用 |
|------|------|
| `@RestController` | `@Controller` + `@ResponseBody` 的组合 |
| `@RequestMapping` | 映射请求路径（类/方法级别） |
| `@GetMapping` / `@PostMapping` 等 | 特化的 `@RequestMapping` |
| `@RequestBody` | 接收请求体的 JSON 数据并反序列化 |
| `@ResponseBody` | 返回值序列化为 JSON 写入响应体 |
| `@RequestParam` | 绑定请求参数到方法参数 |
| `@PathVariable` | 从 URL 路径中获取参数 |
| `@RequestHeader` | 获取请求头数据 |
| `@ControllerAdvice` | 全局异常处理、全局数据绑定 |

### SpringBoot 常见注解

| 注解 | 作用 |
|------|------|
| `@SpringBootApplication` | **核心组合注解** |
| `@EnableAutoConfiguration` | 开启自动配置 |
| `@ConfigurationProperties` | 绑定配置文件属性到 Java Bean |
| `@EnableConfigurationProperties` | 启用配置属性绑定 |
| `@ConditionalOnClass` / `@ConditionalOnMissingBean` / ... | 条件装配家族 |

---

## 15. MyBatis 的执行流程？

```
mybatis-config.xml → 读取配置文件
       ↓
解析 Mapper.xml → 构建配置对象
       ↓
SqlSessionFactory（会话工厂）
       ↓
SqlSession（会话）
       ↓
Executor（执行器）
       ↓
MappedStatement → 动态 SQL 拼接 + 参数映射
       ↓
输入参数映射（Java 参数 → JDBC 预编译参数）
       ↓
数据库执行
       ↓
输出结果映射（ResultSet → Java 对象）
```

> [!info] **核心流程**
> **配置文件 → SqlSessionFactory → SqlSession → Executor → MappedStatement → 结果映射**

---

## 16. MyBatis 中 #{} 和 ${} 的区别？

| 特性 | `#{}` | `${}` |
|------|:---:|:---:|
| 处理方式 | **预编译**（占位符替换） | **字符串直接拼接** |
| ==SQL 注入== | ✅ **安全** | ❌ **不安全** |
| 场景 | **传参**（绝大多数场景） | 表名/字段名等动态 SQL 片段 |
| 底层 | `PreparedStatement` 占位符 `?` | 直接字符串替换 |

> [!warning] **黄金原则**
> 能用 `#{}` 的地方 **绝不** 用 `${}`。只有需要**动态传入列名、表名**时才使用 `${}`，且传入值必须做白名单校验。

---

## 17. MyBatis Mapper 接口的原理？

Mapper 接口不需要实现类也能工作的原因 —— **JDK 动态代理**：

> [!example] **工作原理**
>
> 1. 调用 `SqlSession.getMapper(UserMapper.class)` → MyBatis 使用 **JDK 动态代理** 创建接口的代理对象
> 2. 代理对象通过 **方法全限定名**（如 `com.example.mapper.UserMapper.findById`）查找对应的 **MappedStatement**
> 3. 将 SQL + 执行参数封装 → 交给 Executor 执行并返回结果

---

## 18. MyBatis 是否支持延迟加载？

MyBatis 支持延迟加载（懒加载），在**真正需要用到关联数据时**才执行 SQL 查询。

```xml
<!-- 开启延迟加载 -->
<setting name="lazyLoadingEnabled" value="true" />
<setting name="aggressiveLazyLoading" value="false" />
```

> [!tip] **底层原理（CGLIB 动态代理）**
>
> 1. 使用 CGLIB 为目标对象创建 **代理对象**
> 2. 调用关联属性的 getter 方法时，代理拦截
> 3. 若关联属性为 null → 执行关联查询 SQL
> 4. 获取数据后设置属性值，完成调用

---

## 19. MyBatis 的一级、二级缓存

| 特性 | 一级缓存 | 二级缓存 |
|------|:---:|:---:|
| **默认开启** | ✅ 是 | ❌ 需要手动配置 |
| **作用域** | `SqlSession` 级别 | `Namespace` / Mapper 级别 |
| **存储** | HashMap（PerpetualCache） | HashMap（PerpetualCache） |
| **开启方式** | 无需配置 | Mapper XML 中添加 `<cache/>` + `cacheEnabled=true` |

> [!info] **缓存清理时机**
> 当作用域内执行了 **INSERT / UPDATE / DELETE** 操作后，该作用域下所有 SELECT 缓存将被清空（避免脏读）
> - 一级缓存：当前 SqlSession 的增删改触发清理
> - 二级缓存：该 Mapper 的任何增删改触发清理