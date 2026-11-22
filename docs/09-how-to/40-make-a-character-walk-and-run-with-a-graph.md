---
title: Make a character walk and run with a graph
description: Blend idle, walk and run clips with an animation graph, driven by a Speed value from a script.
---

You end with a character that idles, walks when you hold W and runs when you also hold Shift, blending smoothly between the three. Start with a character that has idle, walk and run clips, such as one from [Play an animation on a loop](01-play-an-animation-on-a-loop.md).

## Steps

1. In the **Project** panel, right-click and choose **Create**, then **Animation Graph**. Name it `Hero`.
2. Select the character's root object. Drag `Hero` into the **Graph** field of its **Animator**.
3. Double-click `Hero` to open the graph editor. Click **Add Node** and add a **State Machine**. If it is not the graph's output, right-click it and choose **Set As Output**.
4. In the **Parameters** panel, click the plus button. Name it `Speed`, choose **Number**, click **Create**.
5. Right-click the empty canvas and choose **Add State**. Name it `Locomotion` in the Inspector. Double-click it to open its graph.
6. Click **Add Node** and add a **Blend 1D**. Wire its output to **State Output**, **Pose**.
7. Add three **Clip** nodes. Set each node's **Clip** to idle, walk and run, and wire them into the Blend 1D inputs.
8. Set each input's threshold: idle 0, walk 1.5, run 5. Drag `Speed` from the **Parameters** panel onto the canvas and wire it to the Blend 1D **Parameter** pin.
9. Add a **Flag** node, turn on **Value**, and wire it to **State Output**, **Enter**. A state with nothing on Enter is never entered.

[screenshot needed: the Locomotion state with Blend 1D, three clips and the Speed parameter wired]

10. Add this script to the character's root object, and press **Play**.

```csharp
using Prowl.Runtime;

public sealed class WalkRun : Component
{
    private Animator _animator;

    public override void OnEnable()
    {
        _animator = GetComponent<Animator>();
        _animator.ApplyRootMotion = true;
    }

    public override void Update()
    {
        float speed = 0f;
        if (Input.GetKey(KeyCode.W)) speed = Input.GetKey(KeyCode.ShiftLeft) ? 5f : 1.5f;
        _animator.SetFloat("Speed", speed);
    }
}
```

## If it does not work

- **The character stays in the first pose.** The state's **Enter** is not open. Check step 9.
- **Feet slide.** See [Locomotion](../05-animation/03-locomotion.md), step 3, for Stride Warp.

## Learn more

- [Locomotion](../05-animation/03-locomotion.md): strafing, turning and foot grounding
- [Graph basics](../05-animation/01-graph-basics.md): why a state needs an open Enter
- [Add a hit reaction with an Any State transition](41-add-a-hit-reaction-with-an-any-state-transition.md)
