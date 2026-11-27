---
title: Switch between two animations
description: Fade a character from one animation to another from a script, with no animation graph.
---

You end with a character that plays one animation and fades to another when you press Space. Start from [Play an animation on a loop](01-play-an-animation-on-a-loop.md), with a character that has two or more clips.

## Steps

1. Import a model that contains both animations, such as an idle and a walk. In the model's **Animation** tab, the **Clips** table lists them.
2. Drag the model into the scene. Its **Animator** lists the clips in **Clips**.
3. Create a script named `ToggleAnimation.cs` in `Assets` with the code below.
4. Add the script to the character's root object, the one with the **Animator**.
5. Press **Play**. The first clip plays. Press Space to fade to the second clip, and again to fade back.

```csharp
using Prowl.Runtime;

public sealed class ToggleAnimation : Component
{
    public float FadeSeconds = 0.25f;

    private Animator _animator;
    private int _index;

    public override void OnEnable() => _animator = GetComponent<Animator>();

    public override void Update()
    {
        if (!Input.GetKeyDown(KeyCode.Space)) return;
        _index = (_index + 1) % 2;
        _animator.CrossFade(_animator.Clips[_index], FadeSeconds);
    }
}
```

[screenshot needed: the script on the character with the Animator beside it]

## If it does not work

- **Nothing changes on Space.** Check that **Clips** holds at least two clips.
- **The second clip stops after one play.** Turn on **Loop** for that clip in the model's **Animation** tab and click **Apply**.

## Learn more

- [Animation](../05-animation/index.md): the Animator and clip settings
- [Make a character walk and run with a graph](40-make-a-character-walk-and-run-with-a-graph.md): for more than two animations
- [Input and time](../02-scripting/03-input-and-time.md)
