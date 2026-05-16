# Agentic RAG 实战

## 一、从标准 RAG 到 Agentic RAG

### 标准 RAG 的局限

```
标准 RAG 流程（固定流水线）
═══════════════════════════════

用户提问 → 向量检索 → Prompt 拼接 → LLM 生成 → 回答
  │          │           │           │
  └─ 问题    └─ 固定 TopK └─ 固定模板  └─ 一次生成
     单一     总是检索       总是包含   不能追问
     无分析    可能无关      可能干扰   不能反思

问题：
1. ❌ 检索是必须的吗？——简单问题不需要检索
2. ❌ 一次检索够吗？——复杂问题需要多步检索
3. ❌ TopK 固定合适吗？——不同问题需要不同数量
4. ❌ 检索质量谁保证？——低质量检索会误导 LLM
5. ❌ 无法处理反问——Agent 不能追问澄清
```

### Agentic RAG 的进化

```
Agentic RAG（Agent 自主决策）
═══════════════════════════════

用户提问 → Agent 分析 → 决定是否检索 → 执行检索
                              │              │
                      ┌───────┴───────┐     │
                      │   需要检索？    │ ◄───┘
                      │   是 / 否      │
                      └───────┬───────┘
                         是 / 否
                        │     │
                        ▼     ▼
                  执行检索   直接回答
                        │
                        ▼
                  评估结果质量
                        │
              ┌─────────┴─────────┐
              │    质量合格？       │
              └─────────┬─────────┘
                   是 / 否
                  │       │
                  ▼       ▼
             生成回答   重新检索/追问
                         │
                         ▼
                    反思和改进

优势：
1. ✅ 按需检索——简单问题不检索，节省 Token
2. ✅ 多步检索——复杂问题步步深入
3. ✅ 自适应——根据检索质量调整策略
4. ✅ 可追问——信息不足时反问用户
5. ✅ 可反思——对生成的回答自我改进
```

### 架构对比

| 维度 | 标准 RAG | Agentic RAG |
|:----|:--------|:-----------|
| 检索策略 | 固定，每次都检索 | 按需，Agent 自主决定 |
| 检索次数 | 1 次 | 1~N 次，可多步 |
| 查询处理 | 直接用原问题 | 重写/分解/扩展 |
| 上下文处理 | 固定模板拼接 | 动态筛选和重排 |
| 回答生成 | 一次生成 | 生成 → 评估 → 改进 |
| 错误处理 | 无 | 自动重试和修正 |
| 追问能力 | 无 | 可向用户追问澄清 |
| Token 效率 | 低（总是检索） | 高（按需检索） |
| 复杂度 | 低 | 中高 |
| 适用场景 | 简单问答 | 复杂知识密集型任务 |

---

## 二、系统架构设计

### 整体架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Agentic RAG 系统架构                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    用户界面                                │ │
│  │              REST API / WebSocket / SSE                    │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                    Orchestrator Layer                     │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │ Query       │  │ Retrieval   │  │ Response    │      │ │
│  │  │ Analyzer    │─▶│ Planner     │─▶│ Generator   │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                   Retrieval Layer                         │ │
│  │                                                           │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │ │
│  │  │ Vector   │ │ Keyword  │ │ Hybrid   │ │ Re-      │    │ │
│  │  │ Search   │ │ Search   │ │ Search   │ │ ranking  │    │ │
│  │  │ (PGVec)  │ │ (ES)     │ │ (Fusion) │ │ (Rerank) │    │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                    Data Layer                              │ │
│  │                                                           │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │ │
│  │  │ PGVector │ │ Redis    │ │ MinIO   │ │ Elastic  │    │ │
│  │  │ (向量)    │ │ (缓存)   │ │ (文档)   │ │ (索引)    │    │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 核心组件职责

