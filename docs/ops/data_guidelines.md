# Data Guidelines

## English
**Purpose**
Define data collection and labeling rules so exported models are compatible with the runtime pipeline.

**Scope**
- CCTV video frames for detection tasks
- Labels aligned with `docs/specs/model_class_taxonomy.md`

**Data Rules**
- Use real deployment-like scenes (night, rain, backlight, occlusion)
- Include empty scenes (no event) to reduce false positives
- Balance classes when possible; record imbalance in experiment logs

**Labeling Rules**
- Bounding boxes should tightly cover the target object
- Partial occlusions: label visible parts if object is identifiable
- Keep class names consistent with taxonomy

**Quality Checks**
- Spot-check at least 5% of labels
- Verify class mapping YAML before training

## 한국어
**목적**
수집/라벨 규칙을 정의해 런타임 파이프라인과 호환되는 모델을 만들기 위함입니다.

**범위**
- CCTV 영상 프레임 기반 탐지
- `docs/specs/model_class_taxonomy.md`와 일치하는 라벨

**데이터 규칙**
- 실환경과 유사한 장면 포함(야간, 비, 역광, 가림)
- 이벤트 없는 장면 포함(오탐 감소)
- 클래스 불균형은 실험 로그에 기록

**라벨링 규칙**
- 박스는 대상 객체를 타이트하게 감싸기
- 가림 상태: 식별 가능하면 가시 영역 라벨링
- 클래스 이름은 taxonomy와 동일하게 유지

**품질 점검**
- 최소 5% 라벨 샘플 검수
- 학습 전 class mapping YAML 점검
