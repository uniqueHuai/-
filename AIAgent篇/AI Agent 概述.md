# AI Agent 概述

## 一、什么是 AI Agent

### 定义

**AI Agent（人工智能体）** 是一个能够**感知环境**、**自主推理决策**、**执行行动**并**从反馈中学习**的智能系统。与传统的程序不同，Agent 不是被动执行固定指令，而是主动地、迭代地完成目标。

```
         ┌────────────────────────────────────────────────┐
         │                 AI Agent                         │
         │                                                  │
         │   感知（Perceive）    推理（Reason）    行动（Act）   │
         │   ┌──────────┐    ┌──────────┐    ┌──────────┐  │
         │   │ 用户输入  │    │  LLM 推理 │    │  调用工具  │  │
    ─────┼──►│ 环境状态  │───►│  记忆检索  │───►│  返回响应  │──┼────►
         │   │ 工具反馈  │    │  规划分解  │    │  更新记忆  │  │
         │   └──────────┘    └──────────┘    └──────────┘  │
         │                         ▲                        │
         │                         │ 循环迭代               │
         └─────────────────────────┼────────────────────────┘
                                   │
                            （直到目标完成）
```

### Agent 与传统的程序的区别

| 对比维度 | 传统程序 | AI Agent |
|:--------:|:--------:|:---------:|
| **逻辑来源** | 开发者硬编码规则 | LLM 推理生成 |
| **灵活性** | 固定流程，超出预期即崩溃 | 动态规划，能处理未知情况 |
| **工具使用** | 写死的 API 调用 | LLM 自主选择工具 |
| **记忆** | 无状态或简单 Session | 短期+长期记忆，知识检索 |
| **错误处理** | 预定义的异常路径 | 自我修正、重试、求助 |
| **迭代能力** | 单次执行 | 多步推理->行动->观察循环 |
| **开发成本** | 高（每改逻辑需改代码） | 低（用自然语言描述目标） |

### 2026 年 AI Agent 发展状况

```
2023    2024            2025                    2026
│       │               │                       │
├─ ChatGPT API       ├─ GPT-4V            ├─ GPT-5 / Claude 4 Opus
├─ Agent 概念提出     ├─ AutoGPT 热潮      ├─ Agent 进入生产成熟期
├─ LangChain 诞生     ├─ RAG 普及          ├─ MCP 协议标准化
                    ├─ Anthropic Tool use  ├─ Multi-Agent 落地
                    ├─ Spring AI 诞生      ├─ Agentic RAG 成熟
                    ├─ AI Coding Agent     ├─ AI Agent 岗位激增
                        (Cursor/Devin)     ├─ Agent-to-Agent 通信
```

截止 2026 年 5 月，AI Agent 已经从实验性概念演变为**生产级技术**：
- **MCP（Model Context Protocol）** 已成为 Agent 工具调用的行业标准协议
- **Spring AI 1.x** 让 Java 生态的 Agent 开发进入稳定期
- **多模态 Agent**（文字+图片+代码+音视频）成为主流
- **Agentic RAG** 替代了简单的文档检索，实现多步推理+检索
- **AI Coding Agent**（如 Cursor、GitHub Copilot、Claude Code）全面进入开发者日常

---

## 二、Agent 的核心组件

### 1. 感知（Perception）

Agent 接收和处理多种输入：

```java
// Java / Spring AI 中的多模态感知
@PostMapping("/chat")
public ChatResponse chat(@RequestBody ChatRequest request) {
    return chatClient.prompt()
        .user(u -> u
            .text(request.getMessage())
            .media(request.getImageUrl())    // 图片输入
            .param("context", getContext())  // 上下文信息
            .param("tools", getToolResults()) // 工具反馈
        )
        .call()
        .chatResponse();
}
```

感知来源：
- **用户输入**：文本、语音、图片、文件
- **环境状态**：系统日志、监控数据、传感器
- **工具反馈**：API 返回值、数据库查询结果
- **记忆检索**：历史会话、知识库

### 2. 推理与规划（Reasoning & Planning）⭐

