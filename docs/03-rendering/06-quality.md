---
title: Quality levels
description: Low to Ultra quality levels, the PBR tier, shadow distance and render scale.
---

The project's quality levels are set in **Project Settings > Quality**. Every camera, light and scene follows the active one, and a game can switch levels at any time.

| Setting | Low | Medium | High | Ultra |
| --- | --- | --- | --- | --- |
| `PbrTier` | Lite | Lite | Full | Full |
| `RenderScale` | 0.8 | 1 | 1 | 1 |
| `ShadowDistance` | 30 | 50 | 80 | 150 |
| `ShadowCascades` | One | Two | Four | Four |
| `MaxShadowResolution` | 512 | 1024 | 2048 | 4096 |
| `MaxProbeResolution` | 64 | 128 | 256 | 512 |
| `LightCutoff` | 0.01 | 0.01 | 0.01 | 0.01 |

High is active by default.

- **PbrTier** is how the standard surfaces shade. `Lite`, for mobile, drops thin film and anisotropy, lights coat and fuzz from ambient light only, blends at most one reflection probe with the sky, and refracts transmissive materials from the probes instead of the scene.
- **RenderScale** multiplies every camera's own render scale.
- **ShadowDistance** is how far directional shadows reach, in world units, fading out over the last tenth.
- **MaxShadowResolution** and **MaxProbeResolution** cap each light's shadow tile and each reflection probe's cube.
- **LightCutoff** is the illuminance in lux where a light's automatic range ends. Higher cuts lights shorter and cheaper.

## From code

```csharp
QualitySettings.SetActive("Low");
QualitySettings.Active.ShadowDistance = 60f;
QualitySettings.Apply();   // after changing a level in place
```

`QualitySettings.Levels` lists every level, and `QualitySettings.Changed` fires after the levels or the active one change.
