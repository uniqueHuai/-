# LLM 原理与选型

## 一、LLM 基本原理

### 什么是大语言模型

**LLM（Large Language Model）** 是基于 **Transformer 架构**、在海量文本数据上训练的深度学习模型，能够理解和生成人类语言。

```
  输入："请解释什么是AI Agent"
        │
        ▼
┌──────────────────────────────────────────┐
│            Token 化（分词）                │
│   ["请", "解释", "什么", "是", "AI",      │
│    "Agent", "?"]                          │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│           Transformer 推理                │
│                                          │
│   ┌──────┐   ┌──────┐   ┌──────┐        │
│   │Attention│──►│  FFN  │──►│  Norm │   │
│   └──────┘   └──────┘   └──────┘        │
│        │          │          │           │
│    （多层堆叠，数十到数百层）               │
└────────────────┬─────────────────────────┘
                 ▼
┌──────────────────────────────────────────┐
│           输出概率分布                      │
│   "AI" → 0.85                             │
│   "智能体" → 0.72                          │
│   "人工" → 0.31                            │
│   ...                                     │
└──────────────────────────────────────────┘
                 │
                 ▼
  输出："AI Agent 是一种能够自主..."

  （自回归生成：每次预测下一个 Token）
```

### 核心概念

**Token（词元）**
- 模型处理的最小单位，不是单词也不是字
- 1 个英文单词 ≈ 1-2 tokens，1 个中文字 ≈ 1-2 tokens
- 例："AI Agent 是什么" ≈ 6-8 tokens

**Context Window（上下文窗口）**
- 模型一次能"看到"的最大 Token 数量
- 2024 年主流：128K-200K tokens
- 2026 年主流：**1M-2M tokens**（Claude、Gemini 等已支持超长上下文）

**Temperature（温度）**
- 控制输出的随机性/创造性
- 0.0 = 确定性输出（适合代码/数学）
- 0.7-0.9 = 创造性输出（适合写作/创意）
- 1.0+ = 高度随机（探索性）

### 训练阶段

```
    预训练（Pre-training）                 有监督微调（SFT）              强化学习（RLHF/DPO）
    ┌─────────────────┐              ┌────────────────┐             ┌─────────────────┐
    │ 海量无标注数据      │              │ 高质量问答对      │             │ 人类偏好对齐      │
    │ 互联网文本/代码/... │  ──────►   │ 指令数据         │  ───────►  │ 基于反馈优化      │
    │ 成本：千万级 $     │              │ 成本：万级 $      │             │ 成本：十万级 $     │
    │ 基座模型（Base）   │              │ 指令模型（Instruct）│            │ 对齐模型（Chat）   │
    └─────────────────┘              └────────────────┘             └─────────────────┘
          │                                │                                │
    原始 LLM（通才）                   能理解指令但可能偏离             安全、有用、诚实
    （如：不安全的回答）                 （如：偶尔幻觉）                 （如：Claude/GPT）
```

### 推理模型 vs 普通模型 ⭐

2025-2026 年最重要的模型分野：

```python
# 普通模型（一次性输出答案）
def standard_llm(prompt):
    return llm.generate(prompt)
    # 输出：答案是 42。

# 推理模型（内部先思考再回答）
def reasoning_llm(prompt):
    thinking = llm.generate("让我们一步一步思考...")
    # 内部推理过程（用户不可见）：
    # "1. 已知... 2. 计算... 3. 验证..."
    answer = llm.generate(f"基于推理：{thinking}\n最终答案：")
    return answer
    # 输出：经过逐步推理，答案是 42。
```

| 对比 | 普通模型 | 推理模型 |
|:----|:---------|:---------|
| **代表** | GPT-4o、Claude 3.5 Sonnet | OpenAI o3、DeepSeek-R1、Claude 4 Opus |
| **数学推理** | 一般 | 优秀 |
| **代码生成** | 好 | 优秀 |
| **速度** | 快（秒级） | 较慢（10秒-几分钟） |
| **Token 消耗** | 较少 | 多（推理过程消耗额外 Token） |
| **适用场景** | 日常对话、翻译、写作 | 数学、编程竞赛、科学推理 |
| **成本** | 较低 | 较高 |

---

## 二、主流模型对比（2026 年 5 月）

### 闭源商业模型

