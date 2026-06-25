#!/usr/bin/env python3
"""
BlogOps v1.0 — AI 驱动的内容生产与发布系统

当前版本：本地质量检查 + 发布辅助
未来版本：接入 DeepSeek API 全自动 Pipeline

用法：
  python scripts/blogops.py check content/posts/xxx/index.md   # 质量检查
  python scripts/blogops.py new "文章标题" "分类"               # 生成空白文章模板
  python scripts/blogops.py slug "文章标题"                     # 生成拼音 slug
  python scripts/blogops.py status                              # 查看草稿状态
"""

import re
import sys
import yaml
import subprocess
import json
import os
import urllib.request
from pathlib import Path
from datetime import datetime

# Force stdout/stderr to use UTF-8 encoding to prevent UnicodeEncodeError / garbled output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "scripts" / "pipeline.yaml"


def load_config():
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def load_quality_checks():
    return yaml.safe_load(
        (ROOT / "scripts" / "rules" / "quality-checks.yaml").read_text(encoding="utf-8")
    )


def extract_body(content):
    """提取正文（去掉 front matter）"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        return match.group(2).strip()
    return content


def extract_frontmatter(content):
    """提取 front matter 为 dict"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def count_chinese_chars(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def count_code_blocks(text):
    """统计代码块数量"""
    return len(re.findall(r'^```', text, re.MULTILINE)) // 2


def has_tables(text):
    """检查是否有表格"""
    return bool(re.search(r'^\|.*\|.*\|', text, re.MULTILINE))


def has_lists(text):
    """检查是否有列表"""
    return bool(re.search(r'^[\s]*[-*+]\s', text, re.MULTILINE))


def to_slug(title):
    """将中文标题转为拼音 slug（简化版，取标题 hash 的前8位作为英文 slug）"""
    # 简化方案：移除特殊字符，转为短 slug
    slug = re.sub(r'[^\w\s-]', '', title)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = slug[:60].lower().strip('-')
    if not slug:
        slug = f"post-{datetime.now().strftime('%Y%m%d')}"
    return slug


def quality_check(article_path):
    """运行质量检查"""
    config = load_config()
    checks = load_quality_checks()
    path = Path(article_path)
    if not path.exists():
        print(f"❌ 文件不存在: {article_path}")
        return False

    content = path.read_text(encoding="utf-8")
    body = extract_body(content)
    fm = extract_frontmatter(content)

    errors = []
    warnings = []

    # 1. 字数检查
    word_count = count_chinese_chars(body)
    min_words = config["content_standards"]["min_word_count"]
    if word_count < min_words:
        errors.append(f"字数不足：{word_count} / {min_words}")
    else:
        print(f"✅ 字数：{word_count} / {min_words}")

    # 2. 代码块检查
    code_blocks = count_code_blocks(content)
    min_code = config["content_standards"]["min_code_blocks"]
    if code_blocks < min_code:
        errors.append(f"代码块不足：{code_blocks} / {min_code}")
    else:
        print(f"✅ 代码块：{code_blocks}")

    # 3. 表格/列表检查
    table_ok = has_tables(body)
    list_ok = has_lists(body)
    if not table_ok and not list_ok:
        warnings.append("缺少表格或列表")
    else:
        print(f"✅ 表格: {table_ok}, 列表: {list_ok}")

    # 4. Front matter 检查
    required = ["title", "summary", "date", "categories", "tags"]
    missing = [f for f in required if f not in fm]
    if missing:
        errors.append(f"Front matter 缺少字段：{', '.join(missing)}")
    else:
        print(f"✅ Front matter 完整")

    # 5. Summary 长度
    if "summary" in fm and fm["summary"]:
        if len(fm["summary"]) > 160:
            warnings.append(f"Summary 过长：{len(fm['summary'])} / 160")
        else:
            print(f"✅ Summary 长度：{len(fm['summary'])} / 160")

    # 6. Title 长度
    if "title" in fm and fm["title"]:
        if len(fm["title"]) > 60:
            warnings.append(f"Title 过长：{len(fm['title'])} / 60")
        else:
            print(f"✅ Title 长度：{len(fm['title'])} / 60")

    # 7. 残留标记检查
    if re.search(r'TODO|FIXME|待补充|内容开发中', body):
        errors.append("发现残留标记（TODO/FIXME/待补充/内容开发中）")
    else:
        print("✅ 无残留标记")

    # 8. 中英文空格检查
    if re.search(r'[\u4e00-\u9fff][A-Za-z]', body):
        warnings.append("存在中英文连写（缺少空格）")
    else:
        print("✅ 中英文空格正常")

    # 汇总
    print()
    if errors:
        print(f"❌ {len(errors)} 个错误（必须修复）：")
        for e in errors:
            print(f"   - {e}")
    if warnings:
        print(f"⚠️  {len(warnings)} 个警告（建议修复）：")
        for w in warnings:
            print(f"   - {w}")

    if not errors and not warnings:
        print("🎉 全部检查通过！可以发布。")

    return len(errors) == 0


