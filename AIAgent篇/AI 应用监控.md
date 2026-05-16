# AI 应用监控

## 一、AI 应用监控的特殊性

### 传统监控 vs AI 监控

```
传统应用监控                          AI 应用监控
══════════════════════               ══════════════════════

基础设施                             基础设施（一样需要）
├── CPU / 内存 / 磁盘                 ├── 同左
├── 请求量 / 错误率 / 延迟            ├── 同左
└── 数据库连接 / 缓存命中              └── 同左

应用层                               AI 特有监控维度
├── 接口响应时间                      ├── Token 消耗与成本
├── 错误日志                          ├── LLM 响应延迟（TTFT/TPOT）
├── 调用链追踪                        ├── 回答质量评估
└── 业务指标                          ├── 工具调用分析
                                     ├── 幻觉检测
                                     ├── 记忆使用情况
                                     ├── RAG 检索质量
                                     ├── Prompt 注入检测
                                     ├── Agent 决策路径追踪
                                     └── 成本分摊与预算管理
```

### 为什么要监控 AI 应用

```text
不监控的代价
═══════════════════════════════════════

💰 成本失控
├── 一个未优化的 RAG 查询 = 5000+ Token
├── 一个循环 Agent 可能消耗 50000+ Token
├── 一个月无监控的 AI 应用 → 账单可能超预期 10x
└── 例：10万日活 × 10次对话 × 2000 Token × $3/M = $60/天

📉 质量下降
├── 模型更新后回答风格变了，没人发现
├── 检索质量下降，LLM 开始产生幻觉
├── Agent 决策路径变差（多调了不必要的工具）
└── 用户满意度下降但无感知

🔒 安全隐患
├── Prompt 注入攻击未被发现
├── 敏感数据通过工具泄露
├── 异常调用模式未被检测
└── 安全事件事后无法追溯
```

### 监控架构总览

```
┌──────────────────────────────────────────────────────────────┐
│                   AI 应用监控平台                              │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  采集层                                                    │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │ │
│  │  │Token   │ │性能    │ │质量    │ │安全    │ │业务    │ │ │
│  │  │采集器   │ │采集器   │ │评估器   │ │检测器   │ │采集器   │ │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                 │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │  存储层                                                    │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐            │ │
│  │  │Prometheus  │ │Elasticsearch│ │PostgreSQL  │            │ │
│  │  │(指标)      │ │(日志)      │ │(业务数据)  │            │ │
│  │  └────────────┘ └────────────┘ └────────────┘            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                 │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │  可视化层                                                  │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐            │ │
│  │  │Grafana     │ │Kibana      │ │告警平台    │            │ │
│  │  │(仪表盘)    │ │(日志分析)  │ │(通知)      │            │ │
│  │  └────────────┘ └────────────┘ └────────────┘            │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 二、Token 成本监控 ⭐

### 成本跟踪核心指标

```java
// ⭐ Token 用量采集器
@Component
public class TokenUsageCollector {

    private final MeterRegistry meterRegistry;

    // 自定义指标
    private final Counter tokenInputCounter;
    private final Counter tokenOutputCounter;
    private final Counter costCounter;
    private final DistributionSummary latencySummary;

    // 按模型/用户/功能分类的 Tag
    private static final double CLAUDE_SONNET_INPUT_COST = 3.0 / 1_000_000;   // $3/M
    private static final double CLAUDE_SONNET_OUTPUT_COST = 15.0 / 1_000_000; // $15/M

    public TokenUsageCollector(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        this.tokenInputCounter = Counter.builder("ai.token.input")
            .description("输入 Token 总数")
            .register(meterRegistry);

        this.tokenOutputCounter = Counter.builder("ai.token.output")
            .description("输出 Token 总数")
            .register(meterRegistry);

        this.costCounter = Counter.builder("ai.cost.usd")
            .description("AI 调用成本（美元）")
            .register(meterRegistry);

        this.latencySummary = DistributionSummary.builder("ai.latency")
            .description("LLM 响应延迟（ms）")
            .register(meterRegistry);
    }

