# Tomcat

## 一、Tomcat 概述

### 什么是 Tomcat

**Apache Tomcat** 是一个开源的 **Servlet 容器**，实现了 Java Servlet、JSP、WebSocket 等 Jakarta EE（原 Java EE）规范，是 Java Web 应用最流行的运行环境。

```
      HTTP 请求
         │
         ▼
    ┌──────────────────────────────────────┐
    │           Tomcat 服务器                │
    │  ┌────────────────────────────────┐   │
    │  │        Catalina（Servlet 容器）    │   │
    │  │  ┌──────┐  ┌──────┐  ┌──────┐ │   │
    │  │  │ Servlet │  │  JSP  │  │Filter│ │   │
    │  │  └──────┘  └──────┘  └──────┘ │   │
    │  └────────────────────────────────┘   │
    │  ┌────────────────────────────────┐   │
    │  │     Coyote（HTTP 连接器）          │   │
    │  └────────────────────────────────┘   │
    │  ┌────────────────────────────────┐   │
    │  │    Jasper（JSP 引擎）             │   │
    │  └────────────────────────────────┘   │
    └──────────────────────────────────────┘
```

### 核心组件

| 组件 | 说明 |
|:----|:-----|
| **Catalina** | Servlet 容器，实现 Servlet/JSP 规范 |
| **Coyote** | HTTP 连接器，处理网络请求 |
| **Jasper** | JSP 引擎，将 JSP 编译为 Servlet |
| **Cluster** | 集群组件，支持会话复制 |
| **Realm** | 安全域，管理用户认证与授权 |

### 版本与规范

| Tomcat 版本 | Jakarta EE | Servlet | JSP | Java 版本 |
|:-----------:|:----------:|:-------:|:---:|:---------:|
| **11.x** | 11 | 6.1 | 4.0 | 17+ |
| **10.1.x** | 10 | 6.0 | 3.1 | 11+ |
| **9.x** | 8 (javax.*) | 4.0 | 2.3 | 8+ |
| **8.5.x** | 7 | 3.1 | 2.3 | 7+ |

> [!warning] **包名变化**
> Tomcat 10+ 使用 `jakarta.*` 替代 `javax.*`。老项目升级时需注意包名变更。

---

## 二、目录结构

```
apache-tomcat-10.1.x/
├── bin/                    # 启动/关闭脚本
│   ├── catalina.sh         # 核心启动脚本（Linux/Mac）
│   ├── catalina.bat        # 核心启动脚本（Windows）
│   ├── startup.sh/startup.bat   # 启动
│   └── shutdown.bat        # 关闭
├── conf/                   # 配置文件
│   ├── server.xml          # ⭐ 核心配置文件
│   ├── web.xml             # 全局 web 配置
│   ├── context.xml         # 全局 Context 配置
│   ├── tomcat-users.xml    # 用户/角色管理
│   ├── logging.properties  # 日志配置
│   └── catalina.policy     # 安全策略
├── lib/                    # Tomcat 自身依赖的 JAR
├── logs/                   # 日志目录
│   ├── catalina.out        # 控制台日志
│   ├── localhost_access_log.*.txt  # 访问日志
│   └── localhost.*.log     # 应用日志
├── temp/                   # 临时文件
├── webapps/                # ⭐ 部署目录（放 WAR 包或展开的目录）
│   ├── ROOT/               # 根应用
│   ├── docs/               # Tomcat 文档
│   ├── examples/           # 示例应用
│   ├── host-manager/       # 虚拟主机管理
│   └── manager/            # Web 管理控制台
└── work/                   # JSP 编译后的 .class 文件
```

---

## 三、核心配置（server.xml）⭐

### 整体结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Server port="8005" shutdown="SHUTDOWN">      <!-- ⭐ 关闭端口（安全：建议修改） -->

    <!-- 全局 JNDI 资源 -->
    <GlobalNamingResources>
        <Resource name="UserDatabase" auth="Container"
                  type="org.apache.catalina.UserDatabase"
                  description="User database"
                  factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                  pathname="conf/tomcat-users.xml"/>
    </GlobalNamingResources>

    <!-- ⭐ Service——将连接器与引擎关联 -->
    <Service name="Catalina">

        <!-- ⭐ 连接器（Connector）——监听 HTTP 请求 -->
        <Connector port="8080" protocol="HTTP/1.1"
                   connectionTimeout="20000"
                   redirectPort="8443"
                   maxParameterCount="1000"/>

        <!-- ⭐ 引擎（Engine）——处理请求的核心 -->
        <Engine name="Catalina" defaultHost="localhost">

            <!-- ⭐ 虚拟主机（Host） -->
            <Host name="localhost" appBase="webapps"
                  unpackWARs="true" autoDeploy="true">

                <!-- ⭐ 应用上下文（Context） -->
                <Context path="/myapp" docBase="myapp"
                         reloadable="true"/>

                <!-- ⭐ 访问日志 -->
                <Valve className="org.apache.catalina.valves.AccessLogValve"
                       directory="logs"
                       prefix="localhost_access_log"
                       suffix=".txt"
                       pattern="%h %l %u %t &quot;%r&quot; %s %b"/>
            </Host>
        </Engine>
    </Service>
