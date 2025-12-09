# Stage 5: DNA 시스템 구현 가이드 (DNA Implementation Guide)

> **목적**: Stage 4 청사진 기반으로 src/core/ DNA 시스템 실제 구현
>
> **버전**: v4.1 (2025-12-03)
>
> - v5.0 (2025-12-03): Gemini 연구 기반 전면 재작성, 01_DNA_METHODOLOGY_DETAILED.md 기준
> - v1.0 (2025-11-13): 초기 버전

---

## 📚 이 가이드의 위치

```
DNA 방법론 문서 체계:

Tier 1: 00_CORE_METHODOLOGY.md (전체 맥락)
           ↓
Tier 2: 01_DNA_METHODOLOGY_DETAILED.md (상세 원리)
           ↓
Tier 3: 이 문서 (Stage 5 실행 가이드) ← 지금 여기!
```

**참조 문서**:

- **원리 이해**: `01_DNA_METHODOLOGY_DETAILED.md` **Part 5**
- **DNA 상세**: `./standards/03_DNA_SYSTEMS_GUIDE.md`

---

## 🧬 DNA 방법론 4대 핵심 원칙 (Stage 5 적용)

> **"AI가 한 세션에서 최고 성과를 낼 수 있는 크기로 작업하고, 완전해질 때까지 반복하며, 기능별로 분해하여 조립한다"**

Stage 5 (DNA 시스템 구현)에서 DNA 4대 핵심 원칙이 적용되는 방식:

---

### DNA 핵심 원칙 1: AI 최적 크기

**"컨텍스트 범위 내에서 작업한다"**

#### Stage 5의 작업 크기 전략

```
❌ 잘못된 접근: 11개 DNA 시스템 한 번에 구현
"11개 DNA 시스템을 한 세션에서 모두 구현하세요"
→ 컨텍스트 초과 (200K 토큰 한계)
→ 후반부 구현 품질 저하
→ 테스트 누락, 타입 오류, print() 사용 등
→ 품질 게이트 실패

✅ 올바른 접근: 시스템별 순차 구현
Session 1: Logging 시스템 구현 (완전)
Session 2: Types 시스템 구현 (완전)
Session 3: Database 시스템 구현 (완전)
Session 4: Cache 시스템 구현 (완전)
...
Session 11: Error 시스템 구현 (완전)

각 세션: 1개 시스템 완전 구현 + 테스트, 80-90K 토큰
```

#### 컨텍스트 구성 (각 세션)

```
Claude 200K 토큰 윈도우:
├─ 시스템 프롬프트: ~30K 토큰
├─ 대화 히스토리: ~20K 토큰
├─ Stage 4 청사진: ~10-15K 토큰
│   └─ 04D-0X_dna_XXX_blueprint.md (해당 시스템)
├─ Stage 6 프로젝트 표준: ~10-15K 토큰
│   └─ 06D-01_project_standards.md (관련 섹션)
├─ Stage 3 ADR 참조: ~5-10K 토큰
│   └─ 03A-40X_dna_XXX.md
├─ 구현 코드 작성: ~20-25K 토큰
│   ├─ core/XXX/* (구현 파일들)
│   └─ tests/core/XXX/* (테스트 파일들)
└─ 응답 생성 여유: ~80-90K 토큰

**참조**: 파일 확장자는 언어별로 다름 (.py, .ts, .rs, .go 등)
```

#### 세션당 작업량 기준

| DNA 시스템               | 파일 수 (근사치) | 테스트 파일 | 총 토큰 | 세션 수        |
| ------------------------ | ---------------- | ----------- | ------- | -------------- |
| Type System              | 3-4개            | 3-4개       | ~15K    | 1 session      |
| Configuration System     | 2-3개            | 2-3개       | ~12K    | 1 session      |
| Error Handling System    | 3-4개            | 3-4개       | ~15K    | 1 session      |
| Observability System     | 5-6개            | 5-6개       | ~20K    | 1 session      |
| Data System (Cache)      | 4-5개            | 4-5개       | ~18K    | 1 session      |
| Testing System           | 4-5개            | 4-5개       | ~18K    | 1 session      |
| Security System          | 6-7개            | 6-7개       | ~22K    | 1 session      |
| Performance System       | 5-6개            | 5-6개       | ~20K    | 1 session      |
| API System               | 6-7개            | 6-7개       | ~22K    | 1 session      |
| Data System (DB)         | 8-10개           | 8-10개      | ~28K    | **2 sessions** |
| Architecture Enforcement | 4-5개            | 4-5개       | ~18K    | 1 session      |

**핵심**: 대부분 시스템은 1 세션, Data System (DB)만 2 세션

**참조**: 파일 수는 언어/프로젝트에 따라 다를 수 있음. 핵심은 "AI 최적 크기 (80-90K 토큰)"

#### Data System (DB) 분해 전략 (유일한 예외)

```
Data System (DB)는 유일하게 2 세션 필요:

Session 1: DB 기초 (Connection + Session)
├─ connection.*: Connection Pool 구현
├─ session.*: Session Manager 구현
├─ protocols.*: ConnectionProvider, SessionProvider 정의
└─ 테스트 (각 모듈 격리)
  → ~25K 토큰

Session 2: DB 고급 (Query + Migration)
├─ query.*: Query Builder 구현
├─ migration.*: Schema Migration 구현
├─ integration.*: 모듈 통합
└─ 테스트 (통합 테스트 포함)
  → ~25K 토큰

**참조**: 파일 확장자는 언어별로 다름 (.py, .ts, .rs, .go 등)
```

---

### DNA 핵심 원칙 2: 완전해질 때까지 반복

**"부족하면 반복해서 부족함이 없어질 때까지"**

#### DNA 시스템 구현 완전성 기준

각 DNA 시스템 구현은 다음을 모두 포함해야 함:

```
✅ 완전한 DNA 구현 체크리스트:
□ 1. 공개 API 구현
   - 청사진의 모든 함수/클래스 구현
   - 타입 안전성 완전 (타입 체커 0 오류, ADR-301 참조)
   - 문서 주석 (프로젝트 표준 참조)

□ 2. 내부 헬퍼 구현
   - Private 함수/클래스
   - 유틸리티 모듈
   - 상수/설정

□ 3. 에러 처리
   - 예외 처리 적절히 배치
   - 커스텀 예외 정의
   - 에러 로깅 (직접 출력 금지, ADR-401 참조)

□ 4. 로깅 통합
   - Observability System 통합
   - 모든 중요 시점에 로그
   - 표준 로거 사용 (ADR-401)

□ 5. 테스트 작성 (TDD)
   - 단위 테스트: 각 함수/클래스
   - 통합 테스트: 모듈 간 상호작용
   - 커버리지: 95%+
   - 테스트 프레임워크 (ADR-801 참조)

□ 6. 품질 검증 (Zero-Tolerance)
   - Linter: 0 오류 (ADR-302 참조)
   - Type Checker: 0 오류 (ADR-301 참조)
   - Import 규칙: 0 위반 (ADR-501 참조)
   - 테스트: 100% pass

□ 7. 문서화
   - Entry point: 공개 API 노출
   - README: 사용 예시
   - 주석: 복잡한 로직 설명
```

#### 3단계 검증 프로토콜

