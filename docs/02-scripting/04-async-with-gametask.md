---
title: Async with GameTask
description: Wait, hop threads and cancel cleanly with the GameTask API.
---

`GameTask` gives components async code that respects frames, game time and play sessions.

## Waiting

```csharp
await GameTask.NextFrame();
await GameTask.Frames(30);
await GameTask.Delay(1f);           // game time, stops while paused
await GameTask.DelayRealtime(1f);
await GameTask.WaitUntil(() => door.IsOpen);
```

Await inside a component resumes on the main thread.

## Moving work off the main thread


![A texture painted on a worker thread while the game keeps running](images/gametask-painter.gif)

```csharp
private async void Paint()
{
    await GameTask.WorkerThread();
    var pixels = GeneratePixels();          // heavy work, the game keeps running

    await GameTask.MainThread();            // scene objects are main-thread only
    var texture = new Texture2D(512, 512, srgb: true);
    texture.SetData(new Memory<Color32>(pixels));
}
```

> [!WARNING]
> Scene objects may only be touched on the main thread. Writes from a worker throw, but reads do not, so a wrong read fails silently.

## Cancellation

When play stops or scripts reload, pending continuations are dropped without running their `finally` blocks. Pass `DestroyCancellationToken` or `GameTask.SessionToken` and catch `OperationCanceledException` when you need to clean up.

```csharp
try
{
    while (true)
    {
        await GameTask.Delay(1f, DestroyCancellationToken);
        Debug.Log("tick");
    }
}
catch (OperationCanceledException) { }
```

Never block with `.Result`, `.Wait()` or `GetAwaiter().GetResult()` in a component. It deadlocks, and an analyzer flags it.
