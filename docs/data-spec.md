# 数据格式规范

本文件规定 `research/` 下每条事实记录与机会记录的字段、枚举、命名与验收标准。向仓库提交资料前请先读完本文；机器校验脚本实现的就是本文第 7 节的条款。

## 1. 搜集原则

1. **事实与推演分离。** 可核验的事实写入 `facts.jsonl`，生存和赚钱的推演写入 `opportunities.jsonl`。两者不混写。
2. **一源一引。** 每条事实至少有一个可靠来源，并保留来源标题、具体链接或书目信息、支持该事实的原文摘录和访问日期。摘录必须真的出现在来源里。
3. **关键事实双源。** 影响主路线的事件日期、法律状态、价格、金融结果和比赛结果，尽量使用第二个独立来源交叉核验，并在 `verification` 中如实标记。
4. **不得编造。** 不允许编造来源、原文摘录、数据或历史结果。无法确认的内容写进 `summary.md` 的资料缺口，不得伪装成事实。
5. **一次只写一个包。** 一个提交只改自己认领的「年份×地区」，不修改其他目录。

## 2. 目录与任务单位

一份任务是「年份×地区」，占用一个目录：

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

- `YYYY` 为四位年份，例如 `1910`。
- `REGION` 优先使用 ISO 3166-1 alpha-2 大写国家或地区代码，例如 `FR`、`US`、`GB`；历史政权或无法对应当代代码的地区使用清晰的大写英文名称，例如 `OTTOMAN`。同一项目内必须保持同一代码。
- `global/` 只放跨地区的年度总览记录，且应在该年份的地区任务完成后再写。
- 每份任务只写自己的三个文件。

## 3. 数据类别

| 英文枚举 | 中文名称 | 要求 |
|:---|:---|:---|
| `events` | 事件日历 | 核心；重大事件、准确日期和行动时间窗口 |
| `survival_cost` | 生存成本 | 核心；货币、物价、工资、食宿和交通 |
| `law_identity` | 法律与身份 | 核心；证件、执法、行业准入、法律灰色地带 |
| `finance` | 金融机会 | 核心；股票、债券、汇率、黄金、房地产和银行制度 |
| `technology_industry` | 科技与产业 | 核心；已有技术、新兴技术、专利和产业风口 |
| `safety_medical` | 安全与医疗 | 按需；战争、灾害、治安、疾病和医疗条件 |
| `business_career` | 商业与职业 | 按需；紧缺技能、就业、贸易和创业机会 |
| `sports_culture` | 体育与文化 | 按需；比赛结果、流行文化、出版和博彩机会 |
| `language` | 语言速查 | 按需；应急表达和当地常用文字 |

「核心」五类必须都有；确实不存在的类别，需在 `summary.md` 说明搜索过程与证据缺口，校验脚本会提示但不阻断。

## 4. `facts.jsonl`

每行一个完整 JSON 对象。不加 Markdown 代码围栏、注释、尾逗号，也不要包成数组。**一个对象只陈述一个可独立核验的事实。**

```json
{"id":"1900-FR-EVENT-001","year":1900,"region":{"continent":"欧洲","country":"法国","city":"巴黎"},"category":"events","fact":"可独立核验的事实陈述","date":"1900-04-14","sources":[{"title":"来源标题","url":"具体链接或书目信息","quote":"支持该事实的原文摘录","accessed_at":"2026-10-30"}],"verification":"single_source","confidence":"high"}
```

### 必填字段

| 字段 | 说明 |
|:---|:---|
| `id` | `YYYY-REGION-类别缩写-三位序号`，全项目唯一 |
| `year` | 四位整数年份，须与所在目录一致 |
| `region` | 含 `continent`、`country`、`city`；全球记录的 `country`、`city` 用 `null` |
| `category` | 第 3 节的九个英文枚举之一 |
| `fact` | 只写事实，不写建议、收益预测或价值判断 |
| `date` | `YYYY`、`YYYY-MM`、`YYYY-MM-DD` 或 `开始日期/结束日期`；不适用时为 `null` |
| `sources` | 至少一项，每项含 `title`、`url`、`quote`、`accessed_at`；纸质书目在 `url` 写完整书目信息与页码 |
| `verification` | `single_source`、`cross_checked` 或 `conflicted` |
| `confidence` | `high`、`medium`、`low`，表示证据可靠程度，不表示故事精彩程度 |

### 类别缩写

| 类别 | 缩写 | 类别 | 缩写 |
|:---|:---|:---|:---|
| `events` | `EVENT` | `safety_medical` | `MED` |
| `survival_cost` | `COST` | `business_career` | `BIZ` |
| `law_identity` | `LAW` | `sports_culture` | `SPORT` |
| `finance` | `FIN` | `language` | `LANG` |
| `technology_industry` | `TECH` | | |

### 关于 `conflicted`

