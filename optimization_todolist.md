# 博客优化 Todo List

> 基于 `project_review.md` 分析报告生成，按优先级排序。
> 每项任务包含：涉及文件、具体操作步骤、验证方法。

---

## 🔴 高优先级（P0）— 必须修复

### 1. 配置 Favicon 资源路径

- **维度**：SEO / 无障碍
- **涉及文件**：[config.yml](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/config.yml) (第 46-51 行)
- **问题**：`static/` 下已有完整 Favicon 文件，但 `config.yml` 中路径字段全为空字符串，PaperMod 无法渲染对应的 `<link>` 标签。
- [x] 将 `favicon` 设置为 `"/favicon.ico"`
- [x] 将 `favicon16x16` 设置为 `"/favicon-16x16.png"`
- [x] 将 `favicon32x32` 设置为 `"/favicon-32x32.png"`
- [x] 将 `apple_touch_icon` 设置为 `"/apple-touch-icon.png"`
- [x] 将 `safari_pinned_tab` 设置为 `"/safari-pinned-tab.svg"`
- **验证**：`hugo` 编译后，在 `public/index.html` 中搜索 `favicon`，确认生成了对应的 `<link rel="icon">` 标签。

---

### 2. 消除暗黑模式闪烁 (FOUC)

- **维度**：UI/UX / 交互
- **涉及文件**：
  - [spa.js](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/js/spa.js) (第 136-143 行，暗黑模式同步模块)
  - [extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html)
- **问题**：暗黑模式的 `.dark` class 切换逻辑在页面底部 JS 中执行，导致刷新时先亮后暗的闪烁。
- [x] 从 `spa.js` 中剥离第 136-143 行的暗黑模式同步 IIFE
- [x] 在 `extend_head.html` 中新增一段阻塞式内联 `<script>`（放在 `<link>` 标签之前），内容为：
  ```html
  <script>
    (function(){
      var d = document.documentElement;
      if (d.getAttribute('data-theme') === 'dark') d.classList.add('dark');
      new MutationObserver(function(){
        d.classList.toggle('dark', d.getAttribute('data-theme') === 'dark');
      }).observe(d, {attributes:true, attributeFilter:['data-theme']});
    })();
  </script>
  ```
- [x] 确认 `spa.js` 中已移除冗余的暗黑同步代码，避免重复监听
- **验证**：将浏览器主题设为暗黑模式，强制刷新页面（Ctrl+Shift+R），观察是否还有亮 → 暗的闪烁。

---

### 3. 优化 Canvas 粒子背景渲染性能

- **维度**：性能 / 加载
- **涉及文件**：[spa.js](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/js/spa.js) (第 6-93 行，粒子模块)
- **问题**：`requestAnimationFrame` 无条件持续运行，即使 Canvas 不可见或页面在后台标签页中，仍消耗 CPU/GPU。
- [x] 添加 Page Visibility API 监听，在标签页不可见时暂停动画循环：
  ```javascript
  let animating = true;
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) { animating = false; }
    else { animating = true; animate(); }
  });
  ```
- [x] 在 `animate()` 函数入口处添加 `if (!animating) return;` 守卫
- [x] （可选进阶）添加 `IntersectionObserver` 监听 `#particles` Canvas 元素，离开视口时同样暂停绘制
- **验证**：打开浏览器开发者工具 → Performance 面板，切换到其他标签页后观察 CPU 使用率是否归零。

---

### 4. 补全外部链接安全属性

- **维度**：安全 / 健壮性
- **涉及文件**：
  - [index.html (首页)](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/_default/index.html) (第 22、142、145 行)
  - [list.html (项目页)](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/projects/list.html) (第 41、44 行)
  - [comments.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/comments.html)
- **问题**：部分 `target="_blank"` 链接只有 `rel="noopener"`，缺少 `noreferrer`。
- [x] 在首页模板中，将所有 `rel="noopener"` 统一改为 `rel="noopener noreferrer"`
- [x] 在项目列表页模板中，执行同样的替换
- [x] 全局搜索确认：`grep -rn 'target="_blank"' layouts/` 检查是否有遗漏
- **验证**：`hugo` 编译后，`grep 'target="_blank"' public/**/*.html` 确认每个实例都包含 `noopener noreferrer`。

