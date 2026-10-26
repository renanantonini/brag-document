# Setup and settings

First-time setup is a short conversation, about 5 minutes, one question per message. Start the config (`~/.brag-document/config.yaml`, or `brag-config.yaml` in the shared-folder layout below) from `assets/config.example.yaml` with every sample value reset (`name: null`, `emails: []`, `handles: {}`, `repos: []`, `tool: null`, `remote_cli: none`, `tags: []`, `timezone` set to the system timezone as an IANA name such as `America/Sao_Paulo`) and every source `enabled: false`, then save after each answer, so a setup stopped midway resumes where it left off. Changing a setting later is the same conversation, limited to that setting.

Run discovery (source-recipes.md, "Discovery") silently before the first message, so every later step can propose what was found instead of asking.

```text
Setup progress:
- [ ] 1 Welcome and experience level
- [ ] 2 Bundle folder
- [ ] 3 Sources and identity
- [ ] 4 Tags
- [ ] 5 Weekly rhythm
- [ ] 6 Bundle created and validated
- [ ] 7 First check-in offered
```

**1. Welcome.** Say in two lines what a brag document is and that the weekly check-in takes about 15 minutes. Ask whether they have used AI skills or slash commands before. A clear yes sets `user_level: experienced`; anything else sets `beginner`.
- **Beginner:** explain in three short lines how to use the skill: ask in plain words (or `/brag-document` where slash commands exist), stop at any time, nothing is saved without their ok.
- **Experienced:** in one message, list the defaults (language they write in, `~/brag-document` or the shared-folder layout where it applies, the detected sources that work, base tags, Friday 16:00 in the system timezone, no reminders), name any failing connector as left out, state the privacy promise from step 3, and offer to accept them all and change anything later. On yes, ask, one per message, only for what step 3 needs and discovery could not fill (name, commit email, code folder when code is enabled), then jump to step 6.
Done when `user_level` is set.

**2. Folder.** Use the language they write in for conversation and entries (they can change it any time) and say so in passing. Propose `~/brag-document` as the bundle folder; a git repository or an Obsidian vault folder both work. Where only a shared folder persists, use the shared-folder layout instead and say in one line that everything will live in that folder. Done when `language` and `bundle_path` are set.

**3. Sources and identity.** Show what discovery found as a short list: "I can read: your git repos, Jira, Google Calendar. Not connected: email, transcripts." Then state the privacy promise in these terms: "I only read these sources, never change anything in them, keep a short summary and a link instead of copying messages, and save nothing without your ok." Ask which to enable. Then fill `identity` (name, emails, usernames) and each source's settings from discovery, asking for each missing piece in its own short message: the name for `index.md`, the email their commits use, the folder where they keep code. When code is enabled, do not skip the commit email: without it the code recipe finds nothing. If the code folder holds no git repositories, say so and ask for another folder (in the shared-folder layout, only folders inside the shared one can be read); if there is none, keep code enabled only when a remote CLI or connector works, otherwise set it to `false`. Never ask for passwords or tokens. If a connector is missing or failing, say where to add or reconnect it (the app's connector settings) and move on. Done when each source type is `enabled: true` or `false` and `identity` is filled.

**4. Tags.** Offer the base set, translated into their language, and let them rename, drop or add:

| Base tag (English meaning) | Covers |
|---|---|
| project | Features, launches, migrations |
| incident | Production issues solved, on-call |
| collaboration | Code reviews, unblocking others, cross-team work |
| mentoring | 1:1s, onboarding, helping someone grow |
| design-docs | Design docs, ADRs, documentation |
| company-building | Hiring, interviews, process, culture |
| learning | Courses, talks attended, new skills |
| outside-work | Talks given, open source, writing |

Tags are lowercase, hyphenated, ASCII (`colaboracao`, not `colaboração`) so they work as Obsidian and Notion tags. Done when `tags` is saved.

**5. Weekly rhythm.** Ask for a day and time (suggest Friday 16:00, in the system timezone, which you name and ask them to confirm, since a VM often runs on UTC). Then offer, one per message:
- **A calendar reminder.** Describe the exact event: a title like "Brag document: weekly check-in" in their language, the chosen day and time, weekly, 20 minutes. With a calendar connector that can create events, create it only on an explicit yes. Without one, give that same text as a suggestion to add by hand, with no question.
- **Scheduled collection**, only if a tool for creating scheduled tasks is available (for example Claude Code desktop or Cowork scheduled tasks); otherwise skip it silently. It gathers candidates into the inbox an hour before the check-in, so the session starts with them ready. Mention that it runs only while the computer is on and the app is open.
Done when `review_day`, `review_time` and `reminders` are set.

**6. Create the bundle.** Create the `inbox_path` folder, and `bundle_path` with `index.md` (entry-format.md) and `.obsidian/app.json` (copy `assets/obsidian-app.json`; if the folder or one of its readable parents already has an `.obsidian/` folder, it is inside a vault: skip it and give the vault-settings tip from entry-format.md instead). Run `scripts/brag.py validate <bundle>` and then `scripts/brag.py log <bundle>`, so the `log.md` that `index.md` links to exists. If validation fails, fix what it names and return to Step 6. Done when it passes.

**7. Offer the first check-in** covering the last 7 days.

## Shared-folder layout

For environments where the home folder is temporary but a folder the person shares persists (Cowork, a VM with a mounted folder). Everything lives in that folder, so it survives between sessions and travels with it:

```text
<shared folder>/
├── brag-config.yaml      # same fields as assets/config.example.yaml
├── brag-inbox/           # inbox_path: brag-inbox
└── brag-document/        # bundle_path: brag-document
```

Set `bundle_path: brag-document` and `inbox_path: brag-inbox`, both relative, so the folder still works if it moves. Code repositories are readable only if they sit inside the shared folder; say so at step 3 and offer the GitHub, GitLab or Gitea connector for the rest. If the person already has a config at `~/.brag-document/` on a computer where that persists, keep using it: this layout is only for when it does not.

## Scheduled collection

A scheduled run does weekly-check-in.md step 1 only and writes an inbox file (weekly-check-in.md, "Inbox files"). It never writes to the bundle or changes `last_check_in`.

## Config fields

`assets/config.example.yaml` is the reference, with a comment on each field. Keep unknown fields intact when rewriting the file.
