---
title: "Code Scanner — 轻量级静态代码安全扫描器"
summary: "基于 AST 的 C/C++ 静态安全扫描器，支持安全规则检测与 CI/CD 集成。"
date: 2026-06-24
draft: true
layout: "single"
showtoc: true
tags: ["SAST", "安全工具", "C++", "AST"]
categories: ["项目"]
---

## 项目简介

一个面向安全审计的轻量级静态代码扫描器，基于 AST（抽象语法树）分析 C/C++ 源码，自动检测常见安全漏洞模式，输出 SARIF 格式报告，可集成 GitHub Actions CI/CD。

## 项目背景

SAST（Static Application Security Testing）是 DevSecOps 中"安全左移"的核心工具。当前主流方案（SonarQube、Fortify）部署重、定制难。本项目旨在学习 SAST 原理的同时，打造一个开发者友好的轻量方案。

## 技术架构

```text
输入：C/C++ 源码
    ↓
tree-sitter Parser → AST
    ↓
Visitor 遍历 AST 节点
    ↓
规则匹配引擎（YAML 配置）
    ├── 缓冲区溢出 (strcpy/gets)
    ├── 格式化字符串 (printf var)
    ├── 空指针解引用
    ├── 资源泄漏 (fopen/no fclose)
    └── 整数溢出
    ↓
结果聚合器 → SARIF / JSON / Console 输出
```

**技术栈**: Python 3.11 · tree-sitter · YAML · GitHub Actions · SARIF

## 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| C/C++ AST 解析 | ✅ | 基于 tree-sitter grammar |
| 规则引擎 | ✅ | YAML 配置，热更新 |
| 5 条安全规则 | ✅ | 缓冲区/格式串/空指针/资源/整数 |
| SARIF 输出 | ✅ | GitHub Code Scanning 兼容 |
| GitHub Actions | 🔜 | 自动化 PR 扫描 |
| 自定义规则 | 🔜 | 用户可编写规则 DSL |

## 技术难点

### 1. AST 遍历性能

tree-sitter 的 `visit()` 方法是递归的，对大项目（>10万行）可能较慢。解决：增量扫描 + 文件级别的并行处理。

### 2. 规则匹配精度

纯 AST 模式匹配会产生误报。例如 `printf(user_input)` 是漏洞，但 `printf("%s", user_input)` 是安全的。通过模式匹配 + 上下文分析降低误报。

## 项目截图

> 截图待补充

## 项目总结

**学到了什么**：AST 的工作原理、SAST 引擎设计模式、SARIF 标准格式、GitHub Code Scanning 集成方式。

**未来计划**：支持 Python/JavaScript、自定义规则 DSL、Web 仪表盘。

## GitHub

[https://github.com/yanchuaner](https://github.com/yanchuaner)

## Roadmap

- [x] v0.1: tree-sitter + 基础规则
- [ ] v0.2: 10+ 规则 + GitHub Actions 集成
- [ ] v0.3: 多语言支持
- [ ] v0.4: Web 仪表盘
- [ ] v1.0: 开源发布 + 文档
