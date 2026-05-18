# Spring AI 实战

## 一、Spring AI 概述

### 什么是 Spring AI

**Spring AI** 是 Spring 生态官方出品的 **AI 工程化框架**，为 Java 开发者提供了一套统一、高质量的 API 来对接 LLM、Vector Store、 embedding 模型等 AI 能力。截至 2026 年 5 月，最新稳定版为 **Spring AI 1.6.x**。

```
           Spring AI 架构
                              ┌──────────────────┐
                              │   Spring Boot     │
                              │   (自动配置)       │
                              └────────┬─────────┘
                                       │
                              ┌────────┴─────────┐
                              │   Spring AI Core   │
                              │   ChatClient       │
                              │   ToolCallback     │
                              │   Document API     │
                              └────────┬─────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │              │              │              │              │
         ▼              ▼              ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ OpenAI   │  │ Anthropic │  │  Ollama  │  │  DashScope│  │ 其他模型  │
   │ (GPT-5)  │  │(Claude 4) │  │(Qwen/Llama)│  │ (通义千问)│  │ (共 20+) │
   └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ PGVector │  │ Milvus   │  │ Redis    │  │ Chroma   │
   │ (向量库)  │  │ (向量库)  │  │ (向量库)  │  │ (向量库)  │
   └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### 核心特性（1.6.x）

| 特性 | 说明 |
|:----|:-----|
| **ChatClient** | 流式流畅的 AI 对话 API，支持 chainable 调用 |
| **多模型支持** | OpenAI、Anthropic、Ollama、DashScope、Azure 等 20+ 模型 |
| **Function Calling** | `@Tool` 注解，自动 JSON Schema，支持并行调用 |
| **RAG 支持** | Document 处理、向量检索、Prompt 模板一站式方案 |
| **MCP 协议** | 原生支持 MCP Server/Client，行业标准工具协议 |
| **多模态** | 图片理解、音频转文字、文本转图片 |
| **Advisor** | 可插拔的拦截器链（日志/安全/缓存/上下文） |
| **Spring Boot 3.x** | 自动配置、starter、Actuator 端点监控 |

---

## 二、快速开始

### 环境准备

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.4.6</version>
</parent>

<dependencies>
    <!-- ⭐ Spring AI 核心 -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
        <version>1.6.2</version>
    </dependency>

    <!-- Anthropic Claude -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-anthropic-spring-boot-starter</artifactId>
        <version>1.6.2</version>
    </dependency>

    <!-- 本地模型 (Ollama) -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-ollama-spring-boot-starter</artifactId>
        <version>1.6.2</version>
    </dependency>

    <!-- 向量数据库 -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-pgvector-store-spring-boot-starter</artifactId>
        <version>1.6.2</version>
    </dependency>
</dependencies>
```

### 基础配置

```yaml
# application.yml
spring:
  ai:
    # ── OpenAI ──
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        options:
          model: gpt-5
          temperature: 0.7

    # ── Anthropic Claude ──
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-4-sonnet-20260516
          max-tokens: 4096

    # ── Ollama 本地模型 ──
    ollama:
      base-url: http://localhost:11434
      chat:
        options:
          model: qwen4:7b

    # ── 向量库 ──
    vectorstore:
      pgvector:
        table-name: knowledge_vectors
        dimensions: 1536
        initialize-schema: true
```

### 第一个对话

```java
@RestController
@RequiredArgsConstructor
public class ChatController {

    private final ChatClient chatClient;

    @GetMapping("/chat")
    public String chat(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .call()
            .content();
    }

    @GetMapping("/chat/stream")
    public Flux<String> streamChat(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .stream()
            .content();
    }
}
```

---

## 三、ChatClient 详解 ⭐

### ChatClient.Builder

```java
@Configuration
public class ChatClientConfig {

    @Bean
    public ChatClient chatClient(ChatClient.Builder builder) {
        return builder
            // 默认 System Prompt（所有对话生效）
            .defaultSystem("""
                你是资深 Java 开发助手。
                - 代码用 Java 17+ / Spring Boot 3.x
                - 给出完整代码，包含异常处理
                - 解释关键设计决策
                """)
            // 默认注册的 Function
            .defaultFunctions("getUser", "queryDatabase", "searchWeb")
            // 默认 Advisor（拦截器链）
            .defaultAdvisors(
                new LoggingAdvisor(),         // 日志
                new SimpleChatMemoryAdvisor(  // 会话记忆
                    chatMemory, 10)           // 保留最近10条
            )
            .build();
    }
}
```