```java
// ⭐ 编排层——Agentic RAG 的核心
@Service
public class AgenticRagOrchestrator {

    private final QueryAnalyzer queryAnalyzer;
    private final RetrievalPlanner retrievalPlanner;
    private final ResponseGenerator responseGenerator;
    private final QualityEvaluator qualityEvaluator;

    public RagResponse process(String userMessage) {
        // 1. 分析用户问题
        QueryAnalysis analysis = queryAnalyzer.analyze(userMessage);

        // 2. 检索规划（Agent 自主决定）
        RetrievalPlan plan = retrievalPlanner.plan(analysis);

        // 3. 多步检索执行
        List<Document> documents = executeRetrieval(plan);

        // 4. 生成回答 + 反思
        RagResponse response = responseGenerator.generate(userMessage, documents);

        // 5. 质量评估（可能需要多轮）
        while (!qualityEvaluator.isSatisfactory(response)) {
            // 检索更多信息
            List<Document> moreDocs = retrievalPlanner.supplement(plan, response);
            documents.addAll(moreDocs);
            // 重新生成
            response = responseGenerator.generate(userMessage, documents);
        }

        return response;
    }
}
```

---

## 三、查询分析器

### 问题分类与策略

```java
// ⭐ 查询分析——Agent 判断问题类型并决定检索策略
@Service
public class QueryAnalyzer {

    private final ChatClient chatClient;

    /**
     * 分析用户问题，返回结构化的查询分析结果
     */
    public QueryAnalysis analyze(String question) {
        return chatClient.prompt()
            .user(u -> u.text("""
                分析以下问题，返回 JSON 格式的分析结果：

                问题：{question}

                分析维度：
                1. question_type: 问题类型
                   - SIMPLE_QA: 简单事实性问题（直接回答）
                   - COMPLEX_REASONING: 复杂推理（需多步推理）
                   - MULTI_HOP: 多跳查询（需多次检索）
                   - COMPARISON: 比较类问题（需对比多个来源）
                   - CLARIFICATION: 模糊查询（需追问澄清）

                2. domains: 涉及的领域列表

                3. key_entities: 关键实体（人名、产品名、术语等）

                4. search_queries: 需要检索的查询列表（1-3个不同角度的查询）

                5. requires_retrieval: boolean，是否需要检索
                   - SIMPLE_QA 且是常识 → false
                   - 其他 → true

                6. time_sensitive: boolean，是否需要最新信息

                只返回 JSON，不要其他内容。
                """)
                .param("question", question))
            .call()
            .entity(QueryAnalysis.class);
    }

    // 分析结果结构
    public record QueryAnalysis(
        String questionType,
        List<String> domains,
        List<String> keyEntities,
        List<String> searchQueries,
        boolean requiresRetrieval,
        boolean timeSensitive
    ) {}
}

// 使用示例
// 输入："Spring AI 的 Advisor 机制和 Spring AOP 有什么区别？"
// 输出：
// {
//   "questionType": "COMPARISON",
//   "domains": ["Spring AI", "Spring AOP"],
//   "keyEntities": ["Advisor", "AOP"],
//   "searchQueries": [
//     "Spring AI Advisor 机制",
//     "Spring AOP 工作原理",
//     "Spring AI Advisor vs Spring AOP 对比"
//   ],
//   "requiresRetrieval": true,
//   "timeSensitive": false
// }
```

### 查询重写

```java
// ⭐ 查询重写——针对不同检索策略优化查询
@Service
public class QueryRewriter {

    private final ChatClient chatClient;

    /**
     * 根据检索策略重写查询
     */
    public RewrittenQueries rewrite(String originalQuery, QueryAnalysis analysis) {
        return chatClient.prompt()
            .user(u -> u.text("""
                针对以下问题，生成多个检索查询：

                原始问题：{question}

                生成要求：
                1. vector_query: 向量检索查询（语义搜索，保持原意但更清晰）
                2. keyword_query: 关键词查询（提取核心关键词，用于全文检索）
                3. hyde_query: HyDE 查询（假设存在答案，生成一段"假设答案"文本）
                4. sub_queries: 子问题分解（如果问题复杂，拆分为多个子问题）

                只返回 JSON。
                """)
                .param("question", originalQuery))
            .call()
            .entity(RewrittenQueries.class);
    }

    public record RewrittenQueries(
        String vectorQuery,
        String keywordQuery,
        String hydeQuery,       // 假设答案，用于 HyDE 检索
        List<String> subQueries  // 子问题
    ) {}
}
```