</Server>
```

### Connector（连接器）

```xml
<!-- ⭐ HTTP 连接器 -->
<Connector
    port="8080"                         <!-- 监听端口 -->
    protocol="HTTP/1.1"                 <!-- 协议 -->
    connectionTimeout="20000"            <!-- 连接超时（毫秒） -->
    redirectPort="8443"                 <!-- SSL 重定向端口 -->
    maxThreads="200"                    <!-- ⭐ 最大工作线程数 -->
    minSpareThreads="10"                <!-- 最小空闲线程数 -->
    acceptCount="100"                   <!-- 等待队列长度 -->
    maxConnections="10000"              <!-- 最大连接数 -->
    compression="on"                    <!-- 启用压缩 -->
    compressionMinSize="2048"           <!-- 最小压缩大小（字节） -->
    compressableMimeType="text/html,text/xml,text/css,application/json"
    URIEncoding="UTF-8"                 <!-- ⭐ URI 编码 -->
/>

<!-- ⭐ AJP 连接器（配合 Apache/Nginx 使用） -->
<Connector port="8009" protocol="AJP/1.3" secretRequired="false"/>
```

### Engine（引擎）

```xml
<Engine name="Catalina" defaultHost="localhost">
    <!-- name:     引擎名称（与 Service 对应）
         defaultHost: 默认虚拟主机名 -->
</Engine>
```

### Host（虚拟主机）

```xml
<!-- ⭐ 虚拟主机——一台 Tomcat 运行多个网站 -->
<Host name="www.example.com" appBase="webapps/example"
      unpackWARs="true" autoDeploy="true">
    <!-- name:        域名
         appBase:    该主机的应用目录
         unpackWARs: 是否解压 WAR 包
         autoDeploy: 自动部署新应用 -->
</Host>

<!-- 第二个虚拟主机 -->
<Host name="admin.example.com" appBase="webapps/admin"
      unpackWARs="true" autoDeploy="true">
</Host>
```

### Context（应用上下文）

```xml
<!-- ⭐ 每个应用一个 Context -->
<Context
    path="/myapp"           <!-- 访问路径：http://localhost:8080/myapp -->
    docBase="/opt/apps/myapp"  <!-- 应用的实际路径（绝对或相对 appBase） -->
    reloadable="true"       <!-- ⭐ 修改类文件时自动重载（开发用，生产关掉） -->
    crossContext="false"    <!-- 是否允许跨 Context 访问 -->
    sessionTimeout="30"     <!-- Session 超时（分钟） -->
/>
```

---

## 四、部署方式 ⭐

### 方式一：直接复制 WAR

```bash
# 将 WAR 包复制到 webapps 目录，Tomcat 自动解压部署
cp myapp.war /path/to/tomcat/webapps/
# 访问：http://localhost:8080/myapp

# 根应用（ROOT）
cp myapp.war /path/to/tomcat/webapps/ROOT.war
# 访问：http://localhost:8080/
```

### 方式二：IDEA 配置

```xml
<!-- IntelliJ IDEA → Run → Edit Configurations → Tomcat Server -->
<!-- Deployment → Artifact → 选择你的 Web 项目 -->
```

### 方式三：Manager App

```bash
# 1. 配置 tomcat-users.xml（添加管理角色）
```

```xml
<role rolename="manager-gui"/>
<role rolename="manager-script"/>
<user username="admin" password="admin" roles="manager-gui,manager-script"/>
```

```bash
# 2. 浏览器访问 http://localhost:8080/manager/html

# 或命令行部署
curl -u admin:admin \
     -T myapp.war \
     "http://localhost:8080/manager/text/deploy?path=/myapp"
```

### 方式四：嵌入式 Tomcat（Spring Boot 默认）⭐

```java
// Spring Boot 内嵌 Tomcat——无需安装，直接运行
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        // Tomcat 在 Spring Boot 内部启动，默认端口 8080
    }
}

