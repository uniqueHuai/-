#!/usr/bin/env python3
"""将 Obsidian 笔记中的独占语法转为 GitHub 兼容格式"""

import re
import os

# 要修复的文件列表（可以根据需要添加）
files_to_fix = [
    "java学习篇/Java基础与进阶篇.md",
]

# Callout 类型映射
CALLOUT_MAP = {
    "info": "NOTE",
    "tip": "TIP",
    "warning": "WARNING",
    "danger": "CAUTION",
    "success": "IMPORTANT",
    "question": "IMPORTANT",
    "failure": "CAUTION",
    "bug": "CAUTION",
    "example": "TIP",
}

def fix_callouts(content):
    """修复 Obsidian Callout 语法"""

    def replace_callout(match):
        indent = match.group(1) or ""
        callout_type = match.group(2).lower()
        rest = match.group(3)  # 可能为 None 或空字符串

        github_type = CALLOUT_MAP.get(callout_type, "NOTE")

        if rest and rest.strip():
            # 内容在同一行：> [!info] 内容
            # 拆成两行：> [!NOTE]\n> 内容
            return f"{indent}> [!{github_type}]\n{indent}> {rest.strip()}"
        else:
            # 没有内容：> [!info]
            return f"{indent}> [!{github_type}]"

    # 匹配行首的 > [!xxx] 语法（可能有缩进）
    pattern = r'(^|\n)(\s*)> \[!(\w+)\](.*?)$'
    content = re.sub(pattern, replace_callout, content, flags=re.MULTILINE)
    return content

def fix_wikilinks(content):
    """将 [[WikiLink]] 转为标准 Markdown 链接"""

    def replace_wikilink(match):
        link_text = match.group(1)
        # 处理带别名的链接 [[目标|别名]]
        if "|" in link_text:
            target, alias = link_text.split("|", 1)
        else:
            target = link_text
            alias = link_text

        # 确保有 .md 后缀
        if not target.endswith(".md"):
            target = target + ".md"

        return f"[{alias}](./{target})"

    content = re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, content)
    return content

def main():
    vault_root = "D:/文档/Obsidian Vault"

    for rel_path in files_to_fix:
        full_path = os.path.join(vault_root, rel_path)
        if not os.path.exists(full_path):
            print(f"❌ 文件不存在: {rel_path}")
            continue

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # 1. 修复 Callout
        content = fix_callouts(content)

        # 2. 修复 Wiki 链接
        content = fix_wikilinks(content)

        if content == original:
            print(f"✅ 无需修改: {rel_path}")
            continue

        # 写回文件
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 统计修改
        callout_count = content.count("> [!")
        old_callouts = sum(1 for t in CALLOUT_MAP.keys() if f"> [!{t}]" in original.lower())
        print(f"✅ 已修复: {rel_path}")
        print(f"   - Callout 转换: {old_callouts} 处")
        print(f"   - WikiLink 转换: {len(re.findall(r'\[\[([^\]]+)\]\]', original))} 处")

if __name__ == "__main__":
    main()
