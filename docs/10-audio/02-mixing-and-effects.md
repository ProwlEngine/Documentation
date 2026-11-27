---
title: Mixing and effects
description: Group sounds into mixer buses, change levels together, and add effects such as reverb.
---

An **audio mixer** is an asset that holds a tree of **groups**, also called buses. A source routes into a group, and the group sets the level of everything routed into it. Use a mixer to control music, effects and voices separately.

## Quick recipe

1. In the **Project** panel, choose **Assets > Create > Audio Mixer**. Name it and press Enter.
2. Select the mixer. In the **Inspector**, click **Add Group**. Select the new group and set its name, such as `Music`.
3. Select an object with an **Audio Source**. Set **Output Group** to the new group.
4. Press **Play** and move the group's fader. The level changes while the sound plays.

[screenshot needed: the Audio Mixer inspector with a Master strip, a Music strip and the faders]

A new mixer starts with a **Master** group. Every other group feeds Master or another group, so a volume set on a parent scales its children. An empty **Output Group** on a source goes straight to the output.

## Groups

Each group strip has these controls.

| Control | Effect |
| --- | --- |
| Fader | Level from -80 dB (silent) to +20 dB. 0 leaves audio unchanged |
| **M** | Mutes the group and everything feeding it |
| **S** | Solos the group. Every other group is silenced |
| Output dropdown | Picks the group this one feeds |
| Meter | Shows the level the group outputs |

## Effects

An **effect** processes audio before it is heard. Effects run in list order, and each one has its own settings. Add them to a group, which affects everything routed into it, or to one Audio Source. For a group, select it under the console in the mixer's **Inspector**.

| Effect | What it does |
| --- | --- |
| `ReverbEffect` | Adds the sound of a room. Settings include `RoomSize`, `Damping`, `Wet` and `Dry` |
| `DelayEffect` | Repeats the sound. Settings include `DelayInSeconds`, `Decay` and `Mix` |
| `FilterEffect` | Cuts or boosts frequencies. `Type` picks lowpass, highpass, bandpass, shelf, peak or notch |
| `PhaserEffect` | A sweeping, swirling sound |
| `DistortionEffect` | Adds grit |

Every effect has a **Bypass** setting that skips it without removing it. An effect instance can belong to only one chain.

From a script, add an effect with `AddEffect` on either the Audio Source or the group:

```csharp
using Prowl.Runtime.Audio.Effects;

source.AddEffect(new ReverbEffect { RoomSize = 0.8f });
```

## Snapshots

A **snapshot** records every level, mute and effect setting in a mixer. Moving to a snapshot changes the whole mix at once. Use one for a pause menu or an underwater scene.

1. Set the mixer to how you want the mix to sound.
2. In the mixer's **Snapshots** row, click **Capture**.
3. To change a snapshot later, select it, set the mix, and click **Recapture**.

Switch snapshots from a script. The mixer must be a field on your component.

```csharp
using Prowl.Runtime.Audio;

public AudioMixer Mixer;

public void OpenPauseMenu() => Mixer.TransitionTo("Paused", 0.5f);
```

`TransitionTo(name, seconds)` eases to the snapshot. `ApplySnapshot` jumps to it at once. To set one level by hand, use `Mixer.FindGroup("Music").VolumeDB = -12f`.

## See also

- [Playing sounds](01-playing-sounds.md)
