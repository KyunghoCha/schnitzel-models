# Model Interface (Mock-First)

## English
Purpose
-------
This document defines the minimum output contract for model/tracker integration.
Mock mode is the default for pipeline validation, while real adapters are supported
when a model is provided. The payload structure must remain stable.

Event Output Contract
---------------------
Each processed frame should produce zero or more event payloads with fields.
The pipeline accepts either a single dict or a list of dicts from the builder.

- `event_id` (uuid string)
- `ts` (ISO-8601 string)
- `site_id` (string)
- `camera_id` (string)
- `event_type` (enum string)
- `object_type` (enum string)
- `severity` (enum string)
- `track_id` (int or null)
- `bbox` (`{x1,y1,x2,y2}` integers)
- `confidence` (0..1 float)
- `zone` (`{zone_id, inside}`) is injected by the pipeline if zones are enabled
- `snapshot_path` (string or null)

Model/Tracker Output (minimal)
------------------------------
Model or tracker outputs must provide:

- `bbox`
- `confidence`
- `track_id` (required for PERSON; use a synthetic id if no tracker)
- `event_type`
- `object_type`
- `severity`

Mapping Rules
-------------
- If the model returns multiple detections, emit one event per detection.
- `event_id`, `ts`, `site_id`, `camera_id` are assigned by the builder/adapter layer.
- `zone` is evaluated in the pipeline using `bbox` and `event_type`.
- `snapshot_path` is injected only when snapshots are enabled and saved successfully.

Mock Builder
------------
- Default mode: `model.mode=mock`
- Produces deterministic placeholder events for pipeline validation.
  - `model.mode=real` requires a real adapter; it raises an error if no adapter is provided.

Real Model Integration (supported)
----------------------------------
Implement or plug in a builder/adapter that:

1. Runs inference on `frame`
2. Converts detections into the payload contract
3. Returns payload dict(s) for downstream emitters

Scope & Constraints (draft)
---------------------------
1) Current protocol v0.2 includes PERSON/FIRE/SMOKE plus PPE/POSTURE/HAZARD (draft).
2) If you add new classes beyond this list, update the protocol first.
3) One model is acceptable if it covers required classes with acceptable FPS.
4) Multiple models are also acceptable; the adapter can merge detections per frame.

Baseline Model (pretrained)
---------------------------
For early integration, use a pretrained YOLO model and validate the pipeline
with limited classes (e.g., PERSON). This provides a stable baseline before
custom training.

Notes
-----
- Pretrained COCO models typically do not cover smoke/fire/PPE/pose.
- Add a class-mapping table in the builder to map model classes to
  `event_type`/`object_type`/`severity`.
- If the model doesn't provide tracking, the adapter should assign a
  per-detection synthetic `track_id` (required for PERSON).
- Baseline tracker: set `TRACKER_TYPE=iou` to enable simple IoU-based tracking.
- Use `AI_MODEL_ADAPTER` to select adapter implementation at runtime.
- For multiple models, pass a comma-separated list (e.g., `a:AdapterA,b:AdapterB`).
- Optional class mapping: set `MODEL_CLASS_MAP_PATH` to a yaml file (draft: `configs/model_class_map.yaml`).
- A custom adapter template is available in the runtime repo:
  `be-ai-endpoint/src/ai/vision/custom_adapter.py`.
- ONNX baseline adapter (runtime repo): `be-ai-endpoint/src/ai/vision/onnx_adapter.py`.

Mock I/O Examples
-----------------
Input (frame metadata, simplified)
```json
{ "frame_idx": 12, "camera_id": "cam01", "ts": "2026-02-05T14:00:01+09:00" }
```

Output (single detection)
```json
{
  "event_type": "ZONE_INTRUSION",
  "object_type": "PERSON",
  "severity": "LOW",
  "track_id": 12,
  "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
  "confidence": 0.75
}
```

Output (multiple detections)
```json
[
  {
    "event_type": "ZONE_INTRUSION",
    "object_type": "PERSON",
    "severity": "LOW",
    "track_id": 12,
    "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
    "confidence": 0.75
  },
  {
    "event_type": "ZONE_INTRUSION",
    "object_type": "PERSON",
    "severity": "LOW",
    "track_id": 13,
    "bbox": { "x1": 220, "y1": 40, "x2": 360, "y2": 300 },
    "confidence": 0.71
  }
]
```

Code Mapping (runtime repo)
---------------------------
- Mock/real builders: `be-ai-endpoint/src/ai/pipeline/events.py`
- Model adapter interface: `be-ai-endpoint/src/ai/pipeline/model_adapter.py`
- Dummy payload schema: `be-ai-endpoint/src/ai/events/schema.py`
- Builder wiring: `be-ai-endpoint/src/ai/pipeline/__main__.py`

## 한국어
목적
-----
이 문서는 모델/트래커 연동을 위한 최소 출력 계약을 정의한다.
모크 모드는 파이프라인 검증 기본값이며, 모델이 제공되면 실제 어댑터를
사용할 수 있다. 페이로드 구조는 안정적으로 유지한다.

