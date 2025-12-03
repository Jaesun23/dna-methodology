# Stage 6: 프로젝트 표준 가이드 (Project Standards Guide)

> **목적**: DNA 시스템 사용 강제 규칙 + 자동화 설정으로 일관성 보장
>
> **버전**: v4.1 (2025-12-03)
>
> - v6.0 (2025-12-03): Gemini 연구 기반 전면 재작성, DNA_METHODOLOGY_DETAILED.md 기준
> - v2.0 (2025-11-12): 입력/출력 문서 추가
> - v1.0 (2025-11-10): 초기 버전

---

## 📚 이 가이드의 위치

```
DNA 방법론 문서 체계:

Tier 1: DNA_PROJECT_OVERVIEW_v2.md (전체 맥락)
           ↓
Tier 2: DNA_METHODOLOGY_DETAILED.md (상세 원리) - Part 5.4
           ↓
Tier 3: 이 문서 (Stage 6 실행 가이드) ← 지금 여기!
```

**참조 문서**:
- **원리 이해**: `DNA_METHODOLOGY_DETAILED.md` Part 5.4

---

## 🤔 왜 Project Standards가 필요한가?

### Bridge의 마지막 조각

```
Bridge(Stage 4-6)의 4대 구성요소:

┌─────────────────────────────────────────────────────┐
│  Stage 3: ADR (결정)                                │
│  "PostgreSQL을 쓰기로 했다"                          │
└─────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────┐
│  Stage 4: DNA 청사진 (설계)                          │
│  "src/core/database/ 구조와 API 설계"                │
└─────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────┐
│  Stage 5: DNA 구현 (코드)                            │
│  "get_session(), Base 클래스 구현"                   │
└─────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────┐
│  Stage 6: Project Standards (강제) ← 지금 여기!     │
│  "직접 SQL 금지, get_session() 필수 사용"            │
│  "위반 시 pre-commit에서 자동 차단"                  │
└─────────────────────────────────────────────────────┘
```

### 규칙만 있고 강제가 없으면?

```
❌ 강제 없는 규칙:

PROJECT_STANDARDS.md:
"print() 대신 logger를 사용하세요"

현실:
domain/orders/service.py:
    print(f"Creating order: {data}")  # 급하니까 일단...
    print("DEBUG: ", response)        # 디버깅용...

결과:
├─ 규칙 문서는 존재하지만 아무도 안 읽음
├─ 코드 리뷰에서 발견? "이번만 넘어가죠"
├─ 운영에서 print 로그가 stdout에 뒤섞임
└─ 3개월 후 "누가 print 쓴 거야?!" 😱
```

```
✅ 강제 있는 규칙:

PROJECT_STANDARDS.md:
"print() 대신 logger를 사용하세요"

자동화:
pyproject.toml:
    select = ["T201"]  # T201 = print 금지

.pre-commit-config.yaml:
    - id: ruff
      args: [--fix]

결과:
$ git commit -m "Add order feature"
Ruff.....Failed
- T201: print found (domain/orders/service.py:15)

├─ 커밋 자체가 차단됨
├─ 개발자가 즉시 수정
├─ 코드 리뷰 불필요 (자동 강제)
└─ 운영 환경 100% 안전
```

### 비유: 교통 법규 vs 과속 카메라

```
교통 법규 (규칙):
"제한 속도 60km/h를 지키세요"

과속 카메라 (강제):
위반 시 자동 촬영 → 벌금 → 면허 정지

Project Standards:
├─ 규칙 = PROJECT_STANDARDS.md (교통 법규)
├─ 강제 = pre-commit hooks (과속 카메라)
├─ 처벌 = 커밋 차단 (벌금)
└─ 결과 = 100% 준수 (안전한 도로)
```

---

## 📥 입력 문서

### Stage 5에서 전달받는 것

| 파일 | 핵심 내용 | 이 Stage에서 사용 |
|------|----------|-----------------|
| `src/core/` | 구현된 DNA 모듈 | 사용 규칙 작성 |
| `05D-01_dna_implementation.md` | 구현 완료 문서 | 금지/필수 규칙 도출 |
| `03A-401~499_*.md` | DNA 시스템 ADR | 기술 선택 근거 |

