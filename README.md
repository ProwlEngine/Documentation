# Prowl Documentation

The docs and news posts for the Prowl website. Everything here is plain Markdown: the website
reads this repository directly, so merging a pull request publishes the change.

## Layout

```
docs/                     Documentation. Folders become sidebar sections.
  01-getting-started/
    index.md              Optional. The section's landing page, title and description.
    01-installation.md    A page.
news/                     News posts, one Markdown file each.
  2026-10-14-preview-5.md
  images/                 Images for posts (covers and inline images).
index.json                Generated. Do not edit by hand.
scripts/build-index.mjs   Generates index.json.
.github/workflows/        Runs the generator on every push to main.
```

## Writing a doc page

```markdown
---
title: Installation
description: Requirements, downloading a release and building from source.
---

Body text. Use `##` and `###` for headings; they build the "On this page" list and search.
```

- **Order** comes from the number prefix: `01-`, `02-`, ... The prefix is stripped from the URL,
  so `docs/01-getting-started/01-installation.md` becomes `getting-started/installation`.
  You can override it with `order: 3` in the frontmatter.
- **Titles** come from `title:`, then the first `# heading`, then the file name.
- **Sections** are folders. Add an `index.md` to give a section a title, a description and a
  landing page. Folders can nest.
- Files and folders starting with `_` or `.` are ignored, which is handy for drafts.

## Writing a news post

Name the file `YYYY-MM-DD-slug.md`:

```markdown
---
title: Prowl 1.0 Preview 5 is here
date: 2026-10-14
author: Prowl Team
summary: One sentence for the news list.
cover: images/preview-5.webp
tags: [release]
---
```

`cover` is relative to `news/`. The slug comes from the file name, or from `slug:` in the frontmatter.

## Links, images and callouts

- Link between pages with relative paths to the `.md` files, for example
  `[Components](../02-scripting/01-components.md)`. They work on GitHub and on the website.
- Images use relative paths too: `![Alt text](images/picture.webp)`.
- GitHub-style callouts are supported: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`.
- Fenced code blocks are highlighted. Tag them: ` ```csharp `, ` ```bash `, ` ```glsl `, ` ```json `.

## Images, GIFs and video

Each docs section keeps its images in its own `images/` folder, and animation nodes in
`docs/05-animation/images/nodes/`. Reference them with relative paths:

```markdown
![What the image shows](images/foliage-wind.gif)
![What the image shows](images/foliage-wind.gif "An optional caption under the image")
```

- PNG, JPG, WebP and GIF work. GIFs animate.
- `.mp4` and `.webm` play as silent, looping clips, and are far smaller than GIFs.
- **A missing image shows as a placeholder** on the website, with its description and path.
  `SCREENSHOTS.md` lists every image still to capture.
- Folders named `images`, `media` or `assets` never appear in the docs sidebar.

## index.json

The website reads `index.json` to build the sidebar, news list and search. The GitHub Action
regenerates it on every push to `main`, so normally you never touch it.

To check your changes locally, run:

```bash
node scripts/build-index.mjs
```

It prints warnings for missing titles, bad dates and covers that do not exist.

> The Action needs permission to push. In the repository go to Settings, Actions, General,
> and under Workflow permissions choose "Read and write permissions".

If `index.json` is missing, the website falls back to reading the folder structure through the
GitHub API. That works, but it is rate limited to 60 requests an hour per visitor, so keep
`index.json` in the repository.

## Sample content

The pages and posts included to start with are samples written for the website. Replace or edit
them freely. The news dates in particular are placeholders.
