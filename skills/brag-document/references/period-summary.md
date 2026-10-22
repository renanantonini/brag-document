# Period summary

For a performance review, a promotion, role or salary review, a 1:1 with a manager, or a CV or LinkedIn update. The summary should make it easy for the person's advocate to defend them. For a CV or LinkedIn, follow the same steps but write the public variant at the end of this file.

1. **Scope**, two messages. First propose exact dates (default, including a bare "semester" or "half": the last 6 months; a named cycle such as "H1 2026" or "Q3" uses its calendar dates), mentioning any high-impact entry just outside the window, and ask "ok?". Then ask whether they have the company's review criteria. If they paste or point at criteria, organize by those; otherwise organize by theme (tags). Done when period and structure are known.
2. **Gather.** `scripts/brag.py list <bundle> --from <start> --to <end>`. If drafts fall in the period, mention the count and offer to polish them first (editing.md), because a missing impact weakens the summary; afterwards, list again and continue here. Done when the entry set is fixed.
3. **Write** a sensible default, adapted to the material:
   - **Highlights:** up to 5 stable entries with the largest impact, one line each, numbers first. Drafts never count as highlights.
   - **By theme or criterion:** one section each, one bullet per entry: what, impact, link to evidence.
   - **Gaps:** criteria with little evidence (without criteria: base tags with no entries, and months with none), said plainly so the person can prepare, not hidden.
   Spread the highlights across the whole period, not only the last weeks, because countering recency bias is the point of the log.
4. **Deliver.** Show it in the chat, then offer to save it to `summaries/` in the bundle (entry-format.md, "Saved summaries"). Before it is shared with anyone, remind the person that it may name colleagues and offer an anonymized copy.
5. **Offer a view** in one line with two formats: "Want to see this period as an interactive page in your browser, or as a simple Markdown file?" The page has a timeline, highlights, filters, a links graph and a presentation mode; the Markdown (`--format md`) has the same highlights, timeline and themes, opens in any editor or Obsidian and is easy to paste elsewhere. Then ask whether they will show it to someone; if so, propose for `--redact` every colleague named in the period's entries (titles, descriptions, impact, notes and their `sources` authors), each written in full as it appears ("Carla Mendes"), and let them add or drop names. Run `scripts/brag.py viz <bundle> --from <start> --to <end> --lang <language> [--format md] [--redact "Name,Name"]` and give the path it prints (a redacted file ends in `-shared`), with how to open it: the page by double-clicking it or dragging it into a browser, the Markdown in any editor. For the page, say once that it is a local file that makes no network requests; only the evidence links open other sites, when clicked. Drafts appear in the timeline, marked as drafts, but never among the highlights.

A direct request to see the log ("show me my year", "open my brag doc as a page") jumps to step 5 after confirming the period, skipping the offer and any question the request already answered (such as "I'll show it to my manager").

## Public variant: CV and LinkedIn

This text leaves the company, so it is written for strangers and checked for confidentiality:
- 3-5 bullets per role, picked from the highest-impact stable entries, one line each: past-tense action verb, then the result, number first when there is one ("Cut duplicate charges from ~30 a week to zero by ...").
- No colleagues' names, internal links, ticket keys, code names or customer names. Turn internal figures into relative ones ("40% faster") unless the person confirms the absolute number is public.
- For LinkedIn, offer one extra version in first person, a short paragraph for the "About" or the role description.
Before delivering, tell the person in one line what you generalized or left out, and remind them to check the company's policy on sharing results publicly.
