---
title: Load the next level
description: Switch to another scene when the player walks into a trigger.
---

You end with a doorway that loads a second level when an object tagged `Player` enters it. It needs two saved scenes and one small script.

## Steps

1. Build your second level in a new scene. Choose **File > New Scene**, add some objects, then **File > Save Scene As...** and name it `Level2`.
2. Open your first scene. Select the player object and set its **Tag** to `Player` in the **Inspector**. The player needs a **Rigidbody**.
3. In the **Project** panel, choose **Assets > Create > C# Script**, name it `LevelExit`, and paste the code below.
4. In the **Hierarchy**, create an empty object at the doorway. Click **Add Component > Physics > Trigger Volume**, then add **LevelExit** the same way.
5. Drag `Level2` from the **Project** panel onto the **Next Level** field of **LevelExit**.

[screenshot needed: the LevelExit component with Next Level filled, beside the Trigger Volume]

6. Press **Play** and walk the player into the volume. The game switches to `Level2`.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class LevelExit : Component
{
    public AssetRef<SceneAsset> NextLevel;

    public override void OnTriggerEnter(Rigidbody3D other)
    {
        if (other.GameObject.CompareTag("Player"))
            NextLevel.Load();
    }
}
```

## If it does not work

- **Nothing happens.** Check that the player has a **Rigidbody** and the tag `Player`, and that the trigger volume's layer mask includes the player's layer.
- **The field says None.** Drag the `.scene` asset from the **Project** panel. Save the scene first, or it is not an asset yet.
- **The game builds but never loads the level.** A scene reached only through the field still ships. Scenes you load by name need to be in the build list.

## Learn more

- [Loading scenes](../02-scripting/06-loading-scenes.md): additive loading, loading screens and the build list
- [Scenes and worlds](../02-scripting/05-scenes-and-worlds.md): what a world and a section are
