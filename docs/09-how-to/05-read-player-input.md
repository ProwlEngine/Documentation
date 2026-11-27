---
title: Read player input
description: Move an object with WASD through an Input Actions asset, so you can add gamepad controls later without code changes.
---

You end with an object that moves when you hold W, A, S or D. The controls live in an asset, so you can change them without editing code.

## Steps

1. In the **Project** panel, right-click and choose **Create > Input Actions**. Name it `Controls`.
2. Select `Controls`. In the **Inspector**, click **Action**.
3. Open the new action. Change **Name** to `Move` and **Kind** to **Vector2**.
4. Click **Add binding** and choose the **WASD** preset.

[screenshot needed: the Move action open with the WASD composite listed]

5. Click **Save** at the bottom of the Inspector.
6. Create a C# script named `Walker` with the code below. Add it to a GameObject.
7. Drag `Controls` from the **Project** panel onto the **Controls** field of **Walker**.
8. Press **Play** and hold W, A, S or D. The object moves.

[screenshot needed: the Walker component with the Controls field filled]

```csharp
using Prowl.Runtime;
using Prowl.Vector;

public sealed class Walker : Component
{
    public AssetRef<InputActionMap> Controls;
    public float Speed = 4f;

    private InputActionMap _map;
    private InputAction _move;

    public override void OnEnable()
    {
        _map = Controls.LoadImmediate();
        Input.RegisterActionMap(_map);
        _map.Enable();
        _move = _map.GetAction("Move");
    }

    public override void OnDisable() => _map.Disable();

    public override void Update()
    {
        Float2 move = _move.ReadValue<Float2>();
        Transform.Position += new Float3(move.X, 0f, move.Y) * Speed * Time.DeltaTime;
    }
}
```

## If it does not work

- **The object does not move.** Check that you called `Enable()` on the map and that **Controls** is not empty.
- **An error says the action was not found.** The name in `GetAction` must match the action's **Name** exactly.
- **You changed the bindings and nothing happened.** Click **Save** in the Inspector.

## Learn more

- [Input actions](../02-scripting/09-input-actions.md): kinds, composites, interactions and reading values
- [Input and time](../02-scripting/03-input-and-time.md)
