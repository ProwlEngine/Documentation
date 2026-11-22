---
title: Sprites and 2D
description: Import an image as a sprite, draw it with a Sprite Renderer, slice sprite sheets, and set up a 2D camera.
---

A **sprite** is a flat image drawn in the world. The **Sprite Renderer** component draws one on the XY plane of its object. Use it for 2D games, billboards and icons in a 3D scene.

## Quick recipe

1. Copy a `.png` file into your `Assets` folder.
2. Select it. In the **Inspector**, set **Texture Type** to **Sprite** and click **Apply**.
3. Select an empty object and click **Add Component > Rendering > Sprite Renderer**.
4. Set **Sprite** to the sprite you imported.

[screenshot needed: a Sprite Renderer in the Inspector with a sprite assigned, and the sprite in the Scene view]

Dragging a sprite into the Scene view does steps 3 and 4 for you.

## Importing a texture as a sprite

A texture imports as a plain texture until its **Texture Type** is **Sprite**. See [Assets and importers](../07-editor/04-assets-and-importers.md) for **Apply**.

| Setting | Effect |
| --- | --- |
| **Sprite Mode** | **Single** makes one sprite from the whole image. **Multiple** makes one per slice |
| **Pixels Per Unit** | Image pixels that equal one world unit. Default 100 |
| **Mesh Type** | **Full Rect** draws a quad. **Tight** follows the opaque shape |
| **Open Sprite Editor** | Opens the Sprite Editor on this texture |

Each sprite is a **sub-asset** of the texture: a separate asset stored inside it. See [Sub-assets](../07-editor/04-assets-and-importers.md#sub-assets).

## The Sprite Editor

Cut a sprite sheet into many sprites here. Open it with **Open Sprite Editor** in the texture's Inspector, or from **Window > Tools > Sprite Editor**.

1. Set **Sprite Mode** to **Multiple**.
2. Open the Sprite Editor and click **Slicing**.
3. Pick a **Mode**, fill in its fields, and click **Slice**.
4. Click a rect to set its **Name** and **Pivot**, the point of the sprite that sits on the object's position.
5. In the texture's Inspector, click **Apply**.

| Slicing mode | Cuts |
| --- | --- |
| **Automatic** | One rect per connected opaque region |
| **GridBySize** | Cells of a fixed **Pixel Size** |
| **GridByCount** | A fixed **Column / Row Count** |
| **Isometric** | A staggered grid, alternate rows offset by half a cell |

**Revert** discards unapplied edits.

[screenshot needed: the Sprite Editor with a sheet sliced into a grid and one rect selected]

## The Sprite Renderer

Add one with **Add Component > Rendering > Sprite Renderer**.

| Property | Default | Effect |
| --- | --- | --- |
| **Sprite** | none | The sprite to draw. Nothing draws without one |
| **Color** | white | Tint multiplied into the sprite |
| **Flip X**, **Flip Y** | off | Mirrors the sprite about its pivot |
| **Material** | none | Replaces the built-in sprite material |
| **Sorting Order** | 0 | Higher values draw in front |
| **Shadow Casting** | Off | Whether the sprite casts shadows |

The default material is unlit and alpha blended. See [Built-in shaders](../04-shaders/12-built-in-shaders.md). A custom material gets the sprite as `_MainTex`.

## Sorting

Each **Sorting Order** step moves the sprite 0.0001 units along its own Z axis, so a higher order draws in front.

## A 2D camera

An orthographic camera has no perspective, so objects keep their size at any distance. That suits 2D.

1. Select **GameObject > Camera**.
2. Set **Projection Mode** to **Orthographic**.
3. Set **Orthographic Size**. It is half the view height in world units. The default is 5.
4. Place the camera in front of the sprites, looking at the XY plane.

For one image pixel per screen pixel at 100 pixels per unit, use screen height / 200.

## Lines

A **Line Renderer** draws a ribbon through a list of points in the object's local space. Add it with **Add Component > Rendering > Line Renderer**. It needs a **Material** and two **Points**.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;
using Prowl.Vector;

public sealed class Beam : Component
{
    public override void Start()
    {
        var line = AddComponent<LineRenderer>();
        line.Material = new Material(Shader.LoadDefault(DefaultShader.Line));
        line.Points = [new Float3(0, 0, 0), new Float3(3, 1, 0)];
    }
}
```

| Property | Default | Effect |
| --- | --- | --- |
| **Start Width**, **End Width** | 0.1 | Width in world units at each end |
| **Start Color**, **End Color** | white | Color at each end |
| **Loop** | off | Joins the last point to the first |
| **Texture Mode** | Stretch | `Stretch`, `Tile` by distance, or `RepeatPerSegment` |

## See also

- [Text and fonts](11-text-and-fonts.md)
- [Cameras and post processing](02-cameras-and-post-processing.md)
