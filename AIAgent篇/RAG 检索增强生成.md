# RAG 检索增强生成

## 一、什么是 RAG

### 定义

**RAG（Retrieval-Augmented Generation，检索增强生成）** 是一种让 LLM 在回答时先从外部知识库**检索相关文档**，再基于这些文档**生成答案**的技术架构。它解决了 LLM 知识固化、无法获取实时信息和内部知识的问题。

```
    传统 LLM 回答                         RAG 回答
    ┌──────────────┐                   ┌──────────────┐
    │  用户提问      │                   │  用户提问      │
    └──────┬───────┘                   └──────┬───────┘
           │                                  │
           ▼                                  ▼
    ┌──────────────┐                   ┌──────────────┐
    │  LLM 直接回答  │                   │  检索知识库    │
    │              │                   │  (向量/全文)   │
    │  依赖训练数据  │                   └──────┬───────┘
    │  知识截止到训练日│                         │
    │  无法获取内部知识│                         ▼
    └──────────────┘                   ┌──────────────┐
                                       │  LLM + 上下文  │
                                       │              │
                                       │  基于检索结果  │
                                       │  生成回答      │
                                       └──────────────┘
```

### 为什么需要 RAG

| 问题 | 传统 LLM | RAG 方案 |
|:----|:---------|:---------|
| **知识过时** | 训练数据截止到某个日期 | 实时检索最新文档 |
| **缺乏内部知识** | 不知道企业内部的文档 | 检索企业知识库 |
| **幻觉** | 可能编造答案 | 基于检索的事实回答 |
| **不可解释** | 不知道答案来自哪 | 附带来源引用 |
| **知识更新** | 需要重新训练 | 更新文档库即可 |

### RAG 发展历程（2023-2026）

```
2023                 2024                 2025                    2026
│                   │                   │                       │
├─ Naive RAG       ├─ Advanced RAG     ├─ Agentic RAG          ├─ RAG 2.0
│  简单检索+生成      │  查询重写+重排序    │  多步推理+动态检索     │  端到端学习
│  基础 Chunking    │  多路检索          │  Agent 自主决定        │  可微检索
│                   │  Hybrid Search    │  何时检索+检索什么     │  全链路优化
```

截止 2026 年 5 月，**Agentic RAG** 是主流范式——Agent 自主决定检索时机、多步检索、融合推理。

---

## 二、RAG 核心流程

```
                     RAG 标准流程
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   索引阶段     │  │   检索阶段    │  │   生成阶段    │
│              │  │              │  │              │
│ 文档          │  │ 用户提问      │  │  Prompt 组装  │
│  ↓           │  │  ↓           │  │  ↓           │
│ 文档分块      │  │ 查询转换      │  │ LLM 生成回答  │
│  ↓           │  │  ↓           │  │  ↓           │
│ Embedding    │  │ 向量检索      │  │ 附带引用来源  │
│  ↓           │  │  ↓           │  │              │
│ 存入向量库    │  │ 重排序        │  │              │
│              │  │  ↓           │  │              │
│              │  │ 结果合并      │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 索引阶段

```java
// ⭐ Spring AI + PGVector 构建知识库
@Configuration
public class RagIndexConfig {

    @Bean
    public VectorStore vectorStore(DataSource dataSource) {
        return PGVectorStore.builder(dataSource)
            .vectorTableName("knowledge_vectors")
            .dimensions(1536)            // embedding 维度
            .distanceType(VectorStoreDistanceType.COSINE)
            .build();
    }

    @Bean
    public DocumentProcessor documentProcessor() {
        return DocumentProcessors.builder()
            // 文档分割策略
            .splitter(DocumentSplitter.recursive()
                .chunkSize(500)          // 每块大小
                .chunkOverlap(100)       // 重叠大小
                .separators(List.of("\n\n", "\n", "。", ".", " "))
            )
            // 元数据提取
            .metadataExtractor(metadata -> metadata
                .add("source", "company_kb")
                .add("department", extractDepartment(metadata))
                .add("last_updated", LocalDate.now().toString())
            )
            .build();
    }
}
```

### 文档分块策略 ⭐

```java
// ⭐ 不同文档类型使用不同的分块策略
public class ChunkingStrategies {