// 配置内嵌 Tomcat
server.port=8080
server.servlet.context-path=/myapp
server.tomcat.max-threads=200
server.tomcat.max-connections=10000
server.tomcat.accept-count=100
```

---

## 五、连接器与线程池 ⭐

### 线程池配置

```xml
<!-- ⭐ 在 server.xml 中自定义线程池 -->
<Executor
    name="tomcatThreadPool"
    namePrefix="catalina-exec-"
    maxThreads="200"             <!-- 最大线程数 -->
    minSpareThreads="20"         <!-- 核心线程数 -->
    maxIdleTime="60000"          <!-- 空闲线程存活时间（毫秒） -->
    maxQueueSize="Integer.MAX_VALUE"  <!-- 等待队列 -->
/>

<!-- 连接器引用线程池 -->
<Connector executor="tomcatThreadPool"
           port="8080"
           protocol="HTTP/1.1"/>
```

### IO 模型

| 模型 | 协议 | 说明 |
|:----|:----|:-----|
| **BIO** | `HTTP/1.1` | 阻塞 IO（Tomcat 9 已移除） |
| **NIO** | `org.apache.coyote.http11.Http11NioProtocol` | ⭐ 非阻塞 IO，默认 |
| **NIO2** | `org.apache.coyote.http11.Http11Nio2Protocol` | 异步 IO，更高性能 |
| **APR** | `org.apache.coyote.http11.Http11AprProtocol` | 基于本地库，最高性能 |

```xml
<!-- 指定 NIO2 协议 -->
<Connector port="8080"
           protocol="org.apache.coyote.http11.Http11Nio2Protocol"
           maxThreads="200"/>
```

### 连接数调优

```xml
<Connector port="8080" protocol="HTTP/1.1"
           maxThreads="200"          <!-- ⭐ 最大工作线程（默认 200） -->
           minSpareThreads="10"      <!-- 最小空闲线程 -->
           acceptCount="100"         <!-- ⭐ 等待队列大小 -->
           maxConnections="10000"    <!-- ⭐ 最大连接数（NIO 默认 10000） -->
           connectionTimeout="20000" <!-- 连接超时 -->
/>
```

---

## 六、SSL/HTTPS ⭐

### 自签名证书

```bash
# ⭐ 生成自签名证书（开发测试用）
keytool -genkey -alias tomcat -keyalg RSA \
    -keystore /path/to/tomcat/conf/keystore.p12 \
    -storetype PKCS12 -storepass changeit \
    -validity 3650 -keysize 2048
```

### server.xml 配置

```xml
<!-- ⭐ HTTPS 连接器 -->
<Connector port="8443" protocol="HTTP/1.1"
           maxThreads="200"
           SSLEnabled="true"
           scheme="https"
           secure="true">

    <SSLHostConfig>
        <Certificate
            certificateKeystoreFile="conf/keystore.p12"
            certificateKeystorePassword="changeit"
            certificateKeystoreType="PKCS12"
            type="RSA"/>
    </SSLHostConfig>
</Connector>

<!-- HTTP 自动跳转到 HTTPS -->
<Connector port="8080" protocol="HTTP/1.1"
           redirectPort="8443"/>
```

### Spring Boot 配置

```yaml
server:
  port: 8443
  ssl:
    key-store: classpath:keystore.p12
    key-store-password: changeit
    key-store-type: PKCS12
    key-alias: tomcat
```

---

## 七、Session 管理

### Session 配置

```xml
<!-- web.xml —— Session 超时设置 -->
<session-config>
    <session-timeout>30</session-timeout>  <!-- 分钟 -->
</session-config>
```

### 会话持久化

```xml
<!-- context.xml —— 重启后 Session 不丢失 -->
<Manager className="org.apache.catalina.session.PersistentManager"
         saveOnRestart="true"
         maxActiveSessions="-1"
         minIdleSwap="0"
         maxIdleSwap="30"
         maxIdleBackup="0">

    <!-- 文件存储 -->
    <Store className="org.apache.catalina.session.FileStore"
           directory="session-data"/>