def new_article(title, category):
    """生成空白文章模板草稿"""
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    slug = to_slug(title)
    
    # 草稿统一放置在 content/raw/ 目录下
    raw_dir = ROOT / "content" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    tags = config["taxonomy"]["tags_by_category"].get(category, [])[:3]
    tags_str = ", ".join(f'"{t}"' for t in tags)

    template = f"""---
title: "{title}"
summary: "待补充"
date: {today}
lastmod: {today}
draft: true
showtoc: true
categories: ["{category}"]
tags: [{tags_str}]
comments: true
---

## 为什么写这篇

待补充

## 正文

待补充

## 总结

待补充
"""
    draft_path = raw_dir / f"{slug}.md"
    draft_path.write_text(template, encoding="utf-8")
    print(f"✅ 已创建草稿模板：{draft_path}")
    print(f"   Slug: {slug}")
    print(f"   分类: {category}")
    print(f"   提示：可在该文件中撰写内容，完成后通过 git push 或运行 scripts/blogops.py process 发布。")
    return str(draft_path)


def show_status():
    """查看草稿状态"""
    posts_dir = ROOT / "content" / "posts"
    drafts = []
    published = []

    for md in sorted(posts_dir.rglob("index.md")):
        content = md.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)
        body = extract_body(content)

        title = fm.get("title", md.parent.name)
        is_draft = fm.get("draft", True)
        word_count = count_chinese_chars(body)
        code_blocks = count_code_blocks(content)

        entry = {
            "title": title,
            "path": str(md.relative_to(ROOT)),
            "words": word_count,
            "code": code_blocks,
            "date": str(fm.get("date", "N/A")),
        }
        if is_draft:
            drafts.append(entry)
        else:
            published.append(entry)

    print(f"📊 博客状态")
    print(f"   已发布：{len(published)} 篇")
    print(f"   草稿：{len(drafts)} 篇")
    print()

    if drafts:
        print("📝 草稿列表：")
        for d in drafts:
            print(f"   [{d['words']}字] {d['title']}")
            print(f"   → {d['path']}")

    if published:
        print("✅ 已发布：")
        for p in published:
            print(f"   [{p['words']}字] {p['title']} ({p['date']})")