---

## 📤 출력 문서

### 필수 산출물

```
docs/
├── 06D-01_project_standards.md    # THE 산출물 (규칙 문서)
└── 06D-02_automation_config.md    # 자동화 설정 문서

프로젝트 루트/
├── pyproject.toml                 # Ruff, MyPy, pytest 설정
├── .pre-commit-config.yaml        # pre-commit hooks
└── .importlinter                  # 아키텍처 의존성 규칙
```

---

## 🔧 Project Standards 3대 영역

### 영역 1: DNA 사용 규칙 (DO/DON'T)

```
각 DNA 시스템마다:

DO (필수):
├─ 어떤 API를 사용해야 하는지
├─ 어떤 패턴을 따라야 하는지
└─ 코드 예시

DON'T (금지):
├─ 어떤 것을 사용하면 안 되는지
├─ 왜 금지인지
└─ Ruff/MyPy 규칙 코드
```

### 영역 2: 품질 기준 (Zero Tolerance)

```
절대 타협 없는 기준:

Ruff:     0 violations
MyPy:     0 errors
pytest:   0 failures
Coverage: 95%+

위반 시:
├─ 커밋 차단 (pre-commit)
├─ PR 머지 차단 (CI)
└─ 배포 차단 (CD)
```

### 영역 3: 자동화 설정 (강제 메커니즘)

```
3단계 강제:

Day 1: 로컬 (pre-commit)
├─ Ruff (린팅 + 포맷팅)
├─ MyPy (타입 체크)
└─ 기본 테스트

Week 2: 아키텍처 (import-linter)
├─ core → domain 금지
├─ domain → api 금지
└─ 의존성 방향 강제

Month 1+: CI/CD
├─ GitHub Actions
├─ 커버리지 게이트
└─ 배포 파이프라인
```

---

## 📋 작성 단계 (Part 1-4)

### Part 1: DNA 사용 규칙 작성 (1시간)

#### Step 1: Logging 규칙

```markdown
## Logging (DNA 1)

### DO ✅

```python
# 올바른 사용
from core.logging import get_logger

logger = get_logger(__name__)

# 기본 로깅
logger.info("주문 생성", order_id=order_id, user_id=user_id)

# 에러 로깅
logger.error("주문 실패", error=str(e), order_id=order_id)

# 컨텍스트 바인딩
from core.logging import bind_context
bind_context(trace_id=trace_id, user_id=user_id)
```

### DON'T ❌

```python
# 금지 1: print() 사용
print(f"Creating order: {data}")  # ❌ T201 위반!

# 금지 2: logging 직접 사용
import logging
logger = logging.getLogger(__name__)  # ❌ 구조화 로깅 불가

# 금지 3: f-string 메시지
logger.info(f"Order {order_id} created")  # ❌ 구조화 파괴
# 올바른: logger.info("Order created", order_id=order_id)
```

### Ruff 규칙
- `T201`: print 금지
- `G004`: f-string in logging 금지
```

#### Step 2: Config 규칙

```markdown
## Configuration (DNA 2)

### DO ✅

```python
# 올바른 사용
from core.config import get_settings

settings = get_settings()

# 설정값 접근
db_url = settings.database_url
redis_url = settings.redis_url

# 환경 확인
if settings.is_production:
    # 운영 전용 로직
```

### DON'T ❌

```python
# 금지 1: os.environ 직접 접근
import os
db_url = os.environ.get("DATABASE_URL")  # ❌ 타입 안전성 없음

# 금지 2: 하드코딩
db_url = "postgresql://localhost/dev"  # ❌ 환경별 분리 불가

# 금지 3: 설정 파일 직접 읽기
import json
config = json.load(open("config.json"))  # ❌ 검증 없음
```

### Ruff 규칙
- 커스텀 규칙으로 `os.environ` 사용 감지 (import-linter)
```

#### Step 3: Types 규칙

```markdown
## Types (DNA 3)

### DO ✅

```python
# 올바른 사용
from core.types import UserId, OrderId, Money

