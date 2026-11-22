---
title: Terrain
description: Create a heightmap terrain, sculpt and paint it, and add grass, details and trees.
---

A **terrain** is a large landscape drawn from a heightmap, a grid of heights. The **Terrain** component draws it and a **Terrain Data** asset stores its shape, paint and vegetation. Use it for hills, fields and forests too big to model by hand.

## Quick recipe

1. Choose **GameObject > 3D Object > Terrain**. [screenshot needed: the GameObject menu with 3D Object > Terrain]
2. Select the new object and choose the **Terrain** scene tool. The Inspector shows a mode rail.
3. Pick **Sculpt** on the rail, then drag on the terrain in the Scene view to raise it.
4. Pick **Paint**, choose a layer and drag to paint it.

The terrain is flat, 1024 by 1024 units, and collides, because the menu also adds a [Terrain Collider](#terrain-collider). It also creates `New Terrain Data.terraindata` in your `Assets` folder.

## Terrain Data

**Terrain Data** is a `.terraindata` asset holding the landscape. The component's **Terrain Data** field points at it.

| Field | Default |
| --- | --- |
| `Size` (width and depth) | 1024 |
| `Height` (tallest point) | 100 |
| `HeightmapResolution` | 513 |
| `SplatmapResolution` (paint) | 512 |
| `DetailResolution` (grass) | 1024 |

The corner is at the object's position. The terrain extends along +X and +Z.

## Editing modes

The rail in the Terrain Inspector has six modes. Drag in the Scene view to apply one. The Scene view tool strip repeats them, plus **Move**.

| Mode | Dragging does |
| --- | --- |
| **Sculpt** | **Raise**, **Lower**, **Flatten** (with a **Target Height** from 0 to 1) or **Smooth** |
| **Paint** | Paints the selected layer |
| **Holes** | Cuts holes. Shift drag fills them |
| **Details** | Paints grass density. Shift drag erases |
| **Trees** | Click places trees. Shift click erases |
| **Settings** | Size, resolution, distances. No brush |

The brush sliders are **Size** (default 5, up to 500), **Strength** (0.5) and **Falloff** (0.5, the share of the radius that fades; 0 is a hard edge).

[screenshot needed: the Terrain Inspector with the mode rail and brush sliders]

## Layers and materials

A **layer** is one surface texture, such as grass or rock. Paint mode blends up to 8. A new terrain has 4.

1. Choose **Paint** on the rail.
2. Click the plus button in **Splat Layers** to add a layer.
3. Select it and set **Albedo**, and optionally **Normal Map**, **Tiling** (10), **Roughness** (1) and **Metallic** (0).
4. Drag in the Scene view to paint.

The component's **Material** (in **Settings**) draws the surface. The menu assigns the built-in Terrain material. See [Built-in shaders](../04-shaders/12-built-in-shaders.md).

## Details and trees

A **detail** is a small object such as grass, scattered by a density map you paint in **Details** mode. Add one with the plus button in **Detail Prototypes**. **Render Mode** is `TextureBillboard` (faces the camera), `TextureNonBillboard` (fixed direction) or `Mesh` (your mesh and materials).

Texture modes use the prototype's **Grass Material**, else the terrain's **Detail Material**, else the built-in Grass material. Width, height, bend, **Healthy Color** and **Dry Color** shape each blade.

A **tree prototype** is a mesh, materials and a **Bend Factor** for wind. In **Trees** mode, add one and click the terrain to place trees.

| Setting | Default | Effect |
| --- | --- | --- |
| **Detail Distance** | 150 | How far details draw |
| **Detail Density** | 2 | Cells per metre. Cost grows with its square |
| **Detail Cascades** | 4 | Bands out to that distance. Each draws a quarter as many blades |
| **Tree View Distance** | 500 | How far trees draw |
| **Max LOD Levels** | 4 | Surface mesh subdivisions |

Mesh details are capped at 20000 instances per prototype.

## Terrain Collider

The **Terrain Collider** (**Add Component > Physics > Colliders > Terrain Collider**) makes the heightmap solid. Holes have no collision. Read the ground height with `GetWorldHeight`.

```csharp
using Prowl.Runtime;

public sealed class GroundSnap : Component
{
    public TerrainCollider Ground;

    public override void Update()
    {
        var p = Transform.Position;
        Transform.Position = new Float3(p.X, Ground.GetWorldHeight((float)p.X, (float)p.Z), p.Z);
    }
}
```

## See also

- [Built-in shaders](../04-shaders/12-built-in-shaders.md)
- [Materials](01-materials.md)