```
검증 함수: validate_dna_implementation(system_name)
─────────────────────────────────────────────────

검증 1: 청사진 대비 완성도
├─ 청사진 읽기: 04B-01_dna_blueprint.md
├─ 구현 파일 탐색: core/{system_name}/*
└─ 각 공개 API 구현 확인:
    ├─ 미구현 발견 시:
    │   ├─ passed: false
    │   ├─ message: "{system_name}: 공개 API {api} 미구현"
    │   └─ action: "해당 API 구현"
    └─ 모두 구현됨 → 검증 2로

검증 2: 품질 게이트 (Zero-Tolerance)
├─ Linter 실행 (ADR-302):
│   └─ 오류 > 0 → 실패, "Linter 오류 수정"
├─ Type Checker 실행 (ADR-301):
│   └─ 오류 > 0 → 실패, "타입 오류 수정"
├─ Import 규칙 검증 (ADR-501):
│   └─ 위반 > 0 → 실패, "Import 규칙 수정"
└─ 모두 통과 → 검증 3으로

검증 3: 테스트 커버리지
├─ 테스트 실행 (ADR-801):
│   └─ tests/core/{system_name}/
├─ 커버리지 측정:
│   └─ < 95% → 실패, "테스트 추가"
└─ >= 95% → passed: true

**참조**: 구체적 도구/명령어는 언어별 매뉴얼 참조
```

#### 불완전 → 재구현 사례

```markdown
## 사례: DNA Observability System (Logging) 구현

### ❌ 불완전한 버전 (1차 구현)

**파일**: core/logging/logger.*

함수: get_logger(name)
  ❌ 타입 정보 없음 (반환 타입 미지정)
  └─ 표준 라이브러리 로거 반환

클래스: Logger
  └─ 메서드: info(msg)
      ❌ 타입 정보 없음
      ❌ 직접 출력 사용! (print/console.log)

**품질 검증 실패**:

Type Checker (ADR-301):
  logger.*:3: error: Missing return type
  logger.*:6: error: Missing type for 'msg'
  → Type Checker: 2 errors

Linter (ADR-302):
  logger.*:8: 직접 출력 금지 (print/console.log)
  → Linter: 1 error

테스트 (ADR-801):
  → Coverage: 45% (목표: 95%)

❌ 문제점:
- 타입 정보 누락 → Type Checker 오류
- 직접 출력 사용 → Linter 위반
- 테스트 부족 → 커버리지 45%
- 청사진의 context() 미구현

### ✅ 완전한 버전 (2차 재구현)

**파일**: core/logging/logger.*

함수: get_logger(name: string) → Logger
  ✅ 타입 정보 완전
  ✅ 문서 주석 포함
  └─ 구조화된 로거 반환 (ADR-401 도구 사용)

클래스: Logger
  ├─ 생성자(logger: LoggerImpl) → Logger
  │   ✅ 타입 정보 완전
  │
  ├─ info(msg: string, context: map) → void
  │   ✅ 타입 정보 완전
  │   ✅ 구조화된 로깅 사용 (ADR-401)
  │   └─ 직접 출력 없음!
  │
  └─ context(context: map) → LogContext
      ✅ 청사진 API 완전 구현

**테스트 파일**: tests/core/logging/test_logger.*


테스트 1: get_logger가 Logger 인스턴스 반환
  └─ get_logger("test") → Logger 타입 확인

테스트 2: info()가 메시지 로깅
  └─ logger.info("테스트", key="value")
      → 로그에 메시지/컨텍스트 포함 확인

테스트 3: context()가 컨텍스트 추가
  └─ logger.context(request_id="123")로
      → 이후 로그에 request_id 자동 포함 확인

**품질 검증 성공**:

Type Checker (ADR-301):
  → Success: no issues found

Linter (ADR-302):
  → All checks passed!

테스트 (ADR-801):
  → Coverage: 97% ✅

**참조**: 구체적 코드 예시는 언어별 매뉴얼 참조
```

---

### DNA 핵심 원칙 3: 기능별 분해 + 연결부 + 조립

**"모듈이 크면 기능별로 나누고, 연결부 설계 후 조립"**

#### Stage 5에서의 적용 (가장 중요!)

Stage 5는 **실제 코드 구현** 단계이므로 원칙 3이 **직접 적용**됩니다!

```markdown
DNA 시스템 크기별 전략:

작은 시스템 (< 5 파일):
├─ 한 세션에 전체 구현
└─ 분해 불필요
    예: Type System, Configuration System, Error Handling System

중간 시스템 (5-7 파일):
├─ 한 세션에 구현 가능
├─ 모듈 간 의존성 관리
└─ Interface/Protocol 정의
    예: Observability System, Data System (Cache), Testing System

큰 시스템 (8+ 파일):
├─ 기능별 분해 필수!
├─ Interface/Protocol 정의 (연결부)
├─ 각 기능 독립 구현
└─ 마지막에 조립
    예: Data System (DB) - 유일한 케이스!
```

#### Data System (DB) 분해 실전 (개념)

**참조**: 구체적 코드는 언어별 매뉴얼 참조

```markdown
Task 000: Interface/Protocol 정의 (연결부)
─────────────────────────────────────────

목적: 모듈 간 연결 인터페이스 정의

정의할 Interface:
├─ ConnectionProvider: DB 연결 제공
│   └─ get_connection() → Connection
├─ SessionProvider: DB 세션 제공
│   └─ get_session() → Session
└─ 테스트: Interface 정의만, 구현 없음

---

Task 001: Connection Pool 구현
─────────────────────────────────────────

목적: DB 연결 풀 관리

구현 체크리스트:
□ ConnectionPool 클래스
  ├─ ConnectionProvider 구현
  ├─ 연결 생성/관리/해제
  └─ 설정 주입 (DB URL, pool size 등)

□ 테스트 (Mock 없음, 실제 DB 사용)
  ├─ 연결 생성 테스트
  ├─ 연결 풀 관리 테스트
  └─ 동시성 테스트

□ 품질 검증
  ├─ Type Checker: 0 오류
  ├─ Linter: 0 오류
  └─ Coverage: 95%+

---

Task 002: Session Manager 구현
─────────────────────────────────────────

목적: 트랜잭션 관리, 세션 라이프사이클

구현 체크리스트:
□ SessionManager 클래스
  ├─ SessionProvider 구현
  ├─ ConnectionProvider Mock 사용 (의존성)
  ├─ 트랜잭션 관리 (begin/commit/rollback)
  └─ 설정 주입

□ 테스트 (ConnectionProvider Mock)
  ├─ 세션 생성 테스트
  ├─ 트랜잭션 테스트 (commit/rollback)
  └─ 에러 처리 테스트

□ 품질 검증: Type/Lint/Coverage

---

Task 999: Database 통합 (조립)
─────────────────────────────────────────

목적: 모든 모듈 통합, 공개 API 제공

통합 체크리스트:
□ 공개 API 모듈 (entry point)
  ├─ ConnectionPool, SessionManager import
  ├─ 실제 구현체 생성
  └─ get_session() 함수 제공

□ 통합 테스트 (E2E)
  ├─ Mock 없음, 실제 DB 사용
  ├─ 전체 플로우 테스트
  └─ 성능 테스트 (선택)

□ 최종 검증
  ├─ 모든 공개 API 동작 확인
  ├─ Type/Lint/Coverage 통과
  └─ 문서화 완료 (README, 사용 예시)
```

---

#### 작은/중간 시스템 구현 전략

**개념**: 작은 시스템 (< 5 파일)은 한 세션에 전체 구현

**예시: Type System (분해 불필요)**

