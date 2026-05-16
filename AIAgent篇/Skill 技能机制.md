# Skill 技能机制

## 一、什么是 Skill

### 定义

在 AI Agent 体系中，**Skill（技能）** 是一组**相关能力的集合**，它比单个 Tool 高一个抽象层级，将 Agent 在某个领域所需的多项能力打包为一个可复用的模块。

```
Skill 在 AI Agent 架构中的定位

    ┌──────────────────────────────────────────────┐
    │               AI Agent                        │
    │                                                │
    │   ┌─────────────┐  ┌─────────────┐            │
    │   │  Reasoning   │  │  Memory     │            │
    │   └──────┬──────┘  └─────────────┘            │
    │          │                                     │
    │   ┌──────┴──────────────────────────┐          │
    │   │      Skill 层（能力分组）         │          │
    │   │                                  │          │
    │   │  ┌──────────────────────────┐   │          │
    │   │  │  CustomerService Skill   │   │          │
    │   │  │  ├─ queryOrder()         │   │          │
    │   │  │  ├─ cancelOrder()        │   │          │
    │   │  │  ├─ returnProduct()      │   │          │
    │   │  │  └─ trackLogistics()     │   │          │
    │   │  └──────────────────────────┘   │          │
    │   │  ┌──────────────────────────┐   │          │
    │   │  │  DataAnalysis Skill      │   │          │
    │   │  │  ├─ queryDatabase()      │   │          │
    │   │  │  ├─ generateChart()      │   │          │
    │   │  │  ├─ runStatistics()      │   │          │
    │   │  │  └─ exportReport()       │   │          │
    │   │  └──────────────────────────┘   │          │
    │   └──────────────────────────────────┘          │
    └──────────────────────────────────────────────┘
```

### Skill 解决了什么问题

| 问题 | 没有 Skill | 有 Skill |
|:----|:----------|:---------|
| **工具组织** | 几十个 `@Tool` 散落各处，难以管理 | 按领域分组为 Skill，清晰有序 |
| **复用性** | 每个 Agent 重复注册相同工具 | Skill 一次定义，多个 Agent 共享 |
| **权限控制** | 逐个配置工具权限，粒度太细 | 按 Skill 统一授权，粗粒度控制 |
| **上下文污染** | LLM 需要从几百个工具中选择，易混淆 | 按需加载 Skill，减少选择空间 |
| **发现性** | 新 Agent 开发者不清楚有哪些能力可用 | 浏览 Skill 目录即可了解能力全景 |

### Skill 的核心特征

1. **领域内聚**：一个 Skill 内的功能属于同一业务领域
2. **可复用**：Skill 可在不同 Agent 间共享
3. **可组合**：Agent 可以装备多个 Skill 形成综合能力
4. **可发现**：通过标准化接口发现和加载 Skill

---

## 二、Skill vs Tool vs Plugin vs Function

在 AI Agent 生态中，这几个概念常被混用，理解它们的区别非常重要。

### 概念分层

```
抽象层次              ┌──────────────┐
  高                 │    Skill     │  ← 领域能力集合（一组相关功能的打包）
                    │  (技能)      │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │   Plugin     │  ← 可插拔模块（Skill 的载体/实现方式）
                    │  (插件)      │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │    Tool      │  ← 具体功能单元（一个可调用的操作）
                    │  (工具)      │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
  低                │  Function    │  ← 底层实现（一段代码/API 调用）
                    │  (函数)      │
                    └──────────────┘
```

### 对比表

| 维度 | Function | Tool | Plugin | Skill |
|:----|:---------|:-----|:-------|:------|
| **粒度** | 最细 | 细 | 中 | 粗 |
| **内容** | 单个操作 | 单个可调用操作 | 一组 Tool + 配置 | 一组 Tool + 知识 + 策略 |
| **举例** | `calculate()` | `@Tool("计算")` | `math-plugin.jar` | `数据分析技能` |
| **依赖** | 无 | 无 | 可能有外部依赖 | 可能依赖多个 Plugin |
| **复用范围** | - | Agent 内 | 项目内 | 组织级 |
| **Spring AI** | `@Service` 方法 | `@Tool` 注解方法 | - | `@Service` 类（按类分组） |
| **Semantic Kernel** | `@kernel_function` | 单个函数 | `Plugin` 类 | 已重命名为 Plugin |
| **MCP** | - | `Tool` 能力 | `MCP Server` | MCP Server 提供的工具集 |

