---
title: Add a hit reaction with an Any State transition
description: Interrupt whatever a character is doing with a one-shot hit animation, then return to normal.
---

You end with a character that plays a hit reaction when a script calls `Hit()`, from any state, then goes back to what it was doing. Start with the `Hero` graph from [Make a character walk and run with a graph](40-make-a-character-walk-and-run-with-a-graph.md), and a hit reaction clip in the character's model.

## Steps

1. Double-click the graph to open it. If you are inside the `Locomotion` state, click the root in the breadcrumb at the top.
2. In the **Parameters** panel, click the plus button. Name it `Hit`, choose **Trigger**, click **Create**.
3. Right-click the empty canvas and choose **Add State**. Name it `Hit` in the Inspector.
4. Right-click again and choose **Add Any State**. A machine has one at most.
5. Drag from **Any State** to `Hit`, then from `Hit` to `Locomotion`. Each drag adds a transition. Select one to set its **Duration (s)** in the Inspector.

[screenshot needed: the state machine with Any State, Hit and Locomotion and two transitions]

6. Double-click `Hit` to open it. Add a **Clip** node. Set **Clip** to your hit reaction and **Looping** to `Once`. Wire it to **State Output**, **Pose**.
7. Drag `Hit` from the **Parameters** panel onto the canvas. Wire it to **State Output**, **Enter**.
8. Add a **State Done** node and wire it to **State Output**, **Exit**.
9. Add a script like this to the character's root object. Call `Hit()` from your damage code.

```csharp
using Prowl.Runtime;

public sealed class HitReaction : Component
{
    private Animator _animator;

    public override void OnEnable() => _animator = GetComponent<Animator>();

    public void Hit() => _animator.SetTrigger("Hit");
}
```

[screenshot needed: the Hit state with Clip, Parameter and State Done wired]

10. To test it, press **Play**, and call `Hit()` from a key press in `Update`.

## If it does not work

- **Nothing happens.** The `Hit` state needs a wired **Enter**. An unwired Enter never lets the Any State in.
- **It never returns.** Wire **State Done** into **Exit**, and set the clip's **Looping** to `Once`.

## Learn more

- [Graph basics](../05-animation/01-graph-basics.md): the gate rule, Any State and triggers
- [Parameters and values](../05-animation/02-parameters-and-values.md)
