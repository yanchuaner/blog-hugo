---
title: "信息安全学习路线：二进制安全入门指南"
summary: "从 CTF 入门到二进制安全，记录学习路线、工具链与环境搭建。"
date: 2026-06-24
lastmod: 2026-06-24
categories:
  - 安全
tags:
  - 信息安全
  - CTF
  - 二进制安全
  - 逆向工程
comments: true
showtoc: true
searchHidden: false
hidemeta: false
draft: true
---

## 起点

信息安全是一个广而深的领域。我选择从二进制安全切入——因为它最接近计算机底层，能真正理解程序是如何运行的。

## 学习路线图

```text
基础知识
  ├── C 语言 / 汇编 (x86/x64)
  ├── 操作系统原理
  └── 计算机网络

逆向工程
  ├── 静态分析：IDA Pro / Ghidra
  ├── 动态调试：GDB / x64dbg
  └── 加壳脱壳基础

Pwn
  ├── 栈溢出 (Buffer Overflow)
  ├── 格式化字符串
  ├── ROP (Return-Oriented Programming)
  └── Heap Exploitation

Web 安全
  ├── SQL 注入 / XSS / CSRF
  ├── 文件上传漏洞
  └── 逻辑漏洞
```

## 工具链

| 工具 | 用途 | 平台 |
|------|------|------|
| IDA Pro | 静态逆向 | Windows/Linux |
| Ghidra | 开源逆向 | 跨平台 |
| GDB + pwndbg | 动态调试 | Linux |
| pwntools | Pwn 脚本 | Python |

## CTF 入门

推荐平台：
- **BUUCTF**：国内新手友好，题量大
- **CTFHub**：技能树式学习路径
- **pwnable.kr**：经典 Pwn 题目

## 核心思维转变

从"写代码"到"读代码"再到"理解代码在内存中的行为"。这是安全方向与开发方向最大的不同。

## 后续计划

- 完成 50 道 Pwn 题
- 深入学习 ROP 链构造
- 参加 XCTF 联赛