    /**
     * 记录完整的 Token 使用情况
     */
    public void recordTokenUsage(TokenUsage usage, String model, String userId, String feature) {
        // 1. Token 计数
        tokenInputCounter.increment(usage.inputTokens());
        tokenOutputCounter.increment(usage.outputTokens());

        // 2. 按模型打标签
        meterRegistry.counter("ai.token.input",
            "model", model, "feature", feature
        ).increment(usage.inputTokens());

        meterRegistry.counter("ai.token.output",
            "model", model, "feature", feature
        ).increment(usage.outputTokens());

        // 3. 成本计算
        double cost = calculateCost(model, usage.inputTokens(), usage.outputTokens());
        costCounter.increment(cost);

        meterRegistry.counter("ai.cost.usd",
            "model", model, "user", userId
        ).increment(cost);

        // 4. 延迟记录
        latencySummary.record(usage.durationMs());
    }

    /**
     * 成本计算（可根据实际价格配置）
     */
    private double calculateCost(String model, long inputTokens, long outputTokens) {
        // Claude 4 Sonnet 定价
        if (model.contains("claude-4-sonnet")) {
            return inputTokens * CLAUDE_SONNET_INPUT_COST
                 + outputTokens * CLAUDE_SONNET_OUTPUT_COST;
        }
        // 本地模型免费
        if (model.contains("ollama") || model.contains("qwen")) {
            return 0;
        }
        // GPT-5 定价
        if (model.contains("gpt-5")) {
            return inputTokens * 10.0 / 1_000_000
                 + outputTokens * 30.0 / 1_000_000;
        }
        return 0;
    }
}
```

### 成本仪表盘

```java
// ⭐ Actuator 成本端点
@RestController
@RequestMapping("/actuator/ai/cost")
public class CostActuator {

    @GetMapping("/summary")
    public CostSummary getCostSummary(
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {

        return costService.getCostSummary(startDate, endDate);
    }

    @GetMapping("/breakdown")
    public List<CostBreakdown> getCostBreakdown(
            @RequestParam(defaultValue = "model") String by) {
        // 按模型/功能/用户/部门 的成本分解
        return costService.getCostBreakdown(by);
    }

    @GetMapping("/budget")
    public BudgetStatus getBudgetStatus() {
        return costService.getBudgetStatus();
    }

    @Data
    public static class CostSummary {
        private double totalCost;           // 总成本
        private double dailyAverageCost;    // 日均成本
        private long totalInputTokens;      // 总输入 Token
        private long totalOutputTokens;     // 总输出 Token
        private Map<String, Double> costByModel;     // 按模型
        private Map<String, Double> costByFeature;    // 按功能
        private Map<String, Double> costByUser;       // 按用户（Top N）
    }
}
```

### 预算告警规则

```yaml
# ⭐ 成本告警规则
ai:
  monitoring:
    cost:
      # 每日预算
      daily-budget: 100.0    # 每日 $100
      weekly-budget: 500.0   # 每周 $500
      monthly-budget: 2000.0 # 每月 $2000

      # 告警阈值
      alerts:
        - name: "daily-budget-80"
          description: "当日预算消耗达 80%"
          threshold: 0.8
          severity: WARNING
          notify: [team-lead]

        - name: "daily-budget-exceeded"
          description: "超过当日预算"
          threshold: 1.0
          severity: CRITICAL
          notify: [team-lead, finance]
          action: "限流降级"

        - name: "token-spike"
          description: "Token 消耗激增（环比>200%）"
          condition: "token_usage_1h / token_usage_prev_1h > 2.0"
          severity: WARNING
          notify: [team-lead]

        - name: "unexpected-model"
          description: "使用了未预期的模型"
          condition: "model not in ['claude-4-sonnet', 'qwen4:7b']"
          severity: CRITICAL
          notify: [engineering]
```

---

## 三、质量监控 ⭐

### 回答质量自动评估

```java
// ⭐ LLM-as-a-Judge——自动质量评估
@Service
public class QualityEvaluator {

    private final ChatClient judgeLlm;  // 用于评估的 LLM（通常更强）

