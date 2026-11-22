---
title: Float a boat on the ocean
description: Add an ocean to the scene and make a physics object bob on its waves.
---

You end with a sea out to the horizon and a box that rises and falls on its waves.

## Steps

1. Choose **GameObject > Empty Object** and name it Sea. Select it and choose **Add Component > Rendering > Ocean**. Its Transform's Y position is the water level.

[screenshot needed: the Scene view with the ocean and the Sea object selected]

2. Choose **GameObject > 3D Object > Cube** and name it Boat. Set its Scale to 4, 0.5, 2 and its Position to 0, 2, 0.
3. Choose **Add Component > Physics > Colliders > Box Collider**, then **Add Component > Physics > Rigidbody**.
4. Choose **Add Component > Physics > Ocean Floater**.
5. In the floater, set **Probes** to a size of 4. Enter these four points, which are the corners of the hull in its own space: `-0.5, 0, -0.5`, `0.5, 0, -0.5`, `-0.5, 0, 0.5` and `0.5, 0, 0.5`.
6. Press Play. The boat drops, settles at the surface and rides the waves.

[screenshot needed: the Boat's Ocean Floater with four probes in the Inspector]

## Tune it

| To get | Change |
| --- | --- |
| Calmer water | Lower `WindSpeed` or `WaveScale` on the Ocean |
| A boat that sits higher | Raise `Buoyancy` on the Ocean Floater |
| A boat that ignores small ripples | Raise `SpatialLength` on the Ocean Floater |

The same setup from a script, on an object that already has a Rigidbody:

```csharp
var floater = gameObject.AddComponent<OceanFloater>();
floater.Probes = [new Float3(-0.5f, 0f, -0.5f), new Float3(0.5f, 0f, 0.5f)];
```

The water is read back from the GPU a few frames late. That is fine for boats and debris.

## Learn more

- [Ocean](../03-rendering/05-ocean.md): waves, foam, currents, wakes and lakes
- [Sky, fog and clouds](../03-rendering/04-environment.md): set the sky and light the sea