    // 1. 递归字符分割（通用）
    public DocumentSplitter recursiveSplitter() {
        return DocumentSplitter.recursive()
            .chunkSize(1000)
            .chunkOverlap(200);
    }

    // 2. 语义分割（按段落/句子边界）
    public DocumentSplitter semanticSplitter() {
        return new SemanticDocumentSplitter(embeddingModel)
            .minChunkSize(200)
            .threshold(0.8);  // 相似度阈值，低于此值切分
    }

    // 3. 代码分割（按函数/类边界）
    public DocumentSplitter codeSplitter() {
        return DocumentSplitter.forCode("java")
            .chunkSize(100);
    }
}

// ⭐ 分块大小选择
// 问答类文档：chunkSize=500, overlap=100  （精确匹配）
// 技术文档：  chunkSize=1000, overlap=200 （上下文充足）
// 代码库：    按函数/类分割
// 书籍/长文： chunkSize=2000, overlap=300 （保留段落完整性）
```

---

## 三、Embedding 与向量检索 ⭐

### Embedding 模型

```java
// ⭐ Spring AI 支持的 Embedding 模型
@Bean
public EmbeddingModel embeddingModel() {
    // OpenAI
    return new OpenAiEmbeddingModel(openAiApi)
        .withModel("text-embedding-3-small");  // 1536 维, 性价比高
    // text-embedding-3-large → 3072 维, 更精确但更贵

    // 或本地模型
    // return new OllamaEmbeddingModel()
    //     .withModel("bge-m3");  // BGE-M3, 支持中英双语
}
```

### 向量检索

```java
@Service
public class VectorSearchService {

    private final VectorStore vectorStore;

    // ⭐ 基础向量检索
    public List<Document> search(String query, int topK) {
        return vectorStore.similaritySearch(
            SearchRequest.query(query)
                .withTopK(topK)           // 返回 top-K 条
                .withSimilarityThreshold(0.7)  // 相似度阈值
        );
    }

    // ⭐ 带元数据过滤的检索
    public List<Document> searchWithFilter(String query,
                                           String department) {
        return vectorStore.similaritySearch(
            SearchRequest.query(query)
                .withTopK(5)
                .withFilterExpression("department == '" + department + "'")
        );
    }

    // ⭐ 多路检索（向量 + 全文）
    public List<Document> hybridSearch(String query) {
        // 向量检索（语义相似）
        List<Document> vectorResults = vectorStore.similaritySearch(
            SearchRequest.query(query).withTopK(5));

        // 全文检索（关键词匹配）——依赖数据库的全文索引
        List<Document> keywordResults = fullTextSearch(query);

        // 合并去重排序
        return mergeAndRerank(vectorResults, keywordResults);
    }
}
```

### 向量数据库对比

| 数据库 | 部署方式 | 性能 | 特点 |
|:------|:--------|:----|:-----|
| **PGVector** ⭐ | PostgreSQL 插件 | 良好 | 和业务数据同库，运维简单 |
| **Milvus** | 独立服务 | 高 | 分布式，十亿级规模 |
| **Chroma** | 嵌入式 | 中等 | 开发/测试首选，简单 |
| **Qdrant** | 独立服务 | 高 | Rust 实现，性能优秀 |
| **Elasticsearch** | 独立服务 | 高 | 全文+向量混合搜索最佳 |
| **Redis Stack** | 独立服务 | 高 | 内存级速度，适合缓存 |

```yaml
# Spring Boot + PGVector 配置
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/knowledge
    username: postgres
    password: postgres

  ai:
    vectorstore:
      pgvector:
        table-name: knowledge_vectors
        dimensions: 1536
        distance-type: cosine
        initialize-schema: true
