# MCP 协议

## 一、什么是 MCP

### 定义

**MCP（Model Context Protocol，模型上下文协议）** 是 Anthropic 于 2024 年底提出、到 2026 年已成为行业标准的 **AI Agent 工具集成协议**。它定义了一套标准化的通信方式，让 AI 应用程序（Host）能够通过统一的接口发现和调用外部工具、获取数据资源。

```
    MCP 解决的问题

    传统方式（每个工具独立集成）               MCP 方式（统一协议）
    ┌──────────────────────┐          ┌──────────────────────┐
    │  Agent 应用          │          │  Agent 应用           │
    │                      │          │                      │
    │  ├─ 文件系统: os lib │          │  MCP Client           │
    │  ├─ 数据库: JDBC    │          │  (统一协议)            │
    │  ├─ 搜索引擎: 专用SDK│          └──────────┬───────────┘
    │  ├─ GitHub: octokit  │                     │
    │  └─ 内部API: HTTP    │          ┌──────────┴───────────┐
    │                      │          │   MCP Server          │
    │  每接一个工具要：     │          │   (提供工具/资源)      │
    │  - 找 SDK 文档       │          │                      │
    │  - 学不同 API 风格   │          │   ├─ 文件系统          │
    │  - 处理不同认证方式   │          │   ├─ 数据库            │
    │  - 维护 N 套集成     │          │   ├─ 搜索引擎          │
    └──────────────────────┘          │   ├─ GitHub           │
                                      │   └─ 内部 API         │
                                      │                      │
                                      │   一次实现，到处可用   │
                                      └──────────────────────┘
```

### 为什么需要 MCP

| 传统问题 | MCP 方案 |
|:---------|:---------|
| 每个工具不同 SDK、不同 API | 统一 JSON-RPC 2.0 协议 |
| 工具接入成本高，重复造轮子 | 一次开发 MCP Server，任何 Agent 可用 |
| 工具和 Agent 紧耦合 | 松耦合，两端独立演进 |
| 工具能力发现靠文档 | MCP Server 自动暴露可用工具列表 |
| 静态工具集，部署后难扩展 | 动态发现，按需加载工具 |

### 2026 年的 MCP

截止 2026 年 5 月，MCP 已成为 Agent 工具集成的行业标准：

```text
MCP 生态发展（2024-2026）
───────────────────────────────────────
2024.11  Anthropic 发布 MCP 规范 (v0.1)
2025.03  OpenAI 宣布支持 MCP
2025.06  Spring AI 原生支持 MCP
2025.09  MCP 规范 v1.0 发布
2025.12  Google、Microsoft、AWS 加入 MCP 联盟
2026.02  MCP Registry 上线（官方工具市场）
2026.05  MCP 已成为 Agent 工具集成的事实标准
         └── 超过 5000+ 公开 MCP Server
         └── 所有主流 AI 框架原生支持
         └── 各大 SaaS 厂商官方提供 MCP Server
```

---

## 二、MCP 核心架构

### 三层架构

```
┌────────────────────────────────────────────────────┐
│  Host（宿主应用）                                    │
│  AI 应用程序，如：                                   │
│  - AI Agent 系统                                    │
│  - AI Coding 工具 (Cursor/Claude Code)              │
│  - AI 聊天应用                                       │
│                                                    │
│  包含 MCP Client                                    │
└──────────────────┬─────────────────────────────────┘
                   │
                   │ JSON-RPC 2.0 over
                   │ stdio / SSE / WebSocket
                   │
┌──────────────────┴─────────────────────────────────┐
│  MCP Server（MCP 服务器）                            │
│  提供工具、资源、提示模板的独立服务                      │
│                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Tools      │  │  Resources  │  │  Prompts    │ │
│  │  (可调用的)  │  │  (数据源)    │  │  (提示模板)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────┘
                   │
                   │ 内部实现
                   ▼
┌────────────────────────────────────────────────────┐
│  实际能力（背后对接的具体工具/数据）                    │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ 文件  │ │ 数据库│ │ 搜索  │ │ API  │ │ 其他  │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
└────────────────────────────────────────────────────┘
```

### 三大核心能力

```
MCP Server 暴露三类能力：

1. Tools（工具）—— ⭐ 最常用
   可被 LLM 调用的函数。
   定义：名称 + 描述 + 参数 JSON Schema
   过程：调用 → 执行 → 返回结果
   示例：get_weather、query_database、send_email

2. Resources（资源）
   暴露给 LLM 的结构化数据。
   类似文件系统的 URI 方案。
   示例：file:///logs/app.log、doc://internal/guide.pdf

3. Prompts（提示模板）
   预定义的 Prompt 模板。
   示例：代码审查模板、系统设计模板
```

