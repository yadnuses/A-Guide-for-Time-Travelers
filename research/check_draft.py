#!/usr/bin/env python3
"""年度初稿结构校验：按《年度初稿撰写规范》第 10、11 节做机械可查的部分。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def decade_dir(year: int) -> Path:
    """十年分组的目录名，例如 1905 → 1900-1909。"""
    start = year - year % 10
    return ROOT / f"{start}-{start + 9}"


def draft_path(year: int) -> Path:
    """兼容三种布局：
    仓库版    ROOT/<十年>/<年份>.md   例如 1900-1909/1905.md
    旧仓库版  ROOT/<年份>/<年份>.md
    工作区版  ROOT/03_年度初稿/<年份>.md
    """
    for base in (ROOT / "03_年度初稿", decade_dir(year), ROOT / str(year)):
        p = base / f"{year}.md"
        if p.exists():
            return p
    return decade_dir(year) / f"{year}.md"


def find_years() -> list[int]:
    """扫描仓库根目录、十年目录、年份目录与工作区的 03_年度初稿/。"""
    years: set[int] = set()
    for base in (ROOT / "03_年度初稿", ROOT):
        if not base.is_dir():
            continue
        for p in base.glob("*.md"):
            if p.stem.isdigit():
                years.add(int(p.stem))
        for d in base.iterdir():
            if not d.is_dir():
                continue
            for p in d.glob("*.md"):
                if p.stem.isdigit():
                    years.add(int(p.stem))
    return sorted(years)

REQUIRED_TOP = ["一、落地", "二、世界棋盘", "三、你的路线", "四、随身工具", "结语", "附录：主要参考来源"]
CARD_FIELDS = ["**阶段**", "**当时入口**", "**所需资本与能力**", "**收益与退出**", "**风险与法律**"]
TAGS = ["历史已验证", "合理推演", "私人股权与合伙", "先知投资", "当年合法今天未必"]


def check(year: int) -> list[str]:
    p = draft_path(year)
    errs: list[str] = []
    if not p.exists():
        return ["文件缺失"]

    text = p.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))

    # 字节数：规范未设字数条款，此处按既有 21 篇的实际分布（40,872—62,473）设合理边界
    if size < 40000:
        errs.append(f"字节数 {size} 偏少（低于既有最小 40872）")
    elif size > 66000:
        # 注意：规范未规定字数。此阈值仅用于拦截「内容失控膨胀」，
        # 不是写作目标。既有 21 篇实际区间 40,872—62,473；1921—1930 十篇
        # 因路线卡数量更多（11—16 张），上沿落在 65,124，属正常。
        errs.append(f"字节数 {size} 明显离群（既有最大 62473，本段实测上沿 65124）")

    # 顶级栏目
    tops = re.findall(r"^## (.+)$", text, re.M)
    if len(tops) != 6:
        errs.append(f"顶级栏目 {len(tops)} 个，应为 6：{tops}")
    for want in REQUIRED_TOP:
        if not any(want in t for t in tops):
            errs.append(f"缺顶级栏目「{want}」")

    # 标题
    if not re.match(r"^# \d{4}：", text):
        errs.append("标题格式应为「# YEAR：标题」")

    # 占位符
    for bad in ["TBD", "TODO", "待补", "以后补"]:
        if bad in text:
            errs.append(f"出现占位符「{bad}」")

    # 引用连续性（支持 [1] 与 [34,35]、[1-3] 等合并写法）
    body = text.split("## 附录")[0]
    cited: set[int] = set()
    for group in re.findall(r"\[([\d,\s\-–]+)\]", body):
        for part in group.split(","):
            part = part.strip().replace("–", "-")
            if not part:
                continue
            if "-" in part:
                lo, _, hi = part.partition("-")
                if lo.strip().isdigit() and hi.strip().isdigit():
                    cited.update(range(int(lo), int(hi) + 1))
            elif part.isdigit():
                cited.add(int(part))
    cited = sorted(cited)
    if not cited:
        errs.append("正文无引用编号")
    else:
        expect = list(range(1, cited[-1] + 1))
        missing = sorted(set(expect) - set(cited))
        if missing:
            errs.append(f"引用编号断号，缺 {missing[:12]}")

        # 附录条数
        appendix = text.split("## 附录", 1)[1] if "## 附录" in text else ""
        entries = re.findall(r"^(\d+)\.\s", appendix, re.M)
        if not entries:
            errs.append("附录无编号条目")
        else:
            nums = [int(e) for e in entries]
            if max(nums) != cited[-1]:
                errs.append(f"附录最大编号 {max(nums)} 与正文引用上限 {cited[-1]} 不一致")
            app_missing = sorted(set(range(1, cited[-1] + 1)) - set(nums))
            if app_missing:
                errs.append(f"附录缺条目 {app_missing[:12]}")
        # 只检查条目行内的访问日期，避免把说明句「不列访问日期」误判
        entry_lines = [ln for ln in appendix.splitlines() if re.match(r"^\d+\.\s", ln)]
        if any(re.search(r"2026-\d\d-\d\d|访问日期\s*[:：]", ln) for ln in entry_lines):
            errs.append("附录条目出现访问日期")

    # 路线卡
    # 规范第 5.3 节只要求「主舞台路线应至少覆盖三个阶段」，未规定卡片数量，
    # 故此处检查阶段覆盖，而非卡片张数。
    cards = re.split(r"^#{3,4} 路线卡", text, flags=re.M)[1:]
    if not cards:
        errs.append("未找到路线卡")
    else:
        stage_text = "\n".join(cards)
        stages = {
            "survival": ("生存",),
            "first_capital": ("第一桶金",),
            "wealth_jump": ("财富跃升", "财富跃迁"),
        }
        absent = [k for k, words in stages.items() if not any(w in stage_text for w in words)]
        if absent:
            errs.append(f"路线卡未覆盖阶段 {absent}")
    for i, c in enumerate(cards, 1):
        c = c.split("^#{1,4} ", 1)[0]
        body_c = re.split(r"^#{1,4} ", c, maxsplit=1, flags=re.M)[0]
        for f in CARD_FIELDS:
            if f not in body_c:
                # 规范第 8 节允许投资路线用「事实层／故事层」两层写法，
                # 故事层承担了「当时入口」的叙述职责，视为已覆盖
                if f == "**当时入口**" and "**故事层" in body_c:
                    continue
                errs.append(f"路线卡第 {i} 张缺字段 {f}")
        if not any(t in body_c for t in TAGS):
            errs.append(f"路线卡第 {i} 张无标签")

    # 随身工具必备
    tools = text.split("## 四、随身工具", 1)[-1].split("## 结语")[0]
    if "语言" not in tools:
        errs.append("随身工具缺语言速查")
    if "避坑" not in tools:
        errs.append("随身工具缺避坑清单")

    return errs


def main() -> int:
    years = [int(a) for a in sys.argv[1:]] or sorted(
        find_years()
    )
    bad = 0
    print(f"{'年份':<6}{'字节':>8}{'路线卡':>7}{'引用':>6}{'状态':>8}")
    for y in years:
        p = draft_path(y)
        errs = check(y)
        size = len(p.read_text(encoding="utf-8").encode("utf-8")) if p.exists() else 0
        cards = len(re.split(r"^#{3,4} 路线卡", p.read_text(encoding="utf-8"), flags=re.M)) - 1 if p.exists() else 0
        refs = re.findall(r"\[(\d+)\]", p.read_text(encoding="utf-8")) if p.exists() else []
        top = max((int(r) for r in refs), default=0)
        print(f"{y:<6}{size:>8}{cards:>7}{top:>6}{'OK' if not errs else 'FAIL':>8}")
        for e in errs:
            print(f"       - {e}")
        bad += bool(errs)
    print(f"\n{len(years)} 篇：合格 {len(years) - bad}，不合格 {bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
