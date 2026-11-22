---
title: Do something after a delay
description: Wait a few seconds in a script, then act, without freezing the game.
---

You end with a component that waits two seconds after the game starts, then logs a message. The same pattern works for timed spawns, door timers and cooldowns.

## Steps

1. In the **Project** panel, choose **Assets > Create > C# Script**, name it `DelayedMessage`, and paste the code below.
2. Select a GameObject in the **Hierarchy**. Click **Add Component** and add **DelayedMessage**.
3. Press **Play**. After two seconds the **Console** shows `Two seconds passed.`

[screenshot needed: the Console showing the logged message]

4. To change the wait, edit the **Seconds** field in the **Inspector** before you press **Play**.

```csharp
using Prowl.Runtime;

public sealed class DelayedMessage : Component
{
    public float Seconds = 2f;

    public override async void Start()
    {
        await GameTask.Delay(Seconds, DestroyCancellationToken);
        Debug.Log("Two seconds passed.");
    }
}
```

## Variations

| To do this | Use |
| --- | --- |
| Wait for the next frame | `await GameTask.NextFrame();` |
| Wait until something is true | `await GameTask.WaitUntil(() => door.IsOpen);` |
| Wait in real time, ignoring pause and slow motion | `await GameTask.DelayRealtime(1f);` |

## If it does not work

- **It never logs.** The component must be enabled in a playing world. Check that **Play** is on.
- **The message appears after the object is destroyed.** Pass `DestroyCancellationToken`, as above, so the wait ends when the object is destroyed.
- **Pausing does not stop it.** Check that you used `Delay`, not `DelayRealtime`. Only `Delay` holds while paused.

## Learn more

- [Async with GameTask](../02-scripting/04-async-with-gametask.md): threads, cancellation and tokens
- [Components](../02-scripting/01-components.md): when `Start` and the other callbacks run
