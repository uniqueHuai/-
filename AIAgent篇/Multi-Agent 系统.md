# Multi-Agent 系统

## 一、什么是 Multi-Agent 系统

### 定义

**Multi-Agent 系统（多智能体系统）** 是由多个 AI Agent 组成、通过**分工协作**完成复杂任务的系统架构。每个 Agent 有独立的角色、目标和能力，通过通信与协调共同解决问题。

```
    单 Agent 模式                          Multi-Agent 模式
    ┌──────────────────┐              ┌──────────────────────────┐
    │    一个 Agent     │              │   多个专业 Agent 协作       │
    │                  │              │                          │
    │  "我什么都能做"    │              │  ┌──────┐  ┌──────┐      │
    │                  │              │  │产品经理│  │架构师│      │
    │  所有功能耦合     │              │  └──┬───┘  └──┬───┘      │
    │  能力边界受限     │              │     │        │          │
    │  单点故障风险     │              │     └──┬─────┘          │
    │                  │              │        │               │
    │                  │              │  ┌──────┴──────┐        │
    │                  │              │  │   程序员     │        │
    │                  │              │  └──────┬──────┘        │
    │                  │              │         │               │
    │                  │              │  ┌──────┴──────┐        │
    │                  │              │  │   测试员     │        │
    │                  │              │  └─────────────┘        │
    └──────────────────┘              └──────────────────────────┘
```

### 为什么需要多 Agent

| 场景 | 单 Agent 的问题 | Multi-Agent 方案 |
|:----|:--------------|:-----------------|
| **复杂任务** | 一个模型能力不够 | 每个 Agent 专注一个领域 |
| **质量要求** | 自己写自己检查，盲区多 | 互相审查，交叉验证 |
| **并行处理** | 串行执行，效率低 | 独立子任务并行执行 |
| **系统稳定性** | 一个错误推理导致全盘失败 | 多 Agent 互相纠错兜底 |
| **角色冲突** | 既要创意又要严谨难兼顾 | 不同角色各司其职 |

### 核心概念

| 概念 | 说明 |
|:----|:-----|
| **Agent 角色** | 每个 Agent 的身份定义（如分析师、编码员、审查员） |
| **通信协议** | Agent 之间的消息格式和交互方式 |
| **任务分解** | 将复杂任务拆分为可分配给各 Agent 的子任务 |
| **协调机制** | 决定谁做什么、何时做的策略 |
| **共享记忆** | 多 Agent 共享的上下文和知识 |
| **冲突解决** | 当 Agent 意见不一致时的仲裁机制 |

---

## 二、Multi-Agent 架构模式 ⭐

### 1. Supervisor 模式（审核制）

```
                   ┌────────────────┐
                   │   Supervisor    │
                   │  (规划/协调/审核) │
                   └──────┬─────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Agent A  │   │  Agent B  │   │  Agent C  │
    │ (分析师)  │   │ (编码员)  │   │ (测试员)  │
    └──────────┘   └──────────┘   └──────────┘
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼
                   ┌────────────────┐
                   │  Supervisor    │
                   │  (汇总/质量审核) │
                   └────────────────┘
```

**适合场景**：目标明确的复杂任务，需要分工+质量把控

```java
// ⭐ Supervisor 模式的 Spring AI 实现
@Service
public class SupervisorAgent {

    private final ChatClient supervisor;
    private final ChatClient analyst;
    private final ChatClient coder;
    private final ChatClient tester;

    public String executeTask(String task) {
        // 1. Supervisor 规划任务
        String plan = supervisor.prompt()
            .user("分析以下任务，制定执行计划：\n" + task)
            .call()
            .content();

        // 2. 分析师 Agent
        String analysis = analyst.prompt()
            .user("基于以下计划进行分析：\n" + plan)
            .call()
            .content();

        // 3. 编码员 Agent
        String code = coder.prompt()
            .user("基于以下分析编写代码：\n" + analysis)
            .call()
            .content();

        // 4. 测试员 Agent
        String review = tester.prompt()
            .user("审查以下代码质量：\n" + code)
            .call()
            .content();

        // 5. Supervisor 审核
        return supervisor.prompt()
            .user("""
                汇总以下结果并给出最终输出：

                分析：{analysis}
                代码：{code}
                审查意见：{review}

                如果审查发现问题，返回需要修改的部分。
                否则返回最终方案。
                """, analysis, code, review)
            .call()
            .content();
    }
}
```

