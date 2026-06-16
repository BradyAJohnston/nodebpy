# assets.PackageLibrary

``` python
PackageLibrary(anchor, relative)
```

A `.blend` shipped inside a Python package, located relative to a module file. Pass `anchor=__file__` from the generated module and the path to the `.blend` relative to it::

    PackageLibrary(__file__, "../data/my_assets.blend")

## Attributes

| Name                                                  | Description |
|-------------------------------------------------------|-------------|
| [`anchor`](#nodebpy.assets.PackageLibrary.anchor)     |             |
| [`relative`](#nodebpy.assets.PackageLibrary.relative) |             |

## Methods

| Name                                        | Description |
|---------------------------------------------|-------------|
| [path](#nodebpy.assets.PackageLibrary.path) |             |

### path

``` python
path()
```
