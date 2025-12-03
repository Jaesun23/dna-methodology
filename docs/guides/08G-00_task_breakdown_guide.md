# Task Breakdown 작성 가이드

> **목적**: Stage 8 - Blueprint(초상세)를 AI가 집중 구현 가능한 Task 단위로 분해
>
> **버전**: v2.0 (2025-11-12)
> - v2.0: Stage 8 범위 명시, 입력/출력 문서 추가

---

## 📥 입력 문서 (Stage 7에서 받은 것)

#### 1. **`07B-01_project_blueprint.md`** (필수)
- 초상세 프로젝트 청사진 (수천 줄)
- **활용**: 작업 분해의 기반

#### 2. **`06D-01_project_standards.md`** (참고)
- 프로젝트 표준
- **활용**: 작업별 표준 반영

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 문서)

### 필수 문서

#### 1. **`08T-01_task_breakdown.md`** - 작업 분해 (THE 산출물)
**내용**:
- AI가 4시간 이내 완료 가능한 작업 단위
- 독립적으로 테스트 가능
- Necessary Information Only

**구조**:
```markdown
# TASK BREAKDOWN

## Task 001: Order Entity 구현
**목표**: Order 엔티티 클래스 및 DB 모델 구현
**예상 시간**: 2-3시간
**의존성**: 없음

### 입력
- ADR-116: Order Schema Design
- 표준: Naming, Validation 규칙

### 출력
- `src/domains/order/models.py`
- 단위 테스트 (95%+ 커버리지)

### 제약
- MUST use Pydantic BaseModel
- UUID for primary key

### 참고
- Blueprint Section 3.2

---

## Task 002: Order Repository 구현
**목표**: Order CRUD 작업
**예상 시간**: 3-4시간
**의존성**: Task 001

...
```

**특징**:
- 1개 Task = 1개 파일 또는 1개 기능
- 4시간 이내 완료 크기
- 독립 테스트 가능
- 명확한 입력/출력

---

## 🔄 다음 Stage로 전달되는 것

Stage 8 → Stage 9:
- ✅ 작업 목록 (Task 001~N)
- ✅ 각 작업의 목표, 시간, 의존성
- ✅ 우선순위

Stage 9 (Checklist)에서는:
- 각 Task마다 TDD 9-Step 체크리스트 생성
- 단계별 실행 가이드

---

## 1. 개요

### 왜 작업분해가 필요한가?

```python
# 문제
Blueprint = 5000줄  # AI가 한 번에 처리 불가
→ 컨텍스트 초과, 집중력 저하, 실수 증가

# 해결
Task = 100줄씩 분해  # AI가 처리 가능한 단위
→ 명확한 집중, 높은 품질, 검증 가능
```

### 작업분해의 목표

1. **정보 압축**: Blueprint 5000줄 → Task 100줄씩
2. **Necessary Information Only**: 이 Task에 필요한 것만
3. **완전한 레고블럭**: 독립적으로 테스트 가능한 기능 단위

### 두 가지 완성 조건

**일관성 (Consistency)**:
- 모든 Task가 같은 도구 사용 (DNA 시스템 환경 기반)
- 모든 Task가 같은 패턴 따름
- 모든 Task가 같은 표준 준수

**누락없음 (No Omissions)**:
- Blueprint의 모든 기능이 Task로 분해됨
- Task 목록 = Blueprint 기능 목록
- 빠진 Task 없음

---

### 에이전트 vs 2호: 왜 에이전트 기준으로 계산하는가? ⭐

**핵심 차이점**:

```python
2호 (오케스트레이터):
    컨텍스트 = 200K
    압축 기능 = ✅ Compact 있음
    역할 = "전체 흐름 관리, 큰 줄기 유지"
    특징 = "압축하면서 긴 작업 가능"
    결과 = "맥락 유지하며 계속 진행"

에이전트 (작업 실행자):
    컨텍스트 = 200K (독립적)
    압축 기능 = ❌ 없음!
    역할 = "독립적 작업 실행"
    특징 = "200K 꽉 차면 종료 💥"
    결과 = "한 세션 안에 완료 필수"
```

**왜 중요한가?**

1. **2호 기준으로 계산하면**: "이 정도면 되겠지?" → 에이전트가 중간에 종료
2. **에이전트 기준으로 계산하면**: 한 세션 안에 안전하게 완료 가능

**작업분해 시 반드시 기억**:
- ✅ 에이전트는 압축 없음 = 200K가 hard limit
- ✅ 체크리스트는 에이전트가 읽음 (2호 아님)
- ✅ 작업 크기는 에이전트 기준 (80-90K 안전 범위)