---

## 四、检索规划器

### Agent 自主检索规划

```java
// ⭐ 检索规划——Agent 决定怎么检索
@Service
public class RetrievalPlanner {

    private final VectorStore vectorStore;
    private final ElasticsearchService elasticsearchService;
    private final RerankService rerankService;

    @Tool(description = "向量语义搜索。"
          + "适合模糊匹配、语义相似的场景。"
          + "参数query为自然语言查询。")
    public List<Document> vectorSearch(
            @ToolParam(description = "自然语言查询") String query,
            @ToolParam(description = "返回数量，默认5") int topK) {

        return vectorStore.similaritySearch(
            SearchRequest.builder()
                .query(query)
                .topK(topK)
                .similarityThreshold(0.7)
                .build());
    }

    @Tool(description = "关键词全文检索。"
          + "适合精确匹配、技术术语、代码片段搜索。"
          + "参数keywords为空格分隔的关键词。")
    public List<Document> keywordSearch(
            @ToolParam(description = "关键词，空格分隔") String keywords,
            @ToolParam(description = "返回数量，默认5") int topK) {

        return elasticsearchService.search(keywords, topK);
    }

    @Tool(description = "混合检索。"
          + "同时使用语义和关键词检索，取加权结果。"
          + "推荐大多数场景使用此方法。")
    public List<Document> hybridSearch(
            @ToolParam(description = "自然语言查询") String query,
            @ToolParam(description = "关键词") String keywords) {

        // 并行执行两种检索
        List<Document> vectorResults = vectorSearch(query, 5);
        List<Document> keywordResults = keywordSearch(keywords, 5);

        // RRF 融合
        return fusionByRRF(vectorResults, keywordResults);
    }

    @Tool(description = "对检索结果重排序。"
          + "使用专门的 Reranker 模型提升排序质量。")
    public List<Document> rerank(
            @ToolParam(description = "原始查询") String query,
            @ToolParam(description = "待排序的文档列表") List<Document> documents) {

        return rerankService.rerank(query, documents);
    }

    /**
     * Agent 的检索入口——它自主决定使用哪些检索工具
     */
    public RetrievalResult retrieve(QueryAnalysis analysis) {
        String userMessage = buildRetrievalPrompt(analysis);

        return chatClient.prompt()
            .user(userMessage)
            .functions("vectorSearch", "keywordSearch",
                       "hybridSearch", "rerank")
            .call()
            .entity(RetrievalResult.class);
    }
}
```

### 检索策略选择

```
Agent 的检索决策树
═══════════════════════════════════════

分析用户问题
│
├─ 常识性简单问题？
│   └─ 不检索，直接回答
│
├─ 需要专业知识？
│   ├─ 技术术语明确？─── keywordSearch（精确）
│   ├─ 概念语义模糊？─── vectorSearch（语义）
│   └─ 两者都有？─────── hybridSearch（混合）
│
├─ 复杂多跳问题？
│   ├─ 第一步：检索问题的核心实体
│   ├─ 第二步：根据第一步结果进一步检索
│   └─ 第三步：汇总所有结果
│
├─ 比较类问题？
│   ├─ 分别检索每个比较对象
│   └─ 合并结果对比
│
└─ 信息不足？
    └─ 反问用户补充信息
```

---

## 五、检索增强生成

### 动态上下文构建

