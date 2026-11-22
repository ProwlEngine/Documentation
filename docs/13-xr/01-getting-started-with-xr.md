---
title: Getting started with XR
description: What XR support Prowl has, what it needs, and how to see your scene in a headset.
---

XR means virtual reality headsets and their controllers. Prowl supports them through **OpenXR**, the standard interface headset makers use. An OpenXR **runtime** is the headset's own software, such as SteamVR or the Meta app. Prowl connects to the active runtime and draws your scene into the headset.

## Requirements

- A headset and an OpenXR runtime that supports Vulkan, such as SteamVR or the Meta app.
- The engine's OpenXR loader library. The repository bundles `openxr_loader.dll` for Windows (`win-x64` and `win-x86`) only. No loader is bundled for Linux, macOS or Android, so XR on those systems is not documented yet.
- In the editor, start it with `--xr` and the headset connected. This makes the graphics device for the headset when the editor starts.

XR cannot run headless, because it needs a window and a graphics device.

## Quick recipe

1. Start the editor with `--xr`, with the headset connected and its runtime running.
2. Open **Edit > Project Settings...**, select **XR** and turn on **Start In Play Mode**.
3. Create an empty object named `Rig`. This stands for the play area.
4. Create a child of `Rig` with a **Camera** and add **XR > Tracked Pose Driver** to it. Leave **Node** on `Head`.
5. Press **Play**.

The headset shows the scene from the camera, and the camera follows your head. The Game view shows one eye.

[screenshot needed: the Rig hierarchy with the camera's Tracked Pose Driver in the Inspector]

The first perspective camera with no target texture draws both eyes. A camera's **StereoTargetEye** property is `Both` by default.

## XR project settings

Open **Edit > Project Settings...** and select **XR**. These settings are `XRSettings`.

| Setting | Default | Effect |
| --- | --- | --- |
| **Start In Play Mode** | off | Starts XR when you press Play |
| **Start In Player** | off | Starts XR when a built game launches |
| **Tracking Origin** | Floor | Where poses are measured from. `Seated` uses the head's start position |
| **Render Scale** | 1 | Scales each eye's resolution, 0.25 to 2. Applies the next time XR starts |

To start XR from a script instead, call `XR.Start()`. It returns false and logs the reason when it cannot connect. In your own game, set `XR.InitializeOnStartup = true` before the game runs, as the `VRBasics` sample does.

## Poses

A **pose** is a position and rotation, measured from the tracking origin. `XR.GetPose(node)` returns an `XRPose` for an `XRNode`.

| Node | Tracks |
| --- | --- |
| `Head` | The headset |
| `LeftHand`, `RightHand` | Where the hand holds the controller |
| `LeftHandAim`, `RightHandAim` | The controller's pointing ray |
| `EyeGaze` | Where the eyes look, on headsets with eye tracking |

Check `HasPosition`, `HasRotation` or `IsValid` before you use a pose. `XR.IsEyeTrackingSupported` and `XR.IsHandTrackingSupported` say what the headset offers.

The **Tracked Pose Driver** component moves its object to a node's pose, relative to its parent. Give each hand object one with `Node` set to a hand.

## Controller input

`XRInput` reads controllers, with an `XRHand` of `Left` or `Right`.

```csharp
float squeeze = XRInput.GetGrip(XRHand.Right);
Float2 stick = XRInput.GetThumbstick(XRHand.Left);
if (XRInput.GetButtonDown(XRHand.Right, XRButton.Primary))
    XRInput.Vibrate(XRHand.Right, 0.5f, 0.1f);
```

Buttons are `Trigger`, `Grip`, `Primary`, `Secondary`, `Menu` and `Thumbstick`. `XRInput` also reads touch sensors, finger joints and pinch for bare hands.

## Eye shaders

The engine has two built-in shaders for XR, `Hidden/XR/Eyes` and `Hidden/XR/Mirror`. They are internal. The engine uses them to submit the eye images to the headset and to show one eye in the window. You do not assign them.

## See also

- [Input and time](../02-scripting/03-input-and-time.md)
- The `VRBasics` and `VRShowcase` samples in the engine repository