```markdown
한 세션 구현 체크리스트:
□ 도메인 타입 정의 (ID types: UserId, OrderId 등)
□ Enum 타입 (LogLevel, Status 등)
□ Value Objects (Email, Money 등)
□ Base 클래스 (BaseEntity, BaseValueObject)
□ 테스트 (모든 타입 생성/검증)
□ 품질 검증 (Type/Lint/Coverage)
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조

**결과**: 1 세션에 전체 완성 (분해 불필요)

---

### DNA 핵심 원칙 4: 역방향 수정 프로토콜

**"앞선 결정의 오류 발견 시 → 되돌아가서 수정 → 다시 현재까지 진행"**

#### Stage 5에서 역방향 수정이 발생하는 경우

```markdown
시나리오 1: Stage 4 청사진 오류 발견
├─ Stage 5 Logging 구현 중
├─ 청사진에 비동기 로그 쓰기 누락 발견
├─ → Stage 4로 돌아가 청사진 보완
├─ → Stage 5 재구현
└─ → 추적성 업데이트

시나리오 2: Stage 3 ADR 오류 발견
├─ Stage 5 Database 구현 중
├─ ADR-402 "PostgreSQL 13+"가 실제로는 14+ 필요
├─ → Stage 3로 돌아가 ADR-402 수정
├─ → Stage 4 청사진 업데이트
├─ → Stage 5 재구현
└─ → 추적성 업데이트

시나리오 3: 구현 중 설계 결함 발견
├─ Stage 5 Cache 구현 중
├─ Redis 연결 풀 전략이 청사진과 다르게 필요
├─ → Stage 4 청사진 수정
├─ → Stage 5 재구현
└─ → 추적성 업데이트
```

#### 6단계 수정 프로토콜

````markdown
## 실제 사례: Logging 시스템 비동기 쓰기 추가

### Step 1: 오류 발견 및 문서화
**발견 시점**: Stage 5 (Observability System 구현 중)
**파일**: `core/logging/handlers.*`
**문제**: 파일 핸들러가 동기 쓰기라 성능 저하
          청사진에 비동기 쓰기 언급 없음

### Step 2: 영향 범위 파악
**영향받는 문서**:
- Stage 4: `04B-01_dna_blueprint.md` (청사진 수정 필요)
- Stage 3: `03A-401_*.md` (ADR 확인 - 수정 불필요)

**영향받는 구현**:
- `core/logging/handlers.*` (재구현 필요)
- `tests/core/logging/test_handlers.*` (재작성 필요)

### Step 3: 해당 Stage로 이동 및 수정
```bash
# Stage 4 청사진 수정
$ edit 04D-01_dna_logging_blueprint.md
  Line 67: 동기 파일 쓰기 → 비동기 파일 쓰기
  Line 78: aiofiles 의존성 추가
  Line 89: FileHandler → AsyncFileHandler

# 수정 이유 명시
> **History**:
> - v1.0 (2024-11-10): 초기 청사진
> - v1.1 (2024-11-12): 비동기 쓰기 추가 (성능 개선)

### Step 4: 중간 Stage 전파

Stage 5 진행 중이므로 즉시 반영

### Step 5: 현재 Stage 재진행

```
Stage 5 재구현 절차:

1. 기존 구현 제거
   ├─ core/logging/handlers.* 삭제
   └─ tests/core/logging/test_handlers.* 삭제

2. 수정된 청사진 기반 재구현
   ├─ AsyncFileHandler 클래스
   │   └─ 비동기 파일 쓰기 구현
   ├─ 비동기 I/O 라이브러리 사용 (ADR-401 참조)
   └─ 설정 주입 (파일 경로 등)

3. 테스트 재작성
   ├─ 비동기 테스트 작성
   ├─ 파일 쓰기/읽기 검증
   └─ 에러 처리 테스트

**참조**: 구체적 코드는 언어별 매뉴얼 참조
```

### Step 6: 재진행 결과 검증

```
품질 검증:
├─ Type Checker (ADR-301): 0 오류 ✅
├─ Linter (ADR-302): 0 오류 ✅
└─ 테스트 (ADR-801): Coverage 97% ✅

검증 체크리스트:
□ 청사진 v1.1 반영 확인
□ 비동기 쓰기 구현 완료
□ 비동기 I/O 의존성 추가
□ 품질 게이트 통과 (Type/Lint: 0 오류)
□ 테스트 커버리지 95%+
□ 추적성 명시 (Ref: 04B-01 v1.1)
```
````

#### 추적성 (Traceability) 유지

**모든 수정은 명시적으로 참조**

````
추적성 예시: 파일 헤더 주석

```
파일: core/logging/handlers.*
목적: 비동기 파일 핸들러

참조: 04B-01_dna_blueprint.md v1.1 (Section 3.2)
수정일: 2024-11-12 (비동기 쓰기로 변경)
사유: 동기 쓰기 성능 저하 → 비동기 쓰기 필요
```

청사진 버전 이력 예시:

```
파일: 04B-01_dna_blueprint.md

History:
- v1.0 (2024-11-10): 초기 청사진
- v1.1 (2024-11-12): 비동기 쓰기 추가 (Stage 5 성능 이슈 발견)

Section 3.2: 파일 핸들러
  전략: 비동기 쓰기
  라이브러리: [ADR-401 참조]
  참조: Stage 5 구현 중 성능 이슈 발견
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조
````

---

## 🎯 DNA 원칙 적용 요약 (Stage 5)

| 원칙                   | Stage 5 적용 방법                               | 체크포인트                              |
| ---------------------- | ----------------------------------------------- | --------------------------------------- |
| **1. AI 최적 크기**    | 시스템별 순차 구현 (1개/세션)                   | Database만 2 sessions                   |
| **2. 완전해질 때까지** | 7개 항목 완전성, Zero-Tolerance                 | Linter 0, Type Checker 0, Coverage 95%+ |
| **3. 기능별 분해**     | Database 시스템만 분해 (Protocol + Mock + 조립) | Protocol 정의 필수                      |
| **4. 역방향 수정**     | 6단계 프로토콜, 추적성 유지                     | Ref + Updated 명시                      |

---

## 🤔 왜 DNA 구현이 필요한가?

### 청사진 vs 구현

```markdown
Stage 4 청사진:
├─ "무엇을" 만들 것인지 설계
├─ 디렉토리 구조, 파일 목록
├─ 공개 API 정의
└─ 문서 (Markdown)

Stage 5 구현:
├─ "실제로" 코드 작성
├─ core/ 모듈 구현
├─ 테스트 작성
└─ 언어별 구현 (ADR-101 참조)

비유:
├─ 청사진 = 건축 도면
└─ 구현 = 실제 건설
```

### DNA 없이 도메인 구현하면?

```
❌ DNA 없이 도메인부터 구현:

domain/orders/service.*:
────────────────────────────────
표준 라이브러리 직접 사용
├─ 직접 출력 사용 (print/console.log)
├─ 표준 로거 직접 사용
├─ 에러 처리 없음
├─ 타입 정보 없음
└─ DB 직접 쿼리

결과 (문제점):
├─ 로깅 형식 불일치 (JSON vs Console)
├─ 직접 출력과 로거 혼재
├─ 에러 처리 누락
├─ 타입 안전성 없음
└─ 테스트 불가능한 코드
```

```
✅ DNA 먼저 구현 후 도메인:

domain/orders/service.*:
────────────────────────────────
DNA Systems 통합 사용
├─ from core.logging import get_logger
├─ from core.errors import ValidationError, NotFoundError
├─ from core.types import OrderId, UserId
└─ from core.database import get_session

OrderService 클래스:
├─ create_order(data: CreateOrderRequest) → OrderId
│   ├─ 타입 안전성 (모든 파라미터/리턴 타입 명시)
│   ├─ 구조화된 로깅 (컨텍스트 포함)
│   ├─ 데이터 검증 (ValidationError 활용)
│   ├─ 세션 관리 (get_session 사용)
│   ├─ 트랜잭션 처리 (commit/rollback)
│   └─ 타입 안전한 반환 (OrderId)

