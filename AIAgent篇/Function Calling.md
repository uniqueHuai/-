# Function Calling

## 一、什么是 Function Calling

### 定义

**Function Calling（函数调用）** 是 LLM 在生成回复时，识别出需要调用外部工具/API 并输出**结构化调用参数**的能力。它是 AI Agent 与外部世界交互的核心机制。

```
    用户："查询 ID 为 1001 的用户信息"
              │
              ▼
    ┌─────────────────────┐
    │       LLM           │
    │                     │
    │  "用户需要查数据库，   │
    │   调用 getUser 工具"  │
    │                     │
    │  输出：              │
    │  {                   │
    │    tool: "getUser",  │
    │    args: {           │
    │      userId: 1001   │
    │    }                │
    │  }                   │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │     Agent 运行时     │
    │                     │
    │  解析 LLM 输出      │
    │  匹配到 getUser 工具 │
    │  调用 getUser(1001) │
    │                     │
    │  获取结果：{         │
    │    "name": "张三",   │
    │    "email": "..."   │
    │  }                  │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │    LLM（第二次）     │
    │                     │
    │  "用户信息已查到，    │
    │   向用户展示结果"    │
    └─────────────────────┘
```

### Function Calling vs 传统 API 调用

| 对比 | 传统 API 调用 | LLM Function Calling |
|:----|:-------------|:-------------------|
| **调用者** | 开发者硬编码调用逻辑 | LLM 自主决定何时调用 |
| **参数决定** | 开发者写死参数 | LLM 根据语义生成参数 |
| **灵活性** | 固定流程 | 动态选择工具 |
| **错误处理** | try-catch 预定义 | LLM 自动重试/换工具 |
| **组合方式** | 开发者编排 | LLM 自主编排多工具 |
| **新增工具** | 修改代码+重新部署 | 注册工具描述即可 |

---

## 二、核心原理

### 工作流程

```
Step 1: 工具注册
    ┌─────────────────────────────┐
    │  开发者定义工具（@Tool）       │
    │  - 函数名                    │
    │  - 描述                      │
    │  - 参数 Schema（JSON Schema） │
    └─────────────┬───────────────┘
                  │
Step 2: 注入 System Prompt
                  │
                  ▼
    ┌─────────────────────────────┐
    │  System Prompt 自动附加：     │
    │  "可用工具：                  │
    │   - getUser(userId: Long):   │
    │     根据ID查询用户信息"       │
    └─────────────┬───────────────┘
                  │
Step 3: LLM 推理
                  │
                  ▼
    ┌─────────────────────────────┐
    │  LLM 判断需要调用工具         │
    │  输出结构化参数               │
    │  → tool_call_id + name + args│
    └─────────────┬───────────────┘
                  │
Step 4: 执行工具
                  │
                  ▼
    ┌─────────────────────────────┐
    │  Agent 运行时拦截输出         │
    │  执行对应函数                 │
    │  将结果返回给 LLM             │
    └─────────────┬───────────────┘
                  │
Step 5: 生成回复
                  │
                  ▼
    ┌─────────────────────────────┐
    │  LLM 基于工具结果生成最终回复  │
    │  "用户张三的信息如下：..."     │
    └─────────────────────────────┘
```

### JSON Schema 工具定义

每种工具的背后是一个 **JSON Schema** 描述：

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "获取指定城市的当前天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称，如 北京、上海、广州"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "温度单位"
        }
      },
      "required": ["city"]
    }
  }
}
```

LLM 的响应：

```json
{
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\": \"北京\", \"unit\": \"celsius\"}"
      }
    }
  ]
}
```

---

## 三、Spring AI 中的 Function Calling ⭐

### 方式一：@Tool 注解（推荐）

```java
// ⭐ 在 @Configuration 或 @Service 中定义工具
@Configuration
public class AgentTools {

    @Bean
    @Tool(name = "get_user", description = "根据用户ID查询用户信息")
    public Function<GetUserRequest, User> getUser() {
        return request -> userRepository.findById(request.userId())
                .orElseThrow(() -> new RuntimeException("用户不存在"));
    }

    @Bean
    @Tool(name = "send_email", description = "发送电子邮件")
    public Function<SendEmailRequest, String> sendEmail() {
        return request -> {
            mailSender.send(request.to(), request.subject(), request.body());
            return "邮件已发送至 " + request.to();
        };
    }

