# SpringSecurity

## 一、概念

Spring Security 本质上就是一串**过滤器链（Filter Chain）**，用于对请求进行**认证（Authentication）和授权（Authorization）**，在 Servlet 进入 Controller **之前**进行过滤拦截。

> [!info] **核心思路**
> 请求 → 过滤器链（依次执行多个过滤器）→ 若全部通过 → 到达 DispatcherServlet → Controller

---

## 二、使用步骤

### 1. 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

> [!tip] 如果你**没有自定义** `@EnableWebSecurity` 或 `SecurityFilterChain`，Spring Boot 会自动启用默认安全配置（跳转默认登录页面）。

---

### 2. 重写 Security 配置类

```java
@Configuration
@EnableWebSecurity  // 启用 Spring Security
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())                           // 禁用 CSRF（JWT 无状态）
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)) // 无状态 Session
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login", "/auth/**", "/css/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter(), UsernamePasswordAuthenticationFilter.class)
            .logout(logout -> logout
                .logoutSuccessUrl("/login?logout")
                .permitAll()
            );

        return http.build();
    }

    @Bean
    public JwtAuthenticationFilter jwtAuthFilter() {
        return new JwtAuthenticationFilter();
    }
}
```

---

### 3. 编写 JWT 配置类

配置 JWT 相关的 Bean：

- **密钥（SecretKey）**：用于签名和验证令牌
- **过期时间**：如 24 小时
- **核心方法**：
  - `generateToken(username)` — 生成令牌
  - `validateToken(token)` — 验证令牌
  - `getUsernameFromToken(token)` — 从令牌提取用户名

> 详见 [[登录认证篇#jwt|登录认证篇中的 JWT 部分]]

---

### 4. 过滤器处理 Token

编写过滤器继承 `OncePerRequestFilter`，重写 `doFilterInternal`：

1. 从请求头（`Authorization: Bearer <token>`）获取 token
2. 调用 JWT 工具类**验证 token**
3. 若有效，将用户信息存入 `SecurityContextHolder`
4. 放行请求

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {
        String token = extractToken(request);
        if (token != null && JwtUtils.validateToken(token)) {
            String username = JwtUtils.getUsernameFromToken(token);
            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(username, null, new ArrayList<>());
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        filterChain.doFilter(request, response);
    }

    private String extractToken(HttpServletRequest request) {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            return header.substring(7);
        }
        return null;
    }
}
```

---

## 三、核心概念总结

| 组件 | 作用 | 位置 |
|------|------|------|
| **SecurityFilterChain** | 配置安全过滤规则 | 配置类 |
| **JwtAuthenticationFilter** | 从请求中提取并验证 JWT | 过滤器链 |
| **SecurityContextHolder** | 存储当前登录用户信息 | 线程本地 |
| **@PreAuthorize** | 方法级别的权限控制 | Service/Controller |

> [!tip] **一句话记忆**
> Spring Security = **过滤器链** + **认证** + **授权**，通过在 Servlet 前拦截请求来实现安全控制。