---

## 2. Task 분할 방식 선택 ⭐

### Case 1: 모듈화 분할 (수평 분할)

**특징**: 재사용 가능한 독립 모듈을 먼저 만들고, 나중에 조립

**언제 사용**:
- ✅ 재사용성이 높은 경우
- ✅ 복잡한 로직
- ✅ 팀 협업 (여러 사람이 동시 작업)

**예시: Auth 시스템**
```
Task T2.1.1: JWT 생성 모듈 (create_token)
  → 입력: user_id
  → 출력: token
  → 의존성: 없음 (독립 모듈)

Task T2.1.2: JWT 검증 모듈 (validate_token)
  → 입력: token
  → 출력: user_id or None
  → 의존성: 없음 (독립 모듈)

Task T2.2.1: Login 엔드포인트
  → 입력: email, password
  → 출력: token
  → 의존성: T2.1.1 (create_token 사용)

Task T2.2.2: Logout 엔드포인트
  → 의존성: T2.1.2 (validate_token 사용)

Task T2.2.3: Refresh 엔드포인트
  → 의존성: T2.1.1, T2.1.2 (둘 다 사용)
```

**장점**:
- 모듈 재사용 가능
- 병렬 작업 가능 (T2.1.1과 T2.1.2를 동시에)
- 테스트 독립적

**단점**:
- 초기 설계 복잡
- 조립 단계 필요

---

### Case 2: 단계별 구현 (수직 분할)

**특징**: 전체 기능을 하나씩 완성

**언제 사용**:
- ✅ 빠른 배포 필요
- ✅ 단순한 기능
- ✅ 학습 곡선 (새로운 기술 학습 중)

**예시: Auth 시스템**
```
Task T2.1.1: Login 기능 전체
  → JWT 생성 로직 포함
  → JWT 검증 로직 포함
  → Login 엔드포인트 완성
  → ✅ Login 완전 작동!

Task T2.2.1: Logout 기능 전체
  → JWT 검증 로직 재구현 (또는 복사)
  → Logout 엔드포인트 완성
  → ✅ Logout 완전 작동!

Task T2.3.1: Refresh 기능 전체
  → JWT 검증 + 생성 로직 재구현
  → Refresh 엔드포인트 완성
  → ✅ Refresh 완전 작동!
```

**장점**:
- 빠른 결과 확인
- 각 기능이 완전히 작동
- 간단한 구조

**단점**:
- 코드 중복 가능
- 병렬 작업 어려움

---

### 분할 방식 선택 가이드

```
┌─ 재사용성이 높은가?
│  ├─ Yes → Case 1 (모듈화)
│  └─ No
│      └─ 빠른 배포가 중요한가?
│          ├─ Yes → Case 2 (단계별)
│          └─ No
│              └─ 복잡도가 높은가?
│                  ├─ Yes → Case 1 (모듈화)
│                  └─ No → Case 2 (단계별)
```

**실용적 판단 기준**:
- **5회 이상 재사용** 예상 → Case 1
- **2-3회 재사용** → Case 2 (나중에 리팩토링)
- **1회만 사용** → Case 2

---

## 3. Task 나누기 4가지 질문

### Q1: 200K 컨텍스트로 가능한가?

**체크리스트 분량 가이드라인** (Agent 기준):
```python
# 일반적인 체크리스트 크기
체크리스트_분량 = "보통 120줄 내외 (100-150줄 범위)"

# 컨텍스트 계산 근거 (Agent implementer 기준):
컨텍스트_사용량 = {
    "Base (시스템 + 에이전트 정의)": "41K",
    "읽기 (체크리스트 + 참조문서)": "7.5K",
    "쓰기 (생각 정리 + 코드 작성)": "22K",
    "실행/디버그 (테스트 + 수정)": "15K",
    "총합": "85.5K (120줄 기준)"
}

# ✅ 80-90K 컨텍스트 범위에서 안전하게 작업 가능
# 💡 중요: 숫자는 참고일 뿐! 작업을 완전하게 설명하는 게 우선
```

**컨텍스트 안전 범위**:
- **80K**: 안정적 ✅ (권장)
- **90K**: 빡빡함 ⚠️ (가능하지만 여유 부족)
- **100K+**: 위험 ❌ (급히 종료 가능성)
- **180K+**: 매우 위험 💥 (거의 확실히 급히 종료)

**작업량 예측의 어려움**:

