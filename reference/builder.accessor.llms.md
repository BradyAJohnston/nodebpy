# builder.accessor

`accessor`

## Classes

| Name | Description |
|----|----|
| [SocketAccessor](#nodebpy.builder.accessor.SocketAccessor) | Unified accessor for a node’s input or output socket collection. |

### SocketAccessor

``` python
SocketAccessor(collection, direction)
```

Unified accessor for a node’s input or output socket collection.

Supports identifier/name lookup, dict-style `[]` access, availability filtering, and type-compatible matching — replacing the former pairs of `_input_idx`/`_output_idx`, `_input`/`_output`, `_available_inputs`/`_available_outputs`, and `_best_output_socket`.
