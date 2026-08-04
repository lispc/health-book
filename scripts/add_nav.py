#!/usr/bin/env python3
"""给 book/ 下所有章节文件追加「上一章 / 返回目录 / 下一章」导航页脚。

幂等：已存在的导航块（<!-- chapter-nav --> 标记到文件结尾）会先被移除再重新生成。
新增、删除、重命名章节后重新运行 `make nav` 即可。
"""
import re
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent / "book"
NAV_MARK = "<!-- chapter-nav -->"


def chapter_title(path: Path) -> str:
    """取文件第一个一级标题作为章节名，去掉「第N章」前缀。"""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            title = m.group(1).strip()
            return re.sub(r"^(第\d+章|前言|结语|附录)\s*", "", title)
    return path.stem


def main() -> int:
    files = sorted(BOOK_DIR.glob("*.md"))
    if not files:
        print("book/ 下没有找到 md 文件", file=sys.stderr)
        return 1

    for i, path in enumerate(files):
        text = path.read_text(encoding="utf-8")
        # 移除旧导航块（幂等）
        if NAV_MARK in text:
            text = text[: text.index(NAV_MARK)].rstrip() + "\n"

        parts = []
        if i > 0:
            prev = files[i - 1]
            parts.append(f"[← 上一章：{chapter_title(prev)}]({prev.name})")
        parts.append("[返回目录](../index.md)")
        if i < len(files) - 1:
            nxt = files[i + 1]
            parts.append(f"[下一章：{chapter_title(nxt)} →]({nxt.name})")

        nav = f"\n{NAV_MARK}\n\n---\n\n{' &nbsp;|&nbsp; '.join(parts)}\n"
        path.write_text(text.rstrip() + "\n" + nav, encoding="utf-8")
        print(f"导航已更新: {path.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