### 不同框架的命名差异

| 框架 | 集合概念 | 单元概念 | 说明 |
|:----|:--------|:---------|:-----|
| **Semantic Kernel** | `Plugin`（原 Skill） | `KernelFunction` | 2024 年起将 Skill 更名为 Plugin |
| **LangChain** | `Toolkit` | `Tool` | Toolkit 是相关 Tool 的集合 |
| **CrewAI** | `Skill` | `Tool` | 直接支持 Agent 装备 Skill |
| **AutoGen** | `Skill` | `Function` | 可序列化和共享的 Skill |
| **Spring AI** | `@Service` 类 | `@Tool` 方法 | 无显式 Skill 概念，按类自然分组 |
| **OpenAI** | `function` 列表 | `function` | 所有工具扁平化传入 |

---

## 三、Semantic Kernel 的 Plugin 系统 ⭐

Semantic Kernel 是 Skill/Plugin 概念的 **最完整实现**。虽然它在 2024 年将术语从 "Skill" 更名为 "Plugin"，但核心思想一脉相承。

### 两种函数类型

```python
# ⭐ Plugin 包含两种函数

# 1. Native Function（原生函数）—— 代码实现
class WeatherPlugin:
    @kernel_function(description="获取指定城市的天气")
    def get_weather(self, city: str) -> str:
        return weather_service.query(city)

    @kernel_function(description="获取未来一周天气预报")
    def get_forecast(self, city: str) -> list:
        return weather_service.forecast(city)


# 2. Semantic Function（语义函数）—— Prompt 实现
# 通过 .prompt 文件定义
"""
system:
你是一个天气助手。根据以下信息生成友好的天气报告。

Input: {{$city}}
Weather Data: {{WeatherPlugin.get_weather $city}}

输出格式：简洁、友好、包含温度范围和建议。
"""

# 这两种函数在同一个 Plugin 中混合使用
kernel.add_plugin(WeatherPlugin(), "Weather")
```

### Plugin 的结构

```
Plugin 目录结构
my-plugin/
├── plugin.json              # Plugin 元数据（名称、描述、版本）
├── functions/
│   ├── function-a/
│   │   ├── function.json    # 函数定义（参数 schema）
│   │   └── skprompt.txt     # 语义函数的 Prompt（仅语义函数需要）
│   └── function-b/
│       └── ...              # 可以是原生函数（代码实现）
```

### Java 版本

```java
// ⭐ Semantic Kernel for Java
public class WeatherPlugin {
    @KernelFunction(description = "获取指定城市的天气")
    public String getWeather(@KernelFunctionParameter(description = "城市名") String city) {
        return weatherService.query(city);
    }

    @KernelFunction(description = "获取未来一周天气预报")
    public List<Forecast> getForecast(
            @KernelFunctionParameter(description = "城市名") String city) {
        return weatherService.forecast(city);
    }
}

// 注册到 Kernel
Kernel kernel = Kernel.builder()
    .withPlugin(new WeatherPlugin())
    .withPlugin(new CustomerServicePlugin())
    .build();

// 自动函数调用
ChatHistory history = kernel.getService().createNewChat("北京明天天气如何？");
// Kernel 会自动决定调用 WeatherPlugin.getWeather
```

### 关键设计思想

1. **Plugin 即 Skill**：每个 Plugin 是一个领域能力的集合
2. **函数类型透明**：Agent 不区分 Native 还是 Semantic 函数，统一调用
3. **模板内联**：语义函数可以通过 `{{plugin.function}}` 语法在 Prompt 中引用其他函数
4. **自动编排**：Kernel 的 Planner 可自动组合多个 Plugin 完成任务

