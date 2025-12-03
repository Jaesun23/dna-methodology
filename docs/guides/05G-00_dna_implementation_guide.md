# Stage 5: DNA 시스템 구현 가이드 (DNA Implementation Guide)

> **목적**: Stage 4 청사진 기반으로 src/core/ DNA 시스템 실제 구현
>
> **버전**: v5.0 (2025-12-03)
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
