---
title: "AI 项目复盘：LangChain + DeepSeek 搭建网文创作框架"
summary: "使用 LangChain 链式调用 DeepSeek API，结合 RAG 向量检索，构建长篇小说 AI 辅助创作系统。"
date: 2026-06-24
lastmod: 2026-06-24
categories:
  - AI
tags:
  - LangChain
  - DeepSeek
  - RAG
  - Python
  - AI Agent
comments: true
showtoc: true
searchHidden: false
hidemeta: false
draft: true
---

## 项目背景

长篇小说创作需要作者在百万字级别保持设定一致性。我尝试用 LangChain 构建 AI 辅助创作框架，帮助管理角色、情节与世界观。

## 系统架构

```text
用户输入 (章节大纲)
    ↓
LangChain Agent
    ├── 角色检索 (RAG → 向量数据库)
    ├── 情节一致性检查
    ├── 文风控制 Prompt
    └── DeepSeek API 生成
    ↓
章节输出 + 自动保存到知识库
```

## 技术栈

| 组件 | 技术 |
|------|------|
| LLM | DeepSeek API |
| 链式编排 | LangChain |
| 向量存储 | ChromaDB |
| Embedding | text-embedding-3-small |
| 前端 | Python CLI + Markdown 输出 |

## 核心代码

```python
from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个网文作者助手，风格为东方玄幻。"),
    ("human", "根据以下大纲写一个章节：{outline}")
])

llm = ChatDeepSeek(model="deepseek-chat", temperature=0.8)
chain = prompt | llm

result = chain.invoke({"outline": "主角在秘境中发现上古传承..."})
```

## 遇到的挑战

1. **长文本上下文丢失** — 单次对话 128K token 对百万字小说仍不够
2. **角色设定漂移** — 使用 RAG 从知识库检索角色信息来解决
3. **文风一致性** — 需要精心设计 System Prompt 和 Few-shot 示例

## 效果评估

- 单章生成时间：约 30 秒
- 设定一致性：通过知识库管理，准确率约 85%
- 人工修改比例：约 20%

## 后续优化

- 引入多 Agent 协作（角色Agent、情节Agent、文风Agent）
- 使用更细粒度的向量索引
- 考虑 Fine-tuning 开源模型
