# Stage 8: 작업 분해 가이드 (Task Breakdown Guide)

> **목적**: Blueprint를 AI가 한 세션에 완료할 수 있는 크기로 분해
>
> **버전**: v4.1 (2025-12-03)
>
> - v8.0 (2025-12-03): Gemini 연구 기반 전면 재작성, DNA_METHODOLOGY_DETAILED.md 기준
> - v2.0 (2025-11-12): 입력/출력 문서 추가
> - v1.0 (2025-11-10): 초기 버전

---

## 📚 이 가이드의 위치

```
DNA 방법론 문서 체계:

Tier 1: DNA_PROJECT_OVERVIEW_v2.md (전체 맥락)
           ↓
Tier 2: DNA_METHODOLOGY_DETAILED.md (상세 원리) - Part 6.2
           ↓
Tier 3: 이 문서 (Stage 8 실행 가이드) ← 지금 여기!
```

**참조 문서**:
- **원리 이해**: `DNA_METHODOLOGY_DETAILED.md` Part 6.2

---

## 🎯 DNA 핵심 원칙 1: AI 최적 크기

### Stage 8이 DNA 방법론의 변환점인 이유

```
Stage 1-7: 인간 중심 (Human-Driven)
────────────────────────────────────
├─ 패밀리 분류, NFR, ADR, Blueprint
├─ 문서 크기 제한 없음
├─ 인간의 이해와 의사결정 중심
└─ 컨텍스트 = 인간의 기억력

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage 8: 변환점 (Transformation Point) ← 여기!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage 8-9: AI 중심 (AI-Driven)
────────────────────────────────────
├─ Task Breakdown, 9-Step Checklist
├─ AI 컨텍스트 한계 고려 필수!
├─ AI가 100% 성공할 수 있는 크기
└─ 컨텍스트 = 80-90K 토큰 (Claude)
```

### 80-90K 토큰 = 100-150줄 체크리스트

```
왜 이 크기인가?

Claude 컨텍스트 윈도우: 200K 토큰
├─ 시스템 프롬프트: ~30K 토큰
├─ 대화 히스토리: ~20K 토큰
├─ 참조 문서 (Blueprint, Standards): ~50K 토큰
├─ 체크리스트 + 코드: ~20K 토큰
└─ 응답 생성 여유: ~80K 토큰 ← 실제 작업 공간!

체크리스트 → 토큰 변환:
├─ 1줄 ≈ 10-15 토큰 (평균)
├─ 100줄 ≈ 1,000-1,500 토큰
├─ 150줄 ≈ 1,500-2,250 토큰
└─ 코드 예시 포함 시 x2-3배

결론:
├─ 체크리스트: 100-150줄 (1,500-2,000 토큰)
├─ 참조 코드: 200-300줄 (3,000-4,500 토큰)
├─ 생성할 코드: 100-200줄 (1,500-3,000 토큰)
└─ 총: ~10K 토큰 = 여유 있게 처리 가능 ✅
```

### 크기 판단 공식

```python
def is_optimal_task_size(task: Task) -> bool:
    """Task 크기가 AI 최적인지 판단"""
    
    # 1. 체크리스트 줄 수
    checklist_lines = estimate_checklist_lines(task)
    if not (80 <= checklist_lines <= 180):
        return False  # 80줄 미만 = 너무 작음, 180줄 초과 = 너무 큼
    
    # 2. 참조 문서 크기
    reference_tokens = estimate_reference_tokens(task)
    if reference_tokens > 50_000:
        return False  # 참조 문서가 너무 많음
    
    # 3. 예상 생성 코드
    code_lines = estimate_code_lines(task)
    if code_lines > 300:
        return False  # 생성할 코드가 너무 많음
    
    # 4. 테스트 포함 여부
    if not task.includes_tests:
        return False  # 테스트 없는 Task는 불완전
    
    return True

# 적용 예시
is_optimal_task_size(Task("User 엔티티 + 테스트"))  # True (120줄)
is_optimal_task_size(Task("전체 도메인 구현"))      # False (500줄+)
is_optimal_task_size(Task("Enum 하나 추가"))       # False (30줄)
```

### 크기가 맞지 않을 때

| 상황 | 증상 | 해결책 |
|------|------|--------|
| **너무 큼** | 180줄 초과, 4시간+ | 분할 (기능별, 레이어별) |
| **너무 작음** | 80줄 미만, 1시간- | 합치기 (관련 기능끼리) |
| **참조 과다** | Blueprint 전체 필요 | 필요 섹션만 발췌 |
| **의존성 복잡** | 3개+ Task 선행 필요 | 의존성 재설계 |

---

## 🤔 왜 Task Breakdown이 필요한가?

### Blueprint vs Task

```
Blueprint (Stage 7):
├─ 전체 시스템 설계도 (1,000+ 줄)
├─ 모든 도메인, API, DB 설계
├─ AI가 한 번에 처리 불가능!
└─ 컨텍스트 한계 (200K 토큰)

Task (Stage 8):
├─ 하나의 집중된 작업 (2-4시간)
├─ 체크리스트: 100-150줄
├─ AI가 완벽하게 처리 가능!
└─ 독립적 테스트 가능
```

### Task 없이 구현하면?

```
❌ Blueprint 전체를 한 번에:

AI: "Blueprint 보고 전체 구현할게요!"

Session 1:
├─ Order 엔티티 구현 시작
├─ ...중간에 User 필요해서 User도 구현
├─ ...DB 연결도 필요해서 추가
├─ 컨텍스트 80% 소진 😰
└─ "나머지는 다음에..."

Session 2:
├─ "이전 세션에서 뭘 했더라?" 🤔
├─ 중복 코드 작성
├─ 스타일 불일치
└─ 테스트 누락

결과:
├─ 일관성 없는 코드
├─ 테스트 커버리지 50% 미만
├─ "처음부터 다시 해야 하나..." 😱
```

```
✅ Task 단위로 분해 후 구현:

08T-01_task_breakdown.md:
────────────────────────────────
Task 001: User 엔티티 + 테스트 (2h)
Task 002: Order 엔티티 + Aggregate (3h)
Task 003: 값 객체 + 열거형 (1.5h)
...

Session 1: Task 001
├─ 목표: User 엔티티만 집중
├─ 입력: Blueprint Section 3.1
├─ 출력: src/domain/user.py + tests/
├─ 완료! ✅ (MyPy 0, Ruff 0, Coverage 95%)

Session 2: Task 002
├─ 목표: Order 엔티티만 집중
├─ 입력: Blueprint Section 3.1, Task 001 완료
├─ 출력: src/domain/order.py + tests/
├─ 완료! ✅

결과:
├─ 각 Task 100% 완료
├─ 일관된 품질
├─ 전체 커버리지 95%+
└─ "레고 블럭처럼 조립 완료!" 🎉
```

### 비유: 이사 짐 싸기

```
❌ 한 번에 이사:
"모든 짐을 한 박스에!"
→ 박스 터짐, 물건 파손, 찾기 어려움

✅ 체계적 포장:
박스 1: 주방용품 (그릇, 컵)
박스 2: 서재 (책, 문구)
박스 3: 침실 (침구, 옷)
→ 분류 명확, 찾기 쉬움, 안전

Task = 라벨 붙은 이사 박스!
├─ 내용물 명확 (목표)
├─ 크기 적절 (2-4시간)
├─ 독립적 운반 (의존성 최소)
└─ 쉽게 확인 (테스트)
```

