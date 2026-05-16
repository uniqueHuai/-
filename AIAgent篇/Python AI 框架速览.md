# Python AI 框架速览

## 一、概述

虽然你是 Java 开发者，但 AI Agent 生态的**核心框架和创新最先出现在 Python 生态**。了解这些框架的概念和设计思想，能帮你更好地理解 AI Agent 的全貌，也能在跨语言协作时心中有数。

```
Python AI 框架生态（2026）

                     ┌─────────────────────────┐
                     │      LangChain           │
                     │    通用 Agent 框架        │
                     │    最广泛使用             │
                     └────────┬────────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  LangGraph    │ │  CrewAI      │ │  AutoGen     │
    │  图状态机     │ │  多角色协作   │ │  多 Agent 对话│
    │  复杂工作流   │ │  开箱即用    │ │  MS 出品     │
    └──────────────┘ └──────────────┘ └──────────────┘
             │                │                │
             └────────────────┼────────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Semantic    │ │  Dify        │ │  Haystack    │
    │  Kernel      │ │  低代码平台  │ │  企业 RAG    │
    │  Microsoft   │ │  可视化编排  │ │  搜索增强    │
    └──────────────┘ └──────────────┘ └──────────────┘
```

### 学习原则

对于 Java 开发者，学习 Python AI 框架应遵循 **"了解概念，理解思想，不深入代码"** 的原则：

```
✅ 需要了解的：
   ├── 核心概念（Chain/Agent/Tool/Graph）
   ├── 设计思想（为什么这样设计）
   ├── 解决的问题和适用场景
   └── 和 Spring AI 的对应关系

❌ 不需要的：
   ├── Python 语法细节
   ├── 具体 API 参数
   ├── 性能调优
   └── 部署运维细节
```

---

## 二、LangChain ⭐

### 定位

**LangChain** 是 AI Agent 领域**最知名、生态最丰富**的通用框架。2026 年的版本为 **LangChain 0.6.x**。

### 核心概念

```
LangChain 的核心抽象

    ┌──────────────────────────────┐
    │        Model（模型抽象）       │
    │  ChatModel / Embedding / ... │
    └──────────────┬───────────────┘
                   │
    ┌──────────────┴───────────────┐
    │        Prompt（提示词管理）    │
    │  Template / FewShot / ...   │
    └──────────────┬───────────────┘
                   │
    ┌──────────────┴───────────────┐
    │        Chain（链）            │
    │  将多个步骤串联为管道          │
    └──────────────┬───────────────┘
                   │
    ┌──────────────┴───────────────┐
    │        Agent（智能体）         │
    │  自主决策 + 工具调用 + 记忆    │
    └──────────────┬───────────────┘
                   │
    ┌──────────────┴───────────────┐
    │        Tool（工具）           │
    │  Function / API / Retriever │
    └──────────────┬───────────────┘
                   │
    ┌──────────────┴───────────────┐
    │        Memory（记忆）         │
    │  Buffer / Summary / Vector  │
    └──────────────────────────────┘
```

### 和 Spring AI 的对应关系

| LangChain 概念 | Spring AI 对应 | 说明 |
|:--------------|:--------------|:-----|
| `ChatModel` | `ChatModel` | LLM 抽象，概念完全一致 |
| `PromptTemplate` | Prompt 模板（`param()`） | 提示词模板化 |
| `Chain` | `ChatClient` chainable API | 处理链（Spring AI 更简洁） |
| `Agent` | `ChatClient` + `@Tool` | Agent 模式 |
| `Tool` | `@Tool` / `ToolCallback` | 工具定义 |
| `BaseMemory` | `ChatMemory` | 会话记忆 |
| `VectorStore` | `VectorStore` | 向量存储 |
| `Document Loader` | `DocumentReader` | 文档加载 |
| `Callbacks` | `Advisor` | 拦截器/回调 |

### 特点

- **优点**：生态最丰富，20+ 模型、15+ 向量库、大量社区插件
- **优点**：文档和教程最完善
- **缺点**：API 变化频繁（0.5→0.6 有 breaking change）
- **缺点**：抽象层较厚，调试困难

---

## 三、LangGraph ⭐

### 定位

**LangGraph** 是基于 **图状态机** 构建 Agent 工作流的框架。相比 LangChain 的线性 Chain，LangGraph 支持**循环、分支、并行**等复杂拓扑结构。

### 解决的问题

```
    传统 Chain（线性）                 LangGraph（图）
    ┌──────────┐                    ┌──────────┐
    │ Step 1   │                    │  Start   │
    └────┬─────┘                    └────┬─────┘
         ▼                               │
    ┌──────────┐                    ┌────┴─────┐
    │ Step 2   │                    │  Router  │
    └────┬─────┘                    └────┬─────┘
         ▼                          │         │
    ┌──────────┐                    ▼         ▼
    │ Step 3   │              ┌────────┐ ┌────────┐
    └──────────┘              │ Step A │ │ Step B │  ← 并行
                              └───┬────┘ └───┬────┘
                                  │         │
                                  └────┬─────┘
                                       ▼
                                  ┌──────────┐
                                  │  Join    │
                                  └────┬─────┘
                                       ▼
                                  ┌──────────┐
                                  │  End     │
                                  └──────────┘
```

### Agent 应用场景

