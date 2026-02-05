# Model Class Taxonomy - Spec

## English
Purpose
-------
Define the target detection taxonomy and default mapping to event fields.
This is a *spec* and requires team agreement before implementation.

Core Classes (Phase 1)
----------------------
1. PERSON (required)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: default `LOW`

2. INTRUSION (derived rule)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: use zone policy

3. DANGER_ZONE_ENTRY (derived rule)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: `MEDIUM` (default)

Extended Classes (Phase 2+)
---------------------------
4. PPE (helmet/vest/etc.)
   - event_type: `PPE_VIOLATION` (new)
   - object_type: `PERSON`
   - severity: `LOW`/`MEDIUM`

5. POSTURE (fall/abnormal)
   - event_type: `POSTURE_ALERT` (new)
   - object_type: `PERSON`
   - severity: `MEDIUM`/`HIGH`

6. SMOKE
   - event_type: `SMOKE_DETECTED`
   - object_type: `SMOKE`
   - severity: `MEDIUM`

7. FIRE
   - event_type: `FIRE_DETECTED`
   - object_type: `FIRE`
   - severity: `HIGH`

8. HAZARD_SITUATION (general)
   - event_type: `HAZARD_ALERT` (new)
   - object_type: `UNKNOWN`
   - severity: `MEDIUM`/`HIGH`

Notes
-----
- New event types require updates to `docs/contracts/protocol.md`.
- Class mapping should live in the model adapter or builder layer.
- Severity can be overridden by rule engine.
- Draft mapping file: `configs/model_class_map.yaml` (used by YOLO adapter when `MODEL_CLASS_MAP_PATH` is set).
- Accuracy validation guide: `docs/ops/ai/accuracy_validation.md`.

Status
------
- Draft. Requires team agreement.

## 한국어
목적
-----
탐지 대상 분류와 기본 이벤트 매핑을 정의한다.
이 문서는 *명세*이며, 구현 전에 팀 합의가 필요하다.

핵심 클래스(Phase 1)
--------------------
1. PERSON (필수)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: 기본 `LOW`

2. INTRUSION (룰 기반 파생)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: zone 정책

3. DANGER_ZONE_ENTRY (룰 기반 파생)
   - event_type: `ZONE_INTRUSION`
   - object_type: `PERSON`
   - severity: 기본 `MEDIUM`

확장 클래스(Phase 2+)
---------------------
4. PPE (헬멧/조끼 등)
   - event_type: `PPE_VIOLATION` (신규)
   - object_type: `PERSON`
   - severity: `LOW`/`MEDIUM`

5. POSTURE (낙상/비정상 자세)
   - event_type: `POSTURE_ALERT` (신규)
   - object_type: `PERSON`
   - severity: `MEDIUM`/`HIGH`

6. SMOKE
   - event_type: `SMOKE_DETECTED`
   - object_type: `SMOKE`
   - severity: `MEDIUM`

7. FIRE
   - event_type: `FIRE_DETECTED`
   - object_type: `FIRE`
   - severity: `HIGH`

8. HAZARD_SITUATION (일반 위험상황)
   - event_type: `HAZARD_ALERT` (신규)
   - object_type: `UNKNOWN`
   - severity: `MEDIUM`/`HIGH`

노트
-----
- 신규 event_type은 `docs/contracts/protocol.md` 업데이트가 필요하다.
- 클래스 매핑은 모델 어댑터 또는 빌더 계층에 둔다.
- severity는 룰 엔진에서 재정의 가능.
- 매핑 초안 파일: `configs/model_class_map.yaml` (YOLO 어댑터에서 `MODEL_CLASS_MAP_PATH` 설정 시 사용).
- 정확도 검증 가이드: `docs/ops/ai/accuracy_validation.md`.

상태
-----
- 초안. 팀 합의 필요.