```java
// ⭐ 智能上下文构建——根据检索结果动态决定上下文内容
@Service
public class ContextBuilder {

    private static final int MAX_CONTEXT_TOKENS = 6000;

    /**
     * 根据检索结果构建最优上下文
     */
    public String buildContext(List<Document> documents, QueryAnalysis analysis) {
        // 1. 重排序
        List<Document> ranked = rerankByRelevance(documents, analysis);

        // 2. 去重
        List<Document> unique = deduplicate(ranked);

        // 3. 按 Token 预算筛选
        List<Document> fitting = selectByTokenBudget(unique, MAX_CONTEXT_TOKENS);

        // 4. 构建带引用的上下文
        return fitting.stream()
            .map(doc -> formatDocument(doc))
            .collect(Collectors.joining("\n\n---\n\n"));
    }

    private String formatDocument(Document doc) {
        return String.format("""
            [%s] (相关度: %.2f)
            来源: %s
            %s
            """,
            doc.getMetadata().get("title"),
            doc.getMetadata().get("score"),
            doc.getMetadata().get("source"),
            doc.getContent());
    }

    /**
     * 基于 Token 预算选择最重要文档
     */
    private List<Document> selectByTokenBudget(
            List<Document> documents, int maxTokens) {
        List<Document> selected = new ArrayList<>();
        int totalTokens = 0;

        for (Document doc : documents) {
            int tokens = estimateTokens(doc.getContent());
            if (totalTokens + tokens <= maxTokens) {
                selected.add(doc);
                totalTokens += tokens;
            } else {
                break;  // 预算用完，停止添加
            }
        }
        return selected;
    }
}
```

### 生成与反思

```java
// ⭐ 生成 + 自我反思
@Service
public class ResponseGenerator {

    private final ChatClient chatClient;
    private final ContextBuilder contextBuilder;

    @Tool(description = "基于检索结果生成回答")
    public GenerationResult generate(
            @ToolParam(description = "用户问题") String question,
            @ToolParam(description = "检索到的文档上下文") String context) {

        return chatClient.prompt()
            .user(u -> u.text("""
                基于以下资料回答问题。

                资料：
                {context}

                问题：{question}

                要求：
                1. 如果资料充分，给出详细回答并在末尾 [来源：文档标题]
                2. 如果资料部分相关，说明哪些有依据、哪些是推断
                3. 如果资料不充分，明确指出信息缺口
                4. 如果资料相互矛盾，指出矛盾并分析

                回答：
                """)
                .param("context", context)
                .param("question", question))
            .call()
            .entity(GenerationResult.class);
    }

    @Tool(description = "评估回答质量")
    public QualityReport evaluate(
            @ToolParam(description = "用户问题") String question,
            @ToolParam(description = "生成的回答") String answer,
            @ToolParam(description = "检索到的文档") String context) {

        return chatClient.prompt()
            .user(u -> u.text("""
                评估以下回答的质量：

                问题：{question}
                回答：{answer}
                参考文档：{context}

                评估维度（1-10分）：
                1. faithfulness: 忠实于参考文档（是否幻觉）
                2. completeness: 完整性（是否回答了所有方面）
                3. relevance: 相关性（是否针对问题）
                4. clarity: 清晰度（是否易懂）

                如果 faithfulness < 7 或 completeness < 6，需要重新回答。

                只返回 JSON。
                """)
                .param("question", question)
                .param("answer", answer)
                .param("context", context))
            .call()
            .entity(QualityReport.class);
    }

    public record GenerationResult(
        String answer,
        List<String> sources,
        List<String> informationGaps   // 信息缺口
    ) {}

    public record QualityReport(
        int faithfulness,
        int completeness,
        int relevance,
        int clarity,
        boolean needsRevision,
        String revisionReason
    ) {}
}
```

---

## 六、完整实战：企业内部知识库助手

### 需求分析

```text
企业知识库助手需求
═══════════════════════════════════════

场景：大型企业内部知识库问答
文档类型：技术文档、产品手册、流程规范、API 文档
用户：全体员工（技术水平不一）
问题：每日约 5000+ 查询

核心需求：
├─ 准确：回答必须基于公司文档，不产生幻觉
├─ 实时：文档更新后立即生效
├─ 全面：覆盖多个业务线的文档
├─ 追溯：每个回答必须有来源引用
└─ 安全：只有授权用户能访问对应文档
```

### 完整实现