---

## 📥 입력 문서

### Stage 7에서 전달받는 것

| 파일 | 핵심 내용 | 이 Stage에서 사용 |
|------|----------|-----------------|
| `07B-01_project_blueprint.md` | 전체 설계도 (9개 섹션) | Task 분해 대상 |
| `06D-01_project_standards.md` | 프로젝트 표준 | Task별 표준 적용 |

---

## 📤 출력 문서

### 필수 산출물

```
docs/
└── 08T-01_task_breakdown.md    # THE 산출물 (작업 분해 목록)
```

---

## 🎯 좋은 Task의 4가지 조건

### 조건 1: 적절한 크기

```
체크리스트 기준:
├─ 100-150줄 범위 (120줄 내외 권장)
├─ 예상 시간: 2-4시간
├─ 컨텍스트: 80-90K 토큰 이내
└─ 💡 숫자는 참고! 작업을 완전하게 설명하는 게 우선

크기 판단 기준:
┌─────────────────┬─────────────┬─────────────┐
│ 구분            │ 너무 작음   │ 적절        │ 너무 큼     │
├─────────────────┼─────────────┼─────────────┼─────────────┤
│ 체크리스트      │ 50줄 미만   │ 100-150줄   │ 200줄 초과  │
│ 예상 시간       │ 1시간 미만  │ 2-4시간     │ 5시간 초과  │
│ 파일 수         │ 1개 미만    │ 1-3개       │ 5개 초과    │
│ 테스트 수       │ 2개 미만    │ 5-15개      │ 20개 초과   │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

### 조건 2: 독립성

```
좋은 Task:
├─ 다른 Task 없이 테스트 가능
├─ 명확한 입력/출력
├─ 자체 완결적
└─ 롤백 가능 (실패해도 다른 Task 영향 없음)

나쁜 Task:
├─ "Order 만들려면 User 먼저 해야 하고..."
├─ "이건 다음 Task에서 마무리할게요"
├─ "테스트는 통합 테스트로 한 번에..."
└─ 얽힌 의존성 = 실패의 도미노
```

### 조건 3: 검증 가능

```
좋은 Task:
├─ 테스트 작성 가능
├─ 성공/실패 판단 명확
├─ 품질 기준 적용 가능
│   ├─ MyPy 0 errors
│   ├─ Ruff 0 violations
│   └─ Coverage 95%+
└─ "이 Task 완료 = 이 기능 작동"

나쁜 Task:
├─ "일단 코드 짜고 나중에 테스트"
├─ "완료 조건: 대충 돌아가면 됨"
├─ 품질 검증 불가
└─ "되는 것 같은데...?" 🤔
```

### 조건 4: 가치 있음

```
좋은 Task:
├─ 완료 시 실제 기능 동작
├─ 데모 가능
├─ 진행 상황 확인 가능
└─ "Task 5개 완료 = 25% 진행"

나쁜 Task:
├─ "설정 파일만 만들기" (가치 없음)
├─ "나중에 쓸 유틸리티 함수" (당장 불필요)
├─ 완료해도 아무것도 작동 안 함
└─ "Task 5개 했는데 뭐가 된 거지?"
```

---

## 🔄 DNA 핵심 원칙 2: 완전해질 때까지 반복

### "부족함이 없어질 때까지"의 의미

```
Task Breakdown의 목표:
├─ AI가 체크리스트만 보고 100% 완료 가능
├─ 추가 질문 없이 독립 실행 가능
├─ 모호함, 누락, 불완전함 = 0
└─ "완전한" Task만 Stage 9로 전달

완전하지 않은 Task의 증상:
❌ "Blueprint 참조"만 있고 구체적 내용 없음
❌ "적절히 구현"같은 모호한 표현
❌ 입력/출력 중 하나라도 누락
❌ 완료 조건이 주관적
❌ 테스트 케이스 미정의
```

### 3단계 검증 프로토콜

```
모든 Task는 3단계 검증을 통과해야 함:

┌─────────────────────────────────────────────────────────┐
│ 검증 1: 크기 (Size Check)                               │
├─────────────────────────────────────────────────────────┤
│ □ 체크리스트 예상 줄 수: 80-180줄?                        │
│ □ 예상 시간: 2-4시간?                                    │
│ □ 생성 파일 수: 1-4개?                                   │
│ □ 테스트 케이스 수: 3-15개?                              │
│                                                         │
│ 실패 시 → 분할 또는 합치기                                │
└─────────────────────────────────────────────────────────┘
            ↓ 통과
┌─────────────────────────────────────────────────────────┐
│ 검증 2: 의존성 (Dependency Check)                       │
├─────────────────────────────────────────────────────────┤
│ □ 선행 Task 명확히 정의?                                 │
│ □ 순환 의존성 없음?                                      │
│ □ 병렬 실행 가능 Task 식별?                              │
│ □ 핵심 경로 계산 가능?                                   │
│                                                         │
│ 실패 시 → 의존성 재설계                                   │
└─────────────────────────────────────────────────────────┘
            ↓ 통과
┌─────────────────────────────────────────────────────────┐
│ 검증 3: 완전성 (Completeness Check)                     │
├─────────────────────────────────────────────────────────┤
│ □ 목표: 한 문장으로 명확?                                 │
│ □ 입력: 모든 참조 문서/코드 명시?                         │
│ □ 출력: 생성될 파일 경로 명시?                            │
│ □ 제약: MUST/MUST NOT 명시?                             │
│ □ 완료 조건: 측정 가능? (MyPy 0, Ruff 0, Coverage 95%)   │
│ □ 테스트: 구체적 케이스 3개 이상?                         │
│                                                         │
│ 실패 시 → Task 상세 보완 후 재검증                        │
└─────────────────────────────────────────────────────────┘
            ↓ 통과
        Stage 9로 전달 ✅
```

### 재작업 사례: "주문 도메인" Task

```
1차 시도 (불완전):
────────────────────────────────────
Task: 주문 도메인 구현
목표: Order 관련 기능 구현
입력: Blueprint
출력: 주문 관련 파일들

검증 1 실패: 크기 불명확 (몇 줄? 몇 시간?)
검증 3 실패: 목표 모호, 출력 불명확

2차 시도 (분할 후에도 불완전):
────────────────────────────────────
Task 002: Order 엔티티 구현
목표: Order 클래스 작성
입력: Blueprint Section 3.1
출력: src/domain/order.py

검증 3 실패: 테스트 누락, 완료 조건 주관적

3차 시도 (완전!):
────────────────────────────────────
Task 002: Order 엔티티 + Aggregate + 테스트
목표: Order Aggregate Root 구현 (엔티티 + 상태 전이 + 도메인 이벤트)
입력: 
  - Blueprint Section 3.1 (Order 필드)
  - Blueprint Section 3.3 (Aggregate 규칙)
  - core/types (OrderId, Money, OrderStatus)
출력:
  - src/domain/entities/order.py
  - tests/unit/domain/test_order.py
제약:
  - MUST: 상태 전이 로직 (pending → submitted → filled)
  - MUST: 도메인 이벤트 발행
  - MUST NOT: DB 접근 코드
완료 조건:
  - MyPy 0 errors
  - Ruff 0 violations  
  - Coverage 95%+
  - 상태 전이 테스트 4개 포함
