# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DNA Methodology v4.0 is a 9-Stage software design framework that overcomes AI context limitations during collaboration. It provides a systematic approach from abstract ideas to production-ready systems.

**DNA**: Like DNA is the foundation of life, the 11 DNA Systems are the foundation of software - the most fundamental systems every project needs.

**Core Problem**: AI context decay (Context Rot) - as conversations grow, initial decisions fade, leading to inconsistency and incomplete implementations.

**Solution Strategy**:
1. **Staged Definition**: Build environment (Stage 1-6) → Execute (Stage 7-9)
2. **Environment Enforcement**: Standards + DNA Systems + Automation ensure consistency
3. **LEGO Block Strategy**: Break work into independent, self-contained units

---

## ⚠️ 프로젝트의 진짜 목표 (IMPORTANT!)

**이 프로젝트는 "아이디어에서 완성된 소프트웨어까지" AI와 함께 만드는 완전한 방법론을 확립하는 것입니다.**

### 현재 상태

```
✅ 검증 완료 (Stage 7-9): Blueprint → Task Breakdown → Checklist → 구현
❌ 연구 필요 (Stage 1-6): 아이디어 → Blueprint 작성
```

### 최우선 과제

**Stage 1-6를 각각 "단위작업"으로 만들기**

- 단위작업 = AI가 한 세션에서 최고 성과를 낼 수 있는 크기
- 명확한 입력과 출력
- 일관성 유지 방법
- 검증 가능

### ⚠️ 중요: Stage의 진짜 의미

**Stage ≠ 한 번의 작업**
**Stage = 여러 세션에 걸친 점진적 누적**

예시:
```
Stage 3 (ADR 작성):
  Session 1: ADR 001-003 작성 📝
  Session 2: ADR 004-006 작성 📝
  Session 3: ADR 007-009 작성 📝
  ...
  결과: 총 20개 ADR 완성
```

각 세션은 "일부분"만 작업하지만, 일관성 유지 (제약조건, 전체 맥락 항상 제공)

### 📖 완전한 컨텍스트

**백지상태의 2호가 이 프로젝트를 이해하려면 반드시 읽어야 할 문서:**

👉 **[docs/DNA_PROJECT_OVERVIEW.md](docs/DNA_PROJECT_OVERVIEW.md)**

이 문서에는 다음이 포함되어 있습니다:
- AI 협업의 6가지 문제점과 해결책
- DNA 방법론의 2가지 핵심 (부분으로 전체 + 환경 제어)
- Stage의 진짜 의미 (여러 세션 누적, 구체적 예시)
- 세 가지 컴포넌트 (Skills/Commands/Agents) 역할
- 9-Stage 구조 상세 설명
- 주식 거래 플랫폼 전체 작업 예시

---

## 9-Stage Process

```
Stage 1: Core Definition (Family Classification)
Stage 2: Environment Constraints (Layer 3 Investigation)
Stage 3: ADR (Architecture Decision Records)
Stage 4: DNA System Planning (11 Common Modules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage 5: DNA System Implementation
Stage 6: Project Standards
Stage 7: Blueprint Creation
Stage 8: Task Breakdown
Stage 9: Governance & Automation
```

## Agent Architecture

DNA Methodology uses 9 specialized agents (all with `-dna` suffix):

### Stage 1-4: New Agents (Not Yet Implemented)
- `classifier-dna` - Family classification using CoD (Chain of Density)
- `investigator-dna` - Environment constraints investigation
- `decision-maker-dna` - ADR authoring with Context7
- `planner-dna` - DNA system planning

### Stage 5-9: Copied from SPARK (Completed)
- `implementer-dna` - DNA system implementation
- `documenter-dna` - Standards documentation
- `designer-dna` - Blueprint creation
- `analyzer-dna` - Task breakdown
- `qc-dna` - Governance & automation

**Note**: Stage 5-9 agents are copied from SPARK Agent System with only the `name` field changed in YAML frontmatter. All Traits, Workflow, and Behavior Protocol remain identical.

## Key Concepts

### 18 Architecture Families