---

## 四、各框架的 Skill 机制对比

### LangChain：Toolkit

```python
# ⭐ LangChain Toolkit——相关 Tool 的集合
from langchain.tools import BaseToolkit

class CustomerServiceToolkit(BaseToolkit):
    """客服工具包"""

    def get_tools(self):
        return [
            Tool(name="query_order", func=query_order,
                 description="查询订单状态"),
            Tool(name="cancel_order", func=cancel_order,
                 description="取消订单"),
            Tool(name="track_logistics", func=track_logistics,
                 description="查询物流信息"),
        ]

# 使用
agent = create_react_agent(
    llm=llm,
    tools=CustomerServiceToolkit().get_tools(),
    # 也可以组合多个 Toolkit
    # tools=CustomerServiceToolkit().get_tools() + DataAnalysisToolkit().get_tools()
)
```

### CrewAI：Skill

```python
# ⭐ CrewAI Skill——Agent 可直接装备
from crewai import Agent, Skill

# 定义 Skill
data_analysis_skill = Skill(
    name="数据分析",
    description="数据查询、统计分析和可视化",
    tools=[sql_tool, chart_tool, statistics_tool]
)

# 装备给 Agent
analyst = Agent(
    role="数据分析师",
    goal="从数据中提取业务洞察",
    skills=[data_analysis_skill]  # ⭐ 装备 Skill
)

# 一个 Agent 可以装备多个 Skill
senior_analyst = Agent(
    role="高级分析师",
    skills=[data_analysis_skill, reporting_skill, python_skill]
)
```

### AutoGen：Skill

```python
# ⭐ AutoGen Skill——可序列化、可共享
from autogen import Skill

# 定义 Skill
data_pipeline_skill = Skill(
    name="data_pipeline",
    description="数据处理流水线技能",
    functions=[
        {
            "name": "extract_data",
            "description": "从数据源提取数据",
            "parameters": {...}
        },
        {
            "name": "transform_data",
            "description": "数据转换和清洗",
            "parameters": {...}
        },
        {
            "name": "load_data",
            "description": "加载数据到目标存储",
            "parameters": {...}
        }
    ]
)

# Skill 可以导出和分享
data_pipeline_skill.export("data_pipeline.yaml")
# 其他项目/Agent 可以导入使用
```

### Spring AI：按类自然分组

Spring AI 虽然没有显式的 `Skill` 注解，但通过 `@Service` 类来实现自然分组：

```java
// ⭐ Spring AI 中按类分组的等效 Skill 模式

// 一个 @Service 类 = 一个 Skill
@Service
public class CustomerServiceSkill {

    @Tool(description = "查询订单状态和物流信息")
    public Order queryOrder(@ToolParam String orderId) {
        return orderRepo.findById(orderId);
    }

    @Tool(description = "取消订单，仅待发货状态可取消")
    public CancelResult cancelOrder(@ToolParam String orderId,
                                     @ToolParam(required = false) String reason) {
        return orderService.cancel(orderId, reason);
    }

    @Tool(description = "申请退货退款")
    public ReturnResult requestReturn(@ToolParam String orderId,
                                       @ToolParam String reason) {
        return returnService.createReturn(orderId, reason);
    }
}

// 另一个 Skill
@Service
public class DataAnalysisSkill {

    @Tool(description = "执行 SQL 查询并返回结果")
    public List<Map<String, Object>> queryDatabase(@ToolParam String sql) {
        return jdbcTemplate.queryForList(sql);
    }

    @Tool(description = "根据数据生成图表 URL")
    public String generateChart(@ToolParam String data, @ToolParam String chartType) {
        return chartService.createChart(data, chartType);
    }
}

// Agent 选择要装备的 Skill
String result = chatClient.prompt()
    .user("查询订单 ORD-001 的状态")
    .tools(/* 仅注册 CustomerServiceSkill 的方法 */)
    .call()
    .content();
```

