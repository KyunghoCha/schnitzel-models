# Train / Eval / Export

## English
**Flow**
1. Prepare dataset (train/val split)
2. Train model
3. Evaluate (mAP, recall/precision)
4. Export to ONNX/PT
5. Validate in runtime pipeline

**Skeletons (this repo)**
- Train: `scripts/train.py` with `configs/train_base.yaml`
- Eval: `scripts/eval.py` with `configs/eval_base.yaml`
- Export: `scripts/export.py` with `configs/export_base.yaml`

**Notes**
- ONNX export must match runtime adapter input/output expectations
- Update `MODEL_CLASS_MAP_PATH` when labels change
- Requires `ultralytics` and `pyyaml`

**Example (train)**
```bash
python scripts/train.py \
  --config configs/train_base.yaml \
  --weights yolov8n.pt \
  --data datasets/data.yaml \
  --epochs 50 --batch 16 --img-size 640
```

**Example (eval)**
```bash
python scripts/eval.py \
  --config configs/eval_base.yaml \
  --weights runs/train/weights/best.pt \
  --data datasets/data.yaml
```

**Example (export)**
```bash
python scripts/export.py \
  --config configs/export_base.yaml \
  --weights runs/train/weights/best.pt \
  --format onnx --opset 12
```

**Recommended Outputs**
- `models/` for exported weights (local)
- `experiments/` for logs/metrics (local)

## 한국어
**흐름**
1. 데이터 준비(train/val 분할)
2. 학습
3. 평가(mAP, recall/precision)
4. ONNX/PT export
5. 런타임 파이프라인 검증

**골격 스크립트(본 레포)**
- 학습: `scripts/train.py` + `configs/train_base.yaml`
- 평가: `scripts/eval.py` + `configs/eval_base.yaml`
- export: `scripts/export.py` + `configs/export_base.yaml`

**노트**
- ONNX export는 런타임 어댑터 입출력 규격과 일치해야 함
- 라벨 변경 시 `MODEL_CLASS_MAP_PATH` 갱신 필요
- `ultralytics`, `pyyaml` 필요

**예시(학습)**
```bash
python scripts/train.py \
  --config configs/train_base.yaml \
  --weights yolov8n.pt \
  --data datasets/data.yaml \
  --epochs 50 --batch 16 --img-size 640
```

**예시(평가)**
```bash
python scripts/eval.py \
  --config configs/eval_base.yaml \
  --weights runs/train/weights/best.pt \
  --data datasets/data.yaml
```

**예시(export)**
```bash
python scripts/export.py \
  --config configs/export_base.yaml \
  --weights runs/train/weights/best.pt \
  --format onnx --opset 12
```

**권장 출력 경로**
- `models/`: export 결과(로컬)
- `experiments/`: 로그/메트릭(로컬)
