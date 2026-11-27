---
title: Playing sounds
description: Import audio clips, play them with an AudioSource, and place them in 3D space.
---

An **AudioClip** is an imported sound file. An **AudioSource** is a component that plays a clip from its object's position. An **AudioListener** is the point in the scene where sound is heard, normally the camera. You use them for music and sound effects.

## Quick recipe

Add this component, assign a clip in the **Inspector**, and press **Play**.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class Beeper : Component
{
    public AudioClip Clip;

    public override void Start() => GetComponent<AudioSource>().PlayOneShot(Clip);
}
```

Put it on an object with an **Audio Source**. The clip plays once at start. [Play a sound](../09-how-to/04-play-a-sound.md) has the click steps.

## Importing clips

Copy a `.wav`, `.mp3`, `.ogg` or `.flac` file into your `Assets` folder. The editor imports it as an AudioClip. Select it to see its format, a waveform and a play button.

Change the import settings in the **Inspector**, then click **Apply**.

| Setting | Effect |
| --- | --- |
| **Load Type** | `CompressedInMemory` keeps the file encoded and decodes while playing. `DecompressOnLoad` stores raw audio |
| **Force Mono** | Mixes the clip down to one channel |
| **Sample Rate Override** | Resamples the clip. 0 keeps the file's own rate |

Force Mono or a rate override stores the clip uncompressed.

## The Audio Source

Add one with **GameObject > Audio > Audio Source**, or **Add Component**. These are its main properties.

| Property | Default | Effect |
| --- | --- | --- |
| **Clip** | none | The clip `Play()` plays |
| **Play On Start** | off | Plays when the component is enabled |
| **Loop** | off | Restarts the clip when it ends |
| **Volume** | 1 | 1 is the clip as authored, 0 is silent, above 1 amplifies |
| **Pitch** | 1 | Playback speed. The lowest value is 0.01 |
| **Pan** | 0 | -1 is fully left, 1 is fully right |
| **Output Group** | none | A mixer group to route into. See [Mixing and effects](02-mixing-and-effects.md) |

## 2D and 3D sound

**Spatial** is on by default, so the source is a 3D sound. It gets quieter as you move away from it and pans left or right with its direction. Turn **Spatial** off for a 2D sound such as music or a menu click. A 2D sound plays at the same level everywhere.

A 3D sound is heard from the **AudioListener**. Add one with **GameObject > Audio > Audio Listener** and put it on the camera object.

| Property | Default | Effect |
| --- | --- | --- |
| **Min Distance** | 1 | Inside this distance the sound is at full volume |
| **Max Distance** | 10 | At this distance the sound is at its quietest |
| **Attenuation Model** | Linear | The falloff curve: `None`, `Inverse`, `Linear` or `Exponential` |

Keep one enabled listener. A second logs a warning and which one is heard is arbitrary.

[screenshot needed: an Audio Source in the Inspector with Spatial, Min Distance and Max Distance visible]

## Playing from a script

Assign `Clip` and call `Play()`, or play any clip with `PlayOneShot`. Here `Music` and `Step` are `AudioClip` fields.

```csharp
var source = GetComponent<AudioSource>();
source.Clip = Music;
source.Loop = true;
source.Play();

source.PlayOneShot(Step, 0.5f);
```

| Member | What it does |
| --- | --- |
| `Play()` | Plays `Clip` from the start |
| `Pause()` and `Resume()` | Stop and continue from the same position |
| `Stop()` | Stops and rewinds |
| `PlayOneShot(clip, volumeScale)` | Plays a clip alongside `Clip` without cutting it off |

Assigning a different `Clip` stops what is playing. A one shot uses the source's volume, pitch and spatial settings.

## Playing at a point

`AudioSource.PlayClipAtPoint` plays a clip at a world position and cleans up after itself. Use it for sounds whose object is destroyed at the same moment, such as an explosion or a pickup.

```csharp
AudioSource.PlayClipAtPoint(Boom, Transform.Position, 0.8f);
```

It creates a temporary 3D source in the active scene and destroys it when the clip ends. It returns null when no audio device is running.

## Project audio settings

**Edit > Project Settings > Audio** sets **Global Volume** (0 to 1). It also sets the device **Sample Rate**, **Channels** and **Buffer Size**.

## See also

- [Mixing and effects](02-mixing-and-effects.md)
- [Play a sound](../09-how-to/04-play-a-sound.md)
