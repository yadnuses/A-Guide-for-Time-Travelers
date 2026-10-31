> **English** ｜ [中文](draft-spec.md)

# Annual Draft Specification

> **On language.** `research/check_draft.py` matches the six section headings **literally against the Chinese strings** listed in Section 2. Those headings are therefore kept in Chinese throughout this document, with an English gloss beside them for reading. If you write a draft, copy the Chinese headings exactly — an English heading will fail validation. The title, the lead-in, and all body prose are free-form; every existing guide in this repository happens to be in Chinese, but nothing in the validator requires that.

This document specifies how to turn an accepted annual research pack into a public-facing annual guide. A writer needs no other background. Read only:

1. this document;
2. `facts.jsonl`, `opportunities.jsonl`, and `summary.md` for each region under `research/YYYY/`;
3. where useful, existing finished drafts for style, for example [`1900-1909/1901.md`](../1900-1909/1901.md).

## 1. Deliverables

One file per year, placed in the decade folder that contains that year:

```text
YYYY-YYYY/YYYY.md
```

A decade folder covers ten consecutive years, for example `1900-1909/`, `1910-1919/`. For 1911, the path is `1910-1919/1911.md`. Do not modify the draft for any other year, or anything under `research/`.

## 2. Fixed structure

Organize every piece in the following order. **Do not split it into more top-level sections:**

```markdown
# YYYY：[适合该年的标题]

> **Demo v2｜第二人称故事化硬核指南**
>
> 引导语。

## 一、落地

## 二、世界棋盘

## 三、你的路线

## 四、随身工具

## 结语

## 附录：主要参考来源
```

The six headings are matched literally by the validator, so they stay in Chinese. For reading:

| Heading (copy this) | Meaning |
|:---|:---|
| `一、落地` | I. Landing |
| `二、世界棋盘` | II. The World Board |
| `三、你的路线` | III. Your Routes |
| `四、随身工具` | IV. What You Carry |
| `结语` | Closing |
| `附录：主要参考来源` | Appendix: Principal Sources |

The title line and the lead-in are yours to write; the bold strap-line under the title has read "Demo v2｜第二人称故事化硬核指南" in every guide so far, and may be adapted.

Facts, opportunities, risks, and sources all belong inside these four sections, the route cards, or the appendix. Do not open a new chapter for them.

## 3. Tone and narrative

Write in the second person, "you", but not as empty game narration:

- Open with one concrete scene that puts "you" inside that year's main stage.
- Write places, sounds, smells, prices, and institutional constraints, not grand events alone.
- The main stage carries a complete storyline; secondary focuses and opportunity cards stay short and specific.
- No success-guru slogans. Drive each route with concrete choices, capital, and risk.
- Do not package historical inequality as a cost-free shortcut to wealth.
- Humour is allowed, but it must not dissolve war, disaster, colonialism, discrimination, or labour risk.

## 4. Core setup

### 4.1 Time-travel conditions

- The reader is "you", arriving with modern knowledge and memory.
- You have no local papers, no modern equipment, and no credible modern identity.
- You carry a small, explainable amount of starting capital, by default roughly equal to 100 days' wages for an ordinary local worker.
- Starting capital guarantees nothing. It is only enough to fund your first risky commitment.

### 4.2 Year timeline

Each piece is an independent timeline. It opens from real history; personal action may produce local change, but a change in one piece is not required to affect another.

### 4.3 Foreknowledge

You may use future events, technologies, industries, and historical figures, but you must state plainly:

- whether they could be reached at the time;
- whether a legal or practical entry point existed;
- what capital, identity, capability, or connections it required;
- when to exit;
- what happens on failure.

A company succeeding later does not mean that buying its shares at any price at the time would have made money, and it does not mean an unlisted company could have been bought by an ordinary time traveler at the time.

## 5. How to write the four sections

### 5.1 I. Landing

State plainly:

- where you are, when you are, and what institutions you face;
- the identity, food and lodging, safety, and cash problems you must solve first;
- the first viable action on the main stage;
- the problems that forged papers, modern equipment, or an implausible protagonist halo cannot solve.

Do not write "empty-handed" as unrealistic invincible survival. Where the research pack gives no support, write it as an unverified limitation.

### 5.2 II. The World Board

Keep only global information that affects action:

- war, revolution, trade, finance, law, technology, disaster, popular culture;
- why regions outside the main stage are worth writing;
- which future outcomes could change a route.

Do not write a chronicle. Facts must come from the research pack; details you cannot verify go into risk or uncertainty.

### 5.3 III. Your Routes

This is the core of the piece. Use one standard route card per route:

```markdown
### Route card: [title]

**Stage**: survival / first_capital / wealth_jump.

**Entry point at the time**: what exactly you do, whom you approach, where you start.

**Capital and capability required**: cash, tools, identity, language, skill, channels, law.

**Returns and exit**: how cash flow or equity forms, and when you transfer, take dividends, buy back, or leave.

**Risk and law**: the ways it can fail, period law, differences from modern law, the moral boundary.

标签 (Tags): `历史已验证` / `合理推演` / `私人股权与合伙` / `先知投资` / `当年合法今天未必`

Tag glosses: `历史已验证` = historically proven · `合理推演` = reasoned inference · `私人股权与合伙` = private equity and partnership · `先知投资` = foresight investment · `当年合法今天未必` = legal then, not necessarily now. The tag names are written in the body text, not in the data files, so they are kept in Chinese to match the existing drafts; nothing in the validator checks them.
```

The main-stage route must cover at least three stages:

