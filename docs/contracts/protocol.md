# Event Protocol v0.2 (Person + Fire/Smoke + PPE/Posture/Hazard)

## English
Common Rules
------------
### Coordinate System
- All coordinates are pixel coordinates in the video frame
- Origin `(0,0)` is **top-left**
- `x` increases to the right, `y` increases downward
- Example: `(120,80)` means 120px from left, 80px from top

### Zone Inside Rule (common)
- `inside=true` is decided by computing a **rule_point** per `event_type`, then checking if it is inside the zone polygon
- rule_point:
  - **Person intrusion (`ZONE_INTRUSION`, `object_type=PERSON`)**
    `bottom_center = ((x1+x2)/2, y2)`
  - **Fire/Smoke (`FIRE_DETECTED`, `SMOKE_DETECTED`, `object_type=FIRE|SMOKE`)**
    `bbox_center = ((x1+x2)/2, (y1+y2)/2)` *(recommended)*

> Note: The team may unify all types to bottom_center, but bbox_center is more natural for fire/smoke.

---

## 1) Event JSON Schema (AI -> Backend)
### Field summary
- **Required**: `event_id`, `ts`, `site_id`, `camera_id`, `event_type`, `severity`, `bbox`, `confidence`, `zone`
- **Conditional**:
  - `track_id`: **required** for `object_type=PERSON`, **optional** for FIRE/SMOKE
  - `object_type`: **recommended (effectively required)** to simplify frontend/IoT
  - `snapshot_path`: **required when snapshot is enabled and saved successfully**; otherwise null/omitted

### Example 1) Person Zone Intrusion
```jsonc
{
  "event_id": "2f7f3e6a-3c0e-4f3b-9a2e-5f1d7d0b9f3a",
  // Unique event ID (typically UUID)

  "ts": "2026-01-28T14:03:21+09:00",
  // Event time (ISO-8601). +09:00 is KST.
  // Recommended: frame capture time

  "site_id": "S001",
  // Site ID

  "camera_id": "C012",
  // Camera ID

  "event_type": "ZONE_INTRUSION",
  // Enum: ZONE_INTRUSION | FIRE_DETECTED | SMOKE_DETECTED | PPE_VIOLATION | POSTURE_ALERT | HAZARD_ALERT

  "object_type": "PERSON",
  // Enum: PERSON | FIRE | SMOKE | UNKNOWN

  "severity": "HIGH",
  // Severity: LOW/MEDIUM/HIGH/CRITICAL (team decision)

  "track_id": 37,
  // Track ID (required for PERSON)

  "bbox": { "x1": 120, "y1": 80, "x2": 260, "y2": 410 },
  // Bounding box (pixels)

  "confidence": 0.91,
  // Confidence (0~1)

  "zone": { "zone_id": "Z3", "inside": true },
  // Zone result

  "snapshot_path": "snapshots/S001/C012/20260128_140321_37.jpg"
  // Snapshot path/key
}
```

### Example 2) Fire Detected
```jsonc
{
  "event_id": "7a9c9f2b-8d7f-4a6a-9a4c-4b2b2e1f0c21",
  "ts": "2026-01-28T14:03:21+09:00",
  "site_id": "S001",
  "camera_id": "C012",

  "event_type": "FIRE_DETECTED",
  "object_type": "FIRE",

  "severity": "CRITICAL",

  "bbox": { "x1": 430, "y1": 210, "x2": 560, "y2": 390 },
  "confidence": 0.88,

  "zone": { "zone_id": "Z3", "inside": true },

  "snapshot_path": "snapshots/S001/C012/20260128_140321_fire.jpg"

  // track_id is optional for FIRE/SMOKE
}
```

> Note: JSON with comments is shown as `jsonc`. Actual payload must be plain JSON.

> ⚠️ Current scope notes:
> - Mock mode emits PERSON-only dummy events for pipeline validation.
> - Real model adapters exist, but production accuracy/coverage is not validated yet.
> - Backend POST integration is supported in code, but real backend availability is environment-dependent.

---

## 2) Zone Polygon Format (Frontend/Backend/AI)
```jsonc
{
  "zone_id": "Z3",
  // Zone ID

  "site_id": "S001",
  // Site ID

  "camera_id": "C012",
  // Camera ID

  "name": "restricted_area_1",
  // Display name

  "zone_type": "restricted",
  // Example enum: restricted/danger/warning

  "polygon": [[120,80],[500,90],[520,400],[140,420]],
  // List of polygon vertices ([x,y] pixels)

  "enabled": true
  // Enabled flag (false => AI ignores)
}
```