    /**
     * 评估回答质量
     */
    public QualityScore evaluate(String question, String answer, String context) {
        return judgeLlm.prompt()
            .user(u -> u.text("""
                评估以下 AI 回答的质量。

                问题：{question}
                回答：{answer}
                参考上下文：{context}

                评估维度（1-5分）：

                1. 忠实度（faithfulness）：
                   回答是否忠实于参考上下文？
                   有没有无根据的推断或幻觉？
                   5=完全基于上下文，1=完全虚构

                2. 相关性（relevance）：
                   回答是否直接针对用户问题？
                   5=完全相关，1=答非所问

                3. 完整性（completeness）：
                   是否覆盖了问题的所有方面？
                   5=全面覆盖，1=遗漏关键点

                4. 清晰度（clarity）：
                   回答是否结构清晰、易于理解？
                   5=非常清晰，1=混乱难懂

                5. 安全性（safety）：
                   回答是否安全、合规？
                   5=完全安全，1=包含有害内容

                只返回 JSON 格式评估结果。
                """)
                .param("question", question)
                .param("answer", answer)
                .param("context", context != null ? context : "无上下文"))
            .call()
            .entity(QualityScore.class);
    }

    public record QualityScore(
        int faithfulness,
        int relevance,
        int completeness,
        int clarity,
        int safety,
        double averageScore,
        boolean passQuality
    ) {
        public QualityScore {
            averageScore = (faithfulness + relevance + completeness + clarity + safety) / 5.0;
            passQuality = faithfulness >= 4 && averageScore >= 4.0;
        }
    }
}
```

### 幻觉检测

```java
// ⭐ 幻觉检测——发现无根据的回答
@Service
public class HallucinationDetector {

    private final ChatClient detectorLlm;

    @Tool(description = "检测 AI 回答中是否有幻觉（无根据的陈述）")
    public HallucinationReport detectHallucination(
            @ToolParam(description = "AI 生成的回答") String answer,
            @ToolParam(description = "检索到的参考文档") List<Document> documents) {

        return detectorLlm.prompt()
            .user(u -> u.text("""
                分析以下 AI 回答中是否有幻觉。

                回答：{answer}

                参考文档：
                {documents}

                请列出回答中所有：
                1. 有文档支持的陈述（标记 ✅）
                2. 没有文档支持的陈述（标记 ❌ 幻觉）
                3. 与文档矛盾的陈述（标记 ⚠️ 矛盾）

                对每个幻觉陈述，给出严重程度：
                - HIGH: 关键事实错误
                - MEDIUM: 不太准确的推断
                - LOW: 轻微不准确

                只返回 JSON。
                """)
                .param("answer", answer)
                .param("documents", formatDocuments(documents)))
            .call()
            .entity(HallucinationReport.class);
    }

    public record HallucinationReport(
        List<Statement> supportedStatements,
        List<Statement> hallucinatedStatements,
        List<Statement> contradictedStatements,
        double hallucinationRate,   // 幻觉率
        boolean acceptable           // 是否可接受（幻觉率<5%）
    ) {}

    public record Statement(
        String content,
        String severity,    // HIGH / MEDIUM / LOW
        String explanation
    ) {}
}
```

### 用户反馈集成

```java
// ⭐ 用户反馈采集
@Service
public class UserFeedbackCollector {

    private final FeedbackRepository feedbackRepository;

    /**
     * 收集用户显式反馈（赞/踩）
     */
    public void collectFeedback(String sessionId, Feedback feedback) {
        feedbackRepository.save(feedback);

        // 负面反馈立即告警
        if (feedback.rating() < 3) {
            alertService.sendAlert(String.format(
                "用户负面反馈 [%s]: %s (评分: %d/5)",
                feedback.feature(), feedback.comment(), feedback.rating()
            ));
        }

        // 更新质量指标
        updateQualityMetrics(feedback);
    }

    /**
     * 隐式反馈（用户行为）
     * - 是否复制了回答 → 满意
     * - 是否立即追问 → 可能需要澄清
     * - 是否离开页面 → 不满意
     */
    public void collectImplicitFeedback(String sessionId, UserBehavior behavior) {
        double satisfaction = calculateImplicitSatisfaction(behavior);

        meterRegistry.gauge("ai.user.satisfaction.implicit",
            Tags.of("feature", behavior.feature()),
            satisfaction);
    }

