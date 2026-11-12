---
title: Input and time
description: Keyboard, mouse, input actions and the Time class.
---

## Time

`Time.DeltaTime`, `Time.UnscaledDeltaTime`, `Time.FixedDeltaTime`, `Time.TimeScale`, `Time.FrameCount` and `Time.TimeSinceStartup`.

Every world has its own clock. The scaled values, `DeltaTime`, `SmoothDeltaTime`, `TimeSinceStartup`, `TimeScale`, `EffectiveTimeScale` and `FixedAlpha`, read the clock of the world your code runs in, so a paused world's time stands still while a menu world over it keeps moving. `UnscaledDeltaTime`, `UnscaledTotalTime`, `FixedDeltaTime` and `FrameCount` are shared by every world.

For slow motion or a hit stop, add a modifier rather than setting `TimeScale`, so overlapping effects each remove only their own:

```csharp
TimeScaleModifier slowMo = Time.AddTimeScaleModifier(0.25f);
await GameTask.DelayRealtime(2f);
slowMo.Remove();
```

`Scene.Clock` is the same clock as a `SceneClock`, for code that needs another world's time. `SceneClock.Defaults` holds the project's time settings, which every new world starts with.

## Direct input

```csharp
if (Input.GetKeyDown(KeyCode.Space)) Jump();
if (Input.GetMouseButton(0)) Fire();

Float2 move = Input.GetWASD();
Float2 look = Input.MouseDelta;
```

> [!NOTE]
> `Input.MouseDelta.Y` is positive when the mouse moves **down**, as in window coordinates. For mouse look, subtract it from the pitch.

## Input actions


![The Input Actions editor with a Move composite and a Jump action](images/input-actions-editor.png)

For rebindable controls, create an Input Actions asset from the create menu and edit it in its dedicated editor. Actions support composites such as WASD to a `Float2`, D-pads, gamepads and XR controllers.

```csharp
Input.RegisterActionMap(map);
map.Enable();   // actions start disabled

var move = Input.FindAction("Move");
Float2 value = move.ReadValue<Float2>();
if (Input.FindAction("Jump").WasPressedThisFrame()) Jump();
```

## Logging

`Debug.Log`, `LogWarning`, `LogError` and `LogOnce(id, message)` for messages that would otherwise repeat every frame. `Debug.DrawLine`, `DrawWireCube` and `DrawWireSphere` draw gizmos.