Systems classified by 3-layer decision tree:
- **Layer 1**: Failure Impact (A: Critical, B: Serious, C: Minor)
- **Layer 2**: Data Attributes (A: Structured, B: Semi-structured, C: Unstructured)
- **Layer 3**: Response Time (A: Milliseconds, B: Seconds, C: Minutes/Hours)

Examples:
- **A-A-A**: Financial trading system
- **C-B-B**: Blog platform
- **A-C-A**: Real-time transactions (newly discovered pattern!)

### 11 DNA Systems

Reusable common modules for all projects:
1. Logging (structlog)
2. Configuration (Pydantic)
3. Database (SQLAlchemy)
4. Cache (Redis)
5. Messaging (RabbitMQ)
6. Types (Strong type system)
7. Testing (pytest)
8. Monitoring (Prometheus)
9. Security (Auth/Authorization)
10. Error Handling
11. API Gateway

### Context Rot Prevention (3-Layer Defense)

1. **JSON State**: Store each Stage result in structured files
2. **Context Re-ranking**: Load only relevant context for next Stage
3. **Validation**: Automatic verification at each Stage completion

## Development Workflow

### Plugin Installation

```bash
# 1. Install SPARK plugin (required dependency)
/plugin install https://github.com/Jaesun23/spark-claude

# 2. Install DNA plugin
cd dna-methodology
/plugin install .
```

### Usage Commands

```bash
# Initialize DNA project
/dna:init "Stock Trading Platform"

# Execute stages sequentially
/dna:stage1  # Family classification
/dna:stage2  # Environment constraints
/dna:stage3  # ADR creation
/dna:stage4  # DNA system planning
/dna:stage5  # DNA system implementation
/dna:stage6  # Project standards
/dna:stage7  # Blueprint creation
/dna:stage8  # Task breakdown
/dna:stage9  # Governance & automation
```

**Current Status**: Commands not yet implemented. Only agents for Stage 5-9 are complete.

## File Structure

```
dna-methodology/
├── dna-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   │   ├── implementer-dna.md       ✅ Stage 5
│   │   ├── documenter-dna.md        ✅ Stage 6
│   │   ├── designer-dna.md          ✅ Stage 7
│   │   ├── analyzer-dna.md          ✅ Stage 8
│   │   └── qc-dna.md                ✅ Stage 9
│   │   # Missing: classifier-dna, investigator-dna, decision-maker-dna, planner-dna
│   ├── skills/
│   │   ├── assets/templates/
│   │   └── references/
│   └── commands/                    ❌ Not yet created
├── docs/
│   ├── guides/                      📚 Stage 1-9 methodology guides
│   ├── plugin-guide/                📚 Plugin development guides
│   └── integration/                 📚 SPARK integration docs
└── .claude/
    └── dependencies.json
```

## DNA File Naming Convention

Pattern: `{Stage}{Type}-{Seq}_{descriptive_name}.md`

### Type Codes
- **F** = Function (기능 정의)
- **C** = Classification (분류/분석)
- **D** = Decision (결정 사항)
- **A** = ADR (Architecture Decision Record)
- **B** = Blueprint (청사진)
- **T** = Task (작업 분해)
- **L** = List/Checklist (체크리스트)
- **G** = Guide (간결한 가이드)
- **M** = Manual (상세 해설서)
- **E** = Example/Case (사례집)

Examples:
```
01F-01_core_functions.md          # Stage 1 function definition
02C-01_layer3_constraints.md      # Stage 2 constraints classification
03A-001_logging.md                # Stage 3 ADR (Bootstrap #1)
07B-01_blueprint.md               # Stage 7 blueprint
09L-001_task1_checklist.md        # Stage 9 checklist for task 1
```

## DNA 방법론 4대 핵심 원칙 (2025-12-03 확정)

### 1. AI 최적 크기 (AI Optimal Size)
**"AI가 가장 잘 작업을 수행할 크기로 작업을 하게 한다"**

- **핵심**: 80-90K 토큰 = 100-150줄 체크리스트
- **의미**: DNA 방법론 전체의 근본 원칙
- **구현**: Stage 8이 이를 실제로 구현하는 변환점 (Blueprint → Tasks)
- **판단 기준**:
  - 체크리스트 예상 줄 수: 100-150줄
  - 예상 시간은 부차적 (2-4시간은 참고용, AI가 빨리 끝낼 수 있음)