### Prompt 模板

```java
// ⭐ 结构化 Prompt 模板
@Service
public class PromptTemplateService {

    private final ChatClient chatClient;

    public String reviewCode(String code, String language) {
        return chatClient.prompt()
            .user(u -> u
                .text("""
                    请审查以下 {language} 代码：

                    ```{language}
                    {code}
                    ```

                    审查维度：正确性、性能、安全、可维护性。
                    """
                )
                .param("language", language)
                .param("code", code)
            )
            .call()
            .content();
    }
}
```

### 流式输出

```java
// ⭐ SSE 流式输出——适合 AI 打字机效果
@RestController
public class StreamController {

    private final ChatClient chatClient;

    @GetMapping("/chat/stream")
    public Flux<String> stream(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .stream()
            .content();   // 逐 Token 推送

        // 或者使用 Flux<ChatResponse> 获取更详细的响应
    }

    // WebFlux SSE
    @GetMapping("/chat/sse")
    public Flux<ServerSentEvent<String>> sse(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .stream()
            .content()
            .map(token -> ServerSentEvent.builder(token)
                .event("token")
                .build()
            );
    }
}
```

### 多模型切换

```java
// ⭐ 一个系统对接多个模型
@Service
public class MultiModelService {

    // 分别注入不同模型的 ChatClient
    private final ChatClient claudeClient;     // 复杂推理
    private final ChatClient gptClient;        // 多模态
    private final ChatClient localClient;      // 简单任务

    public MultiModelService(
            @Qualifier("claudeChatClient") ChatClient claude,
            @Qualifier("gptChatClient") ChatClient gpt,
            @Qualifier("ollamaChatClient") ChatClient local) {
        this.claudeClient = claude;
        this.gptClient = gpt;
        this.localClient = local;
    }

    public String routeByTask(String task, TaskType type) {
        return switch (type) {
            case COMPLEX_REASONING -> claudeClient.prompt().user(task).call().content();
            case IMAGE_ANALYSIS   -> gptClient.prompt().user(task).call().content();
            case SIMPLE_QA        -> localClient.prompt().user(task).call().content();
        };
    }
}
```

---

## 四、Function Calling ⭐

### @Tool 注解

```java
@Service
public class OrderTools {

    @Tool(name = "query_order",
          description = "查询订单状态和物流信息。需提供订单号。")
    public Order queryOrder(
            @ToolParam(description = "订单号，格式 ORD-xxxx") String orderId) {

        return orderRepository.findById(orderId)
            .orElseThrow(() -> new RuntimeException("订单不存在"));
    }

    @Tool(description = "取消订单，仅待发货状态可取消。取消后自动退款。")
    public CancelResult cancelOrder(
            @ToolParam(description = "订单号") String orderId,
            @ToolParam(description = "取消原因", required = false) String reason) {

        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new RuntimeException("订单不存在"));

        return orderService.cancel(order, reason);
    }
}

// 使用
chatClient.prompt()
    .user("查询 ORD-2024-0001 的订单状态")
    .tools("query_order", "cancelOrder")  // 注册可用工具
    .call()
    .content();
```

### 结构化输出（Entity）

```java
// ⭐ 直接解析为 Java 对象
public record UserInfo(
    String name,
    int age,
    String email,
    List<String> skills
) {}

UserInfo user = chatClient.prompt()
    .user("从以下文本提取用户信息：张三，28岁，邮箱zhangsan@test.com，"
        + "技能包括 Java、Spring、Kubernetes")
    .call()
    .entity(UserInfo.class);  // ⭐ 自动解析 JSON → Java 对象

System.out.println(user.name());   // 张三
System.out.println(user.skills()); // [Java, Spring, Kubernetes]
```

### 多工具协作

```java
// ⭐ Agent 自动编排多步工具调用
// 用户："查一下用户1001的订单状态，如果已发货就发短信通知"

// Agent 的内部执行流程：
// 1. LLM 调用 queryUser(1001) → 获取用户信息（含手机号）
// 2. LLM 调用 queryOrders(1001) → 获取订单状态
// 3. LLM 判断订单已发货 → 调用 sendSms(手机号, "您的订单已发货")
// 4. LLM 回复用户
```

