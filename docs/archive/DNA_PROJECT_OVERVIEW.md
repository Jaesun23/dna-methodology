# DNA Methodology Project - 프로젝트 개요

> **핵심**: 백지상태의 2호가 이 문서만 읽으면 DNA 프로젝트의 전체를 이해할 수 있습니다.

---

## 📌 프로젝트의 진짜 목표

이 프로젝트는 **"아이디어에서 완성된 소프트웨어까지"** AI와 함께 만드는 **완전한 방법론**을 확립하는 것입니다.

### 현재 상태

| Stage | 방법 유효성 | 프레임워크화 | 상태 |
|:-----:|:----------:|:-----------:|:----:|
| 1-6 | ❌ 연구 필요 | ❌ 미착수 | 우선 과제 |
| 7-9 | ✅ 방법이 통함 | ❌ 미착수 | 구체화 필요 |

```
⚠️ Stage 7-9의 방법론 내용은 "이 방법이 통한다"를 확인한 것이지,
   "누가 어떤 식으로 작업한다" 같이 프레임워크화는 아직 정해지지 않음
```

### 최우선 과제

**Stage 1-6를 각각 "단위작업"으로 만들기**

- 단위작업 = AI가 한 세션에서 최고 성과를 낼 수 있는 크기
- 명확한 입력과 출력
- 일관성 유지 방법
- 검증 가능

### 최종 목표

**전체 9-Stage를 2호 기능(Skills, Commands, Agents)과 조합한 하나의 프레임워크로 완성**

1. Stage 1-6: 방법 연구 + 프레임워크화
2. Stage 7-9: 프레임워크화 (2호의 새 기능 활용)
3. 전체 9-Stage 통합 검증

---

## Part 1: AI 협업의 문제와 해결

### 🚨 Jason의 경험: 여러 프로젝트 실패

> "여러가지 프로젝트를 1, 2호와 함께 하면서 성공한 프로젝트가 몇 가지 없음"

**가장 기본적인 문제**:

- Jason의 소프트웨어 개발 경험/지식 부족 → 전체 컨트롤 불가
- AI의 여러 한계와 행동패턴

### AI의 6가지 문제점

#### 1. Context 문제 ⚠️
```
- 일정 용량 넘으면 앞선 내용 잊어버림
- 현재 작업이 전체 어디에 위치하는지 파악 불가
- 트랜스포머 모델의 태생적 문제: Context Rot
- 많은 정보를 제공해도 문제 발생
```

#### 2. 회피 🙈
```
- 너무 많은 정보를 대하면 모른 척 하거나 적당히 하다가 멈춤
- 긍정표현 규칙이 많으면: 그냥 좋은 말로 여기고 넘김
- 부정표현 규칙이 많으면: 부담스러워서 포기하고 싶다고 함
```

#### 3. AI의 자기 과신 😤
```
- Context 한계가 있다는 것을 인지하지 못함
- 학습 데이터가 최신이 아니라는 걸 모름
- "차근차근 정리하면서" 하자고 해도 "모두 할 수 있다"고 자신감
- 타입스크립트 타입 사용 주의 → "할 수 있다" → 결국 프로젝트 폐기
```

#### 4. 불필요하게 과한 작업 🔨
```
실제 사례:
- 랜덤값 실험 필요 → "안정성" 이유로 고정값 하드코딩
  ➟ 실패도 실험의 중요한 결과인데!!

- 미운영 시스템 리팩토링 → 이전버전 호환, 마이그레이션 전략 수립
  ➟ 그냥 틀린부분 없애고 다시 구축하는 건데!!
```

#### 5. 할루시네이션 🌫️
```
- 여러 기능 조사 → 구현 완료 → 그때서야 안 되는 걸 알게 됨
- "사실확인 안 된 사항 사용 금지" 경고해도
- 없는 사실 언급하거나 동의 없이 임의 추정
```

#### 6. 압박감 또는 강박증? 😰
```
- 컨텍스트 한계를 느끼는지 한 번에 다 해버리려고 함
- 애매모호한 질문 → 잘 대답해야 한다는 생각 → 할루시네이션
```

### ✨ AI가 최고 성과를 낼 때