이벤트 출력 계약
----------------
처리된 각 프레임은 0개 이상의 이벤트 페이로드를 생성해야 하며 필드는 아래와 같다.
빌더는 단일 dict 또는 dict 리스트를 반환할 수 있다.

- `event_id` (uuid 문자열)
- `ts` (ISO-8601 문자열)
- `site_id` (문자열)
- `camera_id` (문자열)
- `event_type` (enum 문자열)
- `object_type` (enum 문자열)
- `severity` (enum 문자열)
- `track_id` (정수 또는 null)
- `bbox` (`{x1,y1,x2,y2}` 정수)
- `confidence` (0..1 실수)
- `zone` (`{zone_id, inside}`)는 zone이 활성화된 경우 파이프라인에서 주입
- `snapshot_path` (문자열 또는 null)

모델/트래커 출력(최소)
----------------------
모델 또는 트래커는 아래 값을 제공해야 한다:

- `bbox`
- `confidence`
- `track_id` (PERSON은 필수. 트래커가 없으면 합성 id를 사용)
- `event_type`
- `object_type`
- `severity`

매핑 규칙
---------
- 모델이 여러 detection을 반환하면 detection 당 이벤트 1개를 발행한다.
- `event_id`, `ts`, `site_id`, `camera_id`는 빌더/어댑터 레이어가 할당한다.
- `zone`은 파이프라인에서 `bbox`와 `event_type`로 평가한다.
- `snapshot_path`는 스냅샷 활성화 + 저장 성공 시에만 파이프라인이 주입한다.

모크 빌더
---------
- 기본 모드: `model.mode=mock`
- 파이프라인 검증을 위한 결정적 더미 이벤트를 생성한다.
  - `model.mode=real`은 실제 어댑터가 필요하며, 없으면 에러로 중단된다.

실제 모델 연동(지원됨)
---------------------
빌더/어댑터를 구현하거나 연결한다:

1. `frame`에 대해 추론 수행
2. detection을 페이로드 계약으로 변환
3. 하위 emitter에 전달할 payload dict를 반환

범위 및 제약(초안)
------------------
1) 현재 프로토콜 v0.2는 PERSON/FIRE/SMOKE + PPE/POSTURE/HAZARD(초안)을 포함한다.
2) 그 외 신규 클래스는 프로토콜 업데이트가 선행되어야 한다.
3) 요구 클래스와 FPS를 만족하면 단일 모델도 허용.
4) 복수 모델도 허용하며, 어댑터가 프레임 단위로 병합 가능.

초기 기준 모델(사전학습)
------------------------
초기 연동 단계에서는 사전학습 YOLO 모델을 사용하고, 제한된 클래스
(예: PERSON)로 파이프라인을 먼저 검증한다.

노트
-----
- 사전학습 COCO 모델은 연기/화재/PPE/자세 클래스가 없는 경우가 많다.
- 빌더에 클래스 매핑 테이블을 두어 모델 클래스 →
  `event_type`/`object_type`/`severity`로 변환한다.
- 트래킹이 없으면 어댑터에서 detection마다 합성 `track_id`를 부여해야 한다
  (PERSON은 필수).
- 기준 트래커: `TRACKER_TYPE=iou`로 간단 IoU 트래킹을 활성화할 수 있다.
- 런타임 어댑터 선택은 `AI_MODEL_ADAPTER`를 사용한다.
- 복수 모델은 콤마로 구분하여 지정한다(예: `a:AdapterA,b:AdapterB`).
- 선택 클래스 매핑: `MODEL_CLASS_MAP_PATH`로 yaml을 지정한다(초안: `configs/model_class_map.yaml`).
- 커스텀 어댑터 템플릿은 런타임 레포에 있다:
  `be-ai-endpoint/src/ai/vision/custom_adapter.py`.
- ONNX 기준 어댑터(런타임 레포): `be-ai-endpoint/src/ai/vision/onnx_adapter.py`.

모크 입출력 예시
---------------
입력(프레임 메타데이터, 단순화)
```json
{ "frame_idx": 12, "camera_id": "cam01", "ts": "2026-02-05T14:00:01+09:00" }
```

출력(단일 detection)
```json
{
  "event_type": "ZONE_INTRUSION",
  "object_type": "PERSON",
  "severity": "LOW",
  "track_id": 12,
  "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
  "confidence": 0.75
}
```

출력(복수 detection)
```json
[
  {
    "event_type": "ZONE_INTRUSION",
    "object_type": "PERSON",
    "severity": "LOW",
    "track_id": 12,
    "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
    "confidence": 0.75
  },
  {
    "event_type": "ZONE_INTRUSION",
    "object_type": "PERSON",
    "severity": "LOW",
    "track_id": 13,
    "bbox": { "x1": 220, "y1": 40, "x2": 360, "y2": 300 },
    "confidence": 0.71
  }
]
```

코드 매핑
---------
- 모크/실제 빌더: `be-ai-endpoint/src/ai/pipeline/events.py`
- 모델 어댑터 인터페이스: `be-ai-endpoint/src/ai/pipeline/model_adapter.py`
- 더미 페이로드 스키마: `be-ai-endpoint/src/ai/events/schema.py`
- 빌더 연결: `be-ai-endpoint/src/ai/pipeline/__main__.py`
