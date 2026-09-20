"""Float formatting shared by ``to_python`` export and the node-class generator.

Blender stores socket values as float32. This module renders such a value as
the shortest Python literal that rebuilds the identical float32 (``0.1`` rather
than ``0.10000000149011612``), or as a ``math.pi`` / ``math.tau`` / ``math.e``
expression for the rational multiples of those constants (``3 * math.pi / 4``).

It is a leaf: stdlib and numpy only, no ``nodebpy`` imports. The generator in
``gen/`` loads it straight from this file (see ``gen/config.py``) so that a
broken generated tree can never block regenerating it.
"""

from __future__ import annotations

import math

import numpy as np


def within_one_ulp(candidate: float, f32) -> bool:
    """Whether ``candidate`` lands on ``f32`` or its immediate float32
    neighbour. One ULP is the round-off a value picks up crossing precisions
    (an authored ``0.15`` surviving as ``0.14999999``), so snapping across it
    restores the authored constant without moving any genuinely different
    value."""
    # A candidate beyond float32 range (a huge clamp bound) overflows the
    # cast to inf with a RuntimeWarning; it is never within one ULP.
    with np.errstate(over="ignore"):
        c32 = np.float32(candidate)
    if not np.isfinite(c32):
        return False
    return bool(c32 == f32 or np.nextafter(f32, c32) == c32)


def math_constant_expression(f32) -> str | None:
    """A ``math.pi``/``math.tau``/``math.e`` expression for a rational
    multiple of one of those constants, or None.

    Constants authored as expressions (``2 * math.pi``, ``pi / 3``, ``tau``,
    ``e``) survive in a blend only as float32 values; matching small-fraction
    multiples (within one ULP) restores the readable form. Numerators up to 48
    over denominators up to 12 cover the usual turns and subdivisions while
    keeping a chance coincidence with an ordinary decimal essentially
    impossible. An even multiple of pi renders in tau form (``math.tau``,
    ``math.tau / 3``) — with the fraction reduced, halving the numerator is
    always the simpler expression.
    """
    magnitude = abs(float(f32))
    if magnitude == 0.0:
        return None
    for name, const in (("pi", math.pi), ("e", math.e)):
        for den in range(1, 13):
            num = round(magnitude * den / const)
            if not 1 <= num <= 48 or math.gcd(num, den) != 1:
                continue
            if not within_one_ulp(num * const / den, abs(f32)):
                continue
            if name == "pi" and num % 2 == 0:
                name, num = "tau", num // 2
            expr = f"math.{name}" if num == 1 else f"{num} * math.{name}"
            if den > 1:
                expr = f"{expr} / {den}"
            return f"-{expr}" if float(f32) < 0 else expr
    return None


def group_digits(text: str) -> str:
    """Underscore-group a positional float literal's integer part when it has
    five or more digits (``10000.0`` → ``10_000.0``)."""
    sign = ""
    if text.startswith("-"):
        sign, text = "-", text[1:]
    int_part, dot, frac = text.partition(".")
    if len(int_part) < 5:
        return sign + text
    return sign + f"{int(int_part):_}" + dot + frac


def fmt_float(value: float, *, snap: bool = True) -> str:
    """Shortest readable literal for a float32-backed value.

    Blender stores socket values as float32, so reading them back through
    Python gives noisy float64 reprs (``0.10000000149011612``); the shortest
    decimal that uniquely identifies the float32 (``0.1``) rebuilds the
    identical socket value. On top of that, rational multiples of pi, tau
    and e render as ``math.*`` expressions, a value one ULP off a much shorter decimal
    snaps to it (``0.14999999`` → ``0.15``), and long integer parts get
    underscore grouping (``-10_000.0``). ``snap=False`` keeps the literal that
    rebuilds exactly this float32 (a generated default must be Blender's own
    value, not its prettier neighbour).
    """
    if not math.isfinite(value):
        return repr(value)
    f32 = np.float32(value)
    if float(f32) != value:
        return repr(value)  # genuine float64 — keep full precision
    const_expr = math_constant_expression(f32)
    if const_expr is not None:
        return const_expr
    text = np.format_float_positional(f32, unique=True, trim="0")
    # Snap to the shortest decimal within one ULP: fewer significant digits
    # first, so ``0.14999999`` becomes ``0.15`` rather than ``0.1499999``.
    digits = sum(c.isdigit() for c in text.lstrip("-0.")) if snap else 0
    for sig in range(1, digits):
        candidate = float(f"%.{sig}g" % float(f32))
        if not within_one_ulp(candidate, f32):
            continue
        snapped = np.format_float_positional(
            np.float32(candidate), unique=True, trim="0"
        )
        if len(snapped) < len(text):
            text = snapped
        break
    return group_digits(text)