来源互相矛盾时，`verification` 填 `conflicted`，并用多个 `sources` 把两种口径都列出来，在 `fact` 中并列保留，例如「A 来源记 X，B 来源记 Y」。**不得为了整齐而抹平分歧**——读者有权看到证据本身的不一致。

## 5. `opportunities.jsonl`

每行一个完整 JSON 对象。每条机会必须通过 `based_on` 引用至少一个已存在的事实 ID。

```json
{"id":"1900-FR-OPP-001","year":1900,"region":{"continent":"欧洲","country":"法国","city":"巴黎"},"title":"机会名称","stage":"first_capital","opportunity_type":"inferred","outcome":null,"outcome_date":null,"hypothesis":"这条路线为什么可能成立","based_on":["1900-FR-EVENT-001"],"time_window":"可行动的时间范围","requirements":["启动所需条件"],"steps":["推演中的行动步骤"],"legal_then":"gray","legal_today":"illegal","risks":["主要风险"],"uncertainties":["尚未证实或需进一步核查的部分"],"confidence":"medium"}
```

### 字段约束

| 字段 | 说明 |
|:---|:---|
| `id` | `YYYY-REGION-OPP-三位序号`，全项目唯一 |
| `stage` | `survival`、`first_capital`、`wealth_jump` |
| `opportunity_type` | `history_proven`（后来被真实结果验证）或 `inferred`（尚未被验证的推演） |
| `outcome` | `history_proven` 必须填具体成功结果；`inferred` 必须为 `null` |
| `outcome_date` | 结果发生时间，格式同 `date`；`inferred` 必须为 `null` |
| `hypothesis` | 说明因果逻辑，不能只写「利用信息差赚钱」 |
| `based_on` | 事实 ID 数组，不得为空，引用的 ID 必须真实存在 |
| `time_window` | 可行动的时间范围；未知时写「未知」并在 `uncertainties` 说明 |
| `requirements` / `steps` / `risks` / `uncertainties` | 字符串数组；无内容用空数组，但关键未知条件不得省略 |
| `legal_then` / `legal_today` | `legal`、`gray`、`illegal`、`varies`、`unknown`；不同现代法域结论不同时用 `varies` |
| `confidence` | `high`、`medium`、`low`，表示路线成立的可信程度 |

推演允许大胆，但不得删除启动成本、法律风险、市场容量、身份限制和记忆误差等约束。**收益数字没有事实依据时不得填写精确金额。** 公司后来成功不等于当时任意价格买入都能盈利，也不等于该公司当时已经上市。

## 6. `summary.md`

按以下顺序组织，标题文字保持一致：

```markdown
# YYYY×REGION 资料摘要

## 任务范围
实际覆盖的地区、时间和数据类别。

## 核心发现
最重要的事实 ID 及其意义，不复制成正文。

## 主要机会
机会 ID、类型、阶段和一句话结论。

## 后来者的成功，当下的财富
全部 `history_proven` 机会：后续真实结果、当时参与渠道、仍然存在的执行限制；没有则写「未形成证据充分的路线」。

## 来源冲突
来源之间的矛盾及当前处理依据；没有则写「未发现」。

## 资料缺口
未能核实的内容及其对路线的影响；没有则写「未发现」。

## 主舞台建议
该地区是否适合作为年度主舞台，并说明理由。
```

## 7. 验收标准

机器校验脚本 `research/validate_pack.py` 逐条检查以下前七项，第八项由人工复核：

1. 三个文件均存在，JSONL 每行都能被标准 JSON 解析器读取。
2. 必填字段齐全，枚举值合法，`id` 格式与所在目录、`category` 一致。
3. 所有事实 ID 与机会 ID 在包内唯一，`based_on` 引用均可解析。
4. `history_proven` 具有具体 `outcome`、`outcome_date` 及证明该结果的事实引用；`inferred` 两个结果字段均为 `null`。
5. 五类核心数据均有搜集，或已在摘要中说明缺口。
6. `summary.md` 七个小节齐全。
7. 每条事实至少一个完整来源，`legal_*`、`risks`、`uncertainties` 没有留空规避。
8. **人工复核**：`quote` 是否真的支持 `fact` 的陈述，以及来源等级是否达标。

## 8. 来源等级

审核时按以下等级判断，等级越低越需要说明：

| 等级 | 类型 | 处理 |
|:---|:---|:---|
| 一手 | 政府公报、统计年鉴、同期报刊、档案、法律原文 | 最优先 |
| 二手学术 | 学术专著、期刊论文、专门史著作 | 可用，标注页码 |
| 权威机构 | 央行、统计局、国际组织、博物馆、大学机构页 | 可用 |
| 百科原始条目 | Wikipedia 等原始条目 | 可用，但关键事实需另找来源 |
| 镜像/代理站 | wikiwand、wiki2、us-wikipedia、translate.goog 等 | 尽量避免；已存在的会被标记待替换 |

镜像站不是禁止项，但引入新的镜像源会在校验时提示，并计入待替换清单（`research/list_mirror_sources.py` 可导出全量）。**能用一手源就用一手源。**
