#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml


def load_cfg(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export model (skeleton)")
    parser.add_argument("--config", default="configs/export_base.yaml")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"config not found: {cfg_path}")
        return 1

    cfg = load_cfg(cfg_path)
    print("[export] config loaded")
    print(cfg)
    print("[export] TODO: implement export pipeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
