#!/usr/bin/env python3
"""Helper for a brag-document OKF bundle. Standard library only (Python 3.8+).

Usage:
  brag.py validate <bundle>
  brag.py log <bundle>
  brag.py list <bundle> [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--status draft|stable] [--tag TAG]

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


def cmd_list(bundle, start, end, status, tag):
    entries, problems = load(bundle)
    if problems:
        print("warning: %d files have errors and may be missing from this list; run validate" % len(problems), file=sys.stderr)
    picked = [
        e for e in entries
        if (not start or str(e.get("date")) >= start)
        and (not end or str(e.get("date")) <= end)
        and (not status or e.get("status") == status)
        and (not tag or tag in (e.get("tags") or []))
    ]
    json.dump(picked, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


def main():
    parser = argparse.ArgumentParser(description="brag-document bundle helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "log", "list"):
        p = sub.add_parser(name)
        p.add_argument("bundle")
        if name == "list":
            p.add_argument("--from", dest="start")
            p.add_argument("--to", dest="end")
            p.add_argument("--status", choices=sorted(STATUSES))
            p.add_argument("--tag")
    args = parser.parse_args()
    bundle = os.path.expanduser(args.bundle)
    if not os.path.isdir(bundle):
        print("bundle folder not found: %s (check bundle_path in ~/.brag-document/config.yaml)" % bundle)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "validate":
        return cmd_validate(bundle)
    if args.cmd == "log":
        return cmd_log(bundle)
    return cmd_list(bundle, args.start, args.end, args.status, args.tag)


if __name__ == "__main__":
    sys.exit(main())