```python
# 예측 가능한 것
체크리스트_분량 = "120줄" → 2.5K 토큰 (계산 가능)

# 예측 어려운 것 ⚠️
실제_작업 = {
    "예상보다 복잡한 구현",
    "테스트 실패 반복",
    "디버깅 과정 길어짐",
    "타입 오류 수정"
}
→ 실제 소모량은 작업하면서 결정됨
```

**에이전트의 위험한 행동 패턴**:

```
정상 완료:
  작업 → 테스트 → 검증 → 보고서
  컨텍스트: 150K ✅

급히 종료:
  작업 → 테스트 중... → 190K! 😱
  → 급히 보고서 작성하고 종료
  보고서: "✅ 완료했습니다"
  실제: 테스트 미완료, 검증 부족 ❌
```

**따라서**:
- 체크리스트 분량으로 "대략" 예측
- 하지만 반드시 **완료 후 검증** 필요 (Section 6 참고)
- 컨텍스트 180K 이상이면 급히 종료 의심

**너무 큰 Task 신호**:
- 체크리스트가 200줄 이상 필요할 것 같음 (컨텍스트 한계)
- 구현 코드 예상이 500줄 이상
- 5개 이상의 표준 문서 참조
- 3개 이상의 DNA 시스템 동시 사용

→ **해결**: Task를 2-3개로 분할

---

### Q2: 이 Task만으로 의미있는 기능인가?

**✅ 의미있는 Task**:
```python
# Task T2.1.1: JWT 생성 모듈
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성"""
    # ✅ 완전히 작동
    # ✅ 단독 테스트 가능
    # ✅ 의존성 없음
    return token
```

**❌ 의미없는 Task**:
```python
# Task X: User 클래스 정의만
class User:
    id: str
    email: str
    # ❌ 동작하지 않음
    # ❌ 테스트 불가능
    # ❌ 불완전한 블럭
```

**판단 기준**:
- 이 Task가 완료되면 무언가가 **작동**하는가?
- 단독으로 **테스트**할 수 있는가?
- 명확한 **입력/출력**이 있는가?

---

### Q3: 다른 Task와 일관성이 있나?

**체크 항목**:

**도구 일관성**:
```python
# ✅ 모든 Task가 같은 도구
Task T2.1.1: structlog, Pydantic, pytest
Task T2.2.1: structlog, Pydantic, pytest
Task T2.3.1: structlog, Pydantic, pytest

# ❌ Task마다 다른 도구
Task T2.1.1: structlog
Task T2.2.1: logging  # ❌ 다름!
Task T2.3.1: print()  # ❌ 완전히 다름!
```

**패턴 일관성**:
- 모든 API는 FastAPI + Pydantic
- 모든 설정은 pydantic-settings
- 모든 테스트는 Given-When-Then

**DNA 시스템 환경 기반**:
```python
# ✅ DNA 시스템 환경 사용
from core.logging import get_logger
from core.config import settings

# ❌ 커스텀 구현
import logging  # DNA 시스템에 없음!
```

---

### Q4: 청사진에서 누락된 Task는 없나?

**검증 방법**:

**1. Blueprint 기능 목록 추출**:
```markdown
# Blueprint: Auth 시스템
1. JWT 토큰 생성
2. JWT 토큰 검증
3. Login 엔드포인트
4. Logout 엔드포인트
5. Refresh 엔드포인트
6. 비밀번호 해싱
7. Redis 세션 관리
```

**2. Task 목록과 비교**:
```markdown
# Task 목록
✅ T2.1.1: JWT 생성
✅ T2.1.2: JWT 검증
✅ T2.2.1: Login 엔드포인트
✅ T2.2.2: Logout 엔드포인트
✅ T2.2.3: Refresh 엔드포인트
❌ 비밀번호 해싱 → 누락!
❌ Redis 세션 관리 → 누락!
```

**3. 누락 Task 추가**:
```markdown
추가:
- T2.1.3: 비밀번호 해싱 모듈
- T2.1.4: Redis 세션 관리 모듈
```

---

## 4. Task 문서 9-Section 템플릿

### 템플릿 구조

```markdown
# Task T{domain}.{module}.{number}: {Task 이름}

## 1. 📘 청사진 참조
**Blueprint Line {start}-{end}**: {참조 내용 요약}

## 2. 📋 프로젝트 표준 참조
**PROJECT_STANDARDS.md Line {start}-{end}**: {참조 표준}
**ARCHITECTURE.md Line {start}-{end}**: {참조 아키텍처}

## 3. 🔧 사용 도구
- **{도구명}**: {용도}

## 4. 📦 입력/출력
**입력**: {타입} - {설명}
**출력**: {타입} - {설명}

## 5. 🔗 조립 정보
**이 블럭을 사용하는 Task**: T{x.x.x}
**이 블럭이 사용하는 Task**: T{a.a.a} (또는 "없음")

## 6. 🎯 완성 기준
- [ ] {기능 동작 확인}
- [ ] {테스트 통과}

## 7. 💡 구현 힌트
```python
{실제 코드 예시}
```

## 8. ⏱️ 예상 작업 시간
총 예상: {시간}

## 9. 📌 메타정보
- 우선순위: {High/Medium/Low}
- 의존성: {선행 Task}
```

