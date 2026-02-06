# Ops Quickstart

## English
Purpose
-------
Provide a minimal, reproducible flow for local training/eval/export.

Prereqs
-------
- Python 3.10+
- `pip install ultralytics pyyaml`
- Default device is `cpu`; use `--device 0` for GPU

Dataset (YOLO)
--------------
- Update `datasets/data.yaml` to point at your local paths.
- Images/labels should follow YOLO format.
- Ensure `datasets/images/train` and `datasets/images/val` exist (or adjust paths).

Train
-----
```bash
python scripts/train.py \
  --config configs/train_base.yaml \
  --weights yolov8n.pt \
  --data datasets/data.yaml \
  --epochs 50 --batch 16 --img-size 640
```

Eval
----
```bash
python scripts/eval.py \
  --config configs/eval_base.yaml \
  --weights runs/train/weights/best.pt \
  --data datasets/data.yaml
```

Export
------
```bash
python scripts/export.py \
  --config configs/export_base.yaml \
  --weights runs/train/weights/best.pt \
  --format onnx --opset 12
```

Runtime Validation
------------------
Use the runtime repo to validate:
- `AI_MODEL_ADAPTER=ai.vision.onnx_adapter:ONNXYOLOAdapter`
- `ONNX_MODEL_PATH=models/model_export.onnx`
- `MODEL_CLASS_MAP_PATH=configs/model_class_map.yaml`

## 한국어
목적
-----
로컬에서 학습/평가/export를 빠르게 재현하는 최소 흐름을 제공한다.

사전 준비
---------
- Python 3.10+
- `pip install ultralytics pyyaml`
- 기본 device는 `cpu`, GPU 사용 시 `--device 0` 지정

데이터셋(YOLO)
-------------
- `datasets/data.yaml`의 경로를 로컬 환경에 맞게 수정한다.
- 이미지/라벨은 YOLO 포맷을 따른다.
- `datasets/images/train`, `datasets/images/val` 경로가 존재해야 한다(필요 시 수정).

학습
----
```bash
python scripts/train.py \
  --config configs/train_base.yaml \
  --weights yolov8n.pt \
  --data datasets/data.yaml \
  --epochs 50 --batch 16 --img-size 640
```

평가
----
```bash
python scripts/eval.py \
  --config configs/eval_base.yaml \
  --weights runs/train/weights/best.pt \
  --data datasets/data.yaml
```

Export
------
```bash
python scripts/export.py \
  --config configs/export_base.yaml \
  --weights runs/train/weights/best.pt \
  --format onnx --opset 12
```

런타임 검증
----------
런타임 레포에서 아래 설정으로 검증:
- `AI_MODEL_ADAPTER=ai.vision.onnx_adapter:ONNXYOLOAdapter`
- `ONNX_MODEL_PATH=models/model_export.onnx`
- `MODEL_CLASS_MAP_PATH=configs/model_class_map.yaml`
