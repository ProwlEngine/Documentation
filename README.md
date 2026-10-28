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

Copy `news/_template.md` to `news/YYYY-MM-DD-slug.md`, fill it in, and put its images in `news/images/`. The template explains every field. Its frontmatter looks like this:

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

## Adding your project to the showcase

Anyone can add a project made with Prowl to the website's showcase with a pull request.

1. Copy `showcase/_template` to `showcase/<your-project>`. The folder name becomes the project's link.
2. Put your images in that folder: a cover and any screenshots. 16:9 works best; WebP, PNG and JPG are fine.
3. Fill in `index.md`. Only `title` and `cover` are required.
4. Open a pull request.

| Field | Meaning |
| --- | --- |
| `title`, `summary` | The name, and one sentence for the grid |
| `author`, `author_url` | Who made it, and where to find them |
| `cover` | The image shown in the grid and at the top of the project page |
| `images` | Screenshots for the gallery, in order |
| `tags` | Filters on the showcase page, such as `[game, 2d, vr]` |
| `date` | `YYYY-MM-DD`; newest projects are listed first |
| `website`, `steam`, `itch`, `github`, `video` | Links shown as buttons on the project page |
| `pick` | Maintainers set `true` for Contributor picks at the top of the page |

### Featured images

`feature` lists the big captioned images shown when your project is a Contributor pick, and at the top of its page: full-width shots that fade into the black background. Without it, your cover is used.

```yaml
feature:
  - image: mars.webp
    title: Mars
    caption: Seen from orbit.
    width: full
  - image: exoplanet.webp
    title: An exoplanet
    caption: Half in night.
    width: narrow
    align: right
```

| Key | Values |
| --- | --- |
| `image` | A file in your project folder |
| `title`, `caption` | The label on the image. Both optional |
| `width` | `full` (edge to edge, the default), `wide` or `narrow` |
| `align` | Where the label sits: `left` (default), `right` or `center` |
| `fade` | `true` (default) fades the top and bottom into black; `false` shows the image's edges |

Images on black backgrounds, such as space or night scenes, look best, because their edges disappear into the page.

The text under the frontmatter is the project page, in Markdown.

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
