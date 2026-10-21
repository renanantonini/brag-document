# Notion sync

One-way: the local bundle is the source of truth; Notion is a read-only showcase with date and tag filters. Edits made in Notion are not read back, and the next sync overwrites them. Say this once at first sync.

## Requirements

A Notion connector (MCP) with access to the target page or database. If none is available, say so and point to the app's connector settings; do not try other ways to reach Notion.

## First sync

1. Ask for the parent page or an existing database. To create one, use these properties: `Title` (title), `Date` (date), `Description` (text), `Impact` (text), `Tags` (multi-select), `Status` (select: draft, stable), `Evidence` (text, one reference per line), `Brag ID` (text, the entry's path without `.md`). Save the database in `notion.database`.
2. Ask how to handle other people's names: keep them, replace with roles ("a junior engineer on the team"), or ask each time. Save as `notion.anonymize_names` (`never`, `always`, `ask`).

## Every sync

1. `scripts/brag.py list <bundle>` gives the entries. Query the database for existing `Brag ID` values.
2. Show the plan in one message: N to create, N to update, N in Notion with no local entry (left alone, never deleted). Mention that the content will leave the machine.
3. On ok, create or update one page per entry, matching on `Brag ID`. Apply the anonymization choice to Title, Description, Impact and Evidence. Body notes are not synced.
4. Report counts and any failures in one or two lines.
