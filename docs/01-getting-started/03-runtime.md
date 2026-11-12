---
title: Getting started with the runtime
description: A game built entirely in code with Prowl.Runtime, with no editor involved.
---

Prowl.Runtime works on its own. If you would rather build a game in code, or embed Prowl in another app, reference it from a plain .NET project and drive everything from C#. Every sample in `Samples/Runtime` is written this way.

## Set up the project

Create a console project targeting .NET 10, and reference `Prowl.Runtime` from your clone of the Prowl repository, as the samples do:

```bash
dotnet new console -n MyGame
```

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\Prowl\Prowl.Runtime\Prowl.Runtime.csproj" />
  </ItemGroup>
</Project>
```

`Prowl.Runtime` builds with the same Anthology setting as the editor. Use a [local Anthology](01-installation.md#build-from-source) for the most up to date libraries.

## The game class

```csharp
using Prowl.Runtime;
using Prowl.Runtime.Rendering;
using Prowl.Runtime.Resources;
using Prowl.Vector;

new HelloGame().Run("Hello Prowl", 1280, 720);

public sealed class HelloGame : Game
{
    public override void Initialize()
    {
        // The game world, made running and presented before Initialize.
        SceneInstance world = SceneInstance.Main;

        // A light, angled down like an afternoon sun.
        var sun = new GameObject("Sun");
        sun.AddComponent<DirectionalLight>();
        sun.Transform.LocalEulerAngles = new Float3(50f, 30f, 0f);
        sun.MoveTo(world);

        // The camera. Camera.Main is the enabled camera with the highest Depth that draws to the screen.
        var cameraObject = new GameObject("Main Camera");
        var camera = cameraObject.AddComponent<Camera>();
        camera.Profile = VolumeProfile.CreateCameraDefault("Main Camera Profile");   // tonemapping
        cameraObject.Transform.Position = new Float3(0f, 3f, -8f);
        cameraObject.Transform.LookAt(new Float3(0f, 1f, 0f));
        cameraObject.MoveTo(world);

        // A spinning cube with our own component on it.
        var cube = new GameObject("Spinning Cube");
        cube.AddComponent<MeshRenderer>().Mesh = Mesh.CreateCube(Float3.One);
        cube.AddComponent<Spinner>();
        cube.Transform.Position = new Float3(0f, 1.5f, 0f);
        cube.MoveTo(world);
    }
}
```

`new GameObject` makes a detached object. Each one is set up first and then moved into the world with `MoveTo`, so its components start with their final settings. `world.Create("Name")` makes an object straight in the world instead.

The game binds a world as `SceneInstance.Main` before `Initialize` runs, and levels load into it. Override `CreateMainWorld` to set that world up differently. See [Scenes and worlds](../02-scripting/05-scenes-and-worlds.md).

## The component

```csharp
public sealed class Spinner : Component
{
    public float DegreesPerSecond = 90f;

    public override void Update()
    {
        Transform.Rotate(new Float3(0f, DegreesPerSecond * Time.DeltaTime, 0f));
    }
}
```

## Next steps

- Add physics with a [Rigidbody3D and a collider](../06-physics/01-rigidbodies-and-collisions.md).
- Read the samples in `Samples/Runtime` for lights, physics, vehicles, particles and VR, all in code.
- Give the camera post processing in [Cameras and post processing](../03-rendering/02-cameras-and-post-processing.md).
