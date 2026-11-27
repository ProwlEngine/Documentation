---
title: Detect when the player enters an area
description: Use a trigger volume and a small script to react when a physics object or a character enters a zone.
---

You end with a message in the console each time something enters an invisible zone. It needs one empty object with a trigger volume and one script.

## Steps

1. Choose **GameObject > Empty Object**. Name it `Checkpoint`, and move it where the zone should be.
2. In the **Project** panel, choose **Assets > Create > C# Script**, name it `Checkpoint`, and paste the code below.
3. Select the object. Click **Add Component** and choose **Trigger Volume**.
4. Set **Shape** and **Size** (or **Radius**) so the volume covers the zone. Its bounds show in the scene view.
5. Click **Add Component** and choose **Checkpoint**.
6. Make sure the thing that enters has a **Rigidbody** and a collider, or is a **Character Controller**.
7. Press **F5** and move into the zone. The console prints a line on entry.

[screenshot needed: the Trigger Volume bounds around a zone in the scene view, and the Inspector]

```csharp
using Prowl.Runtime;

[RequireComponent(typeof(TriggerVolume))]
public sealed class Checkpoint : Component
{
    public override void OnTriggerEnter(Rigidbody3D other)
    {
        Debug.Log($"{other.GameObject.Name} reached the checkpoint");
    }

    public override void OnCharacterEnter(CharacterController character)
    {
        Debug.Log($"{character.GameObject.Name} reached the checkpoint");
    }
}
```

## If nothing prints

- **The zone is the wrong size.** Check the **Size**, **Center** and **Layer Mask** fields on the **Trigger Volume**.

## Learn more

- [Rigidbodies and collisions](../06-physics/01-rigidbodies-and-collisions.md#triggers): enter, stay and exit events
- [Character controller](../06-physics/02-character-controller.md): moving a player