---

## 五、RAG 实战 ⭐

### 文档索引

```java
@Service
public class KnowledgeIndexService {

    private final VectorStore vectorStore;
    private final DocumentProcessor documentProcessor;

    /**
     * 将文档导入向量知识库
     */
    public void indexDocuments(List<String> filePaths) {
        for (String path : filePaths) {
            // 1. 读取文档
            Document doc = new Document(Resource.fromFile(path));

            // 2. 分块处理
            List<Document> chunks = documentProcessor.process(List.of(doc));

            // 3. 写入向量库
            vectorStore.write(chunks);

            log.info("已索引：{} → {} 个块", path, chunks.size());
        }
    }
}

// 自动同步
@Component
public class DocumentSyncJob {

    @Scheduled(cron = "0 0 3 * * ?")  // 每天凌晨3点
    public void syncKnowledgeBase() {
        List<String> changedFiles = gitService.getChangedFiles();
        if (!changedFiles.isEmpty()) {
            indexService.indexDocuments(changedFiles);
        }
    }
}
```

### RAG 查询

```java
@Service
public class RagQueryService {

    private final VectorStore vectorStore;
    private final ChatClient chatClient;

    public String query(String question) {
        // 1. 检索
        List<Document> docs = vectorStore.similaritySearch(
            SearchRequest.query(question)
                .withTopK(3)
                .withSimilarityThreshold(0.7)
        );

        // 2. 构建上下文
        String context = docs.stream()
            .map(d -> String.format(
                "[来源：%s]\n%s",
                d.getMetadata().get("source"),
                d.getContent()))
            .collect(Collectors.joining("\n\n---\n\n"));

        // 3. 生成回答
        return chatClient.prompt()
            .user(u -> u
                .text("""
                    基于以下资料回答问题。
                    如果资料不足以回答，请明确说明。
                    在回答末尾列出参考来源。

                    资料：
                    {context}

                    问题：{question}
                    """)
                .param("context", context)
                .param("question", question)
            )
            .call()
            .content();
    }

    // ⭐ 流式 RAG
    public Flux<String> streamQuery(String question) {
        List<Document> docs = vectorStore.similaritySearch(
            SearchRequest.query(question).withTopK(3));

        String context = docs.stream()
            .map(Document::getContent)
            .collect(Collectors.joining("\n"));

        return chatClient.prompt()
            .user(u -> u
                .text("基于以下资料回答问题：\n{context}\n问题：{question}")
                .param("context", context)
                .param("question", question))
            .stream()
            .content();
    }
}
```

### Agentic RAG

```java
// ⭐ Agent 自主决定是否检索、何时检索
@Service
public class AgenticRagService {

    @Tool(description = "搜索内部知识库。"
          + "当你需要产品文档、技术文档、流程说明时调用此工具。")
    public String searchKnowledgeBase(
            @ToolParam(description = "搜索关键词，提取核心名词") String query) {
        return vectorStore.similaritySearch(
            SearchRequest.query(query).withTopK(3))
            .stream()
            .map(d -> d.getContent() + "\n[来源：" + d.getMetadata("source") + "]")
            .collect(Collectors.joining("\n\n"));
    }

    @Tool(description = "搜索互联网获取实时信息")
    public String searchWeb(
            @ToolParam(description = "搜索关键词") String query) {
        return webSearchService.search(query);
    }

    public String process(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .functions("searchKnowledgeBase", "searchWeb")
            .call()
            .content();
        // Agent 自主判断：简单问题直接回答，
        // 需要知识库时调 searchKnowledgeBase，
        // 需要实时信息时调 searchWeb
    }
}
```

---

## 六、Advisor 机制 ⭐

Spring AI 的 Advisor 是类似 Servlet Filter / Spring Interceptor 的可插拔拦截链。

### 内置 Advisor

```java
@Bean
public ChatClient chatClient(ChatClient.Builder builder) {
    return builder
        .defaultAdvisors(
            // 1. 日志记录
            new LoggingAdvisor(),

            // 2. 对话记忆（保留最近 N 条）
            new SimpleChatMemoryAdvisor(chatMemory, 20),

            // 3. 安全审查
            new GuardrailAdvisor(guardrails),

            // 4. Token 用量统计
            new TokenUsageAdvisor()
        )
        .build();
}
```