def create_order(
    user_id: UserId,
    amount: Money,
) -> OrderId:
    ...

# 값 객체 사용
price = Money(amount=Decimal("50000"), currency="KRW")
```

### DON'T ❌

```python
# 금지 1: Any 타입
def process(data: Any) -> Any:  # ❌ 타입 안전성 없음
    ...

# 금지 2: Dict[str, Any]
def create_order(data: Dict[str, Any]):  # ❌ TypedDict 사용
    ...

# 금지 3: 타입 힌트 누락
def create_order(user_id, amount):  # ❌ MyPy strict 위반
    ...
```

### MyPy 규칙
- `strict = true`: 모든 함수에 타입 힌트 필수
- `warn_return_any = true`: Any 반환 경고
- `disallow_any_explicit = true`: 명시적 Any 금지
```

#### Step 4: Errors 규칙

```markdown
## Error Handling (DNA 4)

### DO ✅

```python
# 올바른 사용
from core.errors import ValidationError, NotFoundError, KISAPIError

# 도메인 에러
if not items:
    raise ValidationError("주문 항목이 비어있습니다", field="items")

# 리소스 없음
if not order:
    raise NotFoundError("Order", order_id)

# 외부 API 에러
if response.status_code != 200:
    raise KISAPIError("KIS API 호출 실패", status_code=response.status_code)
```

### DON'T ❌

```python
# 금지 1: 일반 Exception
raise Exception("Something went wrong")  # ❌ 에러 코드 없음

# 금지 2: except: pass
try:
    ...
except:  # ❌ 모든 에러 삼킴
    pass

# 금지 3: bare except
try:
    ...
except Exception:  # ❌ 너무 광범위
    logger.error("Error")

# 올바른: 구체적 예외 처리
try:
    ...
except ValidationError as e:
    logger.warning("검증 실패", error=e.message)
    raise
except KISAPIError as e:
    logger.error("외부 API 실패", error=e.message)
    raise
```

### Ruff 규칙
- `E722`: bare except 금지
- `B001`: assert 대신 raise 사용
```

#### Step 5: Database 규칙

```markdown
## Database (DNA 5)

### DO ✅

```python
# 올바른 사용
from core.database import get_session

# 세션 사용 (컨텍스트 매니저)
async with get_session() as session:
    order = Order(user_id=user_id, amount=amount)
    session.add(order)
    await session.commit()

# 쿼리
async with get_session() as session:
    result = await session.execute(
        select(Order).where(Order.user_id == user_id)
    )
    orders = result.scalars().all()
```

### DON'T ❌

```python
# 금지 1: 직접 SQL 문자열
cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")  # ❌ SQL Injection!

# 금지 2: 세션 수동 관리
session = Session()
try:
    ...
finally:
    session.close()  # ❌ 컨텍스트 매니저 사용

# 금지 3: 트랜잭션 없이 여러 쓰기
session.add(order)
session.commit()
session.add(payment)
session.commit()  # ❌ 원자성 위반
```

### 보안 규칙
- `S608`: SQL Injection 가능 코드 감지
```



### Part 2: 품질 기준 설정 (30분)

#### Zero Tolerance 기준

```markdown
## 품질 기준 (Zero Tolerance)

### 정적 분석

| 도구 | 기준 | 위반 시 |
|------|-----|--------|
| Ruff | 0 violations | 커밋 차단 |
| MyPy | 0 errors | 커밋 차단 |
| pytest | 0 failures | 머지 차단 |
| Coverage | 95%+ | 머지 차단 |

### Ruff 규칙 (필수)

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort
    "T201",   # print 금지
    "G004",   # f-string in logging 금지
    "B",      # bugbear
    "S",      # security
    "E722",   # bare except 금지
]

ignore = [
    "E501",   # line too long (formatter가 처리)
]
```

### MyPy 규칙 (필수)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_any_explicit = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### pytest 규칙 (필수)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = """
    --cov=src
    --cov-fail-under=95
    --cov-report=term-missing
    -q