테스트 케이스:
  - test_order_creation
  - test_order_submit_success
  - test_order_submit_invalid_state
  - test_order_fill_success
  - test_order_cancel_success
  - test_order_cancel_already_filled

검증 1 통과: 120줄, 3시간, 2파일, 6테스트 ✅
검증 2 통과: 의존성 없음 ✅
검증 3 통과: 모든 항목 명시 ✅

→ Stage 9로 전달!
```

---

## 📋 작성 단계 (Part 1-4)

### Part 1: Blueprint 섹션별 Task 도출 (1시간)

#### Step 1: Blueprint 9개 섹션 → Task 후보

```
Blueprint 섹션 → Task 후보:

섹션 3 (도메인 모델):
├─ Task: User 엔티티 + 테스트
├─ Task: Order 엔티티 + Aggregate + 테스트
├─ Task: Portfolio + Position 엔티티 + 테스트
└─ Task: 값 객체 + 열거형 + 테스트

섹션 4 (API):
├─ Task: Orders API 엔드포인트 (CRUD)
├─ Task: Portfolio API 엔드포인트
├─ Task: Auth API 엔드포인트
└─ Task: 미들웨어 (인증, 로깅, 에러 처리)

섹션 5 (데이터베이스):
├─ Task: 마이그레이션 (users, orders 테이블)
├─ Task: 마이그레이션 (portfolios, positions 테이블)
└─ Task: 리포지토리 구현

섹션 6 (외부 연동):
├─ Task: KIS API 클라이언트 (인증)
├─ Task: KIS API 클라이언트 (주문)
└─ Task: Rate Limiter + 재시도 로직
```

#### Step 2: Task 크기 검증

```python
# 각 Task 크기 검증

def validate_task_size(task):
    """Task 크기가 적절한지 검증"""
    
    # 체크리스트 예상 줄 수
    checklist_lines = estimate_checklist_lines(task)
    if checklist_lines < 80:
        return "너무 작음 - 다른 Task와 합치기"
    if checklist_lines > 180:
        return "너무 큼 - 분할 필요"
    
    # 예상 시간
    estimated_hours = estimate_hours(task)
    if estimated_hours < 1.5:
        return "너무 작음"
    if estimated_hours > 5:
        return "너무 큼"
    
    return "적절함 ✅"

# 예시
validate_task_size("User 엔티티 + 테스트")  # → "적절함 ✅" (2시간)
validate_task_size("전체 API 구현")          # → "너무 큼" (20시간)
validate_task_size("Enum 하나 추가")         # → "너무 작음" (20분)
```

### Part 2: RDoLT 적용 - 난이도별 분류 (30분)

#### RDoLT: Recursive Decomposition of Logical Thoughts

```
난이도 3단계:

Level 1 - Easy (기본 기능):
────────────────────────────────
├─ 단순 CRUD
├─ 기본 모델 정의
├─ 단순 API 엔드포인트
├─ 명확한 로직
└─ 의존성 없음 또는 최소

예: Task 001 (User 엔티티), Task 003 (값 객체)

Level 2 - Intermediate (상호작용):
────────────────────────────────
├─ 엔티티 간 관계
├─ 트랜잭션 로직
├─ 서비스 계층 통합
├─ 검증 로직
└─ Easy Task에 의존

예: Task 005 (주문 생성 서비스), Task 007 (API 엔드포인트)

Level 3 - Final (엣지 케이스):
────────────────────────────────
├─ 에러 처리 고도화
├─ 동시성 제어
├─ 성능 최적화
├─ 보안 검증
├─ 예외 상황 처리
└─ Intermediate Task에 의존

예: Task 015 (주문 동시성 처리), Task 016 (KIS API 연동)

작업 순서:
Easy → Intermediate → Final
(기반 먼저, 복잡한 것 나중)
```

#### 분류 예시

```
주식 거래 플랫폼 Task 분류:

Phase 1: Easy (기반)
────────────────────────────────
001. User 엔티티 + 테스트         [2h] [의존성: 없음]
002. Order 엔티티 + Aggregate     [3h] [의존성: 없음]
003. Portfolio 엔티티 + Position  [2.5h] [의존성: 없음]
004. 값 객체 + 열거형             [1.5h] [의존성: 없음]
005. 마이그레이션 (users, orders) [2h] [의존성: 001, 002]

Phase 2: Intermediate (상호작용)
────────────────────────────────
006. User 리포지토리              [2h] [의존성: 001, 005]
007. Order 리포지토리             [2.5h] [의존성: 002, 005]
008. 주문 생성 서비스             [4h] [의존성: 007, 004]
009. 주문 조회 서비스             [2h] [의존성: 007]
010. Auth API (로그인, 토큰)      [3h] [의존성: 006]
011. Orders API (CRUD)           [3.5h] [의존성: 008, 009]

Phase 3: Final (엣지 케이스)
────────────────────────────────
012. 인증 미들웨어 + 권한 검증     [3h] [의존성: 010]
013. KIS API 클라이언트 (인증)    [3h] [의존성: 없음]
014. KIS API 클라이언트 (주문)    [4h] [의존성: 013, 008]
015. 주문 동시성 처리             [4h] [의존성: 008, 014]
016. Rate Limiter + 재시도       [3h] [의존성: 013]
017. 전체 통합 테스트             [3h] [의존성: 모든 Task]
```

### Part 3: 의존성 다이어그램 작성 (30분)

#### 의존성 시각화

```
의존성 다이어그램:

Phase 1 (Easy):
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│ 001 │  │ 002 │  │ 003 │  │ 004 │
│User │  │Order│  │Port.│  │Value│
└──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
   │        │        │        │
   └────────┼────────┼────────┘
            │        │
            ▼        │
         ┌─────┐     │
         │ 005 │     │
         │Migr.│     │
         └──┬──┘     │
            │        │
Phase 2:    ▼        ▼
         ┌─────┐  ┌─────┐
         │ 006 │  │ 007 │
         │U.Rep│  │O.Rep│
         └──┬──┘  └──┬──┘
            │        │
            ▼        ▼
         ┌─────┐  ┌─────┐
         │ 010 │  │ 008 │──→ ┌─────┐
         │Auth │  │O.Svc│    │ 009 │
         └──┬──┘  └──┬──┘    │O.Qry│
            │        │       └─────┘
Phase 3:    ▼        ▼
         ┌─────┐  ┌─────┐  ┌─────┐
         │ 012 │  │ 014 │  │ 015 │
         │Auth │  │KIS  │  │Conc.│
         │Midw.│  │Order│  └─────┘
         └─────┘  └──┬──┘
                     │
                  ┌──┴──┐
                  │ 013 │
                  │KIS  │
                  │Auth │
                  └─────┘
```

#### 핵심 경로 (Critical Path)

```
핵심 경로: 전체 일정을 결정하는 최장 경로

001 (User, 2h)
  ↓
005 (Migration, 2h)
  ↓
006 (User Repo, 2h)
  ↓
010 (Auth API, 3h)
  ↓
012 (Auth Middleware, 3h)
────────────────────────
총: 12시간 (최소 4일)

병렬 실행 가능:
├─ 002, 003, 004는 001과 동시에
├─ 007, 008, 009는 005 이후 006과 병렬
└─ 013, 016은 독립적으로 언제든지
```

### Part 4: Task 상세 정의 (1시간)

#### 각 Task 상세 작성

```markdown
## Task 001: User 엔티티 + 테스트