    public record Feedback(
        String sessionId,
        String feature,
        int rating,        // 1-5
        String comment,
        String category,   // 准确/相关/完整/速度/其他
        Instant timestamp
    ) {}
}
```

---

## 四、性能监控

### 核心性能指标

```java
// ⭐ 性能监控采集
@Component
public class PerformanceMonitor {

    private final MeterRegistry meterRegistry;

    // ════════════════════════════════════════
    // LLM 性能指标
    // ════════════════════════════════════════

    /**
     * 记录 LLM 调用性能
     */
    public void recordLlmPerformance(LlmMetrics metrics) {
        // 首 Token 延迟（TTFT - Time to First Token）
        meterRegistry.timer("ai.llm.ttft",
            "model", metrics.model()
        ).record(metrics.ttft());

        // 每 Token 生成时间（TPOT - Time Per Output Token）
        meterRegistry.timer("ai.llm.tpot",
            "model", metrics.model()
        ).record(metrics.tpot());

        // 端到端延迟
        meterRegistry.timer("ai.llm.latency",
            "model", metrics.model(),
            "feature", metrics.feature()
        ).record(metrics.endToEndLatency());

        // 吞吐量
        meterRegistry.counter("ai.llm.tokens_per_second",
            "model", metrics.model()
        ).increment(metrics.tokensPerSecond());
    }

    // ════════════════════════════════════════
    // RAG 性能指标
    // ════════════════════════════════════════

    /**
     * 记录 RAG 检索性能
     */
    public void recordRagPerformance(RagMetrics metrics) {
        // 检索延迟
        meterRegistry.timer("ai.rag.search_latency",
            "strategy", metrics.searchStrategy()
        ).record(metrics.searchDuration());

        // 检索结果数
        meterRegistry.gauge("ai.rag.result_count",
            Tags.of("strategy", metrics.searchStrategy()),
            metrics.resultCount());

        // Rerank 延迟
        meterRegistry.timer("ai.rag.rerank_latency").record(metrics.rerankDuration());

        // 检索质量（分数分布）
        meterRegistry.distributionSummary("ai.rag.similarity_scores")
            .record(metrics.averageScore());
    }

    public record LlmMetrics(
        String model,
        String feature,
        Duration ttft,              // 首 Token 延迟
        Duration tpot,              // 每 Token 生成时间
        Duration endToEndLatency,   // 端到端延迟
        double tokensPerSecond     // 每秒 Token 数
    ) {}

    public record RagMetrics(
        String searchStrategy,      // vector/keyword/hybrid
        Duration searchDuration,
        Duration rerankDuration,
        int resultCount,
        double averageScore
    ) {}
}
```

### 性能基准

```text
AI 应用性能目标（P99）
═══════════════════════════════════════

简单对话（直答）
├── TTFT: <300ms
├── 总延迟: <1s
├── Token 产出: >50 tokens/s
└── 示例：问候、简单问答

RAG 查询
├── 检索延迟: <200ms
├── TTFT: <1s
├── 总延迟: <3s
└── 示例：知识库问答

Agent 多步操作
├── 每步推理: <500ms
├── 工具调用: <1s
├── 总延迟: <10s（3-5步）
└── 示例：查询订单→取消→退款

流式输出
├── TTFT: <500ms
├── 帧间隔: <100ms
├── 总延迟: 取决于内容长度
└── 示例：文章生成、代码生成
```

### Actuator 监控端点

```yaml
# ⭐ Actuator AI 监控配置
management:
  endpoints:
    web:
      exposure:
        include: ai, health, metrics, prometheus

  endpoint:
    ai:
      enabled: true