    @Bean
    @Tool(name = "search_web", description = "搜索互联网获取实时信息")
    public Function<SearchRequest, SearchResponse> searchWeb() {
        return request -> webSearchService.search(request.query());
    }
}

// ⭐ 请求/响应 POJO
public record GetUserRequest(Long userId) {}
public record User(Long id, String name, String email, Integer age) {}
public record SendEmailRequest(String to, String subject, String body) {}
public record SearchRequest(String query) {}
public record SearchResponse(List<SearchResult> results) {}
```

### 使用工具

```java
@Service
public class AgentService {

    private final ChatClient chatClient;

    public AgentService(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("你是一个智能助手，可以查询用户信息和发送邮件。")
            .build();
    }

    public String process(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .functions("get_user", "send_email", "search_web")  // ⭐ 注册可用工具
            .call()
            .content();
    }
}
```

### 方式二：编程式注册

```java
@Bean
public ChatClient chatClient(ChatClient.Builder builder) {
    return builder
        .defaultSystem("你是一个 AI 助手")
        .defaultTools(    // ⭐ 全局注册，所有对话可用
            new ToolCallbackBuilder()
                .name("calculate")
                .description("执行数学计算")
                .inputType(CalculateRequest.class)
                .toolFunction(request -> {
                    // 执行计算逻辑
                    return calculator.evaluate(request.expression());
                })
                .build()
        )
        .build();
}
```

### 方式三：流式 Function Calling

```java
// ⭐ 流式响应 + 工具调用
public Flux<String> streamWithTools(String message) {
    return chatClient.prompt()
        .user(message)
        .functions("get_user", "search_web")
        .stream()
        .content();  // 流式输出，工具调用在后台自动处理
}
```

---

## 四、高级 Function Calling 模式

### 并行工具调用 ⭐

2025+ 的模型支持一次调用多个工具：

```java
// 用户："查询用户1001的信息，同时查一下北京的天气"
// LLM 可能一次调用两个工具：

// LLM 输出：
// tool_call_1: getUser(userId: 1001)
// tool_call_2: getWeather(city: "北京")

// ⭐ Spring AI 自动处理并行调用
@Bean
public ChatClient parallelChatClient(ChatClient.Builder builder) {
    return builder
        .defaultSystem("你可以同时调用多个工具来提高效率")
        .defaultTools(getUser(), getWeather())
        .build();
}
// 框架会：同时执行两个工具 → 合并结果 → 交给 LLM 生成回复
```

### 工具调用链（多步推理）

```java
// ⭐ 复杂场景：Agent 自动编排多步工具调用
// 用户："给昨天注册的所有用户发送欢迎邮件"

// Agent 执行流程：
// Step 1: LLM → queryDatabase("昨天注册的用户")
// Step 2: 工具返回 [用户A, 用户B, 用户C]
// Step 3: LLM → sendEmail(用户A) + sendEmail(用户B) + sendEmail(用户C)
// Step 4: 全部发送成功

// Spring AI 中传递上下文：
public String sendWelcomeEmails() {
    return chatClient.prompt()
        .user("给昨天注册的所有用户发送欢迎邮件")
        .functions("query_database", "send_email")
        .call()
        .content();
    // Spring AI 自动维护多轮工具调用循环
}
```

### 工具选择策略

```java
// ⭐ 限制可用工具范围
@Service
public class OrderService {

    private final ChatClient chatClient;

    public String handleOrderQuery(String message) {
        return chatClient.prompt()
            .user(message)
            // 订单场景只暴露订单相关工具
            .functions("query_order", "cancel_order", "track_delivery")
            .call()
            .content();
    }

    public String handleUserQuery(String message) {
        return chatClient.prompt()
            .user(message)
            // 用户场景只暴露用户相关工具
            .functions("get_user", "update_profile", "list_orders")
            .call()
            .content();
    }
}
```

### 工具调用超时与重试

```java
@Bean
@Tool(name = "call_external_api",
      description = "调用外部第三方 API")
