# Weekly check-in

Target: about 15 minutes of the person's time. The agent does the slow part (collecting, merging, drafting); the person decides and adds what only they know. One step per message.

```text
Check-in progress:
- [ ] 1 Period and candidates collected
- [ ] 2 Opening sent
- [ ] 3 Triage done
- [ ] 4 Each approved item polished
- [ ] 5 Invisible work asked
- [ ] 6 Entries written (SKILL.md, "Every write to the bundle")
- [ ] 7 Older drafts offered
- [ ] 8 Closing sent, last_check_in saved
```

**1. Period and candidates.** The period starts the day after `last_check_in` (no `last_check_in`: 7 days ago) and ends today.
- **Inbox first.** If `inbox_path` holds files, read them all: their candidates keep their marks, and their periods count as already collected. Collect fresh only for the days after the latest inbox period ends.
- **Long gaps.** If the days still to collect exceed 14, offer in one line to cover them all now or only the oldest 14 days now and the rest next time. Never skip the older weeks, because the forgotten ones are what the log exists for.
- **Collect** with each enabled recipe in source-recipes.md.
- **Merge** candidates about the same deliverable: its commits, PR, ticket, launch email and team meetings about it (postmortem, review) become one candidate with several sources. A talk or demo given to people outside the team is a separate accomplishment.
Done when you hold a deduplicated list, each candidate with a one-line summary and its references.

**2. Opening.** Two or three lines: the period, how many candidates from which sources, and how many older drafts are waiting, if any (step 7 offers them; a draft that a candidate continues is not counted). If nothing was found, say so kindly and go to step 5; a quiet week still deserves a few questions.

**3. Triage.** Show the `untriaged` candidates as a numbered list, grouped by theme, one line each; `approved` ones from the inbox skip triage. Ask for a batch answer: "Which go in? e.g. 1, 3, 5". If there are more than 8, mark your suggested top picks so the session still fits in 15 minutes. Mark a candidate that continues an existing entry (same project, same mentee) with "↳ continues: <entry title>". Done when every candidate is in or out.

**4. Polish.** For each approved item, one message: your drafted `title`, `description`, `tags` and, if the sources state one (a number or a plain outcome sentence, such as "caught a rule that let duplicate refunds through"), the proposed `impact` for the person to confirm. Then ask the one most valuable missing piece, usually impact:
- "Can you measure it? Time saved, people using it, before/after?"
- "What would have happened if you had not done this?"
- "Who benefited?"
If nothing is missing, ask only "ok?". A confirmed outcome sentence or a reach count ("35 people attended") is impact, even when the person cannot measure more. Accept "don't know" and a plain sentence; with no impact, the entry becomes `status: draft`.

For a "continues" item, ask first whether to update that entry or add a new one. Recommend a new entry linking to the old one when the new work falls in a later month, so period summaries still see it; recommend an update when it completes the same accomplishment. An update keeps the entry's date and path, adds one sentence to its description, adds the new sources, fills or improves `impact`, and is shown as before → after (editing.md step 2). Done when each approved item has its fields settled.

**5. Invisible work.** In one message, ask two or three short questions about what sources miss, chosen from this list and varied from week to week; the person answers whichever apply:
- Did you help someone get unblocked?
- Any decision you drove or influenced?
- Reviews that caught something important?
- Someone you mentored or onboarded?
- Something you learned or taught?
- Any praise or thanks you received?
Each answer becomes an item, polished as in step 4 (date: today unless they say). "Nothing else" or similar ends the step.

**6. Write** every approved item (SKILL.md, "Every write to the bundle").

**7. Older drafts.** If drafts exist that this session did not create or update, offer in one line to polish them now (editing.md, "Polish drafts"), oldest first, stopping whenever the person wants.

**8. Close.** Three lines at most: what was saved ("4 new, 1 updated, 3 with numbers, 1 draft"), one fact-based encouragement, and the next check-in: the next `review_day` at least 4 days away. Set `last_check_in` to today (the end of the period covered), then delete the inbox files used.

## Stopping early

If the person stops mid-way, write the items already polished. Put every other candidate in an inbox file, tell the person in one line what was saved and that the rest waits for next time, and leave `last_check_in` unchanged, so the next session resumes from the inbox, finishes those items without asking triage again and still asks step 5.

## Inbox files

In the config's `inbox_path` (default `~/.brag-document/inbox/`), named `YYYY-MM-DD-scheduled.md` or `YYYY-MM-DD-paused.md` by who wrote it. Plain Markdown, this exact shape:

```markdown
period: 2026-10-01..2026-10-21

- [approved] Chaves de idempotência em pagamentos
  date: 2026-10-03
  tags: projeto
  impact (confirmed): cobranças duplicadas ~30/semana → 0
  source: PAY-301 Chaves de idempotência
  source: E-mail "No ar: idempotência na criação de pagamentos" | Ana Souza | 2026-10-03
- [approved] 1:1s com o Pedro
  date: 2026-10-16
  tags: mentoria
  continues: 2026/07/2026-07-22-onboarding-dev-junior.md (update or new: not decided)
  source: 1:1 Ana / Pedro, 3x | Ana Souza | 2026-10-02..2026-10-16
- [untriaged] Entrevista técnica backend pleno
  date: 2026-10-14
  tags: construcao-empresa
  source: Entrevista técnica - vaga backend pleno | rh@example.com | 2026-10-14
```

Marks are `approved` or `untriaged`; rejected candidates are left out. `impact (proposed)` is not yet confirmed by the person; `impact (confirmed)` is. Each `source:` line is `title | author | date`, plus `| url` when one exists; leave out parts that are unknown. Recurring meetings become one source with a count and a date range.

## Logging a single win

When the person says "log this: ..." (or "add win", "anota que ...") outside a check-in, skip to step 4 for that one item, then write it. If no date is given, use today and label it "(date assumed: today)" in the message so the person can correct it. If the message already holds what an entry needs, an experienced person gets the saved entry shown in one message, with an offer to change it; a beginner gets the draft and "ok?". Do not change `last_check_in`.
