---
title: Include library reference
description: The Graphite and Prowl include files and the functions they provide.
---

## Relative and world

Positions in Graphite shaders are **relative**: world space moved so the camera sits at the origin, which keeps precision far from it. **World** means true world space. Functions and parameters say which they take: `relativePos`, `Graphite_ObjectToRelative`, `Graphite_RelativeToWorld`. Directions and normals are world space.

## Light is exposed

Light in the library is in real units, lux, candela and nits, and everything a lighting function returns is already multiplied by `Graphite_Exposure()`, the camera's exposure. Colours you write from a lit pass are therefore ready for tonemapping.

## How includes resolve

| Include | Comes from |
| --- | --- |
| `#include "Graphite/..."` | Graphite's built-in library |
| `#include "Prowl/..."` | Prowl's built-in shader includes |
| anything else | Next to the shader first, then from the project's Assets root. A name without an extension also tries `.glsl` |

Project includes are inlined when the shader imports, each file once. `#pragma once` is supported.

## Graphite/Vertex.glsl

Vertex stage only. Pulls vertex data and gives the object's transforms.

| Function | Returns |
| --- | --- |
| `vertexPosition`, `vertexNormal`, `vertexTangent`, `vertexColor` | Vertex streams |
| `vertexUV0` ... `vertexUV3`, `vertexCustom0`, `vertexCustom1` | More streams |
| `vertexBoneIndices`, `vertexBoneWeights` | Skinning data |
| `Graphite_HasStream(n)` | Whether the mesh has stream `n` |
| `Graphite_ObjectToRelative(p)` | Relative position of an object space point |
| `Graphite_ObjectToWorldNormal(n)`, `Graphite_ObjectToWorldDirection(d)` | World space normal or direction |
| `Graphite_ObjectToClip(p)` | Clip position |
| `Graphite_PreviousObjectToClip(p)` | Last frame's clip position |
| `Graphite_SetPreviousPosition(p)` | Tell motion vectors where a moved vertex was last frame |
| `Graphite_PreviousVertexPosition()` | The object space position motion vectors will use for last frame |
| `Graphite_LightmapUV()` | Where this vertex samples the object's lightmap |
| `Graphite_InstanceIndex()` | The instance being drawn |
| `Graphite_Object()`, `Graphite_ObjectIndex()` | The object's record and index |

## Graphite/Core.glsl

Included by the others.

| Function | Returns |
| --- | --- |
| `Graphite_View()` | The view data below |
| `Graphite_Exposure()` | What light is multiplied by before it is written: `1 / (1.2 * 2^EV100)` |
| `Graphite_IsCapture()` | Whether this view is a probe or sky capture |
| `Graphite_RelativeToClip(p)` | Clip position of a camera relative point |
| `Graphite_RelativeToWorld(p)` | The world position of a relative one, for noise and patterns |
| `Graphite_ViewDir(relativePos)` | Unit direction from a point to the camera |
| `Graphite_LinearDepth(depth)` | Distance along the view from a raw depth |
| `Graphite_RelativeFromDepth(view, uv, depth)` | Camera relative position from screen UV and depth, in a view such as `Graphite_View()` |
| `Graphite_ViewRay(clipXY)` | The direction a clip position looks along |

## Graphite/Math.glsl

Included by Core. `GRAPHITE_PI`, `GRAPHITE_TWO_PI`, `GRAPHITE_HALF_PI`, `GRAPHITE_INV_PI` and `GRAPHITE_INV_TWO_PI`, plus `Graphite_Luminance(c)`, `Graphite_SaturateHalf(c)` (clamps to the largest half float), `Graphite_Hash(x)`, `Graphite_ToYCoCg` and `Graphite_FromYCoCg`.

## View data

`Graphite_View()` returns a `Graphite_ViewData`:

| Field | Meaning |
| --- | --- |
| `view` | Rotation only; translation is handled by camera relative positions |
| `projection`, `viewProjection`, `inverseViewProjection` | Matrices |
| `previousViewProjection` | Last frame's, for motion vectors |
| `screen` | Width, height, 1 / width, 1 / height |
| `jitter` | This frame's TAA jitter in `xy`, last frame's in `zw` |
| `time` | Time, delta time, frame index |
| `depth` | Near plane, far distance |
| `exposure` | This frame's exposure in `x`, last frame's in `y` |

## Graphite/Passes.glsl

Fragment stage.

| Function | Use |
| --- | --- |
| `Graphite_WriteGBuffer(normal, reflectance, roughness)` | Write the thin G-buffer and motion vectors from an opaque Forward pass. `reflectance` is a `vec3` |
| `Graphite_WriteMotion(currentClip, previousClip)` | Motion vectors alone |
| `Graphite_WriteReactive(amount)` | How much of the pixel shows what is refracted from behind, so temporal effects trust its history less |

## Graphite/Lighting.glsl

Fragment stage. Includes every part of forward lighting. A shader needing less can include only its part.

