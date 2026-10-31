#!/usr/bin/env python3
"""资料包校验：按《数据格式与搜集规范》第 7 节完成验收做机器可判定部分。

用法：
    python3 02_资料与考据/validate_pack.py 1911 QING
    python3 02_资料与考据/validate_pack.py 1911          # 校验该年全部地区包
    python3 02_资料与考据/validate_pack.py               # 校验全库
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / '02_资料与考据'

CATEGORIES = {'events', 'survival_cost', 'law_identity', 'finance', 'technology_industry',
              'safety_medical', 'business_career', 'sports_culture', 'language'}
CORE = ['events', 'survival_cost', 'law_identity', 'finance', 'technology_industry']
CAT_CODE = {'events': 'EVENT', 'survival_cost': 'COST', 'law_identity': 'LAW', 'finance': 'FIN',
            'technology_industry': 'TECH', 'safety_medical': 'MED', 'business_career': 'BIZ',
            'sports_culture': 'SPORT', 'language': 'LANG'}
FACT_KEYS = ['id', 'year', 'region', 'category', 'fact', 'date', 'sources', 'verification', 'confidence']
OPP_KEYS = ['id', 'year', 'region', 'title', 'stage', 'opportunity_type', 'outcome', 'outcome_date',
            'hypothesis', 'based_on', 'time_window', 'requirements', 'steps', 'legal_then',
            'legal_today', 'risks', 'uncertainties', 'confidence']
SUMMARY_SECTIONS = ['任务范围', '核心发现', '主要机会', '后来者的成功', '来源冲突', '资料缺口', '主舞台建议']


def read_jsonl(path):
    records = []
    for n, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f'{path.name}:{n} JSON 解析失败 — {e}')
    return records


def check_pack(year, region):
    d = RESEARCH / str(year) / region
    issues = []
    for name in ('facts.jsonl', 'opportunities.jsonl', 'summary.md'):
        if not (d / name).is_file():
            issues.append(f'缺文件 {name}')
    if issues:
        return None, None, issues

    try:
        facts = read_jsonl(d / 'facts.jsonl')
        opps = read_jsonl(d / 'opportunities.jsonl')
    except ValueError as e:
        return None, None, [str(e)]

    summary = (d / 'summary.md').read_text(encoding='utf-8')

    fact_ids, seen = set(), set()
    for f in facts:
        fid = f.get('id', '<无 id>')
        miss = [k for k in FACT_KEYS if k not in f]
        if miss:
            issues.append(f'{fid} 缺字段 {miss}')
        if fid in seen:
            issues.append(f'ID 重复 {fid}')
        seen.add(fid)
        fact_ids.add(fid)
        if not re.fullmatch(rf'{year}-[A-Z][A-Z-]*-[A-Z]{{3,5}}-\d{{3}}', str(fid)):
            issues.append(f'{fid} ID 格式不符')
        if f.get('category') not in CATEGORIES:
            issues.append(f'{fid} category 非法：{f.get("category")}')
        elif f.get('category') in CAT_CODE and not str(fid).split('-')[-2] == CAT_CODE[f['category']]:
            issues.append(f'{fid} 类别缩写与 category 不一致')
        if f.get('verification') not in {'single_source', 'cross_checked', 'conflicted'}:
            issues.append(f'{fid} verification 非法：{f.get("verification")}')
        if f.get('confidence') not in {'high', 'medium', 'low'}:
            issues.append(f'{fid} confidence 非法：{f.get("confidence")}')
        reg = f.get('region') or {}
        if not all(k in reg for k in ('continent', 'country', 'city')):
            issues.append(f'{fid} region 缺 continent/country/city')
        srcs = f.get('sources') or []
        if not srcs:
            issues.append(f'{fid} 无 sources')
        for i, s in enumerate(srcs, 1):
            miss = [k for k in ('title', 'url', 'quote', 'accessed_at') if not s.get(k)]
            if miss:
                issues.append(f'{fid} source#{i} 缺 {miss}')
        if f.get('year') != year:
            issues.append(f'{fid} year 与目录不符')

    for o in opps:
        oid = o.get('id', '<无 id>')
        miss = [k for k in OPP_KEYS if k not in o]
        if miss:
            issues.append(f'{oid} 缺字段 {miss}')
        if oid in seen:
            issues.append(f'ID 重复 {oid}')
        seen.add(oid)
        if not re.fullmatch(rf'{year}-[A-Z][A-Z-]*-OPP-\d{{3}}', str(oid)):
            issues.append(f'{oid} ID 格式不符')
        if o.get('stage') not in {'survival', 'first_capital', 'wealth_jump'}:
            issues.append(f'{oid} stage 非法：{o.get("stage")}')
        t = o.get('opportunity_type')
        if t not in {'history_proven', 'inferred'}:
            issues.append(f'{oid} opportunity_type 非法：{t}')
        elif t == 'history_proven':
            if not o.get('outcome') or not o.get('outcome_date'):
                issues.append(f'{oid} history_proven 缺 outcome/outcome_date')
        else:
            if o.get('outcome') is not None or o.get('outcome_date') is not None:
                issues.append(f'{oid} inferred 的 outcome/outcome_date 必须为 null')
        for k in ('legal_then', 'legal_today'):
            if o.get(k) not in {'legal', 'gray', 'illegal', 'varies', 'unknown'}:
                issues.append(f'{oid} {k} 非法：{o.get(k)}')
        if not o.get('based_on'):
            issues.append(f'{oid} based_on 为空')
        if not o.get('risks'):
            issues.append(f'{oid} risks 为空')
        if not o.get('uncertainties'):
            issues.append(f'{oid} uncertainties 为空')
        for fref in o.get('based_on') or []:
            if fref not in fact_ids:
                issues.append(f'{oid} 引用不存在的事实 {fref}')

    cats = {f.get('category') for f in facts}
    missing_core = [c for c in CORE if c not in cats]
    if missing_core:
        noted = all(c.split('_')[0] in summary or c in summary for c in missing_core)
        if not noted:
            issues.append(f'五类核心缺 {missing_core}，且 summary 未说明')
        else:
            issues.append(f'[提示] 五类核心缺 {missing_core}，summary 已说明')

    for sec in SUMMARY_SECTIONS:
        if sec not in summary:
            issues.append(f'summary.md 缺小节「{sec}」')

    return len(facts), len(opps), issues


def main():
    args = sys.argv[1:]
    if len(args) >= 2:
        targets = [(int(args[0]), args[1])]
    else:
        targets = []
        for year_dir in sorted(RESEARCH.iterdir()):
            if not (year_dir.is_dir() or year_dir.name.isdigit()):
                continue
            for region_dir in sorted(year_dir.iterdir()):
                if region_dir.is_dir() and len(args) < 1 or (len(args) == 1 and year_dir.name == args[0]):
                    targets.append((int(year_dir.name), region_dir.name))
                    continue
                if region_dir.is_dir() and len(args) == 1 and year_dir.name != args[0]:
                    break

    total_f = total_o = 0
    bad = 0
    hard = 0
    for year, region in targets:
        nf, no, issues = check_pack(year, region)
        errors = [i for i in issues if not i.startswith('[提示]')]
        if errors:
            bad += 1
        hard += len(errors)
        total_f += nf or 0
        total_o += no or 0
        flag = 'OK  ' if not errors else 'FAIL'
        print(f'{flag} {year}/{region:<15} 事实 {nf if nf is not None else "-":>3}  机会 {no if no is not None else "-":>3}')
        for i in issues:
            print(f'      {i}')

    print(f'\n校验 {len(targets)} 个包：合格 {len(targets) - bad}，不合格 {bad}，错误 {hard} 条')
    print(f'合计事实 {total_f} 条，机会 {total_o} 条')
    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main())