```
✅ 1. 규모가 크지 않아 전체를 한 번에 계획해서 진행 가능
✅ 2. 여러 선택지에서 논리적 흐름/근거에 따른 판단 가능
✅ 3. 요청내용과 결과에 대한 명확한 지침 존재
✅ 4. 매번 새로운 대화지만 기존 작업을 어떤 방식으로든 이해
```

### 💡 해결책 (DNA 방법론의 근본)

```
1. 컨텍스트의 한계를 항상 염두에 두라
2. 전체 흐름을 여러 단계로 나눈 계획을 미리 세운다
3. 하나의 작업 또는 하나의 단계는 하나의 세션에서 완료되도록 한다
4. 명확한 지침과 스스로 도달할 선택지를 사전에 제공한다
```

> **이 결론에서 여러 번의 개정을 거듭한 후에 DNA 방법론까지 오게 됨**

---

## Part 2: DNA 방법론의 2가지 핵심

### 핵심 1: "부분으로 전체를 완성" 🧩

> **"하나의 세션에서 컨텍스트 제한을 고려해서 필요한 정보를 제공하고, 가장 좋은 성과를 낼 수 있는 양의 작업을 정확하게 지시한다."**

#### "부분"의 의미
```
부분 = AI가 최고 성과를 내는 "단위작업" (레고블럭)

특징:
- 입력 명확
- 출력 명확
- 독립 실행 가능
- 한 세션에서 완료
- 검증 가능
```

#### "전체"의 의미
```
전체 = Σ(완벽한 부분)

모든 부분(레고블럭)이 완성되면 = 전체 프로젝트 완성
```

#### 방법 유효성 vs 프레임워크화

| 구분 | Stage 7-9 | Stage 1-6 |
|:----:|:---------:|:---------:|
| **방법 유효성** | ✅ 통함 확인 | ❌ 연구 필요 |
| **프레임워크화** | ❌ 미착수 | ❌ 미착수 |

```
Stage 7-9 (Blueprint → 구현):
  - 방법: Blueprint → Task Breakdown → Checklist → 구현
  - 상태: 실제 프로젝트에서 "이렇게 하면 된다" 확인!
  - 남은 것: 2호 기능(Skills/Commands/Agents)과 조합하여 프레임워크화

Stage 1-6 (아이디어 → Blueprint):
  - 방법: 각 단계를 어떻게 "단위작업"으로 만들까?
  - 상태: 직관적으로 잘 들어맞을 것으로 생각됨
  - 남은 것: 방법 연구 + 프레임워크화 둘 다 필요
```

#### 레고블럭 전략의 핵심

> **"전체를 단위작업으로 쪼개는 이 원칙(컨텍스트 한계 고려, 의미있는 산출물 생산, 일관성 유지, 누락없음)은 청사진을 분해하여 구현까지 실행하는 단계만이 아니라, 아이디어를 확장시켜 청사진으로 구체화하는 단계에도 동일하게 적용된다."**

**단위작업 분할의 4가지 질문** (08G-00_task_breakdown_guide.md 기반):

| 질문 | 후반부 (Stage 7-9) | 전반부 (Stage 1-6) |
|:----:|:-----------------:|:-----------------:|
| **Q1: 컨텍스트 한계** | Task 100줄씩, 80-90K 안전 범위 | ADR 3개씩, 시스템 조사 3개씩 |
| **Q2: 의미있는 산출물 생산** | 독립 테스트 가능한 기능 | 독립 검증 가능한 문서 |
| **Q3: 일관성 유지** | 같은 도구, 같은 패턴 | 같은 템플릿, 같은 검증 기준 |
| **Q4: 누락 없음** | Blueprint 전체 커버 | 아이디어의 모든 요소 커버 |

**Stage 1-6 분할 구상** (현재 연구 방향):

```
예시: Stage 3 (ADR 작성)
├─ 전체: 18개 ADR 작성 필요
├─ 한번에? NO! (컨텍스트 초과)
├─ 분할: 세션당 3개씩 (컨텍스트 범위 내)
│   ├─ Session 1: ADR 001-003 ← Q2: 의미있는 산출물 (3개 ADR)
│   ├─ Session 2: ADR 004-006 ← Q3: 같은 템플릿 (일관성)
│   └─ ...
└─ 누적: 6 세션 → 18개 ADR 완성 ← Q4: 누락 없음
```

