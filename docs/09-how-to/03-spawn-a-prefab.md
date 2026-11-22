---
title: Spawn a prefab
description: Save an object as a prefab and spawn copies of it from a script when you press a key.
---

You end with a key press that spawns a copy of an object at a spawner's position. It needs one object to copy and one small script.

## Steps

1. In the **Hierarchy**, build the object you want to spawn, such as a cube with a **Rigidbody**.
2. Right-click the object and choose **Create Prefab**. A `.prefab` file appears in the current folder of the **Project** panel.

[screenshot needed: the Hierarchy context menu with Create Prefab, and the new prefab in the Project panel]

3. Delete the original object from the scene, so only the spawned copies appear.
4. In the **Project** panel, choose **Assets > Create > C# Script**, name it `Spawner`, and paste the code below.
5. In the **Hierarchy**, create an empty object and place it where copies should appear. Add the **Spawner** component to it.
6. Drag the prefab from the **Project** panel into the **Prefab** field of the **Spawner**.

[screenshot needed: the Spawner in the Inspector with the Prefab field filled]

7. Press **Play** and press F. A copy of the prefab appears at the spawner each time.

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

## If it does not spawn

- **Nothing appears.** Check that **Prefab** is filled and the console shows no `[Instantiate]` error.
- **The copy is at the wrong place.** Copies use the position and rotation of the object that holds the **Spawner**.

## Learn more

- [Prefabs](../02-scripting/08-prefabs.md): overrides, editing a prefab, and every `Instantiate` overload
- [Assets and importers](../07-editor/04-assets-and-importers.md)
