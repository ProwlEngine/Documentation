---
title: Building your game
description: Turn a project into a standalone player that runs without the editor.
---

A **build** turns your project into a folder holding a **player**, the program that runs your game without the editor. You use it to test on a clean setup or to hand the game to someone else. The build writes your scenes, the assets they use and your compiled scripts into one output folder.

## Quick recipe

1. Save your scenes. The build saves open scenes that have changes.
2. Choose **File > Build Project...** to open the Build Project panel.
3. In **Scenes in Build**, click **Add Open** to list every open scene. The first enabled scene opens first in the player.
4. Under **Platform**, pick your target, such as Windows or Linux.
5. Click **Build & Run**. A progress window covers the editor until the build ends.
6. Find the game in `Builds/<ProjectName>/` inside the project folder.

[screenshot needed: the Build Project panel with two scenes listed and a platform card selected]

**Build & Run** launches the result when the target matches your OS. **Build** only produces the folder.

## The scene list

A scene is only in the player if it is in the list, and it must be saved as an asset before **Add Open** accepts it.

Each row has a switch, a drag grip and a remove button. Turn a row off to keep it listed but leave it out.

## Platforms

The panel shows one card per build pipeline. Prowl ships one, the desktop pipeline. An Android card is a disabled placeholder.

Selecting the desktop card shows its profile. Its **Platform** dropdown lists these targets:

| Target | Runtime identifier |
| --- | --- |
| Windows (x64) | win-x64 |
| Windows (arm64) | win-arm64 |
| Linux (x64) | linux-x64 |
| Linux (arm64) | linux-arm64 |
| macOS (Intel) | osx-x64 |
| macOS (Apple Silicon) | osx-arm64 |
| macOS (Universal) | osx-x64 and osx-arm64 |

The build publishes one architecture at a time, so macOS (Universal) fails with an explanation. Build the two macOS targets separately.

| Profile field | Default | Effect |
| --- | --- | --- |
| Self-Contained | off | Includes the .NET runtime in the output |
| Publish Trimmed | off | Removes unused code |
| Native AOT | off | Compiles to one native executable. Needs the target's toolchain, so only for your own OS |
| Width, Height | 1280, 720 | Starting window size. Minimums are 320 and 240 |

## Settings in the panel

These live in the Build Project panel, not in [Project settings](07-project-settings.md). They are saved with the project.

| Setting | Default | Meaning |
| --- | --- | --- |
| Configuration | Release | Debug or Release, passed to the .NET build |
| Output Directory | Builds | Relative to the project folder, or absolute |
| Asset Packaging | ProwlPak | How assets are stored in the output |
| Asset Export | DependenciesOnly | Which assets ship |
| Max Pak Size (MB) | 2048 | Pak split size, 256 to 4096. ProwlPak only |

The output directory must be outside `Assets` and not the project root. Each build gets its own folder named after the project. A second build becomes `<ProjectName> (1)`, so nothing is overwritten.

## What ships

With **DependenciesOnly**, the build ships each listed scene and everything it references, directly or through other assets. With **AllAssets**, it ships every asset in the project.

Two rules apply in both modes:

- Anything under a [`Resources` folder](04-assets-and-importers.md#load-an-asset-from-a-script) always ships, with its dependencies.
- The build leaves out anything under an `Editor` folder and editor-only types such as scripts. It ships them only if a shipping asset references them.

## Packaging modes

| Mode | Result |
| --- | --- |
| LooseFiles | One `.asset` file per asset. Easiest to inspect |
| ProwlPak | `.prowlpak` archives, split at Max Pak Size |
| Embedded | Assets compiled into the player assembly |

## Output and running it

A desktop build contains:

| Item | Purpose |
| --- | --- |
| `<ProjectName>` or `<ProjectName>.exe` | The player. On macOS it sits inside a `.app` bundle |
| `player.manifest` | Product name, version, scene list, packaging mode and window size |
| `Content/` | Assets, `asset_manifest.bin` and `Settings/` |
| `runtimes/` | Native libraries for the target |

Run the executable. The player reads `player.manifest` beside itself and refuses to work properly without it.

`Content/Settings` holds one YAML file per settings page the player reads, such as `PhysicsSettings.yaml` and `QualitySettings.yaml`. Product name, company and version come from **Project Settings > General** and reach the player through the manifest.

## Build from the command line

With the editor open, `prowl command build --out Builds` runs the same build and waits for it. Add `--run true` to launch the result. See [Prowl CLI](01-prowl-cli.md).

## Common failures

| Symptom | Cause and fix |
| --- | --- |
| Asset missing in the player, fine in the editor | Code loads it by path and no scene references it. Move it under a `Resources` folder, reference it from a scene, or use AllAssets |
| "No scenes in build" | Enable or add a scene |
| Build stops on a native plugin | Set its CPU to match the target, or to AnyCPU |
| Native AOT refused | Build on the target OS, or turn Native AOT off |

## See also

- [Prowl CLI](01-prowl-cli.md)
- [Assets and importers](04-assets-and-importers.md)
- [Project settings](07-project-settings.md)
