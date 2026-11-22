---
title: Assets and importers
description: What the editor does with files in your Assets folder, how .meta files and import settings work, and how to load assets or write an importer.
---

An **asset** is a file in your project that the engine can load, such as a model, texture, sound or scene. An **importer** is the editor code that turns a source file into an asset. This page explains what happens when you drop a file into the project, and how to control it.

## The Assets folder

Everything you want in the game lives under the `Assets` folder of your project. The editor watches it. When a file appears or changes, the editor picks an importer by file extension and **imports** the file: it reads the source and builds the runtime objects.

Your source file is never modified. A `.png` stays a `.png`, and the imported texture is built from it.

Files with no matching importer are tracked but produce no asset.

## Meta files

Next to every asset the editor writes a `.meta` file: `Hero.fbx` gets `Hero.fbx.meta`. It is a small text file with four entries.

| Entry | Holds |
| --- | --- |
| `guid` | The asset's permanent unique ID (GUID) |
| `importer` | The importer used for this file |
| `importerVersion` | The importer version that last imported it |
| `settings` | The import settings, if the importer has any |

Commit `.meta` files with your assets. Other assets point at this one by `guid`, so a lost meta file means a new GUID and broken references.

> [!WARNING]
> Move and rename assets inside the editor's Project panel. If you copy a file with its `.meta`, both files share one GUID.

The `Library` folder holds caches. The default `.gitignore` leaves it out.

## Import settings

Select an asset in the Project panel to see its import settings in the Inspector. A texture has its own options, a model has rig and clip options, and so on.

1. Change a setting.
2. Press **Apply**. The editor writes the setting to the `.meta` file and re-imports the asset.
3. Press **Revert** to go back to the last applied values.

To re-import by hand, right-click an asset and choose **Reimport**, or right-click empty space in the Project panel and choose **Reimport All**. The editor also re-imports an asset when its source file is newer, or when the importer's version changes.

## Sub-assets

One file can import as several assets. A model file imports as a prefab plus **sub-assets**: its meshes, materials, avatar and animation clips. See [Importing a character](../05-animation/index.md#importing-a-character).

Each sub-asset has its own GUID, derived from the parent's GUID. Its path is the parent's path, then `#`, then its name: `Models/Hero.fbx#Run`.

## The asset database

The **asset database** is the editor's index of every asset: GUID, path, type and dependencies. See [Asset Database panel](06-debugging-and-profiling.md#asset-database-panel) to open it.

## References

A reference to an asset is saved as its GUID, not its path. You can rename or move a file and every scene, prefab and component that uses it still finds it.

Any plain field of an asset type, such as `public Texture2D Icon;`, is such a reference. It loads with the object that holds it.

An `AssetRef<T>` is a reference that does not load anything. Use it for assets you may never need, such as a list of levels. A build still ships what it points at.

| Call | Does |
| --- | --- |
| `Get()` | Returns the asset, loaded or not. Never loads |
| `LoadImmediate()` | Loads and returns the asset. Blocks |
| `LoadAsync()` | Loads without blocking. Await it |

## Load an asset from a script

Prefer a plain field or an `AssetRef<T>`. To load by name, use `AssetDatabase.FindResource<T>`. It only finds assets inside a folder named `Resources`, and the path is relative to that folder with no extension.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public class IconLoader : Component
{
    public override void Start()
    {
        Texture2D icon = AssetDatabase.FindResource<Texture2D>("Icons/Sword");
        PrefabAsset hero = AssetDatabase.FindResource<PrefabAsset>("Models/Hero");
    }
}
```

`Assets/Resources/Icons/Sword.png` loads as `Icons/Sword`. Add `#Name` for a sub-asset. `FindResourceAsync<T>` loads without blocking.

> [!WARNING]
> A build leaves out an asset you load only by path unless it is in a `Resources` folder. See [What ships](05-building-your-game.md#what-ships).

## Write a custom importer

An importer is a class that extends `AssetImporter` and carries `[ImporterFor]` with the file extensions it handles. Put it in a folder named `Editor`, so it compiles into the editor assembly (see [Editor code and game code](03-extending-the-editor.md#editor-code-and-game-code)). The editor finds it on its own.

This example turns `.note` text files into a `Note` asset.

```csharp
// Assets/Note.cs
using Prowl.Runtime;

public sealed class Note : Asset
{
    public string Text = "";

    public Note() : base("Note") { }
}
```

```csharp
// Assets/Editor/NoteImporter.cs
using System.IO;
using Prowl.Editor.Importers;

[ImporterFor(".note")]
public class NoteImporter : AssetImporter
{
    public override int Version => 1;

    public override bool Import(ImportContext ctx)
    {
        ctx.SetMainAsset(new Note { Name = ctx.FileName, Text = File.ReadAllText(ctx.AbsolutePath) });
        return true;
    }
}
```

Add a `.note` file to `Assets` and it imports as a `Note`. Raise `Version` whenever the import logic changes, and the editor re-imports every `.note` file.

## See also

- [Extending the editor](03-extending-the-editor.md)
- [Building your game](05-building-your-game.md)