---

## 3) Backend APIs
### GET zones
- **GET /api/sites/S001/cameras/C012/zones**
  - Returns zone list for a site/camera

Response example:
```jsonc
[
  {
    "zone_id": "Z3",
    "camera_id": "C012",
    "zone_type": "restricted",
    "polygon": [[120,80],[500,90],[520,400],[140,420]],
    "enabled": true
  }
]
```

### POST events
- **POST /api/events**
  - AI event submission endpoint

Response example:
```json
{ "ok": true }
```

---

## 4) Stream Standard (initial fixed values)
- Protocol: RTSP
- Codec: H.264
- Resolution: 1280x720
- FPS: 15

> ⚠️ Not enforced in code:
> The current pipeline accepts arbitrary RTSP stream settings; these are
> intended as initial deployment targets only.

RTSP example:
- `rtsp://user:pass@192.168.0.10:554/stream1`

---

## v0.2 Decision Items (recommended)
- Fix `ts` as **frame capture time**?
- Fix fire/smoke rule_point as **bbox_center**?

## Implementation Notes (current code)
- Mock mode emits `ZONE_INTRUSION` + `object_type=PERSON` with `severity=LOW`.
- FIRE/SMOKE/PPE/POSTURE/HAZARD types require a model adapter + class map configuration.

Code Mapping (runtime repo)
---------------------------
- Event payload: `be-ai-endpoint/src/ai/events/schema.py`, `be-ai-endpoint/src/ai/pipeline/events.py`
- Zones/rule_point: `be-ai-endpoint/src/ai/rules/zones.py`
- Backend POST: `be-ai-endpoint/src/ai/clients/backend_api.py`

---

## 한국어
공통 규칙
---------
### 좌표 기준
- 모든 좌표는 영상 프레임의 픽셀 좌표
- 원점 `(0,0)`은 **좌상단**
- `x`는 오른쪽, `y`는 아래로 증가
- 예: `(120,80)`은 왼쪽 120px, 위 80px

### Zone inside 판정(공통)
- `inside=true`는 event_type별 **rule_point**를 계산한 뒤, 그 점이 zone polygon 내부면 true
- rule_point:
  - **사람 침입(`ZONE_INTRUSION`, `object_type=PERSON`)**
    `bottom_center = ((x1+x2)/2, y2)`
  - **화재/연기(`FIRE_DETECTED`, `SMOKE_DETECTED`, `object_type=FIRE|SMOKE`)**
    `bbox_center = ((x1+x2)/2, (y1+y2)/2)` *(권장)*

> 참고: 모든 타입을 bottom_center로 통일할 수도 있으나, 화재/연기는 bbox_center가 더 자연스럽다.

---

## 1) 이벤트 JSON 스키마 (AI -> 백엔드)
### 필드 요약
- **필수**: `event_id`, `ts`, `site_id`, `camera_id`, `event_type`, `severity`, `bbox`, `confidence`, `zone`
- **조건부**:
  - `track_id`: `object_type=PERSON`이면 **필수**, FIRE/SMOKE는 **선택**
  - `object_type`: **권장(사실상 필수)**, 프론트/IoT 단순화를 위해 필요
  - `snapshot_path`: 스냅샷 활성화 + 저장 성공 시 **필수**, 아니면 null/미포함

### 예시 1) 사람 Zone 침입
```jsonc
{
  "event_id": "2f7f3e6a-3c0e-4f3b-9a2e-5f1d7d0b9f3a",
  // 이벤트 고유 ID (보통 UUID)

  "ts": "2026-01-28T14:03:21+09:00",
  // 이벤트 시각(ISO-8601). +09:00은 KST
  // 권장: 프레임 캡처 시각

  "site_id": "S001",
  // 현장/시설 ID

  "camera_id": "C012",
  // 카메라 ID

  "event_type": "ZONE_INTRUSION",
  // 이벤트 종류(enum)

  "object_type": "PERSON",
  // 감지 대상(enum)

  "severity": "HIGH",
  // 심각도 (LOW/MEDIUM/HIGH/CRITICAL 등 팀 합의)

  "track_id": 37,
  // 추적 ID (PERSON에서는 필수)

  "bbox": { "x1": 120, "y1": 80, "x2": 260, "y2": 410 },
  // 바운딩 박스(픽셀)

  "confidence": 0.91,
  // 신뢰도(0~1)

  "zone": { "zone_id": "Z3", "inside": true },
  // zone 결과

  "snapshot_path": "snapshots/S001/C012/20260128_140321_37.jpg"
  // 스냅샷 경로/키
}
```

