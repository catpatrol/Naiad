#!/usr/bin/env python
"""TIER-C12 · TickGrid — EXACT INTEGER-TICK ARITHMETIC [LEANS L-D.23; rulings O-20, O-27].

"trades THROUGH the limit by >= 1 tick (low < limit - tick for a long)" (contract :93-94).
O-20: "Tick arithmetic is exact (integer ticks), never float compare."

A PURE module: the stdlib `decimal` and nothing else — no numpy, no I/O, no engine import.  ONE
class, constructed from the venue's tick STRING (the `price_tick` of Stage D's own capture,
research_outputs/tierc12/data/CONTRACT_SPECS.json; no tick is typed anywhere):

    TickGrid(tick: str)          HALT unless `tick` is a str naming a finite Decimal > 0
      .T                         Decimal(tick)
      .ctx                       the grid's TRAPPING decimal.Context (below)
      .dec(x)                    the exact Decimal of an admissible x
      .floor_ticks(x)            q            where q, r = divmod(dec(x), T), 0 <= r < T
      .ceil_ticks(x)             q + (1 if r != 0 else 0)
      .on_grid(x)                r == 0
      .px(n)                     float(n x T), the round trip asserted (dec(px(n)) == n x T)
      .lt(x, n) .le(x, n) .gt(x, n) .ge(x, n)     x against the grid level n x T — INTEGER
                                 comparisons, exact for an off-grid x too:
                                   lt: x <  n.T  <=>  floor_ticks(x) <= n - 1
                                   le: x <= n.T  <=>  ceil_ticks(x)  <= n
                                   gt: x >  n.T  <=>  ceil_ticks(x)  >= n + 1
                                   ge: x >= n.T  <=>  floor_ticks(x) >= n

WHAT AN x MAY BE.  A `float` (a numpy.float64 IS a float) — converted by Decimal(repr(float(x))),
the shortest decimal that round-trips the float64, which for every tape price is the venue's own
printed decimal — or a `decimal.Decimal`, used exactly as given (no float round trip).  It must be
finite and > 0.  Any other type HALTs: an int, a bool, a str, a numpy.float32.

WHAT A LEVEL n MAY BE [amendment AM-59].  An `int` and nothing else — `type(n) is int`: a bool is
not an int here, and a float, a decimal.Decimal and a numpy integer are refused.  px(n) and the
four comparisons lt / le / gt / ge HALT on any other type, so a level is never silently decided by
a float compare.  A consumer takes n from floor_ticks / ceil_ticks, which return an int.

THE TRAPPING CONTEXT.  All arithmetic stays inside ONE local decimal.Context, `ctx`, which TRAPS
Inexact and Rounded (and FloatOperation, so a Decimal is never silently mixed with a float): an
operation that cannot be exact HALTs instead of rounding.  Its precision and exponent limits are
not typed numbers: they are the stdlib objects decimal.MAX_PREC, decimal.MAX_EMAX and
decimal.MIN_EMIN, so a Decimal argument of any length is divided exactly (under the default
28-digit context the same divmod signals Inexact on an argument longer than the precision).  The
class performs only +, -, x, divmod and comparisons.  A decimal signal surfaces as a HALT
(SystemExit), never as a rounded value.  MEASURED AT BUILD: at this precision CPython answers a
quotient that is not exact (Decimal(1) / Decimal(3) under `ctx`) with MemoryError, not with
decimal.Inexact — still a raise and never a rounding; this class turns both into its HALT, and a
consumer forming its own expression under `ctx` must treat MemoryError as the same HALT.

A CONSUMER'S OWN EXACT EXPRESSION (the scalper's T2 and DEEP depth, the conditioned maker entry)
is formed under `decimal.localcontext(grid.ctx)` and under no other context, and its Decimal
result is handed to floor_ticks / ceil_ticks / a comparison as is.

This module defines NO fill rule, no snapping direction and no order model: L-S and L-R state
those in terms of floor_ticks / ceil_ticks, the four comparisons and ctx.  No float subtraction,
no float comparison, no tolerance.
"""
from __future__ import annotations