```
각 Stage마다 이 4가지 질문을 적용해서 "단위작업"을 정의하면
현재 미완성된 방법론의 전반부를 완성할 수 있음
```

### 핵심 2: "환경으로 제어" 🛡️

> **"다른 것들은 시스템적으로 제약하고 관리한다."**

#### 문제: 문서화된 규칙의 한계

```
❌ 문서로 규칙 제공 → AI가 안 읽거나 회피
❌ 긍정표현 많으면 → 그냥 좋은 말로 여김
❌ 부정표현 많으면 → 부담스러워서 포기

"대부분의 프로젝트에서 실패했던 이유는 여러가지가 있는데
가장 큰 문제는 어떻게 일관성, 통일성을 가지고 끝까지 작업할 수 있는가임."
```

#### 해결: "환경" 구축

```
"모든 걸 문서화 된 규칙으로 제공하기에는 한계가 있고
그렇게 많이 제공해봤자 제대로 읽어보지도 않는다는 걸 알게되었음."

→ "환경"을 구축해서 제약하고, 최소의 정보를 제공하여 작업하도록
```

#### DNA 시스템 = 시스템적 제약

```
DNA 시스템 11개 = 전 프로젝트에 공통으로 사용되고, 지켜져야 할 "환경"

예시:
┌─────────────────────────────────────┐
│ 규칙: "print() 사용 금지"            │
│ DNA: src/core/logging/ (structlog)  │
│ 강제: pre-commit hook → print() 감지 → 커밋 차단 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 규칙: "타입 오류 없어야 함"          │
│ DNA: src/core/types/ (Pydantic)     │
│ 강제: MyPy → 타입 오류 발견 → 빌드 실패 │
└─────────────────────────────────────┘

핵심: "조심해라" (X) → "못하게 막는다" (O)
```

**DNA 11 시스템**:
1. Logging (structlog)
2. Configuration (Pydantic)
3. Database (SQLAlchemy)
4. Cache (Redis)
5. Messaging (Kafka/RabbitMQ)
6. Types (Pydantic v2)
7. Testing (pytest)
8. Monitoring (Prometheus)
9. Security (인증/인가)
10. Error Handling
11. API Gateway

#### Stage 6의 역할

```
Stage 6: Project Standards 작성
- 구현된 DNA 시스템의 공통모듈 사용 강제조항 포함
- 프로젝트 종료 시까지 지켜야 할 코딩 스타일, 로깅, 에러, 설정, 기타 룰
- DO/DON'T 명확하게
- 자동화로 강제 (Ruff, MyPy, pytest, pre-commit hooks)
```

---

## Part 3: Stage의 진짜 의미 ⚠️ **중요!**

### ❌ 흔한 착각

```
Stage 1 = 한 번의 세션에서 완료하는 작업
Stage 2 = 한 번의 세션에서 완료하는 작업
...
```

### ✅ 실제 의미

```
Stage = 여러 세션에 걸친 점진적 누적
```

> **"Stage는 한 개의 작업이 아니에요."** - Jason

### 구체적 예시: 청사진 작성 (Stage 7)

```
청사진 문서 작성:
├─ 문서 하나만? NO!
├─ 한 번에 작성? NO!
│
├─ 실제:
│   ├─ 여러 개의 문서로 나눠서 작성
│   ├─ 한 문서도 길면 파트별로 나눠서 작성
│   └─ Session 1: Part 1 작성
│       Session 2: Part 2 작성
│       Session 3: Part 3 작성
```

### 구체적 예시: 체크리스트 작성 (Stage 9)

```
체크리스트 작성:
├─ 단위작업별 별도 파일
├─ 한 세션에 보통 3~4개 작성 (Jason의 경험)
│
└─ 예시:
    Session 1: task1_checklist.md, task2_checklist.md, task3_checklist.md
    Session 2: task4_checklist.md, task5_checklist.md, task6_checklist.md
```

### 구체적 예시: Stage 1-6 (연구 대상!)

> **"제가 얘기하는 전반부의 작업크기는 연구해보자는 거에요."** - Jason

