> **English** ｜ [中文](data-spec.md)

# Data Format Specification

This document defines the fields, enums, naming and acceptance criteria for every fact record and opportunity record under `research/`. Read it to the end before submitting a research pack to the repository; the machine validation script implements exactly the clauses in Section 7.

## 1. Collection Principles

1. **Keep facts and inference apart.** Verifiable facts go into `facts.jsonl`; survival and money-making inference go into `opportunities.jsonl`. Never mix the two.
2. **One source, one quote.** Every fact has at least one reliable source, and keeps the source title, a specific link or bibliographic reference, the passage supporting that fact, and the access date. The quote must actually appear in the source.
3. **Two sources for critical facts.** For event dates, legal status, prices, financial outcomes and match results that affect the main route, cross-check with a second independent source wherever possible, and mark the result honestly in `verification`.
4. **Never fabricate.** Do not invent sources, quotes, data or historical outcomes. Anything you cannot confirm goes into the research gaps in `summary.md`; never dress it up as fact.
5. **One pack per submission.** A commit touches only the year×region you claimed, and modifies no other directory.

## 2. Directories and Task Units

One task is one "year×region" and occupies one directory:

```text
research/
└── YYYY/
    ├── REGION/
    │   ├── facts.jsonl
    │   ├── opportunities.jsonl
    │   └── summary.md
    └── global/
        ├── facts.jsonl
        ├── opportunities.jsonl
        └── summary.md
```

- `YYYY` is a four-digit year, e.g. `1910`.
- `REGION` should preferably be an uppercase ISO 3166-1 alpha-2 country or territory code, e.g. `FR`, `US`, `GB`. For historical polities, or areas with no contemporary code, use a clear uppercase English name, e.g. `OTTOMAN`. The same code must be used consistently within a project.
- `global/` holds cross-region annual overview records only, and should be written after that year's regional tasks are done.
- Each task writes only its own three files.

## 3. Data Categories

| English enum | Name | Requirement |
|:---|:---|:---|
| `events` | event calendar | Core; major events, exact dates and action windows |
| `survival_cost` | cost of living | Core; currency, prices, wages, food and lodging, transport |
| `law_identity` | law and identity | Core; documents, law enforcement, trade access, legal grey areas |
| `finance` | financial opportunity | Core; stocks, bonds, exchange rates, gold, real estate and banking systems |
| `technology_industry` | technology and industry | Core; existing technology, emerging technology, patents and industry booms |
| `safety_medical` | safety and medical | As needed; war, disasters, public order, disease and medical conditions |
| `business_career` | business and career | As needed; scarce skills, employment, trade and startup opportunities |
| `sports_culture` | sports and culture | As needed; match results, popular culture, publishing and betting opportunities |
| `language` | language quick reference | As needed; emergency phrases and common local wording |

All five "Core" categories are mandatory. For a category that genuinely does not exist, explain the search process and the evidence gap in `summary.md`; the validation script will warn but not block.

## 4. `facts.jsonl`

One complete JSON object per line. No Markdown code fences, no comments, no trailing commas, and do not wrap it in an array. **One object states exactly one independently verifiable fact.**

```json
{"id":"1900-FR-EVENT-001","year":1900,"region":{"continent":"Europe","country":"France","city":"Paris"},"category":"events","fact":"A statement of fact that can be verified independently","date":"1900-04-14","sources":[{"title":"Source title","url":"Specific link or bibliographic reference","quote":"The passage from the source that supports this fact","accessed_at":"2026-10-30"}],"verification":"single_source","confidence":"high"}
```

(The original wrote the descriptive values in this example in Chinese; they are given in English here. Field names, IDs and enum values are unchanged.)

### Required Fields

