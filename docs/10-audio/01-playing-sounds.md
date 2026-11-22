---
title: Playing sounds
description: Import audio clips, play them with an AudioSource, and place them in 3D space.
---

An **AudioClip** is an imported sound file. An **AudioSource** is a component that plays a clip from its object's position. An **AudioListener** is the point in the scene where sound is heard, normally the camera.

For click-by-click steps, see [Play a sound](../09-how-to/04-play-a-sound.md).

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

Put it on an object that has an **Audio Source**. The clip plays once when the game starts.

## Importing clips

Copy a `.wav`, `.mp3`, `.ogg` or `.flac` file into your `Assets` folder. The editor imports it as an AudioClip. Select it to see its format, a waveform and a play button.

The import settings are in the **Inspector**. Click **Apply** after a change.

| Setting | Effect |
| --- | --- |
| **Load Type** | `CompressedInMemory` keeps the file encoded and decodes while playing. `DecompressOnLoad` stores raw audio |
| **Force Mono** | Mixes the clip down to one channel |
| **Sample Rate Override** | Resamples the clip. 0 keeps the file's own rate |

Force Mono or a sample rate override stores the clip uncompressed, as 16 bit WAVE data.