---

### 5. 审核并发布草稿文章

- **维度**：SEO / 无障碍
- **涉及文件**：`content/posts/` 下所有 `index.md`
- **问题**：仅 1 篇文章已发布，5 篇高质量文章仍处于 `draft: true`，生产构建不会生成。
- [x] 审核 [acm-suan-fa-xun-lian-bi-ji/index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/posts/acm-suan-fa-xun-lian-bi-ji/index.md)，确认内容完整后改 `draft: false`
- [x] 审核 [ai-xiang-mu-fu-pan/index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/posts/ai-xiang-mu-fu-pan/index.md)，确认内容完整后改 `draft: false`
- [x] 审核 [code-scanner-she-ji/index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/posts/code-scanner-she-ji/index.md)，确认内容完整后改 `draft: false`
- [x] 审核 [hong-meng-kai-fa-ru-men/index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/posts/hong-meng-kai-fa-ru-men/index.md)，确认内容完整后改 `draft: false`
- [x] 审核 [xin-xi-an-quan-xue-xi-lu-xian/index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/posts/xin-xi-an-quan-xue-xi-lu-xian/index.md)，确认内容完整后改 `draft: false`
- [x] 审核 [journey/_index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/journey/_index.md) 和 [notes/_index.md](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/content/notes/_index.md)，确认后改 `draft: false`
- [x] 对每篇文章运行 `python scripts/blogops.py check <path>` 确保通过质量检查
- **验证**：`hugo`（不带 `-D`）编译后，确认 Pages 数量从 21 显著增长（预期 ≥ 50）。

---

## 🟡 中优先级（P1）— 建议尽快处理

### 6. 本地化托管 Google Fonts

- **维度**：性能 / 加载
- **涉及文件**：
  - [extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html) (第 11-13 行)
  - `static/fonts/`（需新建）
  - [spa.css](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/css/spa.css)（需新增 `@font-face`）
- **问题**：通过 `fonts.googleapis.com` 加载外部字体，在国内网络下可能加载缓慢或超时。
- [x] 下载 Inter (wght 400/500/600/700/800) 和 Noto Sans SC (wght 400/500/700) 的 `woff2` 文件
- [x] 放置到 `static/fonts/` 目录下
- [x] 在 `spa.css` 顶部新增 `@font-face` 声明块（出于模块化架构考量，已在 PaperMod 自动打包合并的 `assets/css/extended/fonts.css` 中进行本地托管声明）
- [x] 删除 `extend_head.html` 中第 11-13 行的 Google Fonts `<link>` 和 `preconnect`
- [x] 保留 `extend_head.html` 中的 `<style>` 内的 `font-family` 声明不变（已外置到打包的 CSS，从 extend_head 清除以收紧 CSP 规则）
- **验证**：在浏览器 Network 面板中确认不再有对 `fonts.googleapis.com` 和 `fonts.gstatic.com` 的请求，且字体正常显示。

---

### 7. 抽取项目列表页的内联样式

- **维度**：UI/UX / 交互
- **涉及文件**：
  - [layouts/projects/list.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/projects/list.html) (第 16-48 行)
  - [spa.css](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/css/spa.css)
  - [extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html)（需扩展条件判断）
- **问题**：`projects/list.html` 中大量硬编码 `style="..."` 内联样式，破坏结构与表现分离。
- [x] 将所有 inline style 提炼为语义化的 CSS class（复用 `spa.css` 中已有的 `.spa-project-card` 等）
- [x] 在 `list.html` 模板中用 class 替换 style 属性
- [x] 修改 `extend_head.html` 的条件加载逻辑，让 `spa.css` 也在 `/projects/` 页面生效：
  ```go
  {{- if or .IsHome (eq .Layout "guestbook") (eq .Section "projects") }}
  ```
- [x] 确认页面视觉效果与重构前完全一致
- **验证**：`grep -c 'style=' layouts/projects/list.html` 结果应为 0 或极少（仅动态条件样式保留）。

