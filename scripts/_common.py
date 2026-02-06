from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import os
import tempfile


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - dependency error
        raise RuntimeError(
            "PyYAML is required. Install with: pip install pyyaml"
        ) from exc
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"config must be a mapping: {path}")
    return data


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_required(cfg: dict[str, Any], path: list[str], name: str) -> Any:
    cur: Any = cfg
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            raise ValueError(f"missing required config: {name}")
        cur = cur[p]
    return cur


def set_if_provided(cfg: dict[str, Any], path: list[str], value: Any) -> None:
    if value is None:
        return
    cur = cfg
    for p in path[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[path[-1]] = value


def import_ultralytics():
    try:
        from ultralytics import YOLO  # type: ignore
    except Exception as exc:  # pragma: no cover - dependency error
        raise RuntimeError(
            "ultralytics is required. Install with: pip install ultralytics"
        ) from exc
    return YOLO


def resolve_data_yaml(data_yaml: Path) -> Path:
    cfg = load_yaml(data_yaml)
    base_dir = data_yaml.parent
    root = cfg.get("path")
    if root:
        root_path = Path(root)
        if not root_path.is_absolute():
            root_path = (base_dir / root_path).resolve()
    else:
        root_path = base_dir.resolve()

    def _resolve_entry(key: str) -> str | None:
        val = cfg.get(key)
        if val is None:
            return None
        p = Path(val)
        if not p.is_absolute():
            p = (root_path / p).resolve()
        return str(p)

    cfg["path"] = str(root_path)
    for key in ("train", "val", "test"):
        resolved = _resolve_entry(key)
        if resolved is not None:
            cfg[key] = resolved

    # Write a resolved temp yaml to avoid global Ultralytics settings interference.
    cache_dir = root_path / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_path = cache_dir / "data_resolved.yaml"
    with out_path.open("w", encoding="utf-8") as f:
        import yaml  # type: ignore
        yaml.safe_dump(cfg, f, sort_keys=False)
    return out_path


def assert_dataset_paths(data_yaml: Path) -> None:
    cfg = load_yaml(data_yaml)
    root = Path(cfg.get("path", data_yaml.parent)).resolve()
    missing = []
    for key in ("train", "val"):
        val = cfg.get(key)
        if not val:
            missing.append(f"{key} (missing in data.yaml)")
            continue
        p = Path(val)
        if not p.is_absolute():
            p = root / p
        if not p.exists():
            missing.append(str(p))
    if missing:
        msg = "dataset paths not found: " + ", ".join(missing)
        raise FileNotFoundError(msg)
