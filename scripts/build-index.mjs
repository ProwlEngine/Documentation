// Builds index.json from the docs/ and news/ folders.
//
//   node scripts/build-index.mjs
//
// The website reads index.json to draw the docs sidebar, the news list and the search index
// without having to call the GitHub API. A GitHub Action runs this on every push to main.
// No dependencies: Node 18 or newer is all it needs.

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from "node:fs";
import { join, posix } from "node:path";

const ROOT = process.cwd();
const SKIP_DIRS = new Set(["images", "media", "assets"]);   // image folders are not sidebar sections
const warnings = [];

// ---------- frontmatter ----------
// A small YAML subset: `key: value`, quoted strings, and `[a, b, c]` lists.
export function parseFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!m) return { data: {}, body: text };
  const data = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z0-9_-]+)\s*:\s*(.*)$/.exec(line);
    if (!kv) continue;
    let v = kv[2].trim();
    if (v.startsWith("[") && v.endsWith("]")) {
      v = v.slice(1, -1).split(",").map(s => unquote(s.trim())).filter(Boolean);
    } else {
      v = unquote(v);
      if (/^-?\d+(\.\d+)?$/.test(v)) v = Number(v);
    }
    data[kv[1]] = v;
  }
  return { data, body: text.slice(m[0].length) };
}
function unquote(s) {
  return (s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'")) ? s.slice(1, -1) : s;
}

// ---------- helpers ----------
const ORDER = /^(\d+)[-_ ]/;
const slugOf = name => name.replace(/\.md$/i, "").replace(ORDER, "").toLowerCase();
const prettify = name => {
  const s = slugOf(name).replace(/[-_]+/g, " ");
  return s.charAt(0).toUpperCase() + s.slice(1);
};
const orderOf = (name, data) => (typeof data.order === "number" ? data.order : ORDER.test(name) ? Number(ORDER.exec(name)[1]) : 9999);
const firstHeading = body => (/^#\s+(.+)$/m.exec(body) || [])[1]?.trim();
const headingsOf = body =>
  body
    .replace(/```[\s\S]*?```/g, "")
    .split(/\r?\n/)
    .map(l => /^(#{2,3})\s+(.+?)\s*#*$/.exec(l))
    .filter(Boolean)
    .map(m => m[2].replace(/[`*_]/g, ""));
const read = p => readFileSync(join(ROOT, p), "utf8");
const rel = (...parts) => posix.join(...parts);

// ---------- docs ----------
function walkDocs(dir, slugPath) {
  const entries = readdirSync(join(ROOT, dir)).filter(n => !n.startsWith(".") && !n.startsWith("_") && !SKIP_DIRS.has(n.toLowerCase()));
  const nodes = [];
  for (const name of entries) {
    const path = rel(dir, name);
    if (statSync(join(ROOT, path)).isDirectory()) {
      const indexPath = rel(path, "index.md");
      const hasIndex = existsSync(join(ROOT, indexPath));
      const { data, body } = hasIndex ? parseFrontmatter(read(indexPath)) : { data: {}, body: "" };
      const slug = [...slugPath, slugOf(name)];
      nodes.push({
        type: "folder",
        slug: slug.join("/"),
        title: data.title || firstHeading(body) || prettify(name),
        description: data.description || "",
        path: hasIndex ? indexPath : null,
        headings: hasIndex ? headingsOf(body) : [],
        order: orderOf(name, data),
        children: walkDocs(path, slug),
      });
    } else if (/\.md$/i.test(name) && name.toLowerCase() !== "index.md") {
      const { data, body } = parseFrontmatter(read(path));
      const title = data.title || firstHeading(body);
      if (!title) warnings.push(`${path}: no title in frontmatter or # heading, using the file name`);
      nodes.push({
        type: "page",
        slug: [...slugPath, slugOf(name)].join("/"),
        title: title || prettify(name),
        description: data.description || "",
        path,
        headings: headingsOf(body),
        order: orderOf(name, data),
      });
    }
  }
  return nodes.sort((a, b) => a.order - b.order || a.slug.localeCompare(b.slug));
}

// ---------- news ----------
function readNews() {
  if (!existsSync(join(ROOT, "news"))) return [];
  return readdirSync(join(ROOT, "news"))
    .filter(n => /\.md$/i.test(n) && !n.startsWith("_"))
    .map(name => {
      const path = rel("news", name);
      const { data, body } = parseFrontmatter(read(path));
      const fileDate = (/^(\d{4}-\d{2}-\d{2})/.exec(name) || [])[1];
      const date = String(data.date || fileDate || "");
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) warnings.push(`${path}: date should be YYYY-MM-DD (frontmatter or file name)`);
      const cover = data.cover ? posix.normalize(posix.join("news", String(data.cover))) : null;
      if (cover && !existsSync(join(ROOT, cover))) warnings.push(`${path}: cover ${cover} does not exist`);
      return {
        slug: data.slug || name.replace(/\.md$/i, "").replace(/^\d{4}-\d{2}-\d{2}-/, ""),
        title: data.title || firstHeading(body) || prettify(name),
        date,
        author: data.author || "",
        summary: data.summary || "",
        cover,
        tags: Array.isArray(data.tags) ? data.tags : data.tags ? [String(data.tags)] : [],
        path,
      };
    })
    .sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
}

// ---------- write ----------
const index = {
  version: 1,
  docs: existsSync(join(ROOT, "docs")) ? walkDocs("docs", []) : [],
  news: readNews(),
};
writeFileSync(join(ROOT, "index.json"), JSON.stringify(index, null, 2) + "\n");

// Images referenced by Markdown that do not exist yet: the website shows placeholders for them
const missing = [];
(function scan(dir) {
  if (!existsSync(join(ROOT, dir))) return;
  for (const name of readdirSync(join(ROOT, dir))) {
    const path = rel(dir, name);
    if (statSync(join(ROOT, path)).isDirectory()) { scan(path); continue; }
    if (!/\.md$/i.test(name)) continue;
    for (const m of read(path).matchAll(/!\[[^\]]*\]\(([^)\s]+)/g)) {
      if (/^(https?:|data:)/i.test(m[1])) continue;
      const target = posix.normalize(posix.join(dir, m[1]));
      if (!existsSync(join(ROOT, target))) missing.push(target);
    }
  }
})("docs");

const count = n => n.reduce((s, x) => s + (x.type === "page" ? 1 : 1 + count(x.children)), 0);
console.log(`index.json: ${count(index.docs)} docs entries, ${index.news.length} news posts`);
for (const w of warnings) console.warn("warning: " + w);
if (missing.length) console.log(`${missing.length} images still to capture (see SCREENSHOTS.md); the website shows placeholders for them`);
