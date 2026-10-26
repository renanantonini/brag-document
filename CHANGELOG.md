# Changelog

All notable changes to this skill are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **The interactive page opens by itself.** `brag.py viz --open` opens the page in the default browser, and the period summary uses it on the person's own computer. An app's side panel shows files without running their script, so the page looked blank there and read as broken. Where no browser can open (a VM, Cowork), the skill gives the path and says the side panel may show the page blank.
- **Update notice.** The config keeps `skill_version`. When the installed skill is newer, the next run tells the person in a line or two what is new, from the new `references/whats-new.md`, written in plain words for users. Setup fills `skill_version`, so new users are not told about past updates.
- **README: Updating.** How each install method gets new versions, with auto-update turned on as part of the plugin install, and a release checklist for keeping `plugin.json` and `SKILL.md` versions in step.

### Fixed

- **"X of Y" captions in the interactive view.** A highlight such as "0 de 11" keeps the whole sentence as its caption ("fase 3 com 0 de 11 itens entregues"), instead of cutting the count out and leaving "fase 3 com itens entregues".

## [0.2.1] - 2026-10-26

### Added

- **Connection status table.** Setup, a failing source, or a question like "how are my connections?" shows one row per source type with its status (ready, not responding, not connected, off), what it connects through, what it reads, and what to do next.

### Fixed

- **Highlight numbers in the interactive and Markdown views.**
  - A number that names something is no longer read as a result: "fase 2", "sprint 14", "release 3.4", "versão 2", "phase", "step".
  - "0 de 11" and "9 of 12" are recognized as one metric and take priority over a lone number.
  - Time horizons such as "nos próximos 2 trimestres" and "over the next 3 months" are not highlighted.
  - Bare numbers appear only when the impact has no better metric.

## [0.2.0] - 2026-10-26

### Added

- **Cowork support.** Some environments keep only a folder you share, such as Cowork or a VM with a mounted folder. There, the config (`brag-config.yaml`), the inbox (`brag-inbox/`) and the log (`brag-document/`) all live inside that folder. The skill looks for `brag-config.yaml` in the folder it works in when there is no `~/.brag-document/config.yaml`.
- The marketplace has a description and the plugin has an icon, so `claude plugin validate --strict .` passes without warnings.

### Changed

- The config is looked up in this order: a file you name, then `brag-config.yaml` in the working folder, then `~/.brag-document/config.yaml`.
- An empty `last_check_in` now starts the weekly check-in, the same as a gap of 7 or more days.
- Setup asks you to confirm the timezone, since a VM often runs on UTC.
- Setup creates the inbox folder along with the bundle.
- The README always shows the light theme, which is the page's default.
- The README credits Felipe Adamoli's Tech Leads Club class as the starting point.

## [0.1.0] - 2026-10-22

First public release.

### Added

- **Weekly check-in of about 15 minutes.** The agent gathers candidates from your sources, merges what belongs to the same deliverable and drops noise. You approve items in one batch, and it asks one question per item to pin down the impact. Missed weeks are covered without guilt, and a check-in you stop halfway resumes from where it paused.
- **Sources discovered at runtime**, with one recipe per type: code (git, `gh`, `glab`, `tea` or connectors), tasks (Jira, Linear and similar), calendar, email, meeting transcripts, and pasted text or local files.
- **Entries that can be incomplete.** An entry without an impact is saved as a draft and polished later. The agent encourages numbers but accepts a plain sentence.
- **Editing by conversation**, with every change shown as before and after: correct, complete, polish drafts, merge, remove or rename.
- **Recall.** "Have I done something like this before?" is answered with facts from your own log, which helps with impostor feelings.
- **Period summaries** for performance reviews, promotion, role or salary reviews and 1:1s, organized by theme or by your company's criteria. A public variant for CV and LinkedIn strips names, internal links and confidential figures.
- **Interactive view** (`brag.py viz`). A single local HTML page with a timeline, highlights with impact numbers, combined filters, a links graph and a presentation mode, plus A4 print for saving as PDF. It opens in the light theme, with a button to switch to the dark one. It works offline and makes no network requests.
- **Markdown view** (`brag.py viz --format md`), with the same highlights, timeline and themes as plain text.
- **Redaction for sharing** (`--redact`). It hides full names, their parts and file names that contain them.
- **One-way sync to Notion**, offering to anonymize names before anything is published.
- **Local storage in Open Knowledge Format v0.2.** There is one Markdown file per entry, a generated `log.md`, and the bundle is ready to open as an Obsidian vault.
- **First-time setup in about 5 minutes.** Beginners get short usage tips, and experienced users can accept the defaults in one message. You can add an optional weekly calendar reminder and optional scheduled collection.
- **Helper script** `brag.py`, standard library only, with `validate`, `log`, `list` and `viz`.
- **Install options:** a Claude Code plugin and marketplace, `npx skills add`, or a manual copy.
- **Test scenarios** with fictional data, in `evals/`, and a live example of the interactive view.

### Privacy

- Sources are read only. The single write is the optional calendar reminder, made only after you explicitly say yes.
- Nothing enters your log without your confirmation.
- Entries keep a short summary plus a reference, never the content of email or transcripts.

[0.2.1]: https://github.com/renanantonini/brag-document/releases/tag/v0.2.1
[0.2.0]: https://github.com/renanantonini/brag-document/releases/tag/v0.2.0
[0.1.0]: https://github.com/renanantonini/brag-document/releases/tag/v0.1.0
