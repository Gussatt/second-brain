# How Gemini should treat this vault

> [!important] **NEVER add `# Title` headings to any note.** Obsidian shows the filename as the title; a duplicate H1 is redundant. Start every file with frontmatter, then go straight into body content (callouts, prose, lists). This applies to ALL notes — no exceptions.

## Purpose

This vault is the user's "second brain" and a "powerhouse wiki". It combines action-oriented tracking (meetings, people, projects) with rigorous knowledge synthesis (wiki pages, citations, overviews).

## Folder structure

| Folder              | Purpose                                                                                                                                               |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00 Inbox/`         | Raw inputs, quick notes, and immutable source documents before they are processed.                                                                    |
| `01 Updates/`       | Daily research updates by topic (one file per topic). Newest entries at top, older days collapsed into `> [!note]-` callouts grouped by `## MM-YYYY`. |
| `02 Daily/YYYY/MM/` | Daily notes, named `DD-MM-YYYY ddd.md` (e.g. `29-03-2026 Sun.md`). Mandatory log of session activity.                                                 |
| `03 Meetings/`      | Call/meeting notes and transcripts. Notes named `DD-MM-YYYY Day Name1 x Name2.md`. Transcripts named similarly with ` Transcript` suffix.             |
| `04 People/`        | Person notes. Detailed snapshots of relationships, family, and history.                                                                               |
| `05 Projects/`      | Active project folders. Each has a root note `<projectName>.md` and a running log.                                                                    |
| `06 Wiki/`          | The knowledge powerhouse. Flat slug-named pages in `pages/`, plus `index.md`, `log.md`, and `overview.md`.                                            |
| `07 Summaries/`     | AI-generated summaries of external content (videos, articles, books).                                                                                 |
| `_Assets/`          | Images, PDFs (not in 00 Inbox), and other attachments.                                                                                                |
| `_Bases/`           | Obsidian Bases plugin files (`.base`).                                                                                                                |
| `_Templates/`       | Reusable note templates.                                                                                                                              |
| `_Random/`       | Specialized sub-vaults (e.g., `work/`, `estudos/`, `PQs/`).                                                                                          |
| `Archive/`          | Completed or inactive projects.                                                                                                                       |


## General Rules
- **No `# Title` headings** — never. Filename is the title.
- **Never repeat frontmatter in the body.** Frontmatter = metadata; body = content.
- **Unread tracking**: Set `unread: true` in frontmatter for any created/modified note.
- **Backlinks over tags**: Prefer linking entities (`[[Person]]`) over using tags (`#person`).

## Wiki & Citation Rules (Powerhouse)
- **Slug naming**: Wiki pages must be lowercase with hyphens (e.g., `machine-learning.md`).
- **Strict Citations**: Cite every factual claim using footnotes `[^1]`.
- **Sources**: Cite using `[[source-slug]]`, `00 Inbox/<file>`, or `<URL>`.
- **Overview**: Keep `06 Wiki/overview.md` as the evolving synthesis of everything known.

### Citations

Cite every non-common-knowledge factual claim. "Common knowledge" = uncontroversial,
undergraduate-level facts in this wiki's domain. Granularity is paragraph or claim,
never per-sentence. If you cannot produce a citation in one of the forms below,
find one, weaken the claim, or drop it.

Format: Markdown footnotes. Two citation kinds, three valid targets.

**Quote citation** (preferred):
```
The model uses 8 attention heads.[^1]

[^1]: [[attention-is-all-you-need]] §3.2.2 — "We employ h = 8 parallel attention layers"
```

**Synthesis citation** (when no single quote captures the claim):
```
The architecture is fundamentally an encoder-decoder with attention.[^2]

[^2]: [[attention-is-all-you-need]] §3.2-3.4 [synthesis] — encoder, decoder, and
      attention sections together describe the full multi-head architecture
```

Three rules for every footnote:

1. **The cited target is one of three forms:**
   - `[[source-slug]]` — a source-type wiki page (preferred for sources you've
     ingested via `wiki-ingest`)
   - `raw/<file>` or `assets/<file>` — a path to a local file (for drive-by
     citations where a synthesis page isn't worth creating)
   - `<URL>` — a live URL, tweet, or ephemeral source (no local copy required)

   Never cite entity, concept, or analysis pages — those are syntheses, not sources.

2. **A locator is present:** `§<section>`, `p.<n>`, `[HH:MM:SS]` for transcripts,
   URL anchor for web, or `(DD-MM-YYYY)` for dated posts.

3. **Either a verbatim quote, or the `[synthesis]` tag plus a description** of
   what the cited range supports. No third option.

**Drive-by citation examples:**
```
[^3]: raw/scaling-laws.pdf p.7 — "loss scales as a power law in compute"
[^4]: https://twitter.com/user/status/123 (15-04-2022) — "<tweet text>"
```

### Cross-References
Use `[[slug]]` where slug = filename without `.md`.
Example: `[[transformer-architecture]]` → `wiki/pages/transformer-architecture.md`

## Second Brain Rules (Relationships & Meetings)

- **Link concepts**: Meeting and Person notes MUST link to Wiki pages for technical or domain-specific terms.
- **Person Notes**:
  - Mandatory `> [!info]` snapshot.
  - Link interactions in `## updates` to source Meeting notes, NEVER daily notes.
- **Meetings**: Hyperlink ALL people, places, and notable nouns.

### Person notes

- One note per person, in `04 People/<Full Name>.md`
- Top-level callouts:
  - `> [!note] current age: \`=date(today)-date(this.birthday)\`` — Dataview inline query (skip if Dataview isn't installed). If birthday is estimated, append `(estimated)` to the callout text — but `birthday` in frontmatter must remain a pure YAML date.
  - `> [!info]` — rich snapshot of who they are: life story, mission, current focus, key context. Update as new info emerges.
- `## updates` section — chronological log of interactions, each linking to the call/meeting/episode note where they appeared. **Never link to daily notes from `## updates`** — link the source content note.
- Person notes grow organically. For briefly mentioned people, only add what's known. Don't fill out empty boilerplate sections.

### Aliases and disambiguation

- Use display aliases for relationships in frontmatter: `[[John Doe|older brother]]`, `[[Jane Smith|partner]]`.
- Never create two separate wikilinks for the same entity. Use alias syntax: `[[Cobie|Jordan Fish]]`, not `[[Cobie]] / [[Jordan Fish]]`. One entity = one link target.
- Same for renamed companies/products: `[[Facebook|Meta]]`, `[[X|Twitter]]`.

### Meeting/call note conventions

- Hyperlink ALL people, places, and notable nouns (companies, products, concepts) — even if the note doesn't exist yet.
- Body has `## Summary` with key points. **Never repeat frontmatter in the body** — no `# Title`, no recording link if `recording:` is in frontmatter, no transcript link if `transcript:` is in frontmatter.
- Add a `## People mentioned` section listing everyone referenced with a one-line context.
- Transcript notes (in `03 Meetings/Transcriptions/`): frontmatter only for metadata; body is ONLY the timestamped transcript lines.

### Templates (in `_Templates/`)

- **Person**: see [[new person template]]. The `summarize` and `summarize-call` skills install this on first run.
- Add your own templates for books, places, projects, calls, video notes, etc. as your workflow demands. Keep them minimal — frontmatter + a couple of section headers.
- All templates use `{{date:DD-MM-YYTHH:mm}}` for `created`/`updated`.

### Bases

If you use the Bases plugin, store `.base` files in `_Bases/`. Common ones:

- `meetings.base` — all calls/meetings, with per-person filtered views
- `posts.base` — all videos/podcasts/articles (the `summarize` skill writes here)
- `books.base` — all books

When a new person appears in summarized content (podcast episode, YouTube video, etc.), add a per-person view to `posts.base` and embed it in their person note:

```yaml
- type: table
  name: "Person Name"
  filters:
    and:
      - recording != null
      - people.contains(link("Person Name"))
  order:
    - date
    - views
    - file.name
    - summary
  sort:
    - property: date
      direction: DESC
```

Then in their person note: `![[posts.base#Person Name]]`.

For people with real 1-on-1 calls (not just podcast appearances), do the same with `meetings.base` and embed `![[meetings.base#Person Name]]` in a `## meetings/hangouts` section.

### Daily note format

- Path: `02 Daily/YYYY/MM/DD-MM-YY ddd.md`
- Organize work under `##` headers by project/topic (e.g. `## vault setup`, `## summarize skill bugfix`)
- Bullets under each — terse, link to relevant notes
- Always include `## calls/meetings` if any occurred
- `## TODO for next session` at the bottom for carryover

## Work Privacy
- If a note contains **Work** specific info, ensure it is ignored if syncing to public repositories. (Repo has a `.gitignore` for the `work/` path).

## Skills Integration
- **wiki-ingest**: Target `06 Wiki/` and `00 Inbox/`.
- **summarize**: Output to `07 Summaries/`, create reference notes in `06 Wiki/pages/`.
- **summarize-call**: Output to `03 Meetings/`, participants in `04 People/`.