```java
// ⭐ 企业知识库 Agent——完整实现
@Service
public class EnterpriseKnowledgeAgent {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;
    private final DocumentProcessor documentProcessor;
    private final ContextBuilder contextBuilder;
    private final AuditLogger auditLogger;

    // ════════════════════════════════════════
    // 核心检索工具
    // ════════════════════════════════════════

    @Tool(description = "语义搜索公司内部知识库。推荐使用。")
    public List<Document> searchKnowledgeBase(
            @ToolParam(description = "自然语言问题") String query,
            @ToolParam(description = "文档领域，如 '技术'/'产品'/'流程'") String domain,
            @ToolParam(description = "返回文档数量，默认5") int topK) {

        SearchRequest request = SearchRequest.builder()
            .query(query)
            .topK(topK)
            .similarityThreshold(0.7)
            .filterExpression("domain == '" + domain + "'")  // 领域过滤
            .build();

        return vectorStore.similaritySearch(request);
    }

    @Tool(description = "搜索最新的公司公告和通知。自动过滤最近30天。")
    public List<Document> searchAnnouncements(
            @ToolParam(description = "关键词") String keywords) {

        LocalDate thirtyDaysAgo = LocalDate.now().minusDays(30);

        return vectorStore.similaritySearch(
            SearchRequest.builder()
                .query(keywords)
                .topK(5)
                .filterExpression("type == 'announcement'")
                .build());
    }

    @Tool(description = "精确搜索 API 文档和代码示例。按版本过滤。")
    public List<Document> searchApiDocs(
            @ToolParam(description = "API 名称") String apiName,
            @ToolParam(description = "版本号，如 '1.6.x'") String version) {

        return vectorStore.similaritySearch(
            SearchRequest.builder()
                .query(apiName + " API 文档 示例")
                .topK(3)
                .filterExpression("type == 'api' AND version == '" + version + "'")
                .build());
    }

    @Tool(description = "当用户问题需要跨多个领域检索时使用。传入逗号分隔的领域列表。")
    public Map<String, List<Document>> multiDomainSearch(
            @ToolParam(description = "查询") String query,
            @ToolParam(description = "逗号分隔的领域，如 '技术,产品,流程'") String domains) {

        Map<String, List<Document>> results = new HashMap<>();
        for (String domain : domains.split(",")) {
            results.put(domain.trim(),
                searchKnowledgeBase(query, domain.trim(), 3));
        }
        return results;
    }

    // ════════════════════════════════════════
    // 主入口——Agentic RAG 循环
    // ════════════════════════════════════════

    public String answer(String userMessage) {
        String currentUserId = getCurrentUserId();

        // 1. 分析问题
        QueryAnalysis analysis = queryAnalyzer.analyze(userMessage);

        // 2. 如果不需要检索，直接回答
        if (!analysis.requiresRetrieval()) {
            return chatClient.prompt()
                .user(userMessage)
                .call()
                .content();
        }

        // ⭐ Agent 自主决定检索策略并执行
        RetrievalResult retrieval = chatClient.prompt()
            .user(u -> u.text("""
                用户问题：{question}

                分析结果：
                - 类型：{type}
                - 领域：{domains}
                - 实体：{entities}
                - 检索查询：{queries}

                请使用提供的工具检索信息。
                根据问题类型选择最合适的检索策略。
                """)
                .param("question", userMessage)
                .param("type", analysis.questionType())
                .param("domains", String.join(", ", analysis.domains()))
                .param("entities", String.join(", ", analysis.keyEntities()))
                .param("queries", String.join(", ", analysis.searchQueries())))
            .functions("searchKnowledgeBase", "searchAnnouncements",
                       "searchApiDocs", "multiDomainSearch")
            .call()
            .entity(RetrievalResult.class);

        // 3. 构建上下文
        String context = contextBuilder.buildContext(
            retrieval.documents(), analysis);

        // 4. 生成回答
        GenerationResult generation = chatClient.prompt()
            .user(u -> u.text("""
                基于以下资料回答问题。

                用户问题：{question}

                参考资料：
                {context}

                要求：
                - 回答必须基于资料
                - 标注每个关键信息的来源
                - 如果资料不足，明确说明
                - 回答格式清晰、结构化
                """)
                .param("question", userMessage)
                .param("context", context))
            .call()
            .entity(GenerationResult.class);

        // 5. 质量评估（自动反思）
        QualityReport quality = evaluateQuality(
            userMessage, generation.answer(), context);

        if (quality.needsRevision()) {
            // 重新检索 + 重新生成
            List<Document> supplementDocs = supplementarySearch(
                userMessage, quality.revisionReason());
            generation = regenerate(userMessage,
                context + "\n\n补充资料：\n" + formatDocs(supplementDocs));
        }

        // 6. 审计日志
        auditLogger.log(userMessage, generation, currentUserId);

        return formatFinalAnswer(generation);
    }

    // ════════════════════════════════════════
    // 文档索引
    // ════════════════════════════════════════

    @Scheduled(cron = "0 0 2 * * ?")  // 每天凌晨2点
    public void indexDocuments() {
        List<Resource> newDocs = docScanner.getNewDocuments();

        for (Resource doc : newDocs) {
            Document document = new Document(doc);

            // 元数据
            document.getMetadata().put("source", doc.getFilename());
            document.getMetadata().put("domain", classifyDomain(doc));
            document.getMetadata().put("type", classifyType(doc));
            document.getMetadata().put("indexedAt", Instant.now().toString());

            // 分块
            List<Document> chunks = documentProcessor.split(document, 512, 128);

            // 写入向量库
            vectorStore.write(chunks);
        }
    }

    // ════════════════════════════════════════
    // 辅助方法
    // ════════════════════════════════════════

    private String formatFinalAnswer(GenerationResult generation) {
        StringBuilder sb = new StringBuilder(generation.answer());

        if (!generation.sources().isEmpty()) {
            sb.append("\n\n---\n**参考资料**\n");
            generation.sources().forEach(s ->
                sb.append("- ").append(s).append("\n"));
        }

        if (!generation.informationGaps().isEmpty()) {
            sb.append("\n\n**信息缺口**\n");
            generation.informationGaps().forEach(gap ->
                sb.append("- ⚠️ ").append(gap).append("\n"));
        }

        return sb.toString();
    }
}
```

