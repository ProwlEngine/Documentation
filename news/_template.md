---
title: The headline of your post
date: 2026-11-01
author: Your Name
summary: One sentence shown under the title in the news list and on the home page.
cover: images/your-post-cover.webp
tags: [release]
---

<!--
  To write a post:
    1. Copy this file to news/YYYY-MM-DD-your-post.md. The date and the rest of the name
       become the post's date and link, for example news/2026-11-01-preview-6.md.
    2. Put its images in news/images/. Paths below are relative to news/.
    3. Fill in the frontmatter above. Only title and date are required.
  Files starting with an underscore, like this one, are never published.

  Fields:
    title    The headline.
    date     YYYY-MM-DD. Taken from the file name if left out. Newest posts come first.
    author   Shown on the post. Optional.
    summary  One sentence for the news list. Optional.
    cover    The image on the news list and at the top of the post. Optional.
    tags     Filters on the news page, for example [release], [rendering, deep-dive].
    slug     Optional. Overrides the link taken from the file name.
-->

The opening paragraph. Say what happened or what this post is about in a sentence or two.

## A section heading

Write the body in Markdown. Headings, lists, links, tables and code all work, and `##` and
`###` headings appear in the post's outline.

- A list item
- Another one, with a [link to the docs](../docs/01-getting-started/01-installation.md)

![Describe what the image shows](images/your-post-screenshot.webp)

```csharp
// Code blocks are highlighted. Tag them with a language: csharp, glsl, bash, json.
public sealed class Example : Component { }
```

> [!NOTE]
> Callouts work too: NOTE, TIP, IMPORTANT, WARNING and CAUTION.

## What's next

Close with what's coming, or where readers can try it.