### 2. Debate 模式（辩论制）

```
               ┌──────────────────────────────┐
               │          问题                  │
               └──────────────┬───────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Agent A     │ │  Agent B     │ │  Agent C     │
    │  (正方)      │◄├─── 辩论 ────►│ │  (反方)      │
    │              │ │              │ │              │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │  Judge Agent   │
                   │  (综合裁决)      │
                   └────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │  最终答案       │
                   └────────────────┘
```

**适合场景**：需要多角度分析、方案评估、决策质量要求高的场景

```java
// ⭐ Debate 模式
@Service
public class DebateSystem {

    public String debate(String question) {
        // 第一轮：各 Agent 独立分析
        String viewA = agentA.prompt()
            .user("请从技术可行性角度分析：\n" + question).call().content();

        String viewB = agentB.prompt()
            .user("请从成本和收益角度分析：\n" + question).call().content();

        String viewC = agentC.prompt()
            .user("请从风险和安全性角度分析：\n" + question).call().content();

        // 第二轮：互相评论
        String critiqueB = agentA.prompt()
            .user("对方的观点：" + viewB + "\n请从你的角度评论").call().content();

        // 第三轮：裁决
        return judge.prompt()
            .user("""
                技术可行性：{viewA}
                成本收益：{viewB}
                安全风险：{viewC}
                交叉评论：{critiqueB}

                请给出综合裁决，说明理由。
                """, viewA, viewB, viewC, critiqueB)
            .call()
            .content();
    }
}
```

### 3. Pipeline 模式（流水线）⭐

```
  输入
   │
   ▼
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ 需求分析    │───►│ 系统设计    │───►│ 代码生成    │───►│ 代码审查    │
│ Agent      │    │ Agent      │    │ Agent      │    │ Agent      │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
                                                        │
                                                        ▼
                                                 ┌────────────┐
                                                 │ 测试生成    │
                                                 │ Agent      │
                                                 └────────────┘
                                                        │
                                                        ▼
                                                     输出
```

**适合场景**：流程明确、阶段清晰的线性任务

```java
// ⭐ Pipeline 模式——软件工程流水线
@Service
public class SoftwarePipeline {

    public SoftwareProject execute(Requirement req) {
        // 阶段 1：需求分析
        Spec spec = requirementAgent.analyze(req);

        // 阶段 2：架构设计
        Architecture arch = architectAgent.design(spec);

        // 阶段 3：代码生成（可并行）
        List<CodeFile> codeFiles = coderAgent.generate(arch);

        // 阶段 4：代码审查
        List<ReviewComment> reviews = reviewerAgent.review(codeFiles);

        // 阶段 5：根据审查意见修复
        if (!reviews.isEmpty()) {
            codeFiles = coderAgent.fix(codeFiles, reviews);
        }

        // 阶段 6：生成测试
        List<TestFile> tests = testerAgent.generateTests(codeFiles);

        return new SoftwareProject(spec, arch, codeFiles, tests);
    }
}
```

### 4. Swarm 模式（集群模式）

```
                      ┌──────────────┐
                      │   任务分发器   │
                      └──────┬───────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │  Worker 1  │    │  Worker 2  │    │  Worker N  │
   │ (相同角色)  │    │ (相同角色)  │    │ (相同角色)  │
   └────────────┘    └────────────┘    └────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │   结果聚合器   │
                      └──────────────┘
```

**适合场景**：大量独立任务并行处理（如客服、审核、数据处理）

---

## 三、Agent 间通信

### 通信协议

```java
// ⭐ Agent 通信的消息格式
public record AgentMessage(
    String from,           // 发送者
    String to,             // 接收者
    String messageId,      // 消息ID
    String correlationId,  // 关联ID（跟踪对话链）
    MessageType type,      // 消息类型
    String content,        // 消息内容
    Map<String, Object> metadata,  // 元数据
    Instant timestamp      // 时间戳
) {}

public enum MessageType {
    TASK_ASSIGN,     // 任务分配
    TASK_RESULT,     // 任务结果
    QUESTION,        // 提问
    RESPONSE,        // 回复
    REVIEW,          // 审查意见
    DISAGREE,        // 异议
    CLARIFICATION,   // 澄清请求
    COMPLETE         // 完成通知
}
```

