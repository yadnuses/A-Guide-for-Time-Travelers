#!/usr/bin/env python3
"""年度初稿机器层校验。

按《年度初稿撰写规范》第 7、10、11 节的硬性条款做机器可判定部分的检查，
输出两份结果：
  1. 控制台摘要（供人工快速定位）
  2. JSON 明细（供审校报告引用）

用法：
    python3 check_drafts.py            # 检查全部
    python3 check_drafts.py 1900 1901  # 只检查指定年份
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / '03_年度初稿'
RESEARCH = ROOT / '02_资料与考据'

# 规范要求的四个固定板块 + 结语 + 附录
REQUIRED_SECTIONS = ['一、落地', '二、世界棋盘', '三、你的路线', '四、随身工具', '结语', '附录']
ROUTE_CARD_FIELDS = ['阶段', '当时入口', '所需资本与能力', '收益与退出', '风险与法律']
TAGS = ['历史已验证', '合理推演', '私人股权与合伙', '先知投资', '当年合法今天未必', '当年可以']
PLACEHOLDERS = ['TBD', 'TODO', 'XXX', '待补', '此处省略', '此处待补']
ACCESS_DATE = re.compile(r'(访问日期|accessed[_\s]*(at|on)|检索于|2026-10-3[01])', re.I)


def strip_code(text):
    """去掉代码块，避免把示例里的 [1] 当成正文引用。"""
    return re.sub(r'```.*?```', '', text, flags=re.S)


def load_research_ids():
    """收集全库事实 ID 与机会 ID，用于校验正文引用是否有据。"""
    fact_ids, opp_ids = set(), set()
    for path in RESEARCH.rglob('*.jsonl'):
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            (fact_ids if path.name == 'facts.jsonl' else opp_ids).add(rec.get('id'))
    return fact_ids, opp_ids


def split_appendix(text):
    """返回 (正文, 附录)。附录以最后一个 '## 附录' 开头。"""
    marks = [m.start() for m in re.finditer(r'^## 附录', text, re.M)]
    if not marks:
        return text, ''
    return text[:marks[-1]], text[marks[-1]:]


def check_one(path, fact_ids, opp_ids):
    raw = path.read_text(encoding='utf-8')
    text = strip_code(raw)
    body, appendix = split_appendix(text)
    name = path.name
    issues = []

    # --- 结构 ---
    h2 = re.findall(r'^## (.+)$', text, re.M)
    if len(h2) != 6:
        issues.append(('结构', 'error', f'顶级栏目 {len(h2)} 个，规范要求 6 个：{h2}'))
    seen = {}
    for title in h2:
        key = title.split('：')[0].split(':')[0].strip()
        seen[key] = seen.get(key, 0) + 1
    for key, cnt in seen.items():
        if cnt > 1:
            issues.append(('结构', 'error', f'顶级栏目编号重复：「{key}」出现 {cnt} 次'))
    for want in REQUIRED_SECTIONS:
        if not any(want in t for t in h2):
            issues.append(('结构', 'error', f'缺少必备板块「{want}」'))

    # --- 引用编号 ---
    # 支持 [1]、[14,15]、[19, 20, 21]、[4,5,6]，以及 [12-15]、[12—15] 区间写法
    cited = []
    ranged = []
    for group in re.findall(r'\[(\d+(?:\s*[,，\-—–]\s*\d+)*)\]', body):
        for part in re.split(r'\s*[,，]\s*', group):
            span = re.match(r'^(\d+)\s*[\-—–]\s*(\d+)$', part)
            if span:
                lo, hi = int(span.group(1)), int(span.group(2))
                if lo <= hi:
                    cited.extend(range(lo, hi + 1))
                    ranged.append(f'{lo}-{hi}')
                else:
                    issues.append(('引用', 'error', f'区间引用起止颠倒：{part}'))
            elif part.isdigit():
                cited.append(int(part))
    if ranged:
        issues.append(('引用', 'warn', f'使用区间引用写法 {ranged}，规范要求逐个编号展开'))
    cited_set = set(cited)
    app_nums = [int(n) for n in re.findall(r'^(\d+)\.\s', appendix, re.M)]
    app_set = set(app_nums)

    dangling = sorted(cited_set - app_set)
    if dangling:
        issues.append(('引用', 'error', f'悬空引用（正文有、附录无）：{dangling}'))
    unused = sorted(app_set - cited_set)
    if unused:
        issues.append(('引用', 'error', f'未引用编号（附录有、正文无）：{unused}'))
    if app_nums and app_nums != list(range(1, len(app_nums) + 1)):
        issues.append(('引用', 'error', f'附录编号不连续：{app_nums}'))
    if cited and max(cited) > len(app_nums):
        issues.append(('引用', 'error', f'正文最大引用 [{max(cited)}] 超出附录条数 {len(app_nums)}'))
    # 同一编号被多次引用是正常写法（同一事实支撑多处论述），仅统计不报错
    repeat_ratio = (len(cited) - len(cited_set)) / len(cited) if cited else 0

    # --- 附录来源 ID ---
    ids_in_app = re.findall(r'\b(\d{4}-[A-Z][A-Z-]*-[A-Z]+-\d{3})\b', appendix)
    dup_ids = sorted({i for i in ids_in_app if ids_in_app.count(i) > 1})
    if dup_ids:
        issues.append(('来源', 'error', f'附录来源事实 ID 重复：{dup_ids}'))
    unknown = sorted({i for i in ids_in_app if i not in fact_ids and i not in opp_ids})
    if unknown:
        issues.append(('来源', 'error', f'附录来源 ID 在资料库中不存在：{unknown}'))

    # --- 路线卡字段 ---
    cards = re.findall(r'^###+ .*?路线卡.*?$', text, re.M)
    card_blocks = re.split(r'^###+ .*?路线卡.*?$', text, flags=re.M)[1:]
    for i, block in enumerate(card_blocks, 1):
        head = cards[i - 1].strip('# ').strip()
        missing = [f for f in ROUTE_CARD_FIELDS if f'**{f}**' not in block and f not in block]
        if missing:
            issues.append(('路线卡', 'warn', f'「{head}」缺字段：{missing}'))

    # --- 工具板块必备件 ---
    for want, label in [('年度行动日历', '年度行动日历'), ('语言速查', '语言速查'), ('避坑清单', '避坑清单')]:
        if want not in text:
            issues.append(('工具', 'warn', f'缺少「{label}」'))

    # --- 占位符与访问日期 ---
    for token in PLACEHOLDERS:
        if token in text:
            issues.append(('占位符', 'error', f'出现占位符「{token}」'))
    if ACCESS_DATE.search(appendix):
        issues.append(('来源', 'error', '附录出现访问日期'))

    # --- 标签 ---
    used_tags = [t for t in TAGS if t in text]
    if not used_tags:
        issues.append(('标签', 'warn', '未使用任何规范标签'))

    return {
        'file': name,
        'chars': len(raw),
        'sections': h2,
        'citations': len(cited),
        'appendix': len(app_nums),
        'cards': len(cards),
        'tags': used_tags,
        'issues': issues,
    }


def main():
    targets = sys.argv[1:] or None
    fact_ids, opp_ids = load_research_ids()
    files = sorted(DRAFTS.glob('*.md'))
    if targets:
        files = [f for f in files if f.stem in targets]

    results, total_err, total_warn = [], 0, 0
    for path in files:
        res = check_one(path, fact_ids, opp_ids)
        results.append(res)
        errs = [i for i in res['issues'] if i[1] == 'error']
        warns = [i for i in res['issues'] if i[1] == 'warn']
        total_err += len(errs)
        total_warn += len(warns)
        flag = 'OK  ' if not errs and not warns else ('FAIL' if errs else 'WARN')
        print(f"{flag} {path.stem}  字符 {res['chars']:>6}  栏目 {len(res['sections'])}  "
              f"引用 {res['citations']:>3}  附录 {res['appendix']:>3}  路线卡 {res['cards']}")
        for kind, level, msg in res['issues']:
            print(f"      [{level}] {kind}: {msg}")

    print(f"\n合计 {len(results)} 篇：error {total_err}，warn {total_warn}")
    print(f"资料库可引用：事实 {len(fact_ids)} 条，机会 {len(opp_ids)} 条")

    out = ROOT / '04_审校与修订' / 'machine_check.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'明细已写入 {out.relative_to(ROOT)}')
    return 1 if total_err else 0


if __name__ == '__main__':
    sys.exit(main())
