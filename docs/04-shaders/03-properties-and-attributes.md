---
title: Properties and attributes
description: Property types, defaults, inspector attributes and the C# material API.
---

## Declaring properties

```glsl
Properties
{
    PropertyName("Display Name", Type) = DefaultValue [Attribute] [Attribute]
}
```

The default is optional; without one the property is zero. Property names conventionally start with an underscore.

## Types

| Type | Default syntax | GLSL declaration |
| --- | --- | --- |
| `Integer` | `= 4` | `uniform int` |
| `Float` | `= 0.5` | `uniform float` |
| `Vector2` | `= (1, 1)` | `uniform vec2` |
| `Vector3` | `= (0, 1, 0)` | `uniform vec3` |
| `Vector` | `= (0, 1, 0, 0)` | `uniform vec4` |
| `Color` | `= (1, 1, 1, 1)` | `uniform vec4` |
| `Matrix` | `= ((1,0,0,0)(0,1,0,0)(0,0,1,0)(0,0,0,1))` | `uniform mat4` |
| `Texture2D` | `= "white" {}` | `uniform sampler2D` |
| `Texture2DArray` | `= "" {}` | `uniform sampler2DArray` |
| `Texture3D` | `= "" {}` | `uniform sampler3D` |
| `TextureCubemap` | `= "" {}` | `uniform samplerCube` |
| `TextureCubemapArray` | `= "" {}` | `uniform samplerCubeArray` |

A texture's default names a built-in texture, such as `"white"`, `"black"` or `"normal"`, or `""` for none.

## Reading properties in GLSL

Declare a uniform with the same name:

```glsl
uniform vec4 _Tint;
uniform sampler2D _MainTex;

vec3 albedo = texture(_MainTex, uv * _MainTex_ST.xy + _MainTex_ST.zw).rgb * _Tint.rgb;
```

In a material shader, properties are not real uniforms. Graphite rewrites them to read from the material's record in a GPU buffer, which is how thousands of materials draw in a few calls. Three rules follow:

> [!IMPORTANT]
> - **Every uniform a material pass reads must be a declared property** (or a [global](08-variants-and-globals.md)). Reading any other loose uniform is a compile error.
> - **Every texture gets `NAME_ST`**, its scale in `xy` and offset in `zw`. Use it without declaring it.
> - **To pass a material texture into a function**, pass `NAME_Texture` and `NAME_Sampler` and build the sampler inside: `texture(sampler2D(tex, smp), uv)`.

## Attributes


![A material inspector showing headers, sliders, toggles and hidden properties](images/property-attributes-inspector.png)

Attributes go after the default value, each in brackets.

| Attribute | On | Effect |
| --- | --- | --- |
| `[Range(min, max)]` | Float, Integer | A slider between the bounds |
| `[Enum(A, B, C)]` | Integer | A dropdown, stored as the index |
| `[Gamma]` | Color | Entered in gamma space, stored linear |
| `[HDR]` | Color | The colour may go above 1 |
| `[Header("Text")]` | any | A heading above the property |
| `[Space]` | any | A gap above the property |
| `[ShowIf(AXIS)]` | any | Shown only while toggle `AXIS` is on |
| `[ShowIf(AXIS, VALUE)]` | any | Shown only while enum `AXIS` has `VALUE` |
| `[HideInInspector]` | any | Not shown |
| `[NoScaleOffset]` | textures | Hides the tiling and offset fields |
| `[Normal]` | textures | Expects a tangent space normal map |
| `[Keyword(AXIS)]` | textures | Turns toggle `AXIS` on while a texture is set |
| `[Toggle(AXIS)]` | Float, Integer | Turns toggle `AXIS` on while the value is not zero |
| `[KeywordEnum(AXIS)]` | Integer | Sets enum `AXIS` to the value at that index |
| `[TwoSided]` | Float, Integer | With `[Toggle(AXIS)]`: while the toggle is on the material draws both sides whatever its culling, back faces with the normal flipped |
| `[Transmissive]` | Float, Integer | With `[Toggle(AXIS)]`: while the toggle is on the material draws as transparent through its `Transmission` pass |
| `[Map]` | Texture2D | A texture with its own channel, UV set and rotation, see [Maps](#maps) |

`Keyword`, `Toggle` and `KeywordEnum` connect properties to [variants](08-variants-and-globals.md), so a feature compiles in only while it is used:

```glsl
Properties
{
    _DetailTex("Detail", Texture2D) = "white" {} [Keyword(_DETAIL)]
    _DetailScale("Detail Scale", Float) = 8.0 [ShowIf(_DETAIL)]
}
```

A toggle several properties drive is on while any of them is. The Lit shader's `specular_roughness_anisotropy` and `coat_roughness_anisotropy` both drive `PBR_ANISOTROPY` this way.

## Maps

A `[Map]` texture carries more than its scale and offset: which channel a scalar input reads, which UV set it samples, and a rotation. The Lit shader's maps are all `[Map]` textures. In GLSL a map `X` gives you:

| Name | Type | Meaning |
| --- | --- | --- |
| `X` | `sampler2D` | The texture |
| `X_ST` | `vec4` | Scale in `xy`, offset in `zw` |
| `X_Rotation` | `vec2` | The rotation's cosine and sine |
| `X_Channel` | `int` | 0 to 3 for R to A |
| `X_UV` | `int` | 0 for UV0, 1 for UV1 |
| `X_Present` | `bool` | Whether a texture is set |

Inside a surface function, `Graphite_StandardUV(X_UV, X_ST, X_Rotation, i)` gives the UV to sample:

```glsl
uniform float _Wear;
uniform sampler2D _WearMap;   // declared as _WearMap("Wear Map", Texture2D) = "white" {} [Map]

void Surface(inout PBR_Params p, Graphite_SurfaceData i)
{
    float wear = _Wear;
    if (_WearMap_Present)
        wear *= texture(_WearMap, Graphite_StandardUV(_WearMap_UV, _WearMap_ST, _WearMap_Rotation, i))[_WearMap_Channel];
    p.specularRoughness = mix(p.specularRoughness, 0.9, wear);
}
```

## The material API

```csharp
var material = new Material(myShader);

material.SetFloat("specular_roughness", 0.3f);
material.SetInt("_Steps", 8);
material.SetColor("_Tint", new Color(0.8f, 0.2f, 0.1f, 1f));
material.SetVector("_Wind", new Float4(1f, 0f, 0.5f, 0f));
material.SetTexture("_MainTex", albedo);
material.SetTextureScaleOffset("_MainTex", new Float4(4f, 4f, 0f, 0f));   // writes _MainTex_ST
material.SetTextureChannel("_WearMap", 2);       // [Map] textures: read B
material.SetTextureUVSet("_WearMap", 1);         // sample UV1
material.SetTextureRotation("_WearMap", 0.5f);   // radians

material.SetKeyword("_DETAIL", true);
float roughness = material.GetFloat("specular_roughness");
```

- Changing a shared material asset changes every object that uses it. For a per-object value, `Clone()` the material and assign the copy, then dispose clones you no longer need.
- `material.Surface` sets opaque, cutout or transparent, the blend and the culling. See [Transparency and screen effects](07-transparency-and-screen-effects.md).
- `material.RenderQueue` and `material.CastShadows` override the shader's defaults.
- A keyword the shader does not have, or a value its axis does not take, is kept on the material but ignored, with a warning in the console.
