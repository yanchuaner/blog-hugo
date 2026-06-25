# 博客未来优化 Todo List (已完成)

> 本文档记录的博客优化与拓展方向已全部实现并顺利上线。

---

## 🟢 进阶拓展与自动化 (已全部完成)

### 1. 静态图片自动化压缩管道 (Image Processing Pipeline) [已完成]
- **目标**：自动优化文章与项目卡片中的图片，降低 LCP 指标。
- **状态**：已集成 Hugo 的图片 `.Process "resize 600x webp q85"` 管道，并在 `verify_site.py` 中加入了 `[7/7]` 阶段的图片大小校验（单张大图上限 300 KB 限制）。

### 2. SEO 增强与 JSON-LD 结构化数据 [已完成]
- **目标**：让 Google 等搜索引擎对博客内容生成富媒体摘要（Rich Snippets）。
- **状态**：在 `layouts/_partials/extend_head.html` 中加入了动态 `Person` / `WebSite` / `BlogPosting` 结构化数据，并通过覆盖 `schema_json.html` 屏蔽了 PaperMod 自带的默认格式。

### 3. PWA 离线阅读支持 (Progressive Web App) [已完成]
- **目标**：使博客支持离线或弱网瞬间加载，并可“添加至主屏幕”作为 App 运行。
- **状态**：添加了 `manifest.json` 与 `sw.js` (Service Worker) 核心缓存，并配置了优雅的、符合 Vercel 设计风格的 `offline.html` 离线断网兜底单页。

### 4. BlogOps AI 云端自动化写作发布流水线 (BlogOps Cloud) [已完成]
- **目标**：实现“本地提交原始草稿，云端 AI 自动校对、润色、纠错并回写发布”。
- **状态**：已启用 DeepSeek API（`blogops.py process`），并配置了 `.github/workflows/blogops.yml` 云端自动化工作流，草稿在 push 到 `content/raw/` 时会自动由 AI 润色发布并自动推送回 main 分支。
