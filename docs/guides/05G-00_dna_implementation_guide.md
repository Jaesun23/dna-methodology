# Stage 5: DNA 시스템 구현 가이드 (DNA Implementation Guide)

> **목적**: Stage 4 청사진 기반으로 src/core/ DNA 시스템 실제 구현
>
> **버전**: v4.1 (2025-12-03)
>
> - v5.0 (2025-12-03): Gemini 연구 기반 전면 재작성, DNA_METHODOLOGY_DETAILED.md 기준
> - v1.0 (2025-11-13): 초기 버전

---

## 📚 이 가이드의 위치

```
DNA 방법론 문서 체계:

Tier 1: DNA_PROJECT_OVERVIEW_v2.md (전체 맥락)
           ↓
Tier 2: DNA_METHODOLOGY_DETAILED.md (상세 원리) - Part 5
           ↓
Tier 3: 이 문서 (Stage 5 실행 가이드) ← 지금 여기!
```

**참조 문서**:
- **원리 이해**: `DNA_METHODOLOGY_DETAILED.md` Part 5
- **DNA 상세**: `DNA_Systems_11_Complete_Guide.md`

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
│   ├─ src/core/XXX/*.py (구현)
│   └─ tests/core/XXX/*.py (테스트)
└─ 응답 생성 여유: ~80-90K 토큰
```

#### 세션당 작업량 기준

| DNA 시스템 | 파일 수 | 테스트 파일 | 총 토큰 | 세션 수 |
|-----------|--------|-----------|---------|---------|
| Types | 3-4개 | 3-4개 | ~15K | 1 session |
| Config | 2-3개 | 2-3개 | ~12K | 1 session |
| Error | 3-4개 | 3-4개 | ~15K | 1 session |
| Logging | 5-6개 | 5-6개 | ~20K | 1 session |
| Cache | 4-5개 | 4-5개 | ~18K | 1 session |
| Testing | 4-5개 | 4-5개 | ~18K | 1 session |
| Security | 6-7개 | 6-7개 | ~22K | 1 session |
| Monitoring | 5-6개 | 5-6개 | ~20K | 1 session |
| Messaging | 6-7개 | 6-7개 | ~22K | 1 session |
| API Gateway | 6-7개 | 6-7개 | ~22K | 1 session |
| Database | 8-10개 | 8-10개 | ~28K | **2 sessions** |

**핵심**: 대부분 시스템은 1 세션, Database만 2 세션

#### Database 시스템 분해 전략 (유일한 예외)

```
Database는 유일하게 2 세션 필요:

Session 1: Database 기초 (Connection + Session)
├─ connection.py: Connection Pool
├─ session.py: Session Manager
├─ protocols.py: ConnectionProvider, SessionProvider
└─ 테스트 (각 모듈 격리)
  → ~25K 토큰

Session 2: Database 고급 (Query + Migration)
├─ query.py: Query Builder
├─ migration.py: Schema Migration
├─ integration.py: 모듈 통합
└─ 테스트 (통합 테스트 포함)
  → ~25K 토큰
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
   - 타입 힌트 완전 (mypy 0 오류)
   - Docstring (Google style)

□ 2. 내부 헬퍼 구현
   - Private 함수/클래스
   - 유틸리티 모듈
   - 상수/설정

□ 3. 에러 처리
   - try-except 적절히 배치
   - 커스텀 예외 정의
   - 에러 로깅 (print() 절대 금지!)

□ 4. 로깅 통합
   - from core.logging import get_logger
   - logger = get_logger(__name__)
   - 모든 중요 시점에 로그

□ 5. 테스트 작성 (TDD)
   - 단위 테스트: 각 함수/클래스
   - 통합 테스트: 모듈 간 상호작용
   - 커버리지: 95%+
   - pytest + pytest-cov

□ 6. 품질 검증 (Zero-Tolerance)
   - ruff check: 0 오류
   - mypy: 0 오류
   - import-linter: 0 위반
   - pytest: 100% pass

□ 7. 문서화
   - __init__.py: 공개 API 노출
   - README.md: 사용 예시
   - 주석: 복잡한 로직 설명
```

#### 3단계 검증 프로토콜

```python
def validate_dna_implementation(system_name: str) -> ValidationResult:
    """DNA 시스템 구현 완전성 검증."""

    # 검증 1: 청사진 대비 완성도
    blueprint = read_blueprint(f"04D-0X_dna_{system_name}_blueprint.md")
    impl_files = glob(f"src/core/{system_name}/*.py")

    for api in blueprint.public_apis:
        if not api_implemented(api, impl_files):
            return ValidationResult(
                passed=False,
                message=f"{system_name}: 공개 API {api} 미구현",
                action="해당 API 구현"
            )

    # 검증 2: 품질 게이트 (Zero-Tolerance)
    quality_results = run_quality_checks(system_name)
    if quality_results.ruff_errors > 0:
        return ValidationResult(
            passed=False,
            message=f"{system_name}: ruff 오류 {quality_results.ruff_errors}개",
            action="ruff 오류 수정"
        )

    if quality_results.mypy_errors > 0:
        return ValidationResult(
            passed=False,
            message=f"{system_name}: mypy 오류 {quality_results.mypy_errors}개",
            action="타입 힌트 수정"
        )

    # 검증 3: 테스트 커버리지
    coverage = run_pytest_coverage(f"tests/core/{system_name}/")
    if coverage < 0.95:
        return ValidationResult(
            passed=False,
            message=f"{system_name}: 커버리지 {coverage*100:.1f}% (목표: 95%+)",
            action="테스트 추가"
        )

    return ValidationResult(passed=True)
```

#### 불완전 → 재구현 사례

```markdown
## 사례: DNA Logging 시스템 구현

### ❌ 불완전한 버전 (1차 구현)

```python
# src/core/logging/logger.py
import logging

def get_logger(name):  # ❌ 타입 힌트 없음
    return logging.getLogger(name)

class Logger:
    def info(self, msg):  # ❌ 타입 힌트 없음
        print(f"INFO: {msg}")  # ❌ print() 사용!
```

**품질 검증 실패**:
```bash
$ mypy src/core/logging/
  logger.py:3: error: Missing return type
  logger.py:6: error: Missing type for 'msg'
  → mypy: 2 errors

$ ruff check src/core/logging/
  logger.py:8: T201 `print` found
  → ruff: 1 error

$ pytest tests/core/logging/ --cov
  → Coverage: 45% (목표: 95%)
```

❌ 문제점:
- 타입 힌트 누락 → mypy 오류
- print() 사용 → ruff 위반
- 테스트 부족 → 커버리지 45%
- 청사진의 context() 미구현

### ✅ 완전한 버전 (2차 재구현)

```python
# src/core/logging/logger.py
from typing import Any
import structlog
from core.types import LogLevel

def get_logger(name: str) -> "Logger":
    """로거 인스턴스 반환.

    Args:
        name: 로거 이름 (__name__ 권장)

    Returns:
        Logger: 구조화된 로거 인스턴스
    """
    return Logger(structlog.get_logger(name))

class Logger:
    """구조화된 로거 래퍼."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger

    def info(self, msg: str, **kwargs: Any) -> None:
        """INFO 레벨 로그 출력.

        Args:
            msg: 로그 메시지
            **kwargs: 추가 컨텍스트
        """
        self._logger.info(msg, **kwargs)  # ✅ structlog 사용

    def context(self, **kwargs: Any) -> "LogContext":
        """컨텍스트 관리자 반환."""
        return LogContext(self._logger, kwargs)
```

```python
# tests/core/logging/test_logger.py
import pytest
from core.logging import get_logger

def test_get_logger_returns_logger():
    """get_logger는 Logger 인스턴스를 반환한다."""
    logger = get_logger("test")
    assert isinstance(logger, Logger)

def test_logger_info_logs_message(caplog):
    """info()는 메시지를 로그에 기록한다."""
    logger = get_logger("test")
    logger.info("테스트 메시지", key="value")

    assert "테스트 메시지" in caplog.text
    assert "key" in caplog.text

def test_logger_context_adds_context():
    """context()는 컨텍스트를 추가한다."""
    logger = get_logger("test")

    with logger.context(request_id="123"):
        logger.info("요청 처리")
        # request_id가 자동으로 추가되어야 함
```

**품질 검증 성공**:
```bash
$ mypy src/core/logging/
  → Success: no issues found

$ ruff check src/core/logging/
  → All checks passed!

$ pytest tests/core/logging/ --cov
  → Coverage: 97% ✅
```

---

### DNA 핵심 원칙 3: 기능별 분해 + 연결부 + 조립

**"모듈이 크면 기능별로 나누고, 연결부 설계 후 조립"**

#### Stage 5에서의 적용 (가장 중요!)

Stage 5는 **실제 코드 구현** 단계이므로 원칙 3이 **직접 적용**됩니다!

```
DNA 시스템 크기별 전략:

작은 시스템 (< 5 파일):
├─ 한 세션에 전체 구현
└─ 분해 불필요
    예: Types, Config, Error

중간 시스템 (5-7 파일):
├─ 한 세션에 구현 가능
├─ 모듈 간 의존성 관리
└─ Protocol 정의
    예: Logging, Cache, Testing

큰 시스템 (8+ 파일):
├─ 기능별 분해 필수!
├─ Protocol 정의 (연결부)
├─ 각 기능 독립 구현
└─ 마지막에 조립
    예: Database (유일한 케이스!)
```

#### Database 시스템 분해 실전 (필수 학습!)

```markdown
## Task 000: Protocol 정의 (연결부)

```python
# src/core/database/protocols.py
from typing import Protocol, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

class ConnectionProvider(Protocol):
    """연결 제공 인터페이스."""

    async def get_connection(self) -> AsyncContextManager[AsyncConnection]:
        """비동기 연결 반환."""
        ...

class SessionProvider(Protocol):
    """세션 제공 인터페이스."""

    async def get_session(self) -> AsyncContextManager[AsyncSession]:
        """비동기 세션 반환."""
        ...
```

## Task 001: Connection Pool 구현

```python
# src/core/database/connection.py
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from core.logging import get_logger

logger = get_logger(__name__)

class ConnectionPool:
    """데이터베이스 연결 풀 관리.

    Protocol: ConnectionProvider 구현
    """

    def __init__(self, url: str) -> None:
        self._engine = create_async_engine(url)
        logger.info("연결 풀 생성", url=url)

    async def get_connection(self) -> AsyncContextManager[AsyncConnection]:
        """연결 반환."""
        return self._engine.connect()
```

```python
# tests/core/database/test_connection.py
import pytest
from core.database.connection import ConnectionPool

@pytest.mark.asyncio
async def test_connection_pool_provides_connection():
    """ConnectionPool은 연결을 제공한다."""
    pool = ConnectionPool("sqlite+aiosqlite:///:memory:")

    async with pool.get_connection() as conn:
        result = await conn.execute("SELECT 1")
        assert result is not None
```

## Task 002: Session Manager 구현

```python
# src/core/database/session.py
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.database.protocols import ConnectionProvider  # ← Protocol 의존!
from core.logging import get_logger

logger = get_logger(__name__)

class SessionManager:
    """세션 관리자.

    Protocol: SessionProvider 구현
    Dependency: ConnectionProvider (Protocol)
    """

    def __init__(self, connection_provider: ConnectionProvider) -> None:
        # ✅ 실제 ConnectionPool이 아니라 Protocol에 의존!
        self._connection_provider = connection_provider
        self._session_maker = async_sessionmaker()
        logger.info("세션 관리자 생성")

    async def get_session(self) -> AsyncContextManager[AsyncSession]:
        """세션 반환."""
        async with self._connection_provider.get_connection() as conn:
            yield self._session_maker(bind=conn)
```

```python
# tests/core/database/test_session.py
import pytest
from unittest.mock import AsyncMock, Mock
from core.database.session import SessionManager
from core.database.protocols import ConnectionProvider

@pytest.fixture
def mock_connection_provider():
    """Mock ConnectionProvider 반환."""
    provider = Mock(spec=ConnectionProvider)
    provider.get_connection = AsyncMock()
    return provider

@pytest.mark.asyncio
async def test_session_manager_provides_session(mock_connection_provider):
    """SessionManager는 세션을 제공한다."""
    manager = SessionManager(mock_connection_provider)

    async with manager.get_session() as session:
        assert session is not None
        # ConnectionProvider.get_connection() 호출 확인
        mock_connection_provider.get_connection.assert_called_once()
```

**핵심**: Mock을 사용하여 의존성 격리!

## Task 999: Database 통합 (조립)

```python
# src/core/database/__init__.py
from core.database.connection import ConnectionPool
from core.database.session import SessionManager
from core.database.protocols import ConnectionProvider, SessionProvider

# 실제 구현체 생성
_connection_pool: ConnectionProvider = ConnectionPool("postgresql://...")
_session_manager: SessionProvider = SessionManager(_connection_pool)

# 공개 API
def get_session():
    """세션 반환."""
    return _session_manager.get_session()
```

```python
# tests/core/database/test_integration.py
import pytest
from core.database import get_session

@pytest.mark.asyncio
async def test_database_integration_e2e():
    """Database 시스템 E2E 테스트."""
    async with get_session() as session:
        result = await session.execute("SELECT 1")
        assert result is not None
```
```

#### 작은/중간 시스템 구현 전략

```markdown
## 사례: DNA Types 시스템 (작은 시스템, 분해 불필요)

### 한 세션에 전체 구현

```python
# src/core/types/ids.py
from uuid import UUID
from typing import NewType

UserId = NewType("UserId", UUID)
OrderId = NewType("OrderId", UUID)
```

```python
# src/core/types/enums.py
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    ERROR = "error"
```

```python
# tests/core/types/test_ids.py
from uuid import uuid4
from core.types import UserId

def test_user_id_creation():
    """UserId는 UUID로 생성된다."""
    user_id = UserId(uuid4())
    assert isinstance(user_id, UUID)
```

**구현 완료**: 1 세션에 전체 완성 (분해 불필요)
```

---

### DNA 핵심 원칙 4: 역방향 수정 프로토콜

**"앞선 결정의 오류 발견 시 → 되돌아가서 수정 → 다시 현재까지 진행"**

#### Stage 5에서 역방향 수정이 발생하는 경우

```
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

```markdown
## 실제 사례: Logging 시스템 비동기 쓰기 추가

### Step 1: 오류 발견 및 문서화
**발견 시점**: Stage 5 (Logging 시스템 구현 중)
**파일**: `src/core/logging/handlers.py`
**문제**: 파일 핸들러가 동기 쓰기라 성능 저하
          청사진에 비동기 쓰기 언급 없음

### Step 2: 영향 범위 파악
**영향받는 문서**:
- Stage 4: `04D-01_dna_logging_blueprint.md` (청사진 수정 필요)
- Stage 3: `03A-401_dna_logging.md` (ADR 확인 - 수정 불필요)

**영향받는 구현**:
- `src/core/logging/handlers.py` (재구현 필요)
- `tests/core/logging/test_handlers.py` (재작성 필요)

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
```

### Step 4: 중간 Stage 전파
Stage 5 진행 중이므로 즉시 반영

### Step 5: 현재 Stage 재진행
```bash
# Stage 5 Logging 재구현
$ rm src/core/logging/handlers.py
$ rm tests/core/logging/test_handlers.py

$ implement src/core/logging/handlers.py
  # 비동기 파일 쓰기 구현
  import aiofiles

  class AsyncFileHandler:
      async def write(self, msg: str) -> None:
          async with aiofiles.open(self.path, "a") as f:
              await f.write(msg)

$ implement tests/core/logging/test_handlers.py
  # 비동기 테스트
  @pytest.mark.asyncio
  async def test_async_file_handler_writes():
      handler = AsyncFileHandler("/tmp/test.log")
      await handler.write("test message")

      async with aiofiles.open("/tmp/test.log", "r") as f:
          content = await f.read()

      assert "test message" in content
```

### Step 6: 재진행 결과 검증
```bash
$ mypy src/core/logging/
  → Success: no issues found ✅

$ ruff check src/core/logging/
  → All checks passed! ✅

$ pytest tests/core/logging/ --cov
  → Coverage: 97% ✅

**검증 항목**:
- [ ] 청사진 v1.1 반영 확인
- [ ] 비동기 쓰기 구현 완료
- [ ] aiofiles 의존성 추가
- [ ] 품질 게이트 통과 (ruff 0, mypy 0)
- [ ] 테스트 커버리지 95%+
- [ ] 추적성 명시 (Ref: 04D-01 v1.1)
```
```

#### 추적성 (Traceability) 유지

**모든 수정은 명시적으로 참조**:

```python
# src/core/logging/handlers.py
"""비동기 파일 핸들러.

Ref: 04D-01_dna_logging_blueprint.md v1.1 (Line 67-89)
Updated: 2024-11-12 (비동기 쓰기로 변경)

Reason: 동기 쓰기 성능 저하 → 비동기 쓰기 필요
"""
import aiofiles
from typing import Any

class AsyncFileHandler:
    """비동기 파일 핸들러."""

    async def write(self, msg: str) -> None:
        """메시지를 비동기로 파일에 쓴다."""
        async with aiofiles.open(self.path, "a") as f:
            await f.write(msg)
```

```markdown
## Stage 4 청사진 (04D-01_dna_logging_blueprint.md)
> **History**:
> - v1.0 (2024-11-10): 초기 청사진
> - v1.1 (2024-11-12): 비동기 쓰기 추가 (Stage 5에서 성능 이슈 발견)

Line 67: ## 파일 핸들러
Line 68: **전략**: 비동기 쓰기
Line 69: **라이브러리**: aiofiles==23.2.1
Line 70: **Ref**: Stage 5 구현 중 성능 이슈 발견
```

---

## 🎯 DNA 원칙 적용 요약 (Stage 5)

| 원칙 | Stage 5 적용 방법 | 체크포인트 |
|------|------------------|-----------|
| **1. AI 최적 크기** | 시스템별 순차 구현 (1개/세션) | Database만 2 sessions |
| **2. 완전해질 때까지** | 7개 항목 완전성, Zero-Tolerance | ruff 0, mypy 0, coverage 95%+ |
| **3. 기능별 분해** | Database 시스템만 분해 (Protocol + Mock + 조립) | Protocol 정의 필수 |
| **4. 역방향 수정** | 6단계 프로토콜, 추적성 유지 | Ref + Updated 명시 |

---

## 🤔 왜 DNA 구현이 필요한가?

### 청사진 vs 구현

```
Stage 4 청사진:
├─ "무엇을" 만들 것인지 설계
├─ 디렉토리 구조, 파일 목록
├─ 공개 API 정의
└─ 문서 (Markdown)

Stage 5 구현:
├─ "실제로" 코드 작성
├─ src/core/ 모듈 구현
├─ 테스트 작성
└─ 코드 (Python/TypeScript)

비유:
├─ 청사진 = 건축 도면
└─ 구현 = 실제 건설
```

### DNA 없이 도메인 구현하면?

```
❌ DNA 없이 도메인부터 구현:

domain/orders/service.py:
────────────────────────────────
import logging  # 표준 라이브러리 직접 사용
logger = logging.getLogger(__name__)

class OrderService:
    def create_order(self, data):
        print(f"Creating order: {data}")  # print 사용
        # 에러 처리 없음
        # 타입 힌트 없음
        db.execute("INSERT INTO orders ...")  # 직접 SQL

결과:
├─ 로깅 형식 불일치 (JSON vs Console)
├─ print()와 logger 혼재
├─ 에러 처리 누락
├─ 타입 안전성 없음
└─ 테스트 불가능한 코드
```

```
✅ DNA 먼저 구현 후 도메인:

domain/orders/service.py:
────────────────────────────────
from core.logging import get_logger
from core.errors import ValidationError, NotFoundError
from core.types import OrderId, UserId
from core.database import get_session

logger = get_logger(__name__)

class OrderService:
    async def create_order(self, data: CreateOrderRequest) -> OrderId:
        logger.info("주문 생성", user_id=data.user_id)
        
        if not data.items:
            raise ValidationError("주문 항목이 비어있습니다")
        
        async with get_session() as session:
            order = Order(**data.dict())
            session.add(order)
            await session.commit()
            
        return order.id

결과:
├─ 일관된 로깅 (JSON, trace_id 포함)
├─ 표준화된 에러 처리
├─ 타입 안전성
├─ 테스트 가능한 코드
└─ DNA가 "환경"으로 보호
```

---

## 📥 입력 문서

### Stage 4에서 전달받는 것

| 파일 | 핵심 내용 | 이 Stage에서 사용 |
|------|----------|-----------------|
| `04B-01_dna_blueprint.md` | DNA 시스템 청사진 | 구현 명세 |
| `03A-401~499_*.md` | DNA 시스템 ADR | 기술 선택 근거 |

---

## 📤 출력 문서

### 필수 산출물

```
src/core/                          # 구현된 DNA 모듈
├── __init__.py
├── logging/
├── config/
├── types/
├── errors/
├── database/
├── cache/
└── security/

tests/                             # DNA 테스트
├── unit/core/
│   ├── test_logging.py
│   ├── test_config.py
│   └── ...
└── integration/core/
    └── test_database.py

docs/
└── 05D-01_dna_implementation.md   # 구현 완료 문서
```

---


## 🔧 DNA 구현 3대 원칙

### 원칙 1: 표준 라이브러리 우선

```
❌ 직접 구현 (V5 실패 사례):
────────────────────────────────
# 89개 타입 클래스, 1,679줄...
class MyString:
    def __init__(self, value: str):
        self.value = value
    def validate(self):
        if not isinstance(self.value, str):
            raise TypeError("...")

✅ 표준 라이브러리:
────────────────────────────────
from pydantic import BaseModel, Field

class UserName(BaseModel):
    value: str = Field(min_length=1, max_length=100)

# 3줄로 해결!
```

**DNA별 표준 라이브러리**:

| DNA 시스템 | 표준 라이브러리 | 직접 구현 금지 |
|-----------|---------------|--------------|
| Logging | `structlog` | print(), logging 직접 사용 |
| Config | `pydantic-settings` | os.environ 직접 접근 |
| Types | `pydantic` | 커스텀 타입 클래스 |
| Errors | `pydantic` | 일반 Exception 상속 |
| Database | `sqlalchemy` | 직접 SQL 문자열 |
| Cache | `redis` | 직접 소켓 통신 |
| Testing | `pytest` | unittest 사용 |

### 원칙 2: 인터페이스 추상화

```python
# core/cache/interface.py
────────────────────────────────
from typing import Protocol, Any

class CacheInterface(Protocol):
    """캐시 인터페이스 - 구현체 교체 가능"""
    
    async def get(self, key: str) -> Any | None: ...
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None: ...
    async def delete(self, key: str) -> None: ...


# core/cache/redis.py
────────────────────────────────
class RedisCache:
    """Redis 구현체"""
    
    async def get(self, key: str) -> Any | None:
        return await self.client.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        await self.client.setex(key, ttl, value)


# 나중에 Memcached로 교체 가능!
# core/cache/memcached.py
class MemcachedCache:
    async def get(self, key: str) -> Any | None:
        return await self.client.get(key)
```

**가치**:
- 테스트 시 Mock 주입 용이
- 기술 교체 시 도메인 코드 변경 없음
- 의존성 역전 원칙 (DIP) 준수

### 원칙 3: 설정 주입 (환경별 분리)

```python
# core/config/settings.py
────────────────────────────────
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """환경별 설정 - .env 파일에서 로드"""
    
    # 데이터베이스
    database_url: str = "postgresql://localhost/dev"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # 로깅
    log_level: str = "INFO"
    log_format: str = "json"  # json | console
    
    # 환경
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# 사용
settings = Settings()
logger.info("DB 연결", url=settings.database_url)
```

**환경별 .env 파일**:

```bash
# .env.development
DATABASE_URL=postgresql://localhost/dev
LOG_LEVEL=DEBUG
LOG_FORMAT=console

# .env.production
DATABASE_URL=postgresql://prod-db:5432/prod
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

## 📋 구현 단계 (Part 1-4)

### Part 1: 프로젝트 구조 생성 (30분)

#### Step 1: 디렉토리 생성

```bash
# Stage 4 청사진 기반 디렉토리 생성
mkdir -p src/core/{logging,config,types,errors,database,cache,security}
mkdir -p tests/unit/core
mkdir -p tests/integration/core

# __init__.py 생성
touch src/__init__.py
touch src/core/__init__.py
touch src/core/{logging,config,types,errors,database,cache,security}/__init__.py
```

#### Step 2: 의존성 설치

```bash
# pyproject.toml에 DNA 의존성 추가
uv add pydantic pydantic-settings structlog sqlalchemy redis pytest pytest-cov pytest-asyncio

# 개발 의존성
uv add --dev ruff mypy pre-commit
```

#### Step 3: 기본 설정 파일

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "T201"]  # T201 = print 금지

[tool.mypy]
strict = true
warn_return_any = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = "--cov=src --cov-fail-under=95"
```

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

### Part 3: 각 DNA 시스템 구현

#### 3.1 Types 시스템 (첫 번째)

**파일 구조**:
```
src/core/types/
├── __init__.py      # 공개 API export
├── base.py          # BaseModel 확장
├── ids.py           # ID 타입 (UserId, OrderId)
└── common.py        # 공통 타입 (Email, Money)
```

**구현 코드**:

```python
# src/core/types/__init__.py
"""DNA Types - 타입 안전성의 기반"""

from .base import BaseEntity, BaseValueObject
from .ids import UserId, OrderId, ProductId
from .common import Email, Money, PhoneNumber

__all__ = [
    "BaseEntity",
    "BaseValueObject",
    "UserId",
    "OrderId",
    "ProductId",
    "Email",
    "Money",
    "PhoneNumber",
]
```

```python
# src/core/types/ids.py
"""ID 타입 정의 - UUID 기반 타입 안전 ID"""

from typing import NewType
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# NewType으로 타입 구분 (런타임 비용 없음)
UserId = NewType("UserId", UUID)
OrderId = NewType("OrderId", UUID)
ProductId = NewType("ProductId", UUID)


def generate_user_id() -> UserId:
    """새 UserId 생성"""
    return UserId(uuid4())


def generate_order_id() -> OrderId:
    """새 OrderId 생성"""
    return OrderId(uuid4())
```

```python
# src/core/types/common.py
"""공통 값 객체 - 자체 검증 포함"""

from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, field_validator


class Email(BaseModel):
    """이메일 값 객체"""
    value: EmailStr
    
    def __str__(self) -> str:
        return self.value


class Money(BaseModel):
    """금액 값 객체 - 정밀 계산"""
    amount: Decimal = Field(ge=0)
    currency: str = Field(default="KRW", pattern="^[A-Z]{3}$")
    
    @field_validator("amount", mode="before")
    @classmethod
    def round_amount(cls, v: Decimal | float | int) -> Decimal:
        """소수점 2자리로 반올림"""
        return Decimal(str(v)).quantize(Decimal("0.01"))
    
    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("통화가 다릅니다")
        return Money(amount=self.amount + other.amount, currency=self.currency)
```

**테스트**:

```python
# tests/unit/core/test_types.py
"""Types DNA 테스트"""

import pytest
from decimal import Decimal

from src.core.types import UserId, Email, Money, generate_user_id


class TestUserId:
    def test_generate_unique(self):
        """UserId는 매번 고유해야 함"""
        id1 = generate_user_id()
        id2 = generate_user_id()
        assert id1 != id2


class TestEmail:
    def test_valid_email(self):
        """유효한 이메일 검증"""
        email = Email(value="test@example.com")
        assert str(email) == "test@example.com"
    
    def test_invalid_email_raises(self):
        """유효하지 않은 이메일은 예외"""
        with pytest.raises(ValueError):
            Email(value="invalid-email")


class TestMoney:
    def test_addition(self):
        """같은 통화 덧셈"""
        m1 = Money(amount=Decimal("100.00"))
        m2 = Money(amount=Decimal("50.00"))
        result = m1 + m2
        assert result.amount == Decimal("150.00")
    
    def test_different_currency_raises(self):
        """다른 통화 덧셈은 예외"""
        krw = Money(amount=Decimal("1000"), currency="KRW")
        usd = Money(amount=Decimal("10"), currency="USD")
        with pytest.raises(ValueError):
            krw + usd
```



#### 3.2 Config 시스템 (두 번째)

**파일 구조**:
```
src/core/config/
├── __init__.py      # 공개 API export
├── settings.py      # 환경 설정
└── validators.py    # 커스텀 검증
```

**구현 코드**:

```python
# src/core/config/__init__.py
"""DNA Config - 환경별 설정 관리"""

from .settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]


# 싱글톤 인스턴스
_settings: Settings | None = None


def get_settings() -> Settings:
    """설정 싱글톤 반환"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

```python
# src/core/config/settings.py
"""환경 설정 - pydantic-settings 기반"""

from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 환경
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    # 데이터베이스
    database_url: str = Field(default="postgresql://localhost/dev")
    database_pool_size: int = Field(default=5, ge=1, le=20)
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379")
    redis_ttl: int = Field(default=3600, ge=60)
    
    # 로깅
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    
    # 외부 API (예: KIS)
    kis_app_key: str = Field(default="")
    kis_app_secret: str = Field(default="")
    kis_rate_limit: int = Field(default=15)  # 초당 요청 수
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """로그 레벨 검증"""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level은 {valid_levels} 중 하나여야 합니다")
        return v.upper()
    
    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """로그 포맷 검증"""
        if v not in {"json", "console"}:
            raise ValueError("log_format은 'json' 또는 'console'이어야 합니다")
        return v
    
    @property
    def is_production(self) -> bool:
        """운영 환경 여부"""
        return self.environment == "production"
```

#### 3.3 Logging 시스템 (세 번째)

**파일 구조**:
```
src/core/logging/
├── __init__.py      # 공개 API export
├── logger.py        # structlog 설정
├── config.py        # 로깅 설정
└── processors.py    # 커스텀 프로세서
```

**구현 코드**:

```python
# src/core/logging/__init__.py
"""DNA Logging - 구조화된 로깅"""

from .logger import get_logger, configure_logging

__all__ = ["get_logger", "configure_logging"]
```

```python
# src/core/logging/logger.py
"""structlog 기반 로거"""

import structlog
from typing import Any

from src.core.config import get_settings


def configure_logging() -> None:
    """로깅 초기 설정 - 앱 시작 시 1회 호출"""
    settings = get_settings()
    
    # 공통 프로세서
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    if settings.log_format == "json":
        # 운영: JSON 포맷
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(structlog, settings.log_level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # 개발: 컬러 콘솔
        structlog.configure(
            processors=shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True)
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(structlog, settings.log_level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """로거 인스턴스 반환"""
    return structlog.get_logger(name)


# 컨텍스트 바인딩 헬퍼
def bind_context(**kwargs: Any) -> None:
    """요청 컨텍스트 바인딩 (trace_id, user_id 등)"""
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """컨텍스트 초기화"""
    structlog.contextvars.clear_contextvars()
```

**사용 예시**:

```python
# 앱 시작 시
from src.core.logging import configure_logging, get_logger, bind_context

configure_logging()
logger = get_logger(__name__)

# 요청 처리 시
bind_context(trace_id="abc-123", user_id="user-456")
logger.info("주문 생성", order_id="order-789", amount=50000)

# 출력 (JSON):
# {"event": "주문 생성", "trace_id": "abc-123", "user_id": "user-456", 
#  "order_id": "order-789", "amount": 50000, "level": "info", 
#  "timestamp": "2025-12-03T10:30:00Z"}
```

#### 3.4 Errors 시스템 (네 번째)

**파일 구조**:
```
src/core/errors/
├── __init__.py      # 공개 API export
├── exceptions.py    # 예외 계층
├── codes.py         # 에러 코드
└── handlers.py      # 전역 핸들러
```

**구현 코드**:

```python
# src/core/errors/__init__.py
"""DNA Errors - 표준화된 예외 처리"""

from .exceptions import (
    AppError,
    DomainError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ExternalError,
    KISAPIError,
)
from .codes import ErrorCode
from .handlers import global_exception_handler

__all__ = [
    "AppError",
    "DomainError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "ExternalError",
    "KISAPIError",
    "ErrorCode",
    "global_exception_handler",
]
```

```python
# src/core/errors/codes.py
"""에러 코드 정의"""

from enum import Enum


class ErrorCode(str, Enum):
    """에러 코드 체계
    
    1xxx: 도메인 에러 (비즈니스 로직)
    2xxx: 외부 API 에러
    9xxx: 시스템 에러
    """
    
    # 1xxx: 도메인
    VALIDATION_ERROR = "1001"
    NOT_FOUND = "1002"
    CONFLICT = "1003"
    INSUFFICIENT_BALANCE = "1004"
    ORDER_ALREADY_CANCELLED = "1005"
    
    # 2xxx: 외부 API
    KIS_API_ERROR = "2001"
    KIS_RATE_LIMIT = "2002"
    KIS_AUTH_FAILED = "2003"
    
    # 9xxx: 시스템
    INTERNAL_ERROR = "9001"
    DATABASE_ERROR = "9002"
    CACHE_ERROR = "9003"
```

```python
# src/core/errors/exceptions.py
"""예외 계층 정의"""

from typing import Any
from .codes import ErrorCode


class AppError(Exception):
    """애플리케이션 최상위 예외"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict[str, Any]:
        """API 응답용 딕셔너리"""
        return {
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details,
            }
        }


class DomainError(AppError):
    """도메인 에러 (비즈니스 로직 위반)"""
    pass


class ValidationError(DomainError):
    """검증 에러"""
    
    def __init__(self, message: str, field: str | None = None):
        details = {"field": field} if field else {}
        super().__init__(message, ErrorCode.VALIDATION_ERROR, details)


class NotFoundError(DomainError):
    """리소스 없음"""
    
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            f"{resource}을(를) 찾을 수 없습니다: {identifier}",
            ErrorCode.NOT_FOUND,
            {"resource": resource, "identifier": identifier},
        )


class ConflictError(DomainError):
    """충돌 에러"""
    
    def __init__(self, message: str):
        super().__init__(message, ErrorCode.CONFLICT)


class ExternalError(AppError):
    """외부 API 에러"""
    pass


class KISAPIError(ExternalError):
    """KIS API 에러"""
    
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(
            message,
            ErrorCode.KIS_API_ERROR,
            {"status_code": status_code},
        )
```

```python
# src/core/errors/handlers.py
"""전역 예외 핸들러"""

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logging import get_logger
from .exceptions import AppError

logger = get_logger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """전역 예외 핸들러 - FastAPI용"""
    
    if isinstance(exc, AppError):
        # 예상된 에러 (도메인, 외부 API)
        logger.warning(
            "예상된 에러",
            error_code=exc.code.value,
            message=exc.message,
            details=exc.details,
        )
        status_code = _get_status_code(exc)
        return JSONResponse(status_code=status_code, content=exc.to_dict())
    
    # 예상치 못한 에러
    logger.exception("예상치 못한 에러", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "9001",
                "message": "내부 서버 오류가 발생했습니다",
            }
        },
    )


def _get_status_code(exc: AppError) -> int:
    """에러 코드에 따른 HTTP 상태 코드"""
    mapping = {
        "1001": 400,  # ValidationError
        "1002": 404,  # NotFoundError
        "1003": 409,  # ConflictError
        "2001": 502,  # KISAPIError
        "2002": 429,  # RateLimitError
    }
    return mapping.get(exc.code.value, 500)
```



### Part 4: 통합 검증

#### 4.1 DNA 통합 테스트

```python
# tests/integration/core/test_dna_integration.py
"""DNA 시스템 통합 테스트"""

import pytest
from src.core.config import get_settings
from src.core.logging import configure_logging, get_logger
from src.core.types import UserId, generate_user_id, Money
from src.core.errors import ValidationError, NotFoundError


class TestDNAIntegration:
    """DNA 시스템 간 통합 검증"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """테스트 전 로깅 설정"""
        configure_logging()
    
    def test_logging_uses_config(self):
        """Logging이 Config 설정을 사용"""
        settings = get_settings()
        logger = get_logger("test")
        
        # 설정된 로그 레벨 확인
        assert settings.log_level in {"DEBUG", "INFO", "WARNING", "ERROR"}
        logger.info("통합 테스트", environment=settings.environment)
    
    def test_errors_log_properly(self):
        """Errors가 Logging과 연동"""
        logger = get_logger("test")
        
        try:
            raise NotFoundError("Order", "order-123")
        except NotFoundError as e:
            logger.warning("리소스 없음", error=e.to_dict())
            assert e.code.value == "1002"
    
    def test_types_with_validation_error(self):
        """Types 검증 실패 시 적절한 에러"""
        with pytest.raises(ValueError):
            Money(amount=-100)  # 음수 금액 불가
```

#### 4.2 품질 검증 명령어

```bash
# 1. 타입 체크 (0 errors 필수)
mypy src/core --strict
# Expected: Success: no issues found

# 2. 린팅 (0 violations 필수)
ruff check src/core tests/
# Expected: All checks passed!

# 3. 포맷팅
ruff format src/core tests/

# 4. 테스트 + 커버리지 (95%+ 필수)
pytest tests/unit/core tests/integration/core --cov=src/core --cov-fail-under=95
# Expected: PASSED, Coverage 95%+

# 5. 전체 검증 (CI 파이프라인)
make lint test  # 또는
./scripts/validate.sh
```

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
MyPy:     0 errors ✅
Ruff:     0 violations ✅
pytest:   45 passed, 0 failed ✅
Coverage: 96% (목표: 95%) ✅
```

## 2. 디렉토리 구조

```
src/core/
├── __init__.py         # DNA 공개 API
├── logging/
│   ├── __init__.py
│   ├── logger.py       # 285 lines
│   ├── config.py       # 45 lines
│   └── processors.py   # 62 lines
├── config/
│   ├── __init__.py
│   ├── settings.py     # 120 lines
│   └── validators.py   # 35 lines
├── types/
│   ├── __init__.py
│   ├── base.py         # 50 lines
│   ├── ids.py          # 40 lines
│   └── common.py       # 85 lines
├── errors/
│   ├── __init__.py
│   ├── exceptions.py   # 95 lines
│   ├── codes.py        # 45 lines
│   └── handlers.py     # 60 lines
└── database/
    ├── __init__.py
    ├── session.py      # 75 lines
    ├── base.py         # 55 lines
    └── mixins.py       # 40 lines
```

## 3. 공개 API

### 3.1 사용 예시

```python
# DNA 임포트
from core.logging import get_logger, configure_logging
from core.config import get_settings
from core.types import UserId, OrderId, Money
from core.errors import NotFoundError, ValidationError
from core.database import get_session

# 초기화
configure_logging()
settings = get_settings()
logger = get_logger(__name__)

# 사용
logger.info("서비스 시작", environment=settings.environment)

async with get_session() as session:
    # 데이터베이스 작업
    pass
```

## 4. Stage 6 전달 사항

### 4.1 Project Standards에 포함할 규칙

- [ ] `print()` 금지 → `get_logger()` 사용
- [ ] `os.environ` 금지 → `get_settings()` 사용
- [ ] 일반 `Exception` 금지 → `AppError` 계층 사용
- [ ] 직접 SQL 금지 → SQLAlchemy ORM 사용

### 4.2 자동화 설정

- [ ] pre-commit hooks 설정
- [ ] CI 파이프라인에 DNA 테스트 포함
- [ ] import-linter 규칙 추가
```

---

## ✏️ 구현 예시: 주식 거래 플랫폼

### 예시 1: Logging + Config 연동

**목표**: 환경별 로깅 설정 자동 적용

```python
# src/core/logging/logger.py (실제 구현)
"""주식 거래 플랫폼 로깅 설정"""

import structlog
from src.core.config import get_settings


def configure_logging() -> None:
    """환경별 로깅 설정
    
    - 개발: 컬러 콘솔, DEBUG
    - 스테이징: JSON, INFO
    - 운영: JSON, WARNING + CloudWatch
    """
    settings = get_settings()
    
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        # 거래 시스템 필수 컨텍스트
        add_trading_context,  # trace_id, user_id, account_id
    ]
    
    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def add_trading_context(
    logger: structlog.BoundLogger,
    method_name: str,
    event_dict: dict,
) -> dict:
    """거래 시스템 필수 컨텍스트 추가"""
    # trace_id가 없으면 생성
    if "trace_id" not in event_dict:
        import uuid
        event_dict["trace_id"] = str(uuid.uuid4())[:8]
    
    return event_dict
```

**테스트**:

```python
# tests/unit/core/test_logging.py

def test_production_uses_json(monkeypatch):
    """운영 환경에서 JSON 포맷 사용"""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_FORMAT", "json")
    
    configure_logging()
    logger = get_logger("test")
    
    # JSON 출력 확인 (캡처 후 파싱)
    # ...


def test_trading_context_added():
    """거래 컨텍스트 자동 추가"""
    configure_logging()
    logger = get_logger("trading")
    
    # trace_id 자동 생성 확인
    # ...
```

### 예시 2: Errors + Logging 연동

**목표**: 에러 발생 시 자동 로깅

```python
# src/core/errors/handlers.py (실제 구현)
"""주식 거래 플랫폼 에러 핸들러"""

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logging import get_logger
from .exceptions import AppError, KISAPIError

logger = get_logger("error_handler")


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """전역 예외 핸들러
    
    거래 시스템 특화:
    - 주문 실패는 CRITICAL 로깅
    - KIS API 에러는 WARNING + 상세 정보
    - 기타 에러는 ERROR
    """
    
    # 요청 컨텍스트 추출
    trace_id = request.headers.get("X-Trace-ID", "unknown")
    user_id = getattr(request.state, "user_id", "anonymous")
    
    if isinstance(exc, KISAPIError):
        # KIS API 에러 - 외부 서비스 문제
        logger.warning(
            "KIS API 에러",
            trace_id=trace_id,
            user_id=user_id,
            error_code=exc.code.value,
            message=exc.message,
            kis_status=exc.details.get("status_code"),
            path=request.url.path,
        )
        return JSONResponse(status_code=502, content=exc.to_dict())
    
    if isinstance(exc, AppError):
        # 예상된 비즈니스 에러
        log_level = "critical" if "order" in request.url.path else "warning"
        getattr(logger, log_level)(
            "비즈니스 에러",
            trace_id=trace_id,
            user_id=user_id,
            error_code=exc.code.value,
            message=exc.message,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=_get_status_code(exc),
            content=exc.to_dict(),
        )
    
    # 예상치 못한 에러 - 즉시 알림 필요
    logger.exception(
        "예상치 못한 에러",
        trace_id=trace_id,
        user_id=user_id,
        path=request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "9001",
                "message": "내부 서버 오류",
                "trace_id": trace_id,
            }
        },
    )
```

### 예시 3: 전체 DNA 연동 (주문 서비스)

**목표**: 모든 DNA 시스템이 도메인에서 어떻게 사용되는지

```python
# domain/orders/service.py (DNA 활용 예시)
"""주문 서비스 - DNA 시스템 활용"""

from src.core.logging import get_logger, bind_context
from src.core.config import get_settings
from src.core.types import OrderId, UserId, Money, generate_order_id
from src.core.errors import ValidationError, NotFoundError, KISAPIError
from src.core.database import get_session
from src.core.cache import cached

logger = get_logger(__name__)
settings = get_settings()


class OrderService:
    """주문 서비스"""
    
    async def create_order(
        self,
        user_id: UserId,
        symbol: str,
        quantity: int,
        price: Money,
    ) -> OrderId:
        """주문 생성
        
        DNA 활용:
        - Logging: 모든 단계 로깅
        - Types: 타입 안전한 파라미터
        - Errors: 표준화된 예외 처리
        - Database: 트랜잭션 관리
        - Cache: 시세 캐싱
        """
        order_id = generate_order_id()
        bind_context(order_id=str(order_id), user_id=str(user_id))
        
        logger.info("주문 생성 시작", symbol=symbol, quantity=quantity)
        
        # 1. 검증 (Errors DNA)
        if quantity <= 0:
            raise ValidationError("수량은 0보다 커야 합니다", field="quantity")
        
        if price.amount <= 0:
            raise ValidationError("가격은 0보다 커야 합니다", field="price")
        
        # 2. 현재가 조회 (Cache DNA)
        current_price = await self._get_current_price(symbol)
        
        # 3. 주문 저장 (Database DNA)
        async with get_session() as session:
            order = Order(
                id=order_id,
                user_id=user_id,
                symbol=symbol,
                quantity=quantity,
                price=price.amount,
                status="pending",
            )
            session.add(order)
            await session.commit()
            
            logger.info("주문 저장 완료", status="pending")
        
        # 4. KIS API 호출 (Config DNA - rate limit 설정)
        try:
            await self._submit_to_kis(order)
        except KISAPIError as e:
            logger.error("KIS 주문 실패", error=str(e))
            raise
        
        logger.info("주문 생성 완료")
        return order_id
    
    @cached(ttl=5)  # 5초 캐싱
    async def _get_current_price(self, symbol: str) -> Money:
        """현재가 조회 (캐싱)"""
        # KIS API 호출
        # ...
        pass
```

---

## ✅ Stage 5 완료 체크리스트

### 구조 검증

- [ ] src/core/ 디렉토리 생성됨
- [ ] 각 DNA 시스템 하위 디렉토리 존재
- [ ] tests/unit/core/ 테스트 디렉토리 존재
- [ ] tests/integration/core/ 통합 테스트 존재

### 필수 DNA 구현 (5개)

- [ ] **Types**: ids.py, common.py 구현
- [ ] **Config**: settings.py 구현, 환경별 분리
- [ ] **Logging**: structlog 설정, get_logger() 동작
- [ ] **Errors**: 예외 계층, 에러 코드 정의
- [ ] **Testing**: pytest 설정, 커버리지 95%+

### 패밀리별 추가 DNA

- [ ] **Database** (A-A-B 필수): SQLAlchemy 세션 관리
- [ ] **Cache** (A-A-B 권장): Redis 클라이언트
- [ ] **Security** (A-A-B 필수): 인증/인가 미들웨어

### 품질 검증

- [ ] MyPy 0 errors: `mypy src/core --strict`
- [ ] Ruff 0 violations: `ruff check src/core`
- [ ] 테스트 통과: `pytest tests/unit/core tests/integration/core`
- [ ] 커버리지 95%+: `--cov-fail-under=95`

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

| 전달 항목 | 내용 | 용도 |
|----------|------|------|
| 구현된 DNA 모듈 | src/core/ | 프로젝트 표준의 기반 |
| 금지 규칙 | print(), os.environ 등 | PROJECT_STANDARDS.md 작성 |
| 자동화 설정 | pyproject.toml, pre-commit | 강제 규칙 설정 |

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

| Stage | 산출물 | 검증 항목 |
|-------|--------|----------|
| Stage 1 | 01C-01_*.md | 구현 수준이 NFR 만족? |
| Stage 2 | 02C-01_*.md | 기술 제약 내에서 구현? |
| Stage 3 | 03A-*_*.md | ADR 결정대로 구현? |
| Stage 4 | 04B-01_*.md | DNA 청사진대로 구현? |

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

| 오류 유형 | 예시 | 해결 |
|----------|------|------|
| 청사진 불완전 | 인터페이스 정의 누락 | Stage 4 청사진 보완 |
| ADR 미반영 | 로깅 포맷 ADR과 구현 불일치 | 구현 수정 또는 ADR 갱신 |
| 의존성 오류 | 순환 의존성 발생 | Stage 4 설계 재검토 |

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
✅ pydantic, structlog, sqlalchemy (3줄)

2. 인터페이스 추상화
────────────────────────────────
Protocol 정의 → 구현체 교체 가능
테스트 시 Mock 주입 용이

3. 설정 주입
────────────────────────────────
pydantic-settings로 환경별 분리
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
MyPy:     0 errors    (타입 안전성)
Ruff:     0 violations (코드 품질)
pytest:   0 failures  (기능 정확성)
Coverage: 95%+        (테스트 충분성)
```

---

**Remember**: 
- DNA 없이 도메인 구현 = 기반 없는 건물
- 표준 라이브러리 우선 = 바퀴 재발명 금지
- 의존성 순서 준수 = Types → Config → Logging → Errors
- Kent Beck 수준 = 10/11개 DNA 동작

*DNA가 "환경"으로 구축되어야 도메인 코드가 그 위에서 안전하게 실행됩니다.*
