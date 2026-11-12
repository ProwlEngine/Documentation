---
title: Sky, fog and clouds
description: The scene environment: sky, ambient light, fog, volumetric fog and volumetric clouds.
---

Each scene has a `SceneEnvironment`, edited in the Environment panel or from a component's code through `Scene.Environment`. It holds the sky, the ambient light, fog, volumetric fog and volumetric clouds.

## Sky

```csharp
Scene.Environment.SkyMaterial = SceneEnvironment.CreateSkyMaterial(BuiltInSky.Procedural);
```

`SkyMaterial` is any material whose shader has a sky pass, usually one of `BuiltInSky`: `Procedural`, `Gradient`, `Cubemap`, `Panorama` or `SixSided`. Null shows the flat `SkyColor`. Skies give their light in nits, like everything else, so the Gradient, Cubemap, Panorama and SixSided skies have an `intensity` in nits, 20000 by default, and the Procedural sky follows the scene's brightest directional light. See [Custom skies](../04-shaders/11-custom-skies.md) to write your own.

The sky is also captured into the **sky probe**, which lights the scene's reflections, sky ambient and sky coloured fog. `SkyCapture` sets when:

| Setting | Default | Meaning |
| --- | --- | --- |
| `Mode` | `OnChange` | `OnChange`, `EveryFrame` or `Never` |
| `Resolution` | 128 | The sky probe's cube size, a power of two from 16 to 2048 |
| `Interval` | 2 | Frames at least between two captures on change |

## Ambient light

| `Ambient.Mode` | Lights surfaces with |
| --- | --- |
| `Sky` | The default. The sky's own light, from the sky probe. `Intensity` multiplies it |
| `Hemisphere` | `GroundColor` blended up to `SkyColor`, scaled to `Intensity` nits |
| `Uniform` | `Color`, scaled to `Intensity` nits |

Lightmaps and light probes replace the ambient light where they are baked.

## Fog

`Fog.Mode` is `Off`, `Linear` (from `Start` to `End`), `Exponential` or `ExponentialSquared` (the default, by `Density`). With `UseSky` on, the default, fog takes the colour of the sky behind it, so it meets the horizon seamlessly. Otherwise it is `Color` scaled to `Intensity` nits, 10000 by default.

## Volumetric fog

Fog in the air lit by the scene's lights through their shadows: light shafts through windows, glows around street lamps. Turn it on with `VolumetricFog.Enabled`.

| Setting | Default | Meaning |
| --- | --- | --- |
| `Density` | 0.02 | Light taken out per metre at `BaseHeight` |
| `BaseHeight`, `HeightFalloff` | 0, 0.1 | It thins with height above the base, per metre |
| `Albedo` | white | The share of that light it scatters rather than absorbs |
| `Anisotropy` | 0.6 | 0 scatters evenly, toward 1 forward, glowing around lights seen through it |
| `AmbientScale` | 1 | Scales the ambient light it scatters |
| `Distance`, `Slices` | 128, 128 | How far it reaches in metres, and the depth slices it is lit in |
| `TemporalBlend` | 0.9 | How much of last frame each frame keeps |

Every fogged material reads it, transparent ones included.

### Fog volumes

A **Fog Volume** component (**Rendering > Fog Volume**) adds volumetric fog inside a shape: `Global`, `Box`, `Sphere`, `Cylinder` or `Cone`, sized by its Transform's scale. `DensityMultiplier` is a multiple of the scene's `Density`, `ColorTint` its albedo, and `Falloff` softens its edges. Volumetric fog must be enabled for fog volumes to show.

## Volumetric clouds

Ray marched clouds over the whole scene, turned on with `VolumetricClouds.Enabled`. They shade the ground, the volumetric fog and the water under them, block the sun when dense, and appear in reflection probes.

| Group | Settings |
| --- | --- |
| Shape | `Altitude`, `Thickness`, `Coverage`, `Density`, `PatternScale`, `Erosion`, `DetailScale`, `Wisps`, `Lobes`, and the top layer's `TopStrength` and `TopCoverage` |
| Wind | `WindSpeed` in metres a second, `WindDirection` in degrees |
| Lighting | `Albedo`, `SunBrightness`, `AmbientBrightness`, `SilverLining`, `MultipleScattering`, `HorizonFade` |
| Quality | `Resolution` (`Full`, `Half`, `Quarter`), `Temporal`, `ShadowResolution` |
| High layer | `HighLayer`, a faint flat layer of cirrus above, with `HighLayerAltitude` and `HighLayerScale` |

```csharp
var clouds = Scene.Environment.VolumetricClouds;
clouds.Enabled = true;
clouds.Coverage = 0.5f;
clouds.WindSpeed = 25f;
```

Clouds drift with the scene's own clock.
