# Memory 与上下文管理

## 一、为什么 Agent 需要记忆

### 问题

LLM 本身是**无状态**的——每次调用都是独立的，不记得之前的对话。

```
    无状态 LLM（每次都是新开始）            有记忆的 Agent（持续学习）
    ┌──────────────┐                    ┌──────────────┐
    │  用户："我叫张三" │                    │  用户："我叫张三" │
    └──────┬───────┘                    └──────┬───────┘
           │                                   │
           ▼                                   ▼
    ┌──────────────┐                    ┌──────────────┐
    │  "你好！"     │                    │  "你好，张三！" │
    └──────────────┘                    └──────────────┘
           │                                   │
    ┌──────────────┐                    ┌──────────────┐
    │  用户："我叫什么？"│                    │  用户："我叫什么？"│
    └──────┬───────┘                    └──────┬───────┘
           │                                   │
           ▼                                   ▼
    ┌──────────────┐                    ┌──────────────┐
    │  "我不知道"   │                    │  "你叫张三"   │
    └──────────────┘                    └──────────────┘
```

### Agent 记忆的分类

```
                    Agent 记忆
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   短期记忆          长期记忆         工作记忆
   (会话内)         (跨会话)         (当前任务)
        │               │               │
        ▼               ▼               ▼
   Token 窗口     向量数据库       当前任务状态
   对话历史        用户画像       已完成步骤
   上下文         知识文档       中间结果
                历史经验       待办事项
```

---

## 二、记忆类型详解

### 1. 短期记忆（Short-Term Memory）

当前会话中所有交互的上下文，存在于 Token 窗口内。

```java
// ⭐ Spring AI 中的短期记忆——ChatMemory
@Service
public class ShortTermMemory {

    // 会话记忆存储（默认基于内存）
    private final ChatMemory chatMemory = new InMemoryChatMemory();

    public String chat(String sessionId, String userMessage) {
        // 1. 获取该会话的历史
        List<Message> history = chatMemory.get(sessionId, 10);  // 最近10条

        // 2. 发送给 LLM（历史 + 新消息）
        String response = chatClient.prompt()
            .messages(history)                 // 注入历史
            .user(userMessage)                 // 新消息
            .call()
            .content();

        // 3. 将新消息和回复存入记忆
        chatMemory.add(sessionId, List.of(
            new UserMessage(userMessage),
            new AssistantMessage(response)
        ));

        return response;
    }
}
```

### Token 窗口管理

```java
// ⭐ Token 窗口满了怎么办——滑动窗口策略
@Component
public class TokenWindowManager {

    private final TokenCounter tokenCounter;

    public List<Message> manageWindow(List<Message> history,
                                       int maxTokens) {
        int totalTokens = tokenCounter.count(history);

        if (totalTokens <= maxTokens) {
            return history;  // 没超限，直接返回
        }

        // ⭐ 策略 1：保留最早的消息 + 最新的消息（保留上下文）
        List<Message> preserved = new ArrayList<>();
        preserved.add(history.get(0));  // 保留 System Prompt
        preserved.addAll(history.subList(
            Math.max(1, history.size() - (maxTokens / 2)),
            history.size()
        ));
        return preserved;

        // ⭐ 策略 2：压缩旧消息为摘要
        // String summary = summarize(history.subList(1, history.size() - keepLatest));
        // return List.of(systemMsg, new SummaryMessage(summary), ...latestMsgs);
    }
}
```

### Token 计算

```java
// ⭐ 估算 Token 数（不同模型略有差异）
// 中文：1 个字 ≈ 1.5-2 tokens
// 英文：1 个单词 ≈ 1.3 tokens
// 代码：1 个字符 ≈ 0.25 tokens

public class TokenEstimator {
    public int estimate(String text) {
        // 粗略估算
        int chineseChars = text.replaceAll("[\\x00-\\x7F]", "").length();
        int asciiChars = text.length() - chineseChars;

        return (int)(chineseChars * 1.8 + asciiChars * 0.25);
    }
}

// Claude 4 上下文：200K tokens ≈ ~15 万中文字符
// Gemini 2.5 Pro 上下文：2M tokens ≈ ~150 万中文字符
```

---

### 2. 长期记忆（Long-Term Memory）

跨会话持久化存储的用户信息和知识。

