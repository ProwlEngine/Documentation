---
title: Project structure
description: Describes the structure of user projects.
---

## Directory structure

When a Prowl project is created, the following structure is created:

```
MyProject/
├── Assets/                          # User asset files (.cs scripts, textures, models, etc.)
├── Library/                         # Editor-generated caches (NOT version controlled)
│   ├── cache/                       # Imported asset cache files ({guid}.asset binary files)
│   ├── thumbnails/                  # Asset thumbnail images
│   ├── ScriptAssemblies/            # Compiled user script DLLs
│   │   ├── MyProject.Game.dll
│   │   └── MyProject.Editor.dll
│   ├── metadata.db                  # Full asset index (Echo string format) for fast startup
│   └── EditorState.json             # Editor layout/state persistence
├── ProjectSettings/                 # Project configuration files (settings pages)
├── Packages/                        # Package references (empty by default)
├── Temp/                            # Temporary build files
│   └── PlayerBuild/                 # Player build temp directory
├── Logs/                            # Log files
├── Backups/                         # Project backups (migration backups)
├── MyProject.prowl                  # Project metadata
├── MyProject.Game.csproj            # Generated .csproj for runtime scripts
├── MyProject.Editor.csproj          # Generated .csproj for editor-only scripts
├── MyProject.slnx                   # Generated solution file
├── Directory.Build.props            # User MSBuild customization (NuGet packages, project refs)
└── .gitignore                       # Git source control exclusion list
```


## The Assets folder

This is where user code and assets should be placed. Every asset is assigned a unique GUID, which is
stored in a `*.meta` companion file, along with any importer settings.

> [!CAUTION]
> If you move or rename an asset outside the editor, you must also move or rename the associated .meta file.


## CSProj files

User code is split into two projects:
* `<ProjectName>.Game.csproj` — runtime scripts (all .cs files that are not editor-specific)
* `<ProjectName>.Editor.csproj` — editor-only scripts (.cs files under a `Editor/` folder)

> [!CAUTION]
> Do not modify these files as they are automatically generated.

> [!TIP]
> To add a NuGet package, modify `Directory.Build.props` instead of modifying a .csproj file.


## Plugin system

DLLs under any `Plugins/` folder in `Assets/` are treated as plugins; Prowl will add a reference to the DLL
in the relevant .csproj file.