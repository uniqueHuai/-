# LangChain4j

## 一、什么是 LangChain4j

### 定义

**LangChain4j** 是 LangChain 的 **Java 版本**，为 Java 生态提供了一套构建 AI Agent 应用的框架。诞生于 2023 年底，截至 2026 年 5 月最新版本为 **1.0.0-beta2**（已接近 GA）。

```
    LangChain (Python)              LangChain4j (Java)
    ┌──────────────────┐          ┌──────────────────┐
    │  Python 生态      │          │  Java 生态        │
    │                  │          │                  │
    │  LLM 抽象层      │          │  LLM 抽象层      │
    │  Chain / Agent   │          │  Chain / Agent   │
    │  Tool / Memory   │          │  Tool / Memory   │
    │  RAG / Document  │          │  RAG / Document  │
    │                  │          │                  │
    │  功能最全        │          │  Java 原生        │
    │  新功能最先发布   │          │  与 Spring 整合   │
    │  Python AI 标准  │          │  LLM 适配丰富     │
    └──────────────────┘          └──────────────────┘
```

### Spring AI vs LangChain4j

| 对比维度 | Spring AI | LangChain4j |
|:--------:|:---------:|:------------|
| **出品方** | Spring 官方 | 社区（非官方） |
| **架构整合** | ⭐ 与 Spring Boot 深度整合 | 与 Spring Boot 可整合（非强绑定） |
| **自动配置** | ⭐ Starter 一键配置 | 需手动配置 Bean |
| **Function Calling** | `@Tool` 注解 + 自动 JSON Schema | `@Tool` 注解 + 手动注册 |
| **Agent 能力** | 基础 ChatClient + Tool Use | ⭐ Agent 类型更丰富 |
| **RAG** | ⭐ Document + VectorStore 完整方案 | 类似，但生态文档少 |
| **MCP 协议** | ⭐ 原生支持 | 社区适配器 |
| **模型适配** | 20+ 模型 | 20+ 模型 |
| **成熟度** | ⭐ 1.6.x 生产稳定 | 1.0.0-beta2 接近 GA |
| **学习成本** | ⭐ 低（Spring 开发者友好） | 中等（需额外学习框架概念） |

### 快速开始

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j</artifactId>
    <version>1.0.0-beta2</version>
</dependency>

<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-anthropic-spring-boot-starter</artifactId>
    <version>1.0.0-beta2</version>
</dependency>
```

```yaml
langchain4j:
  anthropic:
    api-key: ${ANTHROPIC_API_KEY}
    model: claude-4-sonnet-20260516
    max-tokens: 4096
    temperature: 0.7
```

```java
// 基础对话
ChatLanguageModel model = AnthropicChatModel.builder()
    .apiKey(System.getenv("ANTHROPIC_API_KEY"))
    .modelName("claude-4-sonnet-20260516")
    .build();

String answer = model.generate("什么是 AI Agent？");
System.out.println(answer);
```

---

## 二、核心功能

### LLM 抽象

```java
// ⭐ 统一接口，不同实现
ChatLanguageModel model;

// OpenAI
model = OpenAiChatModel.builder()
    .apiKey("sk-xxx")
    .modelName("gpt-5")
    .build();

// Anthropic
model = AnthropicChatModel.builder()
    .apiKey("sk-xxx")
    .modelName("claude-4-sonnet-20260516")
    .build();

// 本地 Ollama
model = OllamaChatModel.builder()
    .baseUrl("http://localhost:11434")
    .modelName("qwen4:7b")
    .build();

// 流式
model.generate("Java 17 的新特性有哪些？");
```

### ChatMemory

```java
// ⭐ 多种记忆实现
ChatMemory memory;

memory = MessageWindowChatMemory.builder()
    .maxMessages(20)              // 保留最近 20 条
    .build();

memory = TokenWindowChatMemory.builder()
    .maxTokens(100_000)           // 按 Token 限制
    .build();

// 使用记忆
Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .chatMemory(memory)
    .build();

String answer = assistant.chat("你好，我叫张三");
String answer2 = assistant.chat("我叫什么？");  // 记得"张三"
```

### Tool 支持

```java
// ⭐ @Tool 注解
public class CalculatorTools {