| Field | Description |
|:---|:---|
| `id` | `YYYY-REGION-category abbreviation-three-digit serial`, unique across the project |
| `year` | Four-digit integer year; must match the directory it sits in |
| `region` | Contains `continent`, `country`, `city`; for global records, `country` and `city` are `null` |
| `category` | One of the nine English enums in Section 3 |
| `fact` | State only the fact; no advice, no return forecasts, no value judgements |
| `date` | `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or `start date/end date`; `null` when not applicable |
| `sources` | At least one item, each with `title`, `url`, `quote`, `accessed_at`; for a printed book, put the full bibliographic details and page numbers in `url` |
| `verification` | `single_source`, `cross_checked` or `conflicted` |
| `confidence` | `high`, `medium`, `low`: how solid the evidence is, not how good the story is |

### Category Abbreviations

| Category | Abbreviation | Category | Abbreviation |
|:---|:---|:---|:---|
| `events` | `EVENT` | `safety_medical` | `MED` |
| `survival_cost` | `COST` | `business_career` | `BIZ` |
| `law_identity` | `LAW` | `sports_culture` | `SPORT` |
| `finance` | `FIN` | `language` | `LANG` |
| `technology_industry` | `TECH` | | |

### On `conflicted`

When sources contradict each other, set `verification` to `conflicted`, list both versions under multiple `sources`, and keep them side by side in `fact`, e.g. "source A records X, source B records Y". **Do not flatten the disagreement for the sake of tidiness** — readers are entitled to see the inconsistency in the evidence itself.

## 5. `opportunities.jsonl`

One complete JSON object per line. Every opportunity must reference at least one existing fact ID through `based_on`.

```json
{"id":"1900-FR-OPP-001","year":1900,"region":{"continent":"Europe","country":"France","city":"Paris"},"title":"Opportunity name","stage":"first_capital","opportunity_type":"inferred","outcome":null,"outcome_date":null,"hypothesis":"Why this route might work","based_on":["1900-FR-EVENT-001"],"time_window":"The window in which action is possible","requirements":["Conditions needed to start"],"steps":["Action steps in the inference"],"legal_then":"gray","legal_today":"illegal","risks":["Main risks"],"uncertainties":["What is unconfirmed or needs further checking"],"confidence":"medium"}
```

### Field Constraints

| Field | Description |
|:---|:---|
| `id` | `YYYY-REGION-OPP-three-digit serial`, unique across the project |
| `stage` | `survival`, `first_capital`, `wealth_jump` |
| `opportunity_type` | `history_proven` (later confirmed by real outcomes) or `inferred` (inference not yet confirmed) |
| `outcome` | Required for `history_proven`: the concrete successful outcome; must be `null` for `inferred` |
| `outcome_date` | When the outcome happened, same format as `date`; must be `null` for `inferred` |
| `hypothesis` | Explain the causal logic; "profit from an information gap" alone is not enough |
| `based_on` | Array of fact IDs; must not be empty, and every referenced ID must actually exist |
| `time_window` | The window in which action is possible; write `unknown` when unknown and explain in `uncertainties` |
| `requirements` / `steps` / `risks` / `uncertainties` | Arrays of strings; use an empty array when there is nothing to say, but never drop a critical unknown |
| `legal_then` / `legal_today` | `legal`, `gray`, `illegal`, `varies`, `unknown`; use `varies` when modern jurisdictions differ |
| `confidence` | `high`, `medium`, `low`: how credible the route is |

Inference may be bold, but never delete the constraints: startup cost, legal risk, market size, identity limits, memory error. **Do not put an exact profit figure on a return that has no factual basis.** A company succeeding later does not mean any price at the time was profitable, nor that the company was already listed then.

## 6. `summary.md`

Organise it in the following order, keeping the headings as written:

```markdown
# YYYY×REGION 资料摘要

## 任务范围
The areas, time span and data categories actually covered.

## 核心发现
The most important fact IDs and what they mean; do not copy them into the body.

## 主要机会
Opportunity ID, type, stage and a one-sentence conclusion.

## 后来者的成功，当下的财富
Every `history_proven` opportunity: the real outcome that followed, the channels open at the time, the execution constraints that still apply; if none, write "no route with sufficient evidence".

## 来源冲突
Contradictions between sources and the basis for handling them now; if none, write "none found".

## 资料缺口
What could not be verified and how it affects the routes; if none, write "none found".

## 主舞台建议
Whether the region is suitable as the year's main stage, with reasons.
```

The seven headings are matched literally against Chinese strings by `research/validate_pack.py`, so they stay in Chinese — an English heading will be reported as a missing subsection. The explanatory lines beneath each heading are prose and may be in any language, though every existing summary happens to be in Chinese.

## 7. Acceptance Criteria

The machine validation script `research/validate_pack.py` checks the first seven items one by one; the eighth is reviewed by hand:

1. All three files exist, and every JSONL line parses with a standard JSON parser.
2. All required fields are present, enum values are legal, and the `id` format matches its directory and `category`.
3. All fact IDs and opportunity IDs are unique within the pack, and every `based_on` reference resolves.
4. `history_proven` carries a concrete `outcome`, `outcome_date` and fact references proving that outcome; for `inferred`, both outcome fields are `null`.
5. All five core categories have been collected, or the gap is explained in the summary.
6. `summary.md` has all seven subsections.
7. Every fact has at least one complete source, and `legal_*`, `risks` and `uncertainties` are not left blank to dodge the check.
8. **Manual review**: whether `quote` really supports the statement in `fact`, and whether the source tier clears the bar.

## 8. Source Tiers

Judge by the following tiers at review; the lower the tier, the more justification is needed:

| Tier | Type | Handling |
|:---|:---|:---|
| Primary | government gazettes, statistical yearbooks, contemporary newspapers, archives, legal texts | highest priority |
| Secondary academic | academic monographs, journal articles, specialist histories | usable; cite page numbers |
| Authoritative institution | central banks, statistical offices, international organisations, museums, university institutional pages | usable |
| Encyclopedia entry (original) | original entries such as Wikipedia | usable, but key facts need another source |
| Mirror/proxy site | wikiwand, wiki2, us-wikipedia, translate.goog, etc. | avoid where possible; existing ones are flagged for replacement |

Mirror sites are not banned, but introducing a new mirror source raises a warning at validation and puts it on the replacement list (`research/list_mirror_sources.py` exports the full list). **If a primary source is available, use it.**
