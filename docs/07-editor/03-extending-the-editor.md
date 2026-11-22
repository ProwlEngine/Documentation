---
title: Extending the editor
description: Add menu items, custom inspectors, editor windows and startup code to the Prowl editor from C# scripts.
---

You extend the editor with ordinary C# scripts. The editor scans your scripts for attributes and base classes. It adds what it finds: menu entries, inspectors, windows and startup code. Use this to build tools for your own project, such as a level generator or a nicer inspector for one of your components.

Editor code is compiled apart from game code. See [Editor code and game code](#editor-code-and-game-code).

## Add a menu item

Create `Assets/Editor/HelloMenu.cs`:

```csharp
using Prowl.Editor;
using Prowl.Runtime;

public static class HelloMenu
{
    [MenuItem("Tools/Say Hello")]
    static void SayHello() => Debug.Log("Hello from the editor");
}
```

When the scripts finish compiling, a **Tools** menu appears in the menu bar. Choose **Say Hello** and the message shows in the Console.

The method must be `static`, return `void` and take no parameters. The path is slash separated, and each segment before the last is a submenu. Existing menus work too: `GameObject/...` and `Assets/Create/...` add to the built-in menus.

To grey the item out, add a second method with the same path and `isValidate: true`. It returns `true` when the item is usable:

```csharp
[MenuItem("Tools/Say Hello", isValidate: true)]
static bool CanSayHello() => !Application.IsPlaying;
```

`MenuItem` also takes `priority` (lower sorts first, default 1000) and `Separator = true` to draw a line above the item.

## Editor code and game code

Prowl compiles your scripts into two assemblies. Any script with a folder named `Editor` anywhere in its path under `Assets` goes into the editor assembly. Every other script goes into the game assembly.

- Editor code can use game code.
- Game code cannot use editor code. A reference to an editor type is a compile error.
- Only the game assembly is shipped in a build. The editor assembly is left out.

An assembly definition (`.asmdef`) that is included only for the Editor platform also makes its scripts editor code.

## Customize a component's inspector

A **custom editor** replaces how the Inspector draws one type. Given this component:

```csharp
using Prowl.Runtime;

public class Health : Component
{
    public float Max = 100;
    public float Current = 100;
}
```

Add `Assets/Editor/HealthEditor.cs`:

```csharp
using Prowl.Editor.Core;
using Prowl.Editor.GUI;
using Prowl.OrigamiUI;
using Prowl.PaperUI;

[CustomEditor(typeof(Health))]
public class HealthEditor : CustomEditor
{
    public override void OnGUI(Paper paper, string id, object target)
    {
        var health = (Health)target;

        DrawDefaultInspector(paper, $"{id}_def", target);

        Origami.Button(paper, $"{id}_heal", "Heal to full", () =>
        {
            Undo.RecordObject(health, "Heal to full");
            health.Current = health.Max;
        }).Show();
    }
}
```

Select a GameObject with a `Health` component. The Inspector shows the usual fields, with a **Heal to full** button below them.

- `OnGUI` runs every frame the Inspector is visible. `target` is the component being drawn.
- `DrawDefaultInspector` draws the standard field list. Leave it out to draw every field yourself.
- Call `Undo.RecordObject` before you change a value, so Undo reverts it.
- Build the UI with `Origami` widgets (the editor's UI widget library) and `EditorGUI.Row`, as the built-in editors do. Every ID must be unique, so prefix them with `id`.

A custom editor applies to the type you name and to types derived from it. This works for any type, not only components.

## Add an editor window

An editor window is a class that derives from `DockPanel`. It docks and tabs like the built-in panels. Add `Assets/Editor/ClickCounter.cs`:

```csharp
using Prowl.Editor;
using Prowl.Editor.Core;
using Prowl.OrigamiUI;
using Prowl.PaperUI;

public class ClickCounter : DockPanel
{
    [MenuItem("Window/Click Counter")]
    static void Open() => EditorApplication.Instance?.OpenPanel<ClickCounter>();

    public override string Title => "Click Counter";

    int _clicks;

    public override void OnGUI(Paper paper, float width, float height)
    {
        using (paper.Column("cc_root").Width(width).Height(height).Padding(8).Gap(6).Enter())
        {
            Origami.Label(paper, "cc_label", $"Clicks: {_clicks}").Show();
            Origami.Button(paper, "cc_button", "Click me", () => _clicks++).Show();
        }
    }
}
```

Choose **Window > Click Counter**. A panel opens with a label and a button, and the count goes up on each click.

`OpenPanel` opens a new panel, or focuses it if one is already open. `OnGUI` runs every frame with the panel's size. Fields on the class keep their values while the panel stays open.

Override `Icon` to set the tab icon and `OnClosed` to clean up when the panel closes.

## Run code when the editor loads

Mark a `static` method with `[InitializeOnLoad]`. The editor calls it after it scans your editor scripts, when a project opens and after every script reload.

```csharp
using Prowl.Editor;
using Prowl.Editor.Core;
using Prowl.Runtime;

public static class StartupLog
{
    [InitializeOnLoad]
    static void Init() => Debug.Log("Editor scripts loaded");

    [OnSceneSaved]
    static void AfterSave() => Debug.Log("Scene saved");
}
```

The first message appears in the Console when the project opens and whenever scripts recompile. The second appears each time you save a scene.

The method runs again on every reload, so make it safe to run repeatedly. `[OnUndoRedo]` works like `[OnSceneSaved]` and fires after each undo or redo.

## See also

- [Assets and importers](04-assets-and-importers.md) for custom importers
- [Building your game](05-building-your-game.md)