```
예시: 아이디어가 있어요
  ↓
이걸 구현하기 위해서는 무슨 시스템이 필요하지?
  ↓
찾아낸 결과: 20개 시스템이 서로 연결되어야 함
  ↓
다음 Stage: 20개 중 하나씩 결정해야 하는 요소들 찾기
  ├─ 20개를 한 꺼번에? NO!
  ├─ 20번의 새로운 세션에서 각각? Maybe!
  └─ 더 쪼개서 40번, 50번? Maybe!
  ↓
다음 Stage: 결정 요소들에 대한 ADR 하나씩 작성
  ├─ 한 번에? NO!
  └─ 여러 번의 세션으로 작업
```

### 핵심 원칙

```
✅ 각 세션은 "일부분"만 작업
✅ 하지만 일관성 유지:
   - 제약조건은 각 세션에 항상 제공
   - 전체 맥락 제공
   - 현재 작업의 위치 명확히
✅ 누적해서 전체 완성

"대신 원칙도 방향도 없이 찾는 게 아니라
제약조건들은 각 세션에 항상 제공되게 하는 거구요." - Jason
```

### 완전한 예시: 주식 거래 플랫폼

```
아이디어: "주식 거래 플랫폼을 만들자"
  ↓
Stage 1: 핵심 시스템 식별
  Session 1: 거래, 계좌, 시세 시스템 분석 → 01F-01_part1.md
  Session 2: 알림, 인증, 로깅 시스템 분석 → 01F-01_part2.md
  Session 3: 패밀리 분류 (A-C-A) → 01C-01_family.md
  ↓
Stage 2: 각 시스템별 제약 조사
  Session 1: 거래 시스템 - KIS API 조사 → 02C-01_trading.md
  Session 2: 계좌 시스템 - 금융규제 조사 → 02C-02_account.md
  Session 3: 시세 시스템 - KRX 시간 조사 → 02C-03_market.md
  ...
  ↓
Stage 3: 각 시스템별 ADR 작성
  Session 1: Bootstrap ADR 001-003 → 03A-001.md, 002, 003
  Session 2: Bootstrap ADR 004-006 → 03A-004.md, 005, 006
  ...
  Session 10: Domain ADR 101-103 → 03A-101.md, 102, 103
  ...
  결과: 총 20개 ADR 완성!
  ↓
Stage 4: DNA 시스템 청사진
  Session 1: Logging + Config 설계 → 04B-01_bootstrap_part1.md
  Session 2: Database + Cache 설계 → 04B-01_bootstrap_part2.md
  ...
  ↓
Stage 5: DNA 시스템 구현
  Session 1: Logging 구현 → src/core/logging/
  Session 2: Config 구현 → src/core/config/
  ...
  ↓
... (후반부 계속)
```

---

## Part 4: 세 가지 컴포넌트의 역할

### Claude Code의 새 기능 활용

```
1. CLAUDE.md의 단계적 정보 제공
2. Subagent 활용 (2호가 도구로 호출)
3. Slash Commands (복잡한 실행과정 정확히 이행)
4. Skills (방대한 지식과 작업방법 구축) ← 방법론 완성의 핵심!
5. Plugin (하나의 패키지로 묶어서 사용/관리)
```

### 역할 구분

| 컴포넌트 | 역할 | 비유 |
|----------|------|------|
| **Skills** | 지식 저장소 | 전문 서적, 레퍼런스 매뉴얼 |
| **Commands** | 실행 트리거 | 버튼, 명령어 인터페이스 |
| **Agents** | 작업 수행자 | 전문가, 실행자 |

### Skills = 지식 저장소 📚

#### 역할
```
- 방법론, 패턴, 템플릿 등 정적 지식 저장
- Progressive Disclosure: 필요할 때만 로드
- 컨텍스트 효율 극대화
- 여러 Agent/Command가 공유
```

#### DNA에서 담는 내용
```
1. 핵심 개념
   - 7개 패밀리 정의
   - NFR 정의
   - Context Rot 방지 전략

2. 템플릿
   - ADR 템플릿 (5 Categories)
   - 체크리스트 템플릿 (9-Step)
   - Blueprint 구조

3. 패턴
   - 아키텍처 패턴 (Lambda, Kappa, 하이브리드)
   - 기술 선택 가이드

4. 참조 문서
   - 기존 가이드/매뉴얼 링크
```

