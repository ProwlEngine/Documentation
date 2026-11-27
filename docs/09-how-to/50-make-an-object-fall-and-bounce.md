---
title: Make an object fall and bounce
description: Drop a sphere onto a floor and make it bounce, with no code.
---

You end with a sphere that falls onto a floor and bounces when you press Play. It needs two objects and two physics components.

## Steps

1. Choose **GameObject > 3D Object > Plane** for the floor.
2. Select the plane. In the **Inspector**, click **Add Component** and choose **Box Collider**. The collider gives the floor a solid shape.
3. Choose **GameObject > 3D Object > Sphere**. Move it a few units above the floor with the gizmo.
4. Select the sphere. Click **Add Component** and choose **Sphere Collider**.
5. Click **Add Component** again and choose **Rigidbody**. The rigidbody makes physics move the sphere.
6. In the **Rigidbody** component, raise **Restitution** to about 0.8. Restitution is how much speed the object keeps after a hit, from 0 to 1.
7. Press **F5**. The sphere falls and bounces. Press **F5** again to stop.

[screenshot needed: the sphere's Inspector with Sphere Collider and Rigidbody, Restitution set]

## If it does not bounce

- **It falls through the floor.** The plane needs a **Box Collider**, sized to cover it.
- **It lands and stays.** **Restitution** defaults to 0. Raise it.
- **It never falls.** Check the Rigidbody's **MotionType** is **Dynamic** and gravity is on.

## Learn more

- [Rigidbodies and collisions](../06-physics/01-rigidbodies-and-collisions.md): motion types, forces and callbacks
- [Getting started with the editor](../01-getting-started/02-editor.md): the same falling cube, with a script