### 예시 2) 화재 감지(불꽃)
```jsonc
{
  "event_id": "7a9c9f2b-8d7f-4a6a-9a4c-4b2b2e1f0c21",
  "ts": "2026-01-28T14:03:21+09:00",
  "site_id": "S001",
  "camera_id": "C012",

  "event_type": "FIRE_DETECTED",
  "object_type": "FIRE",

  "severity": "CRITICAL",

  "bbox": { "x1": 430, "y1": 210, "x2": 560, "y2": 390 },
  "confidence": 0.88,

  "zone": { "zone_id": "Z3", "inside": true },

  "snapshot_path": "snapshots/S001/C012/20260128_140321_fire.jpg"

  // track_id는 FIRE/SMOKE에서는 선택
}
```

> 참고: 주석 포함 JSON은 `jsonc` 표기. 실제 전송은 주석 없는 JSON.

> ⚠️ 현재 범위 안내:
> - mock 모드는 파이프라인 검증용 PERSON 더미만 전송한다.
> - 실제 모델 어댑터는 존재하지만, 운영 수준 정확도/커버리지는 미검증이다.
> - 백엔드 POST 연동은 코드로 지원되며, 실제 백엔드 가용성은 환경에 따라 다르다.

---

## 2) Zone 폴리곤 포맷 (프론트/백엔드/AI)
```jsonc
{
  "zone_id": "Z3",
  // zone 고유 ID

  "site_id": "S001",
  // 현장 ID

  "camera_id": "C012",
  // 카메라 ID

  "name": "restricted_area_1",
  // 표시용 이름

  "zone_type": "restricted",
  // zone 분류(enum)

  "polygon": [[120,80],[500,90],[520,400],[140,420]],
  // 다각형 꼭짓점 목록([x,y] 픽셀)

  "enabled": true
  // 활성 여부(false면 AI는 무시)
}
```

---

## 3) 백엔드 API 2개
### GET zones
- **GET /api/sites/S001/cameras/C012/zones**
  - 특정 site/camera의 zone 목록 조회

응답 예시:
```jsonc
[
  {
    "zone_id": "Z3",
    "camera_id": "C012",
    "zone_type": "restricted",
    "polygon": [[120,80],[500,90],[520,400],[140,420]],
    "enabled": true
  }
]
```

### POST events
- **POST /api/events**
  - AI 이벤트 전송(저장/알림/프론트 전달/IoT 연동)

응답 예시:
```json
{ "ok": true }
```

---

## 4) 스트림 표준 (초기 고정값)
- 프로토콜: RTSP
- 코덱: H.264
- 해상도: 1280x720
- FPS: 15

> ⚠️ 코드에서 강제하지 않음:
> 현재 파이프라인은 임의 스트림을 허용하며, 위 값은 초기 운영 목표 값이다.

RTSP URL 예시:
- `rtsp://user:pass@192.168.0.10:554/stream1`

---

## v0.2 결정 항목(권장)
- `ts` 기준: 프레임 캡처 시각으로 고정할지?
- 화재/연기의 rule_point: bbox_center로 고정할지?

## 구현 메모(현 코드)
- mock 모드는 `ZONE_INTRUSION` + `object_type=PERSON`, `severity=LOW`만 발행한다.
- FIRE/SMOKE/PPE/POSTURE/HAZARD 타입은 모델 어댑터 + 클래스 매핑 설정이 필요하다.

코드 매핑(런타임 레포)
---------------------
- 이벤트 페이로드: `be-ai-endpoint/src/ai/events/schema.py`, `be-ai-endpoint/src/ai/pipeline/events.py`
- Zone/rule_point: `be-ai-endpoint/src/ai/rules/zones.py`
- 백엔드 POST: `be-ai-endpoint/src/ai/clients/backend_api.py`
