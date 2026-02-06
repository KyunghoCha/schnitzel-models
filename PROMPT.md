# Handoff Prompt (safety-cctv-ai-model)

## English
You are continuing work on the model-training repo for `safety-cctv-ai`.

**Repo purpose**
- Train/evaluate/export models for the runtime pipeline repo: `safety-cctv-ai`
- Keep heavy ML dependencies, datasets, and experiments separate from runtime code

**Current status**
- Repo created and structured with:
  - `configs/`, `datasets/`, `experiments/`, `models/`, `scripts/`, `src/`, `docs/`
- Docs reorganized into:
  - `docs/overview/` (index)
  - `docs/contracts/` (pipeline integration + protocol)
  - `docs/specs/` (model interface, I/O samples, taxonomy)
  - `docs/ops/` (data guidelines, train/eval/export, experiment log, ops/ai/)
- Core docs copied from runtime repo and updated paths
 - Runtime repo code-mapping references normalized to `safety-cctv-ai/...`

**Working Principles**
- Follow `/home/ckh/CapstoneProjects/PROMPTS` as the execution standard and output template SSOT.
- Apply cross-cutting changes: update code, docs, configs, and tests in the same change-set.
- Prefer root-cause fixes over tactical patches; avoid accumulating technical debt.
- Maintain architectural consistency and long-term maintainability (clean boundaries, explicit contracts).
- Prevent doc/code drift; enforce SSOT alignment.
- Make assumptions explicit; validate when uncertainty exists.
- Preserve repository conventions; avoid ad-hoc structure or path hardcoding.
- Prioritize tests by operational risk (export validation, class mapping, runtime compatibility).
- When adding features, update SSOT first, then implement.
- Before making changes, re-read the relevant files to confirm current state.
- If asked for doc/code alignment, follow the established method: read in full, compare to code, update all related docs/configs/tests, and record changes consistently.

**Key docs to read first**
1. `docs/overview/index.md`
2. `docs/contracts/pipeline_integration.md`
3. `docs/specs/model_interface.md`

**What’s NOT done yet**
- Training/eval/export scripts (only placeholders exist)
- Config templates for training/export
- Any dataset tooling or experiment logging automation

**Immediate next steps**
1. Draft minimal training/eval/export script skeletons in `scripts/`
2. Add base config templates in `configs/`
3. Ensure outputs align with runtime adapters:
   - PT -> `ai.vision.yolo_adapter:YOLOAdapter`
   - ONNX -> `ai.vision.onnx_adapter:ONNXYOLOAdapter`
   - Class map YAML -> `MODEL_CLASS_MAP_PATH`

## 한국어
당신은 `safety-cctv-ai` 런타임 파이프라인용 모델 학습 레포 작업을 이어서 진행합니다.

**레포 목적**
- 런타임 레포(`safety-cctv-ai`)에서 사용할 모델을 학습/평가/export
- 데이터/실험/의존성은 런타임 레포와 분리 관리

**현재 상태**
- 기본 구조 생성 완료:
  - `configs/`, `datasets/`, `experiments/`, `models/`, `scripts/`, `src/`, `docs/`
- 문서 구조 정리 완료:
  - `docs/overview/` (index)
  - `docs/contracts/` (연동 규약 + protocol)
  - `docs/specs/` (model interface, I/O, taxonomy)
  - `docs/ops/` (data/train/experiment/ops 문서)
- 런타임 레포에서 필요한 문서 복사 및 경로 정리 완료

**작업 원칙**
- 실행 표준/출력 템플릿 SSOT는 `/home/ckh/CapstoneProjects/PROMPTS`를 따른다.
- 코드 수정 시 관련 문서/설정/테스트를 동일 체인지셋으로 동시 갱신한다.
- 단기 패치가 아닌 근본 원인 해결을 우선하여 기술부채 누적을 방지한다.
- 아키텍처 일관성 및 장기 유지보수성을 보장한다(경계/계약 명확화).
- 문서-코드 드리프트를 금지하고 SSOT 정합성을 유지한다.
- 가정은 명시하고 불확실성은 검증한다.
- 레포 관례/구조를 유지하고 임의 구조/경로 하드코딩을 지양한다.
- 테스트는 운영 리스크 중심(Export 검증/클래스 매핑/런타임 호환성)으로 우선순위화한다.
- 기능 추가 시 SSOT 업데이트를 선행한 뒤 구현한다.
- 변경 전 관련 파일을 다시 읽어 최신 상태를 확인한다.
- 문서-코드 정합성 요청 시 기존 방식대로: 문서 정독 → 코드 비교 → 관련 문서/설정/테스트 동시 갱신 → 일관성 기록.

**우선 읽을 문서**
1. `docs/overview/index.md`
2. `docs/contracts/pipeline_integration.md`
3. `docs/specs/model_interface.md`

**아직 안 한 것**
- 학습/평가/export 스크립트 작성
- 학습/export 기본 설정 템플릿
- 데이터셋/실험 자동화

**다음 단계**
1. `scripts/`에 train/eval/export 기본 골격 추가
2. `configs/`에 베이스 설정 템플릿 추가
3. 런타임 어댑터 호환성 유지
   - PT -> `ai.vision.yolo_adapter:YOLOAdapter`
   - ONNX -> `ai.vision.onnx_adapter:ONNXYOLOAdapter`
   - 클래스 매핑 YAML -> `MODEL_CLASS_MAP_PATH`