### 对比总览

| 框架 | Skill 概念 | 定义方式 | 复用机制 | 发现机制 |
|:----|:----------|:--------|:--------|:--------|
| **Semantic Kernel** | `Plugin` | 类 + `@KernelFunction` | 注册到 Kernel | Kernel 自动发现 |
| **LangChain** | `Toolkit` | 继承 `BaseToolkit` | `.get_tools()` | 手动调用获取 |
| **CrewAI** | `Skill` | `Skill(name, tools)` | 赋值给 Agent | Agent 初始化时加载 |
| **AutoGen** | `Skill` | `Skill(name, functions)` | 序列化导出/导入 | 文件系统加载 |
| **Spring AI** | `@Service` 类 | 普通 Spring Bean | DI 注入 | Spring 容器管理 |
| **MCP** | MCP Server | Server 定义 | 连接即获取 | `tools/list` 发现 |

---

## 五、MCP 与 Skill

在 MCP 协议体系中，**一个 MCP Server 天然就是一个 Skill 提供者**。

### MCP Server = Skill Provider

```
MCP Server 作为 Skill
┌─────────────────────────────────────────────┐
│            MCP Registry (工具市场)            │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  GitHub MCP Server     ★5000+ 安装   │   │
│  │  ├─ create_repository()              │   │
│  │  ├─ create_issue()                   │   │
│  │  ├─ create_pull_request()            │   │
│  │  └─ search_code()                    │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Database MCP Server     ★3200+ 安装  │   │
│  │  ├─ query()                          │   │
│  │  ├─ execute()                        │   │
│  │  └─ get_schema()                     │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Slack MCP Server       ★2800+ 安装   │   │
│  │  ├─ send_message()                   │   │
│  │  ├─ list_channels()                  │   │
│  │  └─ search_messages()                │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### MCP 的 Skill 发现流

```
Agent 连接 MCP Server 时：

1. Agent → MCP Client: "你有哪些能力？"
   (Client 发送 tools/list 请求)

2. MCP Client → MCP Server: tools/list
   (JSON-RPC 请求)

3. MCP Server → MCP Client: 返回工具列表
   {
     "tools": [
       {"name": "query_order", "description": "..."},
       {"name": "cancel_order", "description": "..."},
       {"name": "return_product", "description": "..."}
     ]
   }

4. MCP Client → Agent: 提供这些工具
   (Agent 将这些工具加入可用能力池)

5. Agent 判断任务需要哪个 Skill，选择性调用
```

**这意味着**：MCP 让 Skill 的发现、加载、调用变成了**标准化协议**，不同框架和语言之间可以无缝共享 Skill。

---

## 六、Skill 设计最佳实践

### 1. 粒度原则

```
❌ 太粗（一个 Skill 包含太多功能）
┌─────────────────────────────────────┐
│  AllInOneSkill                      │
│  ├─ 查订单、退换货、发短信、         │
│  ├─ 数据库查询、报表生成、           │
│  ├─ 用户管理、权限管理、             │
│  └─ 消息推送、邮件发送、...          │
│  共 30+ 个工具                      │
└─────────────────────────────────────┘
→ LLM 选择困难，上下文被污染

❌ 太细（每个功能独立 Skill）
┌──────────────────┐  ┌──────────────────┐
│  QueryOrderSkill  │  │  CancelOrderSkill │
│  └─ queryOrder()  │  │  └─ cancelOrder() │
└──────────────────┘  └──────────────────┘
→ 管理成本高，失去分组意义