```java
// ⭐ 基于向量数据库的长期记忆
@Service
public class LongTermMemory {

    private final VectorStore vectorStore;

    // 存储用户信息到长期记忆
    public void remember(String userId, String fact) {
        Document doc = Document.builder()
            .withContent(fact)
            .withMetadata(Map.of(
                "user_id", userId,
                "type", "user_fact",
                "timestamp", Instant.now().toString()
            ))
            .build();

        vectorStore.write(List.of(doc));
    }

    // 检索用户的长期记忆
    public List<String> recall(String userId, String query) {
        return vectorStore.similaritySearch(
            SearchRequest.query(query)
                .withTopK(5)
                .withFilterExpression("user_id == '" + userId + "'")
        ).stream()
        .map(Document::getContent)
        .toList();
    }

    // ⭐ 构建用户画像
    public UserProfile buildProfile(String userId) {
        List<String> memories = recall(userId, "用户偏好、兴趣、背景");
        String summary = chatClient.prompt()
            .user("基于以下用户信息构建用户画像：\n" + String.join("\n", memories))
            .call()
            .content();
        return parseProfile(summary);
    }
}
```

### 3. 工作记忆（Working Memory）

当前正在执行的任务的状态和中间结果。

```java
// ⭐ Agent 的工作记忆——跟踪任务进度
@Component
public class WorkingMemory {

    private final Map<String, TaskState> activeTasks = new ConcurrentHashMap<>();

    // 记录 Agent 的当前状态
    public record TaskState(
        String taskId,
        String originalGoal,
        List<Step> completedSteps,
        Step currentStep,
        int totalSteps,
        List<String> intermediateResults,
        int retryCount
    ) {}

    public record Step(
        int stepNumber,
        String description,
        String result,
        Status status
    ) {}

    public enum Status { PENDING, IN_PROGRESS, SUCCESS, FAILED }

    public void updateProgress(String taskId, Step step) {
        activeTasks.computeIfPresent(taskId, (id, state) ->
            new TaskState(
                id, state.originalGoal(),
                concat(state.completedSteps(), step),
                null,
                state.totalSteps(),
                state.intermediateResults(),
                state.retryCount()
            )
        );
    }

    public String getProgressSummary(String taskId) {
        TaskState state = activeTasks.get(taskId);
        if (state == null) return "无进行中的任务";

        return String.format("""
            任务：%s
            进度：%d/%d 步
            已完成：%s
            当前：%s
            """,
            state.originalGoal(),
            state.completedSteps().size(),
            state.totalSteps(),
            state.completedSteps().stream()
                .map(Step::description).collect(Collectors.joining(" → ")),
            state.currentStep()
        );
    }
}
```

---

## 三、记忆管理策略 ⭐

### 策略总览

```
    策略        方法                效果          适用场景
    ──────      ──────────          ──────────    ──────────
    窗口截断    保留最近 N 条消息      简单快速      日常对话
    摘要压缩    将旧消息压缩为摘要      保留上下文     长对话
    重要性筛选  只保留关键信息          Token 高效     Agent 任务
    分层记忆    Short+Long+Work      全面但复杂     生产级系统
    RAG 记忆    向量检索历史信息       可扩展        知识型 Agent
```

### 1. 窗口截断

```java
// ⭐ 最简单的记忆管理——保留最近 N 轮对话
public List<Message> slidingWindow(List<Message> history, int windowSize) {
    if (history.size() <= windowSize) return history;

    // 保留 System Prompt + 最近 windowSize-1 条消息
    List<Message> result = new ArrayList<>();
    result.add(history.get(0));  // System Prompt
    result.addAll(history.subList(
        history.size() - (windowSize - 1),
        history.size()
    ));
    return result;
}

// Spring AI 内置支持
chatMemory = new InMemoryChatMemory();  // 默认不限制
// 或自定义窗口大小
```

### 2. 摘要压缩 ⭐

```java
// ⭐ 当 Token 快满时，将历史对话压缩为摘要
@Service
public class ConversationSummarizer {

    private final ChatClient chatClient;

    public String summarize(List<Message> conversation) {
        return chatClient.prompt()
            .user("""
                请压缩以下对话为一段简洁的摘要。
                保留：用户的关键信息、已完成的步骤、未解决的问题。

                {conversation}

                摘要（200字以内）：
                """, formatConversation(conversation))
            .call()
            .content();
    }

    // ⭐ 增量摘要——每次对话结束后更新摘要
    private String runningSummary = "";

    public String updateSummary(String newMessages) {
        this.runningSummary = chatClient.prompt()
            .user("""
                当前摘要：{currentSummary}

                新对话：{newMessages}

                请合并更新摘要：
                """, runningSummary, newMessages)
            .call()
            .content();
        return runningSummary;
    }
}
```

### 3. 重要性筛选