public Function<ApiRequest, ApiResponse> callExternalApi() {
    return request -> {
        try {
            // ⭐ 设置超时
            return restTemplate.exchange(
                request.url(),
                HttpMethod.GET,
                null,
                ApiResponse.class
            );
        } catch (ResourceAccessException e) {
            // ⭐ 超时后返回明确的错误信息，LLM 会决定是否重试
            throw new RuntimeException("API 调用超时，请稍后重试");
        } catch (Exception e) {
            throw new RuntimeException("API 调用失败：" + e.getMessage());
        }
    };
}
```

---

## 五、MCP 协议 ⭐

### 什么是 MCP

**MCP（Model Context Protocol）** 是 Anthropic 于 2024 年底提出、到 2026 年已成为行业标准的 **Agent 工具协议**。它定义了 Agent 与外部工具/数据源之间的标准化通信方式。

```
    传统方式（点对点集成）                 MCP 方式（标准化协议）
    ┌──────────────────┐              ┌──────────────────┐
    │  Agent           │              │  Agent           │
    │                  │              │                  │
    │  ├─ MySQL 驱动   │              │  MCP Client      │
    │  ├─ Redis 客户端  │              └────────┬─────────┘
    │  ├─ 阿里云 SDK   │                       │
    │  ├─ 微信 SDK     │              ┌────────┴─────────┐
    │  ├─ 钉钉 API     │              │   MCP Server      │
    │  └─ ...各 SDK    │              │                  │
    │                  │              │  ├─ 文件系统      │
    │  每个工具不同协议  │              │  ├─ 数据库        │
    │  每接一个要学新API │              │  ├─ 搜索引擎      │
    └──────────────────┘              │  ├─ API 网关      │
                                      │  └─ 自定义工具    │
                                      │                  │
                                      │  统一协议         │
                                      └──────────────────┘
```

### MCP 核心概念

```
┌──────────────────────────────────────────────────────────────┐
│                       MCP 架构                                │
│                                                              │
│  ┌─────────────┐          ┌──────────────────────────┐       │
│  │  AI Agent    │          │      MCP Server           │       │
│  │              │          │                          │       │
│  │  MCP Client  │◄── JSON-RPC ──►│  ├─ Tools（可调用工具） │       │
│  │              │   2.0     │  ├─ Resources（数据源）  │       │
│  │  Chat Client │  传输层    │  ├─ Prompts（提示模板）  │       │
│  └─────────────┘          └──────────────────────────┘       │
│                                                              │
│  发现：Client 连接 Server 后获取可用工具列表                     │
│  调用：Client 请求 → Server 执行 → 返回结果                    │
│  通知：Server 主动推送状态变更                                  │
└──────────────────────────────────────────────────────────────┘
```

### Spring AI + MCP

```java
// ⭐ Spring AI 对 MCP 的原生支持
@Configuration
public class McpConfig {

    // MCP Server 配置
    @Bean
    public McpServer mcpServer() {
        return McpServer.using(
            StdioServerTransport.builder()
                .command("node")
                .args("path/to/mcp-server.js")
                .build()
        );
    }

    // MCP 工具自动注册为 Spring AI 的 @Tool
    @Bean
    public McpToolAdapter mcpToolAdapter(McpServer mcpServer) {
        return new McpToolAdapter(mcpServer);
    }
}
```

```java
// ⭐ 使用 MCP 工具
@Service
public class McpAgentService {

    private final ChatClient chatClient;

    public String processWithMcp(String message) {
        return chatClient.prompt()
            .user(message)
            // MCP 注册的工具自动可用
            .call()
            .content();
    }
}
```

### MCP 工具示例

```python
# mcp-server.py —— Python MCP 服务器
from mcp.server import Server, stdio_server

app = Server("my-tools")

@app.tool()
def query_database(sql: str) -> list[dict]:
    """执行 SQL 查询"""
    # 执行查询逻辑
    return db.execute(sql)

