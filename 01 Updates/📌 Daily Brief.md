---
created:
updated:
topic: daily brief
frequency: daily
ongoing: true
unread: false
---

> [!prompt]- Agent Instructions
> A daily personal briefing — what's happening today across the things you care about. Edit the section list, sources, and format to match your life.
>
> **How to use**
> 1. Edit this prompt callout to define your sections (Weather, Calendar, Email, Messages, Tasks — or whatever matters to you).
> 2. Wire up data sources for each section. Common options:
>    - Weather: a weather API or web search
>    - Calendar: Google Calendar / Apple Calendar via MCP, or just have the agent ask you
>    - Email: Gmail / IMAP MCP, or you paste highlights
>    - Messages: any messaging MCP (Beeper, Slack, Discord), or you summarize
>    - Tasks: Things3 / Todoist / Apple Reminders MCP, or your own task file
> 3. Decide how the brief gets generated:
>    - **Manual**: ask the agent "update my daily brief" whenever you want it
>    - **On a schedule**: use `/schedule` (cloud) or `/loop` (local recurring) to run it automatically each morning
>
> **Sections (default — customize freely):**
> One callout per section. Keep each section to the most important items only.
> - **Weather**: short line — temperature, conditions, what to wear
> - **Calendar**: today's events with time + brief context
> - **Email**: items needing a reply or action. For each: who, what they want, suggested reply
> - **Messages**: unreplied DMs across your messengers. For each: who, what they said, suggested reply
> - **Tasks**: today's priorities — anything urgent or scheduled
>
> **Callout types:**
> - `[!news]` — informational, nothing urgent (grey)
> - `[!breaking]` — urgent items needing action today (yellow/amber)
>
> **Rules:**
> - Newest day at the top, after this prompt callout
> - Group days under `## YYYY-MM` month headers
> - Day heading: `### [[MM-DD-YY Day]]` (e.g. `### [[03-29-26 Sun]]`)
> - When inserting a new day, collapse the previous day into a `> [!note]- [[date]]` callout (prefix all its lines with `> `)
> - Set `unread: true` and update `updated:` in frontmatter when adding entries
>
> **Example day entry:**
> ```
> ## 2026-03
>
> ### [[03-29-26 Sun]]
>
> > ☀️ 12–18°C, partly cloudy. Light jacket.
>
> > [!news] Calendar
> > - 10:00am — Team standup (Zoom)
> > - 3:00pm — Dentist appointment
>
> > [!breaking] Email
> > - [ ] **Accountant** — Missing Q4 receipts, needs them by Friday
> >   → `Hey, thanks for following up. I'll get those over by Thursday.`
> > - GitHub — PR approved, no action needed
>
> > [!news] Messages
> > - [ ] **Friend (Discord)**: left comments on a doc, wants to discuss tomorrow
> >   → `nice, I'll take a look — wanna hop on a call after?`
>
> > [!breaking] Tasks
> > - ⚠️ Tax filing — documents due Friday
> > - Today: Review PR, write weekly update, gym at 7pm
> ```
