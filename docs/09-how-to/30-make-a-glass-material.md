---
title: Make a see-through glass material
description: Make a glass sphere that refracts the scene behind it, with no custom shader.
---

You end with a glass sphere that bends and tints the objects behind it. It uses the built-in Lit shader, so you write no shader code.

## Steps

1. Choose **GameObject > 3D Object > Cube** and place it in view. This is something for the glass to refract.
2. Choose **GameObject > 3D Object > Sphere** and place it between the camera and the cube.
3. In the **Project** panel, choose **Assets > Create > Material** and name it `Glass`.
4. Select the material. In the **Inspector**, check that **Shader** is the built-in Lit shader.
5. Under **Transmission**, set **Transmission Weight** to 1. The material now draws as see-through.
6. Set **Specular Roughness** to 0.05 for clear glass. Raise it for frosted glass.
7. Set **Transmission Color** to a pale green or blue for a tint.
8. Assign the `Glass` material to the sphere's **Mesh Renderer**, then look at the sphere in the **Scene** view.

[screenshot needed: the Glass material in the Inspector with the Transmission group set]

[screenshot needed: the glass sphere in front of a cube, refracting it]

## Flat panes and windows

A window pane has no inside to bend light through. On a plane or thin mesh, turn on **Geometry Thin Walled** in the material. Light then passes straight through.

## Set it from a script

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class GlassSetup : Component
{
    public override void Start()
    {
        var material = new Material(Shader.LoadDefault(DefaultShader.Lit));
        material.SetFloat("transmission_weight", 1f);
        material.SetFloat("specular_roughness", 0.05f);
        material.SetColor("transmission_color", new Color(0.8f, 0.95f, 0.9f, 1f));
        GetComponent<MeshRenderer>()!.Material = material;
    }
}
```

## Learn more

- [Transparency and screen effects](../04-shaders/07-transparency-and-screen-effects.md#transmission): thickness, scatter and dispersion
- [Materials](../03-rendering/01-materials.md): every Lit property
