> **English** ｜ [中文](CONTRIBUTING.md)

# Contributing

Thank you for helping make the Guide thicker. This file explains **how to submit, what we will accept, and what will be returned**.

The core of this project is not prose. It is **verifiability**: every fact written into the Guide must stand on a source you can open and check against the original text. The bar for contributing is not writing skill—it is evidence.

## 1. What You Can Contribute

| Type | Form | Merged automatically |
|:---|:---|:---|
| **Correction** | Point out that a fact is wrong, a source has died, or a quote does not match | Issue, not PR |
| **Research layer** | Add facts, add opportunities, open a new regional pack, swap a mirror source for a primary source | ✅ merged after machine validation passes + a human confirms the quotes |
| **Draft layer** | Add or rewrite the Guide for a given year | ❌ **write it in a PR, but it is merged only after human review** |

**Why drafts get their own review.** A finished draft runs over sixty thousand characters; changing one sentence can pull on citation numbers, the tag system, and three-stage coverage. A machine cannot judge that, and "CI is green" is not a reason to merge. So every draft PR goes into the human review queue, may be sent back for several rounds, and should be budgeted for accordingly.

## 2. Environment Setup

All you need is Python 3.9 or later. No third-party dependencies:

```bash
git clone https://github.com/yadnuses/A-Guide-for-Time-Travelers.git
cd A-Guide-for-Time-Travelers
python3 research/validate_pack.py    # should pass in full
```

## 3. Contributing Research: The Full Workflow

**Step 1 | Pick a pack**

Existing packs live in `research/YYYY/REGION/`. Before opening a new pack, file an Issue stating the year and region, so two people do not do the same work.

**Step 2 | Read the specs**

- Fields, enums, naming: [`docs/data-spec.en.md`](docs/data-spec.en.md)
- If you also want to write the draft: [`docs/draft-spec.en.md`](docs/draft-spec.en.md)

**Step 3 | Write three files**

```text
research/1911/CN/
├── facts.jsonl          one fact per line
├── opportunities.jsonl  one opportunity per line
└── summary.md           seven sections, keep the headings unchanged
```

Key requirements:

- **One JSON object per line.** No code fences, no trailing commas, no wrapping array.
- **`quote` must be text that actually exists in the source**, not your paraphrase. Reviewers check this one first.
- **`based_on` must point to a `fact` ID that actually exists in this pack.** Do not write one out of thin air.
- If you mark something `cross_checked`, actually supply two independent sources. With only one source, mark it `single_source` and say so.

**Step 4 | Self-check**

```bash
python3 research/validate_pack.py 1911 CN     # checks only the pack you changed
```

Wait for `OK` before opening a PR. Items flagged `[提示]` (the script's warning marker) do not block the merge, but explain them in the PR description.

**Step 5 | Open a PR**

PR title format: `data: 1911/CN add wartime prices and employment`. In the description, state clearly: what you added, what tier your sources are, and what gaps remain.

## 4. Contributing a Draft

You may write a draft at `YYYY-YYYY/YYYY.md` (for example `1910-1919/1911.md`), but note:

1. **Research first, draft second.** Every `[n]` citation in a draft must point back to a record under `research/`. Paragraphs with no research behind them will be asked to be cut, not kept as "I will write it now and fill it in later".
2. **Do not renumber existing citations in a PR.** Append new citations, and append to the appendix in step. Changing existing numbers makes every later PR conflict.
3. **Do not polish unrelated paragraphs along the way.** One PR does one thing; mixed changes will be asked to be split.
4. **Self-check:**

```bash
python3 research/check_draft.py 1911
```

5. Draft PRs go to human review. The standard is in [`docs/draft-spec.en.md`](docs/draft-spec.en.md), sections 10 and 11.

## 5. Five Hard Rules

1. **Append only, never change old lines.** Write new JSONL records at the end of the file. Editing or reordering existing lines turns the diff into the whole file and makes conflicts unresolvable.
2. **Increment IDs.** Take the highest existing number in the pack + 1, contiguous, no gaps. If two PRs collide on a number, the one merged later is asked to renumber.
3. **One PR does one thing.** Fill one pack, swap one batch of sources, fix one citation—do not mix them.
4. **Do not reformat other people's code or docs.** Do not touch indentation, field order, or punctuation style.
5. **Do not delete source conflicts.** When two sources disagree, write both accounts side by side and tag them `conflicted`. Never pick one just to keep things tidy.

## 6. What Happens Before a Merge

```text
you open a PR → machine validation (automatic, about 1 minute) → human quote check → merge
```

**What the machine checks** (`validate_pack.py` / `check_draft.py`):

- Whether the JSONL parses, whether fields are complete, whether enums are valid
- ID format, category abbreviations, whether the year matches the directory
- Whether `based_on` points to a fact that actually exists
- Whether `history_proven` has an `outcome`, and whether `inferred` is empty
- Whether `summary.md` has all seven sections
- Whether the draft has the six-column structure, the five route card fields, continuous citations, and an appendix count that matches the in-text limit

**What a human checks** (what a machine cannot):

- Whether `quote` really supports what the `fact` states—**this is the most important item**
- Source tier: primary archive > official statistics > academic > original encyclopedia entry > mirror site
- Whether a source conflict was kept side by side, or quietly smoothed away
- Whether "about" or "reportedly" got written up as established fact

## 7. About Mirror Sources

Mirror sites such as `wikiwand`, `wiki2`, `us-wikipedia`, and `translate.goog` are not forbidden, but they are a low source tier. About 17% of the records already in the repo cite mirror sources, and they are being replaced over time.

**New records that cite a mirror source will not fail validation, but they will be flagged in the validation output**, and the PR description will be asked to explain "why the primary source could not be obtained". Replace them where you can.

## 8. Common Rejection Reasons

- `quote` cannot be found in the source, or it is your own summary
- `based_on` points to an ID that does not exist
- One fact crams in three or four separate things, so it cannot be verified on its own
- `history_proven` gives no follow-up outcome, or gives an outcome with no matching fact
- A return figure is precise to the decimal, but the source has no such number
- You reordered someone else's lines, so the diff no longer shows the real change
- One PR touches three packs at once

## 9. License

By submitting, you agree to publish your contribution under this repository's licenses: text and data under [CC BY-NC-SA 4.0](LICENSE), scripts under [MIT](LICENSE-CODE).
