---
title: Project settings
description: Where the project-wide settings live in the editor, what each page controls, how they are saved, and how to add tags and layers.
---

**Project settings** are options that apply to the whole game, such as gravity, audio quality and the fixed timestep. You edit them in one panel, and the editor saves them with your project. For options that belong to you and not the project, see Preferences at the end of this page.

Open the panel with **Edit > Project Settings...**. Pick a page in the sidebar.

## Quick recipe: add a layer and use it

A **layer** is a named group of objects. Physics and rendering use layers to decide what interacts. The names are shared by the whole project.

1. Choose **Edit > Project Settings...** and select **Tags & Layers**.
2. Under **Layers**, type `Enemy` into the empty **Layer 5** field.
3. Select an object in the Hierarchy.
4. In the Inspector, open the **Layer** dropdown and choose `Enemy`.

[screenshot needed: Tags & Layers page with Enemy typed into Layer 5]

To set it from a script, assign the layer by name:

```csharp
using Prowl.Runtime;

public class EnemyMarker : Component
{
    public override void Start()
    {
        GameObject.Layer = "Enemy";
    }
}
```

An unknown name sets the layer index to -1, so spell it as in the panel. Matching ignores case.

## Settings pages

Each page controls one area. The sidebar lists them in this order.

| Page | Controls |
| --- | --- |
| General | Company name, product name and version |
| Editor | Editor color palette, background image and extra Game view sizes |
| Tags & Layers | The project's tag and layer names |
| Physics | Gravity, solver and sub-step counts, and the layer collision matrix |
| Navigation | Navigation agent types, area names and area costs |
| Time | Fixed timestep, maximum fixed steps per frame and default time scale |
| Quality | Quality levels (shadows, render scale, reflections) and the active level |
| Audio | Global volume, sample rate, channels and buffer size |
| XR | Whether to start XR in play mode and in the player, tracking origin, render scale |
| Assets | How long unused assets stay loaded, the player memory budget, mesh distance fields |
| Code Style | Formatting and diagnostics rules, written to `.editorconfig` |

The Build settings page is hidden from this panel. See [Building your game](05-building-your-game.md).

## Where settings are stored

Each page is saved as a YAML file named after the page, in the `ProjectSettings` folder at the project root:

```text
ProjectSettings/
  General.yaml
  Physics.yaml
  Tags & Layers.yaml
  Quality.yaml
```

Commit this folder. The default `.gitignore` does not exclude it, and your team needs the same layers, gravity and quality levels.

Most edits save at once. **Edit > Save Layout** saves every page. A missing file means the page uses its defaults.

A build copies every page except Editor, Code Style and Build into the player. The player reads them at startup.

## Tags and layers

A **tag** is a label for finding or recognizing objects, such as `Player`. A layer is a group for filtering. An object has one tag and one layer.

To add a tag:

1. Open **Tags & Layers** and press **Add Tag**.
2. Rename the new `New Tag` row.
3. Select an object and pick the tag in the Inspector's **Tag** dropdown.

Test a tag from a script with `GameObject.CompareTag("Boss")`. The first seven tags are built in and locked. Use the **x** button to delete one of your own.

There are 32 layer slots. The first four are locked, and an empty name marks an unused slot. A name that another slot already uses is refused.

The **Layer Collision Matrix** in **Physics** sets which layers collide. See [Layers and collision](../06-physics/05-layers-and-collision.md).

## Read a setting from a script

The runtime values are static, so a script reads them directly. In a build, the player sets them from the saved files.

```csharp
using Prowl.Runtime;

public class SettingsProbe : Component
{
    public override void Start()
    {
        Debug.Log($"Fixed step: {Time.FixedDeltaTime}s");
        Debug.Log($"Quality: {QualitySettings.Active.Name}");
        QualitySettings.SetActive("Low");
    }
}
```

`SetActive` takes a level name or an index. It changes the active level for the running game only. The saved choice in **Quality** stays as it is.

## Preferences

**Edit > Preferences...** holds editor options that belong to you, such as the theme and shortcuts. They are not part of the project and are not committed.

## See also

- [Building your game](05-building-your-game.md) for build settings
- [Layers and collision](../06-physics/05-layers-and-collision.md)