### 메타 정보
- **ID**: 001
- **난이도**: Easy (Level 1)
- **예상 시간**: 2시간
- **의존성**: 없음

### 목표
User 엔티티 클래스 구현 및 단위 테스트 작성

### 입력
- Blueprint Section 3.1 (User 엔티티)
- PROJECT_STANDARDS.md (네이밍 규칙)
- core/types (UserId, EmailStr)

### 출력
- `src/domain/entities/user.py`
- `tests/unit/domain/test_user.py`
- 커버리지 95%+

### 제약
- MUST: Pydantic BaseModel 사용
- MUST: UserId (UUID) 타입 사용
- MUST: created_at, updated_at UTC 시간
- MUST NOT: SQLAlchemy 직접 사용 (Infrastructure 레이어)

### 완료 조건
- [ ] MyPy 0 errors
- [ ] Ruff 0 violations
- [ ] pytest 통과
- [ ] Coverage 95%+

---

## Task 002: Order 엔티티 + Aggregate + 테스트

### 메타 정보
- **ID**: 002
- **난이도**: Easy (Level 1)
- **예상 시간**: 3시간
- **의존성**: 없음 (Task 001과 병렬 가능)

### 목표
Order Aggregate Root 구현 (엔티티 + 도메인 로직 + 테스트)

### 입력
- Blueprint Section 3.1 (Order 엔티티)
- Blueprint Section 3.3 (Aggregate)
- core/types (OrderId, Money, OrderStatus)

### 출력
- `src/domain/entities/order.py`
- `tests/unit/domain/test_order.py`
- 커버리지 95%+

### 제약
- MUST: Aggregate Root 패턴 적용
- MUST: 상태 전이 로직 (pending → submitted → filled)
- MUST: 도메인 이벤트 발행 (OrderCreated, OrderSubmitted)
- MUST NOT: 데이터베이스 접근 코드

### 완료 조건
- [ ] MyPy 0 errors
- [ ] Ruff 0 violations
- [ ] pytest 통과
- [ ] 상태 전이 테스트 포함
- [ ] Coverage 95%+
```



---

## 📄 Task Breakdown 템플릿

### 08T-01_task_breakdown.md

```markdown
# Task Breakdown

> **프로젝트**: [프로젝트명]
> **버전**: v1.0
> **작성일**: YYYY-MM-DD
> **Blueprint 참조**: 07B-01_project_blueprint.md

---

## 개요

| 항목 | 값 |
|------|---|
| 총 Task 수 | [N]개 |
| 예상 총 시간 | [X]시간 |
| 예상 세션 수 | [Y]세션 (Task당 1세션) |
| 핵심 경로 | Task 001 → 005 → 008 → 014 |

---

## Phase 1: Easy (기반)

> 의존성 없음, 병렬 실행 가능

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 001 | [Task명] | [X]h | 없음 | Section 3.1 |
| 002 | [Task명] | [X]h | 없음 | Section 3.1 |
| ... | ... | ... | ... | ... |

---

## Phase 2: Intermediate (상호작용)

> Phase 1 완료 후 진행

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 006 | [Task명] | [X]h | 001, 005 | Section 4.2 |
| 007 | [Task명] | [X]h | 002, 005 | Section 4.2 |
| ... | ... | ... | ... | ... |

---

## Phase 3: Final (엣지 케이스)

> Phase 2 완료 후 진행

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 012 | [Task명] | [X]h | 010 | Section 8.1 |
| 015 | [Task명] | [X]h | 008, 014 | Section 6.1 |
| ... | ... | ... | ... | ... |

---

## 의존성 다이어그램

```
Phase 1:
┌─────┐  ┌─────┐  ┌─────┐
│ 001 │  │ 002 │  │ 003 │
└──┬──┘  └──┬──┘  └──┬──┘
   │        │        │
   └────────┼────────┘
            ▼
         ┌─────┐
         │ 005 │
         └──┬──┘
            │
Phase 2:    ▼
         ┌─────┐
         │ 008 │
         └──┬──┘
            │
Phase 3:    ▼
         ┌─────┐
         │ 014 │
         └─────┘
```

---

## Task 상세

### Task 001: [Task명]

#### 메타 정보
- **ID**: 001
- **난이도**: Easy
- **예상 시간**: [X]시간
- **의존성**: 없음

#### 목표
[한 문장으로 명확하게]

#### 입력
- Blueprint Section [X.X]
- PROJECT_STANDARDS.md
- [추가 참조]

#### 출력
- `[파일 경로]`
- `[테스트 파일 경로]`
- 커버리지 95%+

#### 제약
- MUST: [필수 사항]
- MUST NOT: [금지 사항]

#### 완료 조건
- [ ] MyPy 0 errors
- [ ] Ruff 0 violations
- [ ] pytest 통과
- [ ] Coverage 95%+

---

### Task 002: [Task명]

[같은 형식으로 반복...]

---

## 우선순위 및 일정

### 핵심 경로 (Critical Path)

```
001 → 005 → 008 → 014 → 017
 2h    2h    4h    4h    3h = 15시간 (최소 4일)
```

### 병렬 실행 가능

```
Day 1: 001, 002, 003, 004 (병렬)
Day 2: 005, 013 (병렬)
Day 3: 006, 007 (병렬)
Day 4: 008, 009, 010 (병렬)
Day 5: 011, 012, 016 (병렬)
Day 6: 014, 015 (병렬)
Day 7: 017 (통합)
```

---

## 다음 단계

→ Stage 9: 각 Task마다 9-Step Checklist 작성
→ 체크리스트 파일: `09L-001_*.md`, `09L-002_*.md`, ...
```

---

## ✏️ 작성 예시: 주식 거래 플랫폼

### 예시 1: 전체 Task Breakdown

```markdown
# Task Breakdown - 주식 거래 플랫폼

> **프로젝트**: Stock Trading Platform
> **버전**: v1.0
> **작성일**: 2025-12-03
> **Blueprint 참조**: 07B-01_project_blueprint.md

---

## 개요

| 항목 | 값 |
|------|---|
| 총 Task 수 | 17개 |
| 예상 총 시간 | 48시간 |
| 예상 세션 수 | 17세션 |
| 핵심 경로 | 001 → 005 → 006 → 010 → 012 (12h) |

---

## Phase 1: Easy (기반)

> 의존성 없음, 병렬 실행 가능

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 001 | User 엔티티 + 테스트 | 2h | 없음 | Section 3.1 |
| 002 | Order 엔티티 + Aggregate | 3h | 없음 | Section 3.1, 3.3 |
| 003 | Portfolio + Position 엔티티 | 2.5h | 없음 | Section 3.1 |
| 004 | 값 객체 + 열거형 | 1.5h | 없음 | Section 3.2 |
| 005 | 마이그레이션 (users, orders) | 2h | 001, 002 | Section 5.1 |

**Phase 1 소계**: 11시간

---

## Phase 2: Intermediate (상호작용)

> Phase 1 완료 후 진행

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 006 | User 리포지토리 | 2h | 001, 005 | Section 5.1 |
| 007 | Order 리포지토리 | 2.5h | 002, 005 | Section 5.1 |
| 008 | 주문 생성 서비스 | 4h | 004, 007 | Section 4.2 |
| 009 | 주문 조회 서비스 | 2h | 007 | Section 4.2 |
| 010 | Auth API (로그인, 토큰) | 3h | 006 | Section 4.1, 8.1 |
| 011 | Orders API (CRUD) | 3.5h | 008, 009 | Section 4.1 |

