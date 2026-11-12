---
title: Loading scenes
description: Scene fields, loading a level, additive loading and streaming, opening a scene as its own world, loading screens and the build list.
---

Loading lives on the scene asset: `level.Load()`, `level.LoadAdditive()` and `level.Open()`. Each one returns a `SceneLoad` handle you can await. Read [Scenes and worlds](05-scenes-and-worlds.md) first for what a world and a section are.

## Scene fields

Hold a scene in a component as an `AssetRef<Scene>`:

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class LevelExit : Component
{
    public AssetRef<Scene> NextLevel;   // drag a .scene onto it in the inspector
}
```

`AssetRef<Scene>` names the scene without loading it, so holding level two never loads level two, its own next level, and everything those use. A plain `Scene` field would, and analyzer `PROWLSC002` warns about it on a component.

## Loading a level

`Load` replaces a world's content with the scene: every section except `Persistent` unloads, and the new scene becomes the active section.

```csharp
public sealed class LevelExit : Component   // on an object with a TriggerVolume
{
    public AssetRef<Scene> NextLevel;

    public override void OnTriggerEnter(Rigidbody3D other)
    {
        if (other.GameObject.CompareTag("Player"))
            NextLevel.Load();
    }
}
```

`Load()` on an `AssetRef<Scene>` or on a `Scene` loads into Main. Both take an optional world, `into`, so a second world can swap its level without touching Main: `NextLevel.Load(Scene)` loads into the world this component runs in.

> [!NOTE]
> To get the `Scene` asset itself without loading the level, use `NextLevel.LoadImmediate()`, or `Get()` to read it without loading.

What happens, in order, at the end of the frame:

1. Everything the scene uses has already loaded in the background, so nothing in it sees a half loaded asset.
2. Every section except `Persistent` tears down: every `OnDisable`, then every `OnRemovedFromScene`, then every object is disposed. Objects spawned into those sections while they tear down go with them.
3. Each unloaded section's `UnloadToken` is cancelled.
4. The scene becomes the `ActiveSection`, so the world switches to its sky, ambient light and fog.
5. Its objects join the world and get `OnAddedToScene`, then `OnEnable` when the world is running.
6. `SceneInstance.Loaded` fires.

There is no gap where the world is empty or missing, and persistent objects keep running throughout.

> [!IMPORTANT]
> Code awaiting a `Load` on a level object resumes after that object is gone. Run level flow from a [persistent object](05-scenes-and-worlds.md#objects-that-survive-a-load), or pass the object's own token so the await gives up when it is destroyed: `await NextLevel.Load().WaitAsync(DestroyCancellationToken);`

## Additive loading

`LoadAdditive` adds a scene as a new section after the others, and leaves the active section alone. Use it to stream parts of a level in and out:

```csharp
public sealed class StreamingZone : Component   // on an object with a TriggerVolume
{
    public AssetRef<Scene> Area;
    private SceneLoad? _load;

    public override void OnTriggerEnter(Rigidbody3D other)
    {
        if (!other.GameObject.CompareTag("Player") || _load != null) return;
        _load = Area.LoadAdditive(Scene);
    }