---

### 각 섹션 작성 가이드

#### Section 1: 청사진 참조

**목적**: Necessary Information Only - 이 Task에 필요한 Blueprint 부분만

**작성법**:
```markdown
## 1. 📘 청사진 참조
**Blueprint Line 145-178**: JWT 알고리즘 및 토큰 구조

핵심 내용:
- HS256 알고리즘 사용
- Payload: {user_id, exp, iat}
- TTL: 1시간 (3600초)
```

**주의**:
- ❌ Blueprint 전체 링크만 제공
- ✅ 정확한 Line 번호 + 핵심 내용 요약

---

#### Section 2: 프로젝트 표준 참조

**목적**: DNA 시스템 환경의 어떤 부분을 사용하는가

**핵심**: 800 lines 전체가 아닌, "이 Task 관련" 부분만 필터링!

**작성법**:
```markdown
## 2. 📋 프로젝트 표준 참조 (이 Task 관련만!)

#### 로깅 (standards/01_logging.md Line 12-25)
- `logger.info("event_name", key=value)` 형식 사용
- `print()` 절대 금지
- 모든 주요 작업 (생성, 수정, 삭제) 로깅 필수
- 에러는 `logger.error()` 또는 `logger.exception()` 사용

#### 설정 (standards/02_configuration.md Line 30-45)
- 모든 SECRET은 `config.get_secret("KEY_NAME")` 사용
- 하드코딩 절대 금지
- `.env` 파일에서 환경변수 관리
- Pydantic Settings 클래스 사용

#### 아키텍처 (standards/05_architecture.md Line 89-102)
- Domain Layer는 Infrastructure 의존 금지
- interfaces.py로 추상화
- import-linter로 검증
```

**파일 분리 예시**:
```
큰 문서는 파일로 분리하세요!

❌ Before:
PROJECT_STANDARDS.md (800 lines)
→ 너무 길어서 어디 읽어야 할지 모름

✅ After:
standards/
├── 01_logging.md (150 lines)
├── 02_configuration.md (120 lines)
├── 03_error_handling.md (180 lines)
├── 04_database.md (200 lines)
├── 05_architecture.md (150 lines)

각 파일이 200-500 lines로 적정!
Line 참조하기도 쉬움!
```

**필터링 절차**:
1. **이 Task가 무엇을 하나?** → JWT 토큰 생성
2. **필요한 표준 식별**:
   - 로깅? YES (토큰 생성 이벤트 기록)
   - 설정? YES (SECRET_KEY 가져오기)
   - DB? NO (JWT는 DB 안 씀)
   - 에러처리? NO (이 Task는 간단)
3. **필요한 부분만 읽기**:
   - standards/01_logging.md Line 12-25 읽기
   - standards/02_configuration.md Line 30-45 읽기
4. **Task Section 2에 요약 + Line 참조**

**주의**:
- ❌ "프로젝트 표준을 따른다" (추상적)
- ❌ "PROJECT_STANDARDS.md 전체 참조" (800 lines!)
- ✅ 구체적인 파일명 + Line 번호 + 핵심 내용 요약 (30 lines)
- ✅ "이 Task에 필요한" 부분만 필터링

**표준 문서가 없는 경우**:
```markdown
## 2. 📋 프로젝트 표준 (이 Task에서 정의)

프로젝트 초반이라 표준 문서가 없는 경우,
이 Task에서 사용할 패턴을 직접 정의하세요:

#### 로깅 (이 Task에서 정의)
- structlog 사용
- logger.info("event_name", key=value) 형식
- print() 금지

#### 설정 (이 Task에서 정의)
- config.get_secret("KEY_NAME") 패턴
- Pydantic Settings 사용

→ 나중에 이 패턴들이 반복되면
  standards/ 폴더로 추출 고려
```

---

#### Section 3: 사용 도구

**목적**: 이 Task에서 사용할 라이브러리/도구 명시

**작성법**:
```markdown
## 3. 🔧 사용 도구
- **PyJWT**: JWT 토큰 생성/검증
- **structlog**: 구조화된 로깅
- **pytest**: 테스트 프레임워크
```

