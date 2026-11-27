---
title: Particle systems
description: Make fire, smoke, sparks and other effects from many small particles, and start or stop them from a script.
---

A **particle** is one small, short-lived quad or mesh. A **particle system** is a component that spawns thousands of them. It moves them by rules you set and draws them together as one effect.

You use one for fire, smoke, sparks, rain and magic. The component is `ParticleSystemComponent`. Its settings are split into **modules**, groups of settings you switch on as you need them.

## Quick recipe

1. Choose **GameObject > Effects > Particle System**.
2. Select it. Small particles play in the **Scene** view.
3. In the **Inspector**, raise **Rate Over Time** under **Emission** to 40.
4. Turn on **Color Over Lifetime** and set a gradient from yellow to transparent red.

[screenshot needed: the Scene view with the default particles]

To start and stop it from a script, see [Add a particle effect](../09-how-to/08-add-a-particle-effect.md), which has the full steps and a script.

## Main settings

These sit at the top of the component. Add one with the menu above, or with **Add Component > Effects > Particle System**.

| Setting | Default | Effect |
| --- | --- | --- |
| **Duration** | 5 | Seconds in one loop |
| **Looping** | on | Starts the loop again when it ends |
| **Simulation Space** | Local | `Local` particles move with the object. `World` particles stay where they were born. `Custom` follows another object |
| **Play On Enable** | on | Plays when the component is enabled |
| **Stop Action** | None | `Disable` or `Destroy` the object when the system finishes |


## Modules

**Initial**, **Emission**, **Shape** and **Renderer** start enabled. Every other module starts off until you turn on its toggle.

| Module | What it does |
| --- | --- |
| **Initial** | Start lifetime, speed, size, rotation, color and **Gravity Modifier** |
| **Emission** | **Rate Over Time**, **Rate Over Distance** (per unit the emitter moves), and a list of **Bursts** |
| **Shape** | Where particles are born and which way they go. Types are Sphere, Hemisphere, Cone, Box, Circle, Donut, Edge, Rectangle and Mesh |
| **Over Lifetime**, **By Speed** | Modules such as **Color Over Lifetime**. Velocity, force, color, size and rotation change with age or speed |
| **Wind** | **Ambient Wind**, the nearest `WindZone`, and turbulence |
| **Collision** | Bounce off the physics world, or off planes you list. |
| **Sub Emitters** | Another particle system fires on a particle's `Birth`, `Collision`, `Death`, or on a `Manual` call |
| **Texture Sheet** | Plays a grid of frames across each particle. |
| **Trails** | Draws a ribbon behind each particle. Width and color follow the trail |
| **Light** | Gives a share of particles a point light; no shadows |

A **burst** emits a batch of particles at one moment, such as an explosion. Set its **Time**, count, **Cycles** and **Interval**.


## Drawing particles

The **Renderer** module sets how particles are drawn. **Render Mode** is `Billboard` (faces the camera), `StretchedBillboard`, `HorizontalBillboard`, `VerticalBillboard` or `Mesh`.

| Setting | Default | Effect |
| --- | --- | --- |
| **Material** | none | Empty uses the built-in particle material |
| **Blend Mode** | Alpha | `Alpha`, `Additive` or `Premultiplied` |
| **Lit** | off | Shades particles with the scene's lights and ambient |
| **Soft Particle Distance** | 0 | Fades particles near solid geometry. 0 turns it off |

The built-in particle material uses the `Particle` shader. It has two properties: `_MainTex`, the particle texture, and `_MainColor`, a tint. To change the look, make a [material](01-materials.md) on the `Particle` shader, set its texture, and assign it to **Material**.

## Control from a script

All control methods are on `ParticleSystemComponent`.

| Member | Effect |
| --- | --- |
| `Play()` | Starts the system, or resumes it when paused |
| `Stop()` | Stops new particles. Live ones play out |
| `Stop(true, ParticleStopBehavior.StopEmittingAndClear)` | Stops and removes every particle |
| `Restart()` | Clears and plays again from the start |
| `IsPlaying`, `IsEmitting`, `ParticleCount` | Current state |

Each call also reaches child systems unless you pass `false`.

## See also

- [Materials](01-materials.md)
- [Lights](03-lights.md)
- [Add a particle effect](../09-how-to/08-add-a-particle-effect.md)