### 通信协议

```json
// JSON-RPC 2.0 消息

// 请求：列出可用工具
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}

// 响应：工具列表
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "tools": [
            {
                "name": "get_weather",
                "description": "获取天气",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": { "type": "string" }
                    },
                    "required": ["city"]
                }
            }
        ]
    }
}

// 请求：调用工具
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {
            "city": "北京"
        }
    }
}

// 响应：工具结果
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "北京：25°C，晴"
            }
        ]
    }
}
```

---

## 三、快速搭建 MCP Server ⭐

### 使用 MCP SDK（Java/Spring）

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-server-spring-boot-starter</artifactId>
    <version>1.6.2</version>
</dependency>
```

```java
// ⭐ Spring Boot MCP Server
@SpringBootApplication
@EnableMcpServer
public class McpServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }
}
```

```java
// ⭐ 注册 MCP 工具——和 Spring AI 的 @Tool 一致
@Configuration
public class McpTools {

    @Bean
    @Tool(description = "执行 SQL 查询并返回结果")
    public Function<QueryRequest, QueryResponse> queryDatabase() {
        return request -> {
            List<Map<String, Object>> results =
                jdbcTemplate.queryForList(request.sql());
            return new QueryResponse(results);
        };
    }

    @Bean
    @Tool(description = "读取指定路径的文件内容")
    public Function<FileRequest, FileResponse> readFile() {
        return request -> {
            String content = Files.readString(Path.of(request.path()));
            return new FileResponse(content);
        };
    }

    @Bean
    @Tool(description = "搜索内部文档知识库")
    public Function<SearchRequest, SearchResponse> searchDocs() {
        return request -> {
            List<Document> docs = vectorStore.similaritySearch(
                SearchRequest.query(request.query())
                    .withTopK(5)
            );
            return new SearchResponse(docs);
        };
    }
}

// ⭐ POJO
public record QueryRequest(String sql) {}
public record QueryResponse(List<Map<String, Object>> results) {}
public record FileRequest(String path) {}
public record FileResponse(String content) {}
public record SearchRequest(String query) {}
public record SearchResponse(List<Document> results) {}
```

### 配置 MCP 传输

```yaml
# application.yml
spring:
  ai:
    mcp:
      server:
        # 传输方式
        transport: stdio   # stdio（默认）或 sse

        # stdio 模式——子进程通过标准输入输出通信
        # 适用于同一台机器，性能最好

        # SSE 模式——HTTP Server-Sent Events
        # 适用于远程服务，支持跨网络
```

```yaml
# SSE 模式配置
spring:
  ai:
    mcp:
      server:
        transport: sse
        sse:
          port: 8081
```

---

## 四、MCP Client 集成

### Spring AI MCP Client

```java
// ⭐ Spring Boot MCP Client
@SpringBootApplication
@EnableMcpClient
public class AgentApplication {

    public static void main(String[] args) {
        SpringApplication.run(AgentApplication.class, args);
    }
}
```

```java
// ⭐ MCP 客户端——自动发现远程服务器上的工具
@Service
public class McpAgentService {

    private final ChatClient chatClient;

    // MCP 客户端自动将远程服务器上的工具注册为本地 @Tool
    public McpAgentService(ChatClient.Builder builder,
                            McpToolAdapter mcpAdapter) {
        this.chatClient = builder
            .defaultTools(mcpAdapter)  // 注入 MCP 工具
            .build();
    }

    public String chat(String message) {
        return chatClient.prompt()
            .user(message)
            .call()
            .content();
        // Agent 可以调用 MCP Server 上的所有工具，
        // 就像调用本地 @Tool 一样
    }
}
```

### 连接远程 MCP Server

```yaml
# application.yml —— MCP Client 配置
spring:
  ai:
    mcp:
      client:
        # stdio 模式——启动子进程
        stdio:
          servers:
            - command: node
              args: ["path/to/mcp-server.js"]
            - command: java
              args: ["-jar", "mcp-server.jar"]

        # SSE 模式——HTTP 连接远程 MCP Server
        sse:
          servers:
            - url: http://mcp-server.company.com:8081
            - url: http://internal-mcp:8081