```java
// ⭐ 只保留重要的信息进行记忆
@Service
public class ImportanceFilter {

    private final ChatClient chatClient;

    public List<String> extractKeyFacts(String conversation) {
        return chatClient.prompt()
            .user("""
                从以下对话中提取需要记住的关键信息。只提取：
                1. 用户明确的偏好和设置
                2. 未完成的任务和承诺
                3. 重要的业务数据
                4. 用户身份信息

                忽略：寒暄、临时状态、不需要后续跟进的话题。

                对话：
                {conversation}

                返回 JSON 数组，每条一个字符串。
                """, conversation)
            .call()
            .entity(List.class);
    }
}
```

### 4. 分层记忆架构（生产推荐）⭐

```java
// ⭐ 完整的分层记忆系统
@Service
public class LayeredMemory {

    private final ChatMemory shortTerm;     // 短期：当前会话
    private final VectorStore longTerm;     // 长期：跨会话知识
    private final WorkingMemory working;     // 工作：任务状态

    public LayeredMemory(VectorStore vectorStore) {
        this.shortTerm = new InMemoryChatMemory();
        this.longTerm = vectorStore;
        this.working = new WorkingMemory();
    }

    // ⭐ 构建完整的 Prompt 上下文
    public MemoryContext buildContext(String sessionId,
                                       String userId,
                                       String taskId) {
        // 1. 短期记忆（最近 N 条历史）
        List<Message> recentHistory = shortTerm.get(sessionId, 10);

        // 2. 长期记忆（用户画像 + 相关历史知识）
        List<String> userFacts = retrieveUserFacts(userId);

        // 3. 工作记忆（当前任务进度）
        String taskProgress = working.getProgressSummary(taskId);

        // 4. 汇总为上下文
        return new MemoryContext(recentHistory, userFacts, taskProgress);
    }

    // ⭐ 每轮对话后更新所有记忆层
    public void updateAfterTurn(String sessionId,
                                 String userId,
                                 String taskId,
                                 String userMessage,
                                 String assistantResponse) {
        // 更新短期记忆
        shortTerm.add(sessionId, List.of(
            new UserMessage(userMessage),
            new AssistantMessage(assistantResponse)
        ));

        // 提取重要信息存入长期记忆
        List<String> keyFacts = importanceFilter.extractKeyFacts(
            userMessage + "\n" + assistantResponse);

        keyFacts.forEach(fact ->
            longTerm.write(List.of(Document.builder()
                .withContent(fact)
                .withMetadata(Map.of(
                    "user_id", userId,
                    "type", "conversation_fact",
                    "timestamp", Instant.now().toString()
                ))
                .build()))
        );

        // 更新工作记忆中的进度
        if (taskId != null) {
            trackTaskProgress(taskId, userMessage, assistantResponse);
        }
    }
}
```

---

## 四、上下文管理实战 ⭐

### Spring AI ChatMemory

```java
// ⭐ 使用 ChatMemory 管理会话
@Configuration
public class MemoryConfig {

    // 内存存储（开发/测试）
    @Bean
    public ChatMemory inMemoryChatMemory() {
        return new InMemoryChatMemory();
    }

    // Redis 存储（生产——跨服务共享）
    @Bean
    public ChatMemory redisChatMemory(RedisConnectionFactory factory) {
        return new RedisChatMemory(factory)
            .withTtl(Duration.ofHours(24));  // 会话过期时间
    }

    // JDBC 存储（生产——持久化）
    @Bean
    public ChatMemory jdbcChatMemory(DataSource dataSource) {
        return new JdbcChatMemory(dataSource);
    }
}
```

```java
@Service
public class ChatWithMemory {

    private final ChatMemory chatMemory;
    private final ChatClient chatClient;

    // ⭐ 会话式聊天
    public String chat(String sessionId, String message) {
        return chatClient.prompt()
            .user(message)
            .call()
            .content();
    }

    // ⭐ 带历史的管理方式
    public String chatWithHistory(String sessionId, String message) {
        List<Message> history = chatMemory.get(sessionId, 20);
        // 如果总 Token 超限，压缩历史
        if (countTokens(history) > 100000) {
            history = compressHistory(history);
        }

        String response = chatClient.prompt()
            .messages(history)
            .user(message)
            .call()
            .content();

        chatMemory.add(sessionId, List.of(
            new UserMessage(message),
            new AssistantMessage(response)
        ));

        return response;
    }
}
```

### Agent 上下文组装