</Manager>
```

### 集群会话复制

```xml
<!-- ⭐ Tomcat 集群——Session 广播复制 -->
<Cluster className="org.apache.catalina.ha.tcp.SimpleTcpCluster"
         channelSendOptions="8">

    <!-- 多播发现 -->
    <Channel className="org.apache.catalina.tribes.group.GroupChannel">
        <Membership className="org.apache.catalina.tribes.membership.McastService"
                    address="228.0.0.4" port="45564"
                    frequency="500" dropTime="3000"/>
        <Receiver className="org.apache.catalina.tribes.transport.nio.NioReceiver"
                  address="auto" port="4000"/>
        <Sender className="org.apache.catalina.tribes.transport.ReplicationTransmitter">
            <Transport className="org.apache.catalina.tribes.transport.nio.PooledParallelSender"/>
        </Sender>
    </Channel>

    <!-- 会话值过滤 -->
    <Valve className="org.apache.catalina.ha.tcp.ReplicationValve"
           filter=".*\.gif;.*\.js;.*\.css;.*\.png;"/>

    <!-- 部署器 -->
    <Deployer className="org.apache.catalina.ha.deploy.FarmWarDeployer"
              tempDir="/tmp/war-temp" deployDir="/tmp/war-deploy"
              watchDir="/tmp/war-listen" watchEnabled="false"/>
</Cluster>
```

> [!tip] **生产环境不推荐 Tomcat 集群会话复制**
> 性能开销大，建议用 **Redis Session 共享**（Spring Session）替代。

---

## 八、性能调优 ⭐

### JVM 参数

```bash
# ⭐ catalina.sh（在文件开头设置）

# JVM 内存
JAVA_OPTS="-Xms4g -Xmx4g -Xmn1g"           # 堆内存
JAVA_OPTS="$JAVA_OPTS -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m"
JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"         # ⭐ G1 垃圾回收器
JAVA_OPTS="$JAVA_OPTS -XX:+HeapDumpOnOutOfMemoryError"
JAVA_OPTS="$JAVA_OPTS -XX:HeapDumpPath=/path/to/dumps"
JAVA_OPTS="$JAVA_OPTS -Djava.awt.headless=true"
JAVA_OPTS="$JAVA_OPTS -Dfile.encoding=UTF-8"
```

```yaml
# Spring Boot 内嵌 Tomcat JVM 参数
java -Xms4g -Xmx4g -Xmn1g \
     -XX:+UseG1GC \
     -jar myapp.jar
```

### 连接器调优

```xml
<Connector port="8080" protocol="HTTP/1.1"
           maxThreads="200"              <!-- 适当增加 -->
           minSpareThreads="20"
           acceptCount="100"
           maxConnections="10000"
           connectionTimeout="20000"
           keepAliveTimeout="15000"       <!-- keep-alive 超时 -->
           maxKeepAliveRequests="100"     <!-- 最多 keep-alive 请求数 -->
           compression="on"              <!-- 启用压缩 -->
           compressionMinSize="2048"
           compressableMimeType="text/html,text/xml,text/css,
                                 application/json,application/javascript"/>
```

### 禁用自动部署

```xml
<!-- 生产环境建议关闭 autoDeploy 和 reloadable -->
<Host name="localhost" appBase="webapps"
      autoDeploy="false" deployOnStartup="true">
    <Context path="/myapp" docBase="myapp" reloadable="false"/>
</Host>
```

### 静态资源缓存

```xml
<!-- ⭐ 配置静态资源缓存 -->
<Context docBase="myapp" path="/myapp">
    <Resources cachingAllowed="true"
               cacheMaxSize="102400"     <!-- 缓存大小（KB） -->
               cacheObjectMaxSize="2048" <!-- 单个缓存最大（KB） -->
               cacheTtl="5000"/>         <!-- 缓存存活（毫秒） -->
</Context>
```

### 生产环境 checklist

| 项目 | 建议 |
|:----|:-----|
| **JVM 堆** | 4-8G（视应用而定） |
| **GC** | G1GC |
| **连接器** | NIO 或 NIO2 |
| **maxThreads** | 200-500 |
| **autoDeploy** | false |
| **reloadable** | false |
| **SSL** | 生产用 CA 证书 |
| **访问日志** | 开启（排查问题） |
| **监控** | JMX / Prometheus + Grafana |
| **集群** | Nginx 负载均衡 + Redis session |

---

## 九、日志管理

### 日志配置

```properties
# conf/logging.properties

# ⭐ Tomcat 自身日志
org.apache.catalina.level = INFO
org.apache.tomcat.level = INFO

# 访问日志
org.apache.catalina.valves.AccessLogValve.level = INFO

# ⭐ 应用日志（默认使用 JULI——Tomcat 的日志实现）
org.apache.catalina.core.ContainerBase.[Catalina].[localhost].level = INFO
org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/manager].level = INFO
```

### 访问日志格式

```xml
<!-- server.xml 配置访问日志 -->
<Valve className="org.apache.catalina.valves.AccessLogValve"
       directory="logs"
       prefix="localhost_access_log"
       suffix=".txt"
       pattern="%h %l %u %t &quot;%r&quot; %s %b %D">