这是 Agent 区别于普通 LLM 调用的核心能力：

```python
# Agent 的推理循环（简化伪代码）
def run_agent(task):
    # 1. 理解任务
    plan = llm.reason(f"分析任务并制定计划：{task}")

    # 2. 迭代执行
    while not task_complete:
        step = plan.next_step()

        if step.need_tool:
            result = call_tool(step.tool_name, step.params)
            observation = f"工具返回：{result}"

            # 3. 反思与调整
            plan = llm.reason(
                f"当前进度：{progress}\n"
                f"观察结果：{observation}\n"
                f"下一步行动："
            )
        else:
            response = llm.reason(step.prompt)
            plan.update(response)

    return final_answer
```

推理模式：
| 模式 | 说明 | 适用场景 |
|:----|:-----|:---------|
| **ReAct** | 推理+行动交替循环 | 大多数通用 Agent |
| **Plan-and-Execute** | 先规划再执行 | 复杂多步骤任务 |
| **Reflexion** | 执行后反思改进 | 编码、写作等迭代任务 |
| **Tree of Thoughts** | 探索多条推理路径 | 数学、逻辑难题 |
| **LLM Compiler** | 并行执行多个子任务 | 高性能场景 |

### 3. 工具调用（Tool Use / Function Calling）⭐

Agent 通过工具与外部世界交互：

```java
// Spring AI — Function Calling 定义
@Configuration
public class AgentTools {

    @Bean
    @Tool(name = "query_database", description = "查询数据库获取用户信息")
    public Function<QueryRequest, QueryResponse> queryDatabase() {
        return request -> {
            // 执行 SQL 查询
            List<Map<String, Object>> results = jdbcTemplate
                .queryForList(request.sql());
            return new QueryResponse(results);
        };
    }

    @Bean
    @Tool(name = "send_email", description = "发送电子邮件")
    public Function<EmailRequest, String> sendEmail() {
        return request -> {
            mailSender.send(request.to(), request.subject(), request.body());
            return "邮件发送成功";
        };
    }
}

// Agent 自动决定何时调用哪个工具
String response = chatClient.prompt()
    .user("查询昨天新增的用户并发送欢迎邮件")
    .functions("query_database", "send_email")  // 注册可用工具
    .call()
    .content();
```

### 4. 记忆（Memory）

```java
// Spring AI 中的记忆管理
public class AgentMemory {

    // 短期记忆（当前会话）
    private final ChatMemory shortTerm = new InMemoryChatMemory();

    // 长期记忆（向量数据库）
    private final VectorStore longTerm;

    // 会话摘要记忆
    public String getConversationSummary(String sessionId) {
        // 自动压缩长对话为摘要
        return chatClient.prompt()
            .user("请总结这段对话的关键信息：\n" + getHistory(sessionId))
            .call()
            .content();
    }
}
```

| 记忆类型 | 存储方式 | 典型容量 | 用途 |
|:--------:|:--------:|:--------:|:-----|
| **短期记忆** | 内存（Token 窗口） | ~200K tokens | 当前对话上下文 |
| **会话摘要** | LLM 压缩后的摘要 | 几 K tokens | 超长对话压缩 |
| **长期记忆** | 向量数据库 | 无上限 | 跨会话知识 |
| **工作记忆** | 当前任务状态 | 几 K tokens | 正在进行的任务 |

### 5. 安全与防护（Guardrails）

```java
// Agent 的输入/输出护栏
@Bean
public Guardrails agentGuardrails() {
    return Guardrails.builder()
        // 输入检测——拒绝 prompt 注入
        .input(detect -> detect
            .pattern("忽略之前的指令", Action.REJECT)
            .pattern("扮演系统管理员", Action.REVIEW))
        // 输出检测——防止泄露敏感信息
        .output(verify -> verify
            .containsNo("API_KEY|PASSWORD|SECRET")
            .containsNo("个人隐私信息"))
        // 行为边界
        .action(limit -> limit
            .maxSteps(20)            // 最多执行 20 步
            .maxToolCalls(10)        // 最多调用 10 次工具
            .timeoutSeconds(120))    // 超时 2 分钟
        .build();
}
```