    @Tool("执行数学计算，传入数学表达式如 '2+3*4'")
    public double calculate(String expression) {
        return new ExpressionEvaluator().evaluate(expression);
    }

    @Tool("获取指定城市的当前时间")
    public String getCurrentTime(String city) {
        return timeService.getTime(city);
    }
}

// 注册工具
Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .tools(new CalculatorTools())
    .build();
```

### RAG

```java
// ⭐ 简单 RAG 实现
ContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .embeddingModel(embeddingModel)
    .maxResults(3)
    .minScore(0.7)
    .build();

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .contentRetriever(retriever)
    .build();

// 自动在每次回答前检索知识库
String answer = assistant.chat("公司的年假政策是什么？");
```

---

## 三、Agent 能力

LangChain4j 相比 Spring AI 的优势在于 **Agent 模式的丰富度**。

```java
// ⭐ Agent 构建
public interface CustomerServiceAgent {

    @SystemMessage("""
        你是客服助手。可以查询订单、处理退货、查询知识库。
        如果需要更复杂的信息，可以使用提供的工具。
        """)
    String chat(@V("userMessage") String message);
}

// 创建带工具的 Agent
CustomerServiceAgent agent = AiServices.builder(CustomerServiceAgent.class)
    .chatLanguageModel(model)
    .chatMemory(MessageWindowChatMemory.builder()
        .maxMessages(20).build())
    .tools(
        new OrderTools(),
        new ReturnTools(),
        new KnowledgeBaseTools()
    )
    .build();

String response = agent.chat("查询我的订单状态");
```

### 多 Agent 协作

```java
// ⭐ 两个 Agent 分工
public interface AnalyzerAgent {
    @SystemMessage("你负责分析需求，制定执行计划")
    String analyze(@V("requirement") String requirement);
}

public interface ExecutorAgent {
    @SystemMessage("你负责根据计划执行具体任务")
    String execute(@V("plan") String plan);
}

// 编排
AnalyzerAgent analyzer = AiServices.builder(AnalyzerAgent.class)
    .chatLanguageModel(model).build();
ExecutorAgent executor = AiServices.builder(ExecutorAgent.class)
    .chatLanguageModel(model).build();

String plan = analyzer.analyze("实现用户登录功能");
String result = executor.execute(plan);
```

---

## 四、Spring Boot 整合

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-anthropic-spring-boot-starter</artifactId>
    <version>1.0.0-beta2</version>
</dependency>
```

```java
// ⭐ 自动配置
@Service
public class LangChain4jService {

    private final ChatLanguageModel model;
    private final EmbeddingModel embeddingModel;

    public LangChain4jService(ChatLanguageModel model,
                               EmbeddingModel embeddingModel) {
        this.model = model;
        this.embeddingModel = embeddingModel;
    }

    public String chat(String message) {
        return model.generate(message);
    }
}
```

---

## 五、Spring AI vs LangChain4j 选择指南

### 选 Spring AI 当：
- 你的项目已经是 **Spring Boot 全家桶**
- 需要开箱即用的自动配置
- 重视 **MCP 协议** 的原生支持
- 团队熟悉 Spring 生态
- 需要官方长期维护和稳定性

### 选 LangChain4j 当：
- 需要 **更丰富的 Agent 模式**
- 项目不是 Spring Boot（纯 Java SE 或其他框架）
- 需要和已有 Python LangChain 项目保持概念一致
- 追求最大灵活度，愿意手动配置

### 也可以混用

```java
// ⭐ 部分项目混用两者
// Spring AI 做：基础 ChatClient + RAG + MCP
// LangChain4j 做：复杂的 Agent 编排

// 但注意：混用会增加依赖复杂度和学习成本
// 大部分场景选一个就够了
```

---

> [!tip] **使用建议**
> 对于你（Java + Spring Boot 开发者），**推荐首选 Spring AI**。Spring AI 1.6.x 已经非常成熟，覆盖了 90% 的 AI Agent 开发需求，且与 Spring Boot 生态无缝衔接。LangChain4j 可以作为补充参考，当 Spring AI 不支持的特定功能时再考虑引入。
