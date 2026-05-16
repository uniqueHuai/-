# 1. Spring框架中的单例bean是线程安全的吗？

Spring框架中的单例(Singleton)Bean<font style="color:#DF2A3F;">默认不是线程安全的</font>，这取决于Bean的具体实现方式。当bean中包含<font style="color:#DF2A3F;">可变状态（成员属性）</font>时，多个线程访问就要考虑到<font style="color:#DF2A3F;">线程同步问题</font>，线程安全和并发问题需要自行解决。

解决线程安全问题，①使用@Scope（"prototype"）修改为多例。②设置为无状态（没有成员变量或成员变量用final修饰）

# 2. 什么是AOP？

AOP，即面向切面编程，将公共行为和公共模块复用抽离出来，降低耦合。Spring的AOP底层是基于<font style="color:#DF2A3F;">动态代理技术</font>来实现的，也就是说在程序运行的时候，会自动的基于动态代理技术为目标对象生成一个对应的代理对象。在代理对象当中就会对目标对象当中的原始方法进行功能的增强。在我们的项目中我们自己写AOP的场景其实很少 , 但是我们使用的很多框架的功能底层都是AOP , 例如 :<font style="color:#DF2A3F;"> 权限认证、日志、事务处理</font>等。

|**注解**|**类别**|**作用**|**示例**|
|---|---|---|---|
|**@Aspect**|切面声明|声明一个类为切面类|`**@Aspect @Component public class LogAspect {}**`|
|**@Pointcut**|切点定义|定义可重用的切点表达式|`**@Pointcut("execution(* com.service.*.*(..))") public void serviceMethods() {}**`|
|**@Before**|前置通知|在目标方法执行前执行|`**@Before("serviceMethods()") public void beforeAdvice(JoinPoint jp) {}**`|
|**@AfterReturning**|返回通知|在方法成功返回后执行|`**@AfterReturning(pointcut="serviceMethods()", returning="result") public void afterReturn(Object result) {}**`|
|**@AfterThrowing**|异常通知|在方法抛出异常后执行|`**@AfterThrowing(pointcut="serviceMethods()", throwing="ex") public void afterThrows(Exception ex) {}**`|
|**@After**|后置通知|在方法执行后执行（无论是否异常）|`**@After("serviceMethods()") public void afterFinally() {}**`|
|**@Around**|环绕通知|最强大的通知类型，可控制方法执行|`**@Around("serviceMethods()") public Object around(ProceedingJoinPoint pjp) throws Throwable {}**`|
|**@DeclareParents**|引入|为类动态引入新接口|`**@DeclareParents(value="com.service.*+", defaultImpl=DefaultImpl.class) public static NewInterface mixin;**`|
|**@EnableAspectJAutoProxy**|配置|启用AspectJ自动代理|`**@Configuration @EnableAspectJAutoProxy public class AppConfig {}**`|

|**<font style="color:#000000;">通知类型</font>**|**<font style="color:#000000;">执行时机</font>**|**<font style="color:#000000;">能否阻止方法执行</font>**|**<font style="color:#000000;">能否修改返回值</font>**|**<font style="color:#000000;">能否处理异常</font>**|
|---|---|---|---|---|
|**<font style="color:#000000;">@Before</font>**|<font style="color:#000000;">方法执行前</font>|<font style="color:#000000;">可抛出异常阻止</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">否</font>|
|**<font style="color:#000000;">@AfterReturning</font>**|<font style="color:#000000;">方法成功返回后</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">可修改返回值</font>|<font style="color:#000000;">否</font>|
|**<font style="color:#000000;">@AfterThrowing</font>**|<font style="color:#000000;">方法抛出异常后</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">可捕获异常</font>|
|**<font style="color:#000000;">@After</font>**|<font style="color:#000000;">方法执行后（finally）</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">否</font>|<font style="color:#000000;">否</font>|
|**<font style="color:#000000;">@Around</font>**|<font style="color:#000000;">方法执行前后</font>|<font style="color:#000000;">完全控制</font>|<font style="color:#000000;">可完全修改</font>|<font style="color:#000000;">可完全处理</font>|

# 3. 你们项目中有没有使用到AOP？

我们之前在后台管理系统中使用AOP来记录系统操作日志。主要思路是使用AOP的环绕通知和切点表达式，找到需要记录日志的方法，然后通过环绕通知的参数获取请求方法的参数，例如类信息、方法信息、注解、请求方式等，并将这些参数保存到数据库。