**주의**:
- DNA 시스템에 설치된 도구만 사용
- 새로운 도구가 필요하면 DNA 시스템 재검토

---

#### Section 4: 입력/출력

**목적**: 이 레고블럭의 인터페이스 정의

**작성법**:
```markdown
## 4. 📦 입력/출력
**입력**: user_id: str - 사용자 고유 ID
**출력**: token: str - JWT 액세스 토큰 (HS256, 1시간 TTL)
```

**주의**:
- 타입 명시 (Pydantic 타입)
- 설명 간결하게

---

#### Section 5: 조립 정보

**목적**: Task 간 의존성 및 조립 순서

**작성법**:
```markdown
## 5. 🔗 조립 정보
**이 블럭을 사용하는 Task**: T2.2.1 (Login), T2.2.3 (Refresh)
**이 블럭이 사용하는 Task**: 없음 (독립 블럭)
```

**Case 1 (모듈화)에서 중요**:
- 어떤 Task가 이 블럭을 사용하는가?
- 이 블럭은 어떤 Task에 의존하는가?

**Case 2 (단계별)에서는**:
- 보통 "없음" 또는 간단한 의존성

---

#### Section 6: 완성 기준 + 자주 하는 실수

**목적**: 이 Task가 완료되었다는 기준 + 흔한 실수 방지

**작성법**:
```markdown
## 6. 🎯 완성 기준

### 기능 검증
- [ ] create_token(user_id) 함수 완전 작동
- [ ] 생성된 토큰이 유효한 JWT 형식
- [ ] Payload에 user_id, exp, iat 포함
- [ ] TTL 정확히 1시간 (3600초)

### 테스트 검증
- [ ] pytest 테스트 3개 통과:
  - 정상 토큰 생성
  - user_id 검증
  - 만료 시간 검증
- [ ] pytest coverage 95%+ 달성

### 품질 검증
- [ ] ruff check 0 violations
- [ ] mypy --strict 0 errors
- [ ] import-linter 0 violations
- [ ] structlog로 토큰 생성 이벤트 기록

### 자주 하는 실수 (이 Task 특화)

**실수 1: exp를 초 단위로 제공**
```python
❌ payload["exp"] = 3600  # 1970년 1월 1일 1시간 후!
✅ payload["exp"] = datetime.utcnow() + timedelta(hours=1)
```

**실수 2: SECRET_KEY 하드코딩**
```python
❌ SECRET_KEY = "my-secret-key-123"
✅ secret_key = config.get_secret("JWT_SECRET_KEY")
```

**실수 3: print() 사용**
```python
❌ print(f"Token generated for {user_id}")
✅ logger.info("token_generated", user_id=user_id)
```
```

**자주 하는 실수 작성 가이드**:

**출처**:
1. 범용 실수 (모든 Task 적용):
   - `standards/99_common_mistakes.md` 참조
   - print() 사용, 하드코딩 등
2. 도메인별 실수 (JWT, DB, API 등):
   - 과거 비슷한 Task 경험
   - 기술 스택별 known issues
3. Task별 고유 실수:
   - 구현 후 회고에서 발견
   - 다음 비슷한 Task에 적용

**큐레이션 절차**:
1. 범용 실수집에서 이 Task 관련만 선택
2. 도메인 실수 (JWT 관련) 추가
3. 3-5개로 제한 (핵심만)
4. ❌/✅ Before/After 형식으로

**주의**:
- 체크 가능한 명확한 기준
- 숫자로 표현 가능하면 숫자로 (예: "3개 통과")
- 자주 하는 실수 3-5개 (너무 많으면 안 읽음)

---

#### Section 7: 구현 힌트 (스켈레톤 수준!)

**목적**: 핵심 로직 구조 제시 (전체 코드 아님!)

**핵심**: Level 3 스켈레톤 - 40 lines 정도

**작성법**:
```markdown
## 7. 💡 구현 힌트 (스켈레톤)

### 함수 시그니처
```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (1시간 유효)

    Raises:
        ValueError: user_id가 빈 문자열인 경우
    """
```

### 핵심 로직 구조
```python
# src/auth/token.py
import jwt
from datetime import datetime, timedelta
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성."""
    # 1. Payload 구성
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    # 2. SECRET_KEY 가져오기
    secret_key = config.get_secret("JWT_SECRET_KEY")

    # 3. 토큰 생성
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    # 4. 로깅
    logger.info("token_generated", user_id=user_id)

    return token