| 模型 | 公司 | 最新版本 | 上下文 | 推理能力 | 价格（$/M tokens 输入） | 特点 |
|:----|:----|:--------:|:------:|:--------:|:---------------------:|:-----|
| **Claude 4 Opus** | Anthropic | 2026-05 | 200K | ⭐⭐⭐⭐⭐ | $15 | 推理/编码顶级、安全性最佳 |
| **Claude 4 Sonnet** | Anthropic | 2026-05 | 200K | ⭐⭐⭐⭐ | $3 | 性价比之选，速度与质量平衡 |
| **GPT-5** | OpenAI | 2026-03 | 256K | ⭐⭐⭐⭐⭐ | $10 | 推理/多模态能力强 |
| **Gemini 2.5 Pro** | Google | 2026-02 | 2M | ⭐⭐⭐⭐ | $1.25-2.5 | 超长上下文、多模态 |
| **DeepSeek-R2** | DeepSeek | 2026-01 | 128K | ⭐⭐⭐⭐⭐ | $0.5 | 推理顶级、极致性价比 |
| **Qwen 4** | 阿里 | 2026-04 | 128K | ⭐⭐⭐⭐ | $0.8 | 中文能力强、开源可选 |

### 开源模型

| 模型 | 参数规模 | 许可 | 特点 |
|:----|:--------:|:----|:-----|
| **Llama 4** | 8B-405B | 开源（需申请） | Meta 出品，生态最丰富 |
| **Qwen 4** | 0.5B-110B | Apache 2.0 | 中文最强开源，量化友好 |
| **Mistral Large 3** | 123B | Apache 2.0 | 欧洲最佳，多语言 |
| **DeepSeek-R2** | 685B (MoE) | MIT | 推理能力接近最强闭源 |
| **Phi-4** | 14B | MIT | 微软出品，小参数高表现 |
| **Gemma 3** | 2B-27B | 开源 | Google 出品，移动端部署 |

### 模型选择决策树

```
你的需求是什么？
    │
    ├── 需要顶级推理/编码能力？
    │   ├── 预算充足 → Claude 4 Opus / GPT-5
    │   └── 预算有限 → DeepSeek-R2 / Qwen 4
    │
    ├── 日常对话/内容生成？
    │   ├── 追求性价比 → Claude 4 Sonnet / GPT-5-mini
    │   └── 中文为主 → Qwen 4 / DeepSeek-R2
    │
    ├── 需要超长上下文（>200K）？
    │   └── Gemini 2.5 Pro（2M tokens）
    │
    ├── 需要本地部署？
    │   ├── 有 GPU → Qwen 4-72B / Llama 4-70B
    │   └── 无 GPU → Qwen 4-7B / Phi-4 / Gemma 3
    │
    └── 构建 Agent 系统？
        ├── 主推理模型 → Claude 4 / GPT-5
        └── 子任务模型 → Claude 4 Sonnet / Qwen 4（低成本）
```

---

## 三、关键能力维度

### 推理能力（Reasoning）

衡量模型解决复杂逻辑、数学、编程问题的能力：

```text
2026 年推理能力排名（基于公开 Benchmark）：
1. Claude 4 Opus / GPT-5 / DeepSeek-R2（并列顶级）
2. Claude 4 Sonnet / Gemini 2.5 Pro
3. Qwen 4-110B / Llama 4-405B
4. Mistral Large 3 / Qwen 4-72B
```

**Agent 开发中的推理需求**：
- 工具选择推理（选哪个工具、传什么参数）
- 多步规划（先查数据库还是先调 API）
- 错误恢复（工具调用失败后如何补救）

### 函数调用 / Tool Use ⭐

对 Agent 开发来说，这比纯推理能力更重要：

| 模型 | 函数调用质量 | 并行调用 | 工具选择准确率 |
|:----|:-----------:|:--------:|:-------------:|
| Claude 4 Opus | ⭐⭐⭐⭐⭐ | ✅ 支持 | ~98% |
| GPT-5 | ⭐⭐⭐⭐⭐ | ✅ 支持 | ~97% |
| Claude 4 Sonnet | ⭐⭐⭐⭐ | ✅ 支持 | ~95% |
| DeepSeek-R2 | ⭐⭐⭐⭐ | ✅ 支持 | ~93% |
| Qwen 4 | ⭐⭐⭐⭐ | ✅ 支持 | ~92% |
| Gemini 2.5 Pro | ⭐⭐⭐⭐ | ✅ 支持 | ~92% |

### 多模态能力

```text
2026 年主流模型均已支持：
├── 文字理解与生成（所有模型 ✅）
├── 图片理解（所有模型 ✅）
├── 代码执行（Claude / GPT / Gemini ✅）
├── 音频理解（GPT-5 / Gemini ✅）
└── 视频理解（GPT-5 / Gemini ✅）
```