```

---

## 四、检索优化 ⭐

### 查询转换

```java
// ⭐ 用户原始查询 → 优化后的检索查询
@Service
public class QueryTransformer {

    private final ChatClient chatClient;

    // 1. 查询重写——把口语化问题转为检索友好的表述
    public String rewriteQuery(String userQuery) {
        return chatClient.prompt()
            .user("""
                将以下用户问题改写为更利于知识库检索的形式。
                提取核心关键词，去除口语化表达。

                用户问题：{query}

                改写后的检索查询：
                """, userQuery)
            .call()
            .content();
    }

    // 2. 查询分解——复杂问题拆分为多个子查询
    public List<String> decomposeQuery(String complexQuery) {
        return chatClient.prompt()
            .user("""
                将以下复杂问题拆分为多个独立的子问题。

                问题：{query}

                请返回 JSON 数组格式：
                ["子问题1", "子问题2", ...]
                """, complexQuery)
            .call()
            .entity(List.class);
    }

    // 3. 假设性文档嵌入（HyDE）
    public String generateHypotheticalDoc(String query) {
        return chatClient.prompt()
            .user("""
                针对以下问题，假设有一段完美的文档可以回答它。
                请生成这段文档。

                问题：{query}

                假设文档：
                """, query)
            .call()
            .content();
        // 然后用生成的文档去做向量检索
        // 效果：查询 → 答案文档 → 用答案文档搜相似文档
    }
}
```

### 重排序（Rerank）⭐

```java
// ⭐ 重排序——在向量检索后对结果做精细化排序
@Service
public class RerankService {

    // 方法一：用 LLM 重排序（精度高，成本高）
    public List<Document> llmRerank(String query, List<Document> candidates) {
        String result = chatClient.prompt()
            .user("""
                问题：{query}

                请从以下文档中选出与问题最相关的 3 条，按相关性从高到低排序。
                只返回文档的序号列表，如 [3, 1, 5]。

                文档列表：
                {documents}
                """, query, formatDocs(candidates))
            .call()
            .content();

        return reorderByIndices(candidates, parseIndices(result));
    }

    // 方法二：专用 Rerank 模型（精度高，成本低）⭐
    public List<Document> modelRerank(String query, List<Document> candidates) {
        // 使用 BGE-Reranker 或 Cohere Rerank 等专用模型
        return rerankModel.rerank(query, candidates, 3);
    }

    // 方法三：加权融合
    public List<Document> weightedFusion(String query, List<Document> candidates) {
        for (Document doc : candidates) {
            // 向量相似度 * 0.6 + 关键词匹配 * 0.3 + 时效性 * 0.1
            double score = doc.similarity() * 0.6
                         + keywordMatchScore(query, doc) * 0.3
                         + recencyScore(doc) * 0.1;
            doc.setRerankScore(score);
        }
        return candidates.stream()
            .sorted(Comparator.reverseOrder())
            .limit(3)
            .toList();
    }
}
```

### 检索策略总览

```
              ┌──────────────────────────┐
              │      用户提问              │
              └────────────┬─────────────┘
                           │
              ┌────────────┴─────────────┐
              │     查询转换              │
              │  ├─ 重写（Rewrite）        │
              │  ├─ 分解（Decompose）      │
              │  └─ HyDE                  │
              └────────────┬─────────────┘
                           │
              ┌────────────┴─────────────┐
              │     多路检索              │
              │  ├─ 向量检索（语义）        │
              │  ├─ 全文检索（关键词）       │
              │  └─ SQL 检索（结构化数据）   │
              └────────────┬─────────────┘
                           │
              ┌────────────┴─────────────┐
              │     结果融合              │
              │  ├─ RRF（倒数排序融合）     │
              │  └─ 加权合并              │
              └────────────┬─────────────┘
                           │
              ┌────────────┴─────────────┐
              │     重排序（Rerank）       │
              │  ├─ LLM Rerank           │
              │  └─ 专用 Rerank 模型      │
              └────────────┬─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  最终结果 Top-3  │
                    └──────────────┘