### 部署配置

```yaml
# ⭐ 生产 RAG 配置
spring:
  ai:
    # 检索模型
    openai:
      base-url: http://localhost:8000  # vLLM 本地
      chat:
        options:
          model: qwen4:7b

    # 向量库
    vectorstore:
      pgvector:
        table-name: enterprise_knowledge
        dimensions: 1024
        initialize-schema: true
        index-type: HNSW

    # 嵌入模型
    embedding:
      ollama:
        model: nomic-embed-text

  # 文档存储
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 200MB

  # 缓存
  redis:
    host: localhost
    port: 6379

---
# 生产环境配置
spring:
  config:
    activate:
      on-profile: prod

  ai:
    retry:
      max-attempts: 3
      backoff:
        initial-interval: 1000
        multiplier: 2

    circuit-breaker:
      enabled: true
      failure-threshold: 5
      timeout: 30s
```

---

## 七、评估与优化

### RAG 评估指标体系

```text
RAG 系统评估指标
═══════════════════════════════════════

检索质量
├── Recall@K: 前 K 个结果中包含相关文档的比例
│   目标：>0.8
├── Precision@K: 前 K 个结果中相关文档的比例
│   目标：>0.7
├── MRR (Mean Reciprocal Rank): 第一个相关结果的排名
│   目标：>0.9
└── NDCG: 排序质量
    目标：>0.85

生成质量
├── Faithfulness: 回答是否忠实于参考文档
│   目标：>0.9（自动化 LLM-as-a-Judge 评估）
├── Answer Relevance: 回答是否针对问题
│   目标：>0.85
├── Hallucination Rate: 幻觉比例
│   目标：<0.05
└── Citation Accuracy: 引用准确性
    目标：>0.95

系统性能
├── P50 延迟：<2s（端到端）
├── P99 延迟：<10s
├── 吞吐量：>100 QPS（单节点）
└── 索引更新延迟：<5min
```

