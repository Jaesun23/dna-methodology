# DNA 에이전트 네이밍 컨벤션

## 프로젝트 정체성 및 네이밍 전략

### spark-claude
**정체성**: 범용 AI 에이전트 오케스트레이션 시스템
**목적**: Traits + Role 기반 에이전트 연구
**네이밍**: `{역할}-spark`
**예시**: `analyzer-spark`, `implementer-spark`, `designer-spark`

### dna-methodology
**정체성**: AI 협업 개발 프레임워크 (소프트웨어 설계 방법론)
**목적**: 9-Stage 프로세스 + Skills 세밀화
**네이밍**: `{역할}-dna`
**예시**: `classifier-dna`, `investigator-dna`, `planner-dna`

---

## 최종 결정: 완전한 `-dna` 통일

**전략**: 모든 DNA 에이전트는 `-dna` 접미사 사용

### 최종 네이밍

| Stage | 에이전트 이름 | 구현 방식 | 역할 |
|-------|--------------|----------|------|
| **Stage 1** | `classifier-dna` | 신규 | 패밀리 분류 |
| **Stage 2** | `investigator-dna` | 신규 | 환경 제약 조사 |
| **Stage 3** | `decision-maker-dna` | 신규 | ADR 작성 |
| **Stage 4** | `planner-dna` | 신규 | DNA 시스템 계획 |
| **Stage 5** | `implementer-dna` | 복사 (이름 변경) | DNA 시스템 구현 |
| **Stage 6** | `documenter-dna` | 복사 (이름 변경) | 표준 문서화 |
| **Stage 7** | `designer-dna` | 복사 (이름 변경) | 청사진 작성 |
| **Stage 8** | `analyzer-dna` | 복사 (이름 변경) | 작업 분해 |
| **Stage 9** | `qc-dna` | 복사 (이름 변경) | 거버넌스 |

---

## Stage 5-9 에이전트 (복사 및 이름 변경)

**작업 방법**:
1. spark-claude 프로젝트에서 에이전트 파일 복사
2. 파일명: `-spark` → `-dna` 변경
3. YAML frontmatter의 `name` 필드만 변경
4. 나머지 내용 (Traits, Workflow 등) 모두 동일하게 유지

**복사된 에이전트**:
- `implementer-spark.md` → `implementer-dna.md`
- `documenter-spark.md` → `documenter-dna.md`
- `designer-spark.md` → `designer-dna.md`
- `analyzer-spark.md` → `analyzer-dna.md`
- `qc-spark.md` → `qc-dna.md`

---

## 장점

### 1. 완전한 통일성
✅ 모든 Stage에 DNA 에이전트 존재
✅ `/dna:stage1` ~ `/dna:stage9` 일관된 경험
✅ 일관된 `-dna` 네이밍

### 2. 검증된 에이전트 활용
✅ Stage 5-9는 spark-claude의 검증된 에이전트 정의 사용
✅ Traits, Workflow 모두 동일 (이름만 변경)
✅ 안정적이고 신뢰할 수 있는 동작

### 3. 명확한 책임
✅ `-dna`: DNA 방법론 프레임워크
✅ `-spark`: 범용 에이전트 연구
✅ 네이밍만으로 소속 파악

---

## 파일 구조

```bash
dna-plugin/agents/
├── classifier-dna.md         # Stage 1 (신규)
├── investigator-dna.md       # Stage 2 (신규)
├── decision-maker-dna.md     # Stage 3 (신규)
├── planner-dna.md            # Stage 4 (신규)
├── implementer-dna.md        # Stage 5 (복사)
├── documenter-dna.md         # Stage 6 (복사)
├── designer-dna.md           # Stage 7 (복사)
├── analyzer-dna.md           # Stage 8 (복사)
└── qc-dna.md                 # Stage 9 (복사)
```

---

**최종 결정**: 모든 에이전트 `-dna` 접미사 사용
**Stage 5-9**: spark-claude 에이전트 복사 후 이름만 변경
**작성일**: 2025-12-01
**작성자**: Jason & Claude (2호)
