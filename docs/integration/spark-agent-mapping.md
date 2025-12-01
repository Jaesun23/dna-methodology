# SPARK Agent 매핑 가이드

## 개요

DNA Methodology는 9개 Stage로 구성되며, Stage 5-9에서 SPARK 에이전트를 재사용합니다. 이 문서는 각 Stage와 SPARK 에이전트의 매핑 관계를 정의합니다.

---

## 에이전트 매핑 테이블

| Stage | DNA 에이전트 | 구현 방식 | 원본 | 작업 |
|-------|-------------|----------|------|------|
| **Stage 1** | `classifier-dna` | 신규 | - | 패밀리 분류 (CoD) |
| **Stage 2** | `investigator-dna` | 신규 | - | 환경 제약 조사 |
| **Stage 3** | `decision-maker-dna` | 신규 | - | ADR 작성 |
| **Stage 4** | `planner-dna` | 신규 | - | DNA 시스템 계획 |
| **Stage 5** | `implementer-dna` | 복사 (이름 변경) | `implementer-spark` | DNA 시스템 구현 |
| **Stage 6** | `documenter-dna` | 복사 (이름 변경) | `documenter-spark` | 표준 문서화 |
| **Stage 7** | `designer-dna` | 복사 (이름 변경) | `designer-spark` | 청사진 작성 |
| **Stage 8** | `analyzer-dna` | 복사 (이름 변경) | `analyzer-spark` | 작업 분해 |
| **Stage 9** | `qc-dna` | 복사 (이름 변경) | `qc-spark` | 체크리스트 + 자동화 |

---

## Stage 1-4: DNA 전용 에이전트 (신규 작성)

### Stage 1: System Classifier

**에이전트**: `classifier-dna`
**목표**: 추상적 아이디어 → 고밀도 SRS + 패밀리 결정
**기술**: CoD (Chain of Density), 재귀적 질문

**Traits**:
- **Ambiguity Intolerance**: 모호함 불허, 반드시 구체화 요구
- **Pattern Recognition**: 18개 패밀리 패턴 즉시 인식
- **Evidence-Based**: 검증 사례 기반 결정
- **Systematic Inquiry**: Layer 1-2 체계적 질문

**산출물**:
- 패밀리 코드 (예: A-C-A)
- NFR 우선순위 (1-4순위)
- 핵심 엔티티 5개 이상
- 검증 사례 3개 이상

---

### Stage 2: Constraints Investigator

**에이전트**: `investigator-dna`
**목표**: Layer 3 환경 제약 조사 + 충돌 식별
**기술**: Web Research, ToT (Tree of Thoughts)

**Traits**:
- **Research Excellence**: Context7, WebSearch 능숙한 활용
- **Constraint Awareness**: 기술/팀/인프라 제약 민감성
- **Conflict Detection**: 제약 간 충돌 패턴 발견
- **Solution Oriented**: 충돌 해결안 제시

**산출물**:
- Layer 3 제약 목록 (기술/팀/인프라)
- 충돌 패턴 3개 이상
- 충돌 해결안
- 기술 후보 목록

---

### Stage 3: Architecture Decision Maker

**에이전트**: `decision-maker-dna`
**목표**: Bootstrap ADR 작성 (DB, Cache, Messaging 등)
**기술**: ADR 템플릿, Context7 최신 정보

**Traits**:
- **Decision Clarity**: 결정 배경/이유 명확히 문서화
- **Technology Awareness**: 최신 기술 트렌드 숙지
- **Trade-off Analysis**: 장단점 균형 있는 분석
- **Future Proof**: 확장성/유지보수성 고려

**산출물**:
- Bootstrap ADR 10-20개
- 5 Categories (External, Conflicts, Tech, Data/API, Quality/Security)
- ADR별 Context, Decision, Consequences

---

### Stage 4: DNA System Planner

**에이전트**: `planner-dna`
**목표**: 11개 DNA 시스템 구현 계획 수립
**기술**: 시스템 분해, 의존성 분석

**Traits**:
- **System Thinking**: 전체 시스템 구조 파악
- **Modularity**: 독립적 모듈 설계
- **Interface Design**: 명확한 인터페이스 정의
- **Reusability**: 재사용 가능한 설계