  metrics:
    export:
      prometheus:
        enabled: true

spring:
  ai:
    actuator:
      # 启用 AI 监控端点
      info:
        enabled: true
      metrics:
        enabled: true
      tracing:
        enabled: true
```

```bash
# 查看 AI 运行信息
GET /actuator/ai/info
# {
#   "models": ["claude-4-sonnet", "qwen4:7b"],
#   "tools": ["queryOrder", "searchKnowledge", ...],
#   "features": ["chat", "rag", "agent"],
#   "status": "UP"
# }

# 查看 AI 指标
GET /actuator/ai/metrics
# {
#   "ai.token.input": 1523456789,
#   "ai.token.output": 345678901,
#   "ai.cost.usd": 4567.89,
#   "ai.llm.ttft": "...",
#   "ai.quality.faithfulness": 4.5,
#   ...
# }

# Prometheus 格式
GET /actuator/prometheus
# ai_token_input_total{model="claude-4-sonnet",feature="rag"} 1234567
# ai_cost_usd_total{model="claude-4-sonnet"} 4567.89
```

### 自定义监控 Grafana 面板

```java
// ⭐ 关键指标注册
@Configuration
public class AiMetricsConfiguration {

    @Bean
    public MeterBinder aiMetricsBinder() {
        return registry -> {
            // 1. Token 消耗
            Gauge.builder("ai.daily.token.input", tokenService,
                    TokenService::getDailyInputTokens)
                .description("当日输入 Token 总量")
                .register(registry);

            Gauge.builder("ai.daily.token.output", tokenService,
                    TokenService::getDailyOutputTokens)
                .description("当日输出 Token 总量")
                .register(registry);

            // 2. 成本
            Gauge.builder("ai.daily.cost", costService,
                    CostService::getDailyCost)
                .description("当日 AI 成本（美元）")
                .register(registry);

            // 3. 质量
            Gauge.builder("ai.quality.faithfulness", qualityService,
                    QualityService::getAverageFaithfulness)
                .description("平均忠实度评分")
                .register(registry);

            Gauge.builder("ai.quality.hallucination_rate", qualityService,
                    QualityService::getHallucinationRate)
                .description("幻觉率")
                .register(registry);

            // 4. 性能
            Gauge.builder("ai.performance.p50_latency", performanceService,
                    () -> performanceService.getLatencyPercentile(50))
                .description("P50 延迟（ms）")
                .register(registry);

            Gauge.builder("ai.performance.p99_latency", performanceService,
                    () -> performanceService.getLatencyPercentile(99))
                .description("P99 延迟（ms）")
                .register(registry);

            // 5. 用户满意度
            Gauge.builder("ai.user.satisfaction", feedbackService,
                    FeedbackService::getAverageRating)
                .description("用户满意度评分（1-5）")
                .register(registry);
        };
    }
}
```

---

## 五、Agent 行为监控

### Agent 决策追踪

```java
// ⭐ Agent 调用链追踪
@Component
public class AgentTraceInterceptor implements ChatClientAdvisor {

    private final Tracer tracer;

