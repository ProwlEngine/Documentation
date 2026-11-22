---
title: Play an animation on a loop
description: Get an animated FBX or glTF character playing on a loop in your scene, with no graph and no code.
---

You end with an animated character playing its animation on a loop when you press Play. This works for a Mixamo character or any FBX or glTF file that contains an animation.

## Steps

1. Download the character as FBX.
2. Copy the file into your project's `Assets` folder, or drag it into the **Project** panel. The editor imports it by itself.

[screenshot needed: the FBX file in the Project panel]

3. Select the file in the **Project** panel. In the **Inspector**, open the **Animation** tab.
4. Leave **Rig Type** on **Generic**. It works for a character with its own animation.
5. Leave **Import Animations** and **Loop Animations** on. Both are on by default.

[screenshot needed: the Animation tab with Rig Type, Loop Animations and the clips list]

If you change any setting, click **Apply** at the bottom of the Inspector. The model imports again.

6. Drag the file from the **Project** panel into the **Hierarchy** or the **Scene** view. The character appears in the scene.
7. Select the character's root object. The importer already added an **Animator** with the rig and the clips filled in, and **Play Automatically** is on.
8. Press **Play** in the editor toolbar. The first clip in the Animator's **Clips** list plays on a loop.

[screenshot needed: the Animator in the Inspector with Avatar, Clips and Play Automatically]

## If it does not play

- **Nothing moves.** On the Animator, check that **Avatar** is set and **Clips** is not empty. If not, set **Rig Type** to Generic in the model's **Animation** tab and click **Apply**.
- **The wrong clip plays.** Play Automatically plays the first clip. Move the clip you want to the top of **Clips**, or use the script below.
- **It plays once and stops.** In the model's **Animation** tab, select the clip in the **Clips** table, turn on **Loop**, and click **Apply**.

## Play it from a script instead

Use this when you want the code to choose the clip. Put the name shown in **Clips** in the call.

```csharp
using Prowl.Runtime;

public sealed class PlayWalk : Component
{
    public override void OnEnable() => GetComponent<Animator>().Play("Walk");
}
```

The clip still loops only if its **Loop** setting is on.

## Learn more

- [Animation](../05-animation/index.md): rig types, clip settings and the Animator
- [Switch between two animations](02-switch-between-two-animations.md)
- [Make a character walk and run with a graph](40-make-a-character-walk-and-run-with-a-graph.md)
