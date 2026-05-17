# Powerhouse Vault Template

Welcome to the Powerhouse Vault template! This repository contains the structure, guidelines, and AI skills needed to bootstrap a hybrid **Second Brain** and **Powerhouse Wiki** in Obsidian.

This system is designed to balance the action-oriented tracking of daily life (meetings, people, projects) with rigorous, citable knowledge synthesis.

## 🚀 Installation & Quick Start

1. **Clone this repository** (or download it).
2. **Run the bootstrap script**:
   ```bash
   ./bootstrap.sh <path-to-your-new-vault>
   ```
   If you don't provide a path, it will create the folders in the current directory.
3. **Open the vault in Obsidian**.
4. **Create Today's Daily Note**: Go to `02 Daily/` and create a note for today (e.g., `17-05-2026 Sun.md`). Use it to log your activities.
5. **Setup Your Person Note**: Create `04 People/Your Name.md`.

## 🧠 Philosophy

This vault serves two main purposes:
- **Second Brain**: For ephemeral or chronological data like daily logs (`02 Daily/`), meetings (`03 Meetings/`), relationships (`04 People/`), and active projects (`05 Projects/`).
- **Powerhouse Wiki**: For formal knowledge (`06 Wiki/`). Here, knowledge is distilled into flat, slug-named files, and every claim is backed by strict footnotes.

## 📂 Directory Structure

- **`00 Inbox/`**: Raw inputs to be processed.
- **`01 Updates/`**: Daily research or topic updates.
- **`02 Daily/YYYY/MM/`**: Your daily notes. The heartbeat of your session.
- **`03 Meetings/`**: Notes and transcripts from calls.
- **`04 People/`**: Rich snapshots of your relationships.
- **`05 Projects/`**: Active, multi-step goals.
- **`06 Wiki/`**: The core knowledge base (slug-named pages).
- **`07 Summaries/`**: AI-distilled content.
- **`_Assets/`**: Images, PDFs, etc.
- **`_Bases/`**: Database views (if using the Obsidian Bases plugin).
- **`_Templates/`**: Reusable markdown templates.
- **`99 Context/`**: Sub-vaults or specific context areas.
- **`Archive/`**: Completed projects.

## 📏 Core Rules

> **CRITICAL: The "No H1" Rule**
> Never add `# Title` headings to notes. Obsidian displays the filename as the H1. Start every note with YAML frontmatter, then go straight into `##` headings or callouts.

- **Unread Tracking**: Every new or modified note must have `unread: true` in its frontmatter.
- **Backlinks over Tags**: Prefer linking (`[[Concept]]`) over tags (`#tag`). Links provide context.

## 🏛️ The Wiki (Powerhouse)

- **Naming**: Pages in `06 Wiki/pages/` must be lowercase with hyphens (e.g., `machine-learning.md`).
- **Strict Citations**: Cite every non-trivial factual claim using footnotes `[^1]`.
  - *Quote Citation*: `[^1]: [[source-slug]] §1.1 — "Direct quote here"`
  - *Synthesis Citation*: `[^2]: [[source-slug]] §2 — [synthesis] Summary of concepts`

## 🤖 AI Configuration & Skills

This repository includes `GEMINI.md`, `CLAUDE.md`, and `AGENTS.md` files that instruct LLMs (like Gemini CLI or Claude Code) on how to interact with this specific vault structure.

It also includes specialized skills in `.gemini/skills/` and `.claude/skills/`:
- **`wiki-ingest`**: Process raw documents into the wiki.
- **`summarize`**: Distill articles/videos into `07 Summaries/`.
- **`summarize-call`**: Generate transcripts and meeting notes.

When you run `bootstrap.sh`, these files are copied into your new vault, making your AI agents instantly aware of the rules.