### 自动化评估流水线

```java
// ⭐ RAG 评估框架
@Service
public class RagEvaluator {

    private final ChatClient judgeLlm;  // 评估用的 LLM（通常用更强的模型）

    /**
     * 运行评估套件
     */
    public EvaluationReport evaluate(List<TestCase> testCases) {
        List<EvaluationResult> results = new ArrayList<>();

        for (TestCase testCase : testCases) {
            // 执行 RAG
            String answer = ragService.answer(testCase.question);

            // 评估
            EvaluationResult result = judgeLlm.prompt()
                .user(u -> u.text("""
                    请评估以下 RAG 回答质量：

                    问题：{question}
                    预期答案：{expected}
                    实际回答：{actual}
                    参考文档：{context}

                    评估维度：
                    1. faithfulness (1-5): 回答是否基于参考文档
                    2. completeness (1-5): 是否覆盖了答案的各个方面
                    3. conciseness (1-5): 是否简洁不冗余

                    输出 JSON 格式评估结果。
                    """)
                    .param("question", testCase.question())
                    .param("expected", testCase.expectedAnswer())
                    .param("actual", answer)
                    .param("context", testCase.context()))
                .call()
                .entity(EvaluationResult.class);

            result.setQuestion(testCase.question());
            result.setActualAnswer(answer);
            results.add(result);
        }

        return aggregateResults(results);
    }

    public record TestCase(
        String question,
        String expectedAnswer,
        String context
    ) {}
}

// 持续集成
@Component
public class RagCiPipeline {

    @Scheduled(cron = "0 0 4 * * ?")  // 每天凌晨4点
    public void nightlyEvaluation() {
        List<TestCase> testCases = loadTestCases();
        EvaluationReport report = evaluator.evaluate(testCases);

        if (report.faithfulnessScore() < 0.85) {
            alertService.sendAlert("RAG 忠实度下降："
                + report.faithfulnessScore());
        }

        reportGenerator.saveReport(report);
    }
}
```

### 优化路线图

```
RAG 优化优先级
═══════════════════════════════════════

第一阶段（基础，第1-2周）
├── ✅ 搭建标准 RAG 流水线
├── ✅ 选择合适的 Embedding 模型
├── ✅ 确定分块策略（递归分块，chunk=512, overlap=128）
├── ✅ 配置向量库索引（HNSW, ef_search=40）
└── ✅ 建立基线评估指标

第二阶段（检索优化，第3-4周）
├── ✅ 实现混合检索（语义 + 关键词）
├── ✅ 添加 Reranker
├── ✅ 实现查询重写（HyDE + 子问题分解）
├── ✅ 添加元数据过滤（领域过滤、时间过滤）
└── ✅ 评估 Recall@K 提升

第三阶段（Agent 化，第5-6周）
├── ✅ Agent 自主决定是否检索
├── ✅ 多步检索推理链
├── ✅ 回答质量自我评估
├── ✅ 信息不足时追问
└── ✅ 评估端到端准确率

第四阶段（工程化，第7-8周）
├── ✅ 生产部署（高可用、负载均衡）
├── ✅ 缓存策略（语义缓存）
├── ✅ 监控告警（延迟/质量/成本）
├── ✅ A/B 测试框架
└── ✅ 持续评估 CI 流水线
```

> [!tip] **实战建议**
> 1. **不要一步到位**：先从标准 RAG 开始跑通，再逐步引入 Agent 能力
> 2. **先有基线再优化**：没有评估指标就没有优化方向
> 3. **检索质量 > 模型大小**：一个 7B 模型 + 高质量检索，效果常好于 70B + 低质量检索
> 4. **缓存是关键**：高频重复问题的语义缓存可以节省 60%+ 的 Token 和延迟
> 5. **监控回答质量**：用 LLM-as-a-Judge 自动监控回答忠实度，低于阈值时告警
