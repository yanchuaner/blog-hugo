# 博客未来优化 Todo List (待启动任务)

> 本文档记录博客未来可探索的优化与拓展方向。

---

## 🟢 进阶拓展与自动化 (待启动)

### 1. 静态图片自动化压缩管道 (Image Processing Pipeline)
- **目标**：自动优化文章与项目卡片中的图片，降低 LCP 指标。
- **方案**：
  - 利用 Hugo 内建的 `.Resize` / `.Process` 对模板中的本地图片进行自动 WebP 转换和尺寸压缩。
  - 或者在 `verify_site.py` 中增加对 static 目录下新增大图的警告。
- **涉及文件**：`verify_site.py` 或相关 layout 文件

### 2. SEO 增强与 JSON-LD 结构化数据
- **目标**：让 Google 等搜索引擎对博客内容生成富媒体摘要（Rich Snippets）。
- **方案**：
  - 在 [extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/_partials/extend_head.html) 中根据页面类型，动态生成 `Person` 规范及 `BlogPosting` 规范的 `<script type="application/ld+json">`。
- **涉及文件**：[extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/_partials/extend_head.html)

### 3. PWA 离线阅读支持 (Progressive Web App)
- **目标**：使博客支持离线或弱网瞬间加载，并可“添加至主屏幕”作为 App 运行。
- **方案**：
  - 在 `static/` 下配置 `manifest.json`。
  - 编写 `static/sw.js` 实现核心资源与已读文章的 Service Worker 离线缓存。
- **涉及文件**：`static/manifest.json` (新文件), `static/sw.js` (新文件)

### 4. BlogOps AI 云端自动化写作发布流水线 (BlogOps Cloud)
- **目标**：实现“本地提交原始草稿，云端 AI 自动校对、润色、纠错并回写发布”。
- **方案**：
  - 打通 [blogops.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/.github/workflows/blogops.yml) 中被注释的第二阶段，配置 DeepSeek API 的 GitHub Secrets，完成草稿润色、拼音 slug 和 front-matter 生成。
- **涉及文件**：[blogops.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/.github/workflows/blogops.yml), [blogops.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/blogops.py)
