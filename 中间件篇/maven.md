# Maven

## 一、Maven 概述

### 什么是 Maven

**Maven** 是一个 Java 项目的**构建管理工具**和**依赖管理工具**，使用 `pom.xml` 描述项目结构和依赖关系。

```
         Maven 核心能力
    ┌──────────────────────────────┐
    │  依赖管理     — 自动下载 JAR   │
    │  项目构建     — compile/test/  │
    │               package/install │
    │  项目信息     — 文档/报告      │
    │  多模块管理   — 聚合与继承      │
    │  统一结构     — 约定的目录结构   │
    └──────────────────────────────┘
```

### 核心概念

| 概念 | 说明 |
|:----:|:----|
| **POM** | `pom.xml`，项目对象模型，Maven 的核心配置文件 |
| **坐标** | `groupId:artifactId:version` 唯一定位一个依赖 |
| **仓库** | 本地仓库 → 中央仓库 → 远程仓库（私服） |
| **生命周期** | `clean` → `default` → `site` 三套生命周期 |
| **插件** | Maven 的构建步骤由插件执行 |
| **约定优于配置** | 遵循约定的目录结构，无需额外配置 |

### 约定的目录结构

```
my-app/
├── pom.xml                    # Maven 配置文件
├── src/
│   ├── main/
│   │   ├── java/              # 源代码
│   │   └── resources/         # 资源文件
│   └── test/
│       ├── java/              # 测试代码
│       └── resources/         # 测试资源
└── target/                    # 编译输出目录（自动生成）
```

### 安装与配置

```bash
# 下载解压后配置环境变量
# MAVEN_HOME = /path/to/apache-maven-3.9.x
# PATH = %MAVEN_HOME%/bin

mvn --version
# Apache Maven 3.9.9
# Java version: 17.0.10
```

```xml
<!-- settings.xml（~/.m2/settings.xml）—— 全局/用户配置 -->
<settings>
    <!-- 本地仓库位置（默认 ~/.m2/repository） -->
    <localRepository>D:/maven/repository</localRepository>

    <!-- 镜像——加速依赖下载 -->
    <mirrors>
        <mirror>
            <id>aliyun</id>
            <name>阿里云 Maven 镜像</name>
            <url>https://maven.aliyun.com/repository/public</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
    </mirrors>

    <!-- 全局 JDK 版本 -->
    <profiles>
        <profile>
            <id>jdk-17</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <properties>
                <maven.compiler.source>17</maven.compiler.source>
                <maven.compiler.target>17</maven.compiler.target>
            </properties>
        </profile>
    </profiles>
</settings>
```

```xml
<!-- pom.xml —— 最小项目 -->
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <!-- ⭐ 项目坐标——唯一标识 -->
    <groupId>com.demo</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>  <!-- jar / war / pom -->

    <name>my-app</name>
    <description>示例项目</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
</project>
```

---

## 二、POM 详解

### 坐标（Coordinates）

```xml
<!-- ⭐ 坐标三要素——Maven 仓库中的唯一地址 -->
<groupId>com.example</groupId>     <!-- 公司/组织名（反写域名） -->
<artifactId>user-service</artifactId>  <!-- 项目/模块名 -->
<version>2.1.0-RELEASE</version>      <!-- 版本号 -->
```

版本命名规范：
| 类型 | 示例 | 说明 |
|:----:|:----|:----|
| 正式版 | `1.0.0` | 稳定发布版 |
| SNAPSHOT | `1.0.0-SNAPSHOT` | 开发中的快照版 |
| RC | `1.0.0-RC1` | 发布候选 |
| RELEASE | `1.0.0-RELEASE` | Spring 风格的正式版 |

### packaging

```xml
<packaging>jar</packaging>   <!-- Java 类库（默认） -->
<packaging>war</packaging>   <!-- Web 应用，部署到 Tomcat -->
<packaging>pom</packaging>   <!-- 父项目/聚合项目，无代码 -->
<packaging>maven-plugin</packaging>  <!-- Maven 插件项目 -->
```

### properties

