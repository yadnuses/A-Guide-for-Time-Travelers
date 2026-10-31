<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-Switch-95a5a6?style=for-the-badge" alt="Switch to Chinese"></a>
  <img src="https://img.shields.io/badge/English-Current-2c3e50?style=for-the-badge" alt="English">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Coverage-1900%E2%80%931930-2c3e50?style=flat-square" alt="1900–1930">
  <img src="https://img.shields.io/badge/Guides-31-27ae60?style=flat-square" alt="31 guides">
  <img src="https://img.shields.io/badge/Research-172%20packs%20%C2%B7%201%2C791%20facts%20%C2%B7%20521%20opportunities-2980b9?style=flat-square" alt="172 packs">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Content-CC%20BY--NC--SA%204.0-8e44ad?style=flat-square" alt="CC BY-NC-SA 4.0">
  <img src="https://img.shields.io/badge/Code-MIT-e67e22?style=flat-square" alt="MIT">
</p>

# A Guide for Time Travelers

Welcome to *A Guide for Time Travelers* — a guide that lets you land in any year of the past, read that year's politics and news, and build a fortune from nothing.

Every citation and historical detail in these guides comes from real sources, so the series also works as an entertaining popular history of the years it covers.

## ⚠️ Time travelers: read this before you open the guide

```
1. Each year's guide sits in the folder named after that year in Arabic numerals. Find the one that matches where you land.
2. The guide is written for a global readership. It usually puts its weight on the year's main stage, but the content applies to every continent.
3. The guide assumes you carry some local currency as starting capital (you have a time machine — a little cash should not be the hard part). If you truly arrive empty-handed, read route cards A–B first: they teach you how to earn your first capital.
4. The guide will show you how to make more money with the advantage of foresight — backing Bill Gates while he was still working out of a garage, buying bitcoin early. The historical drift your decisions will cause is beyond anything we can predict.
5. Read the pitfalls checklist carefully. Ignoring it can get you killed.
```

## 📖 Contents

```
1900-1909/          Annual drafts for 1900–1909 (e.g. 1900-1909/1905.md)
1910-1919/          Annual drafts for 1910–1919
1920-1929/          Annual drafts for 1920–1929
1930-1939/          Annual drafts for 1930–1939
research/           Facts, opportunities and summaries filed by year and region, plus validation scripts
CONTRIBUTING.md     How to contribute, submission rules, review process
docs/               Data format spec, annual draft spec
README.md
LICENSE             License for the drafts and research
LICENSE-CODE        License for the scripts
```

## If you are a time traveler, this is all you need. Safe travels.

---

## What follows is the data spec and how we work together — you are welcome to join us.

## 📊 Coverage (kept current)

```
Drafts:   1900–1930, 31 guides, all reviewed
Research: 1900–1930, 172 regional packs, 1,791 facts, 521 opportunities

We want you to build this with us: a Guide covering the whole span of human existence, with every entry getting deeper and wider as we go. Read "Contributing" below to see how.
```

## 🤝 Contributing

We welcome two kinds of contribution: **adding research** and **writing a new year**. Whichever you pick, read the matching spec first.

### How to use these specs

| What you want to do | Read first | Then do this |
|:---|:---|:---|
| Add facts, add opportunities, or adapt an existing year's guide to a new region | [`docs/data-spec.en.md`](docs/data-spec.en.md) | Fill in the field tables in sections 4 and 5 line by line. For `id` naming, see the category abbreviation table in the same section, and continue numbering after the current maximum in that pack |
| Write a new year, or revise an existing draft | [`docs/draft-spec.en.md`](docs/draft-spec.en.md) | Section 10 is the pre-writing checklist, section 11 the post-delivery checklist. Tick them off one by one |
| Not sure about the format | Just run the validator | A red light tells you exactly which ID and which field is wrong. Fix that one thing |

Three steps:

```bash
# 1. After writing to spec, run the validator locally first
python3 research/validate_pack.py 1911 CN

# 2. Once it says OK, open the PR. Items marked [提示] ("hint") do not block — explain them in the PR

# 3. If you are writing a year's guide, clear the draft validator too
python3 research/check_draft.py 1911
```

**The validators are the spec, in code.** Write to spec and CI stays green; write off spec and your PR gets sent back. So the cheapest path is "open the spec → fill in the fields → run it locally → open the PR", not "write first, fix later".

### Three kinds of contribution, three ways to handle them

