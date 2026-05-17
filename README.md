# Second Brain

This is my spin on [LLM-Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) by **Andrej Kaparthy** and [Reysu's](https://www.youtube.com/watch?v=UXJA22y4C80) vault structure and workflows.

It'll help you ingest content through a CLI LLM Agent, like Claude Code or Gemini CLI! I'm using Gemini CLI as it has some generous free limts, but using local models with this is completely doable!

## Installation & Quick Start

1. **Clone this repository** (or download it).
2. **Run the bootstrap script**:
   ```bash
   ./bootstrap.sh <path-to-your-new-vault>
   ```
   If you don't provide a path, it will create the folders in the current directory (not advised)
3. **Open the vault in Obsidian**.
4. **Setup Your Person Note**: Create `04 People/Your Name.md`.
5. **Customize AI Prompts**: Open the files in `01 Updates/` (e.g., `📌 Daily Brief.md`, `📰 Daily News.md`) and edit the prompt instructions within to better align with your specific preferences and workflow.

## Philosophy

This vault serves two main purposes:
- **Second Brain**: For ephemeral or chronological data like daily logs (`02 Daily/`), meetings (`03 Meetings/`), relationships (`04 People/`), and active projects (`05 Projects/`).
- **Wiki**: For raw sources (`_Sources`) formal knowledge (`06 Wiki/`). Here, knowledge is distilled into flat, slug-named files, and every claim is backed by strict footnotes, which you can then ask your Agent to query for important information!

## Capabilities

This vault structure empowers you to:
- **Capture Everything**: Quickly log raw thoughts, links, and documents into the `00 Inbox/`.
- **Maintain Context**: Keep track of people, meetings, and projects organically as they evolve.
- **Synthesize Knowledge**: Transform raw notes into a rigorous, citable knowledge base in the `06 Wiki/`.
- **Automate with AI**: Leverage built-in AI skills to ingest data, summarize content, and structure meetings automatically.
- **Obsidian Web Clipper (Optional but Recommended)**: I highly recommend using the [Obsidian Web Clipper](https://obsidian.md/clipper) extension for your browser. It integrates perfectly with the `00 Inbox/`, allowing you to seamlessly clip articles, recipes, or documentation directly into your vault for later processing and summarization.

## Directory Structure

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
- **`_Random/`**: Sub-vaults or specific context areas.
- **`Archive/`**: Completed projects.

## AI Configuration & Skills

This repository includes `GEMINI.md`, `CLAUDE.md`, and `AGENTS.md` files that instruct LLMs (like Gemini CLI or Claude Code) on how to interact with this specific vault structure.

It also includes specialized skills in `.gemini/skills/` and `.claude/skills/`. When you run `bootstrap.sh`, these files are copied into your new vault.

### Included AI Skills

*   **`defuddle`**: Extracts clean markdown content from web pages using Defuddle CLI, removing clutter to save tokens and focus on the main content.
*   **`json-canvas`**: Creates and edits JSON Canvas files (`.canvas`) for visual mind maps and flowcharts.
*   **`obsidian-bases`**: Manages `.base` files to create database-like views, filters, and summaries of notes.
*   **`obsidian-cli`**: Interacts with the vault using the Obsidian CLI to read, search, and manage notes and properties from the command line.
*   **`obsidian-markdown`**: Native support for creating and editing Obsidian Flavored Markdown, including wikilinks, callouts, properties, and embeds.
*   **`summarize`**: Summarizes any external content (videos, articles, books) into rich notes with section breakdowns and wikilinks. Output goes to `07 Summaries/`.
*   **`summarize-call`**: Transcribes and summarizes call recordings, generating dedicated notes for the meeting and participants.
*   **`vault-update`**: Automates daily updates for the vault, including reading and updating daily briefs and news notes.
*   **`wiki-audit`**: Fact-checks single wiki pages against their cited sources, ensuring accuracy and surfacing uncited claims.
*   **`wiki-ingest`**: Processes and adds new source documents (papers, articles, URLs) into the wiki structure.
*   **`wiki-lint`**: Audits the wiki for health issues, such as contradictions, broken cross-references, and coverage gaps.
*   **`wiki-query`**: Answers questions based specifically on the content ingested into the personal wiki, rather than general LLM knowledge.
*   **`wiki-update`**: Safely revises existing wiki pages when new information contradicts or updates current knowledge.

## References & Inspiration

This setup is heavily inspired by and builds upon the ideas and workflows shared in the following resources:
*   [Reysu's AI Life Skills (`reysu/ai-life-skills`)](https://github.com/reysu/ai-life-skills)
*   [Andrej Karpathy's LLM Workflow Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
*   [Kevin Chou's Wiki Skills (`kfchou/wiki-skills`)](https://github.com/kfchou/wiki-skills#)
*   [Steph Ango's Obsidian Skills (`kepano/obsidian-skills`)](https://github.com/kepano/obsidian-skills)

## Contributing

Contributions are welcome! If you have suggestions for new skills, folder structures, or improvements to the AI instructions, please open an issue or submit a pull request.

## License

MIT