```

---

## 五、Spring AI + RAG 实战 ⭐

### 基础 RAG

```java
@Service
public class RagService {

    private final VectorStore vectorStore;
    private final ChatClient chatClient;

    public String answer(String question) {
        // 1. 检索相关文档
        List<Document> docs = vectorStore.similaritySearch(
            SearchRequest.query(question).withTopK(3));

        // 2. 文档内容作为上下文
        String context = docs.stream()
            .map(Document::getContent)
            .collect(Collectors.joining("\n---\n"));

        // 3. 基于上下文生成回答
        return chatClient.prompt()
            .user("""
                基于以下资料回答问题。
                如果资料中找不到答案，请明确说"资料中未提及"。
                回答时引用资料来源。

                资料：
                {context}

                问题：{question}
                """, context, question)
            .call()
            .content();
    }
}
```

### Agentic RAG ⭐

2025-2026 年的主流范式——Agent 自主决定检索策略：

```java
@Service
public class AgenticRagService {

    private final ChatClient chatClient;

    // ⭐ Agent 自主判断：直接回答还是需要检索
    public String process(String question) {
        return chatClient.prompt()
            .user(question)
            .tools(  // Agent 自主决定是否调用检索工具
                searchKnowledgeBase(),
                queryDatabase(),
                searchWeb()
            )
            .call()
            .content();
    }

    // ⭐ 知识库检索工具
    @Tool(description = "搜索内部知识库，用于回答产品、技术、流程相关问题。"
          + "输入：搜索关键词；输出：相关文档片段")
    public List<String> searchKnowledgeBase(
            @ToolParam(description = "搜索关键词，建议提取核心名词") String query) {
        return vectorStore.similaritySearch(
            SearchRequest.query(query).withTopK(3))
            .stream()
            .map(Document::getContent)
            .toList();
    }

    // ⭐ 数据库查询工具
    @Tool(description = "查询关系数据库用于获取结构化数据")
    public List<Map<String, Object>> queryDatabase(
            @ToolParam(description = "SQL 查询语句") String sql) {
        return jdbcTemplate.queryForList(sql);
    }

    // ⭐ 联网搜索工具
    @Tool(description = "搜索互联网获取实时信息")
    public String searchWeb(
            @ToolParam(description = "搜索关键词") String query) {
        return webSearchService.search(query);
    }
}
```

### 多步 RAG 推理

```java
// ⭐ 复杂问题需要多步检索
// 用户："对比一下我们公司和竞争对手的 A 产品差异"

// Agent 执行流程：
// 1. 检索内部知识库 → 获取本公司 A 产品资料
// 2. 联网搜索 → 获取竞争对手 A 产品信息
// 3. 再次检索内部知识库 → 获取产品对比的历史报告
// 4. 综合分析 → 生成对比报告
```

### RAG + 流式响应

```java
@RestController
public class RagController {

    private final RagService ragService;

    @GetMapping("/chat/stream")
    public Flux<String> streamChat(@RequestParam String question) {
        // ⭐ 先检索，再流式生成
        List<Document> docs = vectorStore.similaritySearch(
            SearchRequest.query(question).withTopK(3));

        String context = formatContext(docs);

        return chatClient.prompt()
            .user("""
                基于以下资料回答问题：
                {context}
                问题：{question}
                """, context, question)
            .stream()
            .content();  // 流式输出
    }
}
```

---

## 六、RAG 评估与优化

### RAG 质量评估框架

```
RAG 评估三角
        ┌──────────────┐
        │   检索质量    │
        │  (找到对的)   │
        └──────┬───────┘
               │
               ▼