```xml
<properties>
    <!-- ⭐ 统一管理版本号 -->
    <java.version>17</java.version>
    <spring-boot.version>3.2.5</spring-boot.version>
    <mybatis.version>3.5.16</mybatis.version>
    <lombok.version>1.18.32</lombok.version>

    <!-- 编译器版本 -->
    <maven.compiler.source>${java.version}</maven.compiler.source>
    <maven.compiler.target>${java.version}</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

---

## 三、依赖管理 ⭐

### 依赖声明

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.2.5</version>
        <!-- scope 不写则默认 compile -->
    </dependency>

    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>${lombok.version}</version>
        <scope>provided</scope>    <!-- 编译期需要，不打包 -->
    </dependency>

    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>        <!-- 仅测试使用 -->
    </dependency>

    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <version>8.3.0</version>
        <scope>runtime</scope>     <!-- 运行时需要，编译不需要 -->
    </dependency>
</dependencies>
```

### scope 详解

| Scope | 编译 | 测试 | 运行 | 说明 |
|:-----:|:----:|:----:|:----:|:----|
| **compile** | ✅ | ✅ | ✅ | 默认，所有阶段都需要 |
| **provided** | ✅ | ✅ | ❌ | 容器提供（如 Servlet API、Lombok） |
| **runtime** | ❌ | ✅ | ✅ | JDBC 驱动等 |
| **test** | ❌ | ✅ | ❌ | JUnit、Mockito 等 |
| **system** | ✅ | ✅ | ❌ | 本地系统路径（不推荐） |
| **import** | - | - | - | 仅用于 `dependencyManagement` 的 BOM 导入 |

### 依赖传递与排除

```xml
<!-- ⭐ 依赖传递：A → B → C，A 自动获得 C -->

<!-- ⭐ 排除传递性依赖 -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>some-library</artifactId>
    <version>1.0</version>
    <exclusions>
        <exclusion>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
        </exclusion>
        <exclusion>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

### 依赖冲突

Maven 处理冲突的两条原则：

1. **最短路径优先**：`A → B → C → D 1.0` 和 `A → D 2.0` 选 2.0
2. **最先声明优先**：相同路径长度，先声明的生效

```bash
# 查看依赖树，排查冲突
mvn dependency:tree
mvn dependency:tree -Dincludes=org.springframework:spring-core
```

```txt
com.demo:my-app:jar:1.0.0
├── org.springframework.boot:spring-boot-starter-web:jar:3.2.5
│   ├── org.springframework.boot:spring-boot-starter:jar:3.2.5
│   │   └── org.springframework.boot:spring-boot:jar:3.2.5
│   └── org.springframework:spring-webmvc:jar:6.1.6
├── org.mybatis:mybatis:jar:3.5.16
│   └── org.springframework:spring-jdbc:jar:6.1.8 (omitted)
└── ...
```

### dependencyManagement

```xml
<!-- ⭐ 父 POM 中统一管理版本——子模块无需写 version -->

<!-- parent/pom.xml -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>  <!-- ⭐ BOM 导入 -->
        </dependency>

        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
            <version>3.5.9</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

```xml
<!-- child/pom.xml——无需写 version -->
<dependencies>
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
        <!-- version 继承自父 POM -->
    </dependency>
</dependencies>
```

---

## 四、生命周期 ⭐

### 三套生命周期

```
clean 生命周期：清理构建产物
    pre-clean → clean → post-clean

default 生命周期：核心构建（最常用）
    validate → compile → test → package → verify → install → deploy

site 生命周期：生成项目文档
    pre-site → site → post-site → site-deploy
```

### 常用命令

```bash
# ⭐ 日常开发
mvn clean           # 清理 target/
mvn compile         # 编译源代码到 target/classes
mvn test            # 运行测试
mvn package         # 打包为 jar/war
mvn install         # 安装到本地仓库
mvn deploy          # 部署到远程仓库

# ⭐ 组合命令
mvn clean install   # 先清理再安装（最常用）
mvn clean package   # 先清理再打包
mvn clean test      # 先清理再测试

# ⭐ 跳过测试
mvn package -DskipTests         # 跳过编译测试
mvn package -Dmaven.test.skip=true  # 完全跳过测试

# ⭐ 指定 profile
mvn package -P production
```

