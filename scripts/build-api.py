#!/usr/bin/env python3
"""Builds the scripting API reference for the Prowl website from C# source.

    pip install tree-sitter==0.25.2 tree-sitter-c-sharp==0.23.1
    python scripts/build-api.py --prowl ../Prowl --anthology ../Anthology --out api

Reads Prowl.Runtime, Prowl.Editor and every Anthology library straight from source with a
C# parser, so nothing has to be built. Every public and protected type and member is
documented with its signature, its /// XML documentation and a link to the source line.

Writes:
    api/index.json          assemblies, namespaces and types, plus a compact search list
    api/types/<id>.json     one file per type, with all of its members
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

import tree_sitter_c_sharp
from tree_sitter import Language, Parser

PARSER = Parser(Language(tree_sitter_c_sharp.language()))
SKIP_DIR = re.compile(r"(^|/)(obj|bin|\.git|\.github|[^/]*tests?|[^/]*samples?|benchmarks?|debugger)(/|$)", re.I)
GENERATED = (".g.cs", ".Designer.cs", ".generated.cs", "AssemblyInfo.cs")

TYPE_KINDS = {
    "class_declaration": "class", "struct_declaration": "struct", "interface_declaration": "interface",
    "enum_declaration": "enum", "record_declaration": "record", "record_struct_declaration": "record struct",
    "delegate_declaration": "delegate",
}
MEMBER_KINDS = {
    "constructor_declaration": "constructor", "method_declaration": "method", "property_declaration": "property",
    "indexer_declaration": "indexer", "field_declaration": "field", "event_field_declaration": "event",
    "event_declaration": "event", "operator_declaration": "operator", "conversion_operator_declaration": "operator",
}


# ---------------------------------------------------------------- helpers
def text(node, src):
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def modifiers(node, src):
    return [text(c, src) for c in node.children if c.type == "modifier"]


def visible(mods, in_interface=False, in_enum=False):
    if in_enum:
        return True
    if "private" in mods and "protected" in mods:  # private protected
        return False
    if "public" in mods or "protected" in mods:
        return True
    return in_interface and "private" not in mods


def header(node, src, stop_types):
    """Declaration text from the first modifier or keyword up to the body, without attributes."""
    start = None
    end = node.end_byte
    for c in node.children:
        if c.type == "attribute_list" or c.type == "comment":
            continue
        if c.type in stop_types:
            end = c.start_byte
            break
        if start is None:
            start = c.start_byte
    if start is None:
        start = node.start_byte
    # Attributes on parameters ([NotNull], [DynamicallyAccessedMembers(...)]) are not part of how you call it
    cuts = []
    def find(n):
        for c in n.children:
            if c.end_byte <= start or c.start_byte >= end:
                continue
            if c.type == "attribute_list":
                cuts.append((c.start_byte, c.end_byte))
            else:
                find(c)
    find(node)
    out, pos = b"", start
    for a, b in sorted(cuts):
        out += src[pos:a]
        pos = b
    out += src[pos:end]
    sig = squash(out.decode("utf-8", "replace")).rstrip(";").strip()
    sig = re.sub(r"\(\s+", "(", sig)
    sig = re.sub(r"\s+([,)\]])", r"\1", sig)
    return sig


def attributes(node, src):
    names = []
    for c in node.children:
        if c.type == "attribute_list":
            for a in c.children:
                if a.type == "attribute":
                    n = a.child_by_field_name("name")
                    names.append(text(n, src) if n else text(a, src))
    return names


def split_top(s, sep=","):
    """Splits on sep outside of <> () [] brackets."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "<([":
            depth += 1
        elif ch in ">)]":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def arity(name):
    """`Dictionary<TKey, TValue>` -> ("Dictionary", 2)."""
    m = re.match(r"^([\w.]+)\s*<(.*)>$", name.strip())
    if not m:
        return name.strip(), 0
    return m.group(1), len(split_top(m.group(2)))


# ---------------------------------------------------------------- XML doc comments
def doc_lines_to_xml(lines):
    body = "\n".join(re.sub(r"^\s*///\s?", "", l) for l in lines)
    return body


def parse_docs(lines):
    if not lines:
        return {}
    raw = doc_lines_to_xml(lines)
    try:
        root = ET.fromstring("<doc>" + raw + "</doc>")
    except ET.ParseError:
        try:
            root = ET.fromstring("<doc>" + re.sub(r"&(?!\w+;|#\d+;)", "&amp;", raw).replace("<=", "&lt;=") + "</doc>")
        except ET.ParseError:
            return {"summary": squash(re.sub(r"<[^>]+>", " ", raw))}
    d = {}
    for tag in ("summary", "remarks", "returns", "value", "example"):
        el = root.find(tag)
        if el is not None:
            d[tag] = to_md(el).strip()
    for tag, key in (("param", "params"), ("typeparam", "typeparams")):
        for el in root.findall(tag):
            d.setdefault(key, {})[el.get("name", "")] = to_md(el).strip()
    for el in root.findall("exception"):
        d.setdefault("exceptions", []).append({"cref": el.get("cref", ""), "text": to_md(el).strip()})
    for el in root.findall("seealso"):
        if el.get("cref"):
            d.setdefault("seealso", []).append(el.get("cref"))
    if root.find("inheritdoc") is not None:
        d["inheritdoc"] = root.find("inheritdoc").get("cref") or True
    if not d and squash("".join(root.itertext())):
        d["summary"] = squash("".join(root.itertext()))
    return d


def to_md(el, code=False):
    out = escape_md(el.text or "") if not code else (el.text or "")
    for ch in el:
        tag = ch.tag
        if tag in ("see", "seealso"):
            label = squash("".join(ch.itertext()))
            if ch.get("langword"):
                out += f"`{ch.get('langword')}`"
            elif ch.get("cref"):
                out += f"[{label}](cref:{ch.get('cref')})" if label else f"[[cref:{ch.get('cref')}]]"
            elif ch.get("href"):
                out += f"[{label or ch.get('href')}]({ch.get('href')})"
        elif tag == "c":
            out += "`" + squash("".join(ch.itertext())).replace("`", "'") + "`"
        elif tag == "code":
            body = "".join(ch.itertext()).strip("\n")
            out += "\n\n```csharp\n" + dedent(body) + "\n```\n\n"
        elif tag in ("paramref", "typeparamref"):
            out += "`" + ch.get("name", "") + "`"
        elif tag == "para":
            out += "\n\n" + to_md(ch).strip() + "\n\n"
        elif tag == "list":
            for item in ch.findall("item"):
                term, desc = item.find("term"), item.find("description")
                line = ""
                if term is not None:
                    line += "**" + to_md(term).strip() + "**"
                    if desc is not None:
                        line += ": "
                if desc is not None:
                    line += to_md(desc).strip()
                if term is None and desc is None:
                    line = to_md(item).strip()
                out += "\n- " + line
            out += "\n\n"
        elif tag == "br":
            out += "\n"
        elif tag in ("b", "strong"):
            out += "**" + to_md(ch).strip() + "**"
        elif tag in ("i", "em"):
            out += "*" + to_md(ch).strip() + "*"
        else:
            out += to_md(ch)
        out += escape_md(ch.tail or "")
    return tidy(out)


def escape_md(s):
    return re.sub(r"[ \t\r\n]+", " ", s)


def tidy(s):
    parts = re.split(r"(```.*?```)", s, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r" *\n *", "\n", re.sub(r"[ \t]+", " ", parts[i]))
        parts[i] = re.sub(r"\n{3,}", "\n\n", parts[i])
    return "".join(parts)


def dedent(s):
    lines = s.split("\n")
    pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return "\n".join(l[pad:] for l in lines).rstrip()


# ---------------------------------------------------------------- extraction
class Extractor:
    def __init__(self):
        self.types = {}  # id -> type

    def file(self, path, rel, source):
        src = open(path, "rb").read()
        tree = PARSER.parse(src)
        self.ctx = {"src": src, "rel": rel, "source": source}
        self.walk_container(tree.root_node, "", None)

    def walk_container(self, node, ns, outer):
        """Namespaces, file-scoped namespaces and type declarations inside a compilation unit or namespace body."""
        src = self.ctx["src"]
        docs = []
        for c in node.children:
            if c.type == "comment":
                t = text(c, src)
                if t.startswith("///"):
                    docs.append(t)
                continue
            if c.type == "file_scoped_namespace_declaration":
                ns = text(c.child_by_field_name("name"), src)
                docs = []
            elif c.type == "namespace_declaration":
                name = text(c.child_by_field_name("name"), src)
                body = c.child_by_field_name("body")
                if body:
                    self.walk_container(body, f"{ns}.{name}" if ns else name, None)
                docs = []
            elif c.type in TYPE_KINDS:
                self.type_decl(c, ns, outer, docs)
                docs = []
            elif c.type not in ("attribute_list",):
                docs = []

    def type_decl(self, node, ns, outer, docs):
        src, kind = self.ctx["src"], TYPE_KINDS[node.type]
        mods = modifiers(node, src)
        in_iface = outer is not None and outer["kind"] == "interface"
        if not visible(mods, in_iface):
            return
        if node.type == "record_declaration" and any(c.type == "struct" for c in node.children):
            kind = "record struct"
        name = text(node.child_by_field_name("name"), src)
        tparams = node.child_by_field_name("type_parameters")
        tp = text(tparams, src) if tparams else ""
        n_args = len(split_top(tp[1:-1])) if tp else 0
        parent = outer["id"] if outer else ns
        tid = f"{parent}.{name}" if parent else name
        if n_args:
            tid += f"-{n_args}"
        display = name + (squash(tp) if tp else "")
        body_types = ("declaration_list", "enum_member_declaration_list", "{", ";")
        sig = header(node, src, body_types)
        bases = []
        bl = next((c for c in node.children if c.type == "base_list"), None)
        if bl:
            bases = split_top(squash(text(bl, src))[1:].strip())
        t = self.types.get(tid)
        if t is None:
            t = self.types[tid] = {
                "id": tid, "name": name, "display": display, "kind": kind, "assembly": self.ctx["source"]["assembly"],
                "namespace": ns, "outer": outer["id"] if outer else None, "signature": sig, "bases": bases,
                "docs": parse_docs(docs), "attributes": attributes(node, src), "members": [],
                "source": {"repo": self.ctx["source"]["repo"], "path": self.ctx["rel"], "line": node.start_point[0] + 1},
                "_primary": os.path.basename(self.ctx["rel"]) == name + ".cs",
            }
        else:  # partial type in another file: merge
            # The file named after the type (GameObject.cs, not GameObject.Instantiate.cs) is the primary declaration
            primary = os.path.basename(self.ctx["rel"]) == name + ".cs" and not t.get("_primary")
            if docs and (primary or not t["docs"].get("summary")):
                t["docs"] = parse_docs(docs)
            if primary:
                t["_primary"] = True
                t["signature"] = sig
                t["source"] = {"repo": self.ctx["source"]["repo"], "path": self.ctx["rel"], "line": node.start_point[0] + 1}
            for b in bases:
                if b not in t["bases"]:
                    t["bases"].append(b)
        if kind == "delegate":
            return
        body = next((c for c in node.children if c.type in ("declaration_list", "enum_member_declaration_list")), None)
        if body is None:
            return
        if kind == "enum":
            self.enum_members(body, t)
        else:
            self.members(body, t)

    def enum_members(self, body, t):
        src, docs = self.ctx["src"], []
        for c in body.children:
            if c.type == "comment":
                if text(c, src).startswith("///"):
                    docs.append(text(c, src))
                continue
            if c.type == "enum_member_declaration":
                name = text(c.child_by_field_name("name"), src)
                t["members"].append(self.member("value", name, squash(text(c, src)), docs, c, False))
            docs = [] if c.type != "attribute_list" else docs

    def members(self, body, t):
        src, docs = self.ctx["src"], []
        in_iface = t["kind"] == "interface"
        for c in body.children:
            if c.type == "comment":
                if text(c, src).startswith("///"):
                    docs.append(text(c, src))
                continue
            if c.type in TYPE_KINDS:
                self.type_decl(c, t["namespace"], t, docs)
            elif c.type in MEMBER_KINDS:
                mods = modifiers(c, src)
                if visible(mods, in_iface):
                    for m in self.member_decl(c, t, mods, docs):
                        t["members"].append(m)
            docs = []

    def member(self, kind, name, sig, docs, node, static, attrs=None):
        return {"kind": kind, "name": name, "signature": sig, "docs": parse_docs(docs), "static": static,
                "obsolete": any(a.split(".")[-1].startswith("Obsolete") for a in (attrs or [])),
                "line": node.start_point[0] + 1, "path": self.ctx["rel"]}

    def member_decl(self, node, t, mods, docs):
        src, kind = self.ctx["src"], MEMBER_KINDS[node.type]
        static = "static" in mods or "const" in mods
        attrs = attributes(node, src)
        if node.type in ("field_declaration", "event_field_declaration"):
            var = next(c for c in node.children if c.type == "variable_declaration")
            vtype = squash(text(var.child_by_field_name("type"), src))
            prefix = " ".join(m for m in mods) + (" event" if kind == "event" else "")
            out = []
            for d in var.children:
                if d.type != "variable_declarator":
                    continue
                dname = text(d.child_by_field_name("name") or d.children[0], src)
                sig = f"{prefix} {vtype} {dname}".strip()
                if "const" in mods:
                    val = squash(text(d, src)).split("=", 1)
                    if len(val) == 2 and len(val[1]) < 60:
                        sig += " =" + val[1]
                out.append(self.member(kind, dname, sig, docs, node, static, attrs))
            return out
        if node.type in ("property_declaration", "indexer_declaration"):
            base = header(node, src, ("accessor_list", "arrow_expression_clause", "=", ";"))
            acc = next((c for c in node.children if c.type == "accessor_list"), None)
            if acc:
                parts = []
                for a in acc.children:
                    if a.type == "accessor_declaration":
                        amods = [text(x, src) for x in a.children if x.type == "modifier"]
                        kw = next((text(x, src) for x in a.children if x.type in ("get", "set", "init", "add", "remove")), None)
                        if kw is None:
                            kw = next((text(x, src) for x in a.children if text(x, src) in ("get", "set", "init")), "get")
                        if "private" in amods:
                            continue  # a private accessor is not part of the API
                        parts.append(" ".join(amods + [kw]) + ";")
                base += " { " + " ".join(parts) + " }"
            else:
                base += " { get; }"
            name = "this[]" if kind == "indexer" else text(node.child_by_field_name("name"), src)
            return [self.member(kind, name, base, docs, node, static, attrs)]
        if node.type == "constructor_declaration":
            sig = header(node, src, ("block", "arrow_expression_clause", "constructor_initializer", ";"))
            return [self.member(kind, t["name"], sig, docs, node, static, attrs)]
        if node.type in ("operator_declaration", "conversion_operator_declaration"):
            sig = header(node, src, ("block", "arrow_expression_clause", ";"))
            m = re.search(r"\boperator\s+([^\s(]+)", sig)
            if node.type == "conversion_operator_declaration":
                conv = "implicit" if "implicit" in sig else "explicit"
                name = f"{conv} operator {m.group(1) if m else ''}".strip()
            else:
                name = "operator " + (m.group(1) if m else "")
            return [self.member(kind, name, sig, docs, node, True, attrs)]
        if node.type == "event_declaration":
            sig = header(node, src, ("accessor_list", ";"))
            return [self.member(kind, text(node.child_by_field_name("name"), src), sig, docs, node, static, attrs)]
        # method
        sig = header(node, src, ("block", "arrow_expression_clause", ";"))
        name = text(node.child_by_field_name("name"), src)
        return [self.member(kind, name, sig, docs, node, static, attrs)]


# ---------------------------------------------------------------- linking
class Linker:
    def __init__(self, types):
        self.types = types
        self.by_simple = defaultdict(list)  # "GameObject" -> [ids]; "AssetRef`1" style via arity
        for tid, t in types.items():
            self.by_simple[(t["name"], tid.count("-") and int(tid.rsplit("-", 1)[1]) or 0)].append(tid)
            self.by_simple[(t["name"], -1)].append(tid)

    def resolve_type(self, name, ctx_type=None):
        name = re.sub(r"^[A-Z]:", "", name.strip())
        name = name.split("(")[0].rstrip("?").strip()
        name = re.sub(r"\{([^}]*)\}", lambda m: "<" + m.group(1) + ">", name)
        base, n = arity(name.split("[")[0])
        if base.startswith("global::"):
            base = base[8:]
        dashed = base.replace(".", ".") + (f"-{n}" if n else "")
        if dashed in self.types:
            return dashed
        simple = base.split(".")[-1]
        cands = self.by_simple.get((simple, n)) or self.by_simple.get((simple, -1)) or []
        if not cands:
            return None
        if len(cands) == 1 or ctx_type is None:
            return cands[0]
        ctx = self.types[ctx_type]
        for pref in (lambda c: self.types[c]["namespace"] == ctx["namespace"],
                     lambda c: self.types[c]["assembly"] == ctx["assembly"]):
            best = [c for c in cands if pref(c)]
            if best:
                return best[0]
        return cands[0]

    def resolve_cref(self, cref, ctx_type):
        """Returns (typeId, memberName or None) for a cref, or None."""
        kind = cref[0] if len(cref) > 1 and cref[1] == ":" else None
        body = cref[2:] if kind else cref
        body = body.split("(")[0]
        body = re.sub(r"\{[^}]*\}", "", body) if kind in ("M", "P", "F", "E") else body
        tid = self.resolve_type(body, ctx_type)
        if tid and kind in (None, "T"):
            return tid, None
        if "." in body:
            tpart, mem = body.rsplit(".", 1)
            mem = re.sub(r"\{[^}]*\}|<[^>]*>", "", mem)
            tid = self.resolve_type(tpart, ctx_type)
            if tid and any(m["name"] == mem for m in self.types[tid]["members"]):
                return tid, mem
        if ctx_type:  # a bare member name of the current type
            mem = re.sub(r"\{[^}]*\}|<[^>]*>", "", body)
            if any(m["name"] == mem for m in self.types[ctx_type]["members"]):
                return ctx_type, mem
        return (tid, None) if tid else None

    def link_md(self, s, ctx_type):
        def label_for(cref):
            short = re.sub(r"^[A-Z]:", "", cref).split("(")[0]
            short = re.sub(r"\{([^}]*)\}", r"<\1>", short)
            return short.split(".")[-1] if short.count(".") else short

        def repl(m, bare):
            label, cref = (None, m.group(1)) if bare else (m.group(1), m.group(2))
            label = label or label_for(cref)
            r = self.resolve_cref(cref, ctx_type)
            if not r:
                return f"`{label}`"
            tid, mem = r
            return f"[`{label}`](#api~{tid}{'~' + member_anchor(mem) if mem else ''})"

        s = re.sub(r"\[\[cref:([^\]]+)\]\]", lambda m: repl(m, True), s)
        return re.sub(r"\[([^\]]*)\]\(cref:([^)]+)\)", lambda m: repl(m, False), s)

    def link_docs(self, docs, ctx_type):
        for k in ("summary", "remarks", "returns", "value", "example"):
            if k in docs:
                docs[k] = self.link_md(docs[k], ctx_type)
        for k in ("params", "typeparams"):
            for n in docs.get(k, {}):
                docs[k][n] = self.link_md(docs[k][n], ctx_type)
        for e in docs.get("exceptions", []):
            r = self.resolve_cref(e["cref"], ctx_type)
            e["type"] = re.sub(r"^[A-Z]:", "", e.pop("cref")).split(".")[-1]
            if r:
                e["id"] = r[0]
            e["text"] = self.link_md(e["text"], ctx_type)
        if "seealso" in docs:
            out = []
            for cref in docs.pop("seealso"):
                r = self.resolve_cref(cref, ctx_type)
                if r:
                    out.append({"id": r[0], "member": member_anchor(r[1]) if r[1] else None,
                                "label": re.sub(r"^[A-Z]:", "", cref).split("(")[0].split(".")[-1]})
            if out:
                docs["seealso"] = out


def member_anchor(name):
    return re.sub(r"[^\w.-]+", "-", name).strip("-") or "member"


def inherit_docs(types, linker):
    """Fills <inheritdoc/> and undocumented overrides from base types and interfaces."""
    def bases_of(t, seen):
        for b in t["bases"]:
            bid = linker.resolve_type(b, t["id"])
            if bid and bid not in seen:
                seen.add(bid)
                yield types[bid]
                yield from bases_of(types[bid], seen)

    for t in types.values():
        if t["docs"].get("inheritdoc") and not t["docs"].get("summary"):
            for b in bases_of(t, set()):
                if b["docs"].get("summary"):
                    t["docs"] = {**b["docs"], "inherited": b["id"]}
                    break
        for m in t["members"]:
            needs = m["docs"].get("inheritdoc") or (not m["docs"].get("summary") and "override " in m["signature"] + " ")
            if not needs:
                continue
            for b in bases_of(t, set()):
                src = next((x for x in b["members"] if x["name"] == m["name"] and x["docs"].get("summary")), None)
                if src:
                    m["docs"] = {**src["docs"], "inherited": b["id"]}
                    break


# ---------------------------------------------------------------- main
def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", path, "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return None


def sources(prowl, anthology):
    out = []
    if prowl:
        for proj in ("Prowl.Runtime", "Prowl.Editor"):
            if os.path.isdir(os.path.join(prowl, proj)):
                out.append({"assembly": proj, "group": "Prowl", "repo": "ProwlEngine/Prowl", "root": prowl, "dir": proj})
    if anthology:
        for lib in sorted(os.listdir(anthology)):
            d = os.path.join(anthology, lib)
            if os.path.isdir(d) and not lib.startswith(".") and not SKIP_DIR.search(lib) and lib != "scripts":
                out.append({"assembly": "Prowl." + lib, "group": "Anthology", "repo": "ProwlEngine/Anthology", "root": anthology, "dir": lib})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prowl", help="a Prowl checkout")
    ap.add_argument("--anthology", help="an Anthology checkout")
    ap.add_argument("--out", default="api")
    args = ap.parse_args()

    ex = Extractor()
    files = 0
    for s in sources(args.prowl, args.anthology):
        base = os.path.join(s["root"], s["dir"])
        for dirpath, dirnames, filenames in os.walk(base):
            rel_dir = os.path.relpath(dirpath, s["root"]).replace(os.sep, "/")
            if SKIP_DIR.search(rel_dir):
                dirnames[:] = []
                continue
            dirnames.sort()
            for f in sorted(filenames):
                if f.endswith(".cs") and not f.endswith(GENERATED):
                    ex.file(os.path.join(dirpath, f), f"{rel_dir}/{f}", s)
                    files += 1
    types = ex.types
    if not types:
        print("error: no public types found; check --prowl and --anthology", file=sys.stderr)
        return 1

    linker = Linker(types)
    inherit_docs(types, linker)
    derived = defaultdict(list)
    for t in types.values():
        resolved = []
        for b in t["bases"]:
            bid = linker.resolve_type(b, t["id"])
            resolved.append({"name": b, "id": bid})
            if bid:
                derived[bid].append(t["id"])
        t["bases"] = resolved
        linker.link_docs(t["docs"], t["id"])
        seen = defaultdict(int)
        for m in t["members"]:
            linker.link_docs(m["docs"], t["id"])
            a = member_anchor(m["name"])
            seen[a] += 1
            m["anchor"] = a if seen[a] == 1 else f"{a}-{seen[a]}"
    for tid, ds in derived.items():
        types[tid]["derived"] = sorted(ds)

    # write
    if os.path.isdir(args.out):
        shutil.rmtree(args.out)
    os.makedirs(os.path.join(args.out, "types"))
    groups = {}
    search = []
    for tid in sorted(types):
        t = types[tid]
        t["docs"].pop("inheritdoc", None)
        t.pop("_primary", None)
        for m in t["members"]:
            m["docs"].pop("inheritdoc", None)
        with open(os.path.join(args.out, "types", tid + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(t, f, ensure_ascii=False, separators=(",", ":"))
        g = groups.setdefault(t.get("assembly"), {"name": t["assembly"], "namespaces": {}})
        summary = t["docs"].get("summary", "")
        short = re.split(r"(?<=[.!?])\s", re.sub(r"\[`?([^\]`]*)`?\]\([^)]*\)", r"\1", summary), 1)[0][:200]
        g["namespaces"].setdefault(t["namespace"] or "(global)", []).append(
            {"id": tid, "name": t["display"] if not t["outer"] else types[t["outer"]]["name"] + "." + t["display"], "kind": t["kind"], "summary": short})
        search.append([tid, sorted({m["name"] for m in t["members"]})])

    assemblies = []
    for s in sources(args.prowl, args.anthology):
        g = groups.get(s["assembly"])
        if g:
            assemblies.append({"name": g["name"], "group": s["group"], "repo": s["repo"],
                               "namespaces": [{"name": n, "types": ts} for n, ts in sorted(g["namespaces"].items())]})
    index = {
        "version": 1,
        "commits": {"prowl": git_head(args.prowl) if args.prowl else None, "anthology": git_head(args.anthology) if args.anthology else None},
        "assemblies": assemblies,
        "search": search,
    }
    with open(os.path.join(args.out, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    members = sum(len(t["members"]) for t in types.values())
    documented = sum(1 for t in types.values() if t["docs"].get("summary")) + sum(1 for t in types.values() for m in t["members"] if m["docs"].get("summary"))
    print(f"{files} files, {len(types)} types, {members} members, {documented * 100 // max(1, len(types) + members)}% documented -> {args.out}/")
    for a in assemblies:
        print(f"  {a['name']:<22} {sum(len(n['types']) for n in a['namespaces']):>5} types")
    return 0


if __name__ == "__main__":
    sys.exit(main())
