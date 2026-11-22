---
title: Joints and constraints
description: Connect rigidbodies with hinges, sliders and other joints, and add wheels to a vehicle.
---

A **constraint** is a rule that limits how two rigidbodies move relative to each other. A **joint** is a ready-made bundle of constraints, such as a door hinge. Use them for doors, chains, pistons and ragdolls. Read [Rigidbodies and collisions](01-rigidbodies-and-collisions.md) first.

## Quick recipe

1. Add a **Rigidbody** to the door object.
2. Choose **Add Component > Physics > Joints > Hinge Joint** on the same object.
3. Set **Anchor** to the hinge edge in the door's local space, and **Axis** to `(0, 1, 0)`.
4. Leave **Connected Body** empty to pin the door to the world. Press **Play** and push the door.

[screenshot needed: a door object with Hinge Joint settings in the Inspector]

## Joints and constraints

Each is a component on a rigidbody, with these shared properties.

| Property | Default | Effect |
| --- | --- | --- |
| **Connected Body** | none | The other rigidbody. Empty connects to the world |
| **Enabled On Start** | on | Whether the constraint solves from the start |
| **Collide Connected** | off | Whether the two bodies still collide with each other |

Add joints from **Add Component > Physics > Joints** and constraints from **Add Component > Physics > Constraints**.

| Component | What it does |
| --- | --- |
| **Hinge Joint** | Rotation around one axis, like a door |
| **Prismatic Joint** | Sliding along one axis, like a drawer |
| **Universal Joint** | Rotation around two axes, like a drive shaft |
| **Ball Socket** | Keeps two anchor points together, free to rotate |
| **Distance Limit** | Holds or limits the distance between two anchors |
| **Fixed Angle** | Locks relative rotation |
| **Hinge Angle** | Allows rotation around one axis only |
| **Twist Angle**, **Cone Limit** | Limit twist, or tilt within a cone |
| **Point On Line**, **Point On Plane** | Keep a point on a line or a plane |
| **Linear Motor**, **Angular Motor** | Drive speed along or around an axis |
| **Drive** | Spring and damper toward a target pose |

## Limits and motors

Joints take limits and motors as plain properties.

| Joint | Limits | Motor |
| --- | --- | --- |
| **Hinge Joint** | `MinAngle`, `MaxAngle` in degrees. Default -180 to 180 | `HasMotor`, `MotorTargetVelocity`, `MotorMaxForce` (default 100) |
| **Prismatic Joint** | `MinDistance`, `MaxDistance`. Default unlimited | Same three. `Pinned` (default on) also blocks rotation |
| **Universal Joint** | None | Same three |

A **motor** pushes the joint toward a target speed, up to its maximum force. Read `CurrentAngleDegrees` on a hinge or universal joint, or `CurrentDistance` on a prismatic joint.

Joints cannot break under load. Disable one with `Active = false`.

## Example: a door that stops

```csharp
public sealed class Door : Component
{
    public override void Start()
    {
        var hinge = GetComponent<HingeJoint>();
        hinge.MinAngle = 0f;
        hinge.MaxAngle = 100f;
    }
}
```

The door now swings 100 degrees and stops.

## Example: a chain

```csharp
public sealed class ChainBuilder : Component
{
    public override void Start()
    {
        Rigidbody3D previous = GetComponent<Rigidbody3D>();
        for (int i = 1; i <= 5; i++)
        {
            GameObject link = Scene.Create("Link " + i);
            link.Transform.Position = Transform.Position + new Float3(0, -i, 0);
            var body = link.AddComponent<Rigidbody3D>();
            var socket = link.AddComponent<BallSocketConstraint>();
            socket.Anchor = new Float3(0, 0.5f, 0);
            socket.ConnectedBody = previous;
            previous = body;
        }
    }
}
```

Put it on a static or kinematic rigidbody. Each link hangs from the one above. Add a collider to each link to see it.

## Wheels

A **Wheel Collider** is a raycast-vehicle wheel. It pushes on the nearest rigidbody above it with a suspension spring and tire grip, and adds no collision shape. Add one per wheel from **Add Component > Physics > Wheel Collider**. Put each on a child of the car body, at the top of the suspension travel.

| Property | Default | Effect |
| --- | --- | --- |
| **Radius** | 0.35 | Wheel size |
| **Suspension Distance** | 0.3 | Travel of the spring |
| **Suspension Frequency** | 2 | Spring stiffness, in hertz |
| **Forward Friction**, **Sideways Friction** | 1.6, 1.8 | Tyre grip along and across the wheel |

Drive it from a script each frame.

```csharp
public sealed class Throttle : Component
{
    public WheelCollider Wheel;

    public override void Update()
    {
        Wheel.MotorTorque = 300f;
        Wheel.SteerAngle = 0.2f;
        Wheel.BrakeTorque = 0f;
    }
}
```

`MotorTorque` and `BrakeTorque` are in newton meters. `SteerAngle` is in radians. Set `VisualTransform` to a child mesh to have it follow the wheel.

## See also

- [Rigidbodies and collisions](01-rigidbodies-and-collisions.md)
- [Layers and collision](05-layers-and-collision.md)