### Agent 通信示例

```java
// ⭐ 两个 Agent 之间的对话
@Service
public class AgentCommunication {

    public void collaborate() {
        // 分析师 Agent 向编码员 Agent 发送需求
        AgentMessage msg = new AgentMessage(
            "analyst", "coder",
            UUID.randomUUID().toString(),
            "task-001",
            MessageType.TASK_ASSIGN,
            "请实现用户注册接口，需要：\n" +
            "1. POST /api/register\n" +
            "2. 校验邮箱格式\n" +
            "3. 密码加密存储",
            Map.of("priority", "high"),
            Instant.now()
        );

        // 编码员回复
        AgentMessage response = coderAgent.handleMessage(msg);

        if (response.type() == MessageType.CLARIFICATION) {
            // 编码员需要澄清
            AgentMessage clarification = analystAgent.handleMessage(response);
            coderAgent.handleMessage(clarification);
        }
    }
}
```

---

## 四、任务分解与分配 ⭐

### 任务分解策略

```java
// ⭐ 将复杂任务自动分解为子任务
@Service
public class TaskDecomposer {

    private final ChatClient chatClient;

    public TaskPlan decompose(String complexTask) {
        String plan = chatClient.prompt()
            .user("""
                将以下复杂任务分解为可执行的子任务。
                每个子任务需要：任务描述、所需技能、前置依赖。

                任务：{task}

                请返回 JSON 格式：
                {
                    "tasks": [
                        {
                            "id": "task-1",
                            "description": "...",
                            "required_skill": "analysis|code|test|review",
                            "depends_on": [],
                            "estimated_steps": 5
                        },
                        ...
                    ],
                    "parallel_groups": [["task-1", "task-2"], ["task-3"]]
                }
                """, complexTask)
            .call()
            .entity(TaskPlan.class);

        return plan;
    }
}
```

### 任务分配

```java
// ⭐ 将子任务分配给合适的 Agent
public class TaskDispatcher {

    private final Map<String, AgentWorker> agents = Map.of(
        "analyst", new AnalystAgent(),
        "architect", new ArchitectAgent(),
        "coder", new CoderAgent(),
        "reviewer", new ReviewerAgent()
    );

    public void dispatch(TaskPlan plan) {
        // 先执行没有依赖的任务
        List<Task> readyTasks = plan.tasks().stream()
            .filter(t -> t.depends_on().isEmpty())
            .toList();

        // 并行执行独立任务
        readyTasks.parallelStream().forEach(task -> {
            AgentWorker agent = agents.get(task.required_skill());
            agent.execute(task);
        });
    }
}
```

---

## 五、Multi-Agent 实战：AI 软件开发团队 ⭐

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                  AI 软件开发团队                               │
│                                                             │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐           │
│  │ 产品经理    │   │  架构师     │   │  技术主管    │           │
│  │ Agent      │   │  Agent      │   │  Agent      │           │
│  └─────┬──────┘   └─────┬──────┘   └─────┬──────┘           │
│        │                │                │                  │
│        └────────────────┼────────────────┘                  │
│                         │                                   │
│            ┌────────────┴────────────┐                      │
│            │                         │                      │
│    ┌───────┴──────┐         ┌───────┴──────┐               │
│    │ 前端开发 Agent│         │ 后端开发 Agent│               │
│    │              │         │              │               │
│    │  ├─ 页面生成  │         │  ├─ API 实现  │               │
│    │  ├─ 组件开发  │         │  ├─ 数据库设计 │               │
│    │  └─ 样式实现  │         │  └─ 业务逻辑  │               │
│    └───────┬──────┘         └───────┬──────┘               │
│            │                         │                      │
│            └────────────┬────────────┘                      │
│                         │                                   │
│            ┌────────────┴────────────┐                      │
│            │   测试 Agent            │                      │
│            │   ├─ 单元测试            │                      │
│            │   ├─ 集成测试            │                      │
│            │   └─ E2E 测试            │                      │
│            └─────────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

### 实现示例

