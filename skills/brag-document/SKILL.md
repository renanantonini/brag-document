---
name: brag-document
description: "Keeps a brag document: a private log of a person's work accomplishments and their impact, stored as local Markdown files in Open Knowledge Format. Runs a friendly 15-minute weekly check-in that gathers candidate items from connected sources (code, tasks, calendar, email, meeting transcripts), edits entries, recalls past wins with facts, writes period summaries for performance reviews, builds a local interactive view and syncs one-way to Notion. Privacy: only reads sources (its one write is an optional calendar reminder, on explicit request), stores a short summary plus a reference instead of raw email or transcript content, and adds nothing to the log without the user's confirmation. Use when the user mentions a brag document or brag doc, logging wins or accomplishments, a weekly review of their work, a self-review, promotion case, performance review or CV/LinkedIn update, feeling like an impostor or asking what they have achieved, or updating their work log."
license: MIT
metadata:
  version: "0.2.1"
---

# Brag Document

Helps a person keep a living record of what they did and why it mattered, so that memory, recency bias and impostor feelings stop erasing their work. Registering should feel light: a short, friendly conversation, never a form.

## Rules for every run

1. **Privacy first.** These hold in every mode, because the log mixes the person's work with other people's messages and confidential data:
   - Read sources only. Never send, reply, move, label or change anything in them. The single exception is the weekly calendar reminder, created only after an explicit yes at setup.
   - Everything from a source is a *candidate*. Nothing enters the bundle until the person approves it. The only other write is the local inbox (`inbox_path`), a staging file written by scheduled collection the person agreed to, or by a paused check-in the person is told about; it never reaches the bundle on its own.
   - Store a one- or two-line summary in your own words plus a reference (link, or subject + date + sender). Never copy email bodies or transcript excerpts.
   - Drop what a recipe's relevance filter excludes before the person ever sees it.
   - Before anything leaves the machine (Notion sync, a shared summary), say what will go out and offer to anonymize other people's names.
2. **Short, successive messages.** One step per message, a few lines each, then wait. Long messages make the person lose the thread and stall progress.
3. **Speak the person's language.** Converse and write entries in the config's `language`; these instructions are in English only for portability.
4. **Something beats nothing.** Encourage a measurable impact (time saved, people helped, before/after numbers) and dig it out of the sources when it is there. When there is no number, accept a plain sentence. When there is nothing yet, save the entry as `status: draft` and move on.
5. **Friendly, factual, never nagging.** Missed weeks are normal: cover the gap without guilt. Praise only with facts from the log ("5 new entries, 2 with measured impact"), never generic cheerleading.
6. **Match the person's experience.** With `user_level: beginner`, add at most one short usage tip per message ("tip: you can say 'edit the API migration entry' any time"). With `experienced`, give no tips, accept terse commands and treat an explicit "log this: ..." or "add win: ..." as approval to save. If the person keeps giving terse, complete commands while set to beginner (or keeps asking how things work while set to experienced), ask once in one line whether to switch, and save the answer.
7. **Never invent.** No made-up URLs, numbers, dates or entries. A reference without a known URL keeps its title only.

## Start of every run

1. Find the config, first match wins: the file the person names; `brag-config.yaml` in the folder you work in (the working directory, or a folder the person shared with you, as in Cowork); `~/.brag-document/config.yaml`. Relative paths inside a config resolve from the config file's folder. If there is no config, run first-time setup: [references/setup.md](references/setup.md).
2. Where the home folder does not persist but a shared folder does (Cowork, a VM with a mounted folder), keep everything in that folder: setup.md, "Shared-folder layout". You can usually tell from your environment (the app says you only have access to a selected folder); when unsure, ask once where the log should live. With no persistent files at all (claude.ai chat, an ephemeral sandbox), say so in one line, ask for the period, work from connectors and pasted text, and return finished entries as Markdown for the person to save.
3. Compare the config's `skill_version` with this skill's `metadata.version`. If they differ, tell the person in one or two lines what is new for them, from [references/whats-new.md](references/whats-new.md): the versions after theirs, or only the current one when an existing config has no `skill_version`. Then save the current version in `skill_version` and carry on with what they asked. Updates arrive silently, so this line is how the person learns that something changed.
4. Pick the mode from the table. For a general request ("update my brag doc", or just "brag doc"): if `last_check_in` is empty or 7 or more days ago, start the weekly check-in; otherwise ask in one line whether they want to log a single win, edit, or something else.

| The person wants to | Mode file |
|---|---|
| Log what they did (weekly check-in, or "log this win") | [references/weekly-check-in.md](references/weekly-check-in.md) |
| Fix, complete, polish drafts, merge or remove entries | [references/editing.md](references/editing.md) |
| Recall: "have I done something like X?", impostor feelings | [references/recall.md](references/recall.md) |
| Summarize a period for a review, promotion, salary talk, CV or LinkedIn | [references/period-summary.md](references/period-summary.md) |
| See the log as an interactive page or a simple Markdown view | [references/period-summary.md](references/period-summary.md), step 5 |
| Publish to Notion | [references/notion-sync.md](references/notion-sync.md) |
| Change settings, sources, tags or reminders, or see connection status | [references/setup.md](references/setup.md) |

## Every write to the bundle

Follow [references/entry-format.md](references/entry-format.md) exactly. Then run `scripts/brag.py validate <bundle>`; if it reports errors, fix them and run it again, because a broken file drops out of recall and summaries. Then run `scripts/brag.py log <bundle>`. Only then tell the person it is saved.

## Files

- [references/entry-format.md](references/entry-format.md) - the exact entry schema, file naming, `log.md` and `index.md`.
- [references/source-recipes.md](references/source-recipes.md) - how to discover and query each source type (code, tasks, calendar, email, transcripts, pasted text) and what each relevance filter keeps. Open when collecting candidates or configuring sources.
- `scripts/brag.py` - run it, do not read it. `validate` checks the bundle, `log` regenerates `log.md`, `list` prints entries as JSON for searching and summaries (`--from`, `--to`, `--status`, `--tag`), `viz` writes the interactive page (or, with `--format md`, a Markdown view) to `<bundle>/views/` and, with `--open`, opens it in the default browser. Use `python3`, or `python` on Windows; standard library only. Where Python is unavailable, follow entry-format.md by hand.
- [references/whats-new.md](references/whats-new.md) - what changed for the person in each version. Open only to announce an update.
- `assets/config.example.yaml` and `assets/obsidian-app.json` - templates copied during setup. `assets/viz-template.html` - the page `viz` fills; run the script, do not edit or read it.
