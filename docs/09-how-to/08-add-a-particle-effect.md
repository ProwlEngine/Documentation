---
title: Add a particle effect
description: Put a glowing, fading particle effect in your scene and switch it on and off from a script.
---

You end with a particle effect that plays in your scene, fades out as it ages, and starts and stops when you press **Space**.

## Steps

1. Choose **GameObject > Effects > Particle System**. A new object appears and begins to play in the **Scene** view.

[screenshot needed: the Hierarchy with the new Particle System object and the effect in the Scene view]

2. Select the object. Under **Emission**, set **Rate Over Time** to 40.
3. Under **Initial**, set **Start Lifetime** to 1.5 and **Gravity Modifier** to -0.1 so the particles drift up.
4. Under **Shape**, set **Type** to `Sphere` for a ball of particles, or leave `Cone` for a jet.
5. Turn on **Color Over Lifetime**. Set a gradient from yellow to red, with the last stop's alpha at 0.
6. Under **Renderer**, set **Blend Mode** to `Additive` so overlapping particles glow.

[screenshot needed: the Particle System Inspector with Emission, Initial and Renderer sections set]

## Switch it on and off from a script

Add this component to the Particle System object. **Space** starts and stops the effect.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.ParticleSystem;

public sealed class SparkSwitch : Component
{
    public override void Update()
    {
        if (!Input.GetKeyDown(KeyCode.Space)) return;

        var fx = GetComponent<ParticleSystemComponent>();
        if (fx.IsEmitting) fx.Stop();
        else fx.Play();
    }
}
```

Press **Play** in the editor toolbar. Press **Space** and new particles stop. The ones in the air fade out.

To stop an effect from playing at the start, turn off **Play On Enable** on the Particle System.

## If nothing appears

- **Nothing in the Game view.** Check that the object is enabled and **Max Particles** is above 0.

## Learn more

- [Particle systems](../03-rendering/07-particle-systems.md): every module and the Particle shader
- [Materials](../03-rendering/01-materials.md)