**Phase 2 소계**: 17시간

---

## Phase 3: Final (엣지 케이스)

> Phase 2 완료 후 진행

| ID | Task | 예상 | 의존성 | Blueprint 참조 |
|----|------|------|--------|---------------|
| 012 | 인증 미들웨어 + 권한 검증 | 3h | 010 | Section 8.2 |
| 013 | KIS API 클라이언트 (인증) | 3h | 없음 | Section 6.1 |
| 014 | KIS API 클라이언트 (주문) | 4h | 008, 013 | Section 6.1 |
| 015 | 주문 동시성 처리 | 4h | 008, 014 | Section 6.1 |
| 016 | Rate Limiter + 재시도 | 3h | 013 | Section 6.1 |
| 017 | 전체 통합 테스트 | 3h | 모든 Task | - |

**Phase 3 소계**: 20시간

---

## 의존성 다이어그램

```
Phase 1 (Easy):
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│ 001 │  │ 002 │  │ 003 │  │ 004 │
│User │  │Order│  │Port.│  │Value│
│ 2h  │  │ 3h  │  │2.5h │  │1.5h │
└──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
   │        │        │        │
   └────┬───┴────────┘        │
        │                     │
        ▼                     │
     ┌─────┐                  │
     │ 005 │                  │
     │Migr.│                  │
     │ 2h  │                  │
     └──┬──┘                  │
        │                     │
        ├──────────────┬──────┘
        │              │
Phase 2 ▼              ▼
     ┌─────┐        ┌─────┐
     │ 006 │        │ 007 │
     │U.Rep│        │O.Rep│
     │ 2h  │        │2.5h │
     └──┬──┘        └──┬──┘
        │              │
        ▼              ▼
     ┌─────┐        ┌─────┐───→ ┌─────┐
     │ 010 │        │ 008 │     │ 009 │
     │Auth │        │O.Svc│     │O.Qry│
     │ 3h  │        │ 4h  │     │ 2h  │
     └──┬──┘        └──┬──┘     └──┬──┘
        │              │           │
        │              └─────┬─────┘
Phase 3 ▼                    ▼
     ┌─────┐              ┌─────┐
     │ 012 │              │ 011 │
     │Auth │              │Order│
     │Midw.│              │ API │
     │ 3h  │              │3.5h │
     └─────┘              └─────┘

                ┌─────┐
                │ 013 │ ← 독립 (Phase 3 시작 가능)
                │KIS  │
                │Auth │
                │ 3h  │
                └──┬──┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
     ┌─────┐    ┌─────┐    ┌─────┐
     │ 014 │    │ 015 │    │ 016 │
     │KIS  │    │Conc.│    │Rate │
     │Order│    │ 4h  │    │Limit│
     │ 4h  │    └─────┘    │ 3h  │
     └─────┘               └─────┘
                   │
                   ▼
                ┌─────┐
                │ 017 │
                │Integ│
                │Test │
                │ 3h  │
                └─────┘
```

---

## 우선순위 및 일정

### 핵심 경로 (Critical Path)

```
001 (2h) → 005 (2h) → 006 (2h) → 010 (3h) → 012 (3h)
─────────────────────────────────────────────────────
총: 12시간 = 최소 3일 (하루 4시간 기준)
```

### 병렬 실행 계획

```
Day 1: 
├─ 001 User 엔티티 (2h)
├─ 002 Order 엔티티 (3h) ← 병렬
├─ 003 Portfolio 엔티티 (2.5h) ← 병렬
└─ 004 값 객체 (1.5h) ← 병렬

Day 2:
├─ 005 마이그레이션 (2h)
└─ 013 KIS API 인증 (3h) ← 병렬 (독립)

Day 3:
├─ 006 User 리포지토리 (2h)
├─ 007 Order 리포지토리 (2.5h) ← 병렬
└─ 016 Rate Limiter (3h) ← 병렬 (013 의존)

Day 4:
├─ 008 주문 생성 서비스 (4h)
├─ 009 주문 조회 서비스 (2h) ← 병렬
└─ 010 Auth API (3h) ← 병렬

Day 5:
├─ 011 Orders API (3.5h)
├─ 012 인증 미들웨어 (3h) ← 병렬
└─ 014 KIS API 주문 (4h) ← 병렬

Day 6:
├─ 015 주문 동시성 처리 (4h)
└─ 017 전체 통합 테스트 (3h)
```

**총 예상**: 6일 (하루 4-5시간, 2-3세션)
```

### 예시 2: 개별 Task 상세

```markdown
## Task 008: 주문 생성 서비스

### 메타 정보
- **ID**: 008
- **난이도**: Intermediate (Level 2)
- **예상 시간**: 4시간
- **의존성**: 004 (값 객체), 007 (Order 리포지토리)

### 목표
주문 생성 유스케이스 구현 - 검증, 생성, 이벤트 발행

### 입력
- Blueprint Section 4.2 (POST /api/v1/orders)
- Blueprint Section 3.3 (Order Aggregate)
- PROJECT_STANDARDS.md (서비스 레이어 규칙)
- core/logging, core/errors

### 출력
```
src/application/orders/
├── __init__.py
├── commands.py          # CreateOrderCommand
├── services.py          # OrderService.create_order()
└── exceptions.py        # OrderCreationError

tests/unit/application/orders/
├── __init__.py
└── test_order_service.py
```

### 제약
- MUST: CreateOrderCommand (Pydantic) 사용
- MUST: Order Aggregate 도메인 규칙 적용
- MUST: OrderCreated 이벤트 발행
- MUST: 잔고 검증 포함
- MUST: 트랜잭션 경계 명확히
- MUST NOT: 직접 DB 접근 (리포지토리 사용)
- MUST NOT: API 레이어 의존

### 핵심 로직

```python
# src/application/orders/services.py

class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        portfolio_repo: PortfolioRepository,
        event_publisher: EventPublisher,
        logger: Logger,
    ) -> None:
        self._order_repo = order_repo
        self._portfolio_repo = portfolio_repo
        self._event_publisher = event_publisher
        self._logger = logger

    async def create_order(
        self,
        command: CreateOrderCommand,
    ) -> Order:
        """주문 생성"""
        self._logger.info("주문 생성 시작", user_id=str(command.user_id))
        
        # 1. 잔고 검증
        portfolio = await self._portfolio_repo.get_by_user_id(command.user_id)
        if not portfolio.has_sufficient_balance(command.total_amount):
            raise InsufficientBalanceError(
                required=command.total_amount,
                available=portfolio.cash_balance,
            )
        
        # 2. Order Aggregate 생성
        order = Order.create(
            user_id=command.user_id,
            symbol=command.symbol,
            side=command.side,
            order_type=command.order_type,
            quantity=command.quantity,
            price=command.price,
        )
        
        # 3. 저장
        await self._order_repo.save(order)
        
        # 4. 이벤트 발행
        for event in order.domain_events:
            await self._event_publisher.publish(event)
        
        self._logger.info("주문 생성 완료", order_id=str(order.id))
        return order
```

### 테스트 케이스