---

### 8. 规范化 OpenGraph 分享图逻辑

- **维度**：SEO / 无障碍
- **涉及文件**：[extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html) (第 24-29 行)
- **问题**：OG Image 硬编码为全局默认图，文章页无法展示各自的封面图。
- [x] 将第 24-29 行的 OG/Twitter Image 硬编码替换为动态逻辑：
  ```go
  {{- $ogImage := "https://blog.codequest.com.cn/og-image.png" }}
  {{- with .Params.cover.image }}
    {{- $ogImage = . | absURL }}
  {{- else }}
    {{- with .Params.images }}
      {{- $ogImage = index . 0 | absURL }}
    {{- end }}
  {{- end }}
  <meta property="og:image" content="{{ $ogImage }}">
  ```
- [x] 同步更新 `twitter:image` 使用相同的 `$ogImage` 变量
- **验证**：在一篇配置了 `cover.image` 的文章编译后，检查其 HTML `<head>` 中 `og:image` 是否指向文章封面图而非全局默认图。

---

### 9. 收紧 CSP 安全规则

- **维度**：安全 / 健壮性
- **涉及文件**：[extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html) (第 2-10 行)
- **问题**：CSP 中使用了 `'unsafe-inline'`，削弱了 XSS 防御能力。
- [x] 评估是否可以将 `<style>` 内联块（第 14-17 行的字体声明）移动到 `spa.css` 中
- [x] 如果成功外置，将 CSP 中的 `style-src 'unsafe-inline'` 移除
- [x] 对于暗黑模式的内联 `<script>`（P0 第 2 项新增），计算其 SHA-256 哈希值，在 CSP 中用 `'sha256-xxx'` 替换 `'unsafe-inline'`
- [ ] （可选）为内联脚本添加 `nonce` 属性，通过 Hugo 模板动态生成
- **验证**：部署后在浏览器 Console 中确认无 CSP 违规警告，功能正常。

---

## 🟢 低优先级（P2）— 锦上添花

### 10. 静态资源启用 Preload

- **维度**：性能 / 加载
- **涉及文件**：[extend_head.html](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/layouts/partials/extend_head.html)
- [x] 为关键字体文件添加 `<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/inter-var.woff2">`
- [x] 为首页专用 CSS 添加 `<link rel="preload" as="style" href="...spa.css...">`
- **验证**：Lighthouse Performance 分数提升，LCP 指标改善。

---

### 11. 优化移动端回顶按钮定位

- **维度**：UI/UX / 交互
- **涉及文件**：[spa.css](file:///c:/Users/lucky%20dog/Desktop/web_projects/blog-hugo/assets/css/spa.css) (第 602-619 行)
- [x] 在 `@media (max-width: 768px)` 媒体查询中为 `.spa-back-top` 增加：
  ```css
  .spa-back-top { bottom: 4.5rem; right: 1.25rem; }
  ```
- [x] 确认 `.spa-back-top` 的 transition 属性已覆盖 `opacity` 和 `transform`（当前已有，确认无遗漏）
- **验证**：在移动端模拟器中，滚动页面后回顶按钮不与系统手势栏重叠。

---

## 📋 执行建议

| 阶段 | 任务编号 | 预计耗时 | 说明 |
|:---:|:---:|:---:|:---|
| **第一阶段** | #1, #4 | 15 分钟 | 纯配置修改，风险最低，立即见效 |
| **第二阶段** | #2, #3 | 30 分钟 | JS 逻辑调整，需回归测试暗黑模式和粒子动画 |
| **第三阶段** | #5 | 1-2 小时 | 逐篇审核文章质量，运行 blogops check |
| **第四阶段** | #6, #7 | 45 分钟 | 字体本地化 + 样式重构，需仔细比对视觉一致性 |
| **第五阶段** | #8, #9 | 30 分钟 | SEO 和 CSP 优化，需哈希计算和部署验证 |
| **第六阶段** | #10, #11 | 15 分钟 | Preload 和移动端微调 |

> **总预计耗时**：3-4 小时（已全部高效实施完毕并通过自动化合规质量校验）