### 阶段绑定与插件

```xml
<!-- ⭐ Maven 的生命周期阶段由插件执行 -->
<build>
    <plugins>
        <!-- 编译插件 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.13.0</version>
            <configuration>
                <source>17</source>
                <target>17</target>
            </configuration>
        </plugin>

        <!-- 测试插件 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
        </plugin>

        <!-- JAR 打包插件 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.4.1</version>
        </plugin>
    </plugins>
</build>
```

---

## 五、聚合与继承 ⭐

### 多模块项目结构

```
my-project/
├── pom.xml                    # 父 POM（packaging = pom）
├── my-common/                 # 公共模块
│   └── pom.xml
├── my-domain/                 # 领域模型
│   └── pom.xml
├── my-service/                # 业务服务
│   └── pom.xml
└── my-web/                    # Web 接口
    └── pom.xml
```

### 父 POM

```xml
<!-- ⭐ 父 POM：packaging 为 pom -->
<groupId>com.demo</groupId>
<artifactId>my-project</artifactId>
<version>1.0.0</version>
<packaging>pom</packaging>

<!-- 聚合子模块 -->
<modules>
    <module>my-common</module>
    <module>my-domain</module>
    <module>my-service</module>
    <module>my-web</module>
</modules>

<!-- ⭐ 统一版本管理 -->
<properties>
    <java.version>17</java.version>
    <spring-boot.version>3.2.5</spring-boot.version>
</properties>

<!-- 依赖版本管理（子模块可不用写版本） -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 子模块

```xml
<!-- ⭐ 子模块通过 <parent> 继承父 POM -->
<modelVersion>4.0.0</modelVersion>

<parent>
    <groupId>com.demo</groupId>
    <artifactId>my-project</artifactId>
    <version>1.0.0</version>
</parent>

<artifactId>my-domain</artifactId>
<!-- 继承父 POM 的 groupId/version，子模块只需写 artifactId -->
```

```xml
<!-- 其他子模块引用兄弟模块 -->
<dependencies>
    <dependency>
        <groupId>com.demo</groupId>
        <artifactId>my-common</artifactId>
        <version>${project.version}</version>  <!-- 跟随父版本 -->
    </dependency>
</dependencies>
```

```bash
# 构建全部模块（在父目录执行）
mvn clean install

# 构建单个模块
mvn clean install -pl my-service -am
# -pl: 指定模块
# -am: 同时构建依赖模块
```

---

## 六、常用插件

### Spring Boot 打包

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <version>3.2.5</version>
            <!-- 打成可执行 fat JAR -->
            <executions>
                <execution>
                    <goals>
                        <goal>repackage</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 编译器插件

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.13.0</version>
    <configuration>
        <source>17</source>
        <target>17</target>
        <encoding>UTF-8</encoding>
        <parameters>true</parameters>  <!-- 保留方法参数名 -->
    </configuration>
</plugin>
```

### 资源过滤

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>  <!-- 启用占位符替换 -->
            <includes>
                <include>**/*.properties</include>
                <include>**/*.yml</include>
            </includes>
        </resource>
    </resources>
</build>
```

```properties
# application.properties 中的占位符被替换为 pom.xml 的值
app.version=${project.version}
app.name=${project.name}
```

### 其他常用插件

| 插件 | 用途 |
|:----|:----|
| `maven-surefire-plugin` | 运行单元测试 |
| `maven-failsafe-plugin` | 运行集成测试 |
| `maven-source-plugin` | 打包源码 |
| `maven-javadoc-plugin` | 生成 Javadoc |
| `maven-assembly-plugin` | 自定义打包（含依赖） |
| `maven-shade-plugin` | 打包可执行 uber-jar |
| `maven-release-plugin` | 发布管理 |
| `org.owasp:dependency-check-maven` | 依赖安全漏洞检查 |
| `org.jacoco:jacoco-maven-plugin` | 测试覆盖率 |

---

## 七、仓库与私服

### 仓库类型

```
本地仓库（Local）—— ~/.m2/repository
    │
    ▼