```python
# LangGraph 实现的 Agent 循环（伪代码）
def agent_workflow():
    # 定义图结构
    builder = StateGraph(AgentState)

    # 节点
    builder.add_node("reason", reasoning_node)        # 推理
    builder.add_node("tool_call", tool_calling_node)  # 工具调用
    builder.add_node("reflect", reflection_node)      # 反思

    # 边（含条件判断）
    builder.add_conditional_edges("reason",
        decide_next,           # 决定下一步：调工具还是直接回答
        {"tool": "tool_call", "end": END}
    )
    builder.add_edge("tool_call", "reflect")
    builder.add_edge("reflect", "reason")  # 反思后回到推理（循环）

    return builder.compile()

# ⭐ 循环结构：这个 Agent 会持续推理→工具→反思→推理...直到完成
```

### 和 Spring AI 的对应

Spring AI 虽然没有直接的"图状态机"，但可以通过 **Multi-Agent 编排 + Advisor 链** 实现类似效果。

---

## 四、CrewAI

### 定位

**CrewAI** 是专注于 **多 Agent 角色协作** 的框架，让定义 AI 团队变得非常简单。2026 年版本为 **CrewAI 0.9.x**。

### 核心思想

```python
# CrewAI 的核心概念（伪代码）

# 1. 定义角色
analyst = Agent(
    role="数据分析师",
    goal="从数据中发现业务洞察",
    tools=[sql_tool, chart_tool]
)

writer = Agent(
    role="报告撰写员",
    goal="将分析结果写成易读的报告"
)

# 2. 定义任务
analysis_task = Task(
    description="分析上季度销售数据",
    agent=analyst
)

writing_task = Task(
    description="将分析结果写成报告",
    agent=writer,
    depends_on=[analysis_task]  # 依赖前置任务
)

# 3. 组建团队并开始工作
crew = Crew(
    agents=[analyst, writer],
    tasks=[analysis_task, writing_task],
    process=Process.sequential  # 串行执行
)

result = crew.kickoff()
```

### 特点

- **优点**：上手极快，角色定义清晰
- **优点**：内置任务委派、进度跟踪
- **缺点**：灵活性不如 LangGraph
- **应用场景**：内容创作团队、数据分析流水线、客服团队

### Spring AI 对应

可以用 Spring AI 的多个 `ChatClient` Bean 配合 `@Tool` 实现类似效果，但 CrewAI 的"角色+任务"模式更开箱即用。

---

## 五、AutoGen

### 定位

**AutoGen** 是 Microsoft 开源的**多 Agent 对话框架**，强调 Agent 之间的**自主对话**来完成任务。2026 年版本为 **AutoGen 0.8.x**。

### 核心思想

```python
# AutoGen 的对话模式（伪代码）

# 两个 Agent 通过对话协作
assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-5"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution=True  # 可以执行代码
)

# Agent 之间自主对话完成任务
user_proxy.initiate_chat(
    assistant,
    message="帮我分析这份数据并生成图表"
)
# 对话流程：
# UserProxy → Assistant: "帮我分析数据"
# Assistant → UserProxy: "我先读取数据..."
# UserProxy → Assistant: 执行结果
# Assistant → UserProxy: "生成图表如下..."
```

### 特点

- **优点**：Agent 间自由对话，适合复杂协作
- **优点**：内置代码执行沙箱
- **缺点**：对话流程不可控，调试困难
- **应用场景**：代码生成、数据分析、科研实验

---

## 六、框架对比总览

### 选择指南

| 框架 | 核心优势 | 最适合场景 | 学习成本 | 活跃度 |
|:----|:--------|:---------|:--------|:------|
| **LangChain** | 生态最丰富，通用性强 | 通用 Agent 开发 | 中 | ⭐⭐⭐⭐⭐ |
| **LangGraph** | 图状态机，处理循环/分支 | 复杂工作流、Agent 循环 | 高 | ⭐⭐⭐⭐⭐ |
| **CrewAI** | 角色协作，开箱即用 | 多 Agent 团队 | 低 | ⭐⭐⭐⭐ |
| **AutoGen** | Agent 自主对话 | 复杂协作任务 | 中 | ⭐⭐⭐⭐ |
| **Semantic Kernel** | 企业级，Microsoft 生态 | Azure 用户，.NET 项目 | 中 | ⭐⭐⭐⭐ |
| **Dify** | 可视化低代码 | 非开发者、快速原型 | 低 | ⭐⭐⭐⭐ |
| **Haystack** | RAG 和搜索增强 | 文档 QA、搜索系统 | 中 | ⭐⭐⭐ |

### Spring AI 和 Python 框架的定位差异

```text
Spring AI（Java）
├── 定位：企业级 AI 工程化
├── 优势：Spring Boot 整合、类型安全、运维完善
├── 适用：Java 技术栈的生产系统
└── 特点：稳、安全、可维护

Python 框架（LangChain/LangGraph/CrewAI）
├── 定位：AI 创新快速迭代
├── 优势：功能最新、生态最丰富
├── 适用：AI 原型验证、数据科学团队
└── 特点：快、灵活、丰富
```

> [!tip] **给 Java 开发者的建议**
> 了解 Python 框架的**核心概念**比学会 API 更重要。LangChain 的 Chain/Agent/Tool 思想已经被 Spring AI 借鉴吸收。当你遇到 Spring AI 不支持的场景时，可以看看 Python 框架是如何设计的，再在 Java 中用类似思路实现。