┌──────────────┼──────────────────┐
│   生成质量          │    端到端质量  │
│  (用得对)          │    (整体效果)  │
│  忠实度            │    用户满意度  │
│  相关性            │    任务完成率  │
│  完整性            │    回答延迟    │
└───────────────────┘
```

### 评估指标

| 维度 | 指标 | 测量方式 |
|:----|:----|:---------|
| **检索精确率** | 检索结果中相关文档比例 | 人工标注 / LLM 评估 |
| **检索召回率** | 相关文档被检索到的比例 | 人工标注 |
| **忠实度** | 回答是否基于检索结果 | LLM-as-a-Judge |
| **答案相关度** | 回答是否针对问题 | LLM-as-a-Judge |
| **来源引用准确率** | 引用是否匹配实际来源 | 自动校验 |

### 常见问题与优化

| 问题 | 原因 | 优化方案 |
|:----|:-----|:---------|
| **检索不到相关内容** | Embedding 不匹配 / 分块不合理 | 换 Embedding 模型 / 调整分块策略 / 查询重写 |
| **检索到但不相关** | 语义相似但实际无关 | 增加 Rerank / 提高相似度阈值 |
| **答案不忠实于来源** | Prompt 没说清楚 | 强化"基于资料回答"约束 |
| **遗漏关键信息** | 只检了单一路径 | 多路检索 + 查询分解 |
| **回答过于冗长** | 上下文塞了太多文档 | 限制 topK + 压缩上下文 |
| **知识更新不及时** | 文档库没更新 | 建立文档自动同步机制 |

### RAG 优化 Checklist

```
✅ 分块大小与文档类型匹配
✅ 分块有适当重叠（避免信息断裂）
✅ 查询经过重写/转换
✅ 使用混合检索（向量+全文）
✅ 检索后经过 Rerank
✅ 设置了合理的相似度阈值
✅ Prompt 明确要求基于资料回答
✅ 回答附带来源引用
✅ 有兜底策略（查不到时明确告知）
✅ 定期评估检索质量
```

---

## 七、高级 RAG 模式

### RAG-Fusion（多路检索融合）

```java
// ⭐ RAG-Fusion：多角度检索后融合
public List<Document> ragFusion(String question) {
    // 1. 从多个角度生成查询
    List<String> queries = queryTransformer.generateVariations(question);
    // [原始问题, 改写1, 改写2, HyDE文档]

    // 2. 每个查询独立检索
    List<List<Document>> allResults = queries.stream()
        .map(q -> vectorStore.similaritySearch(q, 5))
        .toList();

    // 3. RRF 融合排序
    return reciprocalRankFusion(allResults, 10);
}

// RRF 算法
private List<Document> reciprocalRankFusion(
        List<List<Document>> results, int k) {
    Map<String, Double> scoreMap = new HashMap<>();

    for (List<Document> list : results) {
        for (int rank = 0; rank < list.size(); rank++) {
            String id = list.get(rank).getId();
            // RRF 公式：1 / (k + rank)
            scoreMap.merge(id, 1.0 / (k + rank + 1), Double::sum);
        }
    }

    return scoreMap.entrySet().stream()
        .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
        .limit(10)
        .map(entry -> docMap.get(entry.getKey()))
        .toList();
}
```

### Self-RAG（自我反思 RAG）

```java
// ⭐ Self-RAG：检索后自我评估是否需要更多信息
public String selfRag(String question) {
    // 第一轮检索
    List<Document> docs = retrieve(question);
    String answer1 = generate(question, docs);

    // ⭐ 自我评估
    Evaluation eval = evaluateAnswer(question, answer1, docs);

    if (eval.needsMoreInfo()) {
        // 第二轮检索——根据已了解的内容补充检索
        List<Document> moreDocs = retrieve(eval.getMissingInfo());
        docs.addAll(moreDocs);
        answer1 = generate(question, docs);
    }

    if (eval.hasContradictions()) {
        // 存在矛盾信息，需要进一步核实
        List<Document> verifiedDocs = verifyConflicts(eval.getConflicts());
        return generateWithCitations(question, verifiedDocs);
    }

    return answer1;
}
```

### Graph RAG（知识图谱增强 RAG）

```java
// ⭐ 2025-2026 年兴起：RAG + 知识图谱
// 适用于：多跳推理、关系查询
// 例如："张三负责的项目的技术负责人是谁？"
// 需要：用户→项目→技术负责人（两跳关系）

