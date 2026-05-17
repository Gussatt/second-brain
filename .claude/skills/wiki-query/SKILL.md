---
name: wiki-query
description: Use when asking a question against a personal wiki built with wiki-init and wiki-ingest. Do not answer from general knowledge — always read the wiki pages first.
---

# Wiki Query

## Table of Contents
- [Pre-condition](#pre-condition)
- [Process](#process)
- [Step 1: Read 06 Wiki/index.md first](#step-1-read-wikiindexmd-first)
- [Step 2: Read relevant pages](#step-2-read-relevant-pages)
- [Step 3: Synthesize the answer](#step-3-synthesize-the-answer)
- [Step 4: Always offer to save](#step-4-always-offer-to-save)
- [Common Mistakes](#common-mistakes)

Ask a question. Read the wiki. Synthesize with citations. Offer to file the answer back.

## Pre-condition

Read `GEMINI.md` to learn: wiki root path, page frontmatter format, cross-reference convention, log entry format, index category taxonomy.

## Process

### Step 1: Read `06 Wiki/index.md` first

Use `obsidian read file="index"` to scan the full index and identify relevant pages. Do NOT answer from general knowledge — the wiki is the source of truth here.

### Step 2: Read relevant pages

Use `obsidian read file="<slug>"` (or `obsidian search`) to read the identified pages in full. Follow one level of `[[wikilinks]]` if they point to pages relevant to the question.

### Step 3: Synthesize the answer

Write a response that:
- Is grounded in the wiki pages you read
- Cites inline using `[[wikilinks]]` for every claim sourced from a specific page
- Notes agreements and disagreements between pages
- Flags gaps: "The wiki has no page on X" or "[[page]] doesn't cover Y yet"
- Suggests follow-up sources to ingest or questions to investigate

Format for the question type:
- Factual → prose with citations
- Comparison → table
- How-it-works → numbered steps
- What-do-we-know-about-X → structured summary with open questions

### Step 4: Always offer to save

After answering, say:

> "Worth saving as `06 Wiki/pages/<suggested-slug>.md`?"

If yes:
- Write the page using `obsidian-markdown` (callouts, wikilinks, properties): `tags: [query, analysis]`, `sources: [all cited slugs]`
- Add entry to `06 Wiki/index.md`
- Append to `06 Wiki/log.md`:
  ```
  ## [<today>] query | <question summary>
  Filed as: [[<slug>]]
  ```

If no:
- Append to `06 Wiki/log.md`:
  ```
  ## [<today>] query | <question summary>
  Not filed.
  ```

## Common Mistakes

- **Answering from memory** — Always read the wiki pages. The wiki may contradict what you think you know, and that contradiction is valuable signal.
- **Skipping the save offer** — Good query answers compound the wiki's value. Always offer.
- **No citations** — Every factual claim should trace back to a `[[wikilink]]`.
