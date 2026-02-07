# pipeline_spec

## English

Pipeline Spec
=============

## Entrypoint

- Module: `ai.pipeline` (package)
- Windows (Recommended): `./setup_env.ps1; python -m ai.pipeline`
- Linux/Manual: `PYTHONPATH=src python -m ai.pipeline`

## Inputs

- **Video**: `data/samples/*.mp4` (default)
- **CLI Overrides**:
  - `--video` (mp4 path; forces file source, fails fast if path does not exist)
  - `--camera-id` (string; fails fast if id is not found in `configs/cameras.yaml`)
  - `--source-type` (file|rtsp|webcam; `--video` + `--source-type rtsp` is invalid)
  - `--camera-index` (int; webcam device index, default 0)
  - `--dry-run` (no backend posts)
  - `--output-jsonl` (write events to file)
  - `--max-events` (limit emitting)
  - `--visualize` (show debug window)

## Config (loaded from `configs/*.yaml` if present)

- `app.site_id` -> event site_id
- `app.timezone` -> event ts timezone
- `ingest.fps_limit` -> downsample FPS
- `events.post_url` -> backend endpoint
- `events.timeout_sec` -> request timeout
- `events.retry.max_attempts` / `events.retry.backoff_sec`
- `events.snapshot.base_dir` / `events.snapshot.public_prefix`
- Snapshots are disabled by default; enable by setting `events.snapshot.base_dir`.
- Multi-camera configs can live in `configs/cameras.yaml` under `cameras:`.
- `zones.*` and `rules.rule_point_by_event_type` control zone loading and inside evaluation.

## Output Payload (dummy, aligned to protocol.md)

- `event_id` (uuid string)
- `ts` (ISO-8601, uses app.timezone when set)
- `site_id` (string)
- `camera_id` (string)
- `event_type` = "ZONE_INTRUSION" (placeholder)
- `object_type` = "PERSON"
- `severity` = "LOW"
- `track_id` (int or null; required for PERSON)
- `bbox` = `{x1,y1,x2,y2}`
- `confidence` = 0.42
- `zone` = `{zone_id, inside}`
- `snapshot_path` = string when snapshot is enabled **and saved**, otherwise null

## Multi-Event Support

- Builder may return a single payload dict or a list of payload dicts.
- The pipeline emits each payload in order.

## Model Integration (mock-first)

- `configs/default.yaml` -> `model.mode`
  - `mock`: uses `MockModelEventBuilder` (deterministic placeholder)
  - `real`: requires a real model adapter; raises error if adapter is not provided
- Model/Tracker outputs must map to the same payload keys:
  - `bbox`, `confidence`, `track_id` (required for PERSON; synthetic if no tracker),
    `event_type`, `object_type`, `severity`

## Behavior

- Uses OpenCV to read frames
- Samples frames based on FPS limit
- Sampling uses a rate-based selector to avoid overshooting target FPS
- Mock builder (mock mode) emits one dummy event per processed frame when dedup is disabled
- Real builder may return 0..N events per frame (list)
- If backend host is not resolvable, it falls back to stdout (dry-run)
- Invalid camera id fails fast at startup
- Invalid timezone falls back to UTC
- For RTSP sources, read failures trigger retry with backoff+jitter
  - If `rtsp.max_attempts` is set and exceeded, the source disables reconnect and the pipeline stops.
- After a successful RTSP reconnect, the pipeline applies a short 0.2s delay to avoid a tight loop.
- Logs to `outputs/logs/`
  - Log rotation is enabled: `AI_LOG_MAX_BYTES` (default 10MB), `AI_LOG_BACKUP_COUNT` (default 5)
  - Runtime override: `AI_LOG_LEVEL`, `AI_LOG_FORMAT` (plain or json)
  - Config override: `AI_LOGGING_LEVEL`, `AI_LOGGING_FORMAT`
  - Metrics/heartbeat use dedicated loggers (`ai.metrics`, `ai.heartbeat`)
  - Event metric increments only on successful emit; failures increment errors
  - Heartbeat payload includes `last_frame_age_sec`
- `max-events` counts successful emits only
- `--visualize` shows a debug window with bounding boxes
- `model.mode=real` requires `AI_MODEL_ADAPTER=module:ClassName`
- Multiple adapters can be set with a comma-separated list.
- `MODEL_CLASS_MAP_PATH` can provide class-to-event mapping (optional).
- `AI_MODEL_MODE` can override `model.mode` at runtime