```

### 从 Cursor / Claude Code 连接 MCP

```json
// mcp.json —— 在 Cursor/Claude Code 中配置
{
  "mcpServers": {
    "company-database": {
      "command": "java",
      "args": ["-jar", "mcp-db-server.jar"],
      "env": {
        "DB_URL": "jdbc:mysql://...",
        "DB_USER": "readonly",
        "DB_PASS": "***"
      }
    },
    "company-wiki": {
      "command": "python",
      "args": ["mcp-wiki-server.py"]
    },
    "jira-integration": {
      "url": "https://mcp.company.com/jira"
    }
  }
}
```

---

## 五、MCP Server 开发实战 ⭐

### Python MCP Server

```python
# ⭐ Python MCP Server 示例
# 用任意语言实现，统一协议
from mcp.server import Server, stdio_server
import httpx

app = Server("devops-tools")

@app.tool()
def query_pod_status(namespace: str, pod_name: str = None) -> str:
    """查询 Kubernetes Pod 状态"""
    result = kubectl.get_pods(namespace, pod_name)
    return format_pod_result(result)

@app.tool()
def search_logs(service: str, keywords: str, lines: int = 100) -> str:
    """搜索服务日志"""
    logs = log_service.search(service, keywords, lines)
    return logs

@app.tool()
def get_server_load(host: str) -> str:
    """查询服务器负载"""
    load = monitor.get_load(host)
    return f"CPU: {load.cpu}%, MEM: {load.mem}%, DISK: {load.disk}%"

if __name__ == "__main__":
    with stdio_server() as (read, write):
        app.run(read, write)
