---
name: wiki-audit
description: Use when fact-checking a single wiki page against its cited sources — verifies that every footnote actually supports its claim and surfaces uncited factual claims. Run after ingesting a high-stakes page or any time you want confidence in one page's accuracy.
---

# Wiki Audit

## Table of Contents
- [Pre-condition](#pre-condition)
- [Process](#process)
- [Step 1: Read the target page](#step-1-read-the-target-page)
- [Step 2: Phase A - uncited claim detection](#step-2-phase-a---uncited-claim-detection)
- [Step 3: Phase B - cited claim verification](#step-3-phase-b---cited-claim-verification)
- [Step 4: Write the audit report](#step-4-write-the-audit-report)
- [Step 5: Offer concrete fixes](#step-5-offer-concrete-fixes)
- [Step 6: Append to 06 Wiki/log.md](#step-6-append-to-wikilogmd)
- [Step 7: Report to user](#step-7-report-to-user)

Verify a single wiki page against its cited sources. Two phases: detect uncited factual claims, then verify cited claims by dispatching one subagent per source in parallel.

## Pre-condition

Read `Gemini.md` for the wiki root path and the **Citations** section (the rules and footnote format the audit enforces).

**If `GEMINI.md` has no Citations section** (older wiki, initialized before this skill existed): use the fallback convention below for this run, and offer at the end to append the Citations section to `SCHEMA.md` so future operations stay consistent.

```
Cite every non-common-knowledge factual claim. Granularity is paragraph or claim,
never per-sentence. Format: Markdown footnotes. Two citation kinds:

Quote:     [^N]: <target> <locator> — "<verbatim quote>"
Synthesis: [^N]: <target> <locator> [synthesis] — <what supports the claim>

Three rules:
1. Target is one of: [[source-slug]] (a source-type wiki page), 00 Inbox/<file> or
   _Assets/<file> (a local file path), or a URL. Never an entity / concept /
   analysis page.
2. A locator is present (§section, p.N, [HH:MM:SS], URL anchor, dated post).
3. Either a verbatim quote, or the [synthesis] tag plus a description of what
   the cited range supports.
```

If the user did not name a page, ask which page to audit. Accept slug, filename, or absolute path. Resolve to `06 Wiki/pages/<slug>.md`. Audit one page per run.

## Process

### Step 1: Read the target page

Use `obsidian read file="<slug>"` to get the full page content and frontmatter. Note:
- The frontmatter `sources:` list (use `obsidian property:get` to verify).
- All footnote definitions (`[^N]: ...`) and references (`[^N]` in body text).

If the page has zero footnotes but contains factual content, that is itself the audit result — every claim becomes a Phase A finding. Still run Phase A; skip Phase B.

### Step 2: Phase A — uncited claim detection (1 subagent)

Dispatch one subagent. Give it:
- The full page contents.
- The **Citations** section copied from `SCHEMA.md`.
- The page's `sources:` list.

Task: list every non-common-knowledge factual claim that lacks a footnote. Return a structured list of `(line number, claim text, suggested-source-from-the-sources-list-or-"unknown")`.

The subagent applies the SCHEMA.md "what to cite" rule: paragraph- or claim-level granularity, common knowledge exempt.

### Step 3: Phase B — cited claim verification (N subagents, parallel)

For every footnote definition in the page, parse:
- The **target** — one of `[[source-slug]]`, a path under `00 Inbox/`/`_Assets/`, or a URL.
- The **locator** (§section, p.N, timestamp, URL anchor, dated post).
- Either the verbatim **quote** or the `[synthesis]` description.

**Resolve each target to readable content:**

- `[[source-slug]]` → Use `obsidian read file="<source-slug>"` to find the raw file path (in its `**Source:**` line). Then read that raw file from `00 Inbox/` or `_Assets/`.
- `00 Inbox/<file>` or `_Assets/<file>` → read the file directly.
- `<URL>` → check whether a cached copy exists in `_Assets/` (filename derived from URL). If yes, read it. If not, mark the footnote `🚫 source-missing` (do not re-fetch — that belongs in the fix step).

Any target that cannot be resolved gets verdict `🚫 source-missing`; do not dispatch a subagent for it.

**Group resolvable footnotes by their resolved file** (multiple footnotes against the same PDF read it once). Dispatch one subagent **per file, in parallel** using the `Agent` tool. Each subagent gets:
- The raw source content (from `00 Inbox/`, `_Assets/`, or cached URL).
- The list of footnotes against that source — for each: number, locator, and either the verbatim quote or the `[synthesis]` description.
- The verdict rubric below.

Each subagent returns, per footnote, one verdict and a 1-line note:

- `✅ supported` — quote string-matches the source at the cited locator, or the `[synthesis]` description honestly summarizes the cited range.
- `❌ unsupported` — quote not found at the cited locator, or the claim is contradicted by the source.
- `⚠️ partial` — quote is paraphrased rather than verbatim (and lacks the `[synthesis]` tag), or the synthesis description overstates the cited range.

For ❌ and ⚠️, the note must include what the source actually says, so the user can decide how to fix.

### Step 4: Write the audit report

Always write — do not ask permission. Path: `06 Wiki/pages/audit-<page-slug>-<today>.md`. Write this as an Obsidian note using callouts for sections and [[wikilinks]].

```markdown
---
title: Audit Report — <page-slug> — <today>
tags: [audit, maintenance]
sources: []
updated: <today>
---

# Audit Report — [[<page-slug>]] — <today>

## Summary
> [!info] Statistics
> - Cited claims verified: N
> - ✅ Supported: N    ❌ Unsupported: N    ⚠️ Partial: N    🚫 Source missing: N
> - 🆘 Uncited factual claims: N

## 🆘 Uncited Claims (Phase A)
- Line 42: "Transformers replaced LSTMs as the default sequence model."
  Suggested source: [[attention-is-all-you-need]] or unknown
  Fix: add footnote, weaken claim, or remove

## ❌ Unsupported (Phase B)
- [^3]: claims "8 attention heads with 128 dims each"
  Source says: "h = 8 parallel attention layers ... d_k = d_v = 64"
  Fix: correct the dimension to 64

## ⚠️ Partial (Phase B)
- [^7]: [synthesis] description says "compares to RNNs across 4 benchmarks"
  Source range covers 2 benchmarks, not 4. Tighten the description.

## 🚫 Source Missing
- [^5]: https://example.com/post — no cached copy in _Assets/
  Fix: re-fetch source, or remove citation

## ✅ Supported
- [^1], [^2], [^4], [^6], [^8] — all verified
```

Add the report to `06 Wiki/index.md` under the `Maintenance` category (create the category if it does not yet exist — `wiki-lint` uses the same category).

### Step 5: Offer concrete fixes

For each non-empty category, offer one at a time:

- 🆘 **Uncited:** "Search the page's `sources:` list for support and propose footnotes for these claims?"
- ❌ **Unsupported:** "Apply the corrections shown in the report? (I'll show diffs first.)"
- ⚠️ **Partial:** "Tighten the synthesis descriptions, or add the `[synthesis]` tag where missing? (diffs first.)"
- 🚫 **Source missing:** "Re-fetch URLs / locate misplaced PDFs back into `00 Inbox/`?"

Apply only after user confirmation. Show the exact diff before each write.

### Step 6: Append to `06 Wiki/log.md`

Always append — do not ask permission:

```
## [<today>] audit | [[<page-slug>]] — N supported, N unsupported, N partial, N uncited
Report: [[audit-<page-slug>-<today>]]
Fixed: <list, or "none">
```

### Step 7: Report to user

- Audit report: `06 Wiki/pages/audit-<page-slug>-<today>.md`
- One-line verdict (e.g. "5/8 cited claims verified, 2 uncited claims found")
- Whether any fixes were applied
