# 博客优化 Todo List (第四阶段：细节优化与功能拓展)

> 前三阶段的 UI 灵动感升级、安全 CSP 收紧和本地质量校验已完美闭环。
> 本阶段核心目标：打磨网站性能细节，拓展搜索、时光轴、友链和 AI 流水线等功能。

---

## 🔴 高优先级（P0）— 细节打磨与性能加速

### 1. 补全本地托管字体文件 (Local Fonts)
- **目标**：解决目前 `/fonts/*.woff2` 请求 404 的问题，让本地托管字体真正生效。
- **方案**：
  - 运行 [download_fonts.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/download_fonts.py) 脚本下载 Google Fonts 字体资源至 `static/fonts/` 下。
  - 确认构建后，`public/fonts/` 下能够正常请求 woff2 字体，且在 [verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py) 中增加对字体可访问性检测。
- **涉及文件**：`static/fonts/` (新建文件), [verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py)

### 2. 超轻量页面即时预加载 (Instant Prefetching)
- **目标**：点击文章或跳转页面时达到“零白屏”瞬间切换的极致体验。
- **方案**：
  - 在 [theme-footer.js](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/js/theme-footer.js) 中实现超轻量级的预加载逻辑：监听站内链接的 `mouseenter` / `touchstart` 事件。
  - 当用户悬浮于链接超过 80ms 时，动态向 `<head>` 插入 `<link rel="prefetch">` 预加载目标 HTML。
  - 确保该机制完全符合现有的 strict CSP，不引入任何外部第三方脚本。
- **涉及文件**：[theme-footer.js](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/js/theme-footer.js)

---

## 🟡 中优先级（P1）— 交互与内容拓展

### 3. 符合 CSP 规范的全静态本地搜索 (Local Search)
- **目标**：为博客读者提供免服务器、毫秒级响应的文章搜索功能。
- **方案**：
  - 修改 [config.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/config.yml) 的 outputs 部分，配置主页支持 JSON 格式，编译时自动生成全站索引 `index.json`。
  - 创建搜索页目录与文件 `content/search/index.md`，设置 `layout: "search"`。
  - 将 `fuse.js` 本地化托管，通过 PaperMod 原生 Search 模板在前端实现关键字高亮检索，绕过外部脚本 CSP 限制。
- **涉及文件**：[config.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/config.yml), `content/search/index.md` (新文件)

### 4. 互动成长时光轴重构 (Journey Timeline)
- **目标**：将原有的表格形式成长记录，重构为高度匹配首页 Linear 质感的动态时光轴。
- **方案**：
  - 新建 `layouts/journey/list.html` 布局模板。
  - 运用 CSS 伪元素绘制中心垂直轴线，配合响应式 Grid 布局，将每个里程碑事件作为卡片排列于两侧。
  - 加入卡片 hover 流光动画与滚动淡入动效 (`IntersectionObserver`)。
- **涉及文件**：`layouts/journey/list.html` (新文件), `assets/css/spa.css`

### 5. 现代开发者友情链接卡片墙 (Friends Page)
- **目标**：建立美观的技术博客友情链接面板，并集成死链预警。
- **方案**：
  - 编写 `data/friends.yml` 配置文件，存储友链名称、链接、头像与描述。
  - 编写 `layouts/friends/list.html` 模板，渲染 shadcn-ui 风格的格子卡片墙。
  - 在 [verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py) 中集成 HTTP 探测逻辑，每次编译时检测友链是否存活，发现死链或 SSL 过期在终端给出警示。
- **涉及文件**：`data/friends.yml` (新文件), `layouts/friends/list.html` (新文件), [verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py)

---

## 🟢 低优先级（P2）— 高级自动化与 PWA 适配

### 6. 静态图片自动化压缩管道 (Image Processing Pipeline)
- **目标**：自动优化文章与项目卡片中的图片，降低 LCP 指标。
- **方案**：
  - 利用 Hugo 内建的 `.Resize` / `.Process` 对模板中的本地图片进行自动 WebP 转换和尺寸压缩。
  - 或者在 [verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py) 中增加对 static 目录下新增大图的警示。
- **涉及文件**：[verify_site.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/verify_site.py) 或相关 layout 文件

### 7. SEO 增强与 JSON-LD 结构化数据
- **目标**：让 Google 等搜索引擎对博客内容生成富媒体摘要（Rich Snippets）。
- **方案**：
  - 在 [extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/_partials/extend_head.html) 中根据页面类型，动态生成 `Person` 规范及 `BlogPosting` 规范的 `<script type="application/ld+json">`。
- **涉及文件**：[extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/_partials/extend_head.html)

### 8. PWA 离线阅读支持 (Progressive Web App)
- **目标**：使博客支持离线或弱网瞬间加载，并可“添加至主屏幕”作为 App 运行。
- **方案**：
  - 在 `static/` 下配置 `manifest.json`。
  - 编写 `static/sw.js` 实现核心资源与已读文章的 Service Worker 离线缓存。
- **涉及文件**：`static/manifest.json` (新文件), `static/sw.js` (新文件)

### 9. BlogOps AI 云端自动化写作发布流水线 (BlogOps Cloud)
- **目标**：实现“本地提交原始草稿，云端 AI 自动校对、润色、纠错并回写发布”。
- **方案**：
  - 打通 [blogops.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/.github/workflows/blogops.yml) 中被注释的第二阶段，配置 DeepSeek API 的 GitHub Secrets。
  - 编写 AI 处理逻辑，在 `content/raw/` 放入新草稿并推送后，GitHub Actions 自动润色并生成标准拼音 Slug 与 Front-matter 提交发布。
- **涉及文件**：[blogops.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/.github/workflows/blogops.yml), [blogops.py](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/scripts/blogops.py)