### 成本与速度

```
                GPT-5 ($10)
                  高成本
                   │
      DeepSeek-R2  │  Claude 4 Opus
      ($0.5)       │  ($15)
      ─────────────┼────────────── 高质量
                   │
      Qwen 4       │  Claude 4 Sonnet
      ($0.8)       │  ($3)
      Gemini 2.5   │
      ($1.25)      │
                  低速度（推理模型）
```

---

## 四、本地部署与量化

### 为什么需要本地部署

| 场景 | 说明 |
|:----|:-----|
| **数据隐私** | 敏感数据不能出内网 |
| **离线环境** | 内网/专网无互联网访问 |
| **成本控制** | 高频调用时自部署更便宜 |
| **低延迟** | 本地推理延迟稳定，无网络波动 |
| **定制化** | 可以微调或做模型定制 |

### 部署工具

| 工具 | 说明 | 支持硬件 |
|:----|:-----|:---------|
| **Ollama** | ⭐ 一键部署，体验最佳 | CPU + NVIDIA/AMD GPU |
| **vLLM** | 高吞吐推理，生产首选 | NVIDIA GPU |
| **llama.cpp** | CPU 推理优化，单机首选 | CPU + GPU |
| **TensorRT-LLM** | NVIDIA 官方优化 | NVIDIA GPU（最高性能） |
| **LM Studio** | 可视化操作，新手友好 | CPU + GPU |

### 量化级别

| 量化 | 精度 | 模型大小（7B为例） | 质量损失 |
|:----:|:----:|:-----------------:|:--------:|
| FP16 | 16-bit | ~14GB | 无损 |
| INT8 | 8-bit | ~7GB | 几乎无 |
| **INT4** | 4-bit | ~4GB | 轻微（推荐） |
| INT3 | 3-bit | ~3GB | 明显 |
| INT2 | 2-bit | ~2GB | 严重 |

```bash
# Ollama 一键部署示例
ollama pull qwen4:7b          # 下载 Qwen 4 7B
ollama pull deepseek-r2:7b    # 下载 DeepSeek-R2 7B
ollama pull llama4:8b         # 下载 Llama 4 8B

# 运行
ollama run qwen4:7b

# API 调用（与 OpenAI 兼容）
curl http://localhost:11434/v1/chat/completions \
  -d '{
    "model": "qwen4:7b",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### Spring AI 连接本地模型

```java
// Spring AI + Ollama（本地模型）
@Bean
public ChatClient localModelChatClient() {
    return ChatClient.builder(
        OllamaChatModel.builder()
            .baseUrl("http://localhost:11434")
            .model("qwen4:7b")
            .build()
    ).build();
}

// 也支持 OpenAI 兼容 API
@Bean
public ChatClient vllmChatClient() {
    return ChatClient.builder(
        OpenAiChatModel.builder()
            .baseUrl("http://localhost:8000/v1")  // vLLM 服务
            .apiKey("not-needed")
            .model("Qwen4-72B")
            .build()
    ).build();
}
```

---

## 五、模型路由与混合架构 ⭐

### 为什么需要路由

单一模型无法在所有维度做到最好。生产系统中通常使用**多模型路由**：

```
                   用户请求
                      │
                      ▼
               ┌──────────────┐
               │  Router 模型   │—— 轻量模型（如 Qwen 4-7B）
               │  (分类路由)    │    判断请求类型和复杂度
               └──────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ 简单问答  │ │ 复杂推理  │ │ 代码生成  │
  │ Qwen 4-7B│ │ Claude 4 │ │ DeepSeek │
  │ (快/便宜) │ │ (强/贵)  │ │ -R2      │
  └──────────┘ └──────────┘ └──────────┘
```

### 路由策略

```java
// Spring AI 中的模型路由
@Service
public class ModelRouter {

    private final ChatClient lightModel;    // 轻量模型（本地 Qwen 4-7B）
    private final ChatClient heavyModel;   // 重量模型（Claude 4 Opus）
    private final ChatClient codeModel;    // 代码模型（DeepSeek-R2）

