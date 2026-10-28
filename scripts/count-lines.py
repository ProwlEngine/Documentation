#!/usr/bin/env python3
"""Counts executable lines of C# in every Anthology library and writes stats.json.

    python scripts/count-lines.py

Counted: every line with code on it. Not counted: blank lines, comments (//, ///, /* */),
`using` and `global using` directives, lines made only of brackets and separators such as
`{`, `}` or `});`, #region markers, generated files, and anything in tests, samples,
benchmarks, obj or bin folders. Comment markers inside strings, including raw string
literals, are left alone.

The Prowl website reads stats.json for the line counts on its Anthology page. Run it by
hand from the Actions tab (Count lines > Run workflow), or locally. No dependencies
beyond Python 3.8.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "stats.json")

SKIP_DIR = re.compile(r"(^|/)(obj|bin|\.git|\.github|scripts|[^/]*tests?|[^/]*samples?|benchmarks?)(/|$)", re.I)
GENERATED = (".g.cs", ".Designer.cs", ".generated.cs", "AssemblyInfo.cs")
BRACKETS_ONLY = re.compile(r"^[{}()\[\];,]+$")
USING = re.compile(r"^(global\s+)?using\s+[\w.:=\s<>,]+;$")
REGION = re.compile(r"^#\s*(region|endregion)\b")


def strip_comments(src: str) -> str:
    """Removes comments from C# source, keeping line breaks and the contents of strings."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        nx = src[i + 1] if i + 1 < n else ""
        if c == "/" and nx == "/":  # line comment
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == "/" and nx == "*":  # block comment; keep its newlines so line numbers hold
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("\n" * src.count("\n", i, j))
            i = j
            continue
        if c == '"' or (c in "$@" and nx in '"$@'):  # "..", @"..", $"..", $@"..", """raw"""
            k = i
            while k < n and src[k] in "$@":
                k += 1
            prefix = src[i:k]
            if src.startswith('"""', k):  # raw string literal, any number of quotes
                q = k
                while q < n and src[q] == '"':
                    q += 1
                quotes = src[k:q]
                end = src.find(quotes, q)
                end = n if end < 0 else end + len(quotes)
                out.append(src[i:end])
                i = end
                continue
            if k >= n or src[k] != '"':
                out.append(c)
                i += 1
                continue
            verbatim = "@" in prefix
            j = k + 1
            while j < n:
                if verbatim:
                    if src[j] == '"' and j + 1 < n and src[j + 1] == '"':
                        j += 2
                        continue
                    if src[j] == '"':
                        j += 1
                        break
                else:
                    if src[j] == "\\":
                        j += 2
                        continue
                    if src[j] in '"\n':
                        j += 1
                        break
                j += 1
            out.append(src[i:j])
            i = j
            continue
        if c == "'":  # char literal
            j = i + 1
            while j < n and src[j] not in "'\n":
                j += 2 if src[j] == "\\" else 1
            out.append(src[i : j + 1])
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def count_file(path: str) -> int:
    with open(path, encoding="utf-8", errors="replace") as f:
        text = strip_comments(f.read())
    count = 0
    for line in text.split("\n"):
        t = line.strip()
        if not t or USING.match(t) or REGION.match(t) or BRACKETS_ONLY.match(t.replace(" ", "")):
            continue
        count += 1
    return count


def main() -> int:
    libraries = {}
    for lib in sorted(os.listdir(ROOT)):
        lib_dir = os.path.join(ROOT, lib)
        if not os.path.isdir(lib_dir) or lib.startswith(".") or SKIP_DIR.search(lib):
            continue
        lines = files = 0
        for dirpath, dirnames, filenames in os.walk(lib_dir):
            rel = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
            if SKIP_DIR.search(rel):
                dirnames[:] = []
                continue
            dirnames.sort()
            for name in sorted(filenames):
                if name.endswith(".cs") and not name.endswith(GENERATED):
                    files += 1
                    lines += count_file(os.path.join(dirpath, name))
        if files:
            libraries[lib] = {"lines": lines, "files": files}

    stats = {
        "version": 1,
        "counts": "Executable lines: no comments, blank lines, using directives or bracket-only lines; no tests, samples or benchmarks.",
        "total": sum(v["lines"] for v in libraries.values()),
        "libraries": libraries,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")

    width = max(len(k) for k in libraries) if libraries else 0
    for name, v in sorted(libraries.items(), key=lambda kv: -kv[1]["lines"]):
        print(f"{name:<{width}}  {v['lines']:>8,} lines  {v['files']:>5} files")
    print(f"{'Total':<{width}}  {stats['total']:>8,} lines in {len(libraries)} libraries -> stats.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
