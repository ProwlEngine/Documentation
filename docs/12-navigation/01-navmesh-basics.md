---
title: NavMesh basics
description: Bake a NavMesh from your level, choose agent types and areas, and add links, obstacles and modifiers.
---

A **NavMesh** is a map of the ground that agents can walk on, built from your level's geometry. A **NavMeshSurface** is the component that bakes it. **Baking** means scanning the level once and saving the result.

Agents walk on it: see [Moving agents](02-moving-agents.md).

## Quick recipe

1. Make sure your ground and walls have a **Mesh Renderer**.
2. Create an empty GameObject. Choose **Add Component > Navigation > NavMesh Surface**.
3. Click **Bake NavMesh** in the Inspector.

The editor saves a `.navmesh` asset in a `<SceneName>_navmesh` folder beside your scene. Select the surface to see the walkable area drawn over your level.

[screenshot needed: the NavMesh overlay on a level, and the surface Inspector]

## The NavMesh Surface

A surface bakes one NavMesh for one agent type. These are its settings.

| Setting | Default | Effect |
| --- | --- | --- |
| **Agent Type** | Humanoid | Whose size and slope limits the bake uses |
| **Collect Objects** | All | `All` uses every active object. `Volume` uses objects inside a box. `Children` uses this object and its children |
| **Use Geometry** | Render Meshes | `Render Meshes` bakes what you see. `Physics Colliders` bakes what physics hits |
| **NavMesh Data** | none | The baked asset. Baking fills it in |
| **Default Area** | Walkable | The [area](#areas) of all baked ground, under **Advanced** |

With `Volume`, **Center** and **Size** set the box. Agents never contribute to a bake. Use one surface per agent type in a scene.

## Baking

**Bake NavMesh** runs in the background and saves the `.navmesh` asset. **Clear** removes it.

> [!NOTE]
> Changing the level does not rebake it. Click **Bake NavMesh** again after you move walls or ground.

## Agent types

An **agent type** describes the size of a walker. A tall agent never gets a path through a low tunnel. Edit the table in **Edit > Project Settings > Navigation**, on the **Agents** tab.

| Field | Humanoid default | Meaning |
| --- | --- | --- |
| **Radius** | 0.5 | Keeps the mesh this far from walls |
| **Height** | 2 | Space needed overhead |
| **Slope** | 45 | Steepest slope, in degrees |
| **Climb** | 0.4 | Tallest step it can climb |

**Add Agent Type** adds a row. **Humanoid** is built in. A surface and an agent each pick a type.

## Areas

An **area** labels a kind of ground, such as road or water. A higher **cost** makes agents avoid it. Edit them on the **Areas** tab.

Three areas are built in: **Walkable** (cost 1), **Not Walkable**, and **Jump** (cost 2, used by [links](#links)).

**Add Area** adds a named area, up to 32 in all. Costs below 1 become 1. An agent's **Area Mask** lists the areas it may use.

## Modifiers

A **NavMesh Modifier** changes how one object takes part in a bake. Find it under **Add Component > Navigation**.

| Setting | Default | Effect |
| --- | --- | --- |
| **Ignore From Build** | off | Leaves this object out of the bake |
| **Override Area** | off | Gives this object's ground the chosen **Area** |
| **Apply To Children** | on | Covers child objects too. A child's own modifier wins |

A **NavMesh Modifier Volume** stamps an **Area** on all ground inside a box. It never creates ground. **Not Walkable** cuts a hole.

Rebake after you change a modifier or volume.

## Links

A **NavMesh Link** joins two points that are not connected by ground, such as a ledge and the floor below. Agents cross it as part of their path.

| Setting | Default | Effect |
| --- | --- | --- |
| **Start Point**, **End Point** | Z of -2.5 and 2.5 | The two ends, local to the object |
| **Bidirectional** | on | Agents can cross both ways |
| **Area** | Jump | Sets the cost. Agents whose mask excludes it skip the link |

Put both ends near ground.

## Obstacles

A **NavMesh Obstacle** blocks agents without a rebake, such as a crate or a placed building.

| Setting | Default | Effect |
| --- | --- | --- |
| **Shape** | Box | `Box`, or `Cylinder` with **Radius** and **Height** |
| **Carve** | on | Cuts a hole so paths go around it |

With **Carve** off, agents only steer around the obstacle up close. Paths still lead through it.

## See also

- [Moving agents](02-moving-agents.md)
- [Make an agent walk to a point](../09-how-to/07-make-an-agent-walk-to-a-point.md)
