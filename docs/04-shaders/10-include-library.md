---
title: Include library reference
description: The Graphite and Prowl include files and the functions they provide.
---

## Relative and world

All position uniforms are camera-relative, which means they are offset from the camera. This keeps large worlds free of floating-point precision issues. It fixes jitter and bad z-fighting when the camera is far from the origin (0, 0, 0).

Prowl labels positions `relative` or `world`. `world` is the object's actual position. `relative` is the camera-relative offset. Directions and normals are always world space.

## Light is exposed

Light is in real units: lux, candela and nits. Every lighting function already multiplies its result by `Graphite_Exposure()`. Colours from a lit pass are ready for tonemapping.

## How includes resolve

| Include | Comes from |
| --- | --- |
| `#include "Graphite/..."` | Graphite's built-in library |
| `#include "Prowl/..."` | Prowl's built-in includes. Only `Prowl/Common.glsl` is documented here |
| anything else | Next to the shader, then the project's Assets root. A name with no extension also tries `.glsl` |

Project includes are inlined on import, each file once. `#pragma once` works.

## Core files

| Include | What it gives | Key calls |
| --- | --- | --- |
| `Graphite/Vertex.glsl` | Vertex stage only. Vertex streams and the object's transforms | `vertexPosition`, `vertexNormal`, `vertexUV0`, `vertexBoneIndices`, `Graphite_HasStream(n)`, `Graphite_ObjectToRelative(p)`, `Graphite_ObjectToClip(p)`, `Graphite_ObjectToWorldNormal(n)`, `Graphite_SetPreviousPosition(p)`, `Graphite_LightmapUV()` |
| `Graphite/Core.glsl` | Included by the others. View, exposure and depth helpers | `Graphite_View()`, `Graphite_Exposure()`, `Graphite_RelativeToWorld(p)`, `Graphite_ViewDir(relativePos)`, `Graphite_LinearDepth(depth)`, `Graphite_IsCapture()` |
| `Graphite/ViewData.glsl` | Included by Core. The view data below | `Graphite_RelativeFromDepth(view, uv, depth)` |
| `Graphite/Math.glsl` | Included by Core. Constants and small helpers | `GRAPHITE_PI`, `Graphite_Luminance(c)`, `Graphite_SaturateHalf(c)`, `Graphite_Hash(x)`, `Graphite_ToYCoCg`, `Graphite_FromYCoCg` |
| `Graphite/Passes.glsl` | Fragment stage. Outputs for the G-buffer and motion | `Graphite_WriteGBuffer(normal, reflectance, roughness)`, `Graphite_WriteMotion(currentClip, previousClip)`, `Graphite_WriteReactive(amount)` |

`Graphite_Exposure()` is `1 / (1.2 * 2^EV100)`. `Graphite_WriteGBuffer` is for opaque Forward passes, and `reflectance` is a `vec3`. `Graphite_WriteReactive` marks pixels that show refraction, so temporal effects trust their history less.

## View data

`Graphite_View()` returns a `Graphite_ViewData`:

| Field | Meaning |
| --- | --- |
| `view` | Rotation only. Translation is in the relative positions |
| `projection`, `viewProjection`, `inverseViewProjection` | Matrices |
| `previousViewProjection` | Last frame's, for motion vectors |
| `screen` | Width, height, 1 / width, 1 / height |
| `jitter` | This frame's TAA jitter in `xy`, last frame's in `zw` |
| `time` | Time, delta time, frame index |
| `depth` | Near plane, far distance |
| `exposure` | This frame's exposure in `x`, last frame's in `y` |

## Lighting

`Graphite/Lighting.glsl` is fragment stage. It includes Lights, Ambient, Probes and Fog. Include only the part you need.

| Include | What it gives | Key calls |
| --- | --- | --- |
| `Graphite/Lights.glsl` | Sun and local lights | `Graphite_GetDirectional(i)` (the sun is 0), `Graphite_DirectionalLightShadow(light, i, pos, geomN)`, `Graphite_BeginLights(pos)`, `Graphite_NextLight(it, L)`, `Graphite_LightRadiance(L)`, `Graphite_LocalLightShadow(L, pos, geomN)` |
| `Graphite/Ambient.glsl` | Indirect light | `Graphite_IndirectDiffuse(N, lightmapUV)`, `Graphite_AmbientLight(N)`, `Graphite_SkyAmbient(N)` |
| `Graphite/Probes.glsl` | Reflection probes | `Graphite_FindProbes(pos)`, `Graphite_ProbeRadiance(set, N, V, alpha)`, `Graphite_SampleSkyProbe(dir, roughness)` |
| `Graphite/Fog.glsl` | Fog and volumetric fog | `Graphite_ApplyFog(color, pos)`, `Graphite_FogColor(pos)` |
| `Graphite/Shadows.glsl` | The shadow atlas | Define `GRAPHITE_HARD_SHADOWS` before including to make every shadow hard |