#### Skills가 하지 않는 것
```
❌ 직접 작업 수행
❌ 사용자 입력 처리
❌ 동적 결정
```

### Commands = 실행 트리거 🚀

#### 역할
```
- 사용자 인터페이스 (/stage1, /dna-init)
- 인자 파싱 및 검증
- 적절한 Agent 호출
- 오케스트레이션 (순차/병렬)
```

#### 설계 원칙
```
1. 단순 진입점: 복잡한 로직 없음
2. 명확한 목적: 하나의 명령 = 하나의 목표
3. 에이전트 위임: 실제 작업은 Agent가 수행
4. 체이닝 가능: 여러 Agent 순차/병렬 호출
```

#### 예시
```markdown
---
name: stage3
description: Stage 3 ADR 작성 (Bootstrap)
requires: stage3-adr-author
---

# /stage3 - ADR 작성

이 명령어는:
1. Stage 2 결과 수집 (02C-*.md, 02D-*.md)
2. stage3-adr-author 에이전트 호출
3. Bootstrap ADR 3개 생성 (001-003)
4. 다음 세션 가이드 제공
```

### Agents = 작업 수행자 👨‍💻

#### 역할
```
- 실제 분석/생성/검증 작업 수행
- 전문화된 페르소나로 특정 영역 담당
- 품질 게이트 통과 책임
- 도구 사용 (Read, Write, Bash, Glob, Grep)
```

#### 설계 원칙
```
1. 명확한 정체성: 역할과 전문성 정의
2. 단계별 프로세스: Phase 0-N 구조
3. 품질 검증: 마지막 Phase에서 검증
4. 산출물 정의: 무엇을 생성하는지 명확
```

#### Phase 구조
```
Phase 0: Task Understanding
  - 작업 이해
  - 컨텍스트 수집
  - 이전 작업 읽기

Phase 1-N: Work
  - Skills 참조
  - 실제 작업 수행
  - 점진적 완성

Phase N+1: Verification
  - 품질 검증
  - 템플릿 준수 확인
  - 산출물 검증
```

### 상호작용 흐름

```
┌─────────────────────────────────────────────────┐
│ 1. 사용자: /stage3 "Bootstrap ADR 001-003 작성"  │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│ 2. Command (stage3.md)                          │
│    - 인자 파싱: "Bootstrap ADR 001-003"          │
│    - Agent 선택: stage3-adr-author              │
│    - 컨텍스트 준비: 02C-*.md, 02D-*.md          │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│ 3. Agent (stage3-adr-author.md)                 │
│    Phase 0: 작업 이해                            │
│      - Read 02C-01_constraints.md               │
│      - Read 02D-01_tech_stack.md                │
│    Phase 1: ADR 템플릿 로드                      │
│      - Skills 참조: adr-templates.md            │
│    Phase 2: ADR 001 작성 (KIS API 선택)         │
│    Phase 3: ADR 002 작성 (금융규제 준수)         │
│    Phase 4: ADR 003 작성 (KRX 시장시간)          │
│    Phase 5: 검증                                 │
│      - 템플릿 준수 확인                          │
│      - Context7 최신 정보 확인                   │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│ 4. 산출물                                        │
│    - 03A-001_kis_api_selection.md               │
│    - 03A-002_financial_compliance.md            │
│    - 03A-003_krx_market_hours.md                │
│    - stage3_progress.json (진행 상태)           │
└─────────────────────────────────────────────────┘
```

---

## Part 5: 9-Stage 구조

### 전반부 (Stage 1-6): 아이디어 → Blueprint ❌ 연구 필요

#### Stage 1: 패밀리 구분과 핵심기능 파악
```
목표:
- 3-Layer Decision Tree에 따른 패밀리 구분
- 18가지 경우의 수 → 7가지 패밀리로 분류 (1호 연구 결과)
- 발견한 문제 또는 실현하고자 하는 것의 "핵심기능" 파악

산출물:
- 01F-01_core_functions.md (핵심 기능 정의)
- 01C-01_family_classification.md (패밀리 코드, 예: A-C-A)

Agent: classifier-dna (신규 작성 필요)
```