    public override void OnTriggerExit(Rigidbody3D other)
    {
        if (!other.GameObject.CompareTag("Player") || _load == null) return;
        if (_load.Section is { IsLoaded: true } section) section.Unload();
        else _load.Cancel();
        _load = null;
    }
}
```

- `section.Unload()` removes exactly the objects that section brought, plus anything spawned into it, at the end of the frame.
- Spawns go into the active section, not into the additive one. Set `Scene.ActiveSection` to change that, which also switches the world's environment.
- Unloading the active section makes the next section active, or the previous one when it was last.
- The last section besides `Persistent` cannot be unloaded. `Load` is how a world swaps its only level.
- Light probes from several loaded sections are merged into one set in the background. Until the merge finishes after an additive load, the previous set stays in use.

## Opening a scene as its own world

`Open` makes a new world from a scene, dormant, with the scene as its active section. You activate it, and decide whether it is drawn:

```csharp
SceneSection section = await MenuScene.Open();   // MenuScene is an AssetRef<Scene> field
SceneInstance menu = section.Instance;
menu.Present = true;
menu.RenderOrder = 100;
menu.Activate();
```

Keep a reference to `menu` while you use it, and `menu.Destroy()` it when you are done. Worlds are held weakly.

## A loading screen

A loading screen is a scene opened as its own world over Main, while the level loads into Main underneath. Run it from a persistent object:

```csharp
using System.Threading.Tasks;
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class LevelFlow : Component   // on a persistent object
{
    public AssetRef<Scene> LoadingScreen;

    public async Task Go(Scene level)
    {
        SceneSection screen = await LoadingScreen.Open();
        SceneInstance overlay = screen.Instance;
        overlay.RenderOrder = 100;
        overlay.Present = true;
        overlay.Activate();

        try
        {
            SceneLoad load = level.Load(options: new LoadOptions { HoldActivation = true, UnloadUnusedAssets = true });
            LoadingBar? bar = overlay.Get<LoadingBar>();   // a component of yours in the loading scene

            while (load.Phase < SceneLoadPhase.WaitingForActivation)
            {
                if (bar.IsValid()) bar!.Value = load.Progress;
                await GameTask.NextFrame();
            }

            load.AllowActivation = true;
            await load;
        }
        finally
        {
            overlay.Destroy();
        }
    }
}
```

A failed load leaves the loop on `Failed`, `await load` throws, and the `finally` still destroys the overlay.

## Waiting and failure

Every handle completes exactly once:

| Outcome | `Phase` | Awaiting it |
| --- | --- | --- |
| Done | `Done` | Gives the loaded `SceneSection` |
| Failed | `Failed` | Throws `SceneLoadException`, with the cause in `Error` |
| Cancelled | `Cancelled` | Throws `OperationCanceledException` |

- A missing or unreadable scene fails the load. It never loads as an empty world.
- `Cancel()` works until the load starts activating.
- A second `Load` into the same world cancels the first, and the additive loads queued before it. Additive loads queued after it still apply.
- A load into a world that is destroyed first is cancelled.
- A load started from a callback while another load activates waits for the next safe point.
- `world.PendingLoad` is the `Load` queued for that world, or null.

In game code, `await` the handle so the game keeps running while the scene loads. `Wait()` blocks until the load is ready. Inside a frame it still activates at the end of the frame, and outside one it activates at once, so the scene shows on the very first frame. A built game loads its first scene that way at startup.

## The build list

`SceneBuild` holds the scenes the build ships, in build order. A built game loads the first one at startup. In the editor's play mode it holds the enabled scenes from Build Settings.

```csharp
Scene? level = SceneBuild.Find("Level2");      // by name, or by the end of its path
if (level.IsValid())
    await level!.Load();
```

| Member | Meaning |
| --- | --- |
| `SceneBuild.List` | The scenes in the build, in order |
| `SceneBuild.Find(nameOrPath)` | The scene with this name, or whose path ends with it, like `Levels/Forest`. Null when it is not in the build |
| `SceneBuild.IndexOf(scene)` | Its place in the list, -1 when it is not in it |

A scene reached only through an `AssetRef<Scene>` field still ships, but it is not in the build list.

## Reference

### Loading

| Call | Does |
| --- | --- |
| `scene.Load(into, options)` | Replaces the content of `into`, Main when null. The scene becomes the active section |
| `scene.LoadAdditive(into, options)` | Adds the scene as a section of `into`, Main when null |
| `scene.Open(mode, options)` | Makes a new dormant world from the scene. `mode` defaults to `SceneMode.Game` |
| `section.Unload()` | Unloads a section at the end of the frame |
| `scene.ReadContent()` | A detached copy of the stored scene, in no world and with no callbacks. For tools |

The same three loading calls work on an `AssetRef<Scene>`, with the `Load` caveat above.

### SceneLoad

| Member | Meaning |
| --- | --- |
| `Scene` | The scene being loaded |
| `Phase` | `Preloading`, `Instantiating`, `WaitingForActivation`, `Activating`, `Done`, `Failed` or `Cancelled` |
| `Progress` | 0 to 1. Loading the scene's assets is most of it |
| `Error` | Why it failed |
| `Section` | The loaded section once done. `Section.Instance` is the world, a new one for `Open` |
| `AllowActivation` | False holds a ready load back |
| `Cancel()` | Cancels it unless it is already activating |
| `Wait()` | Blocks until it is ready to activate |
| `WaitAsync(token)` | Awaits it, giving up when `token` is cancelled |

### LoadOptions

| Field | Meaning |
| --- | --- |
| `HoldActivation` | Start with `AllowActivation` false, for a "press any key" screen |
| `UnloadUnusedAssets` | After activation, free every asset nothing uses at once, without the grace period |