中央仓库（Central）—— https://repo.maven.apache.org/maven2
    │
    ▼
远程仓库（Remote）—— 公司私服 / 镜像站
```

### 配置远程仓库

```xml
<repositories>
    <repository>
        <id>aliyun</id>
        <name>阿里云</name>
        <url>https://maven.aliyun.com/repository/public</url>
        <releases>
            <enabled>true</enabled>
            <checksumPolicy>warn</checksumPolicy>
        </releases>
        <snapshots>
            <enabled>true</enabled>
            <updatePolicy>always</updatePolicy>  <!-- SNAPSHOT 更新策略 -->
        </snapshots>
    </repository>
</repositories>
```

### 私服（Nexus）

```bash
# 部署到私服
mvn deploy -DaltDeploymentRepository=my-repo::default::http://nexus:8081/repository/maven-releases/
```

```xml
<!-- 私服配置优先 -->
<distributionManagement>
    <repository>
        <id>nexus-releases</id>
        <url>http://nexus:8081/repository/maven-releases/</url>
    </repository>
    <snapshotRepository>
        <id>nexus-snapshots</id>
        <url>http://nexus:8081/repository/maven-snapshots/</url>
    </snapshotRepository>
</distributionManagement>
```

### settings.xml 服务器认证

```xml
<servers>
    <server>
        <id>nexus-releases</id>  <!-- 与 repository 的 id 对应 -->
        <username>admin</username>
        <password>admin123</password>
    </server>
    <server>
        <id>nexus-snapshots</id>
        <username>admin</username>
        <password>admin123</password>
    </server>
</servers>
```

---

## 八、Profile

### 多环境配置

```xml
<!-- ⭐ Profile 实现多环境切换 -->
<profiles>
    <!-- 开发环境 -->
    <profile>
        <id>dev</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <properties>
            <env>dev</env>
            <db.url>jdbc:mysql://localhost:3306/demo</db.url>
        </properties>
    </profile>

    <!-- 测试环境 -->
    <profile>
        <id>test</id>
        <properties>
            <env>test</env>
            <db.url>jdbc:mysql://test-server:3306/demo</db.url>
        </properties>
    </profile>

    <!-- 生产环境 -->
    <profile>
        <id>prod</id>
        <properties>
            <env>prod</env>
            <db.url>jdbc:mysql://prod-server:3306/demo</db.url>
        </properties>
    </profile>
</profiles>
```

```bash
mvn package -P prod          # 使用生产环境配置
mvn package -P dev           # 使用开发环境配置
mvn package -P test          # 使用测试环境配置
mvn package -P dev,test      # 同时启用多个 profile
```

### 激活方式

```xml
<!-- 1. 命令行 -P -->
mvn package -P prod

<!-- 2. 默认激活 -->
<activation>
    <activeByDefault>true</activeByDefault>
</activation>

<!-- 3. 按系统属性 -->
<activation>
    <property>
        <name>env</name>
        <value>prod</value>
    </property>
</activation>

<!-- 4. 按 JDK 版本 -->
<activation>
    <jdk>17</jdk>
</activation>

<!-- 5. 按操作系统 -->
<activation>
    <os>
        <name>Linux</name>
    </os>
</activation>

<!-- 6. 按文件是否存在 -->
<activation>
    <file>
        <exists>target/config.properties</exists>
    </file>
</activation>
```

---

## 九、Archetype（项目模板）

```bash
# ⭐ 从 archetype 创建项目骨架
mvn archetype:generate

# 常用 archetype
mvn archetype:generate \
    -DgroupId=com.demo \
    -DartifactId=my-app \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DarchetypeVersion=1.5 \
    -DinteractiveMode=false
```

```bash
# ⭐ 创建自定义 archetype（从已有项目）
cd existing-project
mvn archetype:create-from-project
# 生成的 archetype 在 target/generated-sources/archetype/

# 安装到本地仓库
cd target/generated-sources/archetype/
mvn install

