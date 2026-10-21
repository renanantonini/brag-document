# Editing

The person describes the change in plain words; the agent finds the entry, shows the change, and writes only after an ok.

1. **Find.** Run `scripts/brag.py list <bundle>` and match the request against titles, descriptions and dates. If more than one entry fits, list them numbered in one line each and ask which. Done when exactly one entry (or the set for a merge) is chosen.
2. **Show** only the fields that change, as before → after. When the change gives a draft its impact, include `status: draft → stable` in the same view. Done when the person says ok, or adjusts and then says ok.
3. **Write** (SKILL.md, "Every write to the bundle").

## Operations

- **Correct or complete:** change the named fields. A new `date` in a different month means moving the file (see Rename).
- **Polish drafts:** `scripts/brag.py list <bundle> --status draft`, then go through them one per message, oldest first, asking the one missing piece as in weekly-check-in.md step 4. The person can stop at any time.
- **Merge:** combine into the earliest entry: one description, the best impact, the union of tags and sources. Then remove the others.
- **Remove:** confirm the title once more, then delete the file. If the bundle is a git repository, mention the deletion can be undone there.
- **Rename or move:** the path is the OKF id, so before moving search the bundle for links to the old path (`grep -rn "<old-file-name>" <bundle>`), move the file, update each link, then validate.

## Hand edits

The person may edit files directly in Obsidian or any editor. When the validator later reports a broken file, show the error in one line, propose the fix, and apply it on ok.
