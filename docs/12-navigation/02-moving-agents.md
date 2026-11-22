---
title: Moving agents
description: Send a NavMesh Agent to a point, read its path state and tune how it moves.
---

A **NavMeshAgent** is a component that walks its GameObject across a [NavMesh](01-navmesh-basics.md). You give it a destination. It plans a path, steers along it and avoids other agents.

## Quick recipe

Add **Add Component > Navigation > NavMesh Agent** to a character. Add this script and assign **Goal** in the Inspector.

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

Press **Play**. The character walks to the goal. A baked surface for the agent's type must be in the scene.

## Agent settings

| Setting | Default | Effect |
| --- | --- | --- |
| **Agent Type** | Humanoid | Which surface the agent walks on |
| **Radius**, **Height** | 0.5, 2 | The agent's size for avoiding others |
| **Base Offset** | 0 | Height of the Transform above the NavMesh |
| **Speed** | 3.5 | Top speed, in units per second |
| **Angular Speed** | 120 | Top turn rate, in degrees per second |
| **Acceleration** | 8 | Speed gained per second |
| **Stopping Distance** | 0 | Stops this far short of the destination |
| **Auto Braking** | on | Slows down near the destination |
| **Area Mask** | Everything | The [areas](01-navmesh-basics.md#areas) it may walk on |
| **Update Position** | on | Moves the Transform each frame |
| **Update Rotation** | on | Turns the Transform to face its movement |

Set **Update Position** off if you move the object yourself.

## Setting a destination

`SetDestination(Float3 target)` requests a path. It returns `false` if the agent is not on a NavMesh or the target is off it. Before the agent reaches a NavMesh the destination is remembered and requested later.

Path planning takes a moment, so read the result over the next frames.

| Member | What it tells you |
| --- | --- |
| `PathPending` | A requested path is still being computed |
| `HasPath` | The agent is following a path |
| `PathStatus` | `PathComplete`, `PathPartial` (leads to the closest reachable point) or `PathInvalid` |
| `RemainingDistance` | Distance left along the path. Infinity with no path |
| `HasArrived` | True once it reaches the destination, until a new one is set |
| `Velocity` | Current movement, in units per second |

## Reacting to arrival

`DestinationReached` fires once when the agent arrives. Arrival counts at **Stopping Distance**, or within 0.05 units if that is smaller.

```csharp
var agent = GetComponent<NavMeshAgent>();
agent.DestinationReached += () => Debug.Log("Arrived");
agent.SetDestination(Goal.Transform.Position);
```

## Stopping and teleporting

| Member | What it does |
| --- | --- |
| `IsStopped = true` | Halts the agent and keeps its path. Set `false` to carry on |
| `ResetPath()` | Clears the path and destination |
| `Warp(Float3 position)` | Teleports the agent onto the NavMesh and keeps its destination. Returns `false` if it cannot |
| `Speed` | Change it at runtime. It takes effect at once |

A new destination while `IsStopped` is true plans the route but does not resume movement.

## See also

- [NavMesh basics](01-navmesh-basics.md)
- [Make an agent walk to a point](../09-how-to/07-make-an-agent-walk-to-a-point.md)
