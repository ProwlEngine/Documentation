# Prowl docs writing guide

Every agent that writes or edits a doc page reads this first. The goal is docs that read like the Unity manual: calm, short, exact, and easy to scan.

## Who is reading

- They found this page through a link or search. They may know nothing about the topic.
- They may never have made a game. They can read code. Do not talk down to them.
- Core engine ideas (GameObject, Component, Scene, Inspector) are known unless the page is in Getting Started.
- The page's own subsystem is NOT known. Explain it. Example: a page on culling explains culling and batching, not what a scene is.

## Page shape

1. Title. A short noun, or a task ("Play a clip").
2. Opening, two or three sentences:
   - What this is, in plain words.
   - What you use it for.
   - Link to the one page to read first, if any.
3. A quick recipe, as early as possible: a code snippet to copy and paste, or numbered steps that name the exact buttons. Show the result before the theory. See "Quick recipes" below.
4. Concepts: each in its own short section, defined at first use.
5. Tasks (how to do X), as short numbered steps.
6. Reference tables last.
7. "See also": two or three links at most.

Reference pages (node lists, property tables, include lists) skip steps 3 to 5. They open with a short list defining the terms the tables use, then one line on how to read the tables.

## Wording

- Sentences under 20 words. One idea each. Paragraphs of 1 to 3 sentences.
- Table cells are shorter: under 15 words, one sentence, no full stop needed if it is a fragment.
- Second person, present tense, active voice. "You wire the pin", not "the pin should be wired".
- Plain words. Prefer "use", "run", "set", "get", "start". Avoid "utilize", "leverage", "facilitate", "ensure".
- Define a term once, in bold, the first time it appears. After that use the same word every time. Never swap synonyms.
- Say what a thing is before what it does. "A pose is the position of every bone at one moment."
- Compare to a familiar idea when it helps (a light switch, a recipe), then drop the comparison.
- No filler or hype: "simply", "just", "easily", "powerful", "robust", "seamless", "obviously", "note that".
- No "we". No jokes. No rhetorical questions.
- Link a term to its page on first use. Do not re-explain what another page covers.
- On reference pages readers jump to one table. Put a one-sentence definition of any needed term in that category's intro, with a link.
- Keyboard characters only: no arrows, curly quotes, em dashes or fancy bullets. Write "A to B" or "->" never an arrow glyph.

## Quick recipes

Many readers want the result and nothing else. Every page gives them a way to get it fast.

- Each concept page has a copy-paste snippet or short numbered steps near the top, or a link to a how-to guide that does.
- A how-to guide answers one task, such as "Play an animation on a loop". The title is the task. It opens with the result in one sentence.
- Then 4 to 8 numbered steps. Each step is one action and names the exact menu, button or field. Include copy-paste code where code is needed.
- No concepts inside the steps. End with "Learn more" links to the pages that explain why it works.
- Mark each place a screenshot or GIF would help with a line: `[screenshot needed: what it should show]`. Agents cannot capture the editor.
- You may create new how-to pages when a task deserves a whole guide. Put them in `docs/09-how-to/`, numbered, and link them from the concept pages they relate to.

## Examples

- Smallest code that works. Complete enough to paste. Realistic names (`Health`, `Spinner`), not `Foo`.
- Comments only where behaviour is not obvious, two lines at most.
- Show what the reader should see after running it.
- Never use `?.`, `??` or `??=` on EngineObject types (GameObject, Component, Texture and so on). Use `IsValid()`.
- Prefer a short table over a paragraph for settings, options and comparisons.

## Callouts

Use `[!NOTE]`, `[!TIP]`, `[!WARNING]` sparingly. At most two per page. A warning is for something that silently breaks or loses data. Do not repeat the callout's point in the body.

## Accuracy

- Every name, default, menu path and signature is checked against the source. Search the code. Do not trust old docs.
- If something cannot be verified, leave it out and say so in your report. Never guess.
- Say each rule once. If a second page needs it, link.

## Length

State a word budget before writing. Typical: concept page 300 to 600 words, tutorial 500 to 800, reference as long as its table needs. After drafting, cut every sentence that does not help the reader act, then cut about a fifth more.

## Self-check before committing

- [ ] A newcomer can say what this page is about after the first three sentences.
- [ ] Every term is defined or linked before it is used.
- [ ] No sentence over 25 words. No paragraph over 3 sentences.
- [ ] The example runs and was checked against the code.
- [ ] No banned words, no non-keyboard characters.
- [ ] Nothing repeated from another page.
- [ ] Headings read well in the sidebar's "On this page" list.

## Git

Commit to main in the docs repo. Never push, merge, rebase or amend. Stage files by explicit path. Messages are plain, one line and capitalized, with no `docs(...)` prefix, for example `Explain Enter and Exit gates`.

One commit per logical change:

- A real fix is its own commit: a wrong default, a bad menu name, a missing definition.
- A new page is one commit, even if you wrote it section by section.
- A rewrite of one page is one commit.
- A sweep across many pages for one reason (spelling, links, wording, non-ASCII characters) is one commit, not one per page.
- Never split one change into many tiny commits, and never lump unrelated fixes into one.

## Report back

List the commits, the word count before and after, and anything you could not verify.