    @Override
    public AdvisedResponse aroundCall(AdvisedRequest request,
                                       CallAroundAdvisorChain chain) {

        // 创建追踪 Span
        Span span = tracer.nextSpan()
            .name("agent.call")
            .tag("user.message", request.userText())
            .start();

        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            AdvisedResponse response = chain.nextAroundCall(request);

            // 记录工具调用
            if (response.getToolCalls() != null) {
                for (ToolCall tc : response.getToolCalls()) {
                    span.tag("tool." + tc.getName(),
                        "args=" + maskSensitive(tc.getArguments()) +
                        ", result=" + truncate(tc.getResult()));
                }
            }

            // 记录 Token 使用
            if (response.getTokenUsage() != null) {
                span.tag("tokens.input",
                    String.valueOf(response.getTokenUsage().inputTokens()));
                span.tag("tokens.output",
                    String.valueOf(response.getTokenUsage().outputTokens()));
            }

            return response;

        } catch (Exception e) {
            span.tag("error", e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}

// ⭐ Agent 行为分析
@Service
public class AgentBehaviorAnalyzer {

    /**
     * 分析 Agent 决策模式
     */
    public AgentBehaviorReport analyzeBehavior(String sessionId) {
        List<AgentTrace> traces = traceRepository.findBySessionId(sessionId);

        return new AgentBehaviorReport(
            // 工具调用统计
            analyzeToolUsage(traces),

            // 决策路径分析
            analyzeDecisionPath(traces),

            // Token 效率
            calculateTokenEfficiency(traces),

            // 异常行为检测
            detectAnomalies(traces)
        );
    }

    /**
     * 检测异常 Agent 行为
     */
    private List<Anomaly> detectAnomalies(List<AgentTrace> traces) {
        List<Anomaly> anomalies = new ArrayList<>();

        // 工具调用循环检测
        if (hasInfiniteLoop(traces)) {
            anomalies.add(new Anomaly("INFINITE_LOOP",
                "Agent 陷入工具调用循环", Severity.HIGH));
        }

        // 不必要的工具调用检测
        if (hasUnnecessaryCalls(traces)) {
            anomalies.add(new Anomaly("UNNECESSARY_CALLS",
                "Agent 调用了不必要的工具", Severity.MEDIUM));
        }

        // Token 浪费检测
        double efficiency = calculateTokenEfficiency(traces);
        if (efficiency < 0.3) {
            anomalies.add(new Anomaly("TOKEN_WASTE",
                "Token 效率低（<30%），大量 Token 用于非最终回答",
                Severity.MEDIUM));
        }

        return anomalies;
    }
}
```

### 关键行为指标

```text
Agent 行为监控指标
═══════════════════════════════════════

效率指标
├── 工具调用次数/会话（正常 2-8 次）
├── Agent 决策步数/任务（正常 3-10 步）
├── Token 效率（有用 Token / 总 Token，目标 >40%）
└── 任务完成率（目标 >90%）

质量指标
├── 工具调用成功率（目标 >95%）
├── 工具参数错误率（目标 <5%）
├── 首次回答准确率（目标 >80%）
└── 用户追问率（追问多说明首次回答差）

异常检测
├── 工具循环次数（>10 次同一工具 → 告警）
├── 空工具调用（LLM 调了工具但没使用结果）
├── Token 突增（单次调用 >100K Token → 告警）
└── 超时工具（单步 >30s → 告警）
```

---

## 六、灰度发布与实验

### 灰度发布策略

```java
// ⭐ AI 功能灰度发布
@Component
public class AiFeatureGating {

    private final FeatureToggleConfig config;

    /**
     * 判断用户是否在灰度组
     */
    public boolean isEnabled(String feature, String userId) {
        FeatureToggle toggle = config.getFeatures().get(feature);
        if (toggle == null) return false;

        return switch (toggle.strategy()) {
            case ALL -> true;
            case NONE -> false;
            case PERCENTAGE -> hashUserId(userId) < toggle.percentage();
            case WHITELIST -> toggle.whitelist().contains(userId);
            case BETA ->
                toggle.betaUsers().contains(userId)
                || hashUserId(userId) < toggle.percentage();
        };
    }

    /**
     * 路由到不同版本的 Agent
     */
    public ChatClient routeAgent(String feature, String userId) {
        if ("new-agent-v2".equals(feature) && isEnabled(feature, userId)) {
            return newAgentV2Client;  // 新版 Agent 逻辑
        }
        return currentAgentClient;    // 当前稳定版
    }

    @Data
    @ConfigurationProperties(prefix = "ai.feature-toggles")
    @Configuration
    public static class FeatureToggleConfig {
        private Map<String, FeatureToggle> features = new HashMap<>();
    }

    public record FeatureToggle(
        Strategy strategy,
        int percentage,          // 0-100
        List<String> whitelist,
        List<String> betaUsers
    ) {
        enum Strategy { ALL, NONE, PERCENTAGE, WHITELIST, BETA }
    }
}
```

```yaml
# ⭐ 功能开关配置
ai:
  feature-toggles:
    features:
      # 新 Agent 版本灰度
      new-agent-v2:
        strategy: PERCENTAGE
        percentage: 10          # 10% 用户
        whitelist:
          - "internal-test-1"
          - "qa-team"

      # Agentic RAG 实验
      agentic-rag:
        strategy: BETA
        percentage: 5
        beta-users:
          - "beta-user-1"
          - "beta-user-2"

      # 新模型测试
      gpt-5-chat:
        strategy: WHITELIST
        whitelist:
          - "dev-team-1"
```

### A/B 实验

```java
// ⭐ A/B 实验框架
@Service
public class AiExperimentService {

    /**
     * 运行 A/B 实验
     */
    public ExperimentResult runExperiment(
            String experimentName,
            String controlFeature,
            String variantFeature,
            Duration duration) {

        // 1. 获取实验期间的数据
        List<ExperimentData> controlData = collectData(controlFeature, duration);
        List<ExperimentData> variantData = collectData(variantFeature, duration);

        // 2. 计算指标
        return new ExperimentResult(
            experimentName,
            calculateMetrics(controlData, "对照组"),
            calculateMetrics(variantData, "实验组"),
            calculateSignificance(controlData, variantData)
        );
    }

    private Metrics calculateMetrics(List<ExperimentData> data, String label) {
        return new Metrics(
            label,
            average(data, ExperimentData::faithfulness),
            average(data, ExperimentData::userSatisfaction),
            average(data, ExperimentData::completionRate),
            average(data, ExperimentData::tokenEfficiency),
            average(data, ExperimentData::latencyMs)
        );
    }

    public record Metrics(
        String label,
        double faithfulness,
        double userSatisfaction,
        double completionRate,
        double tokenEfficiency,
        double latencyMs
    ) {}

    public record ExperimentResult(
        String experimentName,
        Metrics control,
        Metrics variant,
        boolean statisticallySignificant
    ) {}
}
```

---

## 七、监控实施路线图

```
AI 监控实施路线图
═══════════════════════════════════════

第一阶段（第1周）——基础监控
├── Spring Actuator AI 端点启用
├── Token 消耗采集（按模型/功能）
├── 基本延迟监控
└── 日志采集（请求/响应/错误）

第二阶段（第2周）——成本管理
├── 成本计算与分解
├── 每日/每周/每月预算
├── 成本告警规则
└── Grafana 成本仪表盘

第三阶段（第3周）——质量监控
├── LLM-as-a-Judge 评估
├── 幻觉检测
├── 用户反馈采集
└── 质量趋势分析

第四阶段（第4周）——Agent 行为
├── Agent 决策路径追踪
├── 工具调用分析
├── 异常行为检测
└── A/B 实验框架

第五阶段（持续）——优化
├── 基于监控数据的 Prompt 优化
├── RAG 检索策略调优
├── 成本优化（缓存/模型选择）
└── 告警阈值精细化
```

### 监控 Checklist

```text
□ 1. 成本监控
   □ Token 消耗按模型/功能/用户统计
   □ 成本计算与预算管理
   □ 成本异常告警
   □ 每日成本报告

□ 2. 质量监控
   □ 回答忠诚度评估
   □ 幻觉率检测
   □ 用户满意度采集（显式 + 隐式）
   □ 质量趋势告警（持续下降时通知）

□ 3. 性能监控
   □ TTFT / TPOT / 端到端延迟
   □ RAG 检索延迟与质量
   □ P50/P95/P99 延迟
   □ 流式帧间隔

□ 4. Agent 行为监控
   □ 工具调用次数和成功率
   □ Agent 决策步数
   □ 循环检测
   □ Token 效率

□ 5. 安全监控
   □ Prompt 注入检测告警
   □ 敏感工具调用审计
   □ 异常使用模式检测
   □ 数据泄露检测

□ 6. 实验与发布
   □ 灰度发布框架
   □ A/B 实验能力
   □ 版本对比分析
   □ 回滚机制
```

> [!tip] **从轻开始，逐步完善**
> 不要试图一开始就搭建完整的监控体系。先从 **Token 成本** 和 **Actuator 基础指标** 入手，这两项投入最小、收益最大。当你在成本仪表盘上看到具体数据后，自然就知道下一步该优化什么——质量、性能还是 Agent 行为。监控的价值在于**驱动决策**，而不是收集数据本身。
