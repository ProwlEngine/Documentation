---
title: Layers and collision
description: Choose which objects collide with the layer collision matrix, ignore single pairs, and set gravity.
---

A **layer** is a number from 0 to 31 on every GameObject. The **collision matrix** is a grid that says which pairs of layers collide. Use them to stop bullets hitting the player, or to keep debris from hitting other debris.

## Quick recipe

Make the layers `Player` and `Bullet` ignore each other.

1. Open **Edit > Project Settings...** and select **Tags & Layers**.
2. Type `Player` and `Bullet` into two empty layer slots.
3. Select each object and set **Layer** in the **Inspector**.
4. Open **Physics** in Project Settings. Under **Layer Collision Matrix**, untick the cell where Player meets Bullet.

[screenshot needed: the Layer Collision Matrix with one cell unticked]

## The collision matrix

Every pair of layers collides by default. A ticked cell means the two layers collide. Layers without a name are hidden from the grid.

The matrix is symmetric: Player against Bullet is the same cell as Bullet against Player. It is **project wide**, so every scene shares it. Set it from code with `CollisionMatrix`.

```csharp
int player = LayerMask.NameToLayer("Player");
int bullet = LayerMask.NameToLayer("Bullet");

CollisionMatrix.SetLayerCollision(player, bullet, false);
bool hits = CollisionMatrix.GetLayerCollision(player, bullet);
```

`SetLayerCollisions(layer, false)` clears one layer against all others. `Reset()` makes everything collide again.

## Ignore one pair of bodies

To stop two specific rigidbodies colliding, regardless of layers, call `Physics.IgnoreCollisionBetween`.

```csharp
Physics.IgnoreCollisionBetween(rider, horse);
```

This works on top of the matrix and only affects the current world. Undo it with `Physics.EnableCollisionBetween(a, b)`, or clear every pair with `Physics.ClearIgnoredCollisions()`.

## Gravity

Gravity is the acceleration applied to every body with **Affected By Gravity** on. The default is `(0, -9.81, 0)`. Set it in **Project Settings > Physics > Gravity**, or at run time.

```csharp
Physics.Gravity = new Float3(0, -3.7f, 0);
```

A non-finite value is rejected with an error in the log.

## Layers in queries

A `LayerMask` picks which layers a raycast or overlap sees. It is separate from the matrix, which only affects bodies colliding.

```csharp
var mask = LayerMask.FromMask(1u << LayerMask.NameToLayer("Enemy"));
Physics.Raycast(origin, direction, 50f, out RaycastHit hit, mask);
```

`LayerMask.Everything` is the default. See [Raycasts and queries](03-raycasts-and-queries.md) for the full set of queries and filters.

## See also

- [Rigidbodies and collisions](01-rigidbodies-and-collisions.md)
- [Raycasts and queries](03-raycasts-and-queries.md)
- [Joints and constraints](04-joints-and-constraints.md)