def build_and_verify():
    """运行 hugo build 验证"""
    print("🔨 运行 hugo build...")
    result = subprocess.run(
        ["hugo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ Hugo build 成功")
        return True
    else:
        print("❌ Hugo build 失败：")
        print(result.stderr)
        return False


def process_article(file_path):
    """调用 DeepSeek API 润色并发布文章草稿"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 DEEPSEEK_API_KEY 环境变量！")
        return False

    path = Path(file_path)
    if not path.exists():
        print(f"❌ 错误：文件不存在: {file_path}")
        return False

    print(f"📖 正在读取草稿：{path}")
    raw_content = path.read_text(encoding="utf-8")

    # 系统提示词，用于指导 AI 润色与生成规范
    system_prompt = (
        "You are a professional blog editor and content optimization assistant.\n"
        "Your task is to polish the provided raw article draft and output the final publication-ready markdown. You must follow these requirements:\n"
        "1. Proofread and polish the Chinese text to make it fluent, professional, and clear.\n"
        "2. Ensure proper spacing between Chinese and English/numeric characters (e.g., 'C++' instead of 'C++' when connected to Chinese like '学习C++' -> '学习 C++').\n"
        "3. Retain all code blocks, tables, and lists. Fix formatting if needed.\n"
        "4. Do NOT leave any TODO, FIXME, or draft placeholders. Expand or clean them up.\n"
        "5. Output a structured YAML front matter at the top of the markdown, containing exactly the following keys:\n"
        "   - title: A polished, engaging title (under 60 characters)\n"
        "   - summary: A concise summary of the article (under 160 characters)\n"
        "   - date: Current date in YYYY-MM-DD format\n"
        "   - lastmod: Current date in YYYY-MM-DD format\n"
        "   - draft: false\n"
        "   - showtoc: true\n"
        "   - categories: A list containing 1 or 2 appropriate categories (e.g. ['算法竞赛', '系统开发', '硬件设计'])\n"
        "   - tags: A list containing 2 to 4 appropriate tags (e.g., ['C++', 'Linux', 'FPGA'])\n"
        "   - comments: true\n"
        "6. Also, output a special XML tag at the very end of your response: <slug>pinyin-slug-here</slug> where pinyin-slug-here is a clean, lowercase, hyphen-separated pinyin representation of the article's title (e.g., <slug>hugo-blog-optimization</slug> or <slug>acm-graph-algorithms</slug>).\n\n"
        "Output only the final markdown document containing the front matter, the body, and the <slug>...</slug> tag at the end."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": raw_content}
    ]

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.2
    }

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("🤖 正在调用 DeepSeek API 进行智能润色...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            ai_content = res_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"❌ 调用 API 失败: {e}")
        return False

    # 提取 Pinyin Slug
    slug_match = re.search(r"<slug>(.*?)</slug>", ai_content, re.DOTALL)
    if not slug_match:
        print("❌ 错误：AI 响应中未包含有效的 <slug>...</slug> 标签！")
        print("AI 原始响应片段：")
        print(ai_content[:500] + "...")
        return False

    slug = slug_match.group(1).strip().lower()
    # 格式化 Slug
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = slug.strip("-")
    if not slug:
        slug = f"post-{datetime.now().strftime('%Y%m%d')}"

    # 清除正文尾部的 <slug> 标签
    cleaned_content = re.sub(r"<slug>.*?</slug>", "", ai_content, flags=re.DOTALL).strip()

    # 确定输出发布路径（Option B：按文件夹分流归档）
    prefix_match = re.match(r"^(\d+-)", path.name)
    prefix = prefix_match.group(1) if prefix_match else ""

    fm = extract_frontmatter(cleaned_content)
    categories = fm.get("categories", [])
    
    category_folder = ""
    for cat in categories:
        if cat in ["算法", "ACM", "ACM算法", "算法竞赛"]:
            category_folder = "series-acm"
            break
        elif cat in ["安全", "安全相关", "信息安全", "Security"]:
            category_folder = "security"
            break
        elif cat in ["项目", "项目分析", "日常分析", "Project", "Analysis"]:
            category_folder = "project-analysis"
            break

    if category_folder:
        posts_dir = ROOT / "content" / "posts" / category_folder / f"{prefix}{slug}"
    else:
        posts_dir = ROOT / "content" / "posts" / f"{prefix}{slug}"

    posts_dir.mkdir(parents=True, exist_ok=True)
    output_path = posts_dir / "index.md"

    print(f"✍️ 正在写入正式发布文章：{output_path}")
    output_path.write_text(cleaned_content, encoding="utf-8")

    # 删除 content/raw 中的草稿文件
    print(f"🗑️ 正在删除草稿：{path}")
    path.unlink()

    print(f"🎉 文章已成功发布，Slug 为 '{slug}'！")
    return True


def main():
    if len(sys.argv) < 2:
        print("BlogOps v1.0")
        print()
        print("用法：")
        print("  python scripts/blogops.py check <路径>     # 质量检查")
        print("  python scripts/blogops.py new <标题> <分类> # 新建文章模板")
        print("  python scripts/blogops.py slug <标题>       # 生成 slug")
        print("  python scripts/blogops.py status            # 草稿状态")
        print("  python scripts/blogops.py build             # 验证构建")
        print("  python scripts/blogops.py process [路径]    # 自动润色并发布草稿")
        return

    cmd = sys.argv[1]

    if cmd == "check":
        if len(sys.argv) < 3:
            print("用法：python scripts/blogops.py check <文章路径>")
            return
        quality_check(sys.argv[2])

    elif cmd == "new":
        if len(sys.argv) < 4:
            print("用法：python scripts/blogops.py new <标题> <分类>")
            return
        new_article(sys.argv[2], sys.argv[3])

    elif cmd == "slug":
        if len(sys.argv) < 3:
            print("用法：python scripts/blogops.py slug <标题>")
            return
        print(to_slug(sys.argv[2]))

    elif cmd == "status":
        show_status()

    elif cmd == "build":
        build_and_verify()

    elif cmd == "process":
        if len(sys.argv) >= 3:
            process_article(sys.argv[2])
        else:
            print("🔍 未指定具体文章，正在扫描 content/raw/ 目录以批量处理草稿...")
            raw_dir = ROOT / "content" / "raw"
            draft_files = [f for f in raw_dir.rglob("*.md") if f.is_file() and not f.name.startswith(".")]
            if not draft_files:
                print("  未在 content/raw/ 下找到需要处理的文章草稿。")
                return
            
            print(f"  找到 {len(draft_files)} 篇草稿待处理。")
            success_count = 0
            for f in draft_files:
                if process_article(str(f)):
                    success_count += 1
            print(f"📊 批量处理完成，共 {success_count}/{len(draft_files)} 篇发布成功。")

    else:
        print(f"未知命令：{cmd}")


if __name__ == "__main__":
    main()