### 2. 완전해질 때까지 반복 (Repeat Until Complete)
**"부족하면 반복해서 부족함이 없어질 때까지"**

- **핵심**: 절대 불완전한 채로 다음 단계로 가지 않음
- **프로세스**: 검증 → 실패 → 수정 → 재검증
- **3단계 검증**:
  1. Task 크기 검증
  2. 의존성 검증
  3. 완전성 검증

### 3. 기능별 분해 + 연결부 + 조립 (Function-based Assembly)
**"모듈이 크면 기능별로 나누고, 연결부 설계 후 조립"**

- **핵심**: 레이어별 분해 ❌, 기능별 분해 ✅

**잘못된 방식 (레이어별)**:
```
Task 002: Order 엔티티 (Domain만)
Task 007: Order 리포지토리 (Infrastructure만)
Task 008: 주문 생성 서비스 (Application만)
Task 011: Orders API (API만)
```

**올바른 방식 (기능별)**:
```
Task: Order 생성 기능
  - Domain + Application + API + Infrastructure 모두 포함
  - 🔗 연결부: OrderAggregate 기본 구조 정의

Task: Order 체결 기능
  - Domain + Application + API + Infrastructure 모두 포함
  - 🔗 연결부: OrderAggregate 확장 (메서드 추가)

Task: 조립
  - 연결부를 통한 통합
  - 하나의 완전한 모듈로 완성
```

**3단계 전략**:
1. **기능 단위로 분해**: 하나의 모듈 → 여러 기능
2. **연결부 설계**: Base class, interface, extension points
3. **조립**: 연결부를 통해 하나의 모듈로 통합

### 4. 역방향 수정 프로토콜 (Backward Correction Protocol)
**"앞선 결정의 오류 발견 시 → 되돌아가서 수정 → 다시 현재까지 진행"**

#### 핵심 시나리오:
```
Stage 7 (Blueprint) 작성 중...
  ↓
Stage 3 (ADR)의 결정이 잘못되었다는 걸 발견!
  ↓
❌ 잘못: 그냥 넘어가거나 Blueprint에서 임시방편
✅ 올바름: Stage 3로 되돌아가서 ADR 수정
  ↓
Stage 4 → 5 → 6 → 7 다시 진행
  ↓
수정된 ADR이 반영된 올바른 Blueprint 완성
```

#### 왜 중요한가?
- **선형 진행의 한계 극복**: Stage 1→2→3→...→9가 일방향이 아님
- **품질 vs 속도**: 잘못된 기반 위에 계속 쌓으면 나중에 전체 붕괴
- **AI 특성 고려**: AI는 이전 결정을 맹목적으로 따를 수 있음 → 명시적 수정 프로토콜 필요

#### 6단계 수정 프로토콜:
```
Step 1: 오류 발견 및 문서화
  - 무엇이 잘못되었는가?
  - 어느 Stage의 어떤 결정인가?

Step 2: 영향받는 Stage 범위 파악
  - 잘못된 결정 이후 Stage 모두 영향받음
  - 재작업 범위 명확히 파악

Step 3: 해당 Stage로 이동 → 수정
  - 근본 원인 수정
  - 수정 이유 문서화

Step 4: 수정된 산출물 검증
  - 수정이 올바른지 검증
  - 다른 결정과 충돌 없는지 확인

Step 5: 다음 Stage부터 현재까지 재진행
  - 수정된 결정 기반으로 재작업
  - 모든 영향받은 Stage 다시 실행

Step 6: 재진행 결과 검증
  - 전체 일관성 확인
  - 더 이상 오류 없는지 검증
```

#### 추적성 (Traceability):
- **수정 이력 기록**: `[파일명]_revision_log.md`
- **영향 범위 명시**: 어떤 Stage들이 재작업되었는가
- **재작업 체크리스트**: 재진행 시 누락 방지

#### 각 Stage별 적용:
- **Stage 2**: Stage 1 검증
- **Stage 3**: Stage 1-2 검증
- **Stage 4-6**: Stage 1-3 검증 (ADR 기반)
- **Stage 7**: Stage 1-6 검증 (가장 critical!)
- **Stage 8**: Stage 7 검증
- **Stage 9**: Stage 8 검증

