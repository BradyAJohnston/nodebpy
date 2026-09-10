# export.compare_libraries

``` python
compare_libraries(a, b, *, ignore=frozenset())
```

Differences between two :func:`serialize_library` captures.

`ignore` selects the surfaces to exclude (see :data:`SURFACES`); an unknown surface name raises so a typo can’t silently widen the check.
