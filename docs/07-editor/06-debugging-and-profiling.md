---
title: Debugging and profiling
description: Find out what your game is doing with logs, gizmos, the Console, Frame Stats, the render profiler and the Asset Database panel.
---

This page covers the tools for seeing what your game does: messages in the Console, shapes drawn in the scene, and panels that measure time and memory. Use them when something looks wrong, runs slowly or fails to load.

## Quick recipe: log a message and draw a shape

1. Add this component to a GameObject.
2. Open **Window > General > Console** and press Play.
3. Select the object. A yellow wire sphere appears in the Scene view, and the Console shows one line.

```csharp
using Prowl.Runtime;
using Prowl.Vector;

public class SpawnPoint : Component
{
    public float Radius = 2f;

    public override void Start() => Debug.Log($"Spawn point ready: {GameObject.Name}");

    public override void DrawGizmosSelected()
        => Debug.DrawWireSphere(Transform.Position, Radius, Color.Yellow);
}
```

[screenshot needed: the Scene view with a yellow wire sphere around the selected object and the Console showing the log line]

## Logging

`Debug.Log`, `Debug.LogWarning`, `Debug.LogError` and `Debug.LogSuccess` write a line at that **severity**. `Debug.LogException(context, exception)` logs an exception with its stack trace.

`Debug.LogOnce`, `LogWarningOnce` and `LogErrorOnce` take an id and print only the first time, which keeps a per-frame message from flooding the Console.

Anything your code writes with `Console.WriteLine` or `Console.Error.WriteLine` also reaches the Console, as a warning and an error.

## The Console panel

Open it from **Window > General > Console**. It lists every log with its severity and time.

| Feature | What it does |
| --- | --- |
| Filter box | Shows only logs containing your text |
| Severity toggles | Hide normal, warning or error logs |
| Collapse | Merges identical lines and shows a count |
| Show Time, Multi Line | Adds timestamps, or shows whole messages |
| Clear | Removes every log |
| Right-click a log | Copy, Copy Message, Copy With Stack Trace, Open Source |

Open Source jumps to the line of your script that logged the message.

## Gizmos and debug drawing

A **gizmo** is a shape the editor draws over the scene to show something that is otherwise invisible, such as a trigger radius. Override these on any component:

| Method | Draws |
| --- | --- |
| `DrawGizmos()` | Always, for every object with the component |
| `DrawGizmosSelected()` | Only while the object is selected |

Inside them, call `Debug.DrawLine`, `DrawWireCube`, `DrawWireSphere`, `DrawWireCapsule`, `DrawArrow`, `DrawAxes` and the other `Debug.Draw*` helpers. They draw only in the editor and do nothing in a built game.

Gizmos show in the Scene view when **Show Gizmos** is on in its toolbar. The Game view has its own **Show Gizmos** toggle in its **Game Settings** menu. The Scene view's gizmo menu also hides gizmos per component type.

## Frame Stats

**Window > Debug > Frame Stats** charts where each frame's time goes, split into categories such as Update, Physics, Animation and Render.

Click a column to pause on it, and click a category to hide it. The toolbar chooses the refresh interval, average or max stacking, and the chart scale. A 16 ms line is the budget for 60 frames per second.

To time your own code, wrap it in a scope. It appears as its own category.

```csharp
using (FrameStats.Scope("Game/Pathfinding"))
    RunPathfinding();
```

"Game/Pathfinding" makes a Pathfinding subcategory under Game.

Turn on **Show Stats** in the Game view's **Game Settings** menu for an overlay of draw calls and frame time. `RenderStats.Last` holds the same numbers in code.

## Render Profiler and snapshots

A **snapshot** is a recording of one frame: every pass, draw command and render target. Three entries sit under **Window > Debug**:

| Menu item | Opens |
| --- | --- |
| Render Profiler | Live per-pass timing |
| Render Snapshots | The viewer for captured frames |
| Load Render Snapshot... | A saved snapshot file |

From the terminal, `prowl command snapshot --action capture` records the next frame. See [Prowl CLI](01-prowl-cli.md) for how to run commands.

## Debug views

In the Scene view, **View Settings > Debug View** replaces the lit picture with one property of the surfaces. The modes are Lit, Unlit, Albedo, Normals, Roughness, Metallic, AmbientOcclusion, Emission, Lighting, ShadowCascades and LightmapDensity. Shaders support them through the `GRAPHITE_DEBUG` keyword, described in [Variants and globals](../04-shaders/08-variants-and-globals.md).

## Asset Database panel

**Window > Debug > Asset Database** lists every asset with its type, state, size and load count. Select a row to see what it depends on and what uses it. Use the filter box and type dropdown to narrow the list, and right-click a row to unload it or reveal it in the Project panel.

## Missing assets and crashes

If an asset does not load, search for it in the Asset Database panel, then read the Console for import errors on that file.

If the editor closes without a message, look for `crash-<date>.log` in your project's `Logs` folder. When that folder cannot be written, the editor tries a `Logs` folder next to the editor program, then `ProwlEditor` in the system temp folder.

For scripts, read logs without the window open:

```bash
prowl command logs --level Error
prowl command screenshot --view Game
```

## See also

- [Prowl CLI](01-prowl-cli.md)
- [Assets and importers](04-assets-and-importers.md)
- [Variants and globals](../04-shaders/08-variants-and-globals.md)