#### Stage 2: 구조설계
```
목표:
- 패밀리 → 필수 핵심시스템과 DNA 시스템 선택 범위 자동 결정
- 가용자원, 내/외부 제약조건에 따라 시스템 선택
- 구조설계 요소 검토

산출물:
- 02C-01_layer3_constraints.md (외부 제약)
- 02C-02_conflicts.md (충돌 패턴)
- 02D-01_tech_stack.md (기술 스택 결정)

Agent: investigator-dna (신규 작성 필요)
```

#### Stage 3: 결정 문서화 (ADR)
```
목표:
- 결정된 요소들에 대해 하나씩 ADR 작성
- 너무나도 당연한 요소들도 모두 작성
- DNA 시스템 요소와 도메인 요소 구분

산출물:
- 03A-001~099.md (Bootstrap ADR: DNA 시스템)
- 03A-100+.md (Domain ADR: 도메인 특화)

Agent: decision-maker-dna (신규 작성 필요)
- Context7 활용 (최신 정보 검증)
```

#### Stage 4: DNA 시스템 청사진 → 작업분해 → 체크리스트
```
목표:
- 전 프로젝트 공통 "환경" 구축 계획
- common/ 에 들어갈 모듈들에 대한 ADR 기반 설계

산출물:
- 04B-01_dna_blueprint.md (DNA 시스템 청사진)
- 04T-01_dna_tasks.md (작업 분해)
- 04L-001~.md (각 작업별 체크리스트)

Agent: planner-dna (신규 작성 필요)
```

#### Stage 5: DNA 시스템 실행
```
목표:
- DNA 구축작업 체크리스트 기반 구현
- 구현된 모듈 작동 점검

산출물:
- src/core/logging/ (실제 코드)
- src/core/config/
- ... (11개 DNA 시스템)

Agent: implementer-dna ✅ (SPARK에서 복사)
```

#### Stage 6: Project Standards 작성
```
목표:
- DNA 시스템 공통모듈 사용 강제조항
- 프로젝트 종료까지 지켜야 할 룰 문서화

산출물:
- PROJECT_STANDARDS.md
- pyproject.toml (Ruff, MyPy 설정)
- .pre-commit-config.yaml

Agent: documenter-dna ✅ (SPARK에서 복사)
```

### 후반부 (Stage 7-9): Blueprint → 구현 ✅ 검증됨

#### Stage 7: Project Blueprint 작성
```
목표:
- 도메인 ADR 기반 완전히 상세한 청사진
- 아키텍처 구조, 도메인 구조, 다이어그램
- 최신 기술과 기법으로 구현 명세

산출물:
- 07B-01_project_blueprint.md (또는 여러 파트로 나눔)

Agent: designer-dna ✅ (SPARK에서 복사)
```

#### Stage 8: Task Breakdown 문서 작성
```
목표:
- AI가 집중해서 완전하게 구현할 정도의 크기로 작업 분할
- 작업분할 기준에 따른 분할

산출물:
- 08T-01_task_breakdown.md

Agent: analyzer-dna ✅ (SPARK에서 복사)
```

#### Stage 9: 작업별 Checklist 작성
```
목표:
- 분할된 작업별로 체크리스트 문서 작성
- TDD 기반 9-Step Checklist

산출물:
- 09L-001_task1_checklist.md
- 09L-002_task2_checklist.md
- ... (각 작업별)

9-Step:
1. 목표이해
2. 테스트작성
3. 구현
4. 정적검증 (Ruff, MyPy)
5. 단위테스트실행
6. 리팩토링
7. 종합테스트
8. 문서화
9. 커밋

Agent: qc-dna ✅ (SPARK에서 복사)

최종 목표:
- 모든 기능 구현
- 검증결과 0 violations
- 테스트 95%+ coverage
```

### 현재 상태 요약