| Type | Form | Auto-merged? |
|:---|:---|:---|
| **Correction** | A fact is wrong, a source is dead, a quote does not match | Open an issue |
| **Research layer** | Add facts, add opportunities, open a new pack, swap in primary sources | Open a PR |
| **Draft layer** | Add or rewrite an annual guide | **Yes, open a PR — it is merged after an editor reviews it** |

### Five hard rules

1. **Append only; never change an existing line.** New JSONL records go at the end of the file. Editing an existing line turns the diff into the entire file, and that conflict cannot be resolved.
2. **IDs increment.** Use the current maximum in that pack + 1. If two PRs collide on a number, whichever is merged second renumbers.
3. **One PR does one thing.** Adding a pack, swapping a batch of sources, fixing one citation — do not mix them.
4. **Do not reformat other people's files.** No changes to indentation, field order, or punctuation.
5. **Do not delete a source conflict.** When two sources disagree, keep both and mark the record `conflicted`. Never pick one for the sake of tidiness.

### On mirror sources

`wikiwand`, `wiki2` and similar Wikipedia mirrors are not forbidden, but they sit low in the source hierarchy. When the library was first assembled about 17% of its records cited mirror sites; those have now been almost entirely normalized to Wikipedia itself (six entries were still outstanding as of 2026-10-31).

**Citing a mirror will not turn the light red, but it will be flagged in the validation output**, and your PR will be asked "why couldn't you get a primary source?" Replace it if you can.

For the full submission steps, review standards, and the usual reasons a PR is sent back, see [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md).

## 🧩 How the data fits together

Every "year / region" is one research pack with three files:

```
research/1910/US/
├── facts.jsonl          Fact records, each with a URL, an excerpt from the source, and a verification status
├── opportunities.jsonl  Opportunity records, marked either "historically proven" or "reasoned inference"
└── summary.md           That pack's findings, conflicts, gaps, and writing suggestions
```

A fact record's verification status is one of three values: `cross_checked` (two or more sources agree), `single_source` (one source), `conflicted` (the sources contradict each other; both readings are kept side by side, never forced into one). Not resolving contradictions is a design principle of this library — the reader gets to see where the evidence itself disagrees.

## ✅ How to validate

The repo ships its own scripts, all runnable from any directory. **The first two run automatically on every PR**, and you can run them locally before you submit:

```bash
# Validate pack structure and field completeness (no argument = the whole library)
python3 research/validate_pack.py

# Validate annual drafts: six-section structure, five route-card fields, continuous citations, matching appendix (no argument = scan everything)
python3 research/check_draft.py

# Year summary: fact count, opportunity count, coverage of the five core categories
python3 research/summarize_year.py 1900 1910

# List records citing Wikipedia mirrors or proxies, so they can be swapped for primary sources
python3 research/list_mirror_sources.py
```

## 📐 What this rests on

These are the constraints we hold ourselves to while writing — and the doubts you should carry while reading:

- **Never invent a price.** If there is no verifiable share price, dividend, yield, or ticker, write only private equity, partnerships, concessions, and service entry points.
- **Never turn "it succeeded later" into "any investment would have succeeded."** A company becoming a giant does not mean anyone who bought its shares that year made money, and it does not mean an unlisted firm could have been bought by an ordinary time traveler at all.
- **Never beautify violence or injustice.** Colonial violence, genocide, political purges, the rise of fascism — record them with dates and numbers. No voyeurism, no sentimentality, no judging on the reader's behalf.
- **State gaps as gaps.** If the research pack has no figure, the draft says "not obtained". Common sense is not a substitute.

## 📌 Known limitations

- **Uneven year coverage.** 1900–1930 are written; 1931–2025 exist only as regional plans.
- **Source tiers need raising.** Early research could reach only Wikipedia mirrors for some entries. Those have now been almost entirely normalized to Wikipedia itself, but a few entries still depend on AI-generated encyclopedias and revision sites; they are being replaced one by one.
- **1926 has no wealth-jump stage.** That year's research pack contains no `wealth_jump` opportunity, so the draft offers only survival and first-capital routes. An explicit exemption is registered in `research/stage_exemptions.json`; it will be lifted once the research is filled in.
- **Uneven regional depth.** Each year has one main stage carrying a full storyline; secondary regions are markedly shorter, and opportunity cards give only one entry point and one risk.

## 📜 License

- Drafts and research (the year folders and the `.md` / `.jsonl` files under `research/`): **CC BY-NC-SA 4.0**, see [LICENSE](LICENSE).
- Scripts (`*.py`): **MIT**, see [LICENSE-CODE](LICENSE-CODE).

Reposting or adapting requires attribution, non-commercial use, and the same license.
