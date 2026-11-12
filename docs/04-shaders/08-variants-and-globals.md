---
title: Variants and globals
description: Compile features in and out with variants, and share values across every material with globals.
---

## Variants

A variant axis is a switch resolved at compile time. Each combination of values is its own compiled shader, so unused features cost nothing at runtime.

Declare axes with pragmas anywhere in the program or its includes:

```glsl
#pragma variant _DETAIL                 // toggle: defines _DETAIL when on
#pragma variant _STYLE SOFT TOON FLAT   // enum: defines _STYLE_SOFT, _STYLE_TOON or _STYLE_FLAT
```

Then branch with the preprocessor:

```glsl
#ifdef _DETAIL
    p.baseColor *= texture(_DetailTex, i.uv * _DetailScale).rgb * 2.0;
#endif

#if defined(_STYLE_TOON)
    // ...
#endif
```

### Setting variants


![A material inspector where setting a texture turns its keyword on](images/keyword-inspector.png)

From properties, so the inspector drives them:

```glsl
_DetailTex("Detail", Texture2D) = "white" {} [Keyword(_DETAIL)]     // on while a texture is set
_Glow("Glow", Integer) = 0 [Toggle(_GLOW)]                           // on while not zero
_Style("Style", Integer) = 0 [KeywordEnum(_STYLE)]                   // picks by index
```

Or from code, which overrides what the properties drive:

```csharp
material.SetKeyword("_DETAIL", true);
material.SetKeyword("_STYLE", "TOON");
bool on = material.IsKeywordEnabled("_DETAIL");
material.RevertKeyword("_DETAIL");   // back to what the properties say
```

### Global axes

```glsl
#pragma variant global MYGAME_WEATHER DRY RAIN SNOW
```

A `global` axis is set for every material at once, by the renderer, a quality level or your code, never by a material. The first value is the default. The engine's own global axes are:

| Axis | Values | Set by |
| --- | --- | --- |
| `PBR_TIER` | `FULL`, `LITE` | The quality level, see [Quality levels](../03-rendering/06-quality.md) |
| `GRAPHITE_DEBUG` | `UNLIT` (normal drawing), `ALBEDO`, `NORMALS`, `ROUGHNESS`, `METALLIC`, `AO`, `EMISSION`, `LIGHTING` and more | The editor's debug views |
| `GRAPHITE_DECALS`, `GRAPHITE_LIGHT_MASKS`, `GRAPHITE_CONTACT_SHADOWS` | toggles | On while the scene has decals, light cookies or profiles, or contact hardening shadows |
| `GRAPHITE_PREPASS` | `DEPTH`, `MOTION`, `NORMALS` | What the camera's effects need from the depth prepass |

A shader that declares one of these must use the same default and only its values, though it may leave values out. A shader declaring `GRAPHITE_DEBUG` with a value `OFF` fails to load.

Set your own global axis from C# by defining it once with its values, then setting it on the renderer:

```csharp
using Prowl.Runtime;

using GlobalAxis = Prowl.Graphite.Rendering.GlobalAxis;

public sealed class WeatherSwitch : Component
{
    private static readonly GlobalAxis Weather = GlobalAxis.Define("MYGAME_WEATHER", "DRY", "RAIN", "SNOW");

    public void LetItSnow() => Graphics.Renderer?.Globals.Set(Weather, "SNOW");
}
```

`GlobalAxis.Toggle("NAME")` defines an on and off axis, set with `Globals.Set(axis, true)`.

### Where pragmas count

Pragmas are found in the program and every file it includes, following `#if`, `#ifdef` and `#else` as far as the pass's own defines decide them. A `#pragma variant` inside `#ifdef GRAPHITE_STANDARD_FORWARD` only exists in the Forward pass. A condition on another variant keeps both branches, so no variant loses a pragma.

### Keep the count down

Every axis multiplies the number of combinations: four toggles is sixteen variants per pass. Variants compile on demand, the first time something draws them, and objects show flat grey until theirs is ready. Builds precompile only the variants your materials use. Prefer a uniform and a branch for cheap switches, and variants for expensive features.

## Globals

A global is a value every material can read, set once from C# rather than per material: wind, wetness, time of day, a player position.

```glsl
#pragma global float _Wetness
#pragma global vec4 _PlayerPosition
```

Read them by name like any property. Put the pragma in a shared include so every shader agrees.

```csharp
Material.SetGlobalFloat("_Wetness", rain.Intensity);
Material.SetGlobalVector("_PlayerPosition", new Float4(p.X, p.Y, p.Z, 1f));
```

Also available: `SetGlobalColor`, `SetGlobalInt`, `SetGlobalMatrix`, `SetGlobalTexture` and `SetGlobalTexture3D`.

> [!NOTE]
> In a material pass, a loose `uniform` that is neither a property nor a global is a compile error. If you meant a shared value, declare it with `#pragma global`.
