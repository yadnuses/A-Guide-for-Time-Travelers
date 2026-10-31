#!/usr/bin/env python3
"""跨年份引用检查。

《年度初稿撰写规范》要求每篇只使用本年度资料包；实际写作中出现过借用相邻
年份事实作为物价锚点的情况（如 1901 年缺生存成本时引用 1900 年数据）。
这类借用若在正文标注了年份、且附录如实列出，可视作允许的降级处理，
但必须在审校记录中登记。本脚本把全部跨年引用列出来，供人工判断。
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / '03_年度初稿'
ID_RE = re.compile(r'\b(\d{4})-([A-Z][A-Z-]*)-([A-Z]+)-(\d{3})\b')

total = 0
for path in sorted(DRAFTS.glob('*.md')):
    year = path.stem
    text = path.read_text(encoding='utf-8')
    foreign = defaultdict(list)
    for m in ID_RE.finditer(text):
        if m.group(1) != year:
            line = text.count('\n', 0, m.start()) + 1
            foreign[m.group(0)].append(line)
    if not foreign:
        print(f'{year}  无跨年引用')
        continue
    total += len(foreign)
    print(f'{year}  跨年引用 {len(foreign)} 条：')
    for fid, lines in sorted(foreign.items()):
        print(f'    {fid}  出现在第 {lines} 行')

print(f'\n合计跨年引用 {total} 条')
