---
title: Probes and baked lighting
description: Reflection probes, light probes and lightmaps, and how to bake them in the editor.
---

A **probe** is a point in the scene that stores light for objects nearby. A **reflection probe** stores what the surroundings look like, for shiny surfaces. A **light probe** stores the light that falls on a spot, for moving objects. A **lightmap** is a texture of baked light on static surfaces.

Baking computes this light once, in the editor, and saves it with the scene. Read [Lights](03-lights.md) first.

## Quick recipe: bake a room

1. Select the objects that never move, and tick **Static** in the Inspector.
2. Save the scene. A scene with no file cannot bake.
3. Select a light and set `BakeMode` to `Baked`.
4. Open **Window > General > Environment** and go to the **Lightmapping** tab.
5. Click **Generate Lighting**. Keep the panel open until the bar finishes.
6. Add an empty object, then **Add Component > Rendering > Reflection Probe**. Size `BoxSize` to the room.
7. Click **Bake** in the probe's Inspector, then save the scene.

[screenshot needed: the Lightmapping tab mid-bake]

## Reflection probes

A `ReflectionProbe` captures a cubemap of its surroundings. Surfaces inside its box reflect that capture, projected onto the box, so a probe fitted to a room puts the walls in the right place. Surfaces no probe covers reflect the [sky](04-environment.md#sky).

| Setting | Default | Meaning |
| --- | --- | --- |
| `Mode` | `Baked` | `Baked` is captured by `Bake()` and saved with the scene. `Realtime` captures while the game runs |
| `RefreshMode` | `OnEnable` | Realtime only. `OnEnable`, `EveryFrame`, or `ViaScripting` for `RenderProbe()` |
| `TimeSlicing` | `AllFacesAtOnce` | Realtime only. `IndividualFaces` takes one face a frame |
| `BoxSize`, `BoxOffset` | 10 by 10 by 10, zero | The area it affects. The capture is taken from the box middle |
| `BlendDistance` | 1 | How far in from the box faces it fades, so neighbours blend |
| `Importance` | 1 | Higher wins where probes overlap, then the smaller box |
| `Resolution` | 128 | Cube edge length, a power of two, capped by `MaxProbeResolution` in [Quality levels](06-quality.md) |

A baked probe shows nothing until you click **Bake** in its Inspector. **Clear Baked** removes the capture.

Call `RenderProbe()` to refresh a realtime probe set to `ViaScripting`.

## Light probes

Lightmaps only cover static objects. A `LightProbeGroup` places points in the scene where the bake samples the light, so moving objects match their surroundings. An object blends the four probes around it, or the nearest ones outside them.

Add one with **Add Component > Rendering > Light Probe Group**:

| Control | Meaning |
| --- | --- |
| `Min (local)`, `Max (local)` | The box the grid fills, in the object's local space. Defaults -5, 0, -5 to 5, 5, 5 |
| `Count X`, `Count Y`, `Count Z` | Probes per axis, 4, 3 and 4 by default |
| **Generate Grid** | Replaces the probes with a grid |
| **Add Probe**, **Clear Probes** | Adds one, or removes all |

The **Light Probes** scene tool moves, adds, deletes and duplicates probes by hand. Probes bake with **Generate Lighting**. In code, `GenerateGrid` matches the button.

## Lightmaps

**Generate Lighting** bakes every loaded scene together with the Photonic path tracer, so light and shadow cross between scenes. Each scene writes its pages into a `SceneName_lightmaps` folder beside its file. The bake never saves a scene.

Static renderers with a lightmap UV get a lightmap. The bake uses UV2 when the mesh has it, otherwise UV0. Static renderers without one only cast shadows and bounce colour.

The bake will not start in play mode, with an unsaved scene, or with no static renderers. **Cancel** stops a running bake, and **Clear** deletes the baked lightmaps and probes.

### Settings

Per scene, on the **Lightmapping** tab.

| Setting | Default | Meaning |
| --- | --- | --- |
| `Atlas Size` | 1024 | Edge of each lightmap page in texels |
| `Texels / Unit` | 20 | Lightmap texels per world unit. Higher is sharper |
| `Bounces` | 2 | Times light bounces |
| `Indirect Samples` | 64 | Passes before the bake finishes |
| `Sparse Stride` | 1 | Traces one texel per N by N cell. Faster, less detail |

## Light bake modes and static

A light's `BakeMode` is `Realtime`, `Mixed` or `Baked`, described in [Baked lighting](03-lights.md#baked-lighting). Area lights bake as point lights.

Only static objects take part in a bake. Tick **Static** in the Inspector, or set `GameObject.IsStatic`.

## See also

- [Lights](03-lights.md)
- [Sky, fog and clouds](04-environment.md)