```python
# tests/unit/application/orders/test_order_service.py

class TestOrderService:
    """주문 생성 서비스 테스트"""
    
    async def test_create_order_success(self):
        """정상 주문 생성"""
        # Given
        command = CreateOrderCommand(
            user_id=UserId(uuid4()),
            symbol="005930",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=10,
            price=Money(70000),
        )
        
        # When
        order = await service.create_order(command)
        
        # Then
        assert order.status == OrderStatus.PENDING
        assert order.symbol == "005930"
        assert len(order.domain_events) == 1
        assert isinstance(order.domain_events[0], OrderCreated)
    
    async def test_create_order_insufficient_balance(self):
        """잔고 부족 시 실패"""
        # Given
        portfolio_repo.get_by_user_id.return_value = Portfolio(
            cash_balance=Money(100000)
        )
        command = CreateOrderCommand(
            quantity=100,
            price=Money(70000),  # 총 7,000,000원 필요
        )
        
        # When/Then
        with pytest.raises(InsufficientBalanceError):
            await service.create_order(command)
    
    async def test_create_order_market_type_no_price(self):
        """시장가 주문은 가격 없음"""
        command = CreateOrderCommand(
            order_type=OrderType.MARKET,
            price=None,  # OK
        )
        order = await service.create_order(command)
        assert order.price is None
    
    async def test_create_order_limit_type_requires_price(self):
        """지정가 주문은 가격 필수"""
        command = CreateOrderCommand(
            order_type=OrderType.LIMIT,
            price=None,  # Error!
        )
        with pytest.raises(ValidationError):
            await service.create_order(command)
```

### 완료 조건
- [ ] MyPy 0 errors
- [ ] Ruff 0 violations
- [ ] pytest 통과 (4개 테스트 케이스)
- [ ] Coverage 95%+
- [ ] 잔고 검증 로직 작동
- [ ] 도메인 이벤트 발행
- [ ] 로깅 (INFO: 시작/완료, ERROR: 실패)
```



---

## ✅ Stage 8 완료 체크리스트

### Blueprint 분석

- [ ] Blueprint 9개 섹션 검토
- [ ] 각 섹션에서 Task 후보 도출
- [ ] Task 크기 검증 (100-150줄 체크리스트)

### Task 분류 (RDoLT)

- [ ] Phase 1 (Easy) Task 정의
- [ ] Phase 2 (Intermediate) Task 정의
- [ ] Phase 3 (Final) Task 정의
- [ ] 각 Task 난이도 적절성 확인

### 의존성 분석

- [ ] 각 Task 의존성 명시
- [ ] 의존성 다이어그램 작성
- [ ] 핵심 경로 (Critical Path) 식별
- [ ] 병렬 실행 가능 Task 식별

### Task 상세 정의

- [ ] 각 Task 메타 정보 (ID, 난이도, 예상 시간)
- [ ] 각 Task 목표 (한 문장)
- [ ] 각 Task 입력/출력 명시
- [ ] 각 Task 제약 (MUST/MUST NOT)
- [ ] 각 Task 완료 조건 (MyPy 0, Ruff 0, Coverage 95%)

### 일정 계획

- [ ] 핵심 경로 시간 계산
- [ ] 병렬 실행 계획
- [ ] 일별 Task 배치

### 산출물

- [ ] `08T-01_task_breakdown.md` 작성
- [ ] Stage 9 전달 준비

---

## 🔗 Stage 8 → Stage 9 연결

### Stage 9에 전달하는 것

| 전달 항목 | 내용 | 용도 |
|----------|------|------|
| Task 목록 | 001~017 (17개) | 체크리스트 작성 대상 |
| Task 상세 | 목표, 입출력, 제약 | 체크리스트 내용 |
| 의존성 | Task 간 관계 | 작업 순서 |

### Stage 9 미리보기

```
Stage 9: 9-Step Checklist + 구현

목표: 각 Task마다 TDD 기반 9-Step 체크리스트 작성

9-Step 구조:
────────────────────────────────
Step 1: 목표 이해 📖
Step 2: 테스트 작성 🧪 (TDD - Red)
Step 3: 구현 🔨 (TDD - Green)
Step 4: 정적 검증 🔍 (Ruff, MyPy)
Step 5: 리팩토링 ✨ (TDD - Refactor)
Step 6: 커버리지 📊 (95%+)
Step 7: 통합 확인 🔗
Step 8: 문서화 📝
Step 9: 완료 확인 ✅

체크리스트 파일:
├─ 09L-001_user_entity.md
├─ 09L-002_order_entity.md
├─ 09L-003_portfolio_entity.md
├─ ...
└─ 09L-017_integration_test.md
```

### 체크리스트 크기 예상

```
각 Task별 체크리스트:

Task 001 (User 엔티티):
├─ Step 1: 10줄
├─ Step 2: 30줄 (테스트 코드)
├─ Step 3: 25줄 (구현 코드)
├─ Step 4: 5줄 (명령어)
├─ Step 5: 10줄
├─ Step 6: 5줄
├─ Step 7: 5줄
├─ Step 8: 5줄
└─ Step 9: 5줄
────────────────────────────
총: ~100줄 ✅

Task 008 (주문 생성 서비스):
├─ Step 1: 15줄
├─ Step 2: 50줄 (테스트 코드)
├─ Step 3: 40줄 (구현 코드)
├─ Step 4: 5줄
├─ Step 5: 15줄
├─ Step 6: 5줄
├─ Step 7: 10줄
├─ Step 8: 5줄
└─ Step 9: 5줄
────────────────────────────
총: ~150줄 ✅
```

---

## 💡 핵심 원칙 요약

### 좋은 Task의 4가지 조건

```
1. 적절한 크기:
   ├─ 체크리스트: 100-150줄
   ├─ 예상 시간: 2-4시간
   └─ 컨텍스트: 80-90K 토큰 이내

2. 독립성:
   ├─ 다른 Task 없이 테스트 가능
   ├─ 자체 완결적
   └─ 롤백 가능

3. 검증 가능:
   ├─ MyPy 0 errors
   ├─ Ruff 0 violations
   └─ Coverage 95%+

4. 가치 있음:
   ├─ 완료 시 실제 기능 작동
   └─ 진행 상황 확인 가능
```

### RDoLT 적용

```
Level 1 - Easy (기반):
├─ 단순 모델, 기본 CRUD
├─ 의존성 없음
└─ 예: User 엔티티, 값 객체

Level 2 - Intermediate (상호작용):
├─ 엔티티 간 관계, 서비스
├─ Easy Task에 의존
└─ 예: 주문 생성 서비스, API

Level 3 - Final (엣지 케이스):
├─ 동시성, 외부 연동, 보안
├─ Intermediate Task에 의존
└─ 예: KIS API 연동, 동시성 처리

순서: Easy → Intermediate → Final
```

### Task Breakdown 작성 흐름

```
Blueprint (1,000+ 줄)
        ↓
    섹션별 분석
        ↓
    Task 후보 도출
        ↓
    크기 검증 (100-150줄?)
        ↓
    RDoLT 분류 (Easy/Intermediate/Final)
        ↓
    의존성 분석
        ↓
    핵심 경로 계산
        ↓
    병렬 실행 계획
        ↓
    Task 상세 정의
        ↓
08T-01_task_breakdown.md (16-25 Tasks)
        ↓
    Stage 9: 체크리스트
