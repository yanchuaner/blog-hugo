---
title: "校友会管理平台 — 燕川中学校友社区系统"
summary: "基于 Next.js + React 的全栈校友管理平台，支持成员管理、活动发布与在线捐赠。"
date: 2026-06-24
draft: true
layout: "single"
showtoc: true
tags: ["Next.js", "React", "Tailwind CSS", "全栈开发"]
categories: ["项目"]
---

## 项目简介

为燕川中学校友会打造的在线社区管理平台。校友注册、活动发布、捐赠管理、通讯录维护一站解决。

## 项目背景

校友会日常管理依赖微信群和 Excel，信息分散、效率低下。作为校友会核心成员，我发起此项目，用技术解决实际问题。

## 技术架构

```text
Next.js App Router
    ├── 前端: React + Tailwind CSS + shadcn/ui
    ├── 后端: Next.js API Routes / Server Actions
    ├── 数据库: PostgreSQL (Neon)
    ├── 认证: NextAuth.js
    └── 部署: Vercel
```

**技术栈**: Next.js 14 · React 18 · Tailwind CSS · shadcn/ui · PostgreSQL · NextAuth.js

## 核心功能

| 功能 | 说明 |
|------|------|
| 校友注册 | 邮箱验证 + 校友身份审核 |
| 通讯录 | 按届别/地区/行业筛选 |
| 活动管理 | 创建活动、报名、签到 |
| 捐赠管理 | 在线捐赠 + 资金公示 |
| 消息通知 | 站内通知 + 邮件推送 |

## 技术难点

### 校友身份验证

如何确认注册者确实是该校校友？方案：人工审核 + 校友邀请码机制，而非简单的邮箱正则匹配。

### 数据库设计

校友-届别-活动-捐赠的四维关系建模。使用 Prisma ORM 管理 schema 迁移。

## 项目截图

> 截图待补充

## 项目总结

**学到了什么**：全栈项目的完整生命周期、数据库 schema 设计、用户认证流程、社区产品的产品思维。

**未来计划**：上线运营、校友小程序版、AI 校友匹配。

## GitHub

[https://github.com/yanchuaner](https://github.com/yanchuaner)

## Roadmap

- [ ] v0.1: 基础 CRUD + 校友注册
- [ ] v0.2: 活动管理 + 报名签到
- [ ] v0.3: 捐赠管理 + 资金公示
- [ ] v0.4: 小程序版
- [ ] v1.0: 正式上线 + 运营