---

## Critical Principles (Legacy - kept for reference)

### 1. Environment First, Then Execution

**Wrong Approach**:
```
Idea → Blueprint → Implementation
(Blueprint incomplete due to missing environment context)
```

**Correct Approach**:
```
Stage 1-6: Build Environment (Family, Constraints, ADR, DNA Systems, Standards)
    ↓
Stage 7: Blueprint (Now complete with full environment context)
    ↓
Stage 8-9: Task Breakdown → Execution
```

### 2. Environment Enforcement (Not Just Documentation)

**The Problem**: Telling AI rules verbally → repeated failures
- Type errors
- Using `print()` instead of logger
- Unmocked dependencies
- TODO/pass left in code

**The Solution**: "Environment" = Standards + DNA Systems + Automation
```
Standards (documented rules):
  "DO NOT use print()"
    ↓
DNA Systems (common modules):
  src/core/logging/ (structlog)
    ↓
Automation (enforcement):
  Pre-commit hook detects print() → blocks commit
```

**Result**: AI cannot make mistakes even if it wants to!

### 3. LEGO Block Strategy

Break work into blocks that fit together perfectly:

```
Blueprint (complete design after environment ready)
    ↓
Task Breakdown (independent LEGO blocks)
    - Each task: 2-4 hours
    - No TODO, no pass
    - Complete and verified
    ↓
Checklist (execution manual for each block)
    - Read only this checklist
    - Execute only this task
    - Independent execution
    ↓
Implementation
    - Each checklist done = one block complete
    - All checklists done = project complete
```

### 4. Jason's Blueprint 3-Phase Process

**Phase 1: Blueprint** - Capture everything while context is fresh
- Purpose: Complete design document when context is intact
- Principle: Detailed enough for anyone to implement independently