```

### Node.js MCP Server

```javascript
// ⭐ Node.js MCP Server
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "github-tools",
  version: "1.0.0",
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "create_issue",
    description: "在 GitHub 仓库创建 Issue",
    inputSchema: {
      type: "object",
      properties: {
        repo: { type: "string" },
        title: { type: "string" },
        body: { type: "string" }
      },
      required: ["repo", "title"]
    }
  }]
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "create_issue") {
    const { repo, title, body } = request.params.arguments;
    const issue = await github.createIssue(repo, title, body);
    return {
      content: [{ type: "text", text: `Issue #${issue.number} 已创建` }]
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 用任何语言实现 MCP Server

```bash
# MCP 协议基于 JSON-RPC 2.0 over stdio
# → 任何语言只要支持标准输入输出即可实现

# 标准输入：接收 JSON-RPC 请求
# 标准输出：发送 JSON-RPC 响应
# 标准错误：日志（不影响通信）

# 用一个 bash 脚本就能实现最简单的 MCP Server：
```

```bash
#!/bin/bash
# mcp-server.sh —— 极简 MCP Server
while read -r line; do
    case $(echo "$line" | jq -r '.method') in
        "tools/list")
            echo '{
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "tools": [{
                        "name": "hello",
                        "description": "返回问候",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"}
                            },
                            "required": ["name"]
                        }
                    }]
                }
            }'
            ;;
        "tools/call")
            echo '{"jsonrpc":"2.0","id":1,"result":{"content":[
                {"type":"text","text":"你好！"}
            ]}}'
            ;;
    esac
done
```

---

## 六、MCP 在 Agent 中的应用

### Agent 架构中的 MCP

```
                    ┌──────────────────────────┐
                    │   AI Agent（主应用）       │
                    │                          │
                    │  ChatClient + MCP Client  │
                    └──────────┬───────────────┘
                               │
                               │ 发现工具 / 调用工具
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ 内部 MCP     │   │ 官方 MCP     │   │ 第三方 MCP   │
   │ Server       │   │ Server       │   │ Server       │
   │              │   │              │   │              │
   │ 数据库查询   │   │ 文件系统     │   │ GitHub API   │
   │ 内部 API    │   │ 搜索引擎     │   │ Jira API     │
   │ 知识库      │   │ Shell 执行   │   │ Slack API    │
   │ 日志系统    │   │ 代码操作     │   │ 飞书/钉钉    │
   └──────────────┘   └──────────────┘   └──────────────┘
```

### 企业内部 MCP 实践

```yaml
# 企业级 MCP 工具集配置

# AI 助手可以连接的所有 MCP Server
mcp_servers:
  # 1. 数据库查询（只读）
  database-reader:
    command: java -jar mcp-db-reader.jar
    config: readonly=true

  # 2. 内部知识库
  knowledge-base:
    command: python mcp-wiki-server.py

  # 3. 运维工具
  ops-tools:
    command: node mcp-ops-server.js

  # 4. 代码仓库
  git-platform:
    url: https://mcp.git.company.com

  # 5. 项目管理
  project-management:
    url: https://mcp.jira.company.com

  # 6. 监控告警
  monitoring:
    command: python mcp-monitor-server.py
```

---

## 七、MCP Registry（2026）⭐

### 官方工具市场

2026 年，MCP Registry（官方工具市场）已上线，提供 5000+ 公开 MCP Server：

```bash
# 搜索 MCP Server
mcp search database
mcp search "git platform"
mcp search "weather"

# 安装 MCP Server
mcp install @mcp-server/postgres
mcp install @mcp-server/github
mcp install @mcp-server/slack

# 查看已安装
mcp list
```

```json
{
  "dependencies": {
    "@mcp-server/postgres": "^2.1.0",
    "@mcp-server/github": "^3.0.0",
    "@mcp-server/slack": "^1.5.0"
  }
}
```

---

## 八、安全考虑

### MCP 安全最佳实践

```yaml
# MCP Server 安全配置
spring:
  ai:
    mcp:
      server:
        # 允许的操作
        allowed-tools:
          - query_*
          - search_*
          - read_*
        # 禁止的操作
        denied-tools:
          - delete_*
          - drop_*
          - shutdown_*

        # API 密钥
        api-keys:
          database: ${DB_READONLY_KEY}
          internal-api: ${INTERNAL_API_KEY}
```

```java
// ⭐ 在 MCP 工具实现中做权限校验
@Bean
@Tool(description = "删除用户（仅管理员可用）")
public Function<DeleteUserRequest, String> deleteUser() {
    return request -> {
        // 校验调用来源是否有权限
        if (!mcpContext.hasRole("ADMIN")) {
            throw new SecurityException("仅管理员可执行此操作");
        }
        userService.deleteUser(request.userId());
        return "用户已删除";
    };
}
```

### 安全 Checklist

```
✅ 只读工具和写工具分离在不同 Server
✅ 数据库 MCP Server 使用只读账号
✅ 敏感操作增加二次确认机制
✅ 每个 MCP Server 最小权限原则
✅ 通信加密（TLS for SSE 模式）
✅ 审计日志记录所有工具调用
✅ 调用频率限制（Rate Limit）
✅ 定期安全审查 MCP Server 暴露的能力
```

---

## 九、常见面试题

### 1. MCP 解决了什么问题？

> 解决了 AI Agent 工具集成的**标准化问题**。以前每个工具需要单独的 SDK 和集成方式，MCP 统一为 JSON-RPC 2.0 协议，一次实现 MCP Server 就能被任何支持 MCP 的 Agent 使用。类比 USB 标准——统一接口，即插即用。

### 2. MCP 和普通 API 有什么区别？

> 普通 API 需要 Agent 框架硬编码调用逻辑和参数格式。MCP Server **自动暴露工具列表和参数 Schema**，Agent 可以动态发现可用工具并生成正确的调用参数。MCP 是"让 Agent 能自主使用 API"的协议，不只是一个 API。

### 3. MCP 在 Spring AI 中怎么用？

> `@EnableMcpServer` 开启 MCP Server，`@Tool` 注解自动暴露为 MCP 工具。`@EnableMcpClient` 连接远程 MCP Server，远程工具自动注入为本地可用工具。支持 stdio（本地进程）和 SSE（远程服务）两种传输方式。

### 4. 什么时候需要自己写 MCP Server？

> 当你有内部系统想要暴露给 AI Agent 使用时需要写 MCP Server。比如内部 API、公司知识库、运维工具、数据库查询等。用 Spring AI 的 `@Tool` 或 Python/Node 的 MCP SDK 都可以快速实现。

### 5. MCP 的安全怎么保障？

> 最小权限原则（只读账号拆分）、工具白名单/黑名单、敏感操作二次确认、TLS 加密传输、审计日志。写入和删除操作应该放在独立的 MCP Server 中严格控制。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 MCP 概念 → 三层架构（Host/Server/能力）
> 2. **实践**：用 Spring AI @Tool 写一个 MCP Server → 用 MCP Client 连接它
> 3. **深入**：stdio vs SSE 传输 → 多 Server 编排 → MCP Registry 使用
> 4. **工程化**：企业 MCP 架构设计 → 安全加固 → 监控与审计


---

> **📖 学习路线**：[[AIAgent篇/README|AI Agent 学习路线图]]