1. **Survive**: food and lodging, identity, safety, day labour, or basic supplies.
2. **First capital**: information, services, retail, supply, labour, publishing, or low-capital partnerships.
3. **Wealth jump**: private equity, partnerships, patents, industrial consolidation, underwriting, media, infrastructure, or resource trading.

Write short route cards for secondary-focus regions. An opportunity card carries one clear entry point and one clear risk, and nothing more.

### 5.4 IV. What You Carry

Put in only what the reader will actually use:

- an annual action calendar;
- a language quick reference;
- a pitfalls checklist;
- where necessary, a quick reference for wages, currency, and prices.

The language material covers emergency phrasing only. Do not turn it into a long language course. The pitfalls checklist must cover identity, cash, law, war, disaster, partnership, and differences from modern law.

## 6. Tag system

Tags attach to routes. They do not get a top-level section of their own.

### 6.1 `历史已验证` (historically proven)

For industry, company, product, organisation, or event routes that real historical outcomes later proved. Required:

- a matching `history_proven` opportunity record;
- outcomes drawn from real facts;
- an explanation of the gap between the outcome and the current action;
- no writing of a historical company's success as a return any individual could have earned.

### 6.2 `合理推演` (reasoned inference)

For routes where the research supports some of the conditions but history has not verified the outcome directly. Required:

- `outcome` and `outcome_date` are empty;
- the conditions for success and the conditions for failure are listed explicitly;
- no writing of possibility as certainty.

### 6.3 `私人股权与合伙` (private equity and partnership)

For unlisted companies, family firms, partnerships, contracting, supply, underwriting, licensing, and industrial services:

- state how money, resources, and labour convert into equity or cash flow;
- state control rights, dividends, buyback, dilution, and exit;
- invent no ticker symbols, share prices, dividends, or exchange trades.

### 6.4 `先知投资` (foresight investment)

For recognising in advance a person, company, industry, or institutional window that later succeeds. Four things are required:

1. who that person or company was at the time, and what they were still doing;
2. what vehicle was available to enter at the time;
3. what unique value you supplied;
4. what the exit and the failure are.

### 6.5 `当年合法今天未必` (legal then, not necessarily now)

For conduct that was legal or grey at the time and came under strict regulation later:

- explain the law and the social setting of the time;
- state why today is different;
- do not write it as practical advice;
- do not write fraud, forgery, injury, dangerous industry, or forced labour as viable shortcuts.

## 7. Citation rules

- Number citations consecutively in the body: `[1]`, `[2]`, `[3]`. Write combined citations as `[3,4]`.
- Each number maps to one fact record or one verified source.
- The appendix uses the format `1. **fact ID** — title: URL`, with numbers matching the body one to one.
- The appendix lists source titles and URLs only. **It shows no access dates.**
- A body citation must not point to a source that does not exist; `research/check_draft.py` checks numbering continuity and the number of appendix entries.
- Use two sources for important events wherever possible. A source conflict must appear in the body's boundary statements or in an appendix note.
- **`facts.jsonl` is the basis for facts; `opportunities.jsonl` is the basis for routes. Never add facts from memory.**

## 8. Requirements for investment routes

Investment text must be split into two layers:

### 8.1 The fact layer

- the real outcomes for the company, product, industry, market, and institutions;
- whether it was listed at the time, whether you could take a stake, and whether prices and trading channels existed;
- the dates and sources of later outcomes.

### 8.2 The story layer

- how "you" trade knowledge, capability, orders, partnership, or service for the right to enter;
- how you obtain cash flow, equity, licence fees, or control;
- how you carry dilution, failure, war, policy, and identity risk.

**Prohibited:**

- inventing public share prices;
- inventing price moves, buy and sell dates, and returns;
- writing "it succeeded later" as "any investment succeeded";
- applying modern financial products straight onto an old regime;
- writing a grey or violent historical opportunity as a modern recommendation.

## 9. Handling research gaps

Gaps in the pack's `summary.md` must be handled honestly in the finished draft:

- do not delete the difficulty;
- do not replace missing data with vague common sense;
- where prices are missing, write "by reference to a nearby region or year" and say that it is an approximation;
- where listing prices are missing, write private equity, partnership, service, or industry entry points only;
- where the legal text is missing, write only the legal risk that the existing facts support;
- where sources conflict, present both readings and explain why you did not force them into one.

## 10. Pre-writing checklist

- [ ] Only this year's research pack and confirmed cross-region material are used.
- [ ] The main stage, secondary focuses, and opportunity cards match the coverage of the research pack.
- [ ] All four top-level sections are present, plus the closing and the appendix.
- [ ] Every route card carries the five fixed fields.
- [ ] `history_proven` routes carry real later outcomes.
- [ ] `inferred` routes do not state outcomes as fact.
- [ ] Entry into private equity, partnership, service, and underwriting is stated explicitly.
- [ ] No invented share prices, dividends, ticker symbols, or returns.
- [ ] Every fact traces back to `facts.jsonl`.
- [ ] Body citations run continuously, and appendix sources map one to one.
- [ ] The appendix carries no access dates.
- [ ] A language quick reference and a pitfalls checklist are present.
- [ ] Boundary warnings cover war, disaster, identity, cash, law, and differences from modern law.

## 11. Post-delivery checklist

- [ ] The Markdown heading structure is correct.
- [ ] No dangling numbers in the body, and no uncited numbers in the appendix.
- [ ] No `TBD`, `TODO`, placeholders, or invented "to be added later".
- [ ] No fabricated citations, prices, relationships between people, or historical outcomes.
- [ ] No other year's file is modified.
- [ ] `python3 research/check_draft.py YYYY` has been run and passes.
