---
title: Things to know first
description: The rules of Prowl's scripting, scenes, physics and rendering that catch new developers out most often.
---

A few of Prowl's rules are easy to miss and cause confusing bugs. Learn these first.

![The Prowl editor layout: scene, hierarchy, inspector, project and console](images/editor-layout.png)

## Components

- Scripts derive from **`Component`**.
- Lifecycle methods are **overrides**: `public override void Update()`. A method with the right name but no `override` is never called.
- Set up in **`OnEnable`** or **`Start`**, and clean up in **`OnDispose`**. See the full [lifecycle](../02-scripting/01-components.md#lifecycle).
- **No constructors.** Components are created before they are attached and before saved values are applied.

## Checking objects

A destroyed engine object is still a live C# reference, so ordinary null checks miss it. Prowl's analyzers make them compile errors on engine objects:

- `== null`, `!= null`, `is null` and `is not null`
- `?.` and `?[]`
- `??` and `??=`

Use `obj.IsValid()` and `obj.IsNotValid()` instead. For a true reference-null check, use `object.ReferenceEquals(obj, null)`.

## Scenes and objects

- `Scene` is the `.scene` asset and `SceneInstance` is the running world, both in `Prowl.Runtime.Resources`. Inside a component, `Scene` is the component's own world.
- Hold scenes in fields as `AssetRef<Scene>`, and load one with `NextLevel.Load()`. See [Loading scenes](../02-scripting/06-loading-scenes.md).
- `new GameObject("Name")` is in no world until you move it in with `go.MoveTo(Scene)`. `Scene.Create("Name")` makes one already in the world.
- Loading a level destroys everything except objects marked `Persistent`.
- Destroy an object with `go.Destroy()`. It stays valid until the end of the frame.

## Physics

- Triggers are their own component: add a `TriggerVolume`.
- `Rigidbody3D` has a `MotionType` of `Dynamic`, `Kinematic` or `Static`.
- Move dynamic bodies with velocity or forces, never through their `Transform`.

## Rendering

- Colours are **linear**. A value picked in an image editor needs converting, roughly `value ^ 2.2`.
- For a per-object colour, `Clone()` the material and assign the copy.
