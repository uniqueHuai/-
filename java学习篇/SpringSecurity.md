# 一.概念

本质上就是一串过滤器链，进行认证和过滤。（过滤在Servlet之前）

# 二.使用

## 1.引入依赖

- 如果你**没有自己写** `**@EnableWebSecurity**` **或自定义 SecurityFilterChain**，
- Spring Boot 会自动启用 `@EnableWebSecurity`，开启 Spring Security（默认登录页面）。

## 2.重写springsecurity配置类

注解@EnableWebSecurity，修饰类

@bean方法public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception

.addFilterBefore（后面写的过滤器）

## 3.写jwt配置类

配置密钥，过期时间

生成令牌、验证令牌、令牌提取用户名

## 4.过滤器处理token

从请求获取token，进行生成和验证功能（业务需求）。