✅ 适中（按领域分组）
┌─────────────────────────────────────┐
│  OrderManagementSkill               │
│  ├─ queryOrder()    ← 查询          │
│  ├─ cancelOrder()   ← 取消          │
│  ├─ returnProduct() ← 退货          │
│  └─ trackLogistics() ← 物流        │
│  4-8 个工具/领域                    │
└─────────────────────────────────────┘
```

### 2. Skill 设计清单

```yaml
# ⭐ Skill 设计规范
OrderManagementSkill:
  命名: "订单管理技能"
  描述: "订单查询、取消、退货和物流追踪"
  领域: "电商-订单"
  依赖: [用户服务, 订单服务, 物流服务]
  
  工具列表:
    queryOrder:
      名称: "查询订单"
      输入: "订单号"
      输出: "订单详情（含状态、金额、商品）"
      异常: "订单不存在"
    
    cancelOrder:
      名称: "取消订单"
      输入: "订单号 + 可选原因"
      输出: "取消结果"
      前置条件: "仅待发货可取消"
      异常: "订单状态不允许取消"
    
    returnProduct:
      名称: "申请退货"
      输入: "订单号 + 原因"
      输出: "退货申请结果"
      后置: "自动触发退款流程"
    
    trackLogistics:
      名称: "物流查询"
      输入: "订单号 / 运单号"
      输出: "物流轨迹"
  
  权限:
    角色: [客服, 用户本人]
    限制: "只能查询自己的订单"
```

### 3. Skill 接口规范

```java
// ⭐ Skill 接口定义（推荐）
public interface AgentSkill {
    /** 获取 Skill 名称 */
    String getSkillName();

    /** 获取 Skill 描述 */
    String getSkillDescription();

    /** 获取所属领域 */
    String getDomain();
}

// Skill 实现
@Service
public class OrderManagementSkill implements AgentSkill {

    @Override
    public String getSkillName() {
        return "订单管理技能";
    }

    @Override
    public String getSkillDescription() {
        return "订单查询、取消、退货和物流追踪";
    }

    @Override
    public String getDomain() {
        return "电商-订单";
    }

    @Tool(description = "查询订单状态")
    public Order queryOrder(@ToolParam String orderId) { ... }

    @Tool(description = "取消订单")
    public CancelResult cancelOrder(@ToolParam String orderId) { ... }
}
```

### 4. Skill 组合策略

```java
// ⭐ Agent 按需装载 Skill
@Service
public class SkillOrchestrator {

    private final Map<String, AgentSkill> skillRegistry;

    public SkillOrchestrator(List<AgentSkill> skills) {
        // 自动发现所有 Skill Bean
        this.skillRegistry = skills.stream()
            .collect(Collectors.toMap(AgentSkill::getSkillName, s -> s));
    }

    /**
     * 根据任务类型推荐 Skill
     */
    public List<String> recommendSkills(String taskDescription) {
        // 可以用 LLM 判断任务需要的 Skill
        String prompt = """
            任务描述：%s
            可用技能：%s
            请返回完成任务所需要的技能名称列表。
            """.formatted(taskDescription, skillRegistry.keySet());

        return llm.recommend(prompt);  // ["订单管理技能", "用户管理技能"]
    }

    /**
     * 动态注册推荐的工具到 ChatClient
     */
    public String execute(String task) {
        List<String> skillNames = recommendSkills(task);

        // 只注册推荐的 Skill 中的 Tool
        return chatClient.prompt()
            .user(task)
            .tools(skillNames.stream()
                .flatMap(name -> extractTools(skillRegistry.get(name)))
                .toArray(String[]::new))
            .call()
            .content();
    }
}
```

---

## 七、Skill 实战案例

### 案例：智能客服系统

```java
// ⭐ 多 Skill 组合的客服 Agent

// Skill 1: 订单管理
@Service
public class OrderSkill {
    @Tool(description = "查询订单")
    public Order queryOrder(@ToolParam String orderId) { ... }
    @Tool(description = "取消订单")
    public void cancelOrder(@ToolParam String orderId) { ... }
}

// Skill 2: 售后服务
@Service
public class AfterSaleSkill {
    @Tool(description = "提交退货申请")
    public ReturnRequest createReturn(@ToolParam String orderId) { ... }
    @Tool(description = "查询退款进度")
    public RefundStatus checkRefund(@ToolParam String requestId) { ... }
}