---

## 三、Agent 的类型

### 按复杂度分层

```
                    ┌─────────────────────────┐
                    │   自主 Agent              │
                    │  完全自主决策、长期目标     │
                    │  例：AI Coding Agent      │
                    └─────────────────────────┘
                              ▲
                    ┌─────────────────────────┐
                    │   记忆型 Agent            │
                    │  有记忆、能学习、个性化    │
                    │  例：AI 助手、客服 Agent   │
                    └─────────────────────────┘
                              ▲
                    ┌─────────────────────────┐
                    │   工具型 Agent            │
                    │   能调用工具/API          │
                    │   例：Function Calling    │
                    └─────────────────────────┘
                              ▲
                    ┌─────────────────────────┐
                    │   简单 Agent              │
                    │   单次推理+固定规则        │
                    │   例：LLM + Prompt        │
                    └─────────────────────────┘
```

### 1. 简单 Agent（Simple/Reactive Agent）

- 感知当前输入 → 直接响应
- 无记忆、无工具、无规划
- 本质上就是 LLM + 精心设计的 Prompt
- **适用**：简单问答、文本分类、内容生成

### 2. 工具型 Agent（Tool-Use Agent）

- LLM + Function Calling
- 可调用 API、数据库、搜索引擎
- 单步或多步工具调用
- **适用**：数据查询、业务操作、自动化流程

### 3. 记忆型 Agent（Memory-Enhanced Agent）

- 在工具型基础上增加长期记忆
- 能个性化回应、记住用户偏好
- **适用**：AI 助手、教育辅导、医疗咨询

### 4. 自主 Agent（Autonomous Agent）⭐

- 最复杂的 Agent 形态
- 长期目标驱动、自主规划、自我反思
- 可运行数小时到数天
- **适用**：AI Coding Agent、科研助手、复杂工作流

### 按数量分类

| 类型 | 描述 | 代表框架 |
|:----|:-----|:---------|
| **Single-Agent** | 一个 Agent 独立完成任务 | Spring AI、LangChain |
| **Multi-Agent** | 多个 Agent 协作/竞争 | CrewAI、AutoGen、Semantic Kernel |
| **Agent 集群** | 数十上百个 Agent 并行工作 | 生产级客服系统 |

---

## 四、Multi-Agent 系统 ⭐

### 为什么需要多 Agent

```
单 Agent 的局限                        多 Agent 的优势
─────────────────                    ─────────────────
单个 LLM 的能力边界                     专业分工：每个 Agent 负责一个领域
所有功能耦合在一起                       解耦：规划/执行/审核分离
单点故障（一个推理错误全盘皆输）           容错：互相校验、纠错
无法并行处理                             并行：同时执行独立子任务
缺少角色扮演                             角色：分析师/编码员/审查员
```

### 常见协作模式

```
1.  Supervisor 模式（审核制）
    ┌──────────┐
    │  Supervisor│──── 分配任务 ────► ┌───────┐
    │  (规划/审核)│                   │ Worker │
    │           │◄──── 结果审核 ──── │       │
    └──────────┘                    └───────┘

2.  Debate 模式（辩论制）
    ┌──────────┐         ┌──────────┐
    │ Agent A  │◄─── 辩论 ──►│ Agent B  │
    │ (正方)   │            │ (反方)   │
    └──────────┘            └──────────┘
           │                    │
           └──────────┬─────────┘
                      ▼
               ┌──────────────┐
               │  Judge Agent  │
               │  (裁决)       │
               └──────────────┘

3.  Pipeline 模式（流水线）
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  需求分析  │───►│  代码生成  │───►│  代码审查  │
    │  Agent    │    │  Agent    │    │  Agent    │
    └──────────┘    └──────────┘    └──────────┘
```

### 典型例子：AI 客服系统

