#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from scripts._common import dump_json, get_required, import_ultralytics, load_yaml, set_if_provided


def main() -> int:
    parser = argparse.ArgumentParser(description="Train model (skeleton)")
    parser.add_argument("--config", default="configs/train_base.yaml")
    parser.add_argument("--data", help="Override data.data_yaml")
    parser.add_argument("--weights", help="Override model.weights")
    parser.add_argument("--epochs", type=int, help="Override model.epochs")
    parser.add_argument("--batch", type=int, help="Override model.batch")
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
    set_if_provided(cfg, ["model", "epochs"], args.epochs)
    set_if_provided(cfg, ["model", "batch"], args.batch)
    set_if_provided(cfg, ["model", "img_size"], args.img_size)
    set_if_provided(cfg, ["model", "device"], args.device)
    set_if_provided(cfg, ["output", "exp_dir"], args.exp_dir)
    set_if_provided(cfg, ["output", "run_name"], args.run_name)

    data_yaml = get_required(cfg, ["data", "data_yaml"], "data.data_yaml")
    weights = get_required(cfg, ["model", "weights"], "model.weights")
    img_size = get_required(cfg, ["model", "img_size"], "model.img_size")
    batch = get_required(cfg, ["model", "batch"], "model.batch")
    epochs = get_required(cfg, ["model", "epochs"], "model.epochs")
    device = cfg.get("model", {}).get("device", "auto")
    exp_dir = cfg.get("output", {}).get("exp_dir", "experiments")
    run_name = cfg.get("output", {}).get("run_name", "train_run")

    YOLO = import_ultralytics()
    model = YOLO(weights)

    print("[train] config")
    print(dump_json(cfg))
    model.train(
        data=str(data_yaml),
        imgsz=img_size,
        batch=batch,
        epochs=epochs,
        device=device,
        project=str(exp_dir),
        name=str(run_name),
        exist_ok=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