# 使用自定义 archetype
mvn archetype:generate \
    -DarchetypeGroupId=com.demo \
    -DarchetypeArtifactId=my-archetype \
    -DarchetypeVersion=1.0.0
```

---

## 十、常见问题与技巧

### 依赖下载慢

```bash
# 1. 配置阿里云镜像（settings.xml）
# 2. 使用 -o 离线模式（如果依赖已下载）
mvn compile -o
```

### 依赖冲突警告

```bash
# 查看依赖树
mvn dependency:tree

# 排除冲突依赖
# 在 pom.xml 中添加 <exclusions>
```

### 编译内存不足

```bash
# 设置 MAVEN_OPTS
export MAVEN_OPTS="-Xmx1024m -Xms512m"
# 或
mvn package -Dmaven.options="-Xmx1024m"
```

### 多线程构建

```bash
# ⭐ 多核加速
mvn clean install -T 4               # 4 线程
mvn clean install -T 1C              # CPU 核心数
mvn clean install -T 1.5C            # 1.5 倍核心数
```

### 常用命令速查

| 命令 | 用途 |
|:----|:-----|
| `mvn clean` | 清理 target |
| `mvn compile` | 编译源代码 |
| `mvn test` | 运行测试 |
| `mvn package` | 打包 |
| `mvn install` | 安装到本地仓库 |
| `mvn deploy` | 部署到远程仓库 |
| `mvn clean install -DskipTests` | 跳过测试 |
| `mvn dependency:tree` | 查看依赖树 |
| `mvn dependency:resolve` | 解析所有依赖 |
| `mvn help:effective-pom` | 查看最终生效的 POM |
| `mvn help:active-profiles` | 查看当前激活的 profile |
| `mvn versions:display-dependency-updates` | 检查依赖更新 |
| `mvn versions:set -DnewVersion=2.0.0` | 批量修改版本号 |

---

## 十一、常见面试题

### 1. Maven 的三大生命周期是什么？

> **clean**（清理）、**default**（核心构建：编译→测试→打包→部署）、**site**（生成项目站点）。执行一个阶段会自动触发该生命周期中之前的所有阶段。

### 2. 说说 Maven 的依赖传递原则和冲突解决？

> 依赖传递让 A→B→C 时 A 自动获得 C。**最短路径优先**（距离短的版本胜出），**最先声明优先**（路径相同时先声明的胜出）。用 `mvn dependency:tree` 排查。

### 3. 你们项目怎么统一管理版本号？

> 用父 POM 的 `<dependencyManagement>` 统一管理版本号，子模块只声明依赖不写版本。同时使用 `<properties>` 集中定义版本变量如 `<spring.boot.version>3.2.5</spring.boot.version>`。Spring Boot 项目一般通过 BOM 引入 `spring-boot-dependencies`。

### 4. Maven 和 Gradle 有什么区别？

> Maven 基于 XML（POM），约定优于配置，学习曲线较平缓。Gradle 基于 Groovy/Kotlin DSL，更灵活、性能更好（增量构建、构建缓存），适合大型项目。Gradle 现在是 Android 官方构建工具，Spring Boot 也官方支持 Gradle。

### 5. 什么是 SNAPSHOT 版本？

> SNAPSHOT 表示**开发中的不稳定版本**。每次构建时会检查远程仓库是否有新版本（默认每天一次，可通过 `<updatePolicy>` 配置）。发布版是**不可变**的，SNAPSHOT 可被覆盖。

### 6. 如何跳过测试？

> `mvn package -DskipTests`（跳过测试编译和执行）或 `mvn package -Dmaven.test.skip=true`（完全跳过测试相关的所有操作）。前者在 IDEA 中更常用。

---

> [!tip] **学习路径建议**
> 1. **入门**：安装配置 → 核心概念（坐标、仓库、生命周期）→ 常用命令
> 2. **进阶**：POM 详解 → 依赖管理 → scope → 依赖冲突排查
> 3. **工程化**：聚合与继承 → 多模块项目 → Profile 多环境
> 4. **深入**：插件开发 → Archetype → 私服搭建（Nexus）→ 构建优化
