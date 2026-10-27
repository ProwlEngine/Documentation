---
title: Character controller
description: Moving a player with CharacterController, including gravity and jumping.
---

## The basics

![The FpsMover walking up stairs and jumping](images/fps-mover.gif)

- The pivot is at the **feet**; `Height` and `Radius` extend up from there.
- `Move(displacement)` takes a distance for this frame, not a velocity.
- It applies **no gravity**. Apply gravity yourself.
- Use `Teleport(position)` to place it. Setting the Transform directly is not a move.

## A first-person mover

```csharp
using System;
using Prowl.Runtime;
using Prowl.Vector;

[RequireComponent(typeof(CharacterController))]
public sealed class FpsMover : Component
{
    public float Speed = 5f;
    public float JumpHeight = 1.2f;
    public float Gravity = 20f;

    private CharacterController _controller;
    private Float3 _velocity;

    public override void OnEnable() => _controller = GetComponent<CharacterController>();

    public override void Update()
    {
        float dt = Time.DeltaTime;
        Float2 input = Input.GetWASD();
        Float3 wish = (Transform.Forward * input.Y + Transform.Right * input.X) * Speed;

        float rising = _velocity.Y;
        if (_controller.IsGrounded && rising <= 0f) rising = -2f;
        else rising -= Gravity * dt;
        if (_controller.IsGrounded && Input.GetKeyDown(KeyCode.Space))
            rising = MathF.Sqrt(2f * Gravity * JumpHeight);

        _velocity = new Float3(wish.X, rising, wish.Z);
        _controller.Move(_velocity * dt);
    }
}
```

## Things to know

- It never pushes rigidbodies, and it has no physics body, so raycasts do not hit it. Add a collider and a kinematic `Rigidbody3D` on the same GameObject to make it shootable.
- It gets no `OnCollisionBegin`. After `Move`, read `controller.Hits` and `controller.Collisions`.