import decimal
from decimal import Decimal


def halt(msg: str):
    raise SystemExit(f"HALT: TickGrid: {msg}")


class TickGrid:
    """The exact grid of one venue tick (see the module docstring for the whole interface)."""

    def __init__(self, tick: str):
        if type(tick) is not str:
            halt(f"the tick must be the venue's STRING, got {type(tick).__name__}")
        self.ctx = decimal.Context(
            prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN,
            traps=[decimal.Inexact, decimal.Rounded, decimal.FloatOperation, decimal.InvalidOperation,
                   decimal.DivisionByZero, decimal.Overflow])
        try:
            grid_step = Decimal(tick)
        except decimal.DecimalException as e:
            halt(f"{tick!r} is not a decimal ({type(e).__name__})")
        zero = Decimal()
        if not grid_step.is_finite() or not grid_step > zero:
            halt(f"{tick!r} is not finite and > 0")
        self.T = grid_step

    def dec(self, x) -> Decimal:
        """The exact Decimal of an admissible x: a float by its shortest round-trip repr, a
        Decimal as given.  HALTs on any other type, a non-finite or a non-positive x."""
        if isinstance(x, bool):
            halt(f"x of type bool ({x!r})")
        if isinstance(x, float):
            try:
                d = Decimal(repr(float(x)))
            except decimal.DecimalException as e:
                halt(f"float {x!r} has no decimal ({type(e).__name__})")
        elif isinstance(x, Decimal):
            d = x
        else:
            halt(f"x of type {type(x).__name__} ({x!r}) — a float or a decimal.Decimal only")
        if not d.is_finite() or not d > Decimal():
            halt(f"x = {x!r} is not finite and > 0")
        return d

    def _divmod(self, x):
        try:
            q, r = self.ctx.divmod(self.dec(x), self.T)
        except (decimal.DecimalException, MemoryError) as e:
            halt(f"divmod({x!r}, {self.T}) is not exact ({type(e).__name__})")
        return int(q), r

    def floor_ticks(self, x) -> int:
        q, _ = self._divmod(x)
        return q

    def ceil_ticks(self, x) -> int:
        q, r = self._divmod(x)
        return q + (1 if r != 0 else 0)

    def on_grid(self, x) -> bool:
        _, r = self._divmod(x)
        return r == 0

    def px(self, n: int) -> float:
        """float(n x T), with the round trip asserted."""
        if type(n) is not int:
            halt(f"px(n) takes an int level, got {type(n).__name__}")
        try:
            level = self.ctx.multiply(Decimal(n), self.T)
        except (decimal.DecimalException, MemoryError) as e:
            halt(f"{n} x {self.T} is not exact ({type(e).__name__})")
        out = float(level)
        if self.dec(out) != level:
            halt(f"px({n}) = {out!r} does not round-trip to {level}")
        return out

    def _level(self, n, name: str) -> int:
        """The level of a comparison [AM-59]: an int and nothing else — `type(n) is int`, exactly
        as px(n) (a bool is not an int here; a float, a Decimal or a numpy integer HALTs).  A
        consumer takes n from floor_ticks / ceil_ticks."""
        if type(n) is not int:
            halt(f"{name}(x, n) takes an int level, got {type(n).__name__}")
        return n

    def lt(self, x, n: int) -> bool:
        self._level(n, "lt")
        below = n - 1
        return self.floor_ticks(x) <= below

    def le(self, x, n: int) -> bool:
        self._level(n, "le")
        return self.ceil_ticks(x) <= n

    def gt(self, x, n: int) -> bool:
        self._level(n, "gt")
        above = n + 1
        return self.ceil_ticks(x) >= above

    def ge(self, x, n: int) -> bool:
        self._level(n, "ge")
        return self.floor_ticks(x) >= n
