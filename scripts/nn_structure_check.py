#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nn_structure_check.py - FILE MODE structure guard for natural-narration (v0.5.0).

Compares protected Markdown parts between the source file and an edited copy.
Read-only. Exit code 0 = all protected parts preserved, 1 = something changed.

Usage:
  python3 scripts/nn_structure_check.py BEFORE.md AFTER.md [--json]
"""

import argparse
import json
import re
import sys

FENCE = re.compile(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", re.M | re.S)


def split_code(text):
    """Return (fenced_blocks, text_without_fenced_blocks)."""
    blocks = [m.group(0) for m in FENCE.finditer(text)]
    return blocks, FENCE.sub("\n", text)


def protected_parts(text):
    text = text.replace("\r\n", "\n")
    fm = re.match(r"\A---\n.*?\n---\n", text, re.S)
    body = text[fm.end():] if fm else text
    fenced, prose = split_code(body)
    return {
        "frontmatter": fm.group(0) if fm else None,
        "fenced_code": fenced,
        "inline_code": re.findall(r"(?<!`)`([^`\n]+)`(?!`)", prose),
        "headings": re.findall(r"^#{1,6}[ \t]+.+?$", prose, re.M),
        "link_targets": re.findall(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", prose),
        "bare_urls": re.findall(r"(?<![(\[<])https?://[^\s)>\]]+", prose),
        "table_rows": [r.strip() for r in re.findall(r"^\s*\|.*\|\s*$", prose, re.M)],
        "ordered_steps": re.findall(r"^\s*\d+[.)]\s+.+$", prose, re.M),
        "explicit_ids": re.findall(r"<[^>]*\bid=\"[^\"]+\"[^>]*>", prose),
    }


def compare(before_text, after_text):
    b = protected_parts(before_text)
    a = protected_parts(after_text)
    checks = {}
    diffs = {}
    for key in b:
        same = b[key] == a[key]
        checks[key] = same
        if not same:
            if isinstance(b[key], list):
                diffs[key] = {
                    "before_count": len(b[key]),
                    "after_count": len(a[key] or []),
                    "missing": [x for x in b[key] if x not in (a[key] or [])][:5],
                    "added": [x for x in (a[key] or []) if x not in b[key]][:5],
                }
            else:
                diffs[key] = {"changed": True}
    return {"preserved": checks, "diffs": diffs, "passed": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    with open(args.before, encoding="utf-8") as fh:
        before = fh.read()
    with open(args.after, encoding="utf-8") as fh:
        after = fh.read()
    r = compare(before, after)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("STRUCTURE CHECK: %s -> %s" % (args.before, args.after))
        for k, ok in r["preserved"].items():
            print("   %-14s %s" % (k, "OK" if ok else "CHANGED"))
        for k, d in r["diffs"].items():
            print("      [%s] %s" % (k, json.dumps(d, ensure_ascii=False)))
        print("RESULT: %s" % ("PASS" if r["passed"] else "FAIL"))
    return 0 if r["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