구현 흐름:
1. 입력 데이터 검증 → ValidationError
2. DB 세션 획득 → get_session()
3. 엔티티 생성 및 저장
4. 트랜잭션 커밋
5. 타입 안전한 ID 반환

결과 (장점):
├─ 일관된 로깅 (JSON, trace_id 포함)
├─ 표준화된 에러 처리
├─ 타입 안전성
├─ 테스트 가능한 코드
└─ DNA가 "환경"으로 보호
```

---

## 📥 입력 문서

### Stage 4에서 전달받는 것

| 파일                      | 핵심 내용         | 이 Stage에서 사용 |
| ------------------------- | ----------------- | ----------------- |
| `04B-01_dna_blueprint.md` | DNA 시스템 청사진 | 구현 명세         |
| `03A-401~499_*.md`        | DNA 시스템 ADR    | 기술 선택 근거    |

---

## 📤 출력 문서

### 필수 산출물

```markdown
core/                              # 구현된 DNA 모듈
├── [entry_point]                  # 진입점 (언어별 형식)
├── logging/                       # Observability System
├── config/                        # Configuration System
├── types/                         # Type System
├── errors/                        # Error Handling System
├── database/                      # Data System (DB)
├── cache/                         # Data System (Cache)
└── security/                      # Security System

tests/                             # DNA 테스트
├── unit/core/
│   ├── test_logging.*             # 단위 테스트
│   ├── test_config.*
│   └── ...
└── integration/core/
    └── test_database.*            # 통합 테스트

docs/
└── 05D-01_dna_implementation.md   # 구현 완료 문서

**참조**: 디렉토리 구조는 언어별로 다를 수 있음 (ADR-101 참조)
```

---

## 🔧 DNA 구현 3대 원칙

### 원칙 1: 표준 라이브러리 우선

```markdown
❌ 직접 구현 (실패 사례):
────────────────────────────────
과거 V5 프로젝트:
├─ 89개 커스텀 타입 클래스 직접 작성
├─ 1,679줄의 검증 로직 구현
├─ 버그 발생 시 직접 수정
└─ 유지보수 부담 증가

문제점:
├─ 휠을 재발명 (Reinventing the wheel)
├─ 검증되지 않은 코드
├─ 표준 라이브러리보다 성능 저하
└─ 유지보수 비용 증가

✅ 표준 라이브러리 활용:
────────────────────────────────
타입 시스템 라이브러리 활용 (ADR-301 참조):
├─ 검증된 타입 검증 기능
├─ 자동 변환/직렬화
├─ 명확한 에러 메시지
└─ 3-5줄로 구현 완료

장점:
├─ 커뮤니티 검증된 코드
├─ 성능 최적화 완료
├─ 문서화 및 예제 풍부
└─ 유지보수 부담 최소화
```

**참조**: 구체적 라이브러리는 언어별 매뉴얼 참조

**DNA별 표준 라이브러리 선택 원칙**:

| DNA 시스템           | 라이브러리 선택 기준 (ADR 참조)  | 직접 구현 금지 사항          |
| -------------------- | -------------------------------- | ---------------------------- |
| Observability System | 구조화 로깅 라이브러리 (ADR-401) | print/console 직접 사용      |
| Configuration System | 타입 안전 설정 관리 (ADR-402)    | 환경변수 직접 접근           |
| Type System          | 타입 검증 라이브러리 (ADR-301)   | 커스텀 타입 클래스 직접 작성 |
| Error Handling       | 타입 안전 에러 클래스 (ADR-303)  | 일반 Exception만 사용        |
| Data System (DB)     | ORM/쿼리 빌더 (ADR-501)          | 직접 SQL 문자열 작성         |
| Data System (Cache)  | 캐시 클라이언트 (ADR-502)        | 직접 소켓 통신               |
| Testing System       | 테스트 프레임워크 (ADR-801)      | 커스텀 테스트 러너           |

**원칙**: 언어별 커뮤니티 검증된 표준 라이브러리 사용 (ADR에서 결정)

### 원칙 2: 인터페이스 추상화

**핵심 개념**: 구현체가 아닌 인터페이스에 의존

```
파일 구조:
────────────────────────────────
core/cache/
├── interface.*              # 캐시 인터페이스 정의
│   └─ CacheInterface
│       ├─ get(key) → value
│       ├─ set(key, value, ttl)
│       └─ delete(key)
│
├── redis.*                  # Redis 구현체
│   └─ RedisCache implements CacheInterface
│
└── memcached.*              # 대체 구현체 (교체 가능)
    └─ MemcachedCache implements CacheInterface

인터페이스 정의 (개념):
────────────────────────────────
CacheInterface:
  목적: 캐시 작업 표준 인터페이스
  메서드:
    - get(key: string) → value | null
    - set(key: string, value: any, ttl: number) → void
    - delete(key: string) → void

구현체 1 (Redis):
  RedisCache implements CacheInterface
  ├─ Redis 클라이언트 활용
  └─ 모든 인터페이스 메서드 구현

구현체 2 (Memcached):
  MemcachedCache implements CacheInterface
  ├─ Memcached 클라이언트 활용
  └─ 동일한 인터페이스 구현

교체 시나리오:
  Redis → Memcached 전환
  ├─ 도메인 코드 변경 없음 (인터페이스 동일)
  ├─ 설정만 변경 (ADR-502 업데이트)
  └─ 테스트 통과 확인
```

**가치**:

- **테스트 용이성**: Mock/Stub 주입 간편
- **기술 독립성**: 구현체 교체 시 도메인 코드 무수정
- **설계 원칙**: 의존성 역전 원칙 (DIP) 준수
- **유연성**: 런타임 구현체 선택 가능

**참조**: 구체적 인터페이스 정의는 언어별 매뉴얼 참조

### 원칙 3: 설정 주입 (환경별 분리)

**핵심 개념**: 환경변수 기반 설정 관리, 타입 안전성 보장

```
파일 구조:
────────────────────────────────
core/config/
├── settings.*               # 설정 클래스 정의
└── [환경별 설정 파일]       # .env.* 또는 언어별 형식

설정 클래스 정의 (개념):
────────────────────────────────
Settings 클래스:
  목적: 환경별 설정 중앙 관리

  필드 정의:
    - database_url: string (기본값: 개발 DB URL)
    - cache_url: string (기본값: 로컬 캐시)
    - log_level: string (기본값: "INFO")
    - log_format: string (기본값: "json")
    - environment: string (기본값: "development")

  로딩 전략:
    ├─ 환경변수 파일 읽기 (.env.*)
    ├─ 타입 검증 (문자열 → 타입 변환)
    ├─ 필수 값 검증 (누락 시 에러)
    └─ 기본값 적용 (선택 필드)

사용 패턴:
────────────────────────────────
1. 설정 인스턴스 생성
   settings = Settings()

2. 타입 안전한 접근
   db_url = settings.database_url  # 타입: string
   log_level = settings.log_level  # 타입: string

3. DNA 시스템에서 활용
   logger.configure(level=settings.log_level)
   db.connect(url=settings.database_url)
```

**환경별 설정 파일 예시**:

```bash
# 개발 환경 (.env.development)
DATABASE_URL=postgresql://localhost/dev
CACHE_URL=redis://localhost:6379
LOG_LEVEL=DEBUG
LOG_FORMAT=console
ENVIRONMENT=development

