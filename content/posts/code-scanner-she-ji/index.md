---
title: "Code Scanner 项目设计：面向安全审计的静态代码扫描器"
summary: "从零设计一个基于 AST 的静态代码扫描器，支持 C/C++ 安全规则检测与 CI/CD 集成。"
date: 2026-06-24
lastmod: 2026-06-24
categories:
  - 安全
tags:
  - SAST
  - 安全工具
  - C++
  - AST
  - CI/CD
comments: true
showtoc: true
searchHidden: false
hidemeta: false
draft: false
---

## 为什么做这个项目

SAST (Static Application Security Testing) 是安全左移的关键工具。在了解市场上现有方案（SonarQube、Fortify、Semgrep）后，我决定做一个轻量级的 C/C++ 代码扫描器，用于学习和实践。

## 设计目标

- 支持 C/C++ 常见安全规则检测
- 命令行 + CI/CD 友好
- 输出 SARIF 格式（GitHub Code Scanning 兼容）
- 可扩展的规则引擎

## 架构设计

```text
输入：C/C++ 源码文件
    ↓
1. 词法分析 (Lexer)
    ↓
2. 语法分析 → AST (Parser)
    ↓
3. AST 遍历 (Visitor)
    ↓
4. 规则匹配引擎
    ├── 缓冲区溢出检测
    ├── 格式化字符串漏洞
    ├── 空指针解引用
    └── 资源泄漏
    ↓
5. 结果输出 (SARIF / JSON / Console)
```

## 技术选型

| 组件 | 方案 | 理由 |
|------|------|------|
| Parser | tree-sitter / clang AST | 工业级 AST 解析 |
| 规则引擎 | YAML 配置 + Python | 规则可热更新 |
| 输出格式 | SARIF | GitHub Code Scanning 标准 |
| CI 集成 | GitHub Actions | 仓库原生支持 |

## 已实现的规则

```yaml
rules:
  - id: buffer-overflow
    severity: critical
    description: "检测不安全的 strcpy/gets 调用"
    pattern: "strcpy|gets"

  - id: format-string
    severity: high
    description: "检测格式化字符串漏洞"
    pattern: "printf(variable)"

  - id: null-dereference
    severity: high
    description: "检测潜在空指针解引用"
```

## 与 SonarQube 对比

| 特性 | Code Scanner | SonarQube |
|------|-------------|-----------|
| 部署 | 单二进制 / pip install | 需要 Java + 数据库 |
| CI 集成 | 原生 GitHub Actions | 需要额外配置 |
| 规则定制 | YAML 文件 | Web UI |
| C/C++ 支持 | 聚焦 | 全语言 |

## 下一步开发计划

- [ ] 集成 tree-sitter C/C++ grammar
- [ ] 实现 20+ 安全规则
- [ ] GitHub Actions 模板
- [ ] 性能基准测试
