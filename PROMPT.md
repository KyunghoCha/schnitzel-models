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