# 프로덕션 환경 (.env.production)
DATABASE_URL=postgresql://prod-db:5432/prod
CACHE_URL=redis://prod-cache:6379
LOG_LEVEL=INFO
LOG_FORMAT=json
ENVIRONMENT=production
```

**장점**:

- **타입 안전성**: 설정 값 타입 검증
- **중앙 관리**: 모든 설정 한 곳에서 관리
- **환경 분리**: 개발/스테이징/프로덕션 독립
- **검증 자동화**: 필수 값 누락 시 즉시 에러

**참조**: 구체적 설정 라이브러리는 언어별 매뉴얼 참조 (ADR-402)

---

## 📋 구현 단계 (Part 1-4)

### Part 1: 프로젝트 구조 생성 (30분)

#### Step 1: 디렉토리 구조 생성

**목적**: Stage 4 청사진 기반 DNA 모듈 디렉토리 구조 생성

```
생성할 디렉토리 구조:
────────────────────────────────
[project_root]/
├── core/                        # DNA 시스템 모듈
│   ├── logging/                 # Observability System
│   ├── config/                  # Configuration System
│   ├── types/                   # Type System
│   ├── errors/                  # Error Handling System
│   ├── database/                # Data System (DB)
│   ├── cache/                   # Data System (Cache)
│   └── security/                # Security System
│
└── tests/                       # 테스트
    ├── unit/core/               # 단위 테스트
    └── integration/core/        # 통합 테스트

필수 작업:
□ 각 DNA 시스템별 디렉토리 생성
□ 테스트 디렉토리 분리 (unit/integration)
□ 언어별 진입점 파일 생성 (필요시)
```

**참조**: 언어별 구체적 명령어는 매뉴얼 참조

#### Step 2: 의존성 설치

**목적**: DNA 시스템 구현에 필요한 라이브러리 설치

```
필수 의존성 (ADR 참조):
────────────────────────────────
□ Type System 라이브러리 (ADR-301)
  └─ 타입 검증, 직렬화/역직렬화

□ Configuration 라이브러리 (ADR-402)
  └─ 환경변수 관리, 타입 안전 설정

□ Observability 라이브러리 (ADR-401)
  └─ 구조화 로깅, 메트릭, 추적

□ Data 라이브러리 (ADR-501, ADR-502)
  └─ ORM/쿼리빌더, 캐시 클라이언트

□ Testing 라이브러리 (ADR-801)
  └─ 테스트 프레임워크, 커버리지 도구

개발 도구:
□ 코드 품질 (ADR-302)
  ├─ Linter (코드 스타일)
  ├─ Formatter (자동 정렬)
  └─ Type Checker (타입 검증)

□ 자동화 도구
  └─ Pre-commit hooks (품질 게이트)
```

**참조**: 언어별 패키지명은 매뉴얼 참조

#### Step 3: 기본 설정 파일

**목적**: 코드 품질 자동 검증 설정

```
설정할 항목:
────────────────────────────────
□ Linter 설정 (ADR-302)
  ├─ 코드 스타일 규칙
  ├─ 금지 패턴 (print/console 사용 등)
  └─ 최대 줄 길이

□ Type Checker 설정 (ADR-301)
  ├─ Strict 모드 활성화
  ├─ 타입 추론 경고
  └─ Any 타입 경고

□ Test 설정 (ADR-801)
  ├─ 최소 커버리지 요구 (95%)
  ├─ 비동기 테스트 지원
  └─ 테스트 경로 설정
```

**참조**: 언어별 설정 파일 형식은 매뉴얼 참조

### Part 2: 핵심 DNA 구현 순서 (의존성 기반)

```
구현 순서 (의존성 그래프):

Phase 1: 기반 (의존성 없음)
────────────────────────────────
1. Types      [30분]  ← 다른 모든 DNA가 의존
2. Config     [30분]  ← Types만 의존
3. Logging    [45분]  ← Config, Types 의존
4. Errors     [45분]  ← Types, Logging 의존

Phase 2: 데이터/통신
────────────────────────────────
5. Database   [1시간] ← Config, Types, Errors, Logging
6. Cache      [45분]  ← Config, Types, Errors, Logging

Phase 3: 품질/보안
────────────────────────────────
7. Testing    [30분]  ← 모든 Phase 1-2 완료 후
8. Security   [1시간] ← Database, Config, Types
```

### Part 3: 각 DNA 시스템 구현 (개념)

**참조**: 구체적 코드 예시는 언어별 매뉴얼 참조

- Python 매뉴얼: `docs/manuals/05M-01_python_implementation.md`
- TypeScript 매뉴얼: `docs/manuals/05M-02_typescript_implementation.md`
- Rust 매뉴얼: `docs/manuals/05M-03_rust_implementation.md`

---

각 DNA 시스템별 핵심 구현 체크리스트:

---

#### 3.1 Type System

**목적**: 타입 안전성 보장, 런타임 에러 방지

**핵심 체크리스트**:

```
□ 도메인 타입 정의
  ├─ Entity Base (ID, timestamps, 동등성)
  ├─ Value Object Base (불변성, 자체 검증)
  └─ Domain-specific 타입 (UserId, Money, Email 등)

□ 타입 검증
  ├─ 생성 시점 검증 (불완전한 객체 생성 금지)
  ├─ 불변성 보장
  └─ 타입 체커 0 오류 (ADR-301)

□ 공개 API
  ├─ BaseEntity, BaseValueObject export
  ├─ 도메인 타입들 export
  └─ 타입 검증 함수 (선택)
```

**파일 구조** (언어 무관):

```
core/types/
├── [entry_point]    # 공개 API export
├── base.*           # Entity/ValueObject 기반 클래스
├── ids.*            # ID 타입들 (UserId, OrderId)
└── common.*         # 공통 타입 (Email, Money)
```

**구현 요소**:

```
1. 공개 API (Entry Point)
   └─ BaseEntity, BaseValueObject, 도메인 타입들 export

2. 기반 클래스 (base.*)
   ├─ BaseEntity: ID, timestamps, 동등성 비교
   └─ BaseValueObject: 불변성, 자체 검증

3. ID 타입들 (ids.*)
   ├─ UserId, OrderId, ProductId 등
   ├─ 타입 안전성 (타입 구분)
   └─ ID 생성 함수

4. 공통 값 객체 (common.*)
   ├─ Email: 이메일 검증
   ├─ Money: 정밀 계산, 통화 관리
   └─ PhoneNumber: 전화번호 형식 검증
```

**구현 체크리스트**:

```
□ Base 클래스 구현
  ├─ Entity: 식별자 기반 동등성
  ├─ ValueObject: 값 기반 동등성
  └─ 불변성 보장 (방어적 복사)

□ ID 타입 구현
  ├─ 타입 안전 ID (UserId ≠ OrderId)
  ├─ ID 생성 함수 (UUID/ULID 등)
  └─ 타입 체커 검증 통과

□ 값 객체 구현
  ├─ Email: 형식 검증
  ├─ Money: 정밀 계산 (부동소수점 금지)
  └─ 도메인 규칙 검증

□ 테스트 작성
  ├─ ID 고유성 검증
  ├─ 값 객체 검증 로직 테스트
  ├─ Money 연산 테스트 (덧셈, 통화 체크)
  └─ 불완전한 객체 생성 방지 확인
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조



#### 3.2 Configuration System

**목적**: 환경별 설정 관리, 타입 안전성 보장

**파일 구조** (언어 무관):

```
core/config/
├── [entry_point]    # 공개 API export
├── settings.*       # 환경 설정 클래스
└── validators.*     # 커스텀 검증 (선택)
```

**구현 요소**:

