---
title: Ocean
description: An FFT ocean to the horizon, with foam, wakes, currents, floating bodies and lakes.
---

Add an **Ocean** component (**Add Component > Rendering > Ocean**) and the scene has a sea at the GameObject's height, out to the horizon. Waves come from a wind driven spectrum on repeating tiles, drawn as rings around the camera that curve down with the planet.

## Waves

| Setting | Meaning |
| --- | --- |
| `WindSpeed`, `WindDirection` | Wind in km/h, which cuts off waves too long for it, blowing toward degrees clockwise from +Z |
| `Turbulence` | How far waves spread from the wind's direction. At 1 they travel every way |
| `WaveScale`, `Chop`, `TimeScale` | Scale every wave's height, pinch crests sideways into sharp peaks, speed waves up or down |
| `TileSize` | The largest wave tile in metres, 1024 by default |
| `LoopPeriod` | Seconds before the waves repeat, 0 for never |
| `PlanetRadius` | Curves the water toward the horizon, 0 for flat |

## Water

The water absorbs light along its depth: `Absorption` per colour channel per metre, so shallow water shows the floor and deep water turns to `ScatterColor`. `SubsurfaceColor` is the glow through crests toward a low sun behind them. `ScreenReflections` reflects what is on screen.

The floor is captured once from straight above, over `FloorCaptureSize` metres around the GameObject from `FloorLayers`. Waves shrink in shallow water, foam gathers along the shore up to `ShorelineFoamDepth`, and caustics light the floor.

Foam builds where waves fold over, set by `FoamCoverage`, `FoamStrength` and `FoamFade`. `FoamTexture`, `NormalsTexture` and `CausticsTexture` replace the built-in textures.

Under the water the ocean draws its own fog from the same absorption, scaled by `UnderwaterDensity`.

## Working with the water

| Component | Does |
| --- | --- |
| **Ocean Floater** (**Physics > Ocean Floater**) | Floats a `Rigidbody3D`. Each of its `Probes` pushes up by how deep it sits, scaled by `Buoyancy` |
| **Ocean Wake** | Pushes ripples and a wake into the water as it moves, as a sphere of `Radius`. Several make a hull's wake |
| **Ocean Flow** | A current over a rectangle, along the GameObject's forward, which carries waves, foam and ripples |
| **Ocean Clip** | Cuts the surface away inside a box or other shape, so a hull or a dry dock stays dry |
| **Ocean Water Level** | Holds the water at the GameObject's height over a rectangle, for a lake or pond above or below the sea |

Floaters read the water back from the GPU, a few frames late, which is fine for boats and debris.
