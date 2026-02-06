#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import dump_json, get_required, import_ultralytics, load_yaml, set_if_provided


def main() -> int:
    parser = argparse.ArgumentParser(description="Export model (skeleton)")
    parser.add_argument("--config", default="configs/export_base.yaml")
    parser.add_argument("--weights", help="Override model.weights")
    parser.add_argument("--img-size", type=int, help="Override model.img_size")
    parser.add_argument("--device", help="Override model.device")
    parser.add_argument("--format", help="Override export.format (onnx|torchscript|engine)")
    parser.add_argument("--opset", type=int, help="Override export.opset")
    parser.add_argument("--dynamic", action="store_true", help="Force export.dynamic=true")
    parser.add_argument("--out-dir", help="Override output.out_dir")
    parser.add_argument("--out-name", help="Override output.out_name (basename)")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"config not found: {cfg_path}")
        return 1

    cfg = load_yaml(cfg_path)
    set_if_provided(cfg, ["model", "weights"], args.weights)
    set_if_provided(cfg, ["model", "img_size"], args.img_size)
    set_if_provided(cfg, ["model", "device"], args.device)
    set_if_provided(cfg, ["export", "format"], args.format)
    set_if_provided(cfg, ["export", "opset"], args.opset)
    if args.dynamic:
        set_if_provided(cfg, ["export", "dynamic"], True)
    set_if_provided(cfg, ["output", "out_dir"], args.out_dir)
    set_if_provided(cfg, ["output", "out_name"], args.out_name)

    weights = get_required(cfg, ["model", "weights"], "model.weights")
    img_size = get_required(cfg, ["model", "img_size"], "model.img_size")
    device = cfg.get("model", {}).get("device", "auto")
    fmt = cfg.get("export", {}).get("format", "onnx")
    opset = cfg.get("export", {}).get("opset", 12)
    dynamic = bool(cfg.get("export", {}).get("dynamic", True))
    out_dir = Path(cfg.get("output", {}).get("out_dir", "models"))
    out_name = cfg.get("output", {}).get("out_name", "model_export")

    YOLO = import_ultralytics()
    model = YOLO(weights)

    print("[export] config")
    print(dump_json(cfg))
    export_result = model.export(
        format=str(fmt),
        imgsz=img_size,
        device=device,
        opset=opset,
        dynamic=dynamic,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    exported_path = Path(export_result)
    suffix = exported_path.suffix
    target = out_dir / f"{out_name}{suffix}"
    if exported_path.resolve() != target.resolve():
        shutil.copy2(exported_path, target)
    print(f"[export] saved: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