```
1. Settings 클래스
   ├─ 환경 변수 자동 로딩 (.env.*)
   ├─ 타입 안전 필드 정의
   ├─ 기본값 제공
   └─ 필수 값 검증

2. 설정 카테고리
   ├─ 환경: environment, debug
   ├─ Database: URL, pool_size
   ├─ Cache: URL, TTL
   ├─ Logging: level, format
   └─ External API: keys, rate_limit

3. 접근 패턴
   ├─ 싱글톤 인스턴스
   ├─ get_settings() 함수
   └─ 타입 안전한 접근
```

**구현 체크리스트**:

```
□ Settings 클래스 정의
  ├─ 필드별 타입 지정
  ├─ 기본값 설정
  ├─ 범위 검증 (min/max)
  └─ 환경변수 파일 경로

□ 검증 로직
  ├─ log_level 값 제한 (DEBUG, INFO, etc.)
  ├─ log_format 값 제한 (json, console)
  ├─ URL 형식 검증
  └─ 범위 검증 (pool_size: 1-20)

□ 싱글톤 패턴
  ├─ get_settings() 구현
  ├─ 전역 인스턴스 관리
  └─ 스레드 안전성 (필요시)

□ 환경별 설정 파일
  ├─ .env.development
  ├─ .env.staging
  ├─ .env.production
  └─ 자동 로딩 구현
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조

#### 3.3 Observability System (Logging)

**목적**: 구조화 로깅, 컨텍스트 전파, 환경별 포맷

**파일 구조** (언어 무관):

```
core/logging/
├── [entry_point]    # 공개 API export
├── logger.*         # 로거 설정 및 생성
├── config.*         # 로깅 설정
└── processors.*     # 커스텀 프로세서 (선택)
```

**구현 요소**:

```
1. 로깅 설정 (configure_logging)
   ├─ 환경별 포맷 (JSON/Console)
   ├─ 로그 레벨 필터링
   ├─ 공통 프로세서 체인
   │   ├─ 컨텍스트 병합
   │   ├─ 타임스탬프 추가
   │   ├─ 로그 레벨 추가
   │   └─ 스택 정보 (에러 시)
   └─ 출력 포맷
       ├─ JSON (운영)
       └─ Console (개발)

2. 로거 인스턴스 (get_logger)
   ├─ 모듈별 로거 생성
   ├─ 캐싱 (성능)
   └─ 타입 안전 반환

3. 컨텍스트 관리
   ├─ bind_context(): trace_id, user_id 등
   ├─ clear_context(): 초기화
   └─ 요청 범위 전파
```

**구현 체크리스트**:

```
□ configure_logging() 함수
  ├─ Settings에서 log_level, log_format 로드
  ├─ 프로세서 체인 구성
  ├─ JSON vs Console 렌더러 선택
  └─ 앱 시작 시 1회 호출

□ get_logger() 함수
  ├─ 모듈명 기반 로거 반환
  ├─ 구조화 로깅 지원
  └─ 컨텍스트 자동 포함

□ 컨텍스트 헬퍼
  ├─ bind_context(trace_id, user_id, ...)
  ├─ 스레드/비동기 안전 저장
  └─ 모든 로그에 자동 포함

□ 출력 포맷
  ├─ JSON: {"event": "...", "trace_id": "...", "timestamp": "..."}
  ├─ Console: 컬러 출력 (개발 편의)
  └─ 타임스탬프 ISO 8601 형식
```

**사용 패턴**:

```
1. 앱 시작 시 초기화
   configure_logging()

2. 모듈별 로거 생성
   logger = get_logger(module_name)

3. 요청 컨텍스트 바인딩
   bind_context(trace_id="abc-123", user_id="user-456")

4. 구조화 로깅
   logger.info("주문 생성", order_id="order-789", amount=50000)

5. 출력 (JSON 예시)
   {"event": "주문 생성", "trace_id": "abc-123", "user_id": "user-456",
    "order_id": "order-789", "amount": 50000, "level": "info",
    "timestamp": "2025-12-03T10:30:00Z"}
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조

#### 3.4 Error Handling System

**목적**: 표준화된 예외 처리, 에러 코드 체계, 전역 핸들링

**파일 구조** (언어 무관):

```
core/errors/
├── [entry_point]    # 공개 API export
├── exceptions.*     # 예외 계층 정의
├── codes.*          # 에러 코드 체계
└── handlers.*       # 전역 핸들러
```

**구현 요소**:

```
1. 에러 코드 체계 (ErrorCode)
   ├─ 1xxx: 도메인 에러 (비즈니스 로직)
   │   ├─ 1001: ValidationError
   │   ├─ 1002: NotFoundError
   │   ├─ 1003: ConflictError
   │   └─ 1004+: 도메인 특화
   ├─ 2xxx: 외부 API 에러
   │   ├─ 2001: External API Error
   │   ├─ 2002: Rate Limit
   │   └─ 2003: Auth Failed
   └─ 9xxx: 시스템 에러
       ├─ 9001: Internal Error
       ├─ 9002: Database Error
       └─ 9003: Cache Error

2. 예외 계층
   ├─ AppError (최상위)
   │   ├─ message, code, details
   │   └─ to_dict() (API 응답)
   ├─ DomainError extends AppError
   │   ├─ ValidationError
   │   ├─ NotFoundError
   │   └─ ConflictError
   └─ ExternalError extends AppError
       └─ 외부 API별 에러

3. 전역 핸들러
   ├─ 예상된 에러 (AppError)
   │   ├─ 로깅 (warning level)
   │   ├─ HTTP 상태 코드 매핑
   │   └─ 구조화된 응답
   └─ 예상치 못한 에러
       ├─ 로깅 (error level + stack)
       ├─ 500 Internal Error
       └─ 상세 숨김 (보안)
```

**구현 체크리스트**:

```
□ 에러 코드 정의
  ├─ 1xxx, 2xxx, 9xxx 범위 할당
  ├─ 프로젝트별 도메인 코드 추가
  └─ Enum/Constant로 관리

□ AppError 기반 클래스
  ├─ 생성자: message, code, details
  ├─ to_dict(): API 응답 포맷
  └─ 로깅 친화적 구조

□ 도메인 예외 클래스
  ├─ ValidationError(message, field)
  ├─ NotFoundError(resource, identifier)
  ├─ ConflictError(message)
  └─ 도메인 특화 에러

□ 전역 핸들러 등록
  ├─ AppError → 적절한 HTTP 상태
  ├─ 로깅 (경고 vs 에러)
  ├─ 구조화 응답: {error: {code, message, details}}
  └─ 예상치 못한 에러 처리

□ HTTP 상태 매핑
  ├─ 1001 → 400 Bad Request
  ├─ 1002 → 404 Not Found
  ├─ 1003 → 409 Conflict
  ├─ 2xxx → 502 Bad Gateway
  └─ 9xxx → 500 Internal Error
```

**사용 패턴**:

```
1. 도메인 에러 발생
   if not order.items:
       raise ValidationError("주문 항목이 비어있습니다", field="items")

2. 리소스 없음
   order = find_order(order_id)
   if not order:
       raise NotFoundError("주문", order_id)

3. 전역 핸들러 등록
   app.add_exception_handler(Exception, global_exception_handler)

4. API 응답 (자동)
   {
     "error": {
       "code": "1001",
       "message": "주문 항목이 비어있습니다",
       "details": {"field": "items"}
     }
   }
```

**참조**: 구체적 코드는 언어별 매뉴얼 참조



### Part 4: 통합 검증

#### 4.1 DNA 통합 테스트

