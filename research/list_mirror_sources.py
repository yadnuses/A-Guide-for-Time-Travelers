#!/usr/bin/env python3
"""列出引用了维基镜像站/代理站的记录，供后续替换来源。

背景：部分记录在搜集时只能取到维基镜像站（wikiwand、wiki2、us-wikipedia 等）
而非维基原始条目或一手档案。镜像站内容通常对应真实条目，但来源等级低于
原始条目，需登记待替换为一手档案或官方统计。

用法：
    python3 research/list_mirror_sources.py            # 列出全部
    python3 research/list_mirror_sources.py 1911        # 只看某年
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MIRROR = [
    'wikiwand', 'wiki2.', 'us-wikipedia', 'wikiredia', 'restivo.info',
    'translate.goog', 'wikipedia.com/', 'wikipedia.wiki', 'dbpedia.org',
    'handwiki', 'alchetron', 'britastro', 'everything.explained',
]


def is_mirror(url):
    u = (url or '').lower()
    return any(m in u for m in MIRROR)


def main():
    year_filter = sys.argv[1] if len(sys.argv) > 1 else None
    offenders = defaultdict(list)
    by_year = Counter()
    total_records = 0

    for path in sorted(ROOT.rglob('facts.jsonl')):
        year_dir = path.relative_to(ROOT).parts[0]
        if year_filter and year_dir != year_filter:
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            total_records += 1
            r = json.loads(line)
            bad = [s for s in (r.get('sources') or []) if is_mirror(s.get('url'))]
            if bad:
                rel = f'{path.relative_to(ROOT).parent.as_posix()}'
                offenders[rel].append((r['id'], bad))
                by_year[year_dir] += 1

    for pack in sorted(offenders):
        items = offenders[pack]
        clean = sum(1 for i, s in items if len(s) < len([x for x in s]) )
        print(f'\n{pack}  —— {len(items)} 条记录含镜像来源')
        for rid, srcs in items:
            for s in srcs:
                print(f"    {rid:<28} {s.get('title','')[:40]:<42} {s.get('url','')[:78]}")

    print('\n=== 按年份统计 ===')
    for y in sorted(by_year):
        print(f'  {y}: {by_year[y]} 条')
    print(f'\n合计 {sum(by_year.values())} 条记录含镜像来源，占本次统计 {total_records} 条事实的 '
          f'{sum(by_year.values()) / total_records * 100:.1f}%')


if __name__ == '__main__':
    main()