```

---

## 🎯 Task 크기 판단 가이드

### 크기가 적절한지 확인하는 질문

```
1. 체크리스트 예상 줄 수?
   - 80줄 미만 → 너무 작음 (합치기)
   - 80-180줄 → 적절 ✅
   - 180줄 초과 → 너무 큼 (분할)

2. 예상 시간?
   - 1.5시간 미만 → 너무 작음
   - 2-4시간 → 적절 ✅
   - 5시간 초과 → 너무 큼

3. 생성되는 파일 수?
   - 0개 → 가치 없음
   - 1-3개 → 적절 ✅
   - 5개 초과 → 너무 큼

4. 테스트 케이스 수?
   - 2개 미만 → 너무 작음
   - 5-15개 → 적절 ✅
   - 20개 초과 → 너무 큼

5. 독립적으로 테스트 가능?
   - Yes → 적절 ✅
   - No → 분할 또는 의존성 재검토
```

### 분할 패턴

```
너무 큰 Task 분할 예시:

❌ "Order 도메인 전체 구현" (20시간)
    ↓ 분할
✅ Task 002: Order 엔티티 + Aggregate (3h)
✅ Task 007: Order 리포지토리 (2.5h)
✅ Task 008: 주문 생성 서비스 (4h)
✅ Task 009: 주문 조회 서비스 (2h)
✅ Task 011: Orders API (3.5h)

분할 기준:
├─ 레이어별 분할 (Domain → Application → API)
├─ 기능별 분할 (생성 → 조회 → 수정 → 삭제)
└─ 의존성별 분할 (기반 → 활용)
```

### 합치기 패턴

```
너무 작은 Task 합치기 예시:

❌ Task A: "OrderStatus Enum 정의" (20분)
❌ Task B: "OrderType Enum 정의" (20분)
❌ Task C: "Money 값 객체 정의" (30분)
    ↓ 합치기
✅ Task 004: 값 객체 + 열거형 (1.5h)

합치기 기준:
├─ 같은 레이어
├─ 같은 도메인
├─ 의존성 없음 (서로 독립)
└─ 총 시간 2-4시간 범위
```

---

## 🧩 DNA 핵심 원칙 3: 기능별 분해 + 연결부 + 조립

### 레이어별 vs 기능별 분해

```
❌ 레이어별 분해 (Anti-pattern):
────────────────────────────────────
Task 001: 모든 엔티티 (Domain Layer)
Task 002: 모든 리포지토리 (Infrastructure Layer)
Task 003: 모든 서비스 (Application Layer)
Task 004: 모든 API (Presentation Layer)

문제점:
├─ Task 001 완료해도 "작동하는 기능" 없음
├─ Task 004까지 가야 첫 기능 작동
├─ 중간 검증 불가
├─ 실패 시 전체 재작업
└─ "레고 블럭만 있고 조립된 것 없음"

✅ 기능별 분해 (Best Practice):
────────────────────────────────────
Task 001: User 기능 (Entity + Repo + Service + API)
Task 002: Order 생성 기능 (Entity + Repo + Service + API)
Task 003: Order 조회 기능 (Repo + Service + API)
Task 004: Order 취소 기능 (Service + API)

장점:
├─ Task 001 완료 = User 기능 작동!
├─ 각 Task 완료 시 데모 가능
├─ 중간 검증 가능
├─ 실패 시 해당 기능만 재작업
└─ "조립된 레고 작품이 하나씩 완성"
```

### 기능별 분해 비교표

| 관점 | 레이어별 분해 | 기능별 분해 |
|------|-------------|-----------|
| **Task 완료 시** | 레이어 일부 완성 | 기능 완성 (End-to-End) |
| **테스트** | 단위 테스트만 | 단위 + 통합 테스트 |
| **데모** | 불가능 | 가능 (API 호출 가능) |
| **실패 영향** | 전체 지연 | 해당 기능만 지연 |
| **병렬화** | 어려움 | 쉬움 (기능별 독립) |
| **진행 측정** | 모호함 | 명확함 ("3/10 기능 완료") |

### 연결부 (Interface) 설계

```python
# 기능별 분해 시 연결부가 핵심!

# ❌ 연결부 없이 분해:
Task 001: User 기능 (UserService 직접 구현)
Task 002: Order 기능 (UserService 필요... 어떻게?)

# ✅ 연결부 먼저 정의:
Task 000: 인터페이스 정의 (연결부)
├─ IUserRepository
├─ IOrderRepository
├─ IUserService
└─ IOrderService

Task 001: User 기능 (IUserRepository, IUserService 구현)
Task 002: Order 기능 (IUserService 주입받아 사용)
```

### 연결부 설계 방법

```python
# src/domain/interfaces/repositories.py (Task 000에서 정의)

from abc import ABC, abstractmethod
from typing import Protocol

class IUserRepository(Protocol):
    """User 저장소 인터페이스"""
    async def get_by_id(self, user_id: UserId) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def save(self, user: User) -> None: ...

class IOrderRepository(Protocol):
    """Order 저장소 인터페이스"""
    async def get_by_id(self, order_id: OrderId) -> Order | None: ...
    async def get_by_user_id(self, user_id: UserId) -> list[Order]: ...
    async def save(self, order: Order) -> None: ...

# src/application/interfaces/services.py (Task 000에서 정의)

class IUserService(Protocol):
    """User 서비스 인터페이스"""
    async def get_user(self, user_id: UserId) -> User: ...
    async def create_user(self, command: CreateUserCommand) -> User: ...

class IOrderService(Protocol):
    """Order 서비스 인터페이스"""
    async def create_order(self, command: CreateOrderCommand) -> Order: ...
    async def get_order(self, order_id: OrderId) -> Order: ...
```

### 조립 전략

```
조립 순서 (기능별 분해 후):

Phase 1: 연결부 정의 (Task 000)
────────────────────────────────────
├─ 모든 인터페이스 정의
├─ 타입 힌트만 있는 빈 껍데기
├─ 예상 시간: 1-2시간
└─ 이후 모든 Task가 이 인터페이스 사용

Phase 2: 핵심 기능 (Task 001-005)
────────────────────────────────────
├─ 각 기능별 End-to-End 구현
├─ 인터페이스 구현체 작성
├─ Mock으로 다른 기능 대체
└─ 각 Task 완료 시 해당 기능 작동

Phase 3: 연결 (Task 006-008)
────────────────────────────────────
├─ Mock → 실제 구현체 교체
├─ 기능 간 통합 테스트
├─ E2E 테스트 추가
└─ 전체 시스템 작동 확인
```

### 조립 예시: 주문 생성 기능

```python
# Task 002: Order 생성 기능

# 1. 인터페이스 사용 (Task 000에서 정의된 것)
from src.domain.interfaces import IOrderRepository, IUserRepository

# 2. 서비스 구현
class OrderService:
    def __init__(
        self,
        order_repo: IOrderRepository,  # 인터페이스!
        user_repo: IUserRepository,    # 인터페이스!
    ):
        self._order_repo = order_repo
        self._user_repo = user_repo
    
    async def create_order(self, command: CreateOrderCommand) -> Order:
        # User 검증 (IUserRepository 사용)
        user = await self._user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id)
        
        # Order 생성
        order = Order.create(...)
        
        # 저장 (IOrderRepository 사용)
        await self._order_repo.save(order)
        return order