| File | Gives |
| --- | --- |
| `Graphite/Lights.glsl` | `Graphite_DirectionalCount()`, `Graphite_GetDirectional(i)` (the sun at 0), `Graphite_DirectionalLightShadow(light, i, pos, geomN)`, `Graphite_BeginLights(pos)` and `Graphite_NextLight(it, L)` to walk the local lights reaching a point, `Graphite_LightRadiance(L)`, `Graphite_LocalLightShadow(L, pos, geomN)` |
| `Graphite/Ambient.glsl` | `Graphite_IndirectDiffuse(N, lightmapUV)` (lightmap, probes or ambient), `Graphite_AmbientLight(N)`, `Graphite_SkyAmbient(N)` |
| `Graphite/Probes.glsl` | `Graphite_FindProbes(pos)`, `Graphite_ProbeRadiance(set, N, V, alpha)`, `Graphite_SampleSkyProbe(dir, roughness)` |
| `Graphite/Fog.glsl` | `Graphite_ApplyFog(color, pos)` (fog and volumetric fog), `Graphite_FogColor(pos)` |
| `Graphite/Shadows.glsl` | The shadow atlas. Define `GRAPHITE_HARD_SHADOWS` before including it to take every shadow hard |

## Graphite/PBR

The OpenPBR model the Lit shader uses.

| File | Gives |
| --- | --- |
| `Graphite/PBR/Closure.glsl` | Includes Lighting.glsl and the rest below. `PBR_Prepare(p, pos, V, geomN, mapVariance)`, `PBR_ShadeLights(c)`, `PBR_EvaluateLight(c, l)`, `PBR_EvaluateDiffuse(c, L)`, `PBR_EvaluateSpecular(c, L)`, `PBR_EvaluateAmbient(c, i)`, `PBR_FindProbes(c)`, `PBR_GatherIndirect(c, lightmapUV, probes)`, `PBR_TopReflectance(c, out normal, out roughness)` |
| `Graphite/PBR/Params.glsl` | `PBR_Params` and `PBR_DefaultParams(normal, tangent)` |
| `Graphite/PBR/Microfacet.glsl` | `PBR_Alpha`, `PBR_DistributionGGX`, `PBR_VisibilitySmithGGX` and anisotropic versions |
| `Graphite/PBR/Fresnel.glsl` | `PBR_FresnelDielectric`, `PBR_FresnelF82` |
| `Graphite/PBR/Diffuse.glsl` | `PBR_Eon`, the energy preserving Oren-Nayar diffuse |
| `Graphite/PBR/Fuzz.glsl`, `ThinFilm.glsl`, `Transmission.glsl` | The optional layers |

Define `GRAPHITE_CUSTOM_BRDF` or `GRAPHITE_CUSTOM_AMBIENT_BRDF` before including `Closure.glsl` to supply `Graphite_BRDF` or `Graphite_AmbientBRDF` yourself. Surface Lighting blocks do this for you, see [Custom lighting](06-custom-lighting.md).

## Graphite/Standard/Standard.glsl

Used by surface shaders, and handy in your own passes.

| Function | Use |
| --- | --- |
| `Graphite_SurfaceNormalMap(i, texel, scale)` | A tangent space normal map texel on the surface's frame, as a world normal |
| `Graphite_StandardNormalMap(texel, normal, tangent, bitangent, scale)` | The same on any frame; blends onto an existing normal |
| `Graphite_StandardTangentFrame(normal, tangent, handedness, hasTangent, out t, out b)` | Builds a tangent frame, or an arbitrary one when the mesh has no tangents |
| `Graphite_StandardUV(set, scaleOffset, rotation, i)` | A map's UV from its UV set, scale, offset and rotation, see [Maps](03-properties-and-attributes.md#maps) |

## Graphite/Decals.glsl

| Function | Use |
| --- | --- |
| `Graphite_ApplyDecals(relativePos, geomNormal, inout albedo, inout normal, inout roughness, inout metallic, inout occlusion)` | Applies every decal covering the point. Call it before lighting. Decals are switched by the renderer through the global `GRAPHITE_DECALS` variant, so including the file is all you need |

## Graphite/SceneColor.glsl and SceneDepth.glsl

See [Transparency and screen effects](07-transparency-and-screen-effects.md): `Graphite_ScreenUV()`, `Graphite_PixelRay()`, `Graphite_SampleSceneColor(uv, lod)`, `Graphite_SceneColorMips()`, `Graphite_FetchSceneDepth(uv)`, `Graphite_SceneLinearDepth(uv)`, `Graphite_SceneRelativePosition(uv)` and `Graphite_RelativeToScreenUV(pos)`.

## Graphite/Sky.glsl and Skies.glsl

For sky passes: `Graphite_SkyDirection()`. `Graphite/Skies.glsl` has the built-in skies' parts: `Graphite_SunDirection()`, `Graphite_SunIlluminance()` (the sun's colour times lux), `Graphite_ProceduralSky(...)`, `Graphite_SunDisk(...)`, `Graphite_RotateSkyY(dir, degrees)` and `Graphite_PanoramaUV(dir)`. See [Custom skies](11-custom-skies.md).

## Graphite/Debug.glsl

`Graphite_DebugView(...)` and `Graphite_DebugInputs(...)` let a custom lit shader take part in the editor's debug views (albedo, normals, lighting and so on). Pair them with `#pragma variant global GRAPHITE_DEBUG UNLIT ALBEDO NORMALS ROUGHNESS METALLIC AO EMISSION LIGHTING CASCADES LIGHTMAP_DENSITY`, as the built-in Sprite shader does. `UNLIT` must come first; it is normal drawing.

## Prowl/Common.glsl

| Function | Use |
| --- | --- |
| `gammaToLinearSpace(c)` | sRGB to linear |
| `linearToGammaSpace(c)` | Linear to sRGB |
| `Prowl_Luminance(c)` | Luminance of a linear colour |
| `Prowl_TangentFrame(...)`, `Prowl_ApplyNormalMap(...)` | Prowl's tangent frame and normal map helpers |
