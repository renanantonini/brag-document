# Source recipes

One recipe per source type, not per product, so GitHub, Gitea and GitLab share the code recipe. Each recipe says what to fetch for the period, what its relevance filter keeps, and how a hit becomes a candidate. Every recipe is read-only (SKILL.md rule 1).

## Contents
- Discovery
- Code
- Tasks
- Calendar
- Email
- Transcripts
- Pasted text and files
- Candidate shape

## Discovery

At setup, and whenever a recipe fails, find what this environment offers:
- **Connectors (MCP tools):** look through the available tool names for the service (jira, atlassian, linear, github, gitlab, gitea, google calendar, outlook, microsoft 365, gmail, granola, fireflies, otter, tldv, teams, meet). Name a tool by its full name when you call it.
- **CLIs:** `git --version`; `gh api user --jq .login`; `glab api user`; `tea whoami`. Each prints only the username, so no token reaches the transcript. A failing command means that CLI is unavailable, not an error to fix.
- **Local folders:** the repos listed in config; at setup, ask where they keep code and list the git repos in that folder.
- **Identity:** `git config user.name`, `git config user.email` and `gh api user --jq .login` (or the connector's "current user" call) fill `identity` without asking.

A connector that is configured but failing counts as not connected: name it and say where to reconnect it.

If a source in config has a `fixture` path, read that file as the source's output instead of calling any tool; the test scenarios use this.

Report what you found as the connection status table (setup.md, "Connection status") and let the person choose. If a recipe that worked before fails now, say which source failed, run the others, and offer to look at it after the check-in.

## Code

Fetch, for each repo in config and for the period:
- Local: `git -C <repo> log --since=<start> --until=<end> --author=<email> --no-merges --pretty=format:"%h %ad %s" --date=short` for each identity email.
- Remote CLI or connector: PRs merged that the person authored, and PRs they reviewed. With `gh`: `gh search prs --author=@me --merged --merged-at=<start>..<end>` and `gh search prs --reviewed-by=@me --updated=<start>..<end>`.

Keep: merged PRs; reviews with substantive comments; new repos or services; commits whose messages show fixes to incidents, performance or security. Drop: version bumps, formatting, merge commits, lone typo fixes. Group commits of one feature into one candidate.

## Tasks

Fetch issues the person resolved, or was assignee on, that moved to done in the period. Jira JQL: `assignee = currentUser() AND statusCategory = Done AND resolved >= "<start>" AND resolved <= "<end>"`. Linear and GitHub Issues: the equivalent filter in their connector.

Keep: stories, epics, bugs and incidents. Read the description and last comments for metrics to propose as impact. Drop: subtasks already covered by their parent, chores without outcome.

## Calendar

Fetch events in the period where the person attended.

Keep: events they organized or presented (talks, demos, workshops, trainings; calendars rarely mark the presenter, so treat an organized event with a talk-like title as "presented?" and confirm in triage); interviews (company-building); recurring 1:1s where they are the senior side (mentoring, reported as a count: "6 mentoring 1:1s"); incident or war-room calls. Drop: dailies, all-hands, routine rituals, declined and cancelled events, private events.

## Email

Search received and sent mail in the period for:
- thanks or praise addressed to the person (thank, obrigad, kudos, parabéns, great job, and the same words in the config language);
- announcements the person sent about something shipping or launching;
- invitations to speak, write, review or join a committee.

Keep the subject, sender and date only, and write the candidate as a summary in your own words. Drop newsletters, notifications, automated mail and anything marked confidential or about HR, health or compensation; never surface those even as candidates.

## Transcripts

Through the transcript connector, list meetings in the period the person attended, then read each one's summary rather than the full transcript where the tool offers one.

Keep: decisions the person proposed or drove; problems they solved or explained; help they gave; recognition they received. Write each as a summary in your own words with the meeting title and date as reference. Never quote what anyone said. Drop: meetings where the person only listened, 1:1s about personal or HR matters.

## Pasted text and files

When the person pastes text or points at a file (notes, an exported transcript, a status report), apply the filter of the matching type above. This path always works, including on claude.ai.

## Candidate shape

Hold each candidate as: one-line summary, guessed tags, proposed impact if the source shows one, and its references (`title`, `resource` when there is a URL, `author` and `last_modified` for messages and meetings). Take `resource` only from a URL the tool returned; with just a key or number, keep it in `title` (`PAY-301 Chaves de idempotência`). That maps one-to-one to the entry fields in entry-format.md.