<!--
  %h = 客户端 IP
  %l = 远程登录名（通常为 -）
  %u = 用户名
  %t = 时间
  %r = 请求行（方法 + URI + 协议）
  %s = HTTP 状态码
  %b = 响应字节数
  %D = 处理时间（毫秒）
  %T = 处理时间（秒）
-->
</Valve>
```

### 访问日志轮转

```xml
<!-- ⭐ 按日期轮转 -->
<Valve className="org.apache.catalina.valves.AccessLogValve"
       directory="logs"
       prefix="access_log"
       suffix=".txt"
       pattern="common"
       rotatable="true"
       fileDateFormat="yyyy-MM-dd"/>  <!-- 每天一个文件 -->
```

---

## 十、安全配置

### 修改默认端口

```xml
<!-- 修改关闭端口（默认 8005） -->
<Server port="8005" shutdown="CHANGE_THIS_SECRET">
```

### 删除默认应用

```bash
# 生产环境删除默认的 webapps 应用
rm -rf webapps/docs
rm -rf webapps/examples
rm -rf webapps/host-manager
rm -rf webapps/manager
rm -rf webapps/ROOT  # 替换为自己的应用
```

### 配置安全头

```xml
<!-- ⭐ 添加安全响应头 -->
<Valve className="org.apache.catalina.valves.rewrite.RewriteValve"/>
```

```properties
# conf/web.xml 中添加
<security-constraint>
    <web-resource-collection>
        <web-resource-name>All</web-resource-name>
        <url-pattern>/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```

### 使用非 root 用户运行

```bash
# ⭐ 安全性：禁止用 root 运行 Tomcat
groupadd tomcat
useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
chown -R tomcat:tomcat /opt/tomcat
sudo -u tomcat /opt/tomcat/bin/startup.sh
```

---

## 十一、常见面试题

### 1. Tomcat 的架构是怎样的？

> Tomcat 核心由 **Coyote**（HTTP 连接器）、**Catalina**（Servlet 容器）和 **Jasper**（JSP 引擎）组成。请求流程：`Connector` 接收请求 → `Engine` 选择 `Host` → `Host` 匹配 `Context` → 执行 Servlet。

### 2. Tomcat 有哪些 IO 模型？

> **NIO**（默认，非阻塞）、**NIO2**（异步 IO）、**APR**（基于本地库，最高性能）。早期 BIO 在 Tomcat 9 中已移除。

### 3. Tomcat 有哪几种部署方式？

> ① 复制 WAR 到 `webapps/`；② Manager App 图形化/API 部署；③ IDEA/Eclipse 插件部署；④ Spring Boot 嵌入式部署。

### 4. 怎么优化 Tomcat 性能？

> ① 增大 JVM 堆内存，使用 G1GC；② 调整 `maxThreads` / `acceptCount` / `maxConnections`；③ 开启压缩；④ 关闭 `autoDeploy` 和 `reloadable`；⑤ 配置静态资源缓存；⑥ 使用 NIO2 或 APR 协议。

### 5. 什么是 Tomcat 的类加载机制？

> Tomcat 打破了双亲委派模型：**先用自己的 WebappClassLoader 加载 `WEB-INF/classes` 和 `WEB-INF/lib` 的类**，加载不到才委托给父加载器。这样每个 Web 应用可以隔离依赖（如不同版本的 Spring）。

### 6. 怎么解决 Tomcat 的 Session 共享问题？

> ① Tomcat 集群会话复制（不推荐，性能差）；② **Redis + Spring Session**（推荐）；③ 客户端存储 Session（JWT Token）；④ 粘性 Session（Nginx 配置 `ip_hash`）。

### 7. Tomcat 和 Nginx 的关系？

> **Nginx** 在前端做反向代理、负载均衡、静态资源服务。**Tomcat** 在后端运行 Java Web 应用。典型架构：`Nginx（80）→ Tomcat（8080）`，Nginx 处理静态资源，动态请求转发到 Tomcat 集群。

---

> [!tip] **学习路径建议**
> 1. **入门**：安装启动 → 目录结构 → 部署 WAR 包
> 2. **进阶**：server.xml 配置 → 虚拟主机 → 连接器配置
> 3. **深入**：SSL/HTTPS → Session 管理 → 集群配置
> 4. **高级**：JVM 调优 → 性能优化 → 安全加固 → 生产架构