```java
// ⭐ Agent 的完整上下文组装
@Service
public class AgentContextBuilder {

    public String buildSystemPrompt(UserContext ctx) {
        return """
            你是{name}的个人 AI 助手。

            ## 用户信息
            - 姓名：{name}
            - 角色：{role}
            - 偏好语言：{language}
            - 时区：{timezone}

            ## 当前会话上下文
            {recentHistory}

            ## 用户长期偏好
            {userPreferences}

            ## 进行中的任务
            {activeTask}

            ## 可用工具
            {tools}

            ## 行为规则
            - 基于用户历史偏好个性化回应
            - 跟踪任务进度，适时提醒
            - 不知道的信息坦诚说明
            """.replace("{name}", ctx.name())
               .replace("{role}", ctx.role())
               .replace("{language}", ctx.language())
               .replace("{timezone}", ctx.timezone())
               .replace("{recentHistory}", ctx.recentHistory())
               .replace("{userPreferences}", ctx.userPreferences())
               .replace("{activeTask}", ctx.activeTask())
               .replace("{tools}", ctx.availableTools());
    }
}
```

---

## 五、高并发场景的记忆管理

### 会话隔离

```java
// ⭐ 每个用户/会话独立记忆
@Component
public class SessionManager {

    private final Map<String, SessionState> sessions = new ConcurrentHashMap<>();

    public record SessionState(
        String sessionId,
        String userId,
        ChatMemory chatMemory,
        WorkingMemory workingMemory,
        Instant createdAt,
        Instant lastActiveAt
    ) {}

    // 获取或创建会话
    public SessionState getOrCreateSession(String sessionId, String userId) {
        return sessions.computeIfAbsent(sessionId, id -> {
            // 如果用户有历史会话，恢复
            SessionState previous = findPreviousSession(userId);
            if (previous != null) {
                return previous;
            }
            return createNewSession(sessionId, userId);
        });
    }

    // 定期清理过期会话
    @Scheduled(fixedRate = 600000)  // 每 10 分钟
    public void cleanExpiredSessions() {
        Instant expiry = Instant.now().minus(30, ChronoUnit.MINUTES);
        sessions.entrySet().removeIf(entry ->
            entry.getValue().lastActiveAt().isBefore(expiry)
        );
    }
}
```

### 记忆持久化

```java
// ⭐ 生产环境——Redis 持久化会话
@Configuration
public class RedisMemoryConfig {

    @Bean
    public ChatMemory chatMemory(RedisTemplate<String, List<Message>> redis) {
        return new RedisChatMemory(redis)
            .withTtl(Duration.ofHours(24));  // 24 小时过期
    }
}

// 即使应用重启，用户的会话记忆仍然保留
// 多个实例共享同一个 Redis，Session 跨实例可用
```

---

## 六、Token 优化策略 ⭐

### 减少 Token 消耗的技巧

| 策略 | 节省比例 | 做法 |
|:----|:--------:|:-----|
| **压缩历史** | 40-60% | 旧对话摘要化 |
| **移除冗余** | 10-20% | 去掉思考过程和调试信息 |
| **精简 Prompt** | 20-40% | 去除多余描述，用最短表达 |
| **选择性记忆** | 30-50% | 只保留关键信息 |
| **缓存相同输入** | 20-80% | 语义缓存命中时零 Token 消耗 |

### Prompt 精简示例

```diff
- ❌ 啰嗦版（~200 tokens）
  你是一个非常有帮助的 AI 助手。你的名字叫小智。
  你由某公司开发。你应该礼貌、友好地回应用户的问题。
  不要使用不当语言。要尊重用户。要诚实地回答问题。
  如果你不确定答案，你应该直接说不知道...
  
+ ✅ 精简版（~50 tokens）
  你叫小智，某公司开发的 AI 助手。
  礼貌友好，不确定就说不知道。
```

### 对话压缩实现

```java
// ⭐ Token 预算分配
@Service
public class TokenBudgetManager {

    private static final int MAX_CONTEXT_TOKENS = 200000;  // Claude 4
    private static final int SYSTEM_PROMPT_BUDGET = 2000;
    private static final int TOOL_DESC_BUDGET = 2000;
    private static final int USER_INPUT_BUDGET = 4000;
    private static final int OUTPUT_BUDGET = 4000;

    public int getHistoryBudget() {
        return MAX_CONTEXT_TOKENS
             - SYSTEM_PROMPT_BUDGET
             - TOOL_DESC_BUDGET
             - USER_INPUT_BUDGET
             - OUTPUT_BUDGET;
        // ≈ 188K tokens 可用于对话历史
    }

    // 按优先级分配 Token
    public List<Message> allocateBudget(List<Message> history) {
        int budget = getHistoryBudget();
        int totalTokens = countTokens(history);

        if (totalTokens <= budget) return history;

        // 优先级：最近的对话 > 重要的历史
        List<Message> prioritized = new ArrayList<>();
        int used = 0;

        // 1. 保留最近的 20% Token
        List<Message> recent = getRecentMessages(history, budget / 5);
        prioritized.addAll(recent);
        used += countTokens(recent);

        // 2. 用剩余预算保留早期的重要信息
        int remainingBudget = budget - used;
        List<Message> earlyHistory = getEarlyImportantMessages(
            history, remainingBudget);

        // 3. 合并摘要
        return mergeWithSummary(
            history,
            earlyHistory,
            recent,
            remainingBudget
        );
    }
}
```