// 实现方式：
// 1. 从文档中提取实体和关系 → 构建知识图谱
// 2. 检索时：向量检索 + 图遍历
// 3. 融合文本和图结构信息生成回答
```

---

## 八、生产部署考量

### 索引 Pipeline

```java
// ⭐ 文档自动同步与索引
@Component
public class DocumentIndexPipeline {

    private final VectorStore vectorStore;
    private final DocumentProcessor processor;

    @Scheduled(cron = "0 0 2 * * ?")  // 每天凌晨 2 点
    public void syncDocuments() {
        // 1. 获取新增/变更的文档
        List<Document> changedDocs = docService.getChangedSince(lastSync);

        // 2. 处理和分块
        List<Document> chunks = processor.process(changedDocs);

        // 3. 写入向量库
        vectorStore.write(chunks);

        // 4. 删除已删除文档的向量
        vectorStore.delete(changedDocs.getDeletedIds());

        log.info("文档同步完成：新增 {}，删除 {}", chunks.size(),
                 changedDocs.getDeletedIds().size());
    }
}
```

### 缓存策略

```java
// ⭐ 语义缓存——相同问题直接返回缓存
@Service
public class SemanticCacheService {

    private final VectorStore cacheStore;

    public String getCachedAnswer(String question) {
        List<Document> cached = cacheStore.similaritySearch(
            SearchRequest.query(question)
                .withTopK(1)
                .withSimilarityThreshold(0.95));  // 高阈值确保精确匹配

        if (!cached.isEmpty()) {
            return cached.get(0).getContent();
        }
        return null;  // 缓存未命中
    }

    public void cacheAnswer(String question, String answer) {
        cacheStore.write(List.of(
            Document.builder()
                .withContent(answer)
                .withMetadata(Map.of("question", question))
                .build()
        ));
    }
}
```

---

## 九、常见面试题

### 1. RAG 解决了什么问题？

> 解决 LLM 的三大痛点：**知识过时**（训练数据截止）、**缺乏内部知识**（企业专有信息）、**幻觉**（编造答案）。RAG 让 LLM 在回答时实时检索外部知识库，基于事实生成答案，同时可追溯来源。

### 2. RAG 和微调有什么区别？

> **RAG** 通过检索外部知识实时增强回答，无需训练，知识更新只需更新文档库。**微调**让模型学习新知识和格式，但知识固化在参数中，更新成本高。两者互补：RAG 负责事实知识，微调负责风格/格式/领域能力。

### 3. 怎么优化 RAG 的检索质量？

> ① **查询重写**：把口语转为检索友好格式；② **分块策略**：根据文档类型调整大小和 overlap；③ **多路检索**：向量+全文混合；④ **Rerank**：检索后精细化排序；⑤ **元数据过滤**：缩小检索范围。

### 4. 什么是 Agentic RAG？

> Agent 自主决定检索策略的 RAG 模式。传统 RAG 每次检索固定步骤，Agentic RAG 可以：判断是否需要检索、多步检索（先查A再用结果查B）、根据已获信息决定是否补充检索。2025-2026 年的主流 RAG 范式。

### 5. Spring AI 中如何实现 RAG？

> `VectorStore` 做向量检索，`DocumentProcessor` 处理文档分块，`ChatClient` 基于检索结果生成回答。通过 `@Tool` 将检索工具注册给 Agent，可实现 Agentic RAG。

---

> [!tip] **学习路径建议**
> 1. **入门**：理解 RAG 流程 → Embedding + 向量检索 → 简单 RAG 实现
> 2. **进阶**：查询转换 → 分块优化 → 混合检索 → Rerank
> 3. **深入**：Agentic RAG → 多步推理 → RAG-Fusion → Self-RAG
> 4. **工程化**：生产 Pipeline → 评估体系 → 缓存策略 → 监控
