---
title: Rigidbodies and collisions
description: Motion types, forces, collision callbacks and trigger volumes.
---

## Rigidbody3D

![A stack of rigidbodies toppling](images/rigidbody-stack.gif)

- `MotionType` is `Dynamic`, `Kinematic` or `Static` (namespace `Jitter2.Dynamics`).
- `LinearVelocity`, `AngularVelocity`, `Mass`, `AffectedByGravity`.
- `AddForce(force, ForceMode)`, `ApplyImpulse(impulse)`, `MovePosition`, `MoveRotation`.
- A collider with no `Rigidbody3D` on it or a parent is static. Interpolation is on by default.

> [!WARNING]
> `LinearDamping` and `AngularDamping` remove that fraction of velocity every physics step, so they are strong. At 60 steps a second, 0.1 leaves under 1 percent of the speed after one second. The defaults are 0.002 and 0.005. This may change in the future.

## Colliders

Box, sphere, capsule, cylinder, cone, convex or concave mesh, and terrain.

## Collision callbacks

`OnCollisionBegin`, `OnCollisionStay` and `OnCollisionEnd(Collision collision)` fire on both objects. `collision.GameObject` is the other object, and `collision.Normal` points toward this one.

## Triggers


![A TriggerVolume with its bounds shown in the scene view](images/trigger-volume.png)

Colliders have no trigger flag. Add a `TriggerVolume` component instead:

```csharp
[RequireComponent(typeof(TriggerVolume))]
public sealed class Checkpoint : Component
{
    public override void OnTriggerEnter(Rigidbody3D other)
    {
        Debug.Log($"{other.GameObject.Name} reached the checkpoint");
    }
}
```

Character controllers entering a trigger raise `OnCharacterEnter/Stay/Exit` instead.