```java
// ⭐ Multi-Agent 软件开发团队

// ---- Agent 角色定义 ----
public record TaskResult(String agentName, String output, boolean success) {}

@Service
class ProductManagerAgent {
    private final ChatClient chatClient;

    public Spec analyzeRequirement(String userRequest) {
        return chatClient.prompt()
            .system("你是资深产品经理。负责分析需求、编写 PRD、定义验收标准。"
                  + "输出格式：功能列表 + 优先级 + 验收标准")
            .user(userRequest)
            .call()
            .entity(Spec.class);
    }
}

@Service
class ArchitectAgent {
    private final ChatClient chatClient;

    public Architecture design(Spec spec) {
        return chatClient.prompt()
            .system("你是资深系统架构师。精通微服务、数据库设计、技术选型。"
                  + "输出：技术栈 + 模块划分 + 数据模型 + API 设计")
            .user("根据以下需求设计系统架构：\n" + spec)
            .call()
            .entity(Architecture.class);
    }
}

@Service
class CoderAgent {
    private final ChatClient chatClient;

    public CodeResult implement(Task task) {
        return chatClient.prompt()
            .system("你是高级 Java 工程师。输出可编译的生产级代码。"
                  + "包含：完整类、异常处理、日志、注释。"
                  + "使用 Spring Boot 3.x + Java 17+")
            .user("请实现以下功能：\n" + task.description())
            .call()
            .entity(CodeResult.class);
    }
}

@Service
class ReviewerAgent {
    private final ChatClient chatClient;

    public ReviewResult review(CodeResult code) {
        return chatClient.prompt()
            .system("你是代码审查专家。审查维度："
                  + "正确性、性能、安全、可维护性、代码风格。"
                  + "发现问题时给出具体的修改建议。")
            .user("请审查以下代码：\n" + code.code())
            .call()
            .entity(ReviewResult.class);
    }
}

// ---- 编排器 Orchestrator ----
@Service
public class SoftwareTeamOrchestrator {

    private final ProductManagerAgent pm;
    private final ArchitectAgent architect;
    private final CoderAgent coder;
    private final ReviewerAgent reviewer;

    public SoftwareProject build(String userRequest) {
        // 1. 产品经理分析需求
        Spec spec = pm.analyzeRequirement(userRequest);
        System.out.println("=== PRD ===" + spec);

        // 2. 架构师设计方案
        Architecture arch = architect.design(spec);
        System.out.println("=== 架构 ===" + arch);

        // 3. 按模块分解为开发任务
        List<Task> tasks = arch.modules().stream()
            .map(module -> new Task(module.name(), module.description()))
            .toList();

        List<CodeResult> allCode = new ArrayList<>();

        for (Task task : tasks) {
            // 4. 编码
            CodeResult code = coder.implement(task);
            System.out.println("=== 编码完毕：" + task.name() + " ===");

            // 5. 审查
            ReviewResult review = reviewer.review(code);

            // 6. 如果有问题，修复后再审查
            int maxRetries = 3;
            while (!review.passed() && maxRetries-- > 0) {
                code = coder.fix(code, review.suggestions());
                review = reviewer.review(code);
            }

            if (review.passed()) {
                allCode.add(code);
            } else {
                System.err.println("任务 " + task.name() + " 经过多次修复仍未通过审查");
            }
        }

        return new SoftwareProject(spec, arch, allCode);
    }
}
```

---

## 六、框架对比

### 2026 年主流 Multi-Agent 框架

| 框架 | 语言 | 协作模式 | 特点 |
|:----|:----|:--------|:-----|
| **CrewAI** | Python | 角色+任务 | 最易用，角色定义清晰，适合快速原型 |
| **AutoGen** | Python | 对话式 | Microsoft 出品，Agent 间自由对话 |
| **LangGraph** | Python | 图状态机 | 最灵活，复杂工作流首选 |
| **Semantic Kernel** | C#/Python | Plan+Step | Microsoft 企业级，与 Azure 整合 |
| **Spring AI** ⭐ | Java | 工具+服务 | Java 生态，与 Spring Boot 深度整合 |
| **MCP** | 多语言 | 协议层 | 工具标准化协议，各框架可互操作 |

### Spring AI 实现 Multi-Agent