"""
testpaths = ["tests"]
```
```

### Part 3: 자동화 설정 (1시간)

#### Step 1: pre-commit 설정

```yaml
# .pre-commit-config.yaml

repos:
  # Ruff (린팅 + 포맷팅)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # MyPy (타입 체크)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: 
          - pydantic>=2.0
          - pydantic-settings>=2.0
        args: [--strict]

  # pytest (로컬 테스트)
  - repo: local
    hooks:
      - id: pytest-unit
        name: pytest unit tests
        entry: pytest tests/unit -q --no-cov
        language: system
        pass_filenames: false
        always_run: true

  # import-linter (아키텍처 검증)
  - repo: local
    hooks:
      - id: import-linter
        name: import-linter
        entry: lint-imports
        language: system
        pass_filenames: false
        always_run: true
```

#### Step 2: import-linter 설정

```ini
# .importlinter

[importlinter]
root_package = src

[importlinter:contract:core-independence]
name = Core는 Domain/API에 의존하지 않음
type = forbidden
source_modules = 
    src.core
forbidden_modules = 
    src.domain
    src.api

[importlinter:contract:domain-independence]
name = Domain은 API에 의존하지 않음
type = forbidden
source_modules = 
    src.domain
forbidden_modules = 
    src.api

[importlinter:contract:layers]
name = Clean Architecture 레이어
type = layers
layers = 
    src.api
    src.domain
    src.core
```

**의존성 방향**:
```
허용:
api → domain → core

금지:
core → domain (역방향!)
domain → api (역방향!)
core → api (건너뛰기!)
```

#### Step 3: CI 파이프라인 (GitHub Actions)

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync
      
      - name: Ruff (lint)
        run: uv run ruff check src tests
      
      - name: Ruff (format)
        run: uv run ruff format --check src tests
      
      - name: MyPy
        run: uv run mypy src --strict
      
      - name: import-linter
        run: uv run lint-imports
      
      - name: pytest
        run: uv run pytest --cov=src --cov-fail-under=95
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          fail_ci_if_error: true
```

### Part 4: 자동화 성숙도 로드맵 (30분)

#### Day 1: 기본 정적 분석

```bash
# pre-commit 설치
uv add --dev pre-commit
pre-commit install

# 첫 검증
pre-commit run --all-files
```

**이 시점의 강제**:
- ✅ Ruff (린팅 + 포맷팅)
- ✅ MyPy (타입 체크)
- ✅ 기본 테스트

#### Week 2: 아키텍처 검증

```bash
# import-linter 설치
uv add --dev import-linter

# 검증
lint-imports
```

**이 시점의 강제**:
- ✅ Day 1 모든 것
- ✅ 레이어 의존성 (core ← domain ← api)
- ✅ 역방향 의존성 차단

#### Month 1+: CI/CD 통합

```bash
# GitHub Actions 설정
mkdir -p .github/workflows
cp templates/ci.yml .github/workflows/
```

**이 시점의 강제**:
- ✅ Week 2 모든 것
- ✅ PR 머지 게이트
- ✅ 커버리지 리포트
- ✅ 배포 파이프라인

---

## 📄 PROJECT_STANDARDS.md 템플릿

### 06D-01_project_standards.md

```markdown
# Project Standards

> **프로젝트**: [프로젝트명]
> **버전**: v1.0
> **작성일**: YYYY-MM-DD
> **기반 ADR**: 03A-401 ~ 03A-411 (DNA 시스템)

---

## 1. 코드 스타일

### 1.1 포맷팅
- **도구**: Ruff formatter
- **줄 길이**: 88자
- **들여쓰기**: 4 spaces
- **인용부호**: 큰따옴표 (")

### 1.2 네이밍
| 대상 | 규칙 | 예시 |
|------|-----|------|
| 클래스 | PascalCase | `OrderService` |
| 함수/변수 | snake_case | `create_order` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 비공개 | _prefix | `_internal_method` |

### 1.3 Import 순서
```python
# 1. 표준 라이브러리
import os
from datetime import datetime

# 2. 서드파티
from fastapi import FastAPI
from pydantic import BaseModel

# 3. 로컬 (core → domain → api 순)
from core.logging import get_logger
from domain.orders import OrderService
```

---

## 2. DNA 시스템 사용 규칙

### 2.1 Logging

**DO ✅**
```python
from core.logging import get_logger
logger = get_logger(__name__)
logger.info("주문 생성", order_id=order_id)
```

**DON'T ❌**
```python
print("debug")                    # T201 위반
import logging                    # 직접 사용 금지
logger.info(f"Order {id}")        # G004 위반
```

### 2.2 Configuration

**DO ✅**
```python
from core.config import get_settings
settings = get_settings()
db_url = settings.database_url
```

**DON'T ❌**
```python
import os
os.environ.get("DB_URL")          # 타입 안전성 없음
db_url = "postgresql://..."       # 하드코딩 금지
```

### 2.3 Types

**DO ✅**
```python
from core.types import UserId, OrderId, Money

def create_order(user_id: UserId, amount: Money) -> OrderId:
    ...
```

**DON'T ❌**
```python
def create_order(user_id, amount):  # 타입 힌트 누락
    ...

def process(data: Any) -> Any:      # Any 금지
    ...
```

### 2.4 Error Handling

**DO ✅**
```python
from core.errors import ValidationError, NotFoundError

if not items:
    raise ValidationError("항목 필요", field="items")
```

**DON'T ❌**
```python
raise Exception("error")           # 일반 Exception 금지
except:                            # bare except 금지
    pass
```

### 2.5 Database

**DO ✅**
```python
from core.database import get_session

async with get_session() as session:
    session.add(order)
    await session.commit()
```

**DON'T ❌**
```python
cursor.execute(f"SELECT * WHERE id = {id}")  # SQL Injection!
session = Session()                           # 수동 관리 금지
```

---

## 3. 품질 기준

### 3.1 Zero Tolerance

| 항목 | 기준 | 검증 명령어 |
|------|-----|-----------|
| Ruff | 0 violations | `ruff check src tests` |
| MyPy | 0 errors | `mypy src --strict` |
| pytest | 0 failures | `pytest tests` |
| Coverage | 95%+ | `pytest --cov-fail-under=95` |

### 3.2 커밋 전 필수

```bash
# 모든 검증 통과 필수
pre-commit run --all-files
```

위반 시 커밋 차단됨.

---

## 4. 아키텍처 규칙

### 4.1 레이어 구조

```
src/
├── core/      # DNA 시스템 (공통 인프라)
├── domain/    # 비즈니스 로직
└── api/       # HTTP 인터페이스
```

### 4.2 의존성 방향

```
허용: api → domain → core
금지: core → domain, domain → api
```

### 4.3 import-linter로 강제

```bash
# 검증
lint-imports

# 위반 시
FAILED: Core는 Domain/API에 의존하지 않음
  src.core.database imports src.domain.orders
```

---

## 5. Git 규칙

### 5.1 커밋 메시지

```
<type>(<scope>): <subject>

feat(orders): 주문 생성 API 추가
fix(auth): 토큰 만료 처리 수정
refactor(core): 로깅 설정 개선
test(orders): 주문 서비스 테스트 추가
docs(readme): 설치 가이드 업데이트
```

### 5.2 브랜치 전략

```
main         ← 운영 (보호됨)
develop      ← 개발 통합
feature/*    ← 기능 개발
fix/*        ← 버그 수정
```

### 5.3 PR 규칙

- [ ] 모든 CI 통과
- [ ] 리뷰어 1명 이상 승인
- [ ] 커버리지 유지 또는 증가

---

## 6. 참조

- ADR: `docs/adr/03A-401~411_*.md`
- DNA 구현: `src/core/`
- 자동화 설정: `pyproject.toml`, `.pre-commit-config.yaml`
```



---

## ✏️ 작성 예시: 주식 거래 플랫폼

### 예시 1: DNA 사용 규칙 (Logging 상세)

```markdown
## 2.1 Logging

> **ADR 참조**: ADR-401 (structlog 선택)

### 목적
모든 로그는 JSON 구조화 형식으로, trace_id를 포함하여 추적 가능해야 함.

### DO ✅ (필수 사용법)

```python
# 1. 로거 초기화
from core.logging import get_logger, bind_context

logger = get_logger(__name__)

# 2. 요청 시작 시 컨텍스트 바인딩
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    bind_context(
        trace_id=request.headers.get("X-Trace-ID", str(uuid4())[:8]),
        user_id=getattr(request.state, "user_id", "anonymous"),
    )
    return await call_next(request)

# 3. 비즈니스 로직에서 로깅
async def create_order(self, data: CreateOrderRequest) -> OrderId:
    logger.info("주문 생성 시작", symbol=data.symbol, quantity=data.quantity)
    
    try:
        order = await self._process_order(data)
        logger.info("주문 생성 완료", order_id=str(order.id))
        return order.id
    except KISAPIError as e:
        logger.error("KIS API 실패", error=str(e), symbol=data.symbol)
        raise
```

### DON'T ❌ (금지 사항)

```python
# 금지 1: print() 사용
# Ruff T201 위반 → 커밋 차단
print(f"Order created: {order_id}")

# 금지 2: logging 직접 사용
# 구조화 로깅 불가, trace_id 누락
import logging
logging.info("Order created")

# 금지 3: f-string 메시지
# Ruff G004 위반 → 검색/필터링 어려움
logger.info(f"Order {order_id} created by {user_id}")
# 올바른: logger.info("Order created", order_id=order_id, user_id=user_id)

# 금지 4: 예외 정보 누락
try:
    ...
except Exception:
    logger.error("실패")  # ❌ 예외 정보 없음
# 올바른: logger.exception("실패", exc_info=True)
```

### 검증 방법

```bash
# Ruff로 print 검사
ruff check src --select=T201,G004

# 결과 (위반 시)
src/domain/orders/service.py:45:5: T201 `print` found
src/domain/orders/service.py:52:9: G004 Logging statement uses f-string
```

### 로그 출력 예시

```json
{
  "event": "주문 생성 완료",
  "trace_id": "abc12345",
  "user_id": "user-789",
  "order_id": "order-456",
  "timestamp": "2025-12-03T10:30:00Z",
  "level": "info",
  "logger": "domain.orders.service"
}
```
```

### 예시 2: 자동화 설정 (전체)

```markdown
## 자동화 설정

### pyproject.toml (완전판)

```toml
[project]
name = "stock-trading-platform"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.11.0",
    "pydantic-settings>=2.6.0",
    "structlog>=24.1.0",
    "sqlalchemy>=2.0.0",
    "redis>=5.0.0",
    "httpx>=0.27.0",
    "uvloop>=0.21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",
    "import-linter>=2.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort
    "T201",   # print 금지
    "G004",   # f-string in logging 금지
    "B",      # bugbear
    "S",      # security (SQL injection 등)
    "E722",   # bare except 금지
    "UP",     # pyupgrade
]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = "--cov=src --cov-fail-under=95 --cov-report=term-missing -q"
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### .pre-commit-config.yaml (완전판)

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0
          - pydantic-settings>=2.0
          - sqlalchemy>=2.0
        args: [--strict]
        pass_filenames: false
        entry: mypy src

  - repo: local
    hooks:
      - id: pytest-unit
        name: pytest unit tests
        entry: pytest tests/unit -q --no-cov
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]

      - id: import-linter
        name: import-linter
        entry: lint-imports
        language: system
        pass_filenames: false
        always_run: true
```

### .importlinter (완전판)

```ini
[importlinter]
root_package = src

[importlinter:contract:core-independence]
name = Core는 Domain/API에 의존하지 않음
type = forbidden
source_modules =
    src.core
forbidden_modules =
    src.domain
    src.api

[importlinter:contract:domain-independence]
name = Domain은 API에 의존하지 않음
type = forbidden
source_modules =
    src.domain
forbidden_modules =
    src.api

[importlinter:contract:clean-layers]
name = Clean Architecture 레이어 순서
type = layers
layers =
    src.api
    src.domain
    src.core
```
```

### 예시 3: CI 파이프라인 (GitHub Actions)

```yaml
# .github/workflows/ci.yml

name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: '3.12'

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: Ruff lint
        run: uv run ruff check src tests
      
      - name: Ruff format
        run: uv run ruff format --check src tests

  type-check:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: MyPy
        run: uv run mypy src --strict

  architecture:
    name: Architecture Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: import-linter
        run: uv run lint-imports

  test:
    name: Test & Coverage
    runs-on: ubuntu-latest
    needs: [lint, type-check, architecture]
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: Run tests
        run: uv run pytest --cov=src --cov-fail-under=95 --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: true
```

---

## ✅ Stage 6 완료 체크리스트

### DNA 사용 규칙

- [ ] Logging DO/DON'T 작성
- [ ] Config DO/DON'T 작성
- [ ] Types DO/DON'T 작성
- [ ] Errors DO/DON'T 작성
- [ ] Database DO/DON'T 작성 (패밀리별)

### 품질 기준

- [ ] Zero Tolerance 기준 명시 (Ruff 0, MyPy 0, Coverage 95%)
- [ ] pyproject.toml [tool.ruff] 설정
- [ ] pyproject.toml [tool.mypy] 설정
- [ ] pyproject.toml [tool.pytest] 설정

### 자동화 설정

- [ ] .pre-commit-config.yaml 작성
- [ ] pre-commit install 실행
- [ ] .importlinter 설정
- [ ] lint-imports 검증

### CI/CD (선택)

- [ ] GitHub Actions workflow 작성
- [ ] PR 머지 게이트 설정
- [ ] 커버리지 리포트 설정

### 산출물 생성

- [ ] `06D-01_project_standards.md` 작성
- [ ] `06D-02_automation_config.md` 작성 (선택)
- [ ] 모든 설정 파일 프로젝트 루트에 배치

### 검증

- [ ] `pre-commit run --all-files` 통과
- [ ] `lint-imports` 통과
- [ ] 기존 코드 모두 규칙 준수 확인

---

## 🔗 Stage 6 → Stage 7 연결

### Stage 7에 전달하는 것

| 전달 항목 | 내용 | 용도 |
|----------|------|------|
| PROJECT_STANDARDS.md | DNA 사용 규칙 | 도메인 코드 작성 기준 |
| 자동화 설정 | pre-commit, CI | 품질 강제 |
| 아키텍처 규칙 | import-linter | 의존성 방향 강제 |

### Bridge 완료!

```
Bridge(Stage 4-6) 완료:

Stage 4: DNA 청사진 ✅
  └─ 무엇을 만들지 설계

Stage 5: DNA 구현 ✅
  └─ 실제 코드 작성

Stage 6: Project Standards ✅ ← 지금 여기!
  └─ 강제 규칙 + 자동화

결과:
├─ src/core/ DNA 모듈 완성
├─ PROJECT_STANDARDS.md 규칙 문서
├─ pre-commit, import-linter 자동화
└─ CI 파이프라인 (선택)

이제 도메인 코드를 안전하게 작성할 수 있는 "환경" 완성!
```

### Stage 7 미리보기

```
Stage 7: Project Blueprint
├─ 도메인 모델 설계 (Entity, Value Object, Aggregate)
├─ API 설계 (엔드포인트, 요청/응답)
├─ 데이터베이스 스키마
└─ DNA 환경 위에서 도메인 상세 설계
```

---

## ⏪ 이전 Stage 검증 및 수정 프로토콜

### 검증 시점
- Stage 6 시작 전 필수 체크 (Bridge 완성 직전!)
- 자동화 설정 전 DNA 구현과 교차 검증

### 검증 대상

| Stage | 산출물 | 검증 항목 |
|-------|--------|----------|
| Stage 1 | 01C-01_*.md | 표준이 NFR 우선순위 반영? |
| Stage 2 | 02C-01_*.md | 표준이 기술 제약 반영? |
| Stage 3 | 03A-*_*.md | 표준이 ADR 결정 반영? |
| Stage 4 | 04B-01_*.md | 표준이 DNA 청사진 반영? |
| Stage 5 | 05D-01_*.md | 구현된 DNA와 표준 일치? |

### 오류 발견 시 프로토콜 (Bridge 완성 전 마지막 검증!)

```
Stage 6에서 Stage 1-5 오류 발견 시:

Step 1: 오류 발견 및 문서화
├─ 발견 위치: 표준 [섹션] 작성 중
├─ 오류 내용: [구체적 설명]
├─ 영향 Stage: Stage [1-5]
└─ 기록: 06D-01에 "발견된 이슈" 추가

⚠️ Stage 6은 Bridge 완성 직전!
├─ 여기서 오류 수정 = 비용 최소
├─ Stage 7 이후 발견 = 비용 급증
└─ 철저한 검증 필수!

Step 2: 영향 범위 파악
├─ DNA 구현(Stage 5) 수정 필요?
├─ 청사진(Stage 4) 수정 필요?
├─ ADR(Stage 3) 수정 필요?
└─ 재작업 예상: [X]시간

Step 3: 해당 Stage로 이동 → 수정

Step 4: 중간 Stage 전파 (Stage 4-5)

Step 5: Stage 6 재진행
├─ 수정된 DNA로 표준 재검토
└─ 자동화 설정 재검증

Step 6: Bridge 완성 검증 → Stage 7 전달 ✅
```

### 흔한 오류 패턴

| 오류 유형 | 예시 | 해결 |
|----------|------|------|
| DNA-표준 불일치 | 로깅 함수명 불일치 | Stage 5 구현 또는 표준 수정 |
| ADR 미반영 | 코드 스타일 ADR과 표준 불일치 | 표준 수정 |
| 자동화 불가 | 규칙은 있으나 검증 방법 없음 | 규칙 재정의 또는 커스텀 린터 |

### 추적성

```
수정 이력: docs/revision_log.md
표준 참조: PROJECT_STANDARDS.md에 ADR 링크 포함
```

---

## 💡 핵심 원칙 요약

### Project Standards의 3대 영역

```
1. DNA 사용 규칙 (DO/DON'T)
────────────────────────────────
각 DNA 시스템마다:
├─ DO: 필수 사용법 + 코드 예시
├─ DON'T: 금지 사항 + 이유
└─ Ruff/MyPy 규칙 코드

2. 품질 기준 (Zero Tolerance)
────────────────────────────────
절대 타협 없는 기준:
├─ Ruff: 0 violations
├─ MyPy: 0 errors
├─ pytest: 0 failures
└─ Coverage: 95%+

3. 자동화 설정 (강제 메커니즘)
────────────────────────────────
3단계 강제:
├─ Day 1: pre-commit (로컬)
├─ Week 2: import-linter (아키텍처)
└─ Month 1+: CI/CD (파이프라인)
```

### 규칙 vs 강제

```
규칙만 있으면:
├─ 문서는 존재하지만 아무도 안 읽음
├─ 코드 리뷰에서 "이번만 넘어가죠"
└─ 3개월 후 "누가 이렇게 한 거야?!" 😱

규칙 + 강제:
├─ 커밋 자체가 차단됨
├─ 개발자가 즉시 수정
├─ 코드 리뷰 불필요 (자동 강제)
└─ 운영 환경 100% 안전 ✅
```

### 자동화 성숙도 로드맵

```
Day 1: pre-commit
├─ Ruff (린팅 + 포맷팅)
├─ MyPy (타입 체크)
└─ 기본 테스트

Week 2: import-linter
├─ 레이어 의존성 강제
└─ 역방향 의존성 차단

Month 1+: CI/CD
├─ PR 머지 게이트
├─ 커버리지 리포트
└─ 배포 파이프라인
```

---

**Remember**: 
- 규칙 없는 자동화 = 무엇을 강제할지 모름
- 자동화 없는 규칙 = 아무도 안 지킴
- 둘 다 있어야 = 100% 품질 보장
- Bridge 완료 = 도메인 코드 작성 환경 완성!

*Stage 6으로 Bridge(Stage 4-6)가 완료됩니다. 이제 Stage 7부터 도메인 코드를 안전하게 작성할 수 있습니다.*
