# Model I/O Samples

## English
Purpose
-------
Provide stable input/output samples for adapter implementation and tests.

Input (frame metadata only)
---------------------------
```json
{
  "frame_idx": 12,
  "camera_id": "cam01",
  "ts": "2026-02-05T14:00:01+09:00",
  "shape": [1080, 1920, 3]
}
```

Detection Output (single)
-------------------------
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

Detection Output (multi)
------------------------
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
    "event_type": "PPE_VIOLATION",
    "object_type": "PERSON",
    "severity": "MEDIUM",
    "track_id": 12,
    "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
    "confidence": 0.70
  },
  {
    "event_type": "FIRE_DETECTED",
    "object_type": "FIRE",
    "severity": "HIGH",
    "track_id": null,
    "bbox": { "x1": 220, "y1": 40, "x2": 360, "y2": 300 },
    "confidence": 0.71
  }
]
```

Notes
-----
1. `event_type`/`object_type` must follow `docs/contracts/protocol.md`.
2. `bbox` is pixel coordinates in frame space.

## 한국어
목적
-----
어댑터 구현과 테스트에 사용할 입력/출력 샘플을 제공한다.

입력(프레임 메타데이터)
-----------------------
```json
{
  "frame_idx": 12,
  "camera_id": "cam01",
  "ts": "2026-02-05T14:00:01+09:00",
  "shape": [1080, 1920, 3]
}
```

Detection 출력(단일)
-------------------
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

Detection 출력(복수)
-------------------
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
    "event_type": "PPE_VIOLATION",
    "object_type": "PERSON",
    "severity": "MEDIUM",
    "track_id": 12,
    "bbox": { "x1": 10, "y1": 20, "x2": 200, "y2": 260 },
    "confidence": 0.70
  },
  {
    "event_type": "FIRE_DETECTED",
    "object_type": "FIRE",
    "severity": "HIGH",
    "track_id": null,
    "bbox": { "x1": 220, "y1": 40, "x2": 360, "y2": 300 },
    "confidence": 0.71
  }
]
```

노트
-----
1. `event_type`/`object_type`는 `docs/contracts/protocol.md`를 따른다.
2. `bbox`는 프레임 픽셀 좌표 기준이다.
