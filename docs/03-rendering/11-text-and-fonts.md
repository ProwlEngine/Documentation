---
title: Text and fonts
description: Put text in the world with a Text Mesh, and import your own fonts.
---

A **Text Mesh** draws text as a mesh in the world, so it sits in the scene like any object. Use it for signs, labels and damage numbers. Text on the screen belongs to the [UI](../11-ui/index.md).

## Quick recipe

1. Choose **GameObject > 3D Object > Text Mesh**. The object reads "New Text".
2. In the **Inspector**, type your words into the **Text Input** box.
3. Set **Font Size** and **Text Color**.
4. Move the object, and turn it to face the camera.

[screenshot needed: a Text Mesh in the Scene view with its Inspector open]

The text uses the built-in Geist font until you assign another.

## Importing a font

Copy a `.ttf` or `.otf` file into `Assets`. The editor imports it as a **FontAsset**, which holds the font file's bytes. The importer has no settings.

To use it, drag the font onto **Font Asset** in the Text Mesh. A script can hold one in a field.

```csharp
public FontAsset Font;
```

A FontAsset reports its `FamilyName` and `Style`, such as Regular or Bold. Each file is one style, so import the bold file to get bold text. `FontAsset.LoadDefault()` returns the built-in font.

## Text Mesh settings

Add one by hand with **Add Component > Rendering > Text Mesh**.

| Property | Default | Effect |
| --- | --- | --- |
| **Text** | empty | The words |
| **Font Asset** | none | The font. None uses the built-in font |
| **Font Size** | 32 | Layout size in pixels. The lowest value is 1 |
| **Quality** | Normal | Resolution of the letter images: `Low`, `Normal`, `High` or `Ultra` |
| **Text Color** | white | Color of the text |
| **Anchor** | Center Middle | Which point of the text block sits on the object |
| **Pixels Per Unit** | 100 | Layout pixels per world unit. Larger makes text smaller |
| **Max Width** | 0 | Wraps lines at this width in layout pixels. 0 does not wrap |
| **Material** | none | Replaces the built-in text material |
| **Shadow Casting** | Off | Whether the text casts shadows |

The anchor also sets how lines align. A left anchor aligns lines left, a right anchor aligns them right, and a middle anchor centers them.

## Sizing text

World height is about `Font Size / Pixels Per Unit` units. The defaults give 0.32 units per line. For text 1 unit tall, set **Font Size** to 100 or **Pixels Per Unit** to 32.

Raise **Quality** when large or close text looks soft. A higher quality uses more space in the font texture.

## Changing text from a script

Set the properties on the component. Each change rebuilds the text mesh on the next frame.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.UI;

public sealed class ScoreLabel : Component
{
    public override void Start()
    {
        var label = GetComponent<TextMeshComponent>();
        label.Text = "Score: 0";
        label.Size = 48;
        label.Anchor = TextAlignment.TopLeft;
    }
}
```

## Fonts and Scribe

**Scribe** is the text library the engine uses to read fonts and lay out letters. A FontAsset wraps a Scribe `FontFile`, and `Quality` is a Scribe `FontQuality`.

The [UI section](../11-ui/index.md) covers text on screen.

## See also

- [Sprites and 2D](10-sprites-and-2d.md)
- [Getting started with UI](../11-ui/01-getting-started-with-ui.md)
