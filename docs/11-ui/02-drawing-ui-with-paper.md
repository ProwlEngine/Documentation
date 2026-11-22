---
title: Drawing UI with Paper
description: Draw a HUD or debug panel from code every frame with Paper's immediate-mode API.
---

**Paper** is Prowl's immediate-mode UI library. You describe the UI in code every frame, and Paper lays it out and draws it. You use it for HUDs, debug panels and tools that are easier to write than to build from GameObjects. The editor itself is built with Paper.

For a UI you build and save in the scene, use a [GameCanvas](01-getting-started-with-ui.md) instead.

## Quick recipe

Override `OnGui` in a component. It runs once per frame while the game plays. This script shows a clickable counter in the top-left corner.

```csharp
using Prowl.PaperUI;
using Prowl.Runtime;
using Prowl.Runtime.Resources;
using Prowl.Scribe;
using Prowl.Vector;

public sealed class ScoreHud : Component
{
    private int _score;

    public override void OnGui(Paper paper)
    {
        FontFile font = FontAsset.LoadDefault().FontFile;
        if (font == null) return;

        paper.Box("score").Margin(20).Width(200).Height(40)
            .BackgroundColor(new Color(1f, 1f, 1f, 0.2f)).Rounded(6)
            .Hovered.BackgroundColor(new Color(1f, 1f, 1f, 0.4f)).End()
            .Text($"Score {_score}", font).FontSize(18).TextColor(Color.White)
            .Alignment(TextAlignment.MiddleCenter)
            .Cursor(PaperCursor.Pointer)
            .OnClick(_ => _score++);
    }
}
```

You see a translucent box with the score at the top-left of the game. Clicking it adds one.

[screenshot needed: the Game view with the Score box in the top-left corner]

## How it runs

Each frame the engine calls `BeginFrame` on one `Paper` instance, then calls `OnGui(paper)` on every enabled component, then ends the frame. You never create the `Paper` yourself. It draws over the finished game image.

A `Game` subclass has the same hook, `OnGui(Paper paper)`. Use it for UI that is not tied to a component.

Two helper types connect Paper to the engine:

| Type | Job |
| --- | --- |
| `PaperInputBridge` | Copies the engine's pointer, buttons, wheel, keys and text into a Paper instance each frame. |
| `PaperRenderer` | Draws Paper's output with Graphite, the engine's renderer. |

The engine calls both for you. In the editor, the Game view runs its own Paper instance, so `OnGui` runs there only while you play.

## Keep clicks out of the game

Paper does not stop your game code from also seeing a click. Check `paper.WantsCapturePointer`. It is true while the pointer is over a Paper element.

```csharp
if (Input.GetMouseButtonDown(0) && !paper.WantsCapturePointer)
    Fire();
```

## Where the Paper docs live

This page only covers how Paper is hosted in Prowl. Paper itself is part of the Anthology libraries and has its own guides in the `Anthology/Paper/docs` folder of the Anthology repository:

- `getting-started.md`: set up and first frame
- `elements-and-hierarchy.md`: boxes, rows and columns
- `layout-engine.md`: sizing and positioning
- `styling-and-animation.md`: colors, states and transitions
- `events-and-input.md`: clicks, hover, drag and keys
- `text-and-input-fields.md`: text and text boxes

Origami, a set of ready-made widgets for Paper, is in `Anthology/Origami/docs`.

## See also

- [Getting started with UI](01-getting-started-with-ui.md)
- [Anthology libraries](../08-anthology/index.md)
