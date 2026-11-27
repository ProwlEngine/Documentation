---
title: Serialization
description: What Prowl saves from your components and assets, and how to control it.
---

**Serialization** is turning an object into saved data and back. Scenes, prefabs, assets, play mode, copy and paste, and undo all use it. A value that is not serialized is lost in every one of those.

This page assumes you have written a [component](01-components.md).

## Quick recipe

```csharp
using Prowl.Echo;
using Prowl.Runtime;

public sealed class Turret : Component
{
    public float Range = 20f;                    // shown and saved
    [SerializeField] private int _ammo = 30;     // private, but shown and saved
    [HideInInspector] public int Kills;          // saved, not shown
    [SerializeIgnore] public float Heat;         // not shown, not saved
    private float _cooldown;                     // not shown, not saved
}
```

[screenshot needed: Turret in the Inspector showing Range and Ammo only]

## What is saved

Prowl saves instance fields. It does not save properties, static fields or private fields without an attribute.

| Member | Saved | Shown in Inspector |
| --- | --- | --- |
| Public field | Yes | Yes |
| Private field with `[SerializeField]` | Yes | Yes |
| Any field with `[SerializeIgnore]` or `[NonSerialized]` | No | No |
| Property, static field, plain private field | No | No |
| Field with `[HideInInspector]` | Yes | No |

Fields declared in a base class count too. To save a property, mark it `[DataMember]` (from `System.Runtime.Serialization`). It needs a getter and a setter. A `[SerializeField]` private field behind a property is simpler.

Do not mark serialized fields `readonly`. Loading logs a warning for them.

### Save a field only sometimes

`[SerializeIf("Member")]` saves a field only while a `bool` field, property or method of that name returns true.

```csharp
public bool UseCustomColor;
[SerializeIf(nameof(UseCustomColor))] public Color Tint;
```

## Rename a field without losing data

Saved data is stored under the field name. If you rename `Damage` to `BaseDamage`, old scenes still hold `Damage`, so the new field loads its default. Add the old name:

```csharp
[FormerlySerializedAs("Damage")] public float BaseDamage = 10f;
```

The attribute is repeatable for several old names. Put it on a class to keep data after renaming the class, using the old short or namespace-qualified name.

## Run code around saving

Implement `ISerializationCallbackReceiver` to run code right before saving and right after loading. A component overrides `OnBeforeSerialize` and `OnAfterDeserialize` instead.

```csharp
[SerializeIgnore] public int NameLength;
public string Label = "";

public override void OnAfterDeserialize() => NameLength = Label.Length;
```

A loaded component is not yet in a [world](05-scenes-and-worlds.md) during these callbacks, so check `IsInWorld` before using `Scene`.

## What can be saved

- Numbers, `bool`, `string`, `Guid`, `DateTime`, `TimeSpan`, enums and nullable values.
- Math types such as `Float3` and `Color`.
- Arrays, `List<T>`, `Dictionary<K,V>`, `HashSet<T>`, `Queue<T>` and `Stack<T>`.
- Your own classes and structs, saved field by field with the same rules as above.
- Assets. A plain field such as `Texture` saves a reference to the asset. `AssetRef<T>` saves its ID without loading it.
- Other GameObjects, components and `Transform`s in the same scene. They are saved as links.

`AssetRef<T>` suits assets you may not need right away, such as a list of levels. See [Assets and importers](../07-editor/04-assets-and-importers.md).

Delegates and events are not saved. A scene object reference that cannot be found on load becomes null. Prefabs add a limit of their own, covered in [Prefabs](08-prefabs.md#spawn-from-a-script).

## See also

- [Components](01-components.md)
- [Prefabs](08-prefabs.md)
