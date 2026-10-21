# Recall

For "have I done something like X?", "what did I do on Y?", or "I feel I can't handle this". The answer is evidence from the log, because facts about past work counter impostor feelings better than reassurance does.

1. Run `scripts/brag.py list <bundle>` (add `--from`/`--to` when a period is named) and search titles, descriptions, impact, tags and notes for the topic and its neighbours (similar scope, same skills, same kind of problem). For a large bundle, `grep -rli --exclude=log.md "<term>" <bundle>` narrows it first.
2. Answer with up to three of the closest entries, one line each: date, what they did, the impact, the entry's path in the bundle and its main source URL when it has one. Lead with the closest match.
3. If nothing is close, say so plainly, then show the nearest skills the log does show ("No migrations yet, but you led two projects with zero-downtime deploys"). Never invent or stretch an entry.

Keep the tone warm and matter-of-fact: no therapy language, no generic pep talk. If the person seems in real distress beyond work doubts, acknowledge it briefly and suggest talking to someone they trust.
