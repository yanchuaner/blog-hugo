---
title: "AI 网文创作框架 — 基于 LangChain 的长篇小说辅助创作系统"
summary: "LangChain + DeepSeek + RAG，110+ 章规划，多 Agent 流水线的 AI 辅助网文创作框架。"
date: 2026-06-24
draft: true
layout: "single"
showtoc: true
tags: ["LangChain", "DeepSeek", "RAG", "Python", "AI Agent"]
categories: ["项目"]
---

## 项目简介

一个基于 LangChain 的 AI 辅助长篇小说创作系统。通过 RAG 向量检索管理角色与世界观设定，多 Agent 协作保持长篇情节一致性，支持 110+ 章规划的自动化写作流水线。

## 项目背景

长篇小说创作需要作者在百万字级别维持角色设定、世界观和情节的一致。传统 AI 写作工具（单次对话）无法解决长程记忆和设定漂移问题。本项目探索如何用 LLM + 知识库解决这一痛点。

## 技术架构

```text
用户输入（章节大纲 + 关键事件）
    ↓
编排 Agent（LangChain Router）
    ├── 角色检索 Agent → ChromaDB (RAG)
    ├── 情节一致性 Agent → 前后文比对
    ├── 世界观 Agent → 设定知识库
    └── 写作 Agent → DeepSeek API 生成
    ↓
章节输出 → 自动写入知识库（增量索引）
```

**技术栈**: Python · LangChain · DeepSeek API · ChromaDB · text-embedding-3-small

## 核心功能

| 功能 | 说明 |
|------|------|
| 角色管理 | RAG 向量检索，确保角色行为一致 |
| 情节追踪 | 关键事件记录 + 前后章对比 |
| 文风控制 | System Prompt + Few-shot 模板 |
| 知识库 | ChromaDB 存储设定、关系、事件 |
| 增量索引 | 每章生成后自动入库 |

## 技术难点

### 长程上下文丢失

128K token 对百万字小说仍不够。解决方案：RAG 从知识库检索相关角色和事件，而非把所有内容塞入 prompt。

### 角色设定漂移

角色在前 10 章和后 50 章可能出现言行不一致。解决方案：角色 Agent 在每次生成前从向量库检索角色最新设定。

## 项目截图

> 截图待补充

## 项目总结

**学到了什么**：LangChain 链式调用模式、RAG pipeline 设计、Prompt Engineering 工程化、多 Agent 协作编排。

**未来计划**：Fine-tuning 开源模型、更细粒度的情节图谱、Web 界面。

## GitHub

[https://github.com/yanchuaner](https://github.com/yanchuaner)

## Roadmap

- [x] v0.1: LangChain + DeepSeek + 基础链式调用
- [x] v0.2: RAG 向量检索 + ChromaDB 知识库
- [ ] v0.3: 多 Agent 协作编排
- [ ] v0.4: 情节图谱可视化
- [ ] v1.0: Web 界面 + 开源
