---
name: wiki-ingest
description: Use when adding a new source to a wiki — a paper, article, URL, file, transcript, or any document. One ingest may touch 10-15 wiki pages.
---

# Wiki Ingest

## Table of Contents
- [Pre-condition](#pre-condition)
- [Process](#process)
- [Step 1: Accept the source](#step-1-accept-the-source)
- [Step 2: Read the source in full](#step-2-read-the-source-in-full)
- [Step 3: Surface takeaways](#step-3-surface-takeaways)
- [Step 4: Generate the slug](#step-4-generate-the-slug)
- [Step 5: Write the source summary page](#step-5-write-the-source-summary-page)
- [Step 6: Update entity and concept pages](#step-6-update-entity-and-concept-pages)
- [Step 7: Backlink audit](#step-7-backlink-audit)
- [Step 8: Update 06 Wiki/index.md](#step-8-update-wikiindexmd)
- [Step 9: Update 06 Wiki/overview.md](#step-9-update-wikioverviewmd)
- [Step 10: Append to 06 Wiki/log.md](#step-10-append-to-wikilogmd)
- [Step 10.5: Inbox Sweep](#step-105-inbox-sweep)
- [Common Mistakes](#common-mistakes)
- [Step 11: Report to user](#step-11-report-to-user)

Add a source to the wiki. Read it, discuss with the user, write a summary page, update entity/concept pages, and maintain the index, overview, and log.

## Pre-condition

Read `GEMINI.md` to learn: wiki root path, page frontmatter format, cross-reference convention, log entry format, index category taxonomy.

## Process

### Step 1: Accept the source

The source can be:
- **File path** — read it directly; copy to `00 Inbox/<filename>` if not already there
- **URL** — use the `browse` skill to fetch it; save to `00 Inbox/<slug>.<ext>`
- **Pasted text** — use what was provided

**Link to Summarize Skill:** If the source is a YouTube video, PDF, EPUB, podcast, or long article, trigger the `summarize` skill first to generate a high-fidelity summary in `07 Summaries/` before proceeding with ingestion. This ensures the wiki has access to a deeply synthesized version of the content.

### Step 2: Read the source in full

Read all content. For long sources, read in sections. Do not skip.

### Step 3: Surface takeaways — BEFORE writing anything

Tell the user:
- 3-5 bullet points of key takeaways
- What entities/concepts this introduces or updates
- Whether it contradicts anything already in the wiki (use `obsidian search` to check relevant pages)

Ask: **"Anything specific you want me to emphasize or de-emphasize?"**

Wait for the user's response before proceeding.

### Step 4: Generate the slug

Lowercase, hyphens, no special characters.
Example: "Attention Is All You Need" → `attention-is-all-you-need`

### Step 5: Write the source summary page

Write `06 Wiki/pages/<slug>.md` using `obsidian-markdown` syntax.

```markdown
---
title: <source title>
tags: [<relevant tags>]
sources: [<slug>]
detailed_summary: "[[07 Summaries/...]]" # Link to high-fidelity summary if generated
updated: <today>
---
```

# <Source Title>

**Source:** <original URL or file path>
**Date ingested:** <today>
**Type:** <paper | article | transcript | code | other>

## Summary

<2-3 paragraph synthesis — your own words, not abstract copy-paste>

## Key Takeaways

- <bullet>

## Entities & Concepts

<list of entities/concepts as [[wikilinks]]>

## Relation to Other Wiki Pages

<how this connects to or updates existing knowledge>
```

#### Cite as you write — do not skip

While drafting prose, every non-common-knowledge factual claim must carry a footnote. See the **Citations** section in `SCHEMA.md` for the convention. Use [[wikilinks]] for source-type pages.

### Step 6: Update entity and concept pages

For each entity/concept touched by this source:

- **Page exists:** Use `obsidian read file="<slug>"` to read it, add to/update sections, update `sources` and `updated` frontmatter using `obsidian property:set`.
- **Page doesn't exist:** Create it using `obsidian create`.

### Step 7: Backlink audit — do not skip

Scan ALL existing pages in `06 Wiki/pages/` (use `obsidian search`) for any that mention this source's entities/concepts but don't yet link to the new page. Add `[[new-slug]]` references where appropriate.

This is the step most commonly skipped. A compounding wiki's value comes from bidirectional links.

### Step 8: Update `06 Wiki/index.md`

Add an entry under the correct category:
```
- [[<slug>]] — <one-line summary> _(ingested <date>)_
```

### Step 9: Update `06 Wiki/overview.md`

Re-read `overview.md` (use `obsidian read file="overview"`). If this source:
- Introduces a significant concept: add it to "Key Entities / Concepts"
- Shifts the overall synthesis: update "Current Understanding"
- Raises a new question: add it to "Open Questions"

Update the frontmatter `updated` date using `obsidian property:set`.

### Step 10: Append to `06 Wiki/log.md`

```
## [<today>] ingest | <source title>
Pages written: <slug>
Pages updated: <comma-separated list>
```

## Step 10.5: Inbox Sweep

**Ensure no source is left behind by proactively ingesting other pending items.**

After the primary ingestion is complete and logged:
1. Scan the `00 Inbox/` folder for any files that have not been ingested into the wiki yet. A file is pending if:
    - It does not have a corresponding source page in `06 Wiki/pages/`.
    - It is not listed in `06 Wiki/index.md`.
2. For each pending file found:
    - Trigger the full `wiki-ingest` workflow.
    - As per Step 1, this will automatically trigger `/summarize` first if the source type is supported.
3. Continue until all items in `00 Inbox/` are fully ingested.

## Common Mistakes

- **Appending chronological updates instead of editing in-place** — Wiki pages are living documents, not journals. Do not add sections like `## April 27 update:` or `**Update:**` followed by new content. Update the relevant section in-place, bump the `updated` frontmatter date, and record what changed in `log.md`.
- **Skipping the backlink audit (step 7)** — Always scan existing pages for entities this source introduces.
- **Summarizing the abstract instead of synthesizing** — The Summary section should reflect your own synthesis.

### Step 11: Report to user

- Summary page: `06 Wiki/pages/<slug>.md`
- Entity/concept pages created or updated: <list>
- Pages that received backlinks: <list>
- Index and overview updated
