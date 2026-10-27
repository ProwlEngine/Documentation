---
title: Include library reference
description: The Graphite and Prowl include files and the functions they provide.
---

## Relative and world

Positions in Graphite shaders are **relative**: world space moved so the camera sits at the origin, which keeps precision far from it. **World** means true world space. Functions and parameters say which they take: `relativePos`, `Graphite_ObjectToRelative`, `Graphite_RelativeToWorld`. Directions and normals are world space.

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
| `vertexUV0` … `vertexUV3`, `vertexCustom0`, `vertexCustom1` | More streams |
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
| `Graphite_RelativeToClip(p)` | Clip position of a camera relative point |
| `Graphite_RelativeToWorld(p)` | The world position of a relative one, for noise and patterns |
| `Graphite_ViewDir(relativePos)` | Unit direction from a point to the camera |
| `Graphite_LinearDepth(depth)` | Distance along the view from a raw depth |
| `Graphite_RelativeFromDepth(uv, depth)` | Camera relative position from screen UV and depth |
| `Graphite_ViewRay(clipXY)` | The direction a clip position looks along |

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

## Graphite/Passes.glsl

Fragment stage.

| Function | Use |
| --- | --- |
| `Graphite_WriteGBuffer(normal, roughness, metallic)` | Write the thin G-buffer and motion vectors from an opaque Forward pass |
| `Graphite_WriteMotion(currentClip, previousClip)` | Motion vectors alone |

## Graphite/Lighting.glsl

Fragment stage. Define `GRAPHITE_CUSTOM_BRDF` or `GRAPHITE_CUSTOM_AMBIENT_BRDF` before including it to supply `Graphite_BRDF` or `Graphite_AmbientBRDF` yourself. Surface Lighting blocks do this for you.

| Function | Use |
| --- | --- |
| `Graphite_MakeSurface(pos, N, geomN, V, albedo, metallic, roughness, ao)` | Build a surface |
| `Graphite_ShadeLights(s)` | All lights through the BRDF |
| `Graphite_DefaultBRDF(s, c)` | Prowl's BRDF: GGX, Smith, Fresnel and Disney diffuse |
| `Graphite_AmbientBRDF(s, irradiance, specular)` | How ambient light and reflections shade a surface |
| `Graphite_IndirectDiffuse(N, lightmapUV)` | Ambient light |
| `Graphite_IndirectSpecular(pos, N, V, F0, roughness, ao, ambient)` | Reflections |
| `Graphite_SkyAmbient(N)` | The sky's light along a normal |
| `Graphite_DirectionalCount()`, `Graphite_GetDirectional(i)` | Directional lights, the sun at 0 |
| `Graphite_DirectionalLightShadow(light, i, pos, geomN)` | A directional light's shadow, 1 is lit |
| `Graphite_BeginLights(pos)`, `Graphite_NextLight(it, L)` | Iterate the local lights reaching a point |
| `Graphite_LightRadiance(L)`, `Graphite_LocalLightShadow(L, pos, geomN)` | A local light's colour and shadow |
| `Graphite_ViewDir(pos)` | Unit direction to the camera |
| `ApplyFog(color, pos)`, `FogColor(pos)` | Scene fog |

## Graphite/Standard/Standard.glsl

Used by surface shaders, and handy in your own passes.

| Function | Use |
| --- | --- |
| `Graphite_SurfaceNormalMap(s, texel, scale)` | A tangent space normal map texel on the surface's frame, as a world normal |
| `Graphite_StandardNormalMap(texel, normal, tangent, bitangent, scale)` | The same on any frame; blends onto an existing normal |
| `Graphite_StandardTangentFrame(normal, tangent, handedness, hasTangent, out t, out b)` | Builds a tangent frame, or an arbitrary one when the mesh has no tangents |

## Graphite/Decals.glsl

| Function | Use |
| --- | --- |
| `Graphite_ApplyDecals(relativePos, geomNormal, inout albedo, inout normal, inout roughness, inout metallic, inout occlusion)` | Applies every decal covering the point. Call it before lighting. Decals are switched by the renderer through the global `GRAPHITE_DECALS` variant, so including the file is all you need |

## Standard lighting entry points

These are what the standard shader calls. Use them in your own passes to get the standard features.

| Function | Use |
| --- | --- |
| `CalculateForwardLighting(pos, N, geomN, V, albedo, metallic, roughness, ao)` | All direct light, the same as `Graphite_ShadeLights` |
| `CalculateForwardLighting(..., ao, translucency, power, distortion, scale)` | Direct light with subsurface translucency |
| `CalculateForwardLightingAniso(pos, N, geomN, V, tangent, bitangent, albedo, metallic, roughness, anisotropy, ao)` | Direct light with anisotropic highlights |

## Graphite/PBR.glsl

Building blocks: `DistributionGGX`, `GeometrySmith`, `FresnelSchlick`, `EnvBRDF`, `DisneyDiffuse`, `DistributionGGXAniso`, `ApplySpecularAA` and `ParallaxOcclusionMapping(heightTex, heightSampler, uv, viewDirTS, scale, steps)`. `PI` is defined.

## Graphite/SceneColor.glsl and SceneDepth.glsl

See [Transparency and screen effects](07-transparency-and-screen-effects.md): `Graphite_ScreenUV()`, `Graphite_SampleSceneColor(uv, lod)`, `Graphite_SceneColorMips()`, `Graphite_FetchSceneDepth(uv)`, `Graphite_SceneLinearDepth(uv)`, `Graphite_SceneRelativePosition(uv)` and `Graphite_RelativeToScreenUV(pos)`.

## Graphite/Sky.glsl

For sky passes: `Graphite_SkyDirection()`. See [Custom skies](11-custom-skies.md).

## Graphite/Debug.glsl

`Graphite_DebugView(...)` and `Graphite_DebugInputs(...)` let a custom lit shader take part in the editor's debug views (albedo, normals, lighting and so on). Pair them with `#pragma variant global GRAPHITE_DEBUG OFF UNLIT ALBEDO NORMALS ROUGHNESS METALLIC AO EMISSION LIGHTING CASCADES LIGHTMAP_DENSITY`.

## Prowl/Common.glsl

| Function | Use |
| --- | --- |
| `gammaToLinearSpace(c)` | sRGB to linear |
| `linearToGammaSpace(c)` | Linear to sRGB |