# 3. 테스트 (Mock 사용)
async def test_create_order():
    # Mock 리포지토리
    user_repo = Mock(spec=IUserRepository)
    user_repo.get_by_id.return_value = User(...)
    
    order_repo = Mock(spec=IOrderRepository)
    
    service = OrderService(order_repo, user_repo)
    order = await service.create_order(command)
    
    assert order.status == OrderStatus.PENDING
    order_repo.save.assert_called_once()
```

### 수정된 Task Breakdown 예시 (기능별)

```
# 기존 (레이어별) → 수정 (기능별)

기존:
├─ Task 001: User 엔티티
├─ Task 002: Order 엔티티
├─ Task 003: Portfolio 엔티티
├─ Task 004: 값 객체
├─ Task 005: 마이그레이션
├─ Task 006: User 리포지토리
├─ Task 007: Order 리포지토리
├─ Task 008: 주문 생성 서비스
├─ Task 009: 주문 조회 서비스
├─ Task 010: Auth API
├─ Task 011: Orders API
...

수정:
├─ Task 000: 인터페이스 정의 (모든 Protocol)     [1.5h]
├─ Task 001: User 기능 (Entity→Repo→Service→API) [4h]
├─ Task 002: Auth 기능 (Login, Token, Refresh)   [3h]
├─ Task 003: Order 생성 기능 (E2E)               [4h]
├─ Task 004: Order 조회 기능 (E2E)               [2.5h]
├─ Task 005: Order 취소 기능 (E2E)               [2.5h]
├─ Task 006: Portfolio 기능 (E2E)                [3h]
├─ Task 007: KIS 연동 기능 (E2E)                 [4h]
├─ Task 008: 기능 간 통합                        [3h]
└─ Task 009: E2E 테스트                          [2.5h]

총: 30시간 (10 Tasks) vs 48시간 (17 Tasks)
효율성: 37.5% 향상!
```

---

## ⏪ DNA 핵심 원칙 4: 역방향 수정 프로토콜

### 이전 Stage 오류 발견 시나리오

```
Stage 8 작업 중 발견할 수 있는 오류:

시나리오 1: Blueprint 불완전
────────────────────────────────────
"Task 분해하려는데 Blueprint에 Order 취소 API가 없네?"
→ Stage 7 Blueprint 수정 필요

시나리오 2: ADR 누락
────────────────────────────────────
"외부 결제 API 연동이 필요한데 ADR에 결정 안 되어 있네?"
→ Stage 3 ADR 추가 필요

시나리오 3: NFR 재검토
────────────────────────────────────
"Task 분해하니까 실시간 요구사항이 더 중요했네?"
→ Stage 2 NFR 우선순위 수정 필요

시나리오 4: 패밀리 재분류
────────────────────────────────────
"협업 기능이 핵심인데 CRUD 패밀리로 분류했었네?"
→ Stage 1 패밀리 재분류 필요 (드뭄)
```

### 6단계 수정 프로토콜

```
Stage 8에서 이전 Stage 오류 발견 시:

Step 1: 오류 발견 및 문서화
────────────────────────────────────
├─ 발견 위치: Stage 8 Task Breakdown
├─ 오류 내용: [구체적 설명]
├─ 영향 받는 Stage: Stage [N]
└─ 기록: 08T-01_task_breakdown.md에 "발견된 이슈" 섹션 추가

Step 2: 영향 범위 파악
────────────────────────────────────
├─ 직접 영향: Stage [N]
├─ 간접 영향: Stage [N+1] ~ Stage 7
├─ 재작업 예상 시간: [X]시간
└─ 기록: 영향 범위 문서화

Step 3: 해당 Stage로 이동 → 수정
────────────────────────────────────
├─ Stage [N] 산출물 수정
├─ 수정 이력 기록
├─ 버전 업데이트 (v1.0 → v1.1)
└─ 수정 완료 검증

Step 4: 중간 Stage 전파 (N+1 ~ 7)
────────────────────────────────────
├─ 각 Stage 산출물 영향 확인
├─ 필요 시 수정
├─ 수정 이력 기록
└─ 일관성 검증

Step 5: Stage 8 재진행
────────────────────────────────────
├─ 수정된 입력으로 Task Breakdown 재작성
├─ 3단계 검증 프로토콜 재실행
└─ 완전성 확인

Step 6: 재진행 결과 검증
────────────────────────────────────
├─ 오류가 해결되었는지 확인
├─ 새로운 문제 발생 여부 확인
├─ 최종 승인
└─ Stage 9 전달
```

### 추적성 (Traceability)

```
수정 이력 관리:

파일: docs/revision_log.md
────────────────────────────────────
# Revision Log

## 2025-12-03 (Stage 8 작업 중 발견)

### Issue #001: Order 취소 API 누락
- **발견 Stage**: Stage 8 Task Breakdown
- **영향 Stage**: Stage 7 Blueprint
- **수정 내용**: Section 4.1에 DELETE /orders/{id} 추가
- **영향 범위**: Stage 8 Task 목록에 "Order 취소 기능" 추가
- **수정자**: Jason
- **검증**: 1호 확인 완료

### Issue #002: 외부 결제 API ADR 누락
- **발견 Stage**: Stage 8 Task Breakdown
- **영향 Stage**: Stage 3 ADR
- **수정 내용**: ADR-015 "외부 결제 API 연동" 추가
- **영향 범위**: 
  - Stage 4: DNA Blueprint에 결제 관련 DNA 추가
  - Stage 7: Blueprint Section 6 외부 연동 추가
  - Stage 8: Task 목록에 결제 기능 추가
- **수정자**: Jason
- **검증**: 2호 확인 완료
```

### 예시: Stage 7 작성 중 Stage 3 ADR 오류 발견

```
상황:
Stage 7 Blueprint 작성 중 "KIS API Rate Limiting" 결정이
ADR에 없음을 발견

6단계 프로토콜 적용:

Step 1: 오류 문서화
├─ 발견: Stage 7 Blueprint Section 6.1 작성 중
├─ 오류: KIS API Rate Limiting 전략 ADR 없음
├─ 영향: Stage 3
└─ 기록: 07B-01에 "발견된 이슈" 추가

Step 2: 영향 범위
├─ 직접: Stage 3 (ADR 추가 필요)
├─ 간접: Stage 4-6 (영향 없음, DNA 변경 불필요)
├─ 재작업: 2시간
└─ 기록 완료

Step 3: Stage 3 수정
├─ ADR-016 "KIS API Rate Limiting" 작성
├─ 결정: 초당 15회 제한, 재시도 전략
├─ 버전: v1.0
└─ 검증 완료

Step 4: 중간 Stage 전파
├─ Stage 4-6: 변경 불필요 확인
└─ 스킵

Step 5: Stage 7 재진행
├─ Blueprint Section 6.1 Rate Limiting 추가
├─ ADR-016 참조 추가
└─ 완료

Step 6: 검증
├─ Rate Limiting 설계 완료 확인
├─ 새로운 문제 없음
└─ Stage 8 전달 가능 ✅
```

---

**Remember**: 
- Blueprint는 전체 그림, Task는 레고 블럭
- 좋은 Task = 적절한 크기 + 독립성 + 검증 가능 + 가치
- RDoLT: Easy → Intermediate → Final 순서
- 핵심 경로 파악 = 일정 예측 가능
- Stage 9에서 각 Task마다 9-Step 체크리스트 작성

*Task Breakdown은 "AI가 100% 성공할 수 있는 작업 단위"를 만드는 과정입니다.*
