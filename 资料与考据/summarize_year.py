#!/usr/bin/env python3
"""按年份汇总资料包规模，用于批次验收。

用法：
    python3 02_资料与考据/summarize_year.py 1911 1920
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def year_stats(year):
    year_dir = ROOT / str(year)
    if not year_dir.is_dir():
        return None
    packs = sorted(p for p in year_dir.iterdir() if p.is_dir())
    facts = opps = hp = 0
    cats = defaultdict(int)
    regions = []
    for pack in packs:
        regions.append(pack.name)
        fpath, opath = pack / 'facts.jsonl', pack / 'opportunities.jsonl'
        if fpath.is_file():
            for line in fpath.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    r = json.loads(line)
                    facts += 1
                    cats[r.get('category')] += 1
        if opath.is_file():
            for line in opath.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    r = json.loads(line)
                    opps += 1
                    if r.get('opportunity_type') == 'history_proven':
                        hp += 1
    return {'packs': len(packs), 'regions': regions, 'facts': facts,
            'opps': opps, 'hp': hp, 'cats': dict(cats)}


def main():
    args = sys.argv[1:]
    if len(args) >= 2:
        years = range(int(args[0]), int(args[1]) + 1)
    elif len(args) == 1:
        years = [int(args[0])]
    else:
        years = sorted(int(p.name) for p in ROOT.iterdir()
                       if p.is_dir() and p.name.isdigit())

    tf = to = th = 0
    print(f"{'年份':<6}{'包':>3}{'事实':>6}{'机会':>6}{'已验证':>7}   五类核心")
    for y in years:
        s = year_stats(y)
        if not s:
            print(f'{y:<6}{"-":>3}{"-":>6}{"-":>6}{"-":>7}   未开始')
            continue
        core = sum(1 for c in ('events', 'survival_cost', 'law_identity', 'finance', 'technology_industry')
                   if s['cats'].get(c))
        tf += s['facts']; to += s['opps']; th += s['hp']
        print(f"{y:<6}{s['packs']:>3}{s['facts']:>6}{s['opps']:>6}{s['hp']:>7}   {core}/5")
    print(f"{'合计':<6}{'':>3}{tf:>6}{to:>6}{th:>7}")


if __name__ == '__main__':
    main()
