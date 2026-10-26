#!/usr/bin/env python3
"""Helper for a brag-document OKF bundle. Standard library only (Python 3.8+).

Usage:
  brag.py validate <bundle>
  brag.py log <bundle>
  brag.py list <bundle> [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--status draft|stable] [--tag TAG]
  brag.py viz <bundle> [--from ...] [--to ...] [--lang pt-BR] [--redact "Name,Name"] [--format html|md] [--out FILE]

The frontmatter parser covers the subset of YAML that references/entry-format.md
prescribes (scalars, flow lists, block lists of scalars or of flat mappings),
not YAML in general.
"""
import argparse
import datetime
import json
import os
import re
import sys

RESERVED = {"index.md", "log.md"}
SKIP_DIRS = {".obsidian", ".git", ".trash"}
ENTRY_TYPE = "brag-entry"
SUMMARY_TYPE = "brag-summary"
STATUSES = {"draft", "stable"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PERIOD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}$")
ENTRY_PATH_RE = re.compile(r"^(\d{4})/(\d{2})/(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


class ParseError(Exception):
    pass


def parse_scalar(raw):
    raw = raw.strip()
    if raw == "" or raw in ("null", "~"):
        return None
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    # Real YAML parsers (Obsidian, Notion import) reject or truncate these unquoted.
    if ": " in raw or " #" in raw:
        raise ParseError("value %r needs double quotes (it contains ': ' or ' #')" % raw)
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [parse_scalar(part) for part in inner.split(",")] if inner else []
    if raw.startswith(("[", "{")):
        raise ParseError("unclosed list or mapping: %s" % raw)
    return raw


def split_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ParseError("no frontmatter: the file must start with a '---' line")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    raise ParseError("frontmatter is not closed with a '---' line")


def parse_frontmatter(lines):
    data = {}
    key = None
    for n, line in enumerate(lines, start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            if ":" not in stripped:
                raise ParseError("line %d: expected 'key: value', got %r" % (n, stripped))
            key, _, value = stripped.partition(":")
            key = key.strip()
            data[key] = parse_scalar(value) if value.strip() else []
            continue
        if key is None or not isinstance(data.get(key), list):
            raise ParseError("line %d: indented line without a list key above it" % n)
        items = data[key]
        if stripped.startswith("- "):
            body = stripped[2:]
            if re.match(r"^[A-Za-z_]+:(\s|$)", body):
                k, _, v = body.partition(":")
                items.append({k.strip(): parse_scalar(v)})
            else:
                items.append(parse_scalar(body))
        elif re.match(r"^[A-Za-z_]+:(\s|$)", stripped) and items and isinstance(items[-1], dict):
            k, _, v = stripped.partition(":")
            items[-1][k.strip()] = parse_scalar(v)
        else:
            raise ParseError("line %d: cannot parse %r" % (n, stripped))
    return data


def iter_markdown(bundle):
    for root, dirs, files in os.walk(bundle):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if name.endswith(".md"):
                full = os.path.join(root, name)
                yield full, os.path.relpath(full, bundle).replace(os.sep, "/")


def load(bundle):
    """Return (entries, problems). Each entry is a dict with 'path' and frontmatter fields."""
    entries, problems = [], []
    for full, rel in iter_markdown(bundle):
        is_reserved = os.path.basename(rel) in RESERVED
        with open(full, encoding="utf-8") as f:
            text = f.read()
        if is_reserved:
            if rel == "index.md" and text.startswith("---"):
                try:
                    fm = parse_frontmatter(split_frontmatter(text)[0])
                    if set(fm) - {"okf_version"}:
                        problems.append((rel, "root index.md frontmatter may only hold okf_version"))
                except ParseError as e:
                    problems.append((rel, str(e)))
            continue
        try:
            fm_lines, body = split_frontmatter(text)
            fm = parse_frontmatter(fm_lines)
        except ParseError as e:
            problems.append((rel, str(e)))
            continue
        problems.extend((rel, msg) for msg in check(rel, fm))
        if fm.get("type") == ENTRY_TYPE:
            fm["path"] = rel
            fm["notes"] = body.strip()
            entries.append(fm)
    entries.sort(key=lambda e: (str(e.get("date")), e["path"]))
    return entries, problems


def check(rel, fm):
    kind = fm.get("type")
    if not kind:
        return ["missing 'type' (OKF requires a non-empty type)"]
    if kind == SUMMARY_TYPE:
        msgs = ["summary needs a '%s'" % f for f in ("title", "date", "period") if not fm.get(f)]
        if fm.get("period") and not PERIOD_RE.match(str(fm["period"])):
            msgs.append("period %r must be YYYY-MM-DD..YYYY-MM-DD" % fm["period"])
        return msgs
    if kind != ENTRY_TYPE:
        return []
    msgs = []
    # Drafts may lack a description: saving something beats saving nothing.
    required = ("title", "date", "status") if fm.get("status") == "draft" else ("title", "date", "description", "status")
    for field in required:
        if not fm.get(field):
            msgs.append("missing '%s'" % field)
    date = fm.get("date")
    if date and not DATE_RE.match(str(date)):
        msgs.append("date %r is not YYYY-MM-DD" % date)
    elif date:
        try:
            datetime.date.fromisoformat(str(date))
        except ValueError:
            msgs.append("date %r is not a real date" % date)
    status = fm.get("status")
    if status and status not in STATUSES:
        msgs.append("status %r must be draft or stable" % status)
    if status == "stable" and not fm.get("impact"):
        msgs.append("status is stable but 'impact' is empty; set status: draft or add impact")
    tags = fm.get("tags")
    if tags is not None and not isinstance(tags, list):
        msgs.append("tags must be a list like [projeto, mentoria]")
    sources = fm.get("sources")
    if sources is not None:
        if not isinstance(sources, list) or not all(isinstance(s, dict) for s in sources):
            msgs.append("sources must be a list of items with title/resource")
        else:
            for i, s in enumerate(sources, 1):
                if not s.get("title") and not s.get("resource"):
                    msgs.append("source %d needs a title or resource" % i)
    m = ENTRY_PATH_RE.match(rel)
    if not m:
        msgs.append("path must be YYYY/MM/YYYY-MM-DD-slug.md (lowercase ASCII slug)")
    elif date and DATE_RE.match(str(date)):
        year, month, file_date = m.groups()
        if file_date != str(date) or (year, month) != (str(date)[:4], str(date)[5:7]):
            msgs.append("path date %s does not match date %s" % (file_date, date))
    return msgs


def cmd_validate(bundle):
    entries, problems = load(bundle)
    if not os.path.isfile(os.path.join(bundle, "index.md")):
        problems.insert(0, ("index.md", "missing root index.md (see entry-format.md)"))
    for rel, msg in problems:
        print("ERROR %s: %s" % (rel, msg))
    drafts = sum(1 for e in entries if e.get("status") == "draft")
    print("%d entries (%d drafts), %d errors" % (len(entries), drafts, len(problems)))
    return 1 if problems else 0


def cmd_log(bundle):
    entries, problems = load(bundle)
    by_date = {}
    for e in entries:
        by_date.setdefault(str(e.get("date")), []).append(e)
    out = ["# Log", "", "Generated by brag-document. Do not edit by hand.", ""]
    for date in sorted(by_date, reverse=True):
        out.append("## %s" % date)
        out.append("")
        for e in by_date[date]:
            mark = " (draft)" if e.get("status") == "draft" else ""
            out.append("- [%s](%s)%s" % (e.get("title"), e["path"], mark))
        out.append("")
    with open(os.path.join(bundle, "log.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print("log.md rebuilt: %d entries on %d dates" % (len(entries), len(by_date)))
    if problems:
        print("warning: %d files have errors; run validate" % len(problems))
    return 0


def select(bundle, start=None, end=None, status=None, tag=None):
    entries, problems = load(bundle)
    if problems:
        print("warning: %d files have errors and may be missing; run validate" % len(problems), file=sys.stderr)
    return [
        e for e in entries
        if (not start or str(e.get("date")) >= start)
        and (not end or str(e.get("date")) <= end)
        and (not status or e.get("status") == status)
        and (not tag or tag in (e.get("tags") or []))
    ]


def cmd_list(bundle, start, end, status, tag):
    json.dump(select(bundle, start, end, status, tag), sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


VIZ_MARKER = "/*__BRAG_DATA__*/null"
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)\)")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "viz-template.html")


def redact(value, names, mask):
    """Replace each listed name (whole word, any case) in every string of value."""
    if isinstance(value, str):
        # Full names first, then each part of 3+ letters, so "Carla Mendes" never leaves "Mendes" behind.
        parts = [p for n in names for p in n.split() if len(p) >= 3 and p not in names]
        for name in sorted(names, key=len, reverse=True) + parts:
            value = re.sub(r"\b%s\b" % re.escape(name), mask, value, flags=re.IGNORECASE)
        value = re.sub(r"%s(\s+%s)+" % (re.escape(mask), re.escape(mask)), mask, value)
        return value
    if isinstance(value, list):
        return [redact(v, names, mask) for v in value]
    if isinstance(value, dict):
        return {k: (v if k in ("path", "id", "links", "date") else redact(v, names, mask)) for k, v in value.items()}
    return value


def viz_entries(entries):
    ids = {e["path"][:-3] for e in entries}
    out = []
    for e in entries:
        here = os.path.dirname(e["path"])
        links = []
        for target in LINK_RE.findall(e.get("notes") or ""):
            # OKF allows bundle-absolute ("/2026/04/x.md") and relative links.
            resolved = target.lstrip("/") if target.startswith("/") else os.path.join(here, target)
            rid = os.path.normpath(resolved).replace(os.sep, "/")[:-3]
            if rid in ids and rid not in links:
                links.append(rid)
        out.append({
            "id": e["path"][:-3], "path": e["path"], "title": e.get("title"), "date": str(e.get("date")),
            "description": e.get("description"), "impact": e.get("impact"), "tags": e.get("tags") or [],
            "status": e.get("status"), "sources": e.get("sources") or [], "notes": e.get("notes") or "",
            "links": links,
        })
    return out


MD_TEXT = {
    "pt": {"months": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
                      "setembro", "outubro", "novembro", "dezembro"],
           "title": "Conquistas", "entries": "conquistas", "measured": "com impacto em números",
           "drafts": "rascunhos", "highlights": "Destaques", "timeline": "Linha do tempo",
           "empty": "Nada registrado neste mês.", "draft": "rascunho", "themes": "Temas",
           "theme": "Tema", "count": "Conquistas", "no_impact": "impacto ainda não registrado",
           "footer": "Gerado localmente por brag-document em %s. Os nomes indicados foram ocultados."},
    "en": {"months": ["January", "February", "March", "April", "May", "June", "July", "August",
                      "September", "October", "November", "December"],
           "title": "Accomplishments", "entries": "accomplishments", "measured": "with measured impact",
           "drafts": "drafts", "highlights": "Highlights", "timeline": "Timeline",
           "empty": "Nothing logged this month.", "draft": "draft", "themes": "Themes",
           "theme": "Theme", "count": "Accomplishments", "no_impact": "impact not logged yet",
           "footer": "Generated locally by brag-document on %s. The names you listed were hidden."},
}
DIGIT_RE = re.compile(r"\d")


def pick_highlights(entries, period, limit=5):
    """Up to `limit` stable entries with impact, one per quarter of the period first, to counter recency bias."""
    def score(e):
        return (2 if DIGIT_RE.search(e["impact"]) else 1, e["date"])
    pool = [e for e in entries if e["status"] == "stable" and e["impact"]]
    lo, hi = datetime.date.fromisoformat(period["from"]), datetime.date.fromisoformat(period["to"])
    span = max((hi - lo).days, 1)
    picked = []
    for q in range(4):
        part = [e for e in pool if q == min(3, (datetime.date.fromisoformat(e["date"]) - lo).days * 4 // span)]
        if part:
            picked.append(max(part, key=score))
    rest = sorted((e for e in pool if e not in picked), key=score, reverse=True)
    picked += rest[:max(0, limit - len(picked))]
    return sorted(picked[:limit], key=lambda e: e["date"])


def render_markdown(data):
    t = MD_TEXT["pt" if data["lang"].lower().startswith("pt") else "en"]
    entries, period = data["entries"], data["period"]
    month = lambda d: "%s %s" % (t["months"][int(d[5:7]) - 1], d[:4])
    link = lambda e: "[%s](../%s)" % (e["title"], e["path"]) if e["path"] else e["title"]
    measured = sum(1 for e in entries if e["impact"] and DIGIT_RE.search(e["impact"]))
    drafts = sum(1 for e in entries if e["status"] == "draft")
    out = ["---", "type: brag-view",
           'title: "%s %s..%s"' % (t["title"], period["from"], period["to"]),
           'period: "%s..%s"' % (period["from"], period["to"]),
           "date: %s" % data["generated_at"], "---", "",
           "# %s · %s – %s" % (t["title"], month(period["from"]), month(period["to"])), "",
           "**%d** %s · **%d** %s · **%d** %s" % (len(entries), t["entries"], measured, t["measured"], drafts, t["drafts"]),
           "", "## %s" % t["highlights"], ""]
    for e in pick_highlights(entries, period):
        out.append("- **%s** (%s) · %s" % (link(e), month(e["date"]), e["impact"]))
    out += ["", "## %s" % t["timeline"]]
    y, m = int(period["from"][:4]), int(period["from"][5:7])
    while "%04d-%02d" % (y, m) <= period["to"][:7]:
        key = "%04d-%02d" % (y, m)
        out += ["", "### %s" % month(key + "-01"), ""]
        items = [e for e in entries if e["date"].startswith(key)]
        for e in items:
            impact = e["impact"] or "_%s_" % t["no_impact"]
            tags = " ".join("`#%s`" % x for x in e["tags"])
            mark = " · _%s_" % t["draft"] if e["status"] == "draft" else ""
            out.append("- %s · %s · %s %s%s" % (e["date"][8:], link(e), impact, tags, mark))
        if not items:
            out.append("_%s_" % t["empty"])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    counts = {}
    for e in entries:
        for x in e["tags"]:
            counts[x] = counts.get(x, 0) + 1
    out += ["", "## %s" % t["themes"], "", "| %s | %s |" % (t["theme"], t["count"]), "| --- | --- |"]
    out += ["| %s | %d |" % (x, n) for x, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    if data["redacted"]:
        out += ["", "_%s_" % (t["footer"] % data["generated_at"])]
    return "\n".join(out) + "\n"


def cmd_viz(bundle, start, end, lang, names, out, fmt="html"):
    if fmt == "html" and not os.path.isfile(TEMPLATE):
        print("template not found: %s" % TEMPLATE)
        return 2
    entries = viz_entries(select(bundle, start, end))
    if not entries:
        print("no entries in this period; nothing to show")
        return 1
    dates = [e["date"] for e in entries]
    period = {"from": start or min(dates), "to": end or max(dates)}
    data = {
        "lang": lang, "period": period, "generated_at": datetime.date.today().isoformat(),
        "tags": sorted({t for e in entries for t in e["tags"]}), "entries": entries,
        "redacted": bool(names),
    }
    if names:
        mask = "[colega]" if lang.lower().startswith("pt") else "[colleague]"
        # File names are slugs of titles and can hold a name, so a shared page gets opaque ids.
        opaque = {e["id"]: "e%d" % i for i, e in enumerate(entries, 1)}
        for e in entries:
            e["id"], e["path"] = opaque[e["id"]], ""
            e["links"] = [opaque[x] for x in e["links"]]
        data["entries"] = redact(entries, names, mask)
    if fmt == "md":
        content = render_markdown(data)
    else:
        # Escape "</" so entry text can never close the <script> element it is embedded in.
        payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        with open(TEMPLATE, encoding="utf-8") as f:
            content = f.read()
        if VIZ_MARKER not in content:
            print("template is missing the %s marker" % VIZ_MARKER)
            return 2
        content = content.replace(VIZ_MARKER, payload, 1)
    if not out:
        suffix = "-shared" if names else ""
        out = os.path.join(bundle, "views", "brag-%s_%s%s.%s" % (period["from"], period["to"], suffix, fmt))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("view written: %s (%d entries)" % (os.path.abspath(out), len(entries)))
    return 0


def main():
    parser = argparse.ArgumentParser(description="brag-document bundle helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "log", "list", "viz"):
        p = sub.add_parser(name)
        p.add_argument("bundle")
        if name in ("list", "viz"):
            p.add_argument("--from", dest="start")
            p.add_argument("--to", dest="end")
        if name == "list":
            p.add_argument("--status", choices=sorted(STATUSES))
            p.add_argument("--tag")
        if name == "viz":
            p.add_argument("--lang", default="en", help="interface language, e.g. pt-BR or en")
            p.add_argument("--redact", default="", help="comma-separated names to replace with [colega]")
            p.add_argument("--format", choices=["html", "md"], default="html",
                           help="html = interactive page, md = simple Markdown")
            p.add_argument("--out", help="output file (default: <bundle>/views/brag-<from>_<to>.<format>)")
    args = parser.parse_args()
    bundle = os.path.expanduser(args.bundle)
    if not os.path.isdir(bundle):
        print("bundle folder not found: %s (check bundle_path in your config: ~/.brag-document/config.yaml or brag-config.yaml)" % bundle)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "validate":
        return cmd_validate(bundle)
    if args.cmd == "log":
        return cmd_log(bundle)
    if args.cmd == "viz":
        names = [n.strip() for n in args.redact.split(",") if n.strip()]
        return cmd_viz(bundle, args.start, args.end, args.lang, names, args.out, args.format)
    return cmd_list(bundle, args.start, args.end, args.status, args.tag)


if __name__ == "__main__":
    sys.exit(main())
