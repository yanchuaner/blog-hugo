---
title: "鸿蒙开发入门：从环境搭建到第一个应用"
summary: "HarmonyOS + ArkTS 开发环境搭建与 Hello World 实践记录。"
date: 2026-06-24
lastmod: 2026-06-24
categories:
  - 开发
tags:
  - HarmonyOS
  - ArkTS
  - 鸿蒙
  - 移动开发
comments: true
showtoc: true
searchHidden: false
hidemeta: false
draft: false
---

## 为什么学鸿蒙

鸿蒙生态正在快速扩张。作为计算机专业学生，了解国产操作系统生态既是技术储备，也是职业视野的拓展。

## 环境搭建

### DevEco Studio

下载安装 DevEco Studio，配置 SDK：

```bash
# 检查 Node.js 版本
node -v  # 需要 14.x+

# 安装 DevEco Studio
# 从华为开发者官网下载安装包
```

### 创建第一个项目

```typescript
// index.ets
@Entry
@Component
struct Index {
  @State message: string = 'Hello HarmonyOS';

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(50)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
    }
    .height('100%')
  }
}
```

## ArkTS 特点

- 声明式 UI，类似 SwiftUI / Flutter
- TypeScript 超集，类型安全
- 状态管理：@State、@Prop、@Link
- 组件化开发模式

## 开发体验

| 优点 | 不足 |
|------|------|
| DevEco Studio 集成度高 | 生态还在早期 |
| 文档逐步完善 | 第三方库较少 |
| 华为官方支持力度大 | 学习资料不如 Android 丰富 |

## 下一步

- 学习 ArkUI 组件体系
- 实现一个 Todo List 应用
- 探索鸿蒙分布式能力
