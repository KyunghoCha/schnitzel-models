#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import (
    assert_dataset_paths,
    dump_json,
    get_required,
    import_ultralytics,
    load_yaml,
    resolve_data_yaml,
    set_if_provided,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate model (skeleton)")
    parser.add_argument("--config", default="configs/eval_base.yaml")
    parser.add_argument("--data", help="Override data.data_yaml")
    parser.add_argument("--weights", help="Override model.weights")
    parser.add_argument("--img-size", type=int, help="Override model.img_size")
    parser.add_argument("--device", help="Override model.device")
    parser.add_argument("--exp-dir", help="Override output.exp_dir")
    parser.add_argument("--run-name", help="Override output.run_name")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"config not found: {cfg_path}")
        return 1

    cfg = load_yaml(cfg_path)
    set_if_provided(cfg, ["data", "data_yaml"], args.data)
    set_if_provided(cfg, ["model", "weights"], args.weights)
    set_if_provided(cfg, ["model", "img_size"], args.img_size)
    set_if_provided(cfg, ["model", "device"], args.device)
    set_if_provided(cfg, ["output", "exp_dir"], args.exp_dir)
    set_if_provided(cfg, ["output", "run_name"], args.run_name)

    data_yaml = get_required(cfg, ["data", "data_yaml"], "data.data_yaml")
    data_path = Path(str(data_yaml))
    if not data_path.exists():
        raise FileNotFoundError(f"data yaml not found: {data_path}")
    assert_dataset_paths(data_path)
    data_resolved = resolve_data_yaml(data_path)
    weights = get_required(cfg, ["model", "weights"], "model.weights")
    img_size = get_required(cfg, ["model", "img_size"], "model.img_size")
    device = cfg.get("model", {}).get("device", "auto")
    exp_dir = cfg.get("output", {}).get("exp_dir", "experiments")
    run_name = cfg.get("output", {}).get("run_name", "eval_run")

    YOLO = import_ultralytics()
    model = YOLO(weights)

    print("[eval] config")
    print(dump_json(cfg))
    model.val(
        data=str(data_resolved),
        imgsz=img_size,
        device=device,
        project=str(exp_dir),
        name=str(run_name),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
