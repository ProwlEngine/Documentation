---
title: Anthology libraries
description: Use Prowl's systems on their own, without the engine.
---

Many systems in Prowl are also their own `Prowl.*` NuGet packages, maintained in the [Anthology repository](https://github.com/ProwlEngine/Anthology). They version together, so a change across several libraries lands in one commit.

## Install one

```bash
dotnet add package Prowl.Paper
```

## The libraries

| Package | Purpose |
| --- | --- |
| Prowl.Graphite | Low-level Vulkan graphics with a render graph |
| Prowl.Prism | GLSL to SPIR-V compiler |
| Prowl.Paper | Immediate-mode UI framework |
| Prowl.Origami | Widgets for Paper |
| Prowl.Scaffold | Incremental layout engine |
| Prowl.Quill | GPU 2D vector graphics |
| Prowl.Scribe | TrueType fonts and text layout |
| Prowl.Quire | Markdown parser |
| Prowl.Rosetta | Localization |
| Prowl.Vector | Math and geometry |
| Prowl.Echo | Serialization |
| Prowl.Ember | Hot reload state migration |
| Prowl.Crumb | Tokenizer |
| Prowl.Clay | Model importing (glTF, FBX, OBJ) |
| Prowl.Aperture | Image decoding |
| Prowl.Motion | Skeletal animation and IK |
| Prowl.Recast | Navmesh generation and pathfinding |
| Prowl.Photonic | Progressive CPU lightmapper |
| Prowl.Unwrapper | UV unwrapping |
| Prowl.Slang | Bindings for the Slang compiler |
| Prowl.Courier | Game networking: reliable UDP (KCP) and in-process local transports |