## Graphite/PBR

The OpenPBR model the Lit shader uses. `Closure.glsl` includes Lighting.glsl and the other PBR files.

| Include | What it gives | Key calls |
| --- | --- | --- |
| `Graphite/PBR/Closure.glsl` | The full lit surface | `PBR_Prepare(p, pos, V, geomN, mapVariance)`, `PBR_ShadeLights(c)`, `PBR_FindProbes(c)`, `PBR_GatherIndirect(c, lightmapUV, probes)`, `PBR_TopReflectance(c, out normal, out roughness)` |
| `Graphite/PBR/Params.glsl` | The material inputs | `PBR_Params`, `PBR_DefaultParams(normal, tangent)` |
| `Graphite/PBR/Microfacet.glsl`, `Fresnel.glsl`, `Diffuse.glsl` | Specular, Fresnel and diffuse terms | `PBR_DistributionGGX`, `PBR_VisibilitySmithGGX`, `PBR_FresnelDielectric`, `PBR_Eon` |
| `Graphite/PBR/Fuzz.glsl`, `ThinFilm.glsl`, `Transmission.glsl` | The optional layers | |

Define `GRAPHITE_CUSTOM_BRDF` or `GRAPHITE_CUSTOM_AMBIENT_BRDF` before including `Closure.glsl` to supply `Graphite_BRDF` or `Graphite_AmbientBRDF`. Surface Lighting blocks do this for you, see [Custom lighting](06-custom-lighting.md).

## Surface and screen

| Include | What it gives | Key calls |
| --- | --- | --- |
| `Graphite/Standard/Standard.glsl` | Normal map and UV helpers. Used by surface shaders, handy in your own passes | `Graphite_SurfaceNormalMap(i, texel, scale)`, `Graphite_StandardNormalMap(texel, normal, tangent, bitangent, scale)`, `Graphite_StandardTangentFrame(...)`, `Graphite_StandardUV(set, scaleOffset, rotation, i)` |
| `Graphite/Decals.glsl` | Decals. The renderer switches them with the global `GRAPHITE_DECALS` variant, so including the file is enough | `Graphite_ApplyDecals(relativePos, geomNormal, inout albedo, inout normal, inout roughness, inout metallic, inout occlusion)`. Call it before lighting |
| `Graphite/SceneColor.glsl` | Scene colour. See [Transparency and screen effects](07-transparency-and-screen-effects.md) | `Graphite_ScreenUV()`, `Graphite_RelativeToScreenUV(pos)`, `Graphite_SampleSceneColor(uv, lod)` |
| `Graphite/SceneDepth.glsl` | Scene depth | `Graphite_FetchSceneDepth(uv)`, `Graphite_SceneLinearDepth(uv)`, `Graphite_SceneRelativePosition(uv)` |
| `Graphite/Sky.glsl`, `Skies.glsl` | For sky passes. See [Custom skies](11-custom-skies.md) | `Graphite_SkyDirection()`, `Graphite_SunDirection()`, `Graphite_SunIlluminance()`, `Graphite_ProceduralSky(...)`, `Graphite_RotateSkyY(dir, degrees)`, `Graphite_PanoramaUV(dir)` |
| `Graphite/Debug.glsl` | Lets a custom lit shader join the editor's debug views | `Graphite_DebugView(...)`, `Graphite_DebugInputs(...)` |

For `Debug.glsl`, add `#pragma variant global GRAPHITE_DEBUG UNLIT ALBEDO NORMALS ROUGHNESS METALLIC AO EMISSION LIGHTING CASCADES LIGHTMAP_DENSITY`, as the Sprite shader does. `UNLIT` must come first. It is normal drawing.

## Prowl/Common.glsl

| Function | Use |
| --- | --- |
| `gammaToLinearSpace(c)` | sRGB to linear |
| `linearToGammaSpace(c)` | Linear to sRGB |
| `Prowl_Luminance(c)` | Luminance of a linear colour |
| `Prowl_TangentFrame(...)`, `Prowl_ApplyNormalMap(...)` | Tangent frame and normal map helpers |
