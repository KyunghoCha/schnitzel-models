# Pipeline Integration Contract

## English
This document defines how exported models from this repo must align with the runtime pipeline repo (`schnitzel-stream-platform`).

**Adapters in runtime**
- YOLO PT: `ai.vision.yolo_adapter:YOLOAdapter`
- YOLO ONNX: `ai.vision.onnx_adapter:ONNXYOLOAdapter`
- Multi-adapter merge: comma-separated `AI_MODEL_ADAPTER`

**Required export formats**
- `.pt` for Ultralytics YOLO (PT adapter)
- `.onnx` for ONNX Runtime (ONNX adapter)

**Class mapping**
- Provide a YAML mapping (`MODEL_CLASS_MAP_PATH`) for class_id -> event/object/severity
- Reference: `docs/specs/model_class_taxonomy.md`

**Detection payload contract**
Each detection emitted by a model adapter must include:
- `event_type`, `object_type`, `severity`
- `confidence`
- `bbox` (`x1`, `y1`, `x2`, `y2`)
- `track_id` is required for PERSON (use a synthetic id if no tracker)

**Training/export checklist**
- Update taxonomy if new labels are added
- Update class map YAML
- Export to ONNX/PT
- Validate with sample video using runtime pipeline

## 한국어
이 문서는 본 레포에서 export한 모델이 런타임 파이프라인(`schnitzel-stream-platform`)과 호환되기 위한 규약을 정의합니다.

**런타임 어댑터**
- YOLO PT: `ai.vision.yolo_adapter:YOLOAdapter`
- YOLO ONNX: `ai.vision.onnx_adapter:ONNXYOLOAdapter`
- 멀티 어댑터 병합: `AI_MODEL_ADAPTER` 콤마 구분

**필수 export 형식**
- Ultralytics YOLO용 `.pt`
- ONNX Runtime용 `.onnx`

**클래스 매핑**
- YAML 매핑(`MODEL_CLASS_MAP_PATH`)으로 class_id -> event/object/severity 제공
- 기준 문서: `docs/specs/model_class_taxonomy.md`

**Detection 페이로드 계약**
모델 어댑터가 반환하는 detection은 다음 필드를 포함해야 합니다:
- `event_type`, `object_type`, `severity`
- `confidence`
- `bbox` (`x1`, `y1`, `x2`, `y2`)
- PERSON의 `track_id`는 필수이며, 트래커가 없으면 합성 id를 부여

**학습/export 체크리스트**
- 라벨 추가 시 taxonomy 업데이트
- class map YAML 갱신
- ONNX/PT export
- 런타임 파이프라인에서 샘플 영상 검증