**Phase 2: Task Breakdown** - Create LEGO blocks
- Purpose: Split long blueprint (can't implement at once) into blocks
- Principle: Atomic units, each task 2-4 hours

**Phase 3: Checklist** - Execution manual per block
- Purpose: Detailed checklist per task in separate files
- Principle: Read only this checklist, execute only this task (independent)
- Result: All checklists done = entire project complete

> **"If you can do it all at once, just use the blueprint. But when you can't, make it 'complete' in smaller chunks. Create a plan where executing each piece completes the whole. Context limitation breakthrough!!! The method is to create the 'environment'!"** - Jason

## Relationship with SPARK Agent System

**SPARK** (spark-claude):
- Identity: General-purpose AI agent orchestration system
- Purpose: Traits + Role-based agent research
- Naming: `{role}-spark`

**DNA** (dna-methodology):
- Identity: AI collaboration development framework (software design methodology)
- Purpose: 9-Stage process + Skills refinement
- Naming: `{role}-dna`

**Dependency**: DNA reuses SPARK agents for Stage 5-9 by copying and renaming. No runtime dependency—agents are independent copies.

## Important Documentation

### User Guides
- `docs/guides/00_CORE_METHODOLOGY.md` - DNA v4.0 overview
- `docs/guides/01G-00_*.md` - Stage 1 guides
- `docs/guides/02G-00_*.md` - Stage 2 guides
- `docs/guides/03G-00_*.md` - Stage 3 guides

### Developer Guides
- `docs/plugin-guide/plugin-structure-guide.md` - Claude Code plugin development
- `docs/plugin-guide/agent-definition-structure.md` - 7-Section agent structure
- `docs/plugin-guide/stage-execution-guide.md` - Stage goals, techniques, references

### Integration Guides
- `docs/integration/spark-agent-mapping.md` - DNA ↔ SPARK mapping
- `docs/integration/agent-naming-convention.md` - Agent naming strategy

## Current Project Status

### 📊 Stage 가이드 검토 현황 (2025-12-03)

#### Stage 1-7 검토 완료
- **평균 점수**: 59.14/60 (98.6%)
- **완벽 점수 (60/60)**: Stage 3, 6, 7 (3개/7개 = 43%)
- **최저 점수**: Stage 2 (58/60 = 96.7%)

#### Stage 8 검토 완료
- **기본 품질** (6가지 기준): 59/60 (98.3%)
  - 독립 실행 가능성: 10/10
  - 명확성: 9/10 (AI 최적 크기 강조 부족)
  - 실행 가능성: 10/10
  - 검증 가능성: 10/10
  - Detailed 정합성: 10/10
  - 완전성: 10/10
- **DNA 핵심 원칙 반영**: 13/30 (43.3%)
  - AI 최적 크기: 6/10
  - 완전해질 때까지 반복: 4/10
  - 기능별 분해 + 조립: 3/10
  - 역방향 수정 프로토콜: 0/10
- **종합 점수**: 72/90 (80%)

#### Stage 8 개선 작업 (1호 진행 중)
**4개 섹션 추가** (총 310줄):
1. "🎯 AI 최적 크기" (70줄)
2. "🔄 완전해질 때까지 반복" (60줄)
3. "🧩 기능별 분해 + 연결부 + 조립" (100줄)
4. "⏪ 역방향 수정 프로토콜" (80줄)

**결과 예상**: 1,299줄 → 1,609줄, DNA 핵심 반영 43% → 90%

#### Stage 1-9 전체 보완 (1호 진행 중)
- 각 Stage에 "⏪ 이전 Stage 검증 및 수정 프로토콜" 섹션 추가
- DNA_METHODOLOGY_DETAILED.md에 4대 핵심 원칙 반영

### ✅ 완료된 것

1. **방법론 문서** (Stage 1-9 모두 작성됨)
   - `docs/guides/` - 각 Stage별 가이드/매뉴얼/사례
   - `docs/plugin-guide/` - 플러그인 개발 가이드
   - `docs/integration/` - SPARK 통합 문서
   - **DNA 4대 핵심 원칙 확정** (2025-12-03)

2. **Agents** (Stage 5-9만)
   - `implementer-dna`, `documenter-dna`, `designer-dna`, `analyzer-dna`, `qc-dna`
   - SPARK에서 복사, 이름만 변경

3. **Plugin 구조**
   - `.claude-plugin/plugin.json`
   - `skills/assets/templates/`

### ❌ 아직 안된 것

1. **Agents** (Stage 1-4)
   - `classifier-dna` (패밀리 분류)
   - `investigator-dna` (환경 제약 조사)
   - `decision-maker-dna` (ADR 작성)
   - `planner-dna` (DNA 시스템 계획)

2. **Commands** (전체)
   - `/dna:init` ~ `/dna:stage9` (13개 명령어)

3. **Skills** (지식 구조화)
   - 템플릿만 있음
   - Progressive Disclosure 구현 필요
   - Stage별 참조 문서 작성 필요

4. **Validator Scripts**

### 🎯 최종 목표

1. ✅ Stage 1-6 완성 (단위작업으로 만들기)
2. ✅ Stage 7-9 재검토 (2호의 새 기능 활용)
3. ✅ 전체 9-Stage 통합 검증

### 📝 다음 작업

**우선순위 1**: Stage 1-6 작업 크기 연구
- 각 Stage를 어떻게 여러 세션으로 나눌까?
- 주식 거래 플랫폼 사례로 실험
- 세션당 작업량 검증

**우선순위 2**: Skills 구조화
- Stage별 필요한 지식 정리
- Progressive Disclosure 설계

**우선순위 3**: Stage 1-4 Agents 구현
- Phase 구조 설계
- Skills 참조 방식

**우선순위 4**: Commands 작성
- 오케스트레이션 흐름
- 인자 처리

## Key References

- **SPARK Repository**: https://github.com/Jaesun23/spark-claude
- **SEI Architecture Decision**: Software Engineering Institute
- **Gemini 4-Phase Process**: CoD, ToT, SoT techniques
- **Research Base**: Jason's 2 years of AI collaboration experience, 7 project failure analysis

## Contact

- **Author**: Jason (Jaesun23)
- **Email**: jaesun23@gmail.com
- **GitHub**: https://github.com/Jaesun23
- **Issues**: https://github.com/Jaesun23/dna-methodology/issues

---

**"Context limitation breakthrough!!! The method is to create the 'environment'!"** - Jason