```
방법 유효성:
├─ Stage 1-6: ❌ 연구 필요
└─ Stage 7-9: ✅ 방법이 통함 확인

프레임워크화 (Skills/Commands/Agents 조합):
├─ Stage 1-6: ❌ 미착수
└─ Stage 7-9: ❌ 미착수

Agents:
├─ Stage 1-4: ❌ 없음 (신규 작성 필요)
│   ├─ classifier-dna
│   ├─ investigator-dna
│   ├─ decision-maker-dna
│   └─ planner-dna
│
└─ Stage 5-9: ✅ 있음 (SPARK에서 복사)
    ├─ implementer-dna
    ├─ documenter-dna
    ├─ designer-dna
    ├─ analyzer-dna
    └─ qc-dna

Commands: ❌ 전체 없음 (작성 필요)
Skills: ⚠️ 템플릿만 있음 (지식 구조화 필요)
Guides: ✅ Stage 1-9 모두 작성됨
```

---

## Part 6: 작업 예시 - 주식 거래 플랫폼

### 전체 흐름

```
아이디어: "한국 주식 거래 플랫폼을 만들자"
  ↓
Stage 1: 핵심 기능과 패밀리 분류
  ↓
Stage 2: 환경 제약과 충돌 해결
  ↓
Stage 3: ADR 작성 (18개)
  ↓
Stage 4-6: DNA 시스템 구축
  ↓
Stage 7-9: 도메인 구현
  ↓
완성!
```

### Stage 1: 패밀리 분류 (Session 1-2)

#### Session 1: 핵심 기능 파악
```
입력: "한국 주식 거래 플랫폼을 만들자"

/stage1-function "주식 거래 플랫폼"

Agent 작업:
Phase 0: 프로젝트 이해
  - 주식 거래가 핵심
  - 수동/자동 구분? NO! → 비즈니스 목적으로 구분
  - 핵심 기능: "거래" (1개로 통합)

Phase 1: Skills 참조
  - references/core/methodology-overview.md
  - references/core/families.md

Phase 2: 기능 정의
  - 거래: 주문 생성 → 체결 → 결과 확인
  - 계좌: 잔고 관리
  - 시세: 실시간 데이터

산출물:
  - 01F-01_core_functions.md
```

#### Session 2: 패밀리 분류
```
/stage1-classify

Agent 작업:
Phase 0: 이전 작업 읽기
  - Read 01F-01_core_functions.md

Phase 1: Layer 1-3 질문
  - Layer 1 (실패 영향): 치명적 (금전 손실) → A
  - Layer 2 (데이터): 비구조화 (실시간 스트림) → C
  - Layer 3 (응답시간): 밀리초 (거래 타이밍) → A

Phase 2: 패밀리 결정
  - A-C-A 패밀리 발견! (새로운 패턴)
  - Autonomy-Choreography-Autonomy

Phase 3: NFR 프로파일
  - Performance: High (100ms 이내)
  - Reliability: High (99.9% 가용성)
  - Security: High (금융 데이터)
  - Scalability: Medium

산출물:
  - 01C-01_family_classification.md
```

### Stage 2: 환경 제약 (Session 3-6)

#### Session 3: 외부 제약 조사 (KIS API)
```
/stage2-investigate "증권사 API"

Agent 작업:
Phase 0: 컨텍스트
  - Read 01C-01_family_classification.md (A-C-A)

Phase 1: Layer 3 외부 제약
  - 한국투자증권 API 조사
  - 다른 증권사 비교 (LS, NH, KB)
  - Context7 최신 정보 확인

Phase 2: 제약 문서화
  - API 호출 제한: 초당 20회
  - 인증 방식: OAuth 2.0
  - 시장 시간: 09:00-15:30

산출물:
  - 02C-01_kis_api_constraints.md
```

#### Session 4: 외부 제약 조사 (금융규제)
```
/stage2-investigate "금융 규제"

산출물:
  - 02C-02_financial_regulations.md
  - 전자금융거래법
  - 개인정보보호법
```

#### Session 5: 충돌 패턴 분석
```
/stage2-conflicts

Agent 작업:
Phase 0: 이전 작업 읽기
  - Read 01C-01 (A-C-A: 단일 트랜잭션 vs 독립 배포)
  - Read 02C-01, 02C-02

Phase 1: 충돌 식별
  1. 단일 트랜잭션 ↔ 독립 배포
  2. 강한 일관성 ↔ 높은 독립성
  3. 실시간 정확성 ↔ 고성능

Phase 2: 해결 전략
  1. 하이브리드 아키텍처 (Saga + 이벤트 소싱)
  2. Outbox 패턴
  3. Redis 캐싱 + Write-through

산출물:
  - 02C-03_conflict_patterns.md
```