```

**Agent가 추가해야 할 것**:
- user_id validation (빈 문자열 체크)
- 에러 처리 (try-except)
- 추가 payload 필드 (jti 등)

### 테스트 스켈레톤 (Given-When-Then)
```python
# tests/auth/test_token.py
def test_create_token_success():
    """Given: 유효한 user_id
       When: create_token 호출
       Then: 유효한 JWT 토큰 반환"""
    # Given
    user_id = "test-user-123"

    # When
    token = create_token(user_id)

    # Then
    assert isinstance(token, str)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded["user_id"] == user_id
    assert "exp" in decoded
    # Agent가 exp 시간 검증 등 추가
```
```

**스켈레톤 수준 가이드**:

**Level 1: 인터페이스만** (20 lines) - **불충분** ❌
```python
def create_token(user_id: str) -> str:
    """JWT 토큰 생성."""
    pass
```
→ Agent가 구조를 모름

**Level 2: 주석 의사코드** (30 lines) - **부족** ❌
```python
def create_token(user_id: str) -> str:
    # 1. payload 만들기
    # 2. jwt로 인코딩하기
    # 3. 로깅하기
    # 4. 반환하기
```
→ 구체성 부족

**Level 3: 핵심 로직 스켈레톤** (40 lines) - **균형점!** ✅
```python
def create_token(user_id: str) -> str:
    payload = {"user_id": user_id, "exp": ...}
    secret_key = config.get_secret("JWT_SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    logger.info("token_generated", user_id=user_id)
    return token
```
→ 구조는 명확, 세부사항은 Agent가 채움 (TDD 가능!)

**Level 4: 전체 구현** (200+ lines) - **과함!** ❌
```python
def create_token(user_id: str) -> str:
    try:
        if not user_id:
            raise ValueError(...)
        if not isinstance(user_id, str):
            raise TypeError(...)
        # ... 100+ lines of validation
        # ... 50+ lines of edge cases
        # ... 50+ lines of error handling
    except Exception as e:
        logger.exception(...)
        raise
```
→ Agent가 복붙만 함. TDD 불가능.

**선택: Level 3 (스켈레톤)** - 이유:
- 핵심 로직 구조 명확
- Agent가 validation, 에러 처리 추가
- TDD 가능 (테스트 실패 → 수정 반복)
- "Necessary Information Only" 준수

**주의**:
- ✅ 실행 가능한 수준 (import 정확, 함수 호출 가능)
- ✅ DNA 시스템 환경 사용 (core.*)
- ✅ 핵심 로직만 (40 lines)
- ❌ 전체 에러 처리 포함 (Agent가 추가)
- ❌ 모든 엣지 케이스 (Agent가 추가)
- ✅ 주석으로 단계 설명

---

#### Section 8: 예상 작업 시간

**목적**: Task 일정 계획

**작성법**:
```markdown
## 8. ⏱️ 예상 작업 시간
- 구현: 30분
- 테스트 작성: 30분
- 품질 검증: 10분
- 문서화: 10분
- 총 예상: 1시간 20분
```

---

#### Section 9: 메타정보

**목적**: 프로젝트 관리 정보

**작성법**:
```markdown
## 9. 📌 메타정보
- 우선순위: High (다른 Task의 의존성)
- 의존성: 없음
- 태그: #auth #jwt #core
```

---

## 5. 실전 예시: Auth 시스템 분해

### Blueprint (요약)

```markdown
# Auth 시스템 Blueprint (1000줄 중 요약)

## 기능 목록
1. JWT 토큰 관리
   - 생성 (HS256, 1시간 TTL)
   - 검증 (만료, 형식 체크)
2. Login 엔드포인트
   - POST /auth/login
   - 5회 실패 → 30분 잠금
3. Logout 엔드포인트
   - POST /auth/logout
4. Refresh 엔드포인트
   - POST /auth/refresh

## 기술 스택
- PyJWT
- structlog
- Redis (세션 관리)
- FastAPI
```

---

### Case 1: 모듈화 분할 결과

```markdown
# Auth 시스템 Task 목록 (Case 1)

## 모듈 레이어
- Task T2.1.1: JWT 생성 모듈
- Task T2.1.2: JWT 검증 모듈
- Task T2.1.3: 비밀번호 해싱 모듈
- Task T2.1.4: Redis 세션 관리 모듈

## API 레이어 (모듈 사용)
- Task T2.2.1: Login 엔드포인트 (T2.1.1, T2.1.3, T2.1.4 사용)
- Task T2.2.2: Logout 엔드포인트 (T2.1.2, T2.1.4 사용)
- Task T2.2.3: Refresh 엔드포인트 (T2.1.1, T2.1.2 사용)
```