# 4. Spring中的事务是如何实现的？

Spring事务管理是基于AOP(面向切面编程)和动态代理实现的，它对方法前后进行拦截，在执行方法前开启事务，在执行完目标方法后根据执行情况提交或回滚事务。

# 5. Spring中事务失效的场景有哪些？

1. 如果方法内部捕获并处理了异常，没有将异常抛出，会导致事务失效。因此，处理异常后应该确保异常能够被抛出。
    

原因：

- Spring 事务的回滚机制依赖于异常是否抛出。
    
- 如果在事务方法内部 try-catch 捕获了异常，但没有重新抛出（或手动回滚），Spring 无法感知异常，事务不会回滚。
    

2. 如果方法抛出检查型异常（checked exception），并且没有在`@Transactional`注解上配置`rollbackFor`属性为`Exception`，那么异常发生时事务可能不会回滚。
    

原因

- 默认情况下，Spring 事务只对 RuntimeException 和 Error 回滚。
    
- 检查型异常（如 IOException、SQLException）不会触发回滚，除非显式配置 @Transactional(rollbackFor = Exception.class)
    

3. 如果事务注解的方法不是公开（public）修饰的，也可能导致事务失效。
    

# 6. Spring的bean的生命周期？

Spring中bean的生命周期包括以下步骤：

1. 通过BeanDefinition获取bean的定义信息。
    
2. 调用构造函数实例化bean。
    
3. 进行bean的依赖注入，例如通过setter方法或@Autowired注解。
    
4. 处理实现了Aware接口的bean。（获取bean的名字）
    
5. 执行BeanPostProcessor的前置处理器。（初始化前的最后修改机会，修改Bean属性、处理注解）
    
6. 调用初始化方法，如实现了InitializingBean接口或自定义的init-method。（执行自定义初始化逻辑，连接数据库、加载配置）
    
    . 执行BeanPostProcessor的后置处理器，可能在这里产生代理对象。（生成代理或最终增强 AOP 动态代理（如 @Transactional））
    
7. 最后是销毁bean。
    

# 7. Spring中的循环引用（循环依赖）？

循环依赖发生在两个或两个以上的bean互相持有对方，形成闭环。Spring框架允许循环依赖存在，并通过三级缓存解决大部分循环依赖问题：

1. 一级缓存：单例池，缓存已完成初始化的bean对象。
    
2. 二级缓存：缓存尚未完成生命周期的早期bean对象。
    
3. 三级缓存：缓存ObjectFactory，用于创建bean对象。
    

# 8. 那具体解决流程清楚吗？

解决循环依赖的流程如下：

1. 实例化A对象，并创建ObjectFactory存入三级缓存。（此时A还没完成依赖注入）
    
2. A在初始化时需要B对象，开始B的创建逻辑。
    
3. B实例化完成，也创建ObjectFactory存入三级缓存。
    
4. B需要注入A，通过三级缓存获取ObjectFactory生成A对象，由于A中的是三级缓存早期对象，将A存入二级缓存。清除A的三级缓存。
    
5. B通过二级缓存获得A对象后，B创建成功，存入一级缓存。清除B的三级缓存。
    
6. A对象初始化时，由于B已创建完成，可以直接注入B，A创建成功存入一级缓存。
    
7. 清除二级缓存中的临时对象A。
    

# 9. 构造方法出现了循环依赖怎么解决？

由于构造函数是bean生命周期中最先执行的，Spring框架无法解决构造方法的循环依赖问题。可以使用@Lazy懒加载注解，延迟bean的创建直到实际需要时。

# 10. SpringMVC的执行流程？

SpringMVC的执行流程包括以下步骤：

1. 用户发送请求到前端控制器DispatcherServlet。（请求到达，统一协调处理）
    
2. DispatcherServlet调用HandlerMapping找到具体处理器。（映射器处理，根据URL找对应controller器）
    
3. HandlerMapping返回处理器对象及拦截器（如果有）给DispatcherServlet。
    
4. DispatcherServlet调用HandlerAdapter。
    
5. HandlerAdapter适配并调用具体处理器（Controller）。
    
6. Controller执行并返回ModelAndView对象。
    
7. HandlerAdapter将ModelAndView返回给DispatcherServlet。
    
