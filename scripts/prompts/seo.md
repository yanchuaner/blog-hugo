# SEO 阶段 Prompt

为以下文章生成 front matter 和 SEO 元数据。

## 输出格式

```yaml
---
title: "原标题优化版"
summary: "一句话摘要（用于 RSS 和首页展示，≤160字）"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: false
showtoc: true
categories: ["分类"]
tags: ["标签1", "标签2", "标签3"]
series: ["系列名"]
comments: true
description: "120-160字的 meta description，含核心关键词"
---
```

## 规则

- title：原标题 + 关键词优化，不超过 60 字
- summary：吸引点击的一句话，包含价值点
- description：120-160 字，面向搜索引擎，包含关键词
- tags：3-5 个，从已有标签中选择
- series：如果是系列文章，必须填写
- date/lastmod：使用当前日期

## 输入

文章内容：
{{POLISHED_DRAFT}}

分析结果：
{{ANALYSIS_JSON}}