**조립 순서**:
1. 모듈 레이어 병렬 구현 (T2.1.1 ~ T2.1.4)
2. API 레이어 순차 구현 (T2.2.1 → T2.2.2 → T2.2.3)

---

### Case 2: 단계별 구현 결과

```markdown
# Auth 시스템 Task 목록 (Case 2)

- Task T2.1.1: Login 기능 전체 (JWT 생성 포함)
- Task T2.2.1: Logout 기능 전체 (JWT 검증 포함)
- Task T2.3.1: Refresh 기능 전체 (JWT 생성+검증 포함)
```

**구현 순서**:
1. Login 완전 구현 → ✅ 로그인 작동
2. Logout 완전 구현 → ✅ 로그아웃 작동
3. Refresh 완전 구현 → ✅ 토큰 갱신 작동

---

### Task T2.1.1 전체 예시 (Case 1)

````markdown
# Task T2.1.1: JWT 토큰 생성 모듈

## 1. 📘 청사진 참조
**Blueprint Line 145-178**: JWT 알고리즘 및 토큰 구조

핵심 내용:
- HS256 알고리즘 사용
- Payload: {user_id, exp, iat}
- TTL: 1시간 (3600초)
- Secret key는 환경 설정에서 로드

## 2. 📋 프로젝트 표준 참조
**PROJECT_STANDARDS.md Line 12-25**: structlog 로깅 패턴
- 모든 토큰 생성 이벤트 기록
- user_id 포함한 구조화된 로그

**PROJECT_STANDARDS.md Line 45-58**: Pydantic 모델 규칙
- 환경 설정은 pydantic-settings 사용

## 3. 🔧 사용 도구
- **PyJWT**: JWT 토큰 생성/검증 표준 라이브러리
- **structlog**: 구조화된 로깅
- **pydantic-settings**: 환경 설정 관리
- **pytest**: 테스트 프레임워크

## 4. 📦 입력/출력
**입력**: user_id: str - 사용자 고유 ID
**출력**: token: str - JWT 액세스 토큰 (HS256, 1시간 TTL)

## 5. 🔗 조립 정보
**이 블럭을 사용하는 Task**:
- T2.2.1 (Login 엔드포인트)
- T2.2.3 (Refresh 엔드포인트)

**이 블럭이 사용하는 Task**: 없음 (독립 블럭)

## 6. 🎯 완성 기준
- [ ] create_token(user_id) 함수 완전 작동
- [ ] 생성된 토큰이 유효한 JWT 형식
- [ ] Payload에 user_id, exp, iat 포함
- [ ] TTL 정확히 1시간 (3600초)
- [ ] pytest 테스트 3개 통과:
  - 정상 토큰 생성
  - user_id 검증
  - 만료 시간 검증
- [ ] structlog로 토큰 생성 이벤트 기록
- [ ] mypy --strict 0 errors
- [ ] ruff check 0 violations

## 7. 💡 구현 힌트
```python
# src/auth/token.py
import jwt
from datetime import datetime, timedelta
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (HS256, 1시간 TTL)
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256"
    )

    logger.info("token_created", user_id=user_id)

    return token
    
# tests/auth/test_token.py
import jwt
from datetime import datetime, timedelta
from auth.token import create_token

def test_create_token_정상():
    """Given: user_id가 주어졌을 때
    When: create_token을 호출하면
    Then: 유효한 JWT 토큰이 생성된다
    """
    # Given
    user_id = "user123"

    # When
    token = create_token(user_id)

    # Then
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    assert decoded["user_id"] == user_id
    assert "exp" in decoded
    assert "iat" in decoded

def test_create_token_TTL():
    """Given: 토큰을 생성했을 때
    When: exp를 확인하면
    Then: 정확히 1시간 후로 설정되어 있다
    """
    # Given & When
    token = create_token("user123")
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])

    # Then
    exp = datetime.fromtimestamp(decoded["exp"])
    iat = datetime.fromtimestamp(decoded["iat"])
    assert (exp - iat).total_seconds() == 3600
```

## 8. ⏱️ 예상 작업 시간

- 구현: 30분
- 테스트 작성: 30분
- 품질 검증: 10분
- 문서화: 10분
- 총 예상: 1시간 20분

## 9. 📌 메타정보

- 우선순위: High (다른 Task의 의존성)
- 의존성: 없음 (첫 번째 구현 가능)
- 태그: #auth #jwt #core #module
````

---

## 6. 작업분해 완료 검증

### 분할 방식 검증
- [ ] Case 1 vs Case 2 선택 근거가 명확한가?
- [ ] 모든 Task가 같은 방식으로 분할되었는가?
- [ ] Case 1인 경우, 모듈 레이어와 API 레이어가 구분되었는가?