    public String route(String userInput) {
        // 1. 先用轻量模型判断复杂度
        String complexity = lightModel.prompt()
            .user("判断以下问题的复杂度（simple/complex/code）：\n" + userInput)
            .call()
            .content();

        // 2. 路由到合适的模型
        return switch (complexity.trim()) {
            case "simple"  -> lightModel.call(userInput);   // 快、低成本
            case "code"    -> codeModel.call(userInput);     // 代码优化
            case "complex" -> heavyModel.call(userInput);    // 强推理
            default        -> lightModel.call(userInput);
        };
    }
}
```

### 缓存策略

```java
// ⭐ Semantic Caching——语义缓存（相同语义的问题命中缓存）
@Bean
public SemanticCache semanticCache(VectorStore vectorStore) {
    return new SemanticCache(vectorStore, 0.95);  // 相似度阈值
}

// 使用缓存
String cached = semanticCache.get(userInput);
if (cached != null) {
    return cached;  // 直接返回缓存结果，零 Token 消耗
}
// 未命中 → 调用 LLM → 写入缓存
String response = llm.call(userInput);
semanticCache.put(userInput, response);
```

---

## 六、Token 与成本管理

### Token 计价模型

```text
Token 消耗 = 输入 Token + 输出 Token

示例成本计算（使用 Claude 4 Opus，$15/M tokens 输入，$75/M tokens 输出）：

┌──────────────────────────────────────────┐
│ 场景：日常对话，每次 500 输入 + 200 输出     │
│ 成本 = 500/1M × $15 + 200/1M × $75       │
│      = $0.0075 + $0.015 = $0.0225/次     │
│ 每天 1000 次 = $22.5/天                   │
├──────────────────────────────────────────┤
│ 场景：Agent 复杂任务，5000 输入 + 2000 输出  │
│（含工具调用、多步推理）                      │
│ 成本 = 5000/1M × $15 + 2000/1M × $75     │
│      = $0.075 + $0.15 = $0.225/次        │
│ 每天 1000 次 = $225/天                    │
└──────────────────────────────────────────┘
```

### 省钱策略

| 策略 | 节省 | 做法 |
|:----|:----:|:-----|
| **模型路由** | 40-60% | 简单问题走便宜模型 |
| **语义缓存** | 20-40% | 相似问题缓存结果 |
| **Prompt 压缩** | 30-50% | 压缩历史对话，去除冗余 |
| **批量处理** | 10-20% | 合并多个小请求为一个大请求 |
| **本地部署** | 60-80% | 高频场景走本地模型 |

### Token 使用监控

```java
// Spring AI + Micrometer 监控 Token 消耗
@Bean
public ChatClient monitoredChatClient(ChatClient.Builder builder) {
    return builder
        .defaultSystem("你是 AI 助手")
        .build();
}

// 在 Metrics 中查看：
// ai.token.usage.input   — 输入 Token 数
// ai.token.usage.output  — 输出 Token 数
// ai.token.total.cost    — 总成本估算
```

---

## 七、模型选型决策指南（2026）

### 按场景推荐

| 场景 | 第一推荐 | 备选 |
|:----|:--------|:-----|
| **日常对话/客服** | Claude 4 Sonnet | GPT-5-mini、Qwen 4 |
| **复杂代码生成** | Claude 4 Opus | DeepSeek-R2、GPT-5 |
| **中文场景** | Qwen 4-110B | DeepSeek-R2、Claude 4 |
| **长文档分析** | Gemini 2.5 Pro | Claude 4（200K） |
| **Java Agent 开发** | Claude 4 Sonnet | GPT-5、Qwen 4 |
| **数学/科学推理** | DeepSeek-R2 | Claude 4 Opus、GPT-5 |
| **低成本大批量** | Qwen 4-7B（本地） | DeepSeek-R2-7B |
| **多模态（图/音/视频）** | GPT-5 | Gemini 2.5 Pro |

### 给 Java 开发者的推荐

```yaml
# Agent 系统生产配置参考
ai:
  router:                # 路由模型——轻量快速
    model: qwen4:7b
    provider: ollama     # 本地部署

  reasoning:             # 主推理模型——核心 Agent
    model: claude-4-sonnet-20260516
    provider: anthropic
    max-tokens: 8192

  code:                 # 代码生成
    model: deepseek-r2
    provider: deepseek

  embedding:            # 向量化（RAG）
    model: text-embedding-3-small
    provider: openai

  cache:
    type: semantic
    similarity: 0.92
```

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 LLM 基本概念（Token/上下文/温度）→ 了解主流模型
> 2. **实践**：注册 API 调用体验 → 对比不同模型的输出质量
> 3. **深入**：学习模型路由 → 本地部署（Ollama）→ Token 成本优化
> 4. **工程化**：混合模型架构 → 缓存策略 → 监控与评估体系


---

> **📖 学习路线**：[[AIAgent篇/README|AI Agent 学习路线图]]