@app.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件"""
    mail.send(to, subject, body)
    return f"邮件已发送至 {to}"

@app.tool()
def search_docs(keyword: str) -> list[str]:
    """搜索内部文档"""
    return docs.search(keyword)

if __name__ == "__main__":
    with stdio_server() as (read, write):
        app.run(read, write)
```

---

## 六、工具设计最佳实践 ⭐

### 工具定义原则

```java
// ✅ 好：清晰、具体、单一职责
@Tool(name = "get_user_by_id",
      description = "根据用户ID精确查询用户信息，返回用户姓名、邮箱、角色")
public Function<UserIdRequest, User> getUserById() { ... }

// ✅ 好：区分相似工具
@Tool(name = "search_users_by_name",
      description = "根据用户名模糊搜索用户列表，支持分页")
public Function<SearchUserRequest, PageResult<User>> searchUsersByName() { ... }

// ❌ 差：模糊、职责过多
@Tool(description = "查询用户信息")  // 太模糊
public Function<Map<String, Object>, Object> getUser() { ... }

// ❌ 差：把多个操作合在一个工具里
@Tool(description = "用户相关操作，可以增删改查")
public Function<UserOpRequest, Object> userOperation() { ... }
```

### 工具描述编写技巧

```java
// ⭐ 工具描述决定了 LLM 是否能正确选择工具

// ❌ 差：不够具体
@Tool(description = "查询订单")
public Function<OrderRequest, Order> queryOrder() { ... }

// ✅ 好：包含使用场景和边界
@Tool(name = "query_order",
      description = """
          查询订单详细信息。
          适用场景：用户询问订单状态、物流信息、订单详情。
          输入参数：必须提供 orderId（订单号，格式如 ORD-2024-xxxxx）。
          返回：订单状态、商品列表、金额、物流单号、预计送达时间。
          注意：只能查询当前登录用户的订单。
          """)
public Function<OrderRequest, Order> queryOrder() { ... }
```

### 参数设计原则

```java
// ✅ 好：精确的类型和描述
public record SearchProductRequest(
    @Schema(description = "关键词，支持模糊搜索", example = "手机")
    String keyword,

    @Schema(description = "分类ID，不传则搜索全部分类", required = false)
    Long categoryId,

    @Schema(description = "价格上限（元）", required = false)
    BigDecimal maxPrice,

    @Schema(description = "页码，从1开始", defaultValue = "1")
    int page,

    @Schema(description = "每页条数，最大100", defaultValue = "20")
    int size
) {}

// ❌ 差：模糊类型导致 LLM 理解困难
public record Request(
    String data,       // 这是啥？
    String params,     // 传什么？
    String info        // 不明确
) {}
```

### 错误处理

```java
@Bean
@Tool(name = "cancel_order",
      description = "取消订单，仅支持待发货状态的订单")
public Function<CancelRequest, CancelResult> cancelOrder() {
    return request -> {
        Order order = orderRepository.findById(request.orderId())
                .orElseThrow(() -> new RuntimeException("订单不存在"));

        return switch (order.status()) {
            case PENDING_SHIPMENT -> {
                order.cancel();
                yield new CancelResult(true, "订单已取消");
            }
            case SHIPPED ->
                // ⭐ 明确的错误信息帮助 LLM 理解
                throw new RuntimeException(
                    "订单已发货，无法取消。建议用户联系客服处理退货。"
                );
            case DELIVERED ->
                throw new RuntimeException(
                    "订单已完成，无法取消。请在订单页面申请售后。"
                );
            case CANCELLED ->
                throw new RuntimeException(
                    "该订单已被取消，无需重复操作。"
                );
        };
    };
}
```

---

## 七、Function Calling 在 Agent 中的应用

### 完整 Agent 工具集示例

```java
@Configuration
public class CustomerServiceTools {

    // ========== 用户模块 ==========
    @Bean
    @Tool(description = "根据用户ID查询用户信息")
    public Function<UserIdReq, User> getUser() { ... }

    @Bean
    @Tool(description = "验证用户身份（需要用户名和密码）")
    public Function<AuthRequest, AuthResult> verifyIdentity() { ... }

    // ========== 订单模块 ==========
    @Bean
    @Tool(description = "查询订单状态和物流信息")
    public Function<OrderIdReq, Order> queryOrder() { ... }

    @Bean
    @Tool(description = "取消订单（仅待发货状态可取消）")
    public Function<CancelReq, CancelRes> cancelOrder() { ... }

    @Bean
    @Tool(description = "申请售后/退货")
    public Function<ReturnReq, ReturnRes> applyReturn() { ... }

    // ========== 客服模块 ==========
    @Bean
    @Tool(description = "搜索知识库获取常见问题答案")
    public Function<SearchReq, SearchRes> searchKnowledgeBase() { ... }

    @Bean
    @Tool(description = "创建工单转接人工客服（复杂问题）")
    public Function<TicketReq, TicketRes> createTicket() { ... }

    // ========== 通知模块 ==========
    @Bean
    @Tool(description = "给用户发送短信通知")
    public Function<SmsReq, String> sendSms() { ... }

    @Bean
    @Tool(description = "给用户发送邮件通知")
    public Function<EmailReq, String> sendEmail() { ... }
}
```

### 工具权限控制

```java
// ⭐ 基于用户角色的工具权限
@Service
public class SecuredAgentService {

    private final ChatClient chatClient;

    public String handleRequest(String userId, String role, String message) {
        Set<String> availableTools = getToolsForRole(role);

        return chatClient.prompt()
            .user(message)
            .functions(availableTools.toArray(new String[0]))
            .call()
            .content();
    }

    private Set<String> getToolsForRole(String role) {
        return switch (role) {
            case "ADMIN" -> Set.of("get_user", "query_order", "cancel_order",
                                   "refund_order", "search_kb", "send_email");
            case "AGENT" -> Set.of("get_user", "query_order", "search_kb", "create_ticket");
            case "USER"  -> Set.of("query_order", "search_kb");
            default      -> Set.of("search_kb");
        };
    }
}
```

---

## 八、监控与调试

### 工具调用日志

```java
// ⭐ 记录每次工具调用
@Component
public class ToolCallLogger {

    private final Logger log = LoggerFactory.getLogger(ToolCallLogger.class);

    @EventListener
    public void onToolCall(ToolCallEvent event) {
        log.info("""
            === Tool Call ===
            会话ID：{}
            工具名：{}
            输入参数：{}
            执行耗时：{}ms
            执行结果：{}
            是否成功：{}
            """,
            event.getSessionId(),
            event.getToolName(),
            event.getInputArgs(),
            event.getDurationMs(),
            event.getResult(),
            event.isSuccess()
        );
    }
}
```

### 调试要点

| 问题 | 排查方向 | 解决 |
|:----|:---------|:-----|
| **工具没被调用** | 工具描述是否清晰？ | 优化 `description` 字段 |
| **参数传错** | 参数 Schema 是否精确？ | 添加 `description` + `example` |
| **调用了不该用的工具** | 场景工具隔离？ | 按角色限制可用工具 |
| **工具调用失败后不重试** | 错误信息是否明确？ | 返回 LLM 可理解的错误提示 |
| **并行调用过多** | 是否真需要并行？ | 限制 `maxToolCalls` |
| **调用耗时太长** | 工具本身慢？ | 添加超时机制 |

---

## 九、常见面试题

### 1. Function Calling 的原理是什么？

> LLM 在训练时学习了工具调用的能力。开发者通过 JSON Schema 描述工具的签名和用途，LLM 在生成回复时判断是否需要调用工具，并输出结构化的调用参数。Agent 框架拦截这个输出，执行对应的函数，将结果返回给 LLM 生成最终回复。

### 2. 怎么让 LLM 准确选择工具？

> 三个关键：**工具名**清晰无歧义、**描述**包含使用场景和边界、**参数 Schema** 精确（类型、必填、枚举值）。还可以通过按场景隔离工具集来减少误选。

### 3. 工具调用失败了怎么办？

> 在工具函数中返回**清晰的结构化错误信息**，让 LLM 理解失败原因并决定下一步（重试、换参数、换工具、或告知用户）。同时设置调用次数上限防止无限循环。

### 4. MCP 协议解决了什么问题？

> 标准化 Agent 与工具的通信协议。以前每个工具集成方式不同（不同 SDK、不同认证方式），MCP 统一为 JSON-RPC 2.0 协议，一次实现到处可用。2026 年已成为行业标准。

### 5. Spring AI 的 Function Calling 和直接调用 API 有什么区别？

> 直接调用 API（如通过 `RestTemplate`）是开发者硬编码调用时机和参数。Spring AI 的 Function Calling 把调用决策权交给 LLM，`@Tool` 注解自动生成 JSON Schema，框架自动管理调用循环、上下文传递、流式响应等。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 Function Calling 流程 → `@Tool` 基本使用
> 2. **进阶**：并行调用 → 多步工具链 → 参数 Schema 优化
> 3. **深入**：MCP 协议 → 工具权限控制 → 错误恢复策略
> 4. **工程化**：监控与日志 → 测试与评估 → 生产部署
