# SpringCloud 篇

## 分布式基础

> [!info] 微服务架构将单一应用拆分为多个独立服务，每个服务独立部署、独立演进，服务之间通过轻量级通信机制（HTTP/RPC）交互。

---

## Nacos

Nacos 实现**两大核心功能**：注册中心 + 配置中心。

### Nacos 注册中心

| 概念 | 说明 |
|------|------|
| **服务注册** | 微服务启动时将自身信息（IP、端口、服务名）注册到 Nacos |
| **服务发现** | 服务消费者从 Nacos 查询可用的服务实例列表 |
| **健康检查** | Nacos 定期检测服务状态，剔除不可用实例 |

**使用方法**：

```java
@SpringBootApplication
@EnableDiscoveryClient  // 启用服务发现
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### 远程调用

**基础实现（RestTemplate）**：

```java
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}

// 调用时直接使用 IP + 端口
String url = "http://localhost:8081/api/data";
String result = restTemplate.getForObject(url, String.class);
```

**负载均衡实现（@LoadBalanced）**：

```java
@Bean
@LoadBalanced  // 开启负载均衡
public RestTemplate restTemplate() {
    return new RestTemplate();
}

// 调用时使用服务名代替 IP
String url = "http://user-service/api/data";
String result = restTemplate.getForObject(url, String.class);
```

> [!warning] **Nacos 宕机时的行为**
> - 服务提供者：本地缓存服务列表，继续提供服务
> - 服务消费者：本地缓存的服务列表继续可用，但无法感知新服务
> - Nacos 恢复后自动同步数据

---

### Nacos 配置中心

**作用**：实现配置的**动态更新**，无需重启服务。

#### 三种配置方式

| 方式 | 说明 | 推荐 |
|:----:|------|:----:|
| ① 硬编码 | 代码中直接写配置 | ❌ |
| ② **Spring Cloud 原生集成** | 使用 `@RefreshScope` + `bootstrap.yml` | **✅ 推荐** |
| ③ Nacos Open API | HTTP 接口手动刷新 | 仅特殊场景 |

#### 数据隔离

通过 **Namespace（命名空间）** 实现不同环境（开发/测试/生产）的配置隔离：

```
Namespace: dev     → 开发环境配置
Namespace: test    → 测试环境配置
Namespace: prod    → 生产环境配置
```

---

## OpenFeign

**声明式 HTTP 客户端**，简化服务间远程调用。

### 基本使用

```java
// 1. 引入依赖 + 启动类加 @EnableFeignClients
@SpringBootApplication
@EnableFeignClients
public class Application {}

// 2. 编写 Feign 接口
@FeignClient(name = "user-service", path = "/api/user")
public interface UserFeignClient {
    @GetMapping("/{id}")
    User getUser(@PathVariable("id") Long id);
}

// 3. 注入使用
@Service
public class OrderService {
    @Autowired
    private UserFeignClient userFeignClient;

    public User findUser(Long id) {
        return userFeignClient.getUser(id);
    }
}
```

### 进阶配置

| 功能 | 说明 |
|------|------|
| **日志配置** | 通过配置类设置 Feign 日志级别（BASIC / HEADERS / FULL） |
| **超时控制** | `connectTimeout` + `readTimeout`，默认 1 秒 |
| **重试机制** | 默认不开启，可通过配置或 `Retryer` Bean 开启 |
| **拦截器** | 请求拦截器 / 响应拦截器，用于统一添加 Header |
| **Fallback 兜底** | 编写 Fallback 类实现服务降级 |

> [!tip] **超时配置示例**
> ```yaml
> spring.cloud.openfeign.client.config.default.connect-timeout: 5000
> spring.cloud.openfeign.client.config.default.read-timeout: 5000
> ```

---

## Sentinel（流量防卫兵）

Sentinel 以**流量**为切入点，提供**限流、熔断降级、系统保护**等功能。

### 基本使用

1. 引入 `sentinel-core` 依赖
2. 配置 Sentinel 控制台地址
3. 在控制台中配置规则

### 异常处理

```java
// 实现 BlockExceptionHandler 接口，自定义限流/降级处理
@Component
public class MyBlockHandler implements BlockExceptionHandler {
    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response,
                       BlockException e) throws Exception {
        response.setStatus(429);
        response.getWriter().write("请求过于频繁，请稍后再试");
    }
}
```

### 流控规则

| 概念 | 说明 |
|------|------|
| **资源** | 被保护的方法或接口 |
| **阈值** | 允许的最大 QPS 或线程数 |
| **流控模式** | 直接 / 关联 / 链路 |
| **流控效果** | 快速失败 / Warm Up / 排队等待 |

### 熔断降级规则

> [!warning] 开启熔断后，当请求错误率达到阈值，后续请求将自动触发 **Fallback 兜底**，在设定的时间窗口内不再请求目标服务，防止雪崩效应。

---

## Gateway（网关）

**作用**：统一入口，转发前端请求到后端微服务。

### 三大核心组件

| 组件 | 说明 | 类比 |
|------|------|:----:|
| **Route（路由）** | 路由的基本构建块 | 类似 Nginx location |
| **Predicate（断言）** | 匹配 HTTP 请求的条件 | 类似 if 判断 |
| **Filter（过滤器）** | 对请求/响应进行修改 | 类似中间件 |

### 配置示例

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/user/**
          filters:
            - StripPrefix=1
```

> [!tip] **Gateway  vs  Feign**
> - **Gateway**：外部请求的**统一入口**，处理前端到后端的路由
> - **Feign**：微服务**内部**的声明式 HTTP 调用

---

## Seata（分布式事务）

### 核心原理

Seata 通过 **AT 模式**（自动补偿）实现分布式事务，核心流程：

```
① TM（事务管理器）向 TC（事务协调器）开启全局事务
② RM（资源管理器）注册分支事务，执行本地 SQL 并记录 undo_log
③ TM 根据结果向 TC 发起全局提交或回滚
④ TC 通知各 RM 执行提交或回滚（通过 undo_log）
```

> [!info] **二阶段提交**
> - **一阶段**：业务 SQL + undo_log（记录修改前数据）
> - **二阶段**：成功则删除 undo_log；失败则通过 undo_log 回滚

### 使用方式

1. 引入 `seata-all` 依赖
2. 配置 `file.conf` 和 `registry.conf`
3. 在全局事务入口方法加 `@GlobalTransactional`
