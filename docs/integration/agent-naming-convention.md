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
| **Stage 5** | `implementer-dna` | Wrapper (SPARK) | DNA 시스템 구현 |
| **Stage 6** | `documenter-dna` | Wrapper (SPARK) | 표준 문서화 |
| **Stage 7** | `designer-dna` | Wrapper (SPARK) | 청사진 작성 |
| **Stage 8** | `analyzer-dna` | Wrapper (SPARK) | 작업 분해 |
| **Stage 9** | `qc-dna` | Wrapper (SPARK) | 거버넌스 |

---

## Wrapping 전략 (Stage 5-9)

Stage 5-9의 DNA 에이전트는 SPARK 에이전트를 **내부적으로 호출**합니다.

### 예시: implementer-dna

```markdown
# dna-plugin/agents/implementer-dna.md
---
name: implementer-dna
description: DNA Stage 5 - DNA 시스템 구현 (SPARK implementer-spark 활용)
tools: Task, Read, Write, Bash
---

You are a DNA Stage 5 implementation specialist.

## Core Identity

You orchestrate DNA System implementation by delegating to SPARK's implementer-spark.

## Workflow

**Phase 1: Context Loading**
- Read docs/context/stage4_output.json
- Extract 11 DNA System specs

**Phase 2: SPARK Delegation**
```python
Task("implementer-spark", f"""
프로젝트: {project_name}
작업: DNA 시스템 구현

11개 시스템:
{systems_from_stage4}

참고 표준:
- docs/context/stage3_output.json (ADRs)
- docs/context/stage6_output.json (Standards)
""")
```

**Phase 3: Validation**
- SPARK 완료 확인
- Stage 5 산출물 검증
- docs/context/stage5_output.json 저장
```

---

## Commands에서 호출

```markdown
# Stage 1 실행
/dna:stage1

# 내부적으로:
Task("classifier-dna", "...")

---

# Stage 5 실행
/dna:stage5

# 내부적으로:
Task("implementer-dna", "...")
  └─> Task("implementer-spark", "...")  # SPARK 위임
```

---

## 장점

### 1. 완전한 통일성
✅ 사용자는 DNA 에이전트만 알면 됨
✅ `/dna:stage1` ~ `/dna:stage9` 일관된 경험
✅ SPARK 의존성은 내부 구현 디테일

### 2. 독립적 발전
✅ DNA: 방법론 + Skills 세밀화
✅ SPARK: Traits + Role 연구
✅ 각자의 진화 경로

### 3. 명확한 책임
✅ `-dna`: 방법론 프레임워크
✅ `-spark`: 범용 에이전트 시스템
✅ 네이밍만으로 소속 파악

---

## 파일 구조

```bash
dna-plugin/agents/
├── classifier-dna.md         # Stage 1 (신규)
├── investigator-dna.md       # Stage 2 (신규)
├── decision-maker-dna.md     # Stage 3 (신규)
├── planner-dna.md            # Stage 4 (신규)
├── implementer-dna.md        # Stage 5 (Wrapper)
├── documenter-dna.md         # Stage 6 (Wrapper)
├── designer-dna.md           # Stage 7 (Wrapper)
├── analyzer-dna.md           # Stage 8 (Wrapper)
└── qc-dna.md                 # Stage 9 (Wrapper)
```

---

**최종 결정**: 모든 에이전트 `-dna` 접미사 사용
**Wrapping 전략**: Stage 5-9는 SPARK 에이전트 내부 호출
**작성일**: 2025-12-01
**작성자**: Jason & Claude (2호)
