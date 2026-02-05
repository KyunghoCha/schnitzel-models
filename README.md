# safety-cctv-ai-model

## English
**Overview**
This repository is for training, evaluating, and exporting models used by the `safety-cctv-ai` pipeline. It is intentionally separated from the runtime pipeline repo to keep heavy ML dependencies, datasets, and experiments isolated.

**Scope**
- Data preparation and labeling workflow
- Training/evaluation scripts and configs
- Model export (ONNX/PT) for pipeline integration
- Class taxonomy and mapping maintenance

**Docs (SSOT)**
- Pipeline contract: `docs/pipeline_integration.md`
- Model interface: `docs/model_interface.md`
- Model I/O samples: `docs/model_io_samples.md`
- Class taxonomy: `docs/model_class_taxonomy.md`
- Protocol reference: `docs/protocol.md`
- ML ops guides: `docs/ai/`

**Repository Layout**
- `configs/`: training/export configs
- `datasets/`: local data (not committed)
- `experiments/`: experiment logs/artifacts (local)
- `models/`: exported weights (local)
- `scripts/`: training/eval/export scripts
- `src/`: training code
- `docs/`: documentation

**Integration Target**
Exports should be compatible with the runtime pipeline:
- ONNX: used by `ai.vision.onnx_adapter:ONNXYOLOAdapter`
- PT: used by `ai.vision.yolo_adapter:YOLOAdapter`
- Class map YAML: `MODEL_CLASS_MAP_PATH`

## 한국어
**개요**
이 저장소는 `safety-cctv-ai` 파이프라인에서 사용할 모델을 학습/평가/내보내기(export)하기 위한 전용 레포입니다. 모델 학습 의존성과 데이터/실험을 런타임 파이프라인과 분리해 관리합니다.

**범위**
- 데이터 준비 및 라벨링 워크플로우
- 학습/평가 스크립트와 설정
- 파이프라인 연동용 모델 export(ONNX/PT)
- 클래스 분류 체계 및 매핑 유지

**문서(SSOT)**
- 파이프라인 연동 규약: `docs/pipeline_integration.md`
- 모델 인터페이스: `docs/model_interface.md`
- 모델 입출력 샘플: `docs/model_io_samples.md`
- 클래스 분류 체계: `docs/model_class_taxonomy.md`
- 프로토콜 레퍼런스: `docs/protocol.md`
- ML 운영 문서: `docs/ai/`

**저장소 구조**
- `configs/`: 학습/내보내기 설정
- `datasets/`: 로컬 데이터(커밋 제외)
- `experiments/`: 실험 로그/산출물(로컬)
- `models/`: export 결과(로컬)
- `scripts/`: 학습/평가/내보내기 스크립트
- `src/`: 학습 코드
- `docs/`: 문서

**연동 대상**
런타임 파이프라인과 아래 형식으로 연결됩니다:
- ONNX: `ai.vision.onnx_adapter:ONNXYOLOAdapter`
- PT: `ai.vision.yolo_adapter:YOLOAdapter`
- 클래스 매핑 YAML: `MODEL_CLASS_MAP_PATH`
