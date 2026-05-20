# 全栈知识体系 · Obsidian Vault

> 一个 Java 全栈开发者的个人知识库，覆盖后端、前端、运维、AI Agent 等领域的系统性学习笔记。

---

## 📖 概述

本仓库是一个 **Obsidian 知识库（Vault）**，用于构建可积累、可检索的个人技术知识体系。从"被动收藏"到"主动整理"，每篇笔记都是经过理解、重组后的知识沉淀。

### 核心原则

- **系统性**：按专题分篇，注重概念之间的关联
- **实战导向**：理论 + 代码示例 + 最佳实践
- **时效性**：内容持续更新，标注版本信息（如 Spring AI 1.6.x、MCP v1.0）
- **可追溯**：笔记间通过 Wiki 链接相互引用，形成知识网络

---

## 🗂️ 目录结构

```
📦 Obsidian Vault
├── 📁 AIAgent篇/           AI Agent 专题（从入门到实战）
│   ├── 基础概念篇（3篇）    Agent 概述、LLM 选型、Prompt Engineering
│   ├── 核心技术篇（4篇）    Function Calling、RAG、Multi-Agent、Memory
│   ├── 框架与工具篇（5篇）  Spring AI、LangChain4j、MCP、Skill
│   └── 工程实践篇（4篇）    安全、本地部署、Agentic RAG、监控
│
├── 📁 java学习篇/          Java 核心技术
│   ├── Java 基础           JDK 17+ 新特性
│   ├── Spring Boot         Spring Boot 3.x
│   └── Spring AI           AI 工程化框架
│
├── 📁 python学习篇/        Python 学习笔记
│
├── 📁 前端篇/              前端技术栈
│   ├── HTML/CSS/JS
│   ├── Vue / React
│   └── TypeScript / CSS 预处理器
│
├── 📁 中间件篇/            企业级中间件
│   ├── MyBatis / MyBatis-Plus
│   ├── Maven
│   ├── JPA
│   └── Tomcat
│
├── 📁 数据库篇/            数据库与存储
│
├── 📁 运维篇/              运维与 DevOps
│   ├── Docker & Kubernetes
│   ├── Linux
│   └── Git
│
└── 📁 八股文面试篇/        面试题整理
```

---

## 🔧 技术栈覆盖

| 领域 | 技术 | 状态 |
|:----|:-----|:----:|
| **AI Agent** | Spring AI 1.6.x, MCP v1.0, LangChain4j, Semantic Kernel | ✅ 持续更新 |
| **LLM** | Claude 4, GPT-5, DeepSeek-R2, Qwen 4, Llama 4 | ✅ 2026.05 版 |
| **本地模型** | Ollama, vLLM, llama.cpp | ✅ |
| **Java 框架** | Spring Boot 3.x, Spring AI, MyBatis, JPA | ✅ |
| **前端** | Vue 3, React 19, TypeScript 5.x | ✅ |
| **中间件** | Maven, Tomcat, MyBatis-Plus | ✅ |
| **运维** | Docker, K8s, Linux, Git | ✅ |
| **数据库** | MySQL, PostgreSQL, Redis, PGVector | ✅ |

---

## 📝 笔记规范

### 命名约定

```
[系列]/{主题}/{笔记名}.md
```

- 文件夹按**数字前缀**排序（如 `01.基础概念` → `02.核心技术`）
- 文件名使用有意义的**中文描述**
- 图片等附件放在各篇的 `attachments/` 目录

### 笔记结构

每篇笔记遵循统一的结构：

```markdown
# 标题

## 一、概述

### 定义与背景

### 解决的问题

---

## 二、核心概念

### 概念说明

### 代码示例（如有）

---

## 三、进阶内容

...（按需）

---

## 四、最佳实践

> [!tip] 总结性建议
```

### 引用规范

- **Wiki 链接**：`[[笔记名]]` 用于引用本 Vault 内其他笔记
- **外部链接**：`[描述](URL)` 用于引用外部资源
- **代码块**：标注语言（\`\`\`java / \`\`\`yaml / \`\`\`bash）
- **标注**：使用 Obsidian Callout（`> [!tip]` / `> [!warning]` / `> [!note]`）
- **版本标注**：内容涉及特定版本时明确标注

---

## 🚀 使用方式

### 前提

1. 安装 [Obsidian](https://obsidian.md/)
2. 以**打开本地文件夹**方式打开本仓库根目录

### 推荐插件

| 插件                             | 用途        |
| :----------------------------- | :-------- |
| **obsidian-git**               | 自动备份到 Git |
| **obsidian-excalidraw-plugin** | 绘制架构图/流程图 |
| **RealClaudian**               | AI 辅助笔记编写 |

### 阅读建议

- **按专题顺序阅读**——每个篇目内笔记有递进关系
- **善用图谱**——Obsidian 的 Graph View 展示知识之间的关联
- **搜索优先**——`Ctrl+Shift+F` 全文搜索比翻目录更快
- **动手实践**——笔记中的代码示例建议自己在项目中试一遍

---

## 🔄 版本历史

本 Vault 使用 Git 进行版本管理，通过 **obsidian-git** 插件自动备份。

提交记录格式：
```
笔记备份: YYYY-MM-DD HH:mm:ss
```

---

## 📄 许可

本项目中的笔记内容仅供个人学习使用。其中引用的技术文档、框架名称等均为各所属方的商标或知识产权。