## Mock Backend

- Run: `python -m ai.pipeline.mock_backend`
- Listens on `0.0.0.0:8080` and accepts `POST /api/events`
- Optional: override port via `MOCK_BACKEND_PORT` (e.g., `MOCK_BACKEND_PORT=18080`)

## Run Examples

1. Default run (posts to backend):
   - Windows: `./setup_env.ps1; python -m ai.pipeline`
   - Linux: `PYTHONPATH=src python -m ai.pipeline`

2. Dry run (no backend posts):
   - Windows: `./setup_env.ps1; python -m ai.pipeline --dry-run --max-events 5`
   - Linux: `PYTHONPATH=src python -m ai.pipeline --dry-run --max-events 5`

## Notes

- If backend is not running, you will see retry warnings.
- Replace `build_dummy_event` when real AI inference is ready.

## Code Mapping

- Entrypoint/CLI: `src/ai/pipeline/__main__.py`
- Pipeline core: `src/ai/pipeline/core.py`
- Event builders: `src/ai/pipeline/events.py`
- Config loader: `src/ai/pipeline/config.py`, `src/ai/config.py`
- Sources: `src/ai/pipeline/sources/` (package: `file.py`, `rtsp.py`, `webcam.py`)
- Sampler: `src/ai/pipeline/sampler.py`
- Visualizer: `src/ai/vision/visualizer.py`
- Emitters/backend: `src/ai/pipeline/emitter.py`, `src/ai/clients/backend_api.py`

---

## 한국어

파이프라인 명세
==============

## 엔트리포인트

- 모듈: `ai.pipeline` (패키지)
- 윈도우 (권장): `./setup_env.ps1; python -m ai.pipeline`
- 리눅스/수동: `PYTHONPATH=src python -m ai.pipeline`

## 입력

- **비디오**: `data/samples/*.mp4` (기본값)
- **CLI 오버라이드**:
  - `--video` (mp4 경로; 파일 소스로 강제하며, 경로가 없으면 즉시 종료)
  - `--camera-id` (문자열; `configs/cameras.yaml`에 없으면 즉시 종료)
  - `--source-type` (file|rtsp|webcam; `--video`와 `--source-type rtsp` 조합은 불가)
  - `--camera-index` (정수; 웹캠 장치 인덱스, 기본값 0)
  - `--dry-run` (백엔드 전송 안 함)
  - `--output-jsonl` (이벤트를 파일에 기록)
  - `--max-events` (전송 이벤트 수 제한)
  - `--visualize` (디버그 시각화 창 표시)

## 설정 (`configs/*.yaml`에서 로드)

- `app.site_id` -> 이벤트 site_id
- `app.timezone` -> 이벤트 ts 타임존
- `ingest.fps_limit` -> 다운샘플링 FPS
- `events.post_url` -> 백엔드 엔드포인트
- `events.timeout_sec` -> 요청 타임아웃
- `events.retry.max_attempts` / `events.retry.backoff_sec`
- `events.snapshot.base_dir` / `events.snapshot.public_prefix`
- 스냅샷은 기본적으로 비활성화되어 있으며, `events.snapshot.base_dir` 설정 시 활성화됨.
- 멀티 카메라 설정은 `configs/cameras.yaml`의 `cameras:` 항목 아래에 위치할 수 있음.
- `zones.*` 및 `rules.rule_point_by_event_type`이 구역 로딩 및 내부 판정을 제어함.

## 출력 페이로드 (더미, protocol.md 준수)

- `event_id` (uuid 문자열)
- `ts` (ISO-8601, app.timezone 설정 사용)
- `site_id` (문자열)
- `camera_id` (문자열)
- `event_type` = "ZONE_INTRUSION" (더미)
- `object_type` = "PERSON"
- `severity` = "LOW"
- `track_id` (정수 또는 null; PERSON의 경우 필수)
- `bbox` = `{x1,y1,x2,y2}`
- `confidence` = 0.42
- `zone` = `{zone_id, inside}`
- `snapshot_path` = 스냅샷 활성화 시 저장된 경로 문자열, 아니면 null

## 멀티 이벤트 지원

- 빌더는 단일 페이로드 또는 페이로드 리스트를 반환할 수 있음.
- 파이프라인은 각 페이로드를 순서대로 전송함.

