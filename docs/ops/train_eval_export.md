# Train / Eval / Export

## English
**Flow**
1. Prepare dataset (train/val split)
2. Train model
3. Evaluate (mAP, recall/precision)
4. Export to ONNX/PT
5. Validate in runtime pipeline

**Notes**
- ONNX export must match runtime adapter input/output expectations
- Update `MODEL_CLASS_MAP_PATH` when labels change

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

**노트**
- ONNX export는 런타임 어댑터 입출력 규격과 일치해야 함
- 라벨 변경 시 `MODEL_CLASS_MAP_PATH` 갱신 필요

**권장 출력 경로**
- `models/`: export 결과(로컬)
- `experiments/`: 로그/메트릭(로컬)
