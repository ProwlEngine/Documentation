---
title: Graph basics
description: What an animation graph is, and how states, transitions and Enter and Exit gates work.
---

An **animation graph** decides which animation a character plays and when it changes. It is a set of **states**, such as Idle, Jump and Land, that each play a **pose**: the position of every bone at one moment. A **transition** is a move from one state to another, with a short blend between the two poses.

Quick start:

- [Play an animation on a loop](../09-how-to/01-play-an-animation-on-a-loop.md) or [switch between two animations](../09-how-to/02-switch-between-two-animations.md) with no graph.
- [Make a character walk and run with a graph](../09-how-to/40-make-a-character-walk-and-run-with-a-graph.md).
- [Add a hit reaction with an Any State transition](../09-how-to/41-add-a-hit-reaction-with-an-any-state-transition.md).

## Example: idle, jump and land

![The idle, jump and land state machine](images/jump-graph.png)

![The character jumping and landing](images/jump-land.gif)

A character idles, jumps when you press Space, lands, then returns to idle. The graph has three states: **Idle** (the default), **Jump** and **Land**.

A **parameter** is a named value your script sets on the Animator and the graph reads. This graph uses two Flag (true or false) parameters. `Grounded` is plain. `Jump` is marked **Trigger**, so it turns itself off once a transition fires on it.

Each state also has an **Enter** and an **Exit** gate, explained in [The gate rule](#the-gate-rule). **State Done** is covered in [Finishing states](#finishing-states).

| State | Pose | Enter | Exit |
| --- | --- | --- | --- |
| Idle | Clip: idle, looping | Parameter `Grounded` | open |
| Jump | Clip: jump, `Once` | Parameter `Jump` | Logic Not of `Grounded` |
| Land | Clip: land, `Once` | Parameter `Grounded` | State Done |

Transitions: Idle to Jump (0.1 s), Jump to Land (0.05 s), Land to Idle (0.2 s).

```csharp
using Prowl.Runtime;

public sealed class JumpAnimation : Component
{
    public Animator Animator;
    private CharacterController _controller;

    public override void OnEnable() => _controller = GetComponent<CharacterController>();

    public override void Update()
    {
        Animator.SetBool("Grounded", _controller.IsGrounded);
        if (_controller.IsGrounded && Input.GetKeyDown(KeyCode.Space))
            Animator.SetTrigger("Jump");
    }
}
```

![The root state machine](images/the-root-state-machine.png)

## Creating a graph

![The animation graph editor: state machine, parameters panel and minimap](images/graph-editor-overview.png)

Create an **Animation Graph** from the **Project** panel's **Create** menu, then assign it to an Animator's **Graph** field. Double-click it to open the graph editor:

- The canvas shows the root of the graph, usually a state machine.
- The **Parameters** panel on the right lists the values your scripts set.
- Double-click a state to open the small graph inside it. The breadcrumb at the top takes you back.

## Nodes and pins

A graph is made of nodes. Nodes connect through **pins**, and each pin carries one kind of value:

| Pin kind | Carries |
| --- | --- |
| **Pose** | A full skeleton pose |
| **Number** | A float |
| **Flag** | A bool |
| **Integer** | An int |
| **Vector** | A 3D vector |
| **Target** | A point or bone to reach for, used by IK |
| **Mask** | Per-bone weights |
| **Id** | A name |

> [!WARNING]
> **An unwired required Number pin reads 0**, not the value shown in the editor. Feed constants with a **Number** node.

The first pose node you add to the graph becomes its **root**, the pose the Animator shows.

![Pins of each kind in the graph editor, showing their colours](images/pin-colours.png)

## State machines

A **State Machine** node holds states and the transitions between them. Each state is its own small graph, ending in a **State Output** node with three pins:

| Pin | Meaning |
| --- | --- |
| **Pose** | What the state plays |
| **Enter** | Whether the state *wants to be entered* |
| **Exit** | Whether the state *is willing to be left* |

### The gate rule

![Inside a state: a condition wired into the State Output Enter pin](images/state-output-gates.png)

**A transition from A to B fires only when A's Exit is true and B's Enter is true.**

A new state starts with Enter closed and Exit open, so nothing transitions into it until you wire Enter.

- Wire a condition into Enter to make entry conditional, or open it permanently.
- Wire a condition into Exit to keep a state playing until something is done, such as a one-shot attack.

Each condition lives in one place. "Jump when the Jump trigger fires" sits on Jump's Enter, however many states lead to Jump.

### Default state and Any State

- The **default** state is where the machine starts.
- The **Any State** transitions to its targets from every other state, ignoring the source's Exit. It still respects the target's Enter. Use it for interrupts like hit reactions and death.

### Transitions

![A transition selected, with its duration, easing and timing settings](images/transition-settings.png)

| Setting | Meaning |
| --- | --- |
| **Duration (s)** | Blend time in seconds (default 0.2) |
| **Easing** | `Linear`, `EaseIn`, `EaseOut`, `EaseInOut` |
| **Timing: Start Fresh** | The target starts from its beginning |
| **Timing: Match Time** | The target starts at the source's sync position |
| **Timing: Synchronized** | Phase stays locked to the source, using foot sync |
| **Fit Remaining Time** | The blend may not outlast what is left of the source |
| **Can Interrupt** | May cut in while the target is still blending in from elsewhere |

Use **Synchronized** timing between walk and run so the feet stay in step.

### Finishing states

- **State Done** is true once the state has played through (`Threshold` 0.99 of its progress), or after a number of seconds. Wire it into **Exit** for one-shot states, and set the clip's **Looping** to `Once`.
- **State Query** reads how long the machine has been in its state, or how far through it is.

## Sub-graphs

- A **Sub Graph** node runs another graph as one node. A graph asset's parameters become its inputs.
- A state can play a graph asset instead of its own nodes, which keeps big machines readable.
- A **Graph Slot** is a named hole the game fills at runtime with `animator.SetGraphSlot("Weapon", rifleGraph)`, falling back to its input.

To build graphs from the terminal, see the [Prowl CLI](../07-editor/01-prowl-cli.md).
