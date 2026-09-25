# live.group_names_in_source

``` python
group_names_in_source(code)
```

Literal `_name` values assigned in class bodies of `code`.

Parsed with :mod:`ast`; both `_name = "..."` and `_name: str = "..."` count. Returns an empty set on a :class:`SyntaxError` (`exec` reports it).