// Skill 3: 用户管理
@Service
public class UserSkill {
    @Tool(description = "查询用户信息")
    public User getUser(@ToolParam Long userId) { ... }
    @Tool(description = "更新联系方式")
    public void updateContact(@ToolParam Long userId, @ToolParam String phone) { ... }
}

// 客服 Agent —— 按需装备 3 个 Skill
@Bean
public ChatClient customerServiceBot(ChatClient.Builder builder) {
    return builder
        .defaultSystem("你是电商客服助手，可以处理订单查询、售后和用户信息修改。")
        .defaultTools(
            // 注册 3 个 Skill 中的所有 @Tool
            "queryOrder", "cancelOrder",
            "createReturn", "checkRefund",
            "getUser", "updateContact"
        )
        .build();
}
```

### 案例：数据分析 Agent

```java
// ⭐ 按任务复杂度动态选择 Skill

@Service
public class DataAnalysisAgent {

    private final ChatClient chatClient;

    @Tool(description = "查询客户数据库")
    public List<Map<String, Object>> queryDB(@ToolParam String sql) { ... }

    @Tool(description = "执行 Python 数据分析脚本")
    public String runPython(@ToolParam String code) { ... }

    @Tool(description = "生成可视化图表")
    public String visualize(@ToolParam String data, @ToolParam String type) { ... }

    @Tool(description = "导出报告为 PDF")
    public String exportReport(@ToolParam String content) { ... }

    public String analyze(String question) {
        // 简单问题：只用 queryDB
        if (isSimpleQuestion(question)) {
            return chatClient.prompt()
                .user(question)
                .tools("queryDB")
                .call()
                .content();
        }

        // 复杂分析：使用全部数据技能
        return chatClient.prompt()
            .user(question)
            .tools("queryDB", "runPython", "visualize", "exportReport")
            .call()
            .content();
    }
}
```

---

## 八、总结

### Skill 的核心价值

```
没有 Skill                  有 Skill
───────────                ──────────
30 个 Tool 平铺            按领域分组为 5 个 Skill
├─ queryOrder()            ├─ 📦 订单管理 (4 tools)
├─ cancelOrder()           ├─ 📦 售后服务 (3 tools)
├─ getUser()               ├─ 📦 用户管理 (2 tools)
├─ sendSms()               ├─ 📦 消息通知 (2 tools)
├─ queryDB()               └─ 📦 数据分析 (3 tools)
├─ generateChart()
├─ ...  (共30个)
                            ✅ 清晰：一眼知道 Agent 能做什么
❌ 混乱：LLM 选择困难       ✅ 高效：按需加载，减少上下文
❌ 难复用：每个 Agent 重配  ✅ 复用：一次定义，多处使用
```

### 选型建议

| 你的技术栈 | 推荐的 Skill 模式 |
|:----------|:-----------------|
| **Spring Boot + Spring AI** | `@Service` 类按领域分组 + `tools()` 选择性注册 |
| **Semantic Kernel (Java/.NET)** | `Plugin` + `@KernelFunction`，利用 Kernel 自动编排 |
| **LangChain (Python)** | `Toolkit` + `get_tools()` 组合 |
| **CrewAI (Python)** | `Skill(name, tools)` 直接装备给 Agent |
| **MCP 生态** | MCP Server 作为 Skill Provider，`tools/list` 发现 |

> [!tip] **Spring AI 使用建议**
> Spring AI 虽然没有显式的 Skill 注解，但利用 `@Service` 按领域分组 `@Tool` 方法就是最自然的 Skill 模式。配合 `tools()` 方法选择性注册，可以实现按需加载，既保持代码整洁，又减少 LLM 的上下文污染。

---

> [!note] **术语变迁说明**
> Semantic Kernel 在 2024 年将 "Skill" 更名为 "Plugin"，但社区和其他框架仍广泛使用 "Skill" 一词。本笔记中两者视为同一概念——都是"一组相关能力的集合"。MCP 协议的广泛采用（2025-2026）进一步推动了 Skill 的标准化，使得不同语言和框架间的 Skill 可以互操作。
