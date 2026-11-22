---
title: Show a button on screen
description: Put a clickable button on the screen of your game and run code when the player clicks it.
---

You end with a button over your game that logs a message when you click it in play mode.

## Steps

1. Open a scene. Choose **GameObject > UI > Button**. The editor creates a **Canvas**, an **Event System** and a **Button** under the canvas.

[screenshot needed: the Hierarchy with Canvas, Button and Event System, and the button in the Scene view]

2. Select the **Button**. In the **Inspector**, find **Rect Transform**. Set **SizeDelta** to `260` by `60`. It sits in the middle of the screen.
3. With the **Button** still selected, choose **GameObject > UI > Text**. The new **Text** becomes a child of the button.
4. Select the **Text**. Set **Text** to `Start`. Set **Color** to a dark color, because the button is white.

[screenshot needed: the Text's Inspector with Text and Color set]

5. In the **Project** panel, choose **Assets > Create > C# Script**, name it `StartButton`, and paste the code below.
6. Select the **Button**, choose **Add Component**, and add **StartButton**.
7. Press **Play** in the editor toolbar. Click the button in the **Game** view. The **Console** shows `Start clicked`.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.UI;

public sealed class StartButton : Component
{
    private UIButton _button;

    public override void OnEnable()
    {
        _button = GetComponent<UIButton>();
        _button.OnClick += OnClicked;
    }

    public override void OnDisable() => _button.OnClick -= OnClicked;

    private void OnClicked() => Debug.Log("Start clicked");
}
```

## If it does not work

- **Nothing happens on click.** Check that the scene has an **Event System**. A scene without one draws UI but ignores the mouse.
- **The button does not appear.** Check that it is a child of the **Game Canvas** object.
- **The text is invisible.** Text is white by default. Set its **Color** on the **Text** component.

## Learn more

- [Getting started with UI](../11-ui/01-getting-started-with-ui.md): canvases, rect transforms and the other UI components
- [Drawing UI with Paper](../11-ui/02-drawing-ui-with-paper.md): draw buttons from code instead
