"""Named frozen config variants (build prompt §2 invariant 10).

The engine takes a config id; every journal row carries config_id +
engine_version + run_id.
"""

import hashlib
from pathlib import Path

import yaml

from engine.version import ENGINE_VERSION

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"


def load_config(config_id: str) -> dict:
    path = CONFIG_DIR / f"{config_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"no such config: {config_id} ({path})")
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if cfg.get("config_id") != config_id:
        raise ValueError(
            f"config file {path} declares config_id={cfg.get('config_id')!r}, "
            f"expected {config_id!r}"
        )
    return cfg


def make_run_id(config_id: str, cell_id: str, start: str, end: str) -> str:
    """Deterministic run id — a function of the run's identifying inputs only.

    F1 (bit-identical reruns) forbids random or wall-clock components: two runs
    with identical args must produce byte-identical journals, run_id included.
    """
    key = f"{ENGINE_VERSION}|{config_id}|{cell_id}|{start}|{end}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]