```
用户问题
    │
    ▼
┌──────────────────┐
│  Router Agent    │──── 问题分类
│  (路由分发)       │
└──────┬───────────┘
       │
       ├── 售后问题 ──► ┌──────────────┐
       │               │  AfterSales   │──► 查订单/Tracking
       │               │  Agent        │
       ├── 技术问题 ──► ┌──────────────┐
       │               │  TechSupport  │──► 查文档/查日志
       │               │  Agent        │
       └── 投诉问题 ──► ┌──────────────┐
                       │  Complaint    │──► 转人工/升级
                       │  Agent        │
```

---

## 五、Agent 开发框架对比（2026）

| 框架 | 语言 | 定位 | 特点 |
|:----|:----|:-----|:-----|
| **Spring AI** ⭐ | Java | Java 生态 Agent 框架 | 与 Spring Boot 深度整合，1.x 稳定版，企业级首选 |
| **LangChain** | Python | 通用 Agent 框架 | 生态最丰富，支持最多模型和工具 |
| **LangGraph** | Python | 复杂 Agent 工作流 | 基于图的状态机，适合 Multi-Agent |
| **CrewAI** | Python | Multi-Agent 框架 | 角色协作开箱即用 |
| **AutoGen** | Python | 多 Agent 对话 | Microsoft 出品，强在对话模式 |
| **Semantic Kernel** | C#/Python | 企业级 AI 编排 | Microsoft 出品，与 Azure 深度整合 |
| **MCP SDK** | 多语言 | Agent 工具协议 | Anthropic 主导的 Agent 工具标准，已广泛采用 |
| **Dify** | 平台 | 低代码 Agent 平台 | 可视化工作流编排，适合非开发者 |

---

## 六、Agent 应用场景

### 已大规模落地的场景

| 场景 | 说明 | 典型工具 |
|:----|:-----|:---------|
| **AI Coding Agent** | 辅助开发、代码生成、代码审查 | Cursor、Copilot、Claude Code |
| **智能客服** | 自动回答、工单处理、多轮对话 | 自建 + LLM |
| **数据分析 Agent** | 自然语言查询数据库、生成报表 | Text-to-SQL + 可视化 |
| **文档处理 Agent** | 合同审核、信息提取、文档翻译 | RAG + Multi-Agent |
| **运维 Agent** | 日志分析、故障排查、自动修复 | K8s + LLM |

### 新兴场景（2025-2026）

- **Agent-to-Agent 通信**：不同公司的 Agent 直接协作
- **个人 AI 助理**：跨应用的日程、邮件、信息管理
- **AI 面试官**：自动筛选、面试、评估候选人
- **科研助手**：文献检索、实验设计、论文撰写
- **金融交易 Agent**：市场分析、风险评估、自动交易

---

## 七、当前挑战与趋势（2026）

### 主要挑战

| 挑战 | 说明 | 当前进展 |
|:----|:-----|:---------|
| **幻觉** | Agent 可能做出错误判断 | CoT + 工具验证显著降低 |
| **延迟** | 多步推理耗时长 | 推理模型优化、并行执行 |
| **成本** | Token 消耗大 | 小模型路由、缓存策略 |
| **安全** | Prompt 注入、越狱 | Guardrails + 输入输出检测 |
| **可观测性** | Agent 行为难以追踪 | OpenTelemetry + Agent tracing |
| **评估** | 难以自动化评估 Agent 质量 | LLM-as-a-judge 评测体系 |

### 未来趋势

- **MCP 成为标准**：Agent 工具协议的行业标准化
- **端侧 Agent**：手机/PC 本地运行的小型 Agent
- **Agent 原生应用**：从"App+AI"到"AI Native"的转变
- **Agent 经济**：Agent 即服务（AaaS）商业模式成熟
- **可解释 Agent**：能清晰解释每一步决策的原因

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 Agent 概念 → 了解核心组件（感知/推理/工具/记忆）
> 2. **实践**：用 Spring AI 写第一个 Tool-Use Agent → 尝试简单的 Multi-Agent
> 3. **深入**：研究推理模式（ReAct/Reflexion）→ 学习 RAG + Agent 整合
> 4. **工程化**：Agent 安全 → 可观测性 → 评估体系 → 生产部署


---

> **📖 学习路线**：[[AIAgent篇/README|AI Agent 学习路线图]]
