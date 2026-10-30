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
export function parseFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!m) return { data: {}, body: text };
  return { data: parseYamlLite(m[1]), body: text.slice(m[0].length) };
}

// A small YAML subset: `key: value`, quoted strings, `[a, b]` lists, and a key followed by an indented
// list of `- key: value` entries, as used by `feature:` in showcase projects.
export function parseYamlLite(src) {
  const data = {};
  const lines = src.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const kv = /^([A-Za-z0-9_-]+)\s*:\s*(.*)$/.exec(lines[i]);
    if (!kv) continue;
    const raw = kv[2].trim();
    if (raw !== "") { data[kv[1]] = scalar(raw); continue; }
    const items = []; let cur = null;
    while (i + 1 < lines.length && /^(\s+|-\s)/.test(lines[i + 1])) {
      let t = lines[++i].trim();
      if (!t || t.startsWith("#")) continue;
      if (t.startsWith("- ")) {
        t = t.slice(2).trim();
        const inner = /^([A-Za-z0-9_-]+)\s*:\s*(.*)$/.exec(t);
        if (inner) { cur = {}; items.push(cur); cur[inner[1]] = scalar(inner[2].trim()); }
        else { cur = null; items.push(scalar(t)); }
      } else {
        const inner = /^([A-Za-z0-9_-]+)\s*:\s*(.*)$/.exec(t);
        if (inner && cur) cur[inner[1]] = scalar(inner[2].trim());
      }
    }
    data[kv[1]] = items.length ? items : "";
  }
  return data;
}
function scalar(v) {
  if (v.startsWith("[") && v.endsWith("]")) return v.slice(1, -1).split(",").map(s => unquote(s.trim())).filter(Boolean);
  v = unquote(v);
  return /^-?\d+(\.\d+)?$/.test(v) ? Number(v) : v;
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

// ---------- showcase ----------
// One folder per project: showcase/<slug>/index.md, with its images beside it.
function readShowcase() {
  const picksPath = join(ROOT, "showcase", "picks.txt");
  const picks = existsSync(picksPath)
    ? readFileSync(picksPath, "utf8").split(/\r?\n/).map(l => l.replace(/#.*/, "").trim().toLowerCase()).filter(Boolean)
    : [];

  if (!existsSync(join(ROOT, "showcase"))) return [];
  const out = [];
  for (const name of readdirSync(join(ROOT, "showcase"))) {
    if (name.startsWith("_") || name.startsWith(".")) continue;   // _template and drafts
    const dir = rel("showcase", name);
    if (!statSync(join(ROOT, dir)).isDirectory()) continue;
    const path = rel(dir, "index.md");
    if (!existsSync(join(ROOT, path))) { warnings.push(`${dir}: no index.md`); continue; }
    const { data, body } = parseFrontmatter(read(path));
    if (data.pick !== undefined) warnings.push(`${path}: "pick" is ignored; Contributor picks are set in showcase/picks.txt`);
    const file = f => posix.normalize(posix.join(dir, String(f)));
    const images = [].concat(data.images || []).filter(Boolean).map(file);
    const cover = data.cover ? file(data.cover) : images[0] || null;
    for (const img of [cover, ...images].filter(Boolean))
      if (!existsSync(join(ROOT, img))) warnings.push(`${path}: image ${img} does not exist`);
    if (!data.title) warnings.push(`${path}: no title`);
    if (!cover) warnings.push(`${path}: no cover image`);
    // Contributor picks and project pages render these as full-width images with captions
    const feature = [].concat(data.feature || []).filter(f => f && typeof f === "object" && f.image).map(f => {
      const image = file(f.image);
      if (!existsSync(join(ROOT, image))) warnings.push(`${path}: feature image ${image} does not exist`);
      return {
        image,
        title: f.title ? String(f.title) : "",
        caption: f.caption ? String(f.caption) : "",
        width: ["full", "wide", "narrow"].includes(f.width) ? f.width : "full",
        align: ["left", "right", "center"].includes(f.align) ? f.align : "left",
        fade: String(f.fade).toLowerCase() !== "false",
      };
    });
    const links = {};
    for (const k of ["website", "steam", "itch", "github", "video", "download"]) if (data[k]) links[k] = String(data[k]);
    out.push({
      slug: name.toLowerCase(),
      title: data.title || firstHeading(body) || prettify(name),
      author: data.author ? String(data.author) : "",
      authorUrl: data.author_url ? String(data.author_url) : "",
      summary: data.summary ? String(data.summary) : "",
      date: String(data.date || ""),
      cover,
      images,
      tags: [].concat(data.tags || []).map(String),
      links,
      feature,
      pick: picks.includes(name.toLowerCase()),
      pickOrder: picks.includes(name.toLowerCase()) ? picks.indexOf(name.toLowerCase()) : null,
      path,
    });
  }
  return out.sort((a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title));
}
function checkPicks(showcase) {
  const picksPath = join(ROOT, "showcase", "picks.txt");
  if (!existsSync(picksPath)) return;
  const slugs = new Set(showcase.map(p => p.slug));
  for (const l of readFileSync(picksPath, "utf8").split(/\r?\n/)) {
    const slug = l.replace(/#.*/, "").trim().toLowerCase();
    if (slug && !slugs.has(slug)) warnings.push(`showcase/picks.txt: no project folder named "${slug}"`);
  }
}

// ---------- write ----------
const index = {
  version: 1,
  docs: existsSync(join(ROOT, "docs")) ? walkDocs("docs", []) : [],
  news: readNews(),
  showcase: readShowcase(),
};
checkPicks(index.showcase);
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
console.log(`index.json: ${count(index.docs)} docs entries, ${index.news.length} news posts, ${index.showcase.length} showcase projects`);
for (const w of warnings) console.warn("warning: " + w);
if (missing.length) console.log(`${missing.length} images still to capture (see SCREENSHOTS.md); the website shows placeholders for them`);