**산출물**:
- 11개 DNA 시스템 스펙
- 각 시스템별 Interface, Implementation Plan
- 의존성 그래프
- 우선순위 순서

---

## Stage 5-9: 복사된 에이전트 (이름 변경)

### Stage 5: DNA System Implementation

**DNA 에이전트**: `implementer-dna`
**원본**: `implementer-spark` (spark-claude)
**역할**: Stage 4 계획에 따라 11개 DNA 시스템 구현

**에이전트 파일**:
- 파일명: `implementer-dna.md`
- 내용: `implementer-spark.md`와 동일
- 변경: YAML `name: implementer-dna`만 수정

---

### Stage 6: Project Standards Documentation

**DNA 에이전트**: `documenter-dna`
**원본**: `documenter-spark` (spark-claude)
**역할**: ADR → DO/DON'T 표준 문서 변환

**에이전트 파일**:
- 파일명: `documenter-dna.md`
- 내용: `documenter-spark.md`와 동일
- 변경: YAML `name: documenter-dna`만 수정

---

### Stage 7: Blueprint Design

**DNA 에이전트**: `designer-dna`
**원본**: `designer-spark` (spark-claude)
**역할**: 완전한 청사진 작성 (환경 제외 모든 것)

**에이전트 파일**:
- 파일명: `designer-dna.md`
- 내용: `designer-spark.md`와 동일
- 변경: YAML `name: designer-dna`만 수정

---

### Stage 8: Task Breakdown

**DNA 에이전트**: `analyzer-dna`
**원본**: `analyzer-spark` (spark-claude)
**역할**: 청사진 → 독립 실행 가능한 레고블럭으로 분해

**에이전트 파일**:
- 파일명: `analyzer-dna.md`
- 내용: `analyzer-spark.md`와 동일
- 변경: YAML `name: analyzer-dna`만 수정

---

### Stage 9: Governance & Automation

**DNA 에이전트**: `qc-dna`
**원본**: `qc-spark` (spark-claude)
**역할**: 체크리스트 작성 + Pre-commit hooks 설정

**에이전트 파일**:
- 파일명: `qc-dna.md`
- 내용: `qc-spark.md`와 동일
- 변경: YAML `name: qc-dna`만 수정

---

## 의존성 설치

DNA Methodology를 사용하려면 SPARK 플러그인이 먼저 설치되어야 합니다.

### 설치 순서

```bash
# 1. SPARK 플러그인 설치
/plugin install https://github.com/Jaesun23/spark-claude

# 2. DNA 플러그인 설치
/plugin install .

# 3. 프로젝트 시작
/dna:init "주식 거래 플랫폼"
```

### 확인

```bash
# 설치된 플러그인 확인
/plugin list

# 에이전트 확인
/agents list | grep -E "(stage|spark)"
```

---

## 명령어 흐름 예시

```
사용자: /dna:init "주식 거래 플랫폼"
   │
   ▼
/dna:stage1 → classifier-dna (신규)
   │
   ▼
/dna:stage2 → investigator-dna (신규)
   │
   ▼
/dna:stage3 → decision-maker-dna (신규)
   │
   ▼
/dna:stage4 → planner-dna (신규)
   │
   ▼
/dna:stage5 → implementer-dna (복사)
   │
   ▼
/dna:stage6 → documenter-dna (복사)
   │
   ▼
/dna:stage7 → designer-dna (복사)
   │
   ▼
/dna:stage8 → analyzer-dna (복사)
   │
   ▼
/dna:stage9 → qc-dna (복사)
   │
   ▼
완성! 🎉
```

---

## 참고 문서

- **에이전트 정의 구조**: `docs/plugin-guide/agent-definition-structure.md`
- **Stage별 실행 가이드**: `docs/plugin-guide/stage-execution-guide.md`
- **SPARK 저장소**: https://github.com/Jaesun23/spark-claude
- **DNA 가이드**: `docs/guides/00_CORE_METHODOLOGY.md`

---

**작성일**: 2025-12-01
**작성자**: Jason & Claude (2호)
**버전**: 1.0