### 自定义 Advisor

```java
// ⭐ 自定义 Advisor——实现请求前后的拦截逻辑
@Component
public class AuditAdvisor implements ChatClientAdvisor {

    @Override
    public AdvisedResponse aroundCall(AdvisedRequest request,
                                       CallAroundAdvisorChain chain) {
        // 前置处理
        long start = System.nanoTime();
        log.info("用户请求：{}", request.userText());

        // 执行调用链
        AdvisedResponse response = chain.nextAroundCall(request);

        // 后置处理
        long elapsed = (System.nanoTime() - start) / 1_000_000;
        log.info("响应耗时：{}ms，Token 用量：{}",
            elapsed, response.getTokenUsage());

        // 审计日志
        auditService.log(request.userText(),
                        response.getResponse(),
                        elapsed);

        return response;
    }

    @Override
    public Flux<AdvisedResponse> aroundStream(
            AdvisedRequest request,
            StreamAroundAdvisorChain chain) {
        // 流式版本类似
        return chain.nextAroundStream(request);
    }

    @Override
    public String getName() {
        return "AuditAdvisor";
    }
}
```

---

## 七、生产配置

### 重试与熔断

```yaml
spring:
  ai:
    retry:
      max-attempts: 3              # 最大重试次数
      backoff:
        initial-interval: 1000     # 初始间隔 1s
        multiplier: 2              # 指数退避
        max-interval: 10000        # 最大间隔 10s

    circuit-breaker:
      enabled: true
      failure-threshold: 5
      timeout: 30s
```

### 监控（Actuator）

```yaml
# 暴露 AI 监控端点
management:
  endpoints:
    web:
      exposure:
        include: ai, health, metrics

  endpoint:
    ai:
      enabled: true
```

```bash
# 通过 Actuator 查看 AI 运行状态
GET /actuator/ai/info       # 模型配置、可用工具
GET /actuator/ai/metrics    # Token 用量、延迟、调用次数
GET /actuator/health        # 各模型连接状态
```

### 多环境配置

```yaml
# application-dev.yml —— 开发用本地模型
spring:
  ai:
    ollama:
      base-url: http://localhost:11434
      chat:
        options:
          model: qwen4:7b

---
# application-prod.yml —— 生产用商业模型
spring:
  ai:
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-4-sonnet-20260516
    retry:
      max-attempts: 3
```

---

## 八、常见问题

### 1. Spring AI 和 LangChain4j 怎么选？

> **Spring AI** 是 Spring 官方出品，与 Spring Boot 深度整合（自动配置、Actuator、@Tool 注解），如果你的项目已经是 Spring Boot 生态，**优先选 Spring AI**。LangChain4j 在某些高级功能上更多样（如 Agent），但 Spring AI 1.6.x 已经覆盖了绝大多数需求。

### 2. 如何在 Spring AI 中切换模型？

> 换依赖即可。例如把 `spring-ai-openai-starter` 换成 `spring-ai-anthropic-starter`，改一下 `spring.ai.anthropic.api-key` 配置，代码几乎不用动。或者通过 `@Qualifier` 注入多个 ChatClient Bean，不同场景用不同模型。

### 3. 怎么处理 Token 限流？

> 配置 `spring.ai.retry` 自动重试，配合 `Resilience4j` 熔断。也可以在 Advisors 层做请求排队和限速。生产环境建议同时配置语义缓存减少重复请求。

### 4. 流式 RAG 怎么实现？

> 先同步检索向量库获取上下文，然后用 `ChatClient` 的 `stream()` 方法生成回答。前端配合 SSE（Server-Sent Events）实现打字机效果。参考上面 `RagQueryService.streamQuery()` 的完整实现。

---

> [!tip] **学习路径建议**
> 1. **入门**：Spring Boot 整合 → ChatClient 基础对话 → 流式输出
> 2. **进阶**：@Tool Function Calling → 结构化输出 Entity → 多模型切换
> 3. **深入**：RAG 索引+查询 → Agentic RAG → Advisor 自定义拦截链
> 4. **工程化**：多环境配置 → 重试熔断 → Actuator 监控 → 生产部署


---

> **📖 学习路线**：[[AIAgent篇/README|AI Agent 学习路线图]]
