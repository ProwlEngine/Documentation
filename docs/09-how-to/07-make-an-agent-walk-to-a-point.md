---
title: Make an agent walk to a point
description: Bake a NavMesh and send a character to a goal object that finds its own way.
---

You end with a character that walks across your level to a marker object when you press **Play**, going around walls.

## Steps

1. Make sure the ground and walls have a **Mesh Renderer**.
2. Create an empty GameObject. Choose **Add Component > Navigation > NavMesh Surface**.
3. Click **Bake NavMesh** in the Inspector. Select the surface to see the walkable area.

[screenshot needed: the NavMesh overlay on a level after baking]

4. Select your character. Choose **Add Component > Navigation > NavMesh Agent**. Place it on the ground.
5. Create an empty GameObject named `Goal` and move it to where the character should go.
6. In the **Project** panel, choose **Assets > Create > C# Script**, name it `WalkTo`, and paste the code below.
7. Add **WalkTo** to the character. Drag `Goal` onto its **Goal** field.
8. Press **Play**.

```csharp
using Prowl.Runtime;

public sealed class WalkTo : Component
{
    public GameObject Goal;

    public override void Start()
    {
        if (Goal.IsValid())
            GetComponent<NavMeshAgent>().SetDestination(Goal.Transform.Position);
    }
}
```

The character walks to the goal and stops.

[screenshot needed: the character on its way to the Goal, with the NavMesh overlay visible]

## If the character does not move

- **No NavMesh.** Select the surface. If nothing is drawn, click **Bake NavMesh** again.
- **Wrong agent type.** The surface and the agent must use the same **Agent Type**. Both default to Humanoid.
- **Off the mesh.** Move the character and the goal onto the walkable area.
- **Goal not reachable.** With no gap in a wall, the agent walks to the closest point it can.

## Learn more

- [NavMesh basics](../12-navigation/01-navmesh-basics.md): surfaces, agent types, areas and obstacles
- [Moving agents](../12-navigation/02-moving-agents.md): path state, stopping and arrival
