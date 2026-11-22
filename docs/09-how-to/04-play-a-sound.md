---
title: Play a sound
description: Import an audio file and hear it play from an object in your scene.
---

You end with a sound that plays when you press **Play** in the editor. This works for any WAV, MP3, OGG or FLAC file.

## Steps

1. Copy the audio file into your project's `Assets` folder, or drag it into the **Project** panel. The editor imports it as an AudioClip.

[screenshot needed: the audio file selected in the Project panel with its waveform in the Inspector]

2. Choose **GameObject > Audio > Audio Listener**. This is the point where sound is heard. Move it to where your camera is.
3. Choose **GameObject > Audio > Audio Source**.
4. Select the Audio Source. Drag your file from the **Project** panel onto **Clip**.
5. Turn on **Play On Start**. Turn on **Loop** if the sound should repeat.
6. Select the Audio Source object and move it near the listener. A 3D sound is quiet beyond **Max Distance**, which is 10 by default.
7. Press **Play** in the editor toolbar. The sound starts.

[screenshot needed: the Audio Source in the Inspector with Clip and Play On Start set]

To make the sound the same volume everywhere, such as music, turn off **Spatial** on the Audio Source.

## If you hear nothing

- **The clip field is empty.** Check that **Clip** shows your file.
- **The sound is too quiet.** Move the object closer, or raise **Volume**. Check **Edit > Project Settings > Audio** for **Global Volume**.
- **No device.** The Console logs a warning when no audio device is available.

## Play it from a script instead

Use this to play a sound at a moment you choose, such as a key press. Add the component to the Audio Source object and assign **Clip** in the Inspector.

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Resources;

public sealed class Beeper : Component
{
    public AudioClip Clip;

    public override void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
            GetComponent<AudioSource>().PlayOneShot(Clip);
    }
}
```

Press **Space** while the game runs and the sound plays. Presses can overlap.

## Learn more

- [Playing sounds](../10-audio/01-playing-sounds.md): clip import, 3D sound and `PlayClipAtPoint`
- [Mixing and effects](../10-audio/02-mixing-and-effects.md)
