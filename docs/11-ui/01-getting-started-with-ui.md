---
title: Getting started with UI
description: Build a canvas with text and a button, and learn how Prowl lays out and draws GameObject UI.
---

A **GameCanvas** is a component that turns the GameObjects below it into UI. Its children are laid out with **RectTransforms**, drawn on top of the game, and can react to the mouse. You use it for menus, HUDs and panels that you build in the editor.

## Quick recipe

This script builds a canvas with one button. Add it to any GameObject and press Play. Each click changes the button's text.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.UI;
using Prowl.Vector;

public sealed class ClickCounter : Component
{
    public override void Start()
    {
        GameObject canvasObject = new("Canvas");
        canvasObject.AddComponent<GameCanvas>();
        new GameObject("Event System").AddComponent<EventSystem>();

        GameObject buttonObject = new("Button");
        buttonObject.SetParent(canvasObject, false);
        buttonObject.EnsureRectTransform().SizeDelta = new Float2(260f, 60f);
        UIImage image = buttonObject.AddComponent<UIImage>();
        UIButton button = buttonObject.AddComponent<UIButton>();
        button.TargetGraphic = image;

        GameObject labelObject = new("Label");
        labelObject.SetParent(buttonObject, false);
        RectTransform labelRect = labelObject.EnsureRectTransform();
        labelRect.AnchorMin = Float2.Zero;
        labelRect.AnchorMax = Float2.One;
        labelRect.SizeDelta = Float2.Zero;
        TextComponent label = labelObject.AddComponent<TextComponent>();
        label.Text = "Clicked 0 times";
        label.Color = new Color(0.1f, 0.1f, 0.12f, 1f);

        int clicks = 0;
        button.OnClick += () => label.Text = $"Clicked {++clicks} times";
    }
}
```

You see a white button in the middle of the screen. It dims slightly on hover and more when pressed.

To build the same thing in the editor, see [Show a button on screen](../09-how-to/06-show-a-button-on-screen.md).

## Canvas

A GameCanvas is the root of one UI hierarchy. Everything under it is part of that UI. The canvas itself does not need a RectTransform. Create one with **GameObject > UI > Canvas**.

| Property | Use |
| --- | --- |
| **RenderMode** | `ScreenSpaceOverlay` draws over the screen. `WorldSpace` makes the canvas a panel in the scene. |
| **SortOrder** | Draw order between screen canvases. Higher draws on top. |
| **UIScaleMode** | `ConstantPixelSize` uses **ScaleFactor** as is. `ScaleWithScreenSize` scales from **ReferenceResolution** (default 1280 x 720). |
| **ScreenMatchMode** | How `ScaleWithScreenSize` fits the screen: `MatchWidthOrHeight`, `Expand` or `Shrink`. |
| **MatchWidthOrHeight** | Blend between matching width (0) and height (1). Default 0.5. |

A world-space canvas uses its **ReferenceResolution** as its size. One design pixel is one world unit, so scale the GameObject's transform down to size it.

## Rect transform

A **RectTransform** places a UI element inside its parent's rectangle. Every UI GameObject has one.

| Property | Meaning |
| --- | --- |
| **AnchorMin**, **AnchorMax** | Corners of the anchor rectangle, from 0 to 1 of the parent. Default is the center. |
| **Pivot** | The point the element rotates and sizes around, from 0 to 1. |
| **AnchoredPosition** | Offset of the pivot from the anchor, in pixels. |
| **SizeDelta** | The size when the anchors are together. When apart, the size added to the anchor rectangle. Default is 100 x 100. |

To fill the parent, set the anchors to (0, 0) and (1, 1), and **SizeDelta** to zero. The recipe does this for the label.

## UI components

Every component below is on the **UI** menu in **Add Component**.

| Component | What it does |
| --- | --- |
| **Image** (`UIImage`) | Draws a color or a sprite. |
| **Text** (`TextComponent`) | Draws a string. Uses the built-in font unless you set **Font**. |
| **Canvas Group** | Sets alpha and **Interactable** for all children. |
| **Rect Mask** | Clips children to its rectangle. |
| **Button** | Raises `OnClick` when clicked or submitted. |
| **Toggle**, **Slider**, **Scroll View**, **Input Field**, **Dropdown**, **Scrollbar** | Ready-made controls. |
| **Horizontal**, **Vertical** and **Grid Layout Group** | Arrange children in a row, column or grid. |
| **Layout Element**, **Content Size Fitter** | Give a child a preferred size, or size a parent to its content. |

**GameObject > UI** also has **Panel**, which is a stretched, translucent Image.

## Input

Mouse input needs an **Event System** in the scene. It sends hover, press, drag, click and scroll events to the UI under the pointer. Without one, the canvas still draws but ignores input. Adding an element from **GameObject > UI**, such as a Button, creates one if the scene has none.

A Button has two ways to react. Subscribe to `OnClick` from code, or add calls to its **ClickAction** list in the Inspector. For other events, implement the interfaces in `Prowl.Runtime.UI`, such as `IPointerClickHandler`, `IPointerEnterHandler` and `IDragHandler`, on your own component.

## How it relates to Paper

GameObject UI and [Paper](02-drawing-ui-with-paper.md) are separate systems. A canvas is data in the scene that you edit and save. Paper is code that runs every frame in `OnGui`. You can use both in one game.

## See also

- [Drawing UI with Paper](02-drawing-ui-with-paper.md)
- [Show a button on screen](../09-how-to/06-show-a-button-on-screen.md)