```java
// ⭐ Spring AI 中的多 Agent 编排
@Configuration
public class MultiAgentConfig {

    // 每个 Agent 一个独立的 ChatClient
    @Bean
    public ChatClient analystClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem("你是一个数据分析师，精通数据分析和可视化。")
            .build();
    }

    @Bean
    public ChatClient writerClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem("你是一个技术文档 writer，擅长将复杂概念解释清楚。")
            .build();
    }

    @Bean
    public ChatClient reviewerClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem("你是一个质量审查员，严格检查输出质量和准确性。")
            .build();
    }

    // 编排 Agent
    @Bean
    public ChatClient orchestratorClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem("""
                你是团队负责人。你的团队包括：
                - analyst：数据分析师
                - writer：文档撰写员
                - reviewer：质量审查员

                分配任务给合适的成员，审核他们的输出，
                如果有问题安排修改，最终汇总输出。
                """)
            .build();
    }
}
```

---

## 七、挑战与最佳实践

### 常见挑战

| 挑战 | 问题 | 解决方案 |
|:----|:-----|:---------|
| **成本飙升** | 多个 Agent 多次调用 LLM | 小模型做简单任务、缓存、路由 |
| **延迟累积** | 串行执行总延迟 = 各步之和 | 独立任务并行执行 |
| **协调复杂** | Agent 间通信状态管理困难 | 使用图状态机（LangGraph） |
| **错误传播** | 前序 Agent 错误影响后续 | 增加校验节点、回滚机制 |
| **角色重叠** | 多个 Agent 做了相同的事 | 明确职责边界、去重策略 |
| **评估困难** | 多 Agent 系统整体难以评估 | 分步评估 + 端到端评估 |

### 设计原则

```
1. 明确角色边界
   每个 Agent 只做一件事，做好一件事
   避免角色职责重叠

2. 最小必要原则
   能用单 Agent 解决就不用多 Agent
   每个额外 Agent 都增加成本和复杂度

3. 人类在环中（Human-in-the-Loop）
   关键决策点加入人工审核
   尤其是修改/删除操作的 Agent

4. 可观测性
   记录每个 Agent 的输入输出
   跟踪消息在 Agent 间的流转
   有完整的审计日志

5. 容错设计
   假设每个 Agent 都可能出错
   加入验证和重试机制
   设置最大迭代次数防止死循环
```

### 何时使用 Multi-Agent

```
✅ 适合 Multi-Agent：
   ├── 任务可明确拆分为不同专业领域
   ├── 需要多角度分析和交叉验证
   ├── 不同步骤需要不同的 Prompt/模型
   ├── 有独立可并行的子任务
   └── 对输出质量要求极高

❌ 不适合 Multi-Agent：
   ├── 简单问答（单 Agent 足够）
   ├── 实时对话场景（延迟敏感）
   ├── 成本极其敏感
   └── Agent 间通信成本 > 收益
```

---

## 八、常见面试题

### 1. 什么场景适合用 Multi-Agent？

> 复杂任务可拆分为多个专业领域（如软件开发、金融分析）、需要多角度交叉验证（如决策评估）、有独立并行子任务（如批量数据处理）。简单场景不要用 Multi-Agent，成本和复杂度不划算。

### 2. Multi-Agent 有哪些协作模式？

> **Supervisor**（一个主管分配任务和审核）、**Debate**（多 Agent 辩论后裁决）、**Pipeline**（流水线串行处理）、**Swarm**（多 Worker 并行处理同类型任务）。实际项目中常组合使用。

### 3. 怎么解决 Multi-Agent 的协调问题？

> 定义清晰的通信协议和消息格式、使用状态机管理工作流（LangGraph）、记录完整的 Agent 交互日志、设置超时和重试机制、关键节点人工介入。

### 4. Multi-Agent 和单一 Agent 怎么选？

> 单一 Agent 足够应对大多数场景。当任务需要多个专业技能、输出质量要求极高、或者有天然并行子任务时考虑 Multi-Agent。记住：**每多加一个 Agent，系统复杂度翻倍**。

### 5. 如何控制 Multi-Agent 的成本？

> 子任务尽量用小模型/本地模型、语义缓存避免重复调用、合并短请求、并行执行减少总耗时、设置最大调用次数防止失控。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 Multi-Agent 概念 → 了解 4 种协作模式
> 2. **实践**：用 Spring AI 实现 Supervisor 模式 → Pipeline 模式
> 3. **深入**：Agent 间通信协议 → 任务分解与分配算法
> 4. **工程化**：编排器设计 → 可观测性 → 容错机制 → 成本控制