---

## 七、记忆在 Agent 中的完整应用

### 带记忆的 Agent 架构

```java
// ⭐ 完整记忆 Agent
@Service
public class MemoryEnhancedAgent {

    private final LayeredMemory memory;
    private final ChatClient chatClient;

    @Tool(description = "记住用户说的重要信息")
    public void remember(
            @ToolParam(description = "要记住的信息") String fact) {
        memory.saveUserFact(currentUserId(), fact);
    }

    @Tool(description = "回忆与该话题相关的历史信息")
    public List<String> recall(
            @ToolParam(description = "搜索关键词") String topic) {
        return memory.retrieve(currentUserId(), topic);
    }

    @Tool(description = "忘记指定的信息")
    public void forget(
            @ToolParam(description = "要删除的信息描述") String description) {
        memory.deleteFact(currentUserId(), description);
    }

    public String chat(String sessionId, String message) {
        // Agent 可以自主调用 remember/recall 工具来管理记忆
        return chatClient.prompt()
            .user(message)
            .functions("remember", "recall", "forget")
            .call()
            .content();
    }
}
```

### 示例场景

```
用户："帮我查一下上周的订单"

Agent 推理：
  → 需要知道用户的身份
  → 调用 recall("用户身份") → 找到用户 ID
  → 调用 queryDatabase("查订单") → 获取订单数据
  → 回复用户

用户："我叫张三，记住了"

Agent 推理：
  → 调用 remember("用户张三，ID: 1001")
  → 回复："已记住"

用户："我叫什么？"

Agent 推理：
  → 调用 recall("用户姓名") → 找到"张三"
  → 回复："你叫张三"

用户（新会话）："我之前有什么未完成的订单？"

Agent 推理：
  → 调用 recall("用户身份") → 找到"张三，ID: 1001"
  → 调用 queryDatabase("查未完成订单") → 获取数据
  → 回复："你有 2 个未完成的订单..."
```

---

## 八、常见面试题

### 1. Agent 的记忆有哪些类型？

> 三种：**短期记忆**（当前会话的 Token 窗口内）、**长期记忆**（跨会话的向量数据库存储）、**工作记忆**（当前正在执行的任务状态和中间结果）。生产系统需要三者结合。

### 2. 对话历史太长怎么办？

> 三种策略：**滑动窗口**（只保留最近 N 条）、**摘要压缩**（把旧对话压缩为摘要）、**重要性筛选**（只保留关键信息）。通常会组合使用：先用重要性筛选，再摘要，最后窗口截断。

### 3. 怎么实现跨会话记忆？

> 用户的关键信息在每轮对话后提取，存入**向量数据库**。新会话开始时根据用户 ID 检索相关记忆，注入 System Prompt 或作为上下文。使用 `@Tool` 让 Agent 自主调用 `remember`/`recall` 工具管理记忆。

### 4. Spring AI 中如何管理记忆？

> 使用 `ChatMemory` 接口管理会话历史。实现包括 `InMemoryChatMemory`（开发用）、`RedisChatMemory`（生产推荐）、`JdbcChatMemory`（需要持久化时）。通过 `messages()` 方法将历史注入到每次 Prompt 中。

### 5. 200K Token 窗口够用吗？

> 对于日常聊天足够（约 15 万中文字符）。但对于长时间运行的 Agent（如 Coding Agent），可能需要压缩历史。2026 年 Gemini 2.5 Pro 的 2M Token 窗口可以装下一整本《三体》三部曲，极大地缓解了记忆管理压力。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解短期/长期/工作记忆概念 → ChatMemory 基本使用
> 2. **进阶**：滑动窗口 → 摘要压缩 → 重要性筛选 → 分层记忆架构
> 3. **深入**：Token 预算分配 → 记忆持久化（Redis）→ 高并发会话管理
> 4. **工程化**：Agent 自主管理记忆 → 记忆评估 → 数据隐私合规


---

> **📖 学习路线**：[[AIAgent篇/README|AI Agent 学习路线图]]