**목적**: DNA 시스템 간 연동 검증

**테스트 시나리오**:

```
1. Logging ↔ Config 연동
   ├─ 설정(Settings)에서 log_level, log_format 로드
   ├─ 로거 초기화 시 설정 반영 확인
   └─ 다양한 로그 레벨 동작 검증

2. Errors ↔ Logging 연동
   ├─ 에러 발생 시 자동 로깅
   ├─ 에러 코드, 메시지, details 포함
   └─ 로그 레벨 적절성 (warning vs error)

3. Types ↔ Errors 연동
   ├─ 타입 검증 실패 시 적절한 에러
   ├─ Money 음수 검증 → ValidationError
   └─ Email 형식 검증 → ValidationError

4. Config ↔ All Systems
   ├─ Database URL 주입
   ├─ Cache URL 주입
   ├─ External API 키 주입
   └─ 환경별 설정 격리
```

**테스트 체크리스트**:

```
□ Setup
  ├─ 테스트 환경 초기화
  ├─ DNA 시스템 설정 로드
  └─ 로깅 초기화

□ 통합 테스트
  ├─ Logging이 Config 사용 확인
  ├─ Errors가 Logging 연동 확인
  ├─ Types 검증 실패 → 에러 확인
  └─ 전체 플로우 E2E 테스트

□ 품질 기준
  ├─ 모든 테스트 통과
  ├─ 통합 커버리지 85%+
  └─ 실제 DB/Cache 사용 (Mock 최소화)
```

**참조**: 구체적 테스트 코드는 언어별 매뉴얼 참조

#### 4.2 품질 검증

**목적**: DNA 시스템 품질 게이트 통과

**검증 항목** (ADR 참조):

```
1. Type Checker (ADR-301)
   ├─ Strict 모드 실행
   ├─ 0 errors 필수
   └─ 예상 결과: "Success: no issues found"

2. Linter (ADR-302)
   ├─ 코드 스타일 검증
   ├─ 0 violations 필수
   └─ 예상 결과: "All checks passed!"

3. Formatter (ADR-302)
   ├─ 자동 코드 정렬
   └─ 일관된 스타일 적용

4. Test + Coverage (ADR-801)
   ├─ 단위 + 통합 테스트 실행
   ├─ 최소 커버리지: 95%
   └─ 예상 결과: "PASSED, Coverage 95%+"

5. 전체 검증
   ├─ CI 파이프라인 통과
   ├─ Pre-commit hooks 통과
   └─ 품질 게이트 100% 통과
```

**실행 순서**:

```
Step 1: Type Checker → 0 errors
Step 2: Linter → 0 violations
Step 3: Formatter → 자동 적용
Step 4: Tests → 95%+ coverage
Step 5: Integration → 전체 검증
```

**참조**: 언어별 명령어는 매뉴얼 참조

#### 4.3 DNA 완성도 평가 (Kent Beck 기준)

```
DNA 성숙도 레벨:

Level 0 (미완성): 0-3개 DNA 동작
Level 1 (최소):   4-6개 DNA 동작
Level 2 (양호):   7-9개 DNA 동작
Level 3 (완성):   10-11개 DNA 동작 ← 목표!

Kent Beck 수준 = Level 3 (10/11개 이상)
```

---

## 📄 구현 완료 문서 템플릿

### 05D-01_dna_implementation.md

```markdown
# DNA 시스템 구현 완료 문서

## 1. 구현 현황

### 1.1 완료된 DNA 시스템

| DNA 시스템 | 상태 | 파일 수 | 테스트 커버리지 | 담당자 |
|-----------|------|--------|---------------|-------|
| Types | ✅ 완료 | 4 | 98% | - |
| Config | ✅ 완료 | 3 | 95% | - |
| Logging | ✅ 완료 | 4 | 96% | - |
| Errors | ✅ 완료 | 4 | 97% | - |
| Database | ✅ 완료 | 5 | 94% | - |
| Cache | ✅ 완료 | 3 | 95% | - |
| Security | ⏳ 진행 중 | 2 | 80% | - |
| ... | ... | ... | ... | ... |

### 1.2 품질 메트릭

```

Type Checker: 0 errors ✅
Linter:       0 violations ✅
Tests:        45 passed, 0 failed ✅
Coverage:     96% (목표: 95%) ✅

```
## 2. 디렉토리 구조

```

core/
├── [entry_point]       # DNA 공개 API
├── logging/
│   ├── [entry_point]
│   ├── logger.*        # 285 lines
│   ├── config.*        # 45 lines
│   └── processors.*    # 62 lines
├── config/
│   ├── [entry_point]
│   ├── settings.*      # 120 lines
│   └── validators.*    # 35 lines
├── types/
│   ├── [entry_point]
│   ├── base.*          # 50 lines
│   ├── ids.*           # 40 lines
│   └── common.*        # 85 lines
├── errors/
│   ├── [entry_point]
│   ├── exceptions.*    # 95 lines
│   ├── codes.*         # 45 lines
│   └── handlers.*      # 60 lines
└── database/
    ├── [entry_point]
    ├── session.*       # 75 lines
    ├── base.*          # 55 lines
    └── mixins.*        # 40 lines

```
## 3. 공개 API

### 3.1 사용 예시 (개념)

```

# DNA 임포트

import 필요한 시스템 from core

필수 임포트:

  - Logging: get_logger, configure_logging
  - Config: get_settings
  - Types: UserId, OrderId, Money
  - Errors: NotFoundError, ValidationError
  - Database: get_session

# 초기화

configure_logging()
settings = get_settings()
logger = get_logger(module_name)

# 사용

logger.info("서비스 시작", environment=settings.environment)

database_session 사용:

  - 세션 획득
  - 트랜잭션 수행
  - 자동 커밋/롤백

```
**참조**: 구체적 코드는 언어별 매뉴얼 참조

## 4. Stage 6 전달 사항

### 4.1 Project Standards에 포함할 규칙

- [ ] 직접 출력 금지 (print/console) → get_logger() 사용
- [ ] 환경변수 직접 접근 금지 → get_settings() 사용
- [ ] 일반 Exception 금지 → AppError 계층 사용
- [ ] 직접 쿼리 문자열 금지 → ORM/쿼리빌더 사용 (ADR-501)

### 4.2 자동화 설정

- [ ] Pre-commit hooks 설정 (품질 게이트)
- [ ] CI 파이프라인에 DNA 테스트 포함
- [ ] Import 규칙 강제 (layer 경계)

```

---

## ✏️ DNA 연동 패턴 (개념)

**목적**: DNA 시스템 간 연동 방식 이해

### 패턴 1: Logging ↔ Config

**연동 개념**:

```
configure_logging() 함수:
  1. get_settings()로 설정 로드
  2. 환경별 로거 설정
     - 개발: 컬러 콘솔, DEBUG
     - 운영: JSON, WARNING
  3. 도메인 특화 컨텍스트 추가
     - trace_id, user_id, account_id 등
```

**핵심 포인트**:

- Config에서 log_level, log_format 동적 로드
- 환경 변경 시 코드 수정 불필요
- 도메인 컨텍스트 자동 포함

### 패턴 2: Errors ↔ Logging

**연동 개념**:

```
global_exception_handler():
  1. 에러 타입별 로그 레벨 결정
     - AppError → warning
     - 중요 경로 에러 → critical
     - 예상치 못한 에러 → error + stack
  2. 요청 컨텍스트 포함
     - trace_id, user_id, path
  3. 구조화 로깅
     - error_code, message, details
```

**핵심 포인트**:

- 에러 발생 = 자동 로깅
- 에러 코드로 로그 레벨 결정
- 컨텍스트 전파 (trace_id)

### 패턴 3: 전체 DNA 연동

**도메인 서비스에서 DNA 활용**:

```
OrderService.create_order():
  1. Types DNA
     - 타입 안전 파라미터 (UserId, Money)
     - ID 생성 (generate_order_id)

  2. Logging DNA
     - 컨텍스트 바인딩 (bind_context)
     - 단계별 로깅 (info/error)

  3. Errors DNA
     - 검증 실패 → ValidationError
     - 외부 API 실패 → ExternalError

  4. Database DNA
     - 세션 관리 (get_session)
     - 트랜잭션 (commit/rollback)

  5. Cache DNA
     - 시세 캐싱 (@cached decorator)

  6. Config DNA
     - 외부 API 설정 (rate_limit 등)
```

**핵심 포인트**:

- 도메인 로직에만 집중
- DNA가 횡단 관심사 처리
- 일관성 자동 보장

**참조**: 구체적 코드는 언어별 매뉴얼 참조

---

## ✅ Stage 5 완료 체크리스트

### 구조 검증

- [ ] core/ 디렉토리 생성됨
- [ ] 각 DNA 시스템 하위 디렉토리 존재
- [ ] tests/unit/core/ 테스트 디렉토리 존재
- [ ] tests/integration/core/ 통합 테스트 존재

### 필수 DNA 구현 (5개)

- [ ] **Type System**: ID 타입, 공통 값 객체 구현
- [ ] **Configuration System**: Settings 클래스, 환경별 분리
- [ ] **Observability System**: 로깅 라이브러리 (ADR-401), get_logger() 동작
- [ ] **Error Handling System**: 예외 계층, 에러 코드 정의
- [ ] **Testing System**: 테스트 프레임워크 (ADR-801), 커버리지 95%+

### 패밀리별 추가 DNA

- [ ] **Data System (DB)** (A-A-B 필수): ORM/쿼리빌더 (ADR-501) 세션 관리
- [ ] **Data System (Cache)** (A-A-B 권장): 캐시 클라이언트 (ADR-502)
- [ ] **Security System** (A-A-B 필수): 인증/인가 미들웨어

### 품질 검증

- [ ] Type Checker 0 errors (ADR-301)
- [ ] Linter 0 violations (ADR-302)
- [ ] 테스트 통과 (단위 + 통합)
- [ ] 커버리지 95%+ (ADR-801)

### 통합 검증

- [ ] DNA 간 의존성 정상 (Types → Config → Logging → Errors)
- [ ] 전체 통합 테스트 통과
- [ ] Kent Beck 수준 달성 (10/11개 이상)

### 산출물 생성

- [ ] `05D-01_dna_implementation.md` 작성
- [ ] Stage 6 전달 사항 정리

---

## 🔗 Stage 5 → Stage 6 연결

### Stage 6에 전달하는 것

| 전달 항목       | 내용                        | 용도                      |
| --------------- | --------------------------- | ------------------------- |
| 구현된 DNA 모듈 | core/                       | 프로젝트 표준의 기반      |
| 금지 규칙       | 직접 출력, 환경변수 접근 등 | PROJECT_STANDARDS.md 작성 |
| 자동화 설정     | 설정 파일, pre-commit hooks | 강제 규칙 설정            |

### Stage 6 미리보기

```
Stage 6: Project Standards
├─ PROJECT_STANDARDS.md 작성
│   - 코드 스타일 규칙
│   - DNA 사용 규칙 (금지/필수)
│   - 아키텍처 규칙
├─ 자동화 설정
│   - pre-commit hooks
│   - import-linter
│   - CI 파이프라인
└─ 강제 규칙 검증
```

---

## ⏪ 이전 Stage 검증 및 수정 프로토콜

### 검증 시점

- Stage 5 시작 전 필수 체크
- 각 DNA 시스템 구현 완료 후 청사진과 교차 검증

### 검증 대상

| Stage   | 산출물      | 검증 항목              |
| ------- | ----------- | ---------------------- |
| Stage 1 | 01C-01_*.md | 구현 수준이 NFR 만족?  |
| Stage 2 | 02C-01_*.md | 기술 제약 내에서 구현? |
| Stage 3 | 03A-*_*.md  | ADR 결정대로 구현?     |
| Stage 4 | 04B-01_*.md | DNA 청사진대로 구현?   |

### 오류 발견 시 프로토콜

```
Stage 5에서 Stage 1-4 오류 발견 시:

Step 1: 오류 발견 및 문서화
├─ 발견 위치: DNA 시스템 [N] 구현 중
├─ 오류 내용: [구체적 설명]
├─ 영향 Stage: Stage [1, 2, 3, 또는 4]
└─ 기록: 05D-01에 "발견된 이슈" 추가

Step 2: 영향 범위 파악
├─ 청사진(Stage 4) 수정 필요?
├─ ADR(Stage 3) 수정 필요?
├─ 제약(Stage 2) 재검토 필요?
└─ 재작업 예상: [X]시간

Step 3: 해당 Stage로 이동 → 수정
├─ 해당 산출물 수정
├─ 버전 업데이트
└─ 수정 검증

Step 4: 중간 Stage 전파
├─ Stage 4, 5 영향 확인
└─ 필요 시 청사진 업데이트

Step 5: Stage 5 재진행
├─ 수정된 청사진으로 구현 재검토
└─ 코드 일관성 확인

Step 6: 검증 → Stage 6 전달 ✅
```

### 흔한 오류 패턴

| 오류 유형     | 예시                        | 해결                    |
| ------------- | --------------------------- | ----------------------- |
| 청사진 불완전 | 인터페이스 정의 누락        | Stage 4 청사진 보완     |
| ADR 미반영    | 로깅 포맷 ADR과 구현 불일치 | 구현 수정 또는 ADR 갱신 |
| 의존성 오류   | 순환 의존성 발생            | Stage 4 설계 재검토     |

### 추적성

```
수정 이력: docs/revision_log.md
코드 주석: # Stage 5 구현 - ADR-XXX 참조
```

---

## 💡 핵심 원칙 요약

### DNA 구현의 3대 원칙

```
1. 표준 라이브러리 우선
────────────────────────────────
❌ 직접 구현 (89개 클래스, 1,679줄)
✅ 검증된 라이브러리 사용 (ADR 참조, 3줄)

2. 인터페이스 추상화
────────────────────────────────
Protocol 정의 → 구현체 교체 가능
테스트 시 Mock 주입 용이

3. 설정 주입
────────────────────────────────
설정 라이브러리로 환경별 분리 (ADR-402)
.env.development / .env.production
```

### 구현 순서 (의존성 기반)

```
Phase 1: 기반 (의존성 없음)
Types → Config → Logging → Errors

Phase 2: 데이터/통신
Database → Cache → Messaging

Phase 3: 품질/보안
Testing → Security → Monitoring
```

### 품질 기준 (Zero Tolerance)

```
Type Checker: 0 errors    (타입 안전성, ADR-301)
Linter:       0 violations (코드 품질, ADR-302)
Tests:        0 failures   (기능 정확성, ADR-801)
Coverage:     95%+         (테스트 충분성)
```

---

**Remember**: 

- DNA 없이 도메인 구현 = 기반 없는 건물
- 표준 라이브러리 우선 = 바퀴 재발명 금지
- 의존성 순서 준수 = Types → Config → Logging → Errors
- Kent Beck 수준 = 10/11개 DNA 동작

*DNA가 "환경"으로 구축되어야 도메인 코드가 그 위에서 안전하게 실행됩니다.*
