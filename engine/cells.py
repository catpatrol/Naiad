"""The pre-registered grid: 10 assets x 3 mandates = 30 cells (charter §4).

Frozen at ratification. Any addition requires a ledger entry and fresh
pre-registration — do not edit casually.
"""

from dataclasses import dataclass

INTERVAL_MS = {
    "1m": 60_000,
    "5m": 300_000,
    "15m": 900_000,
    "1h": 3_600_000,
    "4h": 14_400_000,
    "12h": 43_200_000,
}

INTERVALS = list(INTERVAL_MS)

# MTF telemetry set (v11: 5m / 1H / 4H / 12H — no 30m anywhere).
MTF_SET = ["5m", "1h", "4h", "12h"]

# Slippage tiers, bps per side (charter §5, confirmed at ratification).
SLIPPAGE_TIER_BPS = {"A": 2.0, "B": 5.0, "C": 10.0}

# Basket frozen at ratification (charter §4). XMR deferred, FET removed.
SYMBOLS = {
    "BTCUSDT": "A",
    "ETHUSDT": "A",
    "SOLUSDT": "B",
    "NEARUSDT": "B",
    "ZECUSDT": "B",
    "JTOUSDT": "B",
    "TAOUSDT": "B",
    "HYPEUSDT": "C",
    "FARTCOINUSDT": "C",
    "LITUSDT": "C",
}

# LIT two-token trap (charter §4, build prompt §4): LITUSDT carried Litentry
# before the Lighter perp listing. Hard floor — asserted in the loader.
LIT_FLOOR_MS = 1_766_448_000_000  # 2025-12-23T00:00:00Z (charter I1)

# Mandates (charter §4): governor / exec / A-grade alignment TF (build prompt §5:
# 4H gov -> 1H, 1H gov -> 5m, 12H gov -> 4H — mirrors Pine tfAlign options).
MANDATES = {
    "swing": {"gov": "4h", "exec": "5m", "align": "1h"},
    "intraday": {"gov": "1h", "exec": "1m", "align": "5m"},
    "position": {"gov": "12h", "exec": "15m", "align": "4h"},
}


@dataclass(frozen=True)
class Cell:
    cell_id: str
    symbol: str
    mandate: str
    tf_gov: str
    tf_exec: str
    tf_align: str
    slippage_bps: float

    @property
    def zone_memory(self) -> int:
        # Engine 1.0.3 input-parity conformance: match the deployed Pine
        # input DEFAULT zoneMemory=3 (SS_Cascade_v11.0.2.pine input.int,
        # line 121). The former 5-for-5m value is the "zoneMemory-5" v12
        # named-variant candidate (archived journal seed), not live.
        return 3


def make_cell(symbol: str, mandate: str) -> Cell:
    if symbol not in SYMBOLS:
        raise KeyError(f"symbol {symbol} is not in the frozen basket")
    m = MANDATES[mandate]
    return Cell(
        cell_id=f"{symbol}_{mandate}",
        symbol=symbol,
        mandate=mandate,
        tf_gov=m["gov"],
        tf_exec=m["exec"],
        tf_align=m["align"],
        slippage_bps=SLIPPAGE_TIER_BPS[SYMBOLS[symbol]],
    )


def all_cells() -> list[Cell]:
    return [make_cell(s, m) for s in SYMBOLS for m in MANDATES]


def cell_by_id(cell_id: str) -> Cell:
    symbol, _, mandate = cell_id.rpartition("_")
    return make_cell(symbol, mandate)