## 모델 연동 (모크 우선)

- `configs/default.yaml` -> `model.mode`
  - `mock`: `MockModelEventBuilder` 사용 (결정적 더미 데이터 생성)
  - `real`: 실제 모델 어댑터 필요; 어댑터 미제공 시 에러 발생
- 모델/트래커 출력은 동일한 페이로드 키를 가져야 함:
  - `bbox`, `confidence`, `track_id` (PERSON 필수), `event_type`, `object_type`, `severity`

## 동작 방식

- OpenCV를 사용하여 프레임 읽기
- FPS 제한에 따른 프레임 샘플링
- 샘플링은 목표 FPS를 초과하지 않도록 비율 기반 선택기 사용
- 모크 빌더는 중복 제거 비활성화 시 프레임당 하나의 더미 이벤트 생성
- 실제 빌더는 프레임당 0..N개의 이벤트 리스트 반환 가능
- 백엔드 호스트 해석 불가 시 stdout으로 폴백 (dry-run)
- 유효하지 않은 카메라 ID는 시작 시 즉시 실패
- 유효하지 않은 타임존은 UTC로 폴백
- RTSP 소스의 경우, 읽기 실패 시 backoff+jitter를 포함한 재시도 수행
  - `rtsp.max_attempts` 초과 시 재연결 중단 및 파이프라인 종료.
- RTSP 재연결 성공 후 타이트 루프 방지를 위해 0.2초 지연 적용.
- 로그는 `outputs/logs/`에 저장
  - 로그 로테이션 활성화: `AI_LOG_MAX_BYTES` (기본 10MB), `AI_LOG_BACKUP_COUNT` (기본 5)
  - 런타임 오버라이드: `AI_LOG_LEVEL`, `AI_LOG_FORMAT` (plain 또는 json)
  - 설정 오버라이드: `AI_LOGGING_LEVEL`, `AI_LOGGING_FORMAT`
  - 메트릭/하트비트는 전용 로거 사용 (`ai.metrics`, `ai.heartbeat`)
  - 이벤트 메트릭은 전송 성공 시에만 증가하며, 실패 시 에러 카운트 증가
  - 하트비트 페이로드에 `last_frame_age_sec` 포함
- `max-events`는 성공적인 전송 횟수만 카운트함
- `--visualize`는 바운딩 박스를 포함한 디버그 창 표시
- `model.mode=real` 사용 시 `AI_MODEL_ADAPTER=module:ClassName` 설정 필요
- 복수 어댑터는 콤마로 구분하여 설정 가능.
- `MODEL_CLASS_MAP_PATH`로 클래스-이벤트 매핑 제공 가능 (옵션).
- `AI_MODEL_MODE`로 실행 시 `model.mode` 오버라이드 가능

## 모크 백엔드

- 실행: `python -m ai.pipeline.mock_backend`
- `0.0.0.0:8080`에서 수신하며 `POST /api/events` 허용
- 옵션: `MOCK_BACKEND_PORT`로 포트 변경 가능

## 실행 예시

1. 기본 실행 (백엔드 전송):
   - 윈도우: `./setup_env.ps1; python -m ai.pipeline`
   - 리눅스: `PYTHONPATH=src python -m ai.pipeline`

2. 드라이런 (백엔드 전송 안 함):
   - 윈도우: `./setup_env.ps1; python -m ai.pipeline --dry-run --max-events 5`
   - 리눅스: `PYTHONPATH=src python -m ai.pipeline --dry-run --max-events 5`

## 참고 사항

- 백엔드가 실행 중이 아니면 재시도 경고가 표시됨.
- 실제 AI 추론이 준비되면 `build_dummy_event`를 교체할 것.

## 코드 매핑

- 엔트리/CLI: `src/ai/pipeline/__main__.py`
- 파이프라인 코어: `src/ai/pipeline/core.py`
- 이벤트 빌더: `src/ai/pipeline/events.py`
- 설정 로더: `src/ai/pipeline/config.py`, `src/ai/config.py`
- 소스: `src/ai/pipeline/sources/` (`file.py`, `rtsp.py`, `webcam.py`)
- 샘플러: `src/ai/pipeline/sampler.py`
- 시각화: `src/ai/vision/visualizer.py`
- 에미터/백엔드: `src/ai/pipeline/emitter.py`, `src/ai/clients/backend_api.py`