### Task 품질 검증
- [ ] 각 Task는 200K 컨텍스트 내인가?
- [ ] 각 Task는 의미있는 기능 단위인가? (독립 테스트 가능)
- [ ] 모든 Task가 DNA 시스템 환경 기반인가?
- [ ] 모든 Task가 9-section을 갖추었는가?

### 완성도 검증
- [ ] Blueprint의 모든 기능이 Task로 분해되었는가?
- [ ] Task 간 의존성이 명확한가? (Section 5)
- [ ] 조립 순서가 정의되었는가?
- [ ] 누락된 Task가 없는가? (Q4 체크)

### 일관성 검증
- [ ] 모든 Task가 같은 도구를 사용하는가?
- [ ] 모든 Task가 같은 표준을 따르는가?
- [ ] 청사진 참조가 정확한가? (Line 번호 확인)
- [ ] 프로젝트 표준 참조가 정확한가?

### 템플릿 준수 검증
- [ ] Section 1: 청사진 참조 (Line 번호 + 요약)
- [ ] Section 2: 표준 참조 (Line 번호 + 요약)
- [ ] Section 3: 사용 도구 명시
- [ ] Section 4: 입력/출력 타입 명시
- [ ] Section 5: 조립 정보 명시
- [ ] Section 6: 완성 기준 체크리스트
- [ ] Section 7: 구현 힌트 코드 예시
- [ ] Section 8: 예상 작업 시간
- [ ] Section 9: 메타정보

---

### 에이전트 완료 후 검증 ⭐

**왜 필요한가?**
- 에이전트는 컨텍스트가 꽉 차면 급히 종료
- 보고서는 "✅ 완료"라고 하지만 실제로는 불완전할 수 있음
- 2호는 Quality Guardian으로서 반드시 검증 필요

**검증 체크리스트** (에이전트 작업 완료 후):

#### 1. 컨텍스트 사용량 확인
```python
if 에이전트_컨텍스트_사용량 > 180K:
    print("⚠️ 급히 종료했을 가능성!")
    print("→ 더 꼼꼼히 검토 필요")
```
- [ ] 에이전트가 사용한 컨텍스트 확인
- [ ] 180K 이상이면 급히 종료 의심

#### 2. 실제 산출물 확인
- [ ] 요청한 파일이 모두 생성되었나?
- [ ] 코드에 TODO, pass가 없나?
- [ ] 타입 힌트가 완전한가?
- [ ] 에러 처리가 구현되었나?

#### 3. 테스트 결과 확인 (직접 실행!)
```bash
# 에이전트 보고서만 믿지 말고 직접 실행!
pytest tests/ -v
pytest --cov=src tests/ --cov-report=term-missing
```
- [ ] 테스트가 실제로 100% 통과하나?
- [ ] Coverage가 95% 이상인가?
- [ ] 실패한 테스트가 없나?

#### 4. 품질 검증 (직접 실행!)
```bash
ruff check .
mypy --strict src/
```
- [ ] Ruff violations 0개?
- [ ] MyPy errors 0개?
- [ ] Import-linter violations 0개?

#### 5. 로깅 및 표준 준수
- [ ] print() 대신 structlog 사용?
- [ ] 하드코딩된 SECRET 없나?
- [ ] PROJECT_STANDARDS.md 준수?

**문제 발견 시 조치**:
```python
if 문제_발견:
    # Option 1: 2호 직접 수정 (간단한 경우)
    if 문제 == "간단":
        2호_직접_수정()

    # Option 2: 에이전트 재호출 (복잡한 경우)
    else:
        Task("implementer-dna",
             "수정 작업",
             context="이전 작업 + 발견된 문제")
```

**핵심 원칙**:
- ✅ 에이전트 보고서는 "자기 말"일 뿐
- ✅ 2호는 반드시 "실제 결과" 확인
- ✅ 테스트와 품질 검증은 직접 실행
- ✅ 이것이 2호의 "Quality Guardian" 역할!

**Note**:
- 실제 검증 프로세스는 slash command에서 자동화
- 2호는 결과만 확인하고 패스/재작업 결정

---

## 참고

- **기반 문서**: [CORE_METHODOLOGY.md](./CORE_METHODOLOGY.md)
- **다음 단계**: [CHECKLIST_GUIDE.md](./CHECKLIST_GUIDE.md) - Task → 9-Step 체크리스트 변환
- **실행 가이드**: Stage 5 (작업분해) → Stage 6 (체크리스트) → Stage 7 (구현)