#### Session 6: 기술 스택 결정
```
/stage2-tech-stack

산출물:
  - 02D-01_tech_stack_decisions.md
  - FastAPI, PostgreSQL, Redis, Kafka, WebSocket
```

### Stage 3: ADR 작성 (Session 7-16)

#### Session 7-9: Bootstrap ADR (001-009)
```
/stage3-bootstrap "001-003"

Session 7:
  - 03A-001_kis_api_selection.md
  - 03A-002_financial_compliance.md
  - 03A-003_krx_market_hours.md

Session 8:
  - 03A-004_hybrid_architecture.md
  - 03A-005_event_sourcing.md
  - 03A-006_redis_caching.md

Session 9:
  - 03A-007_fastapi_framework.md
  - 03A-008_postgresql_redis.md
  - 03A-009_kafka_messaging.md
```

#### Session 10-16: Domain ADR (101-118)
```
/stage3-domain "101-103"

Session 10-16에 걸쳐:
  - API 설계 (5개 ADR)
  - 보안 (3개 ADR)
  - 기타 (10개 ADR)

총 18개 ADR 완성!
```

### Stage 4-6: DNA 시스템 (Session 17-30)

```
Session 17-20: DNA 청사진 (4개 파트)
Session 21-28: DNA 구현 (11개 시스템)
Session 29-30: Standards 문서화
```

### Stage 7-9: 도메인 구현 (Session 31-50)

```
Session 31-35: Blueprint (5개 파트)
Session 36-40: Task Breakdown (20개 작업)
Session 41-50: Checklist 작성 (20개 × 1개씩)
```

### 구현 Phase

```
Session 51-70: 각 체크리스트 실행 (20개 작업)
```

### 결과

```
✅ 70회 세션으로 완전한 주식 거래 플랫폼 구현!

세션 분포:
- Stage 1-2: 6회 (패밀리 분류 + 환경 제약)
- Stage 3: 10회 (ADR 18개 작성)
- Stage 4-6: 14회 (DNA 시스템 구축)
- Stage 7-9: 20회 (Blueprint + Task + Checklist)
- 구현: 20회 (체크리스트 실행)

각 세션의 특징:
- 명확한 입력과 출력
- 일관성 유지 (제약조건 항상 제공)
- 컨텍스트 효율 (필요한 정보만)
- 검증 가능 (산출물 확인)
```

---

## 요약: 백지상태 2호가 기억해야 할 것

### 🎯 프로젝트 목표
```
Stage 1-6를 "단위작업"으로 만들어서
아이디어 → Blueprint까지 완전한 방법론 확립
```

### 🔑 핵심 원칙
```
1. 부분으로 전체 완성 (레고블럭)
   - Q1: 컨텍스트 한계 고려
   - Q2: 의미있는 산출물 생산
   - Q3: 일관성 유지
   - Q4: 누락없음
2. 환경으로 제어 (DNA 시스템)
3. Stage ≠ 한 작업, Stage = 여러 세션 누적
```

### 📦 세 가지 컴포넌트
```
Skills = 지식 (Progressive Disclosure)
Commands = 인터페이스 (간단하게)
Agents = 실행자 (Phase 구조)
```

### 🏗️ 현재 상태
```
| 구분 | Stage 1-6 | Stage 7-9 |
|------|-----------|-----------|
| 방법 유효성 | ❌ 연구 필요 | ✅ 통함 확인 |
| 프레임워크화 | ❌ 미착수 | ❌ 미착수 |

⚠️ 전체 9-Stage 모두 프레임워크화 작업 필요!
```

### 💡 작업 방식
```
각 세션:
1. 명확한 목표 (ADR 3개 작성)
2. 필요한 정보만 제공 (이전 작업 읽기)
3. 일관성 유지 (제약조건 제공)
4. 검증 가능 (산출물 확인)
5. 다음 세션 가이드
```

---

**이 문서를 다 읽었다면, DNA 프로젝트의 전체 맥락을 이해한 것입니다!** 🎉
