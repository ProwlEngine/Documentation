---
title: Prefabs
description: Save a GameObject as a reusable asset, edit it, override it per instance, and spawn it from a script.
---

A **prefab** is a GameObject, with its children and components, saved as an asset so you can reuse it. You place copies of it in scenes or spawn them from code. Each copy is an **instance**.

This page assumes you know [GameObjects and scenes](02-gameobjects-and-scenes.md).

## Quick recipe

Add this component to an object, drag a prefab from the **Project** panel into its **Prefab** field, and press Play. Pressing F spawns one copy at the spawner's position.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class Spawner : Component
{
    public PrefabAsset Prefab;
    public KeyCode Key = KeyCode.F;

    public override void Update()
    {
        if (Prefab.IsValid() && Input.GetKeyDown(Key))
            GameObject.Instantiate(Prefab, Transform.Position, Transform.Rotation);
    }
}
```

[screenshot needed: the Spawner in the Inspector with a prefab assigned]

## Make a prefab

1. Build the object in the scene.
2. Right-click it in the **Hierarchy** and choose **Create Prefab**. Or select it and use **Assets > Create > Prefab From Selection**.
3. A `.prefab` file appears in the current **Project** folder. The object in the scene becomes an instance of it.

You can also drag an object from the **Hierarchy** into the **Project** panel. Drag a prefab back into the **Hierarchy** or **Scene** view to place another instance. See [Assets and importers](../07-editor/04-assets-and-importers.md) for how assets are stored.

An instance shows a **Prefab** banner at the top of its **Inspector**.

## Edit the prefab

Right-click an instance and choose **Open Prefab**, or select the prefab in the **Project** panel and click **Open Prefab** in its **Inspector**. The prefab opens in a [world](05-scenes-and-worlds.md) of its own, and your scenes wait underneath.

Change it, then click **Save & Exit** in the **Hierarchy**. Every instance in your open scenes updates. Prefab editing is unavailable during play.

A model file you import, such as an FBX, is also a prefab. It is read-only, because the importer rebuilds it from the file.

## Overrides

An **override** is a change you make to one instance that differs from its prefab. Change a value in the **Inspector** and that instance keeps its value while the others follow the prefab.

An instance with overrides shows **Revert** and **Apply** in its banner:

| Action | Effect |
| --- | --- |
| **Revert** | Throws away the overrides and matches the prefab again |
| **Apply** | Writes the overrides into the prefab, so every instance gets them |
| **Break Prefab Instance** | Right-click menu. Turns the instance into plain objects |

Apply is unavailable for generated prefabs such as models. Revert still works.

## Nesting

Prefabs do not nest. When you save an object that contains instances of other prefabs, those instances become plain objects inside the new prefab. Dropping a prefab into one you are editing asks you to confirm the same flattening.

## Spawn from a script

`GameObject.Instantiate` builds a copy and puts it in a world. Each overload returns the new object, or null and a console error when it cannot spawn.

| Call | Where it lands |
| --- | --- |
| `Instantiate(prefab)` | The active world's active section, at the prefab's own transform |
| `Instantiate(prefab, position, rotation)` | The same, placed before `OnEnable` runs |
| `Instantiate(prefab, parent)` | Under `parent`, in its section |
| `Instantiate(prefab, scene)` | A specific `SceneInstance` |

The `parent` overload takes a `worldPositionStays` argument, off by default, so the prefab's transform becomes an offset from the parent. A null `parent` spawns the prefab at the active scene's root. Worlds and sections are covered in [Scenes and worlds](05-scenes-and-worlds.md).

`GameObject.Instantiate(original)` and its variants copy a scene object instead of a prefab. `InstantiateDetached(prefab)` builds the hierarchy without adding it to any world.

An instance reports `IsPrefabInstance` and `HasPrefabOverrides`.

### Plain field or AssetRef

A `PrefabAsset` field keeps the prefab and every asset it uses loaded, so spawning never waits. Use it for anything you spawn often.

An `AssetRef<PrefabAsset>` stores only the asset's ID. `Get()` returns it if already loaded, `LoadImmediate()` loads it and blocks, and `LoadAsync()` loads without blocking. Use it for rare or optional prefabs.

```csharp
public AssetRef<PrefabAsset> Boss;

void SpawnBoss() => GameObject.Instantiate(Boss.LoadImmediate(), Transform.Position, Transform.Rotation);
```

### Destroy

```csharp
GameObject enemy = GameObject.Instantiate(Prefab, Transform.Position, Transform.Rotation);
if (enemy.IsValid()) enemy.Destroy();
```

`Destroy()` removes the object at the end of the frame. See [GameObjects and scenes](02-gameobjects-and-scenes.md#spawning-and-destroying).

> [!WARNING]
> A prefab cannot hold references to scene objects. Those references load as null in each instance, so assign them from code after you spawn. See [Serialization](07-serialization.md).

## See also

- [Spawn a prefab](../09-how-to/03-spawn-a-prefab.md)
- [Multi-scene editing](../07-editor/02-multi-scene-editing.md)