8. DispatcherServlet传给ViewResolver进行视图解析。
    
9. ViewResolver返回具体视图给DispatcherServlet。
    
10. DispatcherServlet渲染视图并响应用户。
    

<font style="color:#DF2A3F;">前端处理器--HandlerMapping--处理适配器--返回给前端处理器</font>

# 11. Springboot自动配置原理？

Spring Boot的自动配置原理基于@SpringBootApplication注解，它封装了@SpringBootConfiguration、@EnableAutoConfiguration和@ComponentScan。<font style="color:#DF2A3F;">@EnableAutoConfiguratio</font>n是核心，它通过<font style="color:#DF2A3F;">@Import({AutoConfigurationImportSelector.class})</font>导入配置选择器，读取META-INF/spring.factories文件中的类名，根据条件注解决定是否将配置类中的Bean导入到Spring容器中。

例如spring-boot-web-start依赖，依赖传递：Starter 依赖 → spring-boot-autoconfigure 。然后@Import({AutoConfigurationImportSelector.class})，读取META-INF/spring.factories文件中的类名，根据条件注解@Condition这些决定是否将配置类中的Bean导入到Spring容器中。

# 12. Spring 的常见注解有哪些？

Spring的常见注解包括：

1. 声明Bean的注解：@Component、@Service、@Repository、@Controller。
    
2. 依赖注入相关注解：@Autowired、@Qualifier、@Resource。
    
3. 设置作用域的注解：@Scope。
    
4. 配置相关注解：@Configuration、@ComponentScan、@Bean。
    
5. AOP相关注解：@Aspect、@Before、@After、@Around、@Pointcut。
    

# 13. SpringMVC常见的注解有哪些？

SpringMVC的常见注解有：

-@RestController：@Controller和@ResponseBody的组合

- @RequestMapping：映射请求路径。
    
- @RequestBody：接收HTTP请求的JSON数据。
    
- @RequestParam：指定请求参数名称。
    
- @PathVariable：从请求路径中获取参数。
    
- @ResponseBody：将Controller方法返回的对象转化为JSON。
    
- @RequestHeader：获取请求头数据。
    
- @PostMapping、@GetMapping等。
    

# 14. Springboot常见注解有哪些？

Spring Boot的常见注解包括：

- @SpringBootApplication：由@SpringBootConfiguration、@EnableAutoConfiguration和@ComponentScan组成。
    
- 其他注解如@RestController、@GetMapping、@PostMapping等，用于简化Spring MVC的配置。
    

# 15. MyBatis执行流程？

MyBatis的执行流程如下：

1. <font style="color:#DF2A3F;">读取MyBatis配置文件</font>mybatis-config.xml。
    
2. <font style="color:#DF2A3F;">解析xml映射文件</font>。
    
3. 构造会话工厂<font style="color:#DF2A3F;">SqlSessionFactory</font>。（每个数据库环境对应一个工厂）
    
4. 会话工厂创建<font style="color:#DF2A3F;">SqlSession对象</font>。
    
5. 操作数据库的接口，<font style="color:#DF2A3F;">Executor执行器</font>。
    
6. Executor执行方法中的<font style="color:#DF2A3F;">MappedStatement</font>参数。
    
7. 输入参数映射。
    
8. 输出结果映射。
    

# 16. Mybatis是否支持延迟加载？

MyBatis支持延迟加载，即在需要用到数据时才加载。可以通过配置文件中的lazyLoadingEnabled配置启用或禁用延迟加载。

# 17. 延迟加载的底层原理知道吗？

延迟加载的底层原理主要使用CGLIB动态代理实现：

1. 使用CGLIB创建目标对象的代理对象。
    
2. 调用目标方法时，如果发现是null值，则执行SQL查询。
    
3. 获取数据后，设置属性值并继续查询目标方法。
    

# 18. Mybatis的一级、二级缓存用过吗？

MyBatis的一级缓存是基于PerpetualCache的HashMap本地缓存，作用域为Session，默认开启。二级缓存需要单独开启，作用域为Namespace或mapper，默认也是采用PerpetualCache，HashMap存储。

# 19. Mybatis的二级缓存什么时候会清理缓存中的数据？

当作用域（一级缓存Session/二级缓存Namespaces）进行了新增、修改、删除操作后，默认该作用域下所有select中的缓存将被清空